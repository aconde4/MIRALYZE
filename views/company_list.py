"""
Company listing with search and filters.
"""

import pandas as pd
import streamlit as st

from database.db_manager import execute_query
from utils.helpers import format_euros, get_available_cnaes, get_available_countries


def render():
    st.title("Listado de empresas")

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        search_text = st.text_input("Buscar por nombre", placeholder="Escribe para buscar...")
    with col2:
        search_cif = st.text_input("Buscar por CIF", placeholder="Ej: B12345678")
    with col3:
        selected_countries = st.multiselect("País", get_available_countries())
    with col4:
        selected_cnaes = st.multiselect("CNAE", get_available_cnaes())

    query = """
        SELECT c.id, c.company_name AS empresa, c.cif, c.country AS pais,
               c.province AS provincia, c.cnae_code AS cnae,
               f.year AS ultimo_ano, f.revenue,
               m.ebitda_margin, m.revenue_growth_yoy
        FROM companies c
        LEFT JOIN financials f ON c.id = f.company_id
        LEFT JOIN metrics m ON c.id = m.company_id AND f.year = m.year
        WHERE f.year = (
            SELECT MAX(f2.year) FROM financials f2 WHERE f2.company_id = c.id
        )
    """
    params = []

    if search_text:
        query += " AND LOWER(c.company_name) LIKE LOWER(%s)"
        params.append(f"%{search_text}%")
    if search_cif:
        query += " AND UPPER(c.cif) LIKE UPPER(%s)"
        params.append(f"%{search_cif}%")
    if selected_countries:
        placeholders = ",".join(["%s"] * len(selected_countries))
        query += f" AND c.country IN ({placeholders})"
        params.extend(selected_countries)
    if selected_cnaes:
        placeholders = ",".join(["%s"] * len(selected_cnaes))
        query += f" AND c.cnae_code IN ({placeholders})"
        params.extend(selected_cnaes)

    query += " ORDER BY c.company_name"
    rows = execute_query(query, tuple(params))

    if not rows:
        st.info("No se encontraron empresas con los filtros seleccionados.")
        return

    df = pd.DataFrame(rows)
    df_display = df.copy()
    df_display["revenue"] = df_display["revenue"].apply(format_euros)
    df_display["ebitda_margin"] = df_display["ebitda_margin"].apply(
        lambda x: f"{x * 100:.1f}%" if pd.notna(x) else "-"
    )
    df_display["revenue_growth_yoy"] = df_display["revenue_growth_yoy"].apply(
        lambda x: f"{x * 100:.1f}%" if pd.notna(x) else "-"
    )

    df_display.columns = [
        "ID", "Empresa", "CIF", "País", "Provincia", "CNAE", "Último año",
        "Revenue (miles EUR)", "Margen EBITDA", "Crec. Revenue YoY",
    ]

    st.caption(f"{len(df_display)} empresas encontradas")
    st.dataframe(
        df_display.drop(columns=["ID"]),
        use_container_width=True,
        hide_index=True,
    )

    company_options = dict(zip(df["empresa"], df["id"]))
    selected_name = st.selectbox(
        "Selecciona una empresa para ver su ficha",
        [""] + list(company_options.keys()),
    )

    if selected_name:
        st.session_state["selected_company_id"] = company_options[selected_name]
        st.session_state["nav_page"] = "Ficha de empresa"
        st.rerun()
