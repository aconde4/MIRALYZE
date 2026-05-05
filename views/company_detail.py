"""
Individual company view with historical data, charts and sector benchmark.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from database.db_manager import execute_query
from utils.helpers import format_euros, format_pct
from utils.theme import (
    COLORS, PLOTLY_BAR_ALPHA, get_combo_layout, get_plotly_layout,
    get_score_color,
)


def render():
    st.title("Ficha de empresa")

    company_id = st.session_state.get("selected_company_id")
    if not company_id:
        st.info("Selecciona una empresa desde el listado.")
        return

    company = execute_query("SELECT * FROM companies WHERE id = %s", (company_id,))
    if not company:
        st.error("Empresa no encontrada.")
        return
    company = company[0]

    st.markdown(f"### {company['company_name']}")
    _render_company_header(company)

    data = execute_query(
        """SELECT f.year, f.revenue, f.ebitda, f.net_income, f.total_assets,
                  f.equity, f.employees, f.working_capital, f.cost_of_goods_sold,
                  f.cash_flow, f.long_term_debts, f.short_term_debts,
                  m.gross_debt, m.net_debt, m.ebitda_margin, m.net_income_margin,
                  m.cash_flow_margin, m.revenue_growth_yoy, m.ebitda_growth_yoy,
                  m.net_debt_ebitda, m.revenue_per_employee,
                  m.ebitda_per_employee, m.cash_conversion, m.equity_ratio
           FROM financials f
           LEFT JOIN metrics m ON f.company_id = m.company_id AND f.year = m.year
           WHERE f.company_id = %s
           ORDER BY f.year""",
        (company_id,),
    )

    if not data:
        st.warning("No hay datos financieros para esta empresa.")
        return

    df = pd.DataFrame(data)
    years = df["year"].tolist()
    st.caption(f"Años disponibles: {min(years)} - {max(years)}. Importes en miles EUR.")

    _render_historical_table(df)
    _render_historical_charts(df)

    st.subheader("Benchmark sectorial (CNAE)")
    _render_benchmark(company_id, company["cnae_code"], df)

    st.subheader("Score global")
    _render_score_circle(company_id, int(df["year"].max()))


def _render_company_header(company: dict):
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"**CIF:** {company.get('cif') or '-'}")
    col2.markdown(f"**BvD ID:** {company.get('bvd_id') or '-'}")
    col3.markdown(f"**País:** {company.get('country') or '-'}")
    col4.markdown(f"**CNAE:** {company.get('cnae_code') or '-'}")

    col5, col6, col7, col8 = st.columns(4)
    col5.markdown(f"**Provincia:** {company.get('province') or '-'}")
    col6.markdown(f"**Web:** {_format_website(company.get('website'))}")
    col7.markdown(f"**Constitución:** {company.get('date_of_establishment') or '-'}")
    col8.markdown(f"**GUO:** {company.get('guo_name') or '-'}")

    short_desc = company.get("native_trade_description")
    long_desc = company.get("english_trade_description")
    if short_desc:
        st.markdown(f"**Actividad:** {short_desc}")
    if long_desc:
        with st.expander("Descripción larga"):
            st.write(long_desc)


def _format_website(website):
    if not website:
        return "-"
    url = website if str(website).startswith(("http://", "https://")) else f"https://{website}"
    return f"[{website}]({url})"


def _render_historical_table(df: pd.DataFrame):
    st.subheader("Datos históricos")
    df_display = df.copy()

    money_cols = [
        "revenue", "ebitda", "net_income", "total_assets", "equity",
        "working_capital", "cost_of_goods_sold", "cash_flow",
        "long_term_debts", "short_term_debts", "gross_debt", "net_debt",
    ]
    for col in money_cols:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(format_euros)

    pct_cols = [
        "ebitda_margin", "net_income_margin", "cash_flow_margin",
        "revenue_growth_yoy", "ebitda_growth_yoy", "equity_ratio",
        "cash_conversion",
    ]
    for col in pct_cols:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(format_pct)

    st.dataframe(df_display, use_container_width=True, hide_index=True)


def _render_historical_charts(df: pd.DataFrame):
    st.subheader("Evolución histórica")
    g1, g2 = st.columns(2)

    with g1:
        fig = _combo_chart(
            df, "year", "revenue", "revenue_per_employee",
            title="Turnover & Revenue por Empleado",
            bar_label="Revenue (miles EUR)",
            line_label="Revenue / Empleado (miles EUR)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with g2:
        df_eb = df.copy()
        df_eb["ebitda_margin_pct"] = df_eb["ebitda_margin"].apply(
            lambda x: x * 100 if pd.notna(x) else None
        )
        fig = _combo_chart(
            df_eb, "year", "ebitda", "ebitda_margin_pct",
            title="EBITDA & Margen EBITDA",
            bar_label="EBITDA (miles EUR)",
            line_label="Margen EBITDA (%)",
        )
        st.plotly_chart(fig, use_container_width=True)

    g3, g4 = st.columns(2)

    with g3:
        fig = _combo_chart(
            df, "year", "net_debt", "net_debt_ebitda",
            title="Deuda Neta & ND/EBITDA",
            bar_label="Deuda Neta (miles EUR)",
            line_label="ND / EBITDA (x)",
            bar_color=PLOTLY_BAR_ALPHA["crimson"],
            line_color=COLORS["sapphire"],
        )
        st.plotly_chart(fig, use_container_width=True)

    with g4:
        df_ni = df.copy()
        df_ni["net_margin_pct"] = df_ni["net_income_margin"].apply(
            lambda x: x * 100 if pd.notna(x) else None
        )
        fig = _combo_chart(
            df_ni, "year", "net_income", "net_margin_pct",
            title="Resultado Neto & Margen Neto",
            bar_label="Net Income (miles EUR)",
            line_label="Margen Neto (%)",
            bar_color=PLOTLY_BAR_ALPHA["navy"],
            line_color=COLORS["gold"],
        )
        st.plotly_chart(fig, use_container_width=True)

    g5, g6 = st.columns(2)

    with g5:
        df_cf = df.copy()
        df_cf["cash_conversion_pct"] = df_cf["cash_conversion"].apply(
            lambda x: x * 100 if pd.notna(x) else None
        )
        fig = _combo_chart(
            df_cf, "year", "cash_flow", "cash_conversion_pct",
            title="Cash Flow & Cash Conversion",
            bar_label="Cash Flow (miles EUR)",
            line_label="Cash Conversion (%)",
            bar_color=PLOTLY_BAR_ALPHA["emerald"],
            line_color=COLORS["gold"],
        )
        st.plotly_chart(fig, use_container_width=True)

    with g6:
        _render_capital_structure(df)


def _render_capital_structure(df: pd.DataFrame):
    df_cap = df.copy()
    df_cap["equity_ratio_pct"] = df_cap["equity_ratio"].apply(
        lambda x: x * 100 if pd.notna(x) else None
    )
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_cap["year"], y=df_cap["equity"], name="Equity",
        marker_color=PLOTLY_BAR_ALPHA["sapphire"],
        marker_line_color=COLORS["sapphire"], marker_line_width=1,
    ))
    fig.add_trace(go.Bar(
        x=df_cap["year"], y=df_cap["net_debt"], name="Deuda Neta",
        marker_color=PLOTLY_BAR_ALPHA["crimson"],
        marker_line_color=COLORS["crimson"], marker_line_width=1,
    ))
    fig.add_trace(go.Scatter(
        x=df_cap["year"], y=df_cap["equity_ratio_pct"],
        name="Equity Ratio (%)", mode="lines+markers",
        line=dict(color=COLORS["gold"], width=3),
        marker=dict(size=7, color=COLORS["gold"]),
        yaxis="y2",
    ))
    fig.update_layout(
        **get_combo_layout(
            title="Equity vs Deuda Neta",
            bar_label="miles EUR",
            line_label="Equity Ratio (%)",
            height=450,
        ),
        barmode="stack",
    )
    st.plotly_chart(fig, use_container_width=True)


def _combo_chart(df, x_col, bar_col, line_col, title, bar_label, line_label,
                 bar_color=None, line_color=None):
    bar_color = bar_color or PLOTLY_BAR_ALPHA["sapphire"]
    line_color = line_color or COLORS["gold"]
    bar_border = COLORS["sapphire"]
    for key, alpha_val in PLOTLY_BAR_ALPHA.items():
        if alpha_val == bar_color:
            bar_border = COLORS[key]
            break

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[x_col], y=df[bar_col], name=bar_label,
        marker_color=bar_color, marker_line_color=bar_border,
        marker_line_width=1,
    ))
    fig.add_trace(go.Scatter(
        x=df[x_col], y=df[line_col], name=line_label, mode="lines+markers",
        line=dict(color=line_color, width=3),
        marker=dict(size=7, color=line_color),
        yaxis="y2",
    ))
    fig.update_layout(**get_combo_layout(
        title=title, bar_label=bar_label, line_label=line_label, height=450,
    ))
    return fig


def _render_benchmark(company_id: int, cnae_code: str, df_company: pd.DataFrame):
    sector_data = execute_query(
        """SELECT m.year,
                  AVG(m.ebitda_margin) AS median_ebitda_margin,
                  AVG(m.revenue_growth_yoy) AS median_revenue_growth
           FROM metrics m
           JOIN companies c ON m.company_id = c.id
           WHERE c.cnae_code = %s AND m.company_id != %s
           GROUP BY m.year
           ORDER BY m.year""",
        (cnae_code, company_id),
    )

    if not sector_data:
        st.info("No hay suficientes empresas del mismo CNAE para comparar.")
        return

    df_sector = pd.DataFrame(sector_data)
    df_cmp = df_company[["year", "ebitda_margin", "revenue_growth_yoy"]].merge(
        df_sector, on="year", how="inner",
    )

    if df_cmp.empty:
        st.info("No hay años coincidentes para la comparación sectorial.")
        return

    col1, col2 = st.columns(2)
    with col1:
        _benchmark_bar(
            df_cmp, "ebitda_margin", "median_ebitda_margin",
            "Margen EBITDA vs Sector (%)",
        )
    with col2:
        _benchmark_bar(
            df_cmp, "revenue_growth_yoy", "median_revenue_growth",
            "Crecimiento Revenue vs Sector (%)",
        )


def _benchmark_bar(df_cmp, company_col, sector_col, title):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Empresa", x=df_cmp["year"],
        y=df_cmp[company_col].apply(lambda x: x * 100 if pd.notna(x) else None),
        marker_color=PLOTLY_BAR_ALPHA["sapphire"],
        marker_line_color=COLORS["sapphire"], marker_line_width=1,
    ))
    fig.add_trace(go.Bar(
        name="Media sector", x=df_cmp["year"],
        y=df_cmp[sector_col].apply(lambda x: x * 100 if pd.notna(x) else None),
        marker_color=PLOTLY_BAR_ALPHA["gold"],
        marker_line_color=COLORS["gold"], marker_line_width=1,
    ))
    fig.update_layout(**get_plotly_layout(
        title=dict(
            text=title,
            font=dict(color=COLORS["ivory"], size=14, weight=600),
            x=0.02, xanchor="left",
        ),
        barmode="group",
        height=420,
        margin=dict(l=55, r=30, t=60, b=80),
    ))
    fig.update_yaxes(title_text="%", title_font=dict(color=COLORS["steel"], size=11))
    st.plotly_chart(fig, use_container_width=True)


def _render_score_circle(company_id: int, latest_year: int):
    all_metrics = execute_query(
        """SELECT company_id, ebitda_margin, revenue_growth_yoy,
                  equity_ratio, ebitda_per_employee
           FROM metrics
           WHERE year = %s""",
        (latest_year,),
    )

    if not all_metrics:
        st.info("No hay suficientes datos para calcular el score.")
        return

    df_all = pd.DataFrame(all_metrics)

    def _norm(series: pd.Series) -> pd.Series:
        filled = series.fillna(series.median())
        min_v, max_v = filled.min(), filled.max()
        if max_v == min_v:
            return pd.Series(0.5, index=series.index)
        return (filled - min_v) / (max_v - min_v)

    df_all["_s_rent"] = _norm(df_all["ebitda_margin"])
    df_all["_s_crec"] = _norm(df_all["revenue_growth_yoy"])
    df_all["_s_solid"] = _norm(df_all["equity_ratio"])
    df_all["_s_efic"] = _norm(df_all["ebitda_per_employee"])
    df_all["score"] = (
        df_all["_s_rent"] + df_all["_s_crec"] +
        df_all["_s_solid"] + df_all["_s_efic"]
    ) / 4 * 100

    company_row = df_all[df_all["company_id"] == company_id]
    if company_row.empty:
        st.info("No hay métricas disponibles para calcular el score.")
        return

    score = float(company_row["score"].iloc[0])
    total = len(df_all)
    rank = int((df_all["score"] > score).sum()) + 1
    arc_color, rating = get_score_color(score)

    fig = go.Figure(go.Pie(
        values=[score, 100 - score],
        hole=0.72,
        marker_colors=[arc_color, "rgba(255,255,255,0.07)"],
        textinfo="none",
        showlegend=False,
        sort=False,
        direction="clockwise",
        rotation=90,
        hoverinfo="skip",
    ))
    fig.add_annotation(
        text=f"<b>{score:.0f}</b>", x=0.5, y=0.55,
        font=dict(size=56, color=COLORS["ivory"], family="Inter, sans-serif"),
        showarrow=False, xanchor="center",
    )
    fig.add_annotation(
        text=f"<span style='color:{COLORS['gold']}'>{rating}</span>",
        x=0.5, y=0.35, font=dict(size=18, family="Inter, sans-serif"),
        showarrow=False, xanchor="center",
    )
    fig.update_layout(height=320, margin=dict(t=20, b=20, l=20, r=20),
                      paper_bgcolor="rgba(0,0,0,0)")

    _, col_center, _ = st.columns([1, 1, 1])
    with col_center:
        st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f"Score calculado sobre {total} empresas con datos en {latest_year} · "
        f"Posición #{rank} de {total} · "
        "Dimensiones: Rentabilidad · Crecimiento · Solidez · Eficiencia"
    )
