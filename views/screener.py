"""
Advanced screener with filters, export, ranking chart and configurable scoring.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from database.db_manager import execute_query
from utils.helpers import (
    format_euros, get_available_cnaes, get_available_countries, get_available_years,
)
from utils.theme import COLORS, get_plotly_layout


PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}
TABLE_RESULT_LIMIT = 1000


def render():
    st.title("Screener")

    years = get_available_years()
    if not years:
        st.info("No hay datos disponibles. Carga un archivo primero.")
        return

    with st.sidebar:
        st.subheader("Filtros del screener")
        selected_year = st.selectbox("Año de análisis", years)
        selected_countries = st.multiselect("País", get_available_countries())
        selected_cnaes = st.multiselect("CNAE", get_available_cnaes())

        st.markdown("---")
        rev_min = st.number_input("Revenue mínimo (miles EUR)", min_value=0, value=0, step=100)
        rev_max = st.number_input(
            "Revenue máximo (miles EUR)", min_value=0, value=0, step=100,
            help="0 = sin límite",
        )
        ebitda_margin_min = st.slider("Margen EBITDA mínimo (%)", -100, 100, -100)
        rev_growth_min = st.slider("Crec. Revenue YoY mínimo (%)", -100, 200, -100)
        nd_ebitda_max = st.number_input(
            "Net Debt/EBITDA máximo", min_value=0.0, value=0.0, step=0.5,
            help="0 = sin límite",
        )
        emp_min = st.number_input("Empleados mínimo", min_value=0, value=0, step=10)

    query = """
        SELECT c.id, c.company_name, c.cif, c.country, c.cnae_code,
               f.revenue, f.ebitda, f.employees, f.cash_flow,
               m.ebitda_margin, m.net_income_margin,
               m.revenue_growth_yoy, m.ebitda_growth_yoy,
               m.gross_debt, m.net_debt, m.net_debt_ebitda,
               m.revenue_per_employee, m.ebitda_per_employee,
               m.equity_ratio, m.revenue_cagr_3y, m.revenue_cagr_5y
        FROM companies c
        JOIN financials f ON c.id = f.company_id
        LEFT JOIN metrics m ON c.id = m.company_id AND f.year = m.year
        WHERE f.year = %s
    """
    params = [selected_year]

    if selected_countries:
        placeholders = ",".join(["%s"] * len(selected_countries))
        query += f" AND c.country IN ({placeholders})"
        params.extend(selected_countries)
    if selected_cnaes:
        placeholders = ",".join(["%s"] * len(selected_cnaes))
        query += f" AND c.cnae_code IN ({placeholders})"
        params.extend(selected_cnaes)
    if rev_min > 0:
        query += " AND f.revenue >= %s"
        params.append(rev_min)
    if rev_max > 0:
        query += " AND f.revenue <= %s"
        params.append(rev_max)
    if emp_min > 0:
        query += " AND f.employees >= %s"
        params.append(emp_min)

    query += " ORDER BY c.company_name"
    rows = execute_query(query, tuple(params))

    if not rows:
        st.warning("No hay resultados para los filtros seleccionados.")
        return

    df = pd.DataFrame(rows)
    df = _apply_numeric_filters(
        df, rev_min, rev_max, ebitda_margin_min, rev_growth_min,
        nd_ebitda_max, emp_min,
    )

    if df.empty:
        st.warning("No hay resultados tras aplicar los filtros numéricos.")
        return

    st.caption(f"{len(df)} empresas encontradas para {selected_year}. Importes en miles EUR.")

    df = _apply_scoring(df)
    df_visible = df.head(TABLE_RESULT_LIMIT).copy()
    df_display = _format_table(df_visible)
    st.caption("Haz click en una empresa de la tabla para abrir su ficha.")
    if len(df) > TABLE_RESULT_LIMIT:
        st.info(
            f"Mostrando las primeras {TABLE_RESULT_LIMIT} empresas por score. "
            "La exportación CSV incluye todos los resultados filtrados."
        )

    table_event = st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="screener_results_table",
    )
    selected_rows = table_event.selection.rows
    if selected_rows:
        selected_position = selected_rows[0]
        st.session_state["selected_company_id"] = int(df_visible.iloc[selected_position]["id"])
        st.session_state["nav_page"] = "Ficha de empresa"
        st.rerun()

    csv_data = _format_table(df).to_csv(index=False).encode("utf-8")
    st.download_button(
        "Exportar a CSV",
        csv_data,
        file_name=f"screener_{selected_year}.csv",
        mime="text/csv",
    )

    _render_priority_chart(df)


def _apply_numeric_filters(df, rev_min, rev_max, ebitda_margin_min,
                           rev_growth_min, nd_ebitda_max, emp_min):
    if rev_min > 0:
        df = df[df["revenue"] >= rev_min]
    if rev_max > 0:
        df = df[df["revenue"] <= rev_max]
    if ebitda_margin_min > -100:
        df = df[df["ebitda_margin"].notna() & (df["ebitda_margin"] >= ebitda_margin_min / 100)]
    if rev_growth_min > -100:
        df = df[df["revenue_growth_yoy"].notna() & (df["revenue_growth_yoy"] >= rev_growth_min / 100)]
    if nd_ebitda_max > 0:
        df = df[df["net_debt_ebitda"].isna() | (df["net_debt_ebitda"] <= nd_ebitda_max)]
    if emp_min > 0:
        df = df[df["employees"].notna() & (df["employees"] >= emp_min)]
    return df


def _render_priority_chart(df: pd.DataFrame):
    st.subheader("Top empresas del screener")
    df_plot = df[df["score"].notna()].copy()
    if df_plot.empty:
        return

    df_plot = df_plot.sort_values("score", ascending=False).head(20).copy()
    df_plot["company_short"] = df_plot["company_name"].apply(_shorten_company_name)
    df_plot["ebitda_margin_pct"] = df_plot["ebitda_margin"].apply(
        lambda value: value * 100 if pd.notna(value) else None
    )
    df_plot["revenue_growth_pct"] = df_plot["revenue_growth_yoy"].apply(
        lambda value: value * 100 if pd.notna(value) else None
    )
    df_plot["net_debt_ebitda_display"] = df_plot["net_debt_ebitda"].apply(
        lambda value: f"{value:.1f}x" if pd.notna(value) else "-"
    )

    fig = go.Figure(go.Bar(
        x=df_plot["score"],
        y=df_plot["company_short"],
        orientation="h",
        marker=dict(
            color=df_plot["score"],
            cmin=0,
            cmax=100,
            colorscale=[
                [0.0, COLORS["bg_input"]],
                [1.0, COLORS["gold"]],
            ],
            line=dict(color="rgba(232, 238, 245, 0.18)", width=1),
            colorbar=dict(
                title=dict(text="Score", font=dict(color=COLORS["steel"], size=11)),
                tickfont=dict(color=COLORS["steel"], size=10),
                thickness=12,
                len=0.72,
                outlinewidth=0,
            ),
        ),
        text=df_plot["score"].apply(lambda value: f"{value:.0f}"),
        textposition="outside",
        cliponaxis=False,
        customdata=df_plot[
            [
                "company_name",
                "cnae_code",
                "revenue",
                "ebitda_margin_pct",
                "revenue_growth_pct",
                "net_debt_ebitda_display",
            ]
        ],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "CNAE: %{customdata[1]}<br>"
            "Score: %{x:.1f}<br>"
            "Revenue: %{customdata[2]:,.0f} miles EUR<br>"
            "Margen EBITDA: %{customdata[3]:.1f}%<br>"
            "Crec. revenue: %{customdata[4]:.1f}%<br>"
            "ND/EBITDA: %{customdata[5]}"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(**get_plotly_layout(
        title=dict(
            text="Empresas priorizadas por score",
            font=dict(color=COLORS["ivory"], size=15, weight=600),
            x=0.02,
            xanchor="left",
        ),
        height=max(460, 34 * len(df_plot) + 120),
        margin=dict(l=220, r=70, t=60, b=55),
        showlegend=False,
        hovermode="closest",
    ))
    fig.update_xaxes(
        title_text="Score",
        range=[0, max(105, float(df_plot["score"].max()) + 8)],
    )
    fig.update_yaxes(
        title_text="",
        autorange="reversed",
        tickfont=dict(color=COLORS["ivory"], size=11),
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def _shorten_company_name(name: str) -> str:
    if not name:
        return "-"
    name = str(name)
    return name if len(name) <= 34 else f"{name[:31]}..."


def _apply_scoring(df: pd.DataFrame) -> pd.DataFrame:
    with st.expander("Configurar scoring"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            w_rent = st.slider("Rentabilidad (Margen EBITDA)", 0, 100, 25)
        with col2:
            w_crec = st.slider("Crecimiento (Revenue YoY)", 0, 100, 25)
        with col3:
            w_solid = st.slider("Solidez (Equity ratio)", 0, 100, 25)
        with col4:
            w_efic = st.slider("Eficiencia (EBITDA/emp)", 0, 100, 25)

        total_w = w_rent + w_crec + w_solid + w_efic
        if total_w == 0:
            st.warning("Los pesos no pueden sumar 0.")
            return df

        w_rent_n = w_rent / total_w
        w_crec_n = w_crec / total_w
        w_solid_n = w_solid / total_w
        w_efic_n = w_efic / total_w

        st.caption(
            f"Pesos normalizados: Rentabilidad {w_rent_n*100:.0f}%, "
            f"Crecimiento {w_crec_n*100:.0f}%, Solidez {w_solid_n*100:.0f}%, "
            f"Eficiencia {w_efic_n*100:.0f}%"
        )

    df = df.copy()
    df["_s_rent"] = _normalize(df["ebitda_margin"])
    df["_s_crec"] = _normalize(df["revenue_growth_yoy"])
    df["_s_solid"] = _normalize(df["equity_ratio"])
    df["_s_efic"] = _normalize(df["ebitda_per_employee"])
    df["score"] = (
        df["_s_rent"] * w_rent_n +
        df["_s_crec"] * w_crec_n +
        df["_s_solid"] * w_solid_n +
        df["_s_efic"] * w_efic_n
    ) * 100
    df.drop(columns=["_s_rent", "_s_crec", "_s_solid", "_s_efic"], inplace=True)
    df.sort_values("score", ascending=False, inplace=True)
    return df


def _normalize(series: pd.Series) -> pd.Series:
    s = series.fillna(0)
    min_val = s.min()
    max_val = s.max()
    if max_val == min_val:
        return pd.Series(0.5, index=series.index)
    return (s - min_val) / (max_val - min_val)


def _format_table(df: pd.DataFrame) -> pd.DataFrame:
    display = pd.DataFrame()
    display["Empresa"] = df["company_name"]
    display["CIF"] = df["cif"]
    display["País"] = df["country"]
    display["CNAE"] = df["cnae_code"]
    display["Revenue (miles EUR)"] = df["revenue"].apply(format_euros)
    display["EBITDA (miles EUR)"] = df["ebitda"].apply(format_euros)
    display["Cash Flow (miles EUR)"] = df["cash_flow"].apply(format_euros)
    display["Gross Debt (miles EUR)"] = df["gross_debt"].apply(format_euros)
    display["Net Debt (miles EUR)"] = df["net_debt"].apply(format_euros)
    display["Margen EBITDA"] = df["ebitda_margin"].apply(
        lambda x: f"{x * 100:.1f}%" if pd.notna(x) else "-"
    )
    display["Crec. Revenue"] = df["revenue_growth_yoy"].apply(
        lambda x: f"{x * 100:.1f}%" if pd.notna(x) else "-"
    )
    display["ND/EBITDA"] = df["net_debt_ebitda"].apply(
        lambda x: f"{x:.1f}x" if pd.notna(x) else "-"
    )
    display["Equity Ratio"] = df["equity_ratio"].apply(
        lambda x: f"{x * 100:.1f}%" if pd.notna(x) else "-"
    )
    display["Empleados"] = df["employees"].apply(
        lambda x: f"{int(x):,}" if pd.notna(x) else "-"
    )
    if "score" in df.columns:
        display["Score"] = df["score"].apply(lambda x: f"{x:.0f}" if pd.notna(x) else "-")
    return display
