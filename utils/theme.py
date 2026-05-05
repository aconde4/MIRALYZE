"""
Sistema de diseño Miralyze — v3.0 Dark
Paleta corporativa dark, estilos CSS premium para Streamlit y configuración base de Plotly.
Todos los gráficos y componentes deben usar estos exports para garantizar consistencia total.
"""

# ── Paleta de colores ──────────────────────────────────────────────────────────

COLORS = {
    # Primary
    "midnight":  "#131f2f",
    "navy":      "#1A3A5C",
    "sapphire":  "#2563A8",
    "gold":      "#C8A96E",
    "ivory":     "#F7F5F2",
    # Support
    "frost":     "#E8EEF5",
    "steel":     "#8BA8C4",
    "emerald":   "#1B7A5A",
    "crimson":   "#B04040",
    # Extended (derivados para gradientes y estados)
    "sapphire_light": "#3A7BD5",
    "sapphire_dark":  "#1B4F8A",
    "gold_light":     "#D4BC8A",
    "navy_light":     "#2A5580",
    "frost_deep":     "#D8E4F0",
    "ivory_warm":     "#FAF8F5",
    # Dark mode surfaces
    "bg_deep":   "#0E1825",
    "bg_card":   "#182639",
    "bg_input":  "#172235",
}

# Secuencia de colores corporativos para series múltiples en Plotly
PLOTLY_SEQUENCE = [
    COLORS["sapphire"],
    COLORS["gold"],
    COLORS["navy_light"],
    COLORS["steel"],
    COLORS["emerald"],
    COLORS["crimson"],
]

# Colores con canal alfa para barras
PLOTLY_BAR_ALPHA = {
    "sapphire": "rgba(37, 99, 168, 0.80)",
    "gold":     "rgba(200, 169, 110, 0.80)",
    "navy":     "rgba(26, 58, 92, 0.80)",
    "steel":    "rgba(139, 168, 196, 0.65)",
    "emerald":  "rgba(27, 122, 90, 0.80)",
    "crimson":  "rgba(176, 64, 64, 0.70)",
}

# Colores semánticos
SEMANTIC = {
    "positive": COLORS["emerald"],
    "negative": COLORS["crimson"],
    "neutral":  COLORS["steel"],
    "premium":  COLORS["gold"],
}


# ── Plotly helpers ─────────────────────────────────────────────────────────────

def get_plotly_layout(**overrides) -> dict:
    """Layout base de Plotly alineado con la marca Miralyze (dark mode).

    Úsalo así:  fig.update_layout(**get_plotly_layout())
    """
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, system-ui, -apple-system, sans-serif",
            color=COLORS["ivory"],
            size=13,
        ),
        title=dict(
            font=dict(color=COLORS["ivory"], size=15, weight=600),
            x=0.02,
            xanchor="left",
            y=0.97,
            yanchor="top",
            pad=dict(b=24),
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(color=COLORS["steel"], size=11),
            bgcolor="rgba(0,0,0,0)",
            itemsizing="constant",
            traceorder="normal",
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            linecolor="rgba(255,255,255,0.08)",
            linewidth=1,
            tickfont=dict(color=COLORS["steel"], size=11),
            title_font=dict(color=COLORS["steel"], size=12),
            title_standoff=12,
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            linecolor="rgba(255,255,255,0.08)",
            linewidth=1,
            tickfont=dict(color=COLORS["steel"], size=11),
            title_font=dict(color=COLORS["steel"], size=12),
            title_standoff=12,
        ),
        hoverlabel=dict(
            bgcolor=COLORS["midnight"],
            font_color="white",
            font_size=12,
            font_family="Inter, system-ui, sans-serif",
            bordercolor=COLORS["gold"],
        ),
        margin=dict(l=60, r=40, t=60, b=70),
        hovermode="x unified",
    )
    base.update(overrides)
    return base


def get_combo_layout(title: str, bar_label: str, line_label: str,
                     height: int = 450, **overrides) -> dict:
    """Layout especializado para gráficos combo (barras + línea en eje secundario)."""
    layout = get_plotly_layout(
        title=dict(
            text=title,
            font=dict(color=COLORS["ivory"], size=14, weight=600),
            x=0.02, xanchor="left", y=0.97, yanchor="top",
            pad=dict(b=20),
        ),
        height=height,
        margin=dict(l=60, r=60, t=60, b=80),
        legend=dict(
            orientation="h",
            yanchor="top", y=-0.15,
            xanchor="center", x=0.5,
            font=dict(color=COLORS["steel"], size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        yaxis=dict(
            title=bar_label,
            gridcolor="rgba(255,255,255,0.06)",
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color=COLORS["steel"], size=10),
            title_font=dict(color=COLORS["steel"], size=11),
            title_standoff=8,
        ),
        yaxis2=dict(
            title=line_label,
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(color=COLORS["steel"], size=10),
            title_font=dict(color=COLORS["gold"], size=11),
            title_standoff=8,
        ),
    )
    layout.update(overrides)
    return layout


def get_plotly_colors() -> list[str]:
    """Secuencia corporativa de colores para series múltiples."""
    return list(PLOTLY_SEQUENCE)


def get_score_color(score: float) -> tuple[str, str]:
    """Devuelve (color_arco, rating_label) según el score 0-100."""
    if score >= 70:
        return COLORS["gold"], "Alto"
    elif score >= 40:
        return COLORS["sapphire"], "Medio"
    else:
        return COLORS["steel"], "Bajo"


# ── CSS para Streamlit — dark mode premium ──────────────────────────────────────

CSS_STYLES = f"""
<style>
/* ═══════════════════════════════════════════════════════════════════
   MIRALYZE — Design System v3.0 Dark
   Herramienta financiera premium • Dark mode
   ═══════════════════════════════════════════════════════════════════ */

/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Variables CSS ── */
:root {{
    --midnight: {COLORS["midnight"]};
    --navy: {COLORS["navy"]};
    --sapphire: {COLORS["sapphire"]};
    --gold: {COLORS["gold"]};
    --ivory: {COLORS["ivory"]};
    --steel: {COLORS["steel"]};
    --emerald: {COLORS["emerald"]};
    --crimson: {COLORS["crimson"]};
    --bg-deep: {COLORS["bg_deep"]};
    --bg-card: {COLORS["bg_card"]};
    --bg-input: {COLORS["bg_input"]};
    --border: rgba(255,255,255,0.07);
    --border-hover: rgba(255,255,255,0.12);
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.25);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.35);
    --shadow-lg: 0 8px 24px rgba(0,0,0,0.40);
    --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* ── Reset & fondo general ── */
*, *::before, *::after {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
}}
.stApp {{
    background-color: {COLORS["bg_deep"]};
}}
/* Texto base en modo oscuro */
.stApp p,
.stApp li,
.stMarkdown p,
.stMarkdown li {{
    color: rgba(247, 245, 242, 0.85) !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {COLORS["midnight"]};
    border-right: 1px solid rgba(255,255,255,0.06);
}}
[data-testid="stSidebar"] * {{
    color: white !important;
}}
[data-testid="stSidebar"] .stCaption p,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown p {{
    color: {COLORS["steel"]} !important;
    font-size: 0.82rem !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: rgba(139, 168, 196, 0.15) !important;
    margin: 0.75rem 0 !important;
}}

/* Sidebar — título */
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2 {{
    background: linear-gradient(135deg, #FFFFFF 0%, {COLORS["gold"]} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}}

/* Sidebar — radio buttons (navegación) */
[data-testid="stSidebar"] [role="radiogroup"] label {{
    background-color: transparent !important;
    border-radius: var(--radius-sm);
    padding: 6px 12px !important;
    margin: 2px 0 !important;
    transition: all var(--transition);
    border-left: 3px solid transparent !important;
}}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {{
    background-color: rgba(255,255,255,0.05) !important;
}}
[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {{
    background-color: rgba(255,255,255,0.07) !important;
    border-left: 3px solid {COLORS["gold"]} !important;
}}

/* ── Tipografía ── */
h1, .stMarkdown h1 {{
    color: {COLORS["gold"]} !important;
    font-weight: 800 !important;
    font-size: 1.9rem !important;
    letter-spacing: -0.5px;
}}
h2, .stMarkdown h2 {{
    color: {COLORS["gold"]} !important;
    font-weight: 700 !important;
    font-size: 1.35rem !important;
    letter-spacing: -0.3px;
}}
h3, .stMarkdown h3 {{
    color: {COLORS["gold_light"]} !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}}
.stCaption, .stCaption p {{
    color: {COLORS["steel"]} !important;
    font-size: 0.8rem !important;
}}

/* ── Botones ── */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {{
    background: linear-gradient(135deg, {COLORS["sapphire"]} 0%, {COLORS["sapphire_dark"]} 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: var(--radius-sm);
    font-weight: 600;
    padding: 0.5rem 1.5rem !important;
    box-shadow: 0 2px 8px rgba(37, 99, 168, 0.30);
    transition: all var(--transition);
    letter-spacing: 0.2px;
}}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {{
    background: linear-gradient(135deg, {COLORS["sapphire_light"]} 0%, {COLORS["sapphire"]} 100%) !important;
    box-shadow: 0 4px 16px rgba(37, 99, 168, 0.40);
    transform: translateY(-1px);
}}
.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {{
    background-color: transparent !important;
    border: 1.5px solid {COLORS["sapphire"]} !important;
    color: {COLORS["sapphire_light"]} !important;
    border-radius: var(--radius-sm);
    font-weight: 600;
    transition: all var(--transition);
}}
.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="stBaseButton-secondary"]:hover {{
    background-color: rgba(37, 99, 168, 0.12) !important;
    border-color: {COLORS["sapphire_light"]} !important;
}}

/* ── Download button ── */
.stDownloadButton > button {{
    background-color: transparent !important;
    border: 1.5px solid {COLORS["sapphire"]} !important;
    color: {COLORS["sapphire_light"]} !important;
    border-radius: var(--radius-sm);
    font-weight: 600;
    transition: all var(--transition);
}}
.stDownloadButton > button:hover {{
    background-color: {COLORS["sapphire"]} !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(37, 99, 168, 0.30);
}}

/* ── KPI / Metric cards ── */
[data-testid="stMetric"] {{
    background: {COLORS["bg_card"]};
    border-radius: var(--radius-md);
    padding: 20px 22px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    transition: all var(--transition);
}}
[data-testid="stMetric"]:hover {{
    box-shadow: var(--shadow-md);
    border-color: var(--border-hover);
}}
[data-testid="stMetric"] label {{
    color: {COLORS["steel"]} !important;
    text-transform: uppercase;
    font-size: 0.7rem !important;
    letter-spacing: 0.8px;
    font-weight: 600 !important;
}}
[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {COLORS["ivory"]} !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
}}
[data-testid="stMetricDelta"][data-testid-direction="positive"] {{
    color: {COLORS["emerald"]} !important;
}}
[data-testid="stMetricDelta"][data-testid-direction="negative"] {{
    color: {COLORS["crimson"]} !important;
}}

/* ── Tablas (st.dataframe) ── */
[data-testid="stDataFrame"] {{
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm);
    background-color: {COLORS["bg_card"]};
}}

/* ── Inputs y selectbox ── */
.stTextInput > div > div,
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stNumberInput > div > div {{
    border-color: rgba(255,255,255,0.10) !important;
    border-radius: var(--radius-sm);
    transition: all var(--transition);
    background-color: {COLORS["bg_input"]} !important;
    color: {COLORS["ivory"]} !important;
}}
.stTextInput input,
.stNumberInput input {{
    color: {COLORS["ivory"]} !important;
    background-color: transparent !important;
}}
.stTextInput > div > div:focus-within,
.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within {{
    border-color: {COLORS["sapphire"]} !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 168, 0.18) !important;
}}
.stTextInput label, .stSelectbox label,
.stMultiSelect label, .stNumberInput label,
.stSlider label, .stRadio label {{
    color: {COLORS["steel"]} !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
}}

/* ── Selectbox dropdown ── */
[data-baseweb="menu"] {{
    background-color: {COLORS["bg_card"]} !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
}}
[data-baseweb="menu"] li {{
    color: {COLORS["ivory"]} !important;
    background-color: transparent !important;
}}
[data-baseweb="menu"] li:hover {{
    background-color: rgba(37, 99, 168, 0.15) !important;
}}
[data-baseweb="menu"] li[aria-selected="true"] {{
    background-color: rgba(37, 99, 168, 0.20) !important;
}}

/* ── Sliders ── */
.stSlider [data-testid="stThumbValue"] {{
    color: {COLORS["gold"]} !important;
    font-weight: 600 !important;
}}

/* ── Expander ── */
.streamlit-expanderHeader {{
    color: {COLORS["ivory"]} !important;
    font-weight: 600 !important;
    background-color: {COLORS["bg_card"]} !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    transition: all var(--transition);
}}
.streamlit-expanderHeader:hover {{
    border-color: var(--border-hover) !important;
    box-shadow: var(--shadow-sm);
}}
.streamlit-expanderContent {{
    background-color: {COLORS["bg_card"]} !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}}

/* ── File uploader ── */
[data-testid="stFileUploader"] {{
    border: 2px dashed rgba(255,255,255,0.12) !important;
    border-radius: var(--radius-md) !important;
    transition: all var(--transition);
    background-color: rgba(255,255,255,0.02) !important;
}}
[data-testid="stFileUploader"]:hover {{
    border-color: {COLORS["sapphire"]} !important;
    background-color: rgba(37, 99, 168, 0.06) !important;
}}

/* ── Alertas ── */
.stAlert[data-baseweb="notification"] {{
    border-radius: var(--radius-md);
    border-left: 4px solid;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0;
    border-bottom: 2px solid rgba(255,255,255,0.08) !important;
    background: transparent !important;
}}
.stTabs [data-baseweb="tab"] {{
    color: {COLORS["steel"]} !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    transition: all var(--transition);
    background: transparent !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {COLORS["ivory"]} !important;
}}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    color: {COLORS["sapphire_light"]} !important;
    border-bottom: 2px solid {COLORS["sapphire_light"]} !important;
    font-weight: 600 !important;
}}

/* ── Separadores ── */
hr {{
    border-color: rgba(255,255,255,0.08) !important;
    margin: 1.2rem 0 !important;
}}

/* ── Scrollbar personalizado ── */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-thumb {{
    background: rgba(139, 168, 196, 0.4);
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {COLORS["steel"]};
}}
::-webkit-scrollbar-track {{
    background: {COLORS["bg_input"]};
}}

/* ── Plotly charts container ── */
.stPlotlyChart {{
    background: {COLORS["bg_card"]};
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    padding: 12px 8px 8px 8px;
    margin-bottom: 0.5rem;
    overflow: hidden;
    transition: box-shadow var(--transition);
}}
.stPlotlyChart:hover {{
    box-shadow: var(--shadow-md);
}}

/* ── Main block padding ── */
.block-container {{
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px;
}}

/* ── Subheaders section spacing ── */
.stMarkdown h2 {{
    margin-top: 1.5rem !important;
    margin-bottom: 0.75rem !important;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid rgba(200, 169, 110, 0.25);
}}

/* ── Sidebar subheader override ── */
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown h3 {{
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {COLORS["gold"]} !important;
    -webkit-text-fill-color: {COLORS["gold"]} !important;
    background: none !important;
    margin-top: 0.5rem !important;
}}
</style>
"""
