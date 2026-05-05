"""
Punto de entrada de la aplicación Streamlit.
Gestiona la navegación entre vistas.
"""

import os
import sys

import streamlit as st

# Asegurar que el directorio raíz del proyecto está en el path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.theme import CSS_STYLES


st.set_page_config(
    page_title="Miralyze",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Aplicar estilos de marca.
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Logo en sidebar.
_logo_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "logo_miralyze_sidebar.png",
)
st.sidebar.image(_logo_path, use_container_width=True)
st.sidebar.markdown("---")

PAGES = {
    "Dashboard": "home",
    "Cargar datos": "upload",
    "Listado de empresas": "company_list",
    "Ficha de empresa": "company_detail",
    "Screener": "screener",
    "Mapa geográfico": "geo_map",
    "Análisis sectorial": "sector",
}

# Si hay navegación forzada desde otra vista, usarla.
default_page = st.session_state.get("nav_page", "Dashboard")
if default_page not in PAGES:
    default_page = "Dashboard"

selection = st.sidebar.radio(
    "Navegación",
    list(PAGES.keys()),
    index=list(PAGES.keys()).index(default_page),
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption("TFG Ingeniería Informática — UPM")

# Importar y renderizar la vista seleccionada.
if selection == "Dashboard":
    from views.home import render
elif selection == "Cargar datos":
    from views.upload import render
elif selection == "Listado de empresas":
    from views.company_list import render
elif selection == "Ficha de empresa":
    from views.company_detail import render
elif selection == "Screener":
    from views.screener import render
elif selection == "Mapa geográfico":
    from views.geo_map import render
elif selection == "Análisis sectorial":
    from views.sector import render

render()
