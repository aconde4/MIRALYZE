"""
Vista de Analisis Sectorial — KPIs, boxplots, rankings y mapa de burbujas por CNAE.
Todos los graficos usan la paleta corporativa Miralyze (dark mode).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from database.db_manager import execute_query
from utils.helpers import format_euros, get_available_years, get_available_cnaes
from utils.theme import (
    COLORS, PLOTLY_BAR_ALPHA, PLOTLY_SEQUENCE,
    get_plotly_layout, get_score_color,
)


PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render():
    st.title("Análisis Sectorial")

    cnaes = get_available_cnaes()
    years = get_available_years()

    if not cnaes or not years:
        st.info("No hay datos disponibles. Carga datos primero.")
        return

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_cnae = st.selectbox(
            "Sector (CNAE)", cnaes, key="sector_cnae_select"
        )
    with col2:
        selected_year = st.selectbox(
            "Año", years, key="sector_year_select"
        )

    df_all = _get_sector_data(selected_cnae)
    if df_all.empty:
        st.info("No hay datos financieros para este CNAE.")
        return

    df_year = df_all[df_all["year"] == selected_year].copy()

    # --- KPI row ---
    st.markdown("---")
    _render_kpi_row(df_year, selected_year, selected_cnae)

    # --- Sector evolution + robust growth trend ---
    st.markdown("---")
    col_box, col_trend = st.columns(2)
    with col_box:
        _render_sector_evolution(df_all, selected_cnae)
    with col_trend:
        _render_growth_trend(df_all, selected_cnae)

    # --- Ranking table ---
    st.markdown("---")
    _render_ranking_table(df_year, selected_year, selected_cnae)

    # --- Bubble map ---
    st.markdown("---")
    _render_bubble_map(df_year, selected_year, selected_cnae)

    # --- Multisector comparison ---
    st.markdown("---")
    st.subheader("Comparativa multisector")
    other_cnaes = [c for c in cnaes if c != selected_cnae]
    compare_cnaes = st.multiselect(
        "Selecciona hasta 3 sectores adicionales para comparar",
        other_cnaes,
        default=[],
        max_selections=3,
        key="sector_compare_multiselect",
    )
    if compare_cnaes:
        _render_multisector_comparison(
            selected_cnae, compare_cnaes, selected_year
        )
    else:
        st.info("Selecciona al menos un sector adicional para comparar.")


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def _get_sector_data(cnae_code: str) -> pd.DataFrame:
    """Fetch all company/year data for a given CNAE code."""
    rows = execute_query(
        """SELECT c.id AS company_id, c.company_name,
                  f.year, f.revenue, f.ebitda, f.employees,
                  m.ebitda_margin, m.revenue_growth_yoy, m.equity_ratio,
                  m.ebitda_per_employee, m.revenue_cagr_3y, m.revenue_cagr_5y,
                  m.net_debt, m.net_debt_ebitda
           FROM companies c
           JOIN financials f ON c.id = f.company_id
           LEFT JOIN metrics m ON c.id = m.company_id AND f.year = m.year
           WHERE c.cnae_code = %s
           ORDER BY f.year, c.company_name""",
        (cnae_code,),
    )
    return pd.DataFrame(rows) if rows else pd.DataFrame()


# ---------------------------------------------------------------------------
# Score computation (full-market normalization, same as company_detail)
# ---------------------------------------------------------------------------

def _compute_sector_scores(df_year: pd.DataFrame, year: int) -> pd.DataFrame:
    """Return df_year with a 'score' column, normalized across ALL companies
    in the given year (not just the sector)."""
    if df_year.empty:
        return df_year

    all_metrics = execute_query(
        """SELECT company_id, ebitda_margin, revenue_growth_yoy,
                  equity_ratio, ebitda_per_employee
           FROM metrics WHERE year = %s""",
        (year,),
    )
    if not all_metrics:
        df_year["score"] = None
        return df_year

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
        df_all["_s_rent"] + df_all["_s_crec"]
        + df_all["_s_solid"] + df_all["_s_efic"]
    ) / 4 * 100

    # Merge scores back to sector companies only
    score_map = df_all.set_index("company_id")["score"]
    df_year = df_year.copy()
    df_year["score"] = df_year["company_id"].map(score_map)
    return df_year


# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------

def _render_kpi_row(df: pd.DataFrame, year: int, cnae_code: str):
    if df.empty:
        st.info(f"Sin datos para el CNAE {cnae_code} en {year}.")
        return

    n_companies = df["company_id"].nunique()
    avg_margin = df["ebitda_margin"].median()
    growth = _filter_growth_outliers(df["revenue_growth_yoy"].dropna())
    avg_growth = growth.median() if not growth.empty else None
    total_revenue = df["revenue"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Empresas en el sector", f"{n_companies}")
    c2.metric(
        "Margen EBITDA mediano",
        f"{avg_margin * 100:.1f}%" if pd.notna(avg_margin) else "—",
    )
    c3.metric(
        "Crecimiento mediano",
        f"{avg_growth * 100:.1f}%" if pd.notna(avg_growth) else "—",
    )
    c4.metric(
        "Revenue total sector",
        format_euros(total_revenue) if pd.notna(total_revenue) else "—",
    )


# ---------------------------------------------------------------------------
# Sector evolution
# ---------------------------------------------------------------------------

def _render_sector_evolution(df: pd.DataFrame, cnae_code: str):
    st.subheader("Evolución del sector")

    if df.empty:
        st.info("Sin datos disponibles para el sector.")
        return

    df_plot = df.dropna(subset=["year"]).copy()
    if df_plot.empty:
        st.info("Sin datos disponibles para construir la evolución.")
        return

    summary = (
        df_plot.groupby("year")
        .agg(
            companies=("company_id", "nunique"),
            total_revenue=("revenue", lambda values: values.sum(min_count=1)),
            median_ebitda=("ebitda", "median"),
            median_margin=("ebitda_margin", "median"),
        )
        .reset_index()
        .sort_values("year")
    )

    if summary["total_revenue"].isna().all() and summary["median_margin"].isna().all():
        st.info("Sin datos suficientes de revenue o margen EBITDA.")
        return

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=summary["year"],
        y=summary["total_revenue"],
        name="Revenue total",
        marker_color=PLOTLY_BAR_ALPHA["sapphire"],
        customdata=summary[["companies", "median_ebitda"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue total: %{y:,.0f} miles EUR<br>"
            "Empresas: %{customdata[0]:,.0f}<br>"
            "EBITDA mediano: %{customdata[1]:,.0f} miles EUR"
            "<extra></extra>"
        ),
    ))
    fig.add_trace(go.Scatter(
        x=summary["year"],
        y=summary["median_margin"].apply(
            lambda value: value * 100 if pd.notna(value) else None
        ),
        name="Margen EBITDA mediano",
        mode="lines+markers",
        yaxis="y2",
        line=dict(color=COLORS["gold"], width=3),
        marker=dict(size=7, color=COLORS["gold"]),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Margen EBITDA mediano: %{y:.1f}%"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(**get_plotly_layout(
        title=dict(
            text=f"Revenue y margen EBITDA - CNAE {cnae_code}",
            font=dict(color=COLORS["ivory"], size=14, weight=600),
            x=0.02, xanchor="left",
        ),
        barmode="group",
        height=520,
        hovermode="x unified",
        margin=dict(l=60, r=68, t=70, b=145),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.23,
            xanchor="center",
            x=0.5,
            font=dict(color=COLORS["steel"], size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        yaxis=dict(
            title="Revenue total (miles EUR)",
            gridcolor="rgba(255,255,255,0.06)",
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color=COLORS["steel"], size=10),
            title_font=dict(color=COLORS["steel"], size=11),
        ),
        yaxis2=dict(
            title="Margen EBITDA mediano (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(color=COLORS["gold"], size=10),
            title_font=dict(color=COLORS["gold"], size=11),
        ),
    ))
    fig.update_xaxes(type="category", title_text="Año", tickangle=-45)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


# ---------------------------------------------------------------------------
# Growth trend (sector vs market)
# ---------------------------------------------------------------------------

def _render_growth_trend(df: pd.DataFrame, cnae_code: str):
    st.subheader("Crecimiento del sector")

    if df.empty:
        st.info("Sin datos de crecimiento disponibles.")
        return

    df_growth = df.dropna(subset=["revenue_growth_yoy"]).copy()
    df_growth = _filter_growth_outliers(df_growth, "revenue_growth_yoy")
    if df_growth.empty:
        st.info("Sin datos de crecimiento comparables para este CNAE.")
        return

    sector_years = sorted(int(year) for year in df_growth["year"].dropna().unique())
    if not sector_years:
        st.info("Sin años comparables para este CNAE.")
        return

    sector_stats = (
        df.dropna(subset=["revenue_growth_yoy"])
        .pipe(lambda data: _filter_growth_outliers(data, "revenue_growth_yoy"))
        .groupby("year")
        .agg(
            sector_median=("revenue_growth_yoy", "median"),
            sector_q1=("revenue_growth_yoy", lambda values: values.quantile(0.25)),
            sector_q3=("revenue_growth_yoy", lambda values: values.quantile(0.75)),
            companies=("company_id", "nunique"),
        )
        .reset_index()
        .sort_values("year")
    )

    if sector_stats.empty:
        st.info("Sin datos de crecimiento disponibles.")
        return

    placeholders = ",".join("%s" for _ in sector_years)
    market_rows = execute_query(
        f"""SELECT year,
                   PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY revenue_growth_yoy)
                       AS market_median,
                   COUNT(*) AS companies
            FROM metrics
            WHERE revenue_growth_yoy IS NOT NULL
              AND revenue_growth_yoy BETWEEN -1 AND 3
              AND year IN ({placeholders})
            GROUP BY year
            ORDER BY year""",
        tuple(sector_years),
    )
    df_market = pd.DataFrame(market_rows) if market_rows else pd.DataFrame()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sector_stats["year"],
        y=sector_stats["sector_q3"] * 100,
        mode="lines",
        line=dict(width=0),
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=sector_stats["year"],
        y=sector_stats["sector_q1"] * 100,
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(200, 169, 110, 0.16)",
        line=dict(width=0),
        name="Rango intercuartil",
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=sector_stats["year"],
        y=sector_stats["sector_median"] * 100,
        name=f"Sector {cnae_code} (mediana)",
        mode="lines+markers",
        line=dict(color=COLORS["gold"], width=3),
        marker=dict(size=7, color=COLORS["gold"]),
        customdata=sector_stats[["companies"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Crecimiento mediano sector: %{y:.1f}%<br>"
            "Empresas: %{customdata[0]:,.0f}"
            "<extra></extra>"
        ),
    ))

    if not df_market.empty:
        fig.add_trace(go.Scatter(
            x=df_market["year"],
            y=df_market["market_median"] * 100,
            name="Mercado total (mediana)",
            mode="lines+markers",
            line=dict(color=COLORS["steel"], width=2, dash="dot"),
            marker=dict(size=5, color=COLORS["steel"]),
            customdata=df_market[["companies"]],
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Crecimiento mediano mercado: %{y:.1f}%<br>"
                "Empresas: %{customdata[0]:,.0f}"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(**get_plotly_layout(
        title=dict(
            text="Crecimiento revenue mediano: sector vs mercado",
            font=dict(color=COLORS["ivory"], size=14, weight=600),
            x=0.02, xanchor="left",
        ),
        height=520,
        hovermode="x unified",
        margin=dict(l=60, r=40, t=70, b=135),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(color=COLORS["steel"], size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
    ))
    fig.update_xaxes(type="category", title_text="Año", tickangle=-45)
    fig.update_yaxes(title_text="Crecimiento (%)")
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def _filter_growth_outliers(data, column: str | None = None):
    """Keep revenue growth values in a practical range for sector charts."""
    if column is None:
        return data[data.between(-1, 3, inclusive="both")]
    return data[data[column].between(-1, 3, inclusive="both")]


# ---------------------------------------------------------------------------
# Ranking table
# ---------------------------------------------------------------------------

def _render_ranking_table(df: pd.DataFrame, year: int, cnae_code: str):
    st.subheader(f"Ranking de empresas — CNAE {cnae_code} ({year})")

    if df.empty:
        st.info("Sin datos para generar el ranking.")
        return

    df_scored = _compute_sector_scores(df, year)

    if "score" not in df_scored.columns or df_scored["score"].isna().all():
        st.info("No se pudo calcular el score para las empresas del sector.")
        return

    df_rank = (
        df_scored[["company_name", "revenue", "ebitda_margin",
                    "revenue_growth_yoy", "equity_ratio", "score"]]
        .dropna(subset=["score"])
        .sort_values("score", ascending=False)
        .reset_index(drop=True)
    )

    if df_rank.empty:
        st.info("Sin datos suficientes para el ranking.")
        return

    # Build display dataframe
    df_disp = df_rank.copy()
    df_disp["Empresa"] = df_disp["company_name"]
    df_disp["Revenue"] = df_disp["revenue"].apply(format_euros)
    df_disp["Margen EBITDA"] = df_disp["ebitda_margin"].apply(
        lambda x: f"{x * 100:.1f}%" if pd.notna(x) else "—"
    )
    df_disp["Crecimiento"] = df_disp["revenue_growth_yoy"].apply(
        lambda x: f"{x * 100:.1f}%" if pd.notna(x) else "—"
    )
    df_disp["Equity Ratio"] = df_disp["equity_ratio"].apply(
        lambda x: f"{x * 100:.1f}%" if pd.notna(x) else "—"
    )
    df_disp["Score"] = df_disp["score"].apply(
        lambda x: f"{x:.1f}" if pd.notna(x) else "—"
    )
    df_disp = df_disp[["Empresa", "Revenue", "Margen EBITDA",
                        "Crecimiento", "Equity Ratio", "Score"]]

    # Style the Score column
    n = len(df_disp)

    def _color_score(col):
        styles = []
        for idx in range(n):
            if idx < 3:
                styles.append(f"color: {COLORS['gold']}; font-weight: 700")
            elif n > 6 and idx >= n - 3:
                styles.append(f"color: {COLORS['crimson']}; font-weight: 600")
            else:
                styles.append(f"color: {COLORS['ivory']}")
        return styles

    styled = df_disp.style.apply(
        _color_score, subset=["Score"]
    )

    st.dataframe(styled, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Bubble map
# ---------------------------------------------------------------------------

def _render_bubble_map(df: pd.DataFrame, year: int, cnae_code: str):
    st.subheader(f"Mapa de burbujas — CNAE {cnae_code} ({year})")

    if df.empty:
        st.info("Sin datos para el mapa de burbujas.")
        return

    # Controls
    ctrl1, ctrl2, ctrl3 = st.columns(3)
    with ctrl1:
        cagr_choice = st.radio(
            "CAGR a mostrar",
            ["3 años", "5 años"],
            horizontal=True,
            key="sector_bubble_cagr",
        )
    cagr_col = "revenue_cagr_3y" if cagr_choice == "3 años" else "revenue_cagr_5y"

    # Filter out rows without the needed columns
    needed = [cagr_col, "ebitda_margin", "revenue", "company_name"]
    df_bubble = df.dropna(subset=needed).copy()

    if df_bubble.empty:
        st.info("Sin datos suficientes para el mapa de burbujas.")
        return

    # Revenue range slider
    rev_min_raw = df_bubble["revenue"].min()
    rev_max_raw = df_bubble["revenue"].max()
    rev_min = int(rev_min_raw)
    rev_max = int(rev_max_raw)

    if rev_min == rev_max:
        rev_range = (rev_min, rev_max)
    else:
        with ctrl2:
            rev_range = st.slider(
                "Rango de revenue (miles EUR)",
                min_value=rev_min,
                max_value=rev_max,
                value=(rev_min, rev_max),
                key="sector_bubble_rev_slider",
            )

    with ctrl3:
        max_companies = st.slider(
            "Max empresas",
            min_value=5,
            max_value=30,
            value=min(20, len(df_bubble)),
            key="sector_bubble_max_slider",
        )

    # Apply filters
    df_bubble = df_bubble[
        (df_bubble["revenue"] >= rev_range[0])
        & (df_bubble["revenue"] <= rev_range[1])
    ]
    df_bubble = (
        df_bubble.sort_values("revenue", ascending=False)
        .head(max_companies)
        .copy()
    )

    if df_bubble.empty:
        st.info("Sin empresas en el rango seleccionado.")
        return

    # Prepare display values
    df_bubble["ebitda_margin_pct"] = df_bubble["ebitda_margin"] * 100
    df_bubble["cagr_pct"] = df_bubble[cagr_col] * 100

    # Bubble sizes: linear scale 12px – 55px
    r_min = df_bubble["revenue"].min()
    r_max = df_bubble["revenue"].max()
    if r_max > r_min:
        df_bubble["_size"] = 12 + (df_bubble["revenue"] - r_min) / (r_max - r_min) * (55 - 12)
    else:
        df_bubble["_size"] = 30

    fig = go.Figure()
    for i, (_, row) in enumerate(df_bubble.iterrows()):
        color = PLOTLY_SEQUENCE[i % len(PLOTLY_SEQUENCE)]
        fig.add_trace(go.Scatter(
            x=[row["cagr_pct"]],
            y=[row["ebitda_margin_pct"]],
            mode="markers",
            name=row["company_name"],
            marker=dict(size=row["_size"], color=color, opacity=0.85),
            hovertemplate=(
                f"<b>{row['company_name']}</b><br>"
                f"CAGR: {row['cagr_pct']:.1f}%<br>"
                f"Margen EBITDA: {row['ebitda_margin_pct']:.1f}%<br>"
                f"Revenue: {format_euros(row['revenue'])} miles EUR"
                "<extra></extra>"
            ),
        ))

    # Quadrant lines
    fig.add_hline(y=0, line_dash="dot", line_color=COLORS["steel"], opacity=0.4)
    fig.add_vline(x=0, line_dash="dot", line_color=COLORS["steel"], opacity=0.4)

    cagr_label = "CAGR 3Y (%)" if cagr_choice == "3 años" else "CAGR 5Y (%)"
    fig.update_layout(**get_plotly_layout(
        title=dict(
            text=f"Mapa de burbujas — CNAE {cnae_code}",
            font=dict(color=COLORS["ivory"], size=14, weight=600),
            x=0.02, xanchor="left",
        ),
        height=550,
        hovermode="closest",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(color=COLORS["steel"], size=10),
        ),
        margin=dict(l=60, r=160, t=60, b=80),
    ))
    fig.update_xaxes(title_text=cagr_label)
    fig.update_yaxes(title_text="Margen EBITDA (%)")

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


# ---------------------------------------------------------------------------
# Multisector comparison
# ---------------------------------------------------------------------------

def _render_multisector_comparison(
    selected_cnae: str,
    compare_cnaes: list[str],
    year: int,
):
    all_cnaes = [selected_cnae] + compare_cnaes
    placeholders = ",".join("%s" for _ in all_cnaes)
    params = tuple(all_cnaes) + (year,)

    rows = execute_query(
        f"""SELECT c.cnae_code,
                   PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY m.ebitda_margin)
                       AS median_ebitda_margin,
                   PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY m.revenue_growth_yoy)
                       FILTER (WHERE m.revenue_growth_yoy BETWEEN -1 AND 3)
                       AS median_revenue_growth,
                   PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY m.equity_ratio)
                       AS median_equity_ratio
            FROM metrics m
            JOIN companies c ON m.company_id = c.id
            WHERE c.cnae_code IN ({placeholders}) AND m.year = %s
            GROUP BY c.cnae_code ORDER BY c.cnae_code""",
        params,
    )

    if not rows:
        st.info("Sin datos para la comparativa multisector.")
        return

    df_cmp = pd.DataFrame(rows)

    if df_cmp.empty:
        st.info("Sin datos para la comparativa multisector.")
        return
    df_cmp["cnae_code"] = df_cmp["cnae_code"].astype(str)

    metrics_config = [
        ("median_ebitda_margin", "Margen EBITDA mediano (%)"),
        ("median_revenue_growth", "Crecimiento revenue mediano (%)"),
        ("median_equity_ratio", "Equity ratio mediano (%)"),
    ]

    fig = go.Figure()
    for i, (col, label) in enumerate(metrics_config):
        color = PLOTLY_SEQUENCE[i % len(PLOTLY_SEQUENCE)]
        vals = df_cmp[col].apply(lambda v: v * 100 if pd.notna(v) else None)
        fig.add_trace(go.Bar(
            x=df_cmp["cnae_code"],
            y=vals,
            name=label,
            marker_color=color,
            marker_line_color=color,
            marker_line_width=1,
        ))

    fig.update_layout(**get_plotly_layout(
        title=dict(
            text=f"Comparativa multisector ({year})",
            font=dict(color=COLORS["ivory"], size=14, weight=600),
            x=0.02, xanchor="left",
        ),
        barmode="group",
        height=500,
        margin=dict(l=60, r=30, t=70, b=125),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(color=COLORS["steel"], size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
    ))
    fig.update_xaxes(title_text="CNAE", type="category")
    fig.update_yaxes(title_text="%")

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
