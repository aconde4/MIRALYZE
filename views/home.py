"""
Dashboard view with global stats, sector ranking and import history.
"""

from textwrap import dedent

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from database.db_manager import execute_query
from utils.theme import COLORS


def render():
    st.title("Dashboard")
    st.markdown("Resumen general del sistema de screening financiero.")

    stats = _get_stats()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Empresas", stats["total_companies"])
    col2.metric("Registros financieros", stats["total_financials"])
    col3.metric("Importaciones", stats["total_imports"])
    col4.metric("Países", stats["total_countries"])

    st.markdown("---")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Top 10 sectores (CNAE) por empresas")
        cnae_data = execute_query(
            """SELECT COALESCE(NULLIF(cnae_code, ''), 'Sin CNAE') AS cnae_code,
                      COUNT(*) AS count
               FROM companies
               GROUP BY cnae_code
               ORDER BY count DESC
               LIMIT 10"""
        )
        if cnae_data:
            _render_sector_ranking(pd.DataFrame(cnae_data))
        else:
            st.info("No hay datos todavía. Carga un archivo para empezar.")

    with col_right:
        st.subheader("Últimas importaciones")
        imports = execute_query(
            """SELECT import_timestamp, file_name, load_mode,
                      rows_accepted, rows_rejected
               FROM import_log
               ORDER BY import_timestamp DESC
               LIMIT 5"""
        )
        if imports:
            df_imports = pd.DataFrame(imports)
            df_imports.columns = ["Fecha", "Archivo", "Modo", "Aceptadas", "Rechazadas"]
            st.dataframe(df_imports, use_container_width=True, hide_index=True)
        else:
            st.info("No se han realizado importaciones todavía.")


def _get_stats() -> dict:
    rows = execute_query(
        """SELECT
              (SELECT COUNT(*) FROM companies) AS total_companies,
              (SELECT COUNT(*) FROM financials) AS total_financials,
              (SELECT COUNT(*) FROM import_log) AS total_imports,
              (SELECT COUNT(DISTINCT country) FROM companies) AS total_countries"""
    )
    stats = rows[0] if rows else {}
    return {
        "total_companies": stats.get("total_companies", 0),
        "total_financials": stats.get("total_financials", 0),
        "total_imports": stats.get("total_imports", 0),
        "total_countries": stats.get("total_countries", 0),
    }


def _render_sector_ranking(df: pd.DataFrame):
    """Render a compact ranking with proportional bars instead of plot axes."""
    max_count = max(df["count"].max(), 1)
    rows_html = []

    for index, row in df.reset_index(drop=True).iterrows():
        cnae = row["cnae_code"]
        count = int(row["count"])
        width = max(4, count / max_count * 100)
        rows_html.append(
            dedent(f"""
            <div class="sector-rank-row">
                <div class="sector-rank-meta">
                    <span class="sector-rank-pos">{index + 1}</span>
                    <span class="sector-rank-code">{cnae}</span>
                    <span class="sector-rank-count">{count:,} empresas</span>
                </div>
                <div class="sector-rank-track">
                    <div class="sector-rank-bar" style="width:{width:.1f}%"></div>
                </div>
            </div>
            """).strip()
        )

    html = dedent(f"""
    <style>
        .sector-rank {{
            background: rgba(24, 38, 57, 0.92);
            border: 1px solid rgba(139, 168, 196, 0.22);
            border-radius: 8px;
            padding: 16px 20px;
            min-height: 500px;
        }}
        .sector-rank-row {{
            padding: 8px 0 9px;
            border-bottom: 1px solid rgba(139, 168, 196, 0.12);
        }}
        .sector-rank-row:last-child {{
            border-bottom: 0;
        }}
        .sector-rank-meta {{
            display: grid;
            grid-template-columns: 32px minmax(64px, 1fr) auto;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
        }}
        .sector-rank-pos {{
            color: {COLORS["gold"]};
            font-weight: 700;
            font-size: 0.88rem;
        }}
        .sector-rank-code {{
            color: {COLORS["ivory"]};
            font-weight: 700;
            font-size: 1rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .sector-rank-count {{
            color: {COLORS["steel"]};
            font-size: 0.88rem;
            white-space: nowrap;
        }}
        .sector-rank-track {{
            height: 9px;
            background: rgba(232, 238, 245, 0.09);
            border-radius: 999px;
            overflow: hidden;
        }}
        .sector-rank-bar {{
            height: 100%;
            background: linear-gradient(90deg, {COLORS["sapphire"]}, {COLORS["gold"]});
            border-radius: 999px;
        }}
    </style>
    <div class="sector-rank">
        {''.join(rows_html)}
    </div>
    """).strip()
    component_height = max(520, 48 * len(df) + 48)
    components.html(html, height=component_height, scrolling=False)
