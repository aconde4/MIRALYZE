"""
Geographic heat map view for Spain and Portugal.
"""

from __future__ import annotations

import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.geography import (
    get_geo_distribution,
    get_region_catalog,
    load_iberia_geojson,
)
from utils.helpers import get_available_cnaes
from utils.theme import COLORS


ALL_SECTORS = "Todos los sectores"
MAP_LATITUDE = 39.5
PENINSULA_X_RANGE = [-10.5 * math.cos(math.radians(MAP_LATITUDE)), 4.6 * math.cos(math.radians(MAP_LATITUDE))]
PENINSULA_Y_RANGE = [35.2, 44.4]
MAP_LOW_COLOR = COLORS["bg_input"]
MAP_HIGH_COLOR = COLORS["gold"]


def render():
    st.title("Mapa geográfico")
    st.markdown(
        "Distribución territorial de empresas por provincia o distrito."
    )

    cnaes = [str(cnae) for cnae in get_available_cnaes() if cnae]
    selector_options = [ALL_SECTORS] + [f"CNAE {cnae}" for cnae in cnaes]

    col_sector, col_view = st.columns([2, 1])
    with col_sector:
        selected_label = st.selectbox(
            "Sector",
            selector_options,
            index=0,
            key="geo_map_cnae_select",
        )
    with col_view:
        view_mode = st.radio(
            "Vista",
            ["Península", "Completo"],
            horizontal=True,
            key="geo_map_view_mode",
        )
    selected_cnae = (
        None
        if selected_label == ALL_SECTORS
        else selected_label.replace("CNAE ", "", 1)
    )

    distribution = get_geo_distribution(selected_cnae)
    map_df, ranking_df, unmatched_df = _prepare_map_data(distribution, selected_label)

    _render_metrics(distribution, ranking_df, selected_cnae)

    if not unmatched_df.empty:
        with st.expander(
            f"{len(unmatched_df)} regiones no se pudieron ubicar en el mapa",
            expanded=False,
        ):
            st.dataframe(
                unmatched_df[["country", "province", "company_count"]].rename(
                    columns={
                        "country": "País",
                        "province": "Región original",
                        "company_count": "Empresas",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    st.plotly_chart(
        _build_choropleth(map_df, selected_label, view_mode),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.subheader("Ranking por región")
    _render_ranking(ranking_df)


def _prepare_map_data(
    distribution: pd.DataFrame,
    selected_label: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    catalog = get_region_catalog()

    if distribution.empty:
        mapped = pd.DataFrame(
            columns=["region_key", "region_name", "country", "company_count"]
        )
        unmatched = distribution
    else:
        unmatched = distribution[~distribution["is_mapped"]].copy()
        mapped = (
            distribution[distribution["is_mapped"]]
            .groupby(["region_key", "region_name"], as_index=False)
            .agg(company_count=("company_count", "sum"))
        )

    map_df = catalog.merge(
        mapped[["region_key", "company_count"]],
        how="left",
        on="region_key",
    )
    map_df["company_count"] = (
        pd.to_numeric(map_df["company_count"], errors="coerce")
        .fillna(0)
        .astype(int)
    )
    map_df["sector_label"] = selected_label
    map_df["display_country"] = map_df["country"].map(
        {"SPAIN": "España", "PORTUGAL": "Portugal"}
    ).fillna(map_df["country"])
    map_df["display_count"] = map_df["company_count"].apply(_format_count)

    ranking_df = (
        map_df[map_df["company_count"] > 0]
        .sort_values("company_count", ascending=False)
        .reset_index(drop=True)
    )

    return map_df, ranking_df, unmatched


def _render_metrics(
    distribution: pd.DataFrame,
    ranking_df: pd.DataFrame,
    selected_cnae: str | None,
):
    total_companies = (
        int(distribution["company_count"].sum()) if not distribution.empty else 0
    )
    regions_with_companies = int(len(ranking_df))

    if ranking_df.empty:
        leader_name = "-"
        leader_count = None
    else:
        top = ranking_df.iloc[0]
        leader_name = top["region_name"]
        leader_count = f"{_format_count(top['company_count'])} empresas"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Empresas", _format_count(total_companies))
    col2.metric("Regiones", _format_count(regions_with_companies))
    col3.metric("Top región", leader_name, leader_count)
    col4.metric("Sector", selected_cnae or "Todos")


def _build_choropleth(
    map_df: pd.DataFrame,
    selected_label: str,
    view_mode: str = "Península",
) -> go.Figure:
    geojson = load_iberia_geojson()
    max_count = int(map_df["company_count"].max()) if not map_df.empty else 0
    max_count = max(max_count, 1)
    region_lookup = map_df.set_index("region_key").to_dict(orient="index")

    fig = go.Figure()
    all_x = []
    all_y = []

    for feature in geojson.get("features", []):
        props = feature.get("properties", {})
        region_key = props.get("region_key")
        row = region_lookup.get(region_key, {})
        count = int(row.get("company_count", 0) or 0)
        region_name = row.get("region_name") or props.get("region_name") or region_key
        country = row.get("display_country") or props.get("country") or "-"
        fillcolor = _region_color(count, max_count)

        for polygon in _iter_polygons(feature.get("geometry")):
            exterior = polygon[0] if polygon else []
            if len(exterior) < 3:
                continue

            x_values, y_values = _project_ring(exterior)
            all_x.extend(x_values)
            all_y.extend(y_values)
            hover_text = (
                f"<b>{region_name}</b><br>"
                f"País: {country}<br>"
                f"Empresas: {_format_count(count)}<br>"
                f"Sector: {selected_label}"
            )

            fig.add_trace(
                go.Scatter(
                    name=region_name,
                    x=x_values,
                    y=y_values,
                    mode="lines",
                    fill="toself",
                    fillcolor=fillcolor,
                    line=dict(color="rgba(232, 238, 245, 0.26)", width=0.55),
                    hoveron="fills",
                    text=[hover_text] * len(x_values),
                    hoverinfo="text",
                    hovertemplate="%{text}<extra></extra>",
                    showlegend=False,
                )
            )

    # Invisible marker used only to render a continuous colorbar.
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(
                color=[0],
                cmin=0,
                cmax=max_count,
                colorscale=_plotly_colorscale(),
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="Empresas",
                        font=dict(color=COLORS["steel"], size=12),
                    ),
                    tickfont=dict(color=COLORS["steel"], size=11),
                    thickness=14,
                    len=0.72,
                    outlinewidth=0,
                ),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    if view_mode == "Completo":
        x_range = _with_padding(all_x, 0.04)
        y_range = _with_padding(all_y, 0.04)
    else:
        x_range = PENINSULA_X_RANGE
        y_range = PENINSULA_Y_RANGE
    fig.update_layout(
        title=dict(
            text=f"Mapa de calor - {selected_label}",
            font=dict(color=COLORS["ivory"], size=15),
            x=0.02,
            xanchor="left",
        ),
        height=650,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, system-ui, -apple-system, sans-serif",
            color=COLORS["ivory"],
        ),
        hoverlabel=dict(
            bgcolor=COLORS["midnight"],
            font_color="white",
            bordercolor=COLORS["gold"],
        ),
        xaxis=dict(
            visible=False,
            range=x_range,
            fixedrange=True,
            constrain="domain",
        ),
        yaxis=dict(
            visible=False,
            range=y_range,
            fixedrange=True,
            scaleanchor="x",
            scaleratio=1,
        ),
        margin=dict(l=8, r=8, t=56, b=8),
        dragmode=False,
    )
    return fig


def _iter_polygons(geometry: dict | None):
    if not geometry:
        return []

    geometry_type = geometry.get("type")
    coordinates = geometry.get("coordinates", [])

    if geometry_type == "Polygon":
        return [coordinates]
    if geometry_type == "MultiPolygon":
        return [polygon for polygon in coordinates]
    return []


def _project_ring(ring: list[list[float]]) -> tuple[list[float], list[float]]:
    factor = math.cos(math.radians(MAP_LATITUDE))
    x_values = [point[0] * factor for point in ring]
    y_values = [point[1] for point in ring]
    return x_values, y_values


def _with_padding(values: list[float], ratio: float) -> list[float]:
    if not values:
        return [0, 1]
    low = min(values)
    high = max(values)
    padding = (high - low) * ratio if high > low else 1
    return [low - padding, high + padding]


def _plotly_colorscale() -> list[list[object]]:
    return [
        [0.00, MAP_LOW_COLOR],
        [1.00, MAP_HIGH_COLOR],
    ]


def _region_color(count: int, max_count: int) -> str:
    if count <= 0:
        return MAP_LOW_COLOR

    value = min(count / max_count, 1)
    scale = _plotly_colorscale()
    for index in range(1, len(scale)):
        left_pos, left_color = scale[index - 1]
        right_pos, right_color = scale[index]
        if value <= right_pos:
            local = (value - left_pos) / (right_pos - left_pos)
            return _mix_hex(left_color, right_color, local)

    return MAP_HIGH_COLOR


def _mix_hex(left: str, right: str, amount: float) -> str:
    amount = max(0, min(amount, 1))
    left_rgb = _hex_to_rgb(left)
    right_rgb = _hex_to_rgb(right)
    mixed = [
        round(left_rgb[i] + (right_rgb[i] - left_rgb[i]) * amount)
        for i in range(3)
    ]
    return f"rgb({mixed[0]}, {mixed[1]}, {mixed[2]})"


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def _render_ranking(ranking_df: pd.DataFrame):
    if ranking_df.empty:
        st.info("No hay empresas para el sector seleccionado.")
        return

    total = ranking_df["company_count"].sum()
    table = ranking_df[["region_name", "display_country", "company_count"]].copy()
    table["share"] = table["company_count"] / total if total else 0
    table = table.rename(
        columns={
            "region_name": "Región",
            "display_country": "País",
            "company_count": "Empresas",
            "share": "% del total",
        }
    )
    table["Empresas"] = table["Empresas"].apply(_format_count)
    table["% del total"] = table["% del total"].apply(
        lambda value: f"{value * 100:.1f}%"
    )

    st.dataframe(table, use_container_width=True, hide_index=True)


def _format_count(value) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{int(value):,}".replace(",", ".")
