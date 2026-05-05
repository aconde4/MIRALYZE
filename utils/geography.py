"""
Geographic helpers for the Iberian choropleth view.
"""

from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

import pandas as pd

from database.db_manager import execute_query


PROJECT_ROOT = Path(__file__).resolve().parents[1]
IBERIA_GEOJSON_PATH = PROJECT_ROOT / "assets" / "geo" / "iberia_regions.geojson"


COUNTRY_CODES = {
    "ES": "ES",
    "ESP": "ES",
    "ESPANA": "ES",
    "ESPAÑA": "ES",
    "SPAIN": "ES",
    "PORTUGAL": "PT",
    "PRT": "PT",
    "PT": "PT",
}


REGION_ALIASES = {
    # SABI / Spanish common names that differ from the GeoJSON canonical names.
    "ES:ALAVA": "ES:ARABA_ALAVA",
    "ES:ARABA": "ES:ARABA_ALAVA",
    "ES:ALACANT": "ES:ALACANT_ALICANTE",
    "ES:ALICANTE": "ES:ALACANT_ALICANTE",
    "ES:CASTELLO": "ES:CASTELLO_CASTELLON",
    "ES:CASTELLON": "ES:CASTELLO_CASTELLON",
    "ES:VALENCIA": "ES:VALENCIA_VALENCIA",
    "ES:GUIPUZCOA": "ES:GIPUZKOA",
    "ES:GUIPUZCOA_GIPUZKOA": "ES:GIPUZKOA",
    "ES:VIZCAYA": "ES:BIZKAIA",
    "ES:VIZCAYA_BIZKAIA": "ES:BIZKAIA",
    "ES:BALEARES": "ES:ILLES_BALEARS",
    "ES:ISLAS_BALEARES": "ES:ILLES_BALEARS",
    "ES:ILLES_BALEARS_BALEARES": "ES:ILLES_BALEARS",
    "ES:LA_CORUNA": "ES:A_CORUNA",
    "ES:CORUNA": "ES:A_CORUNA",
    "ES:LAS_PALMAS_DE_GRAN_CANARIA": "ES:LAS_PALMAS",
    "ES:STA_CRUZ_DE_TENERIFE": "ES:SANTA_CRUZ_DE_TENERIFE",
}


def normalize_text(value) -> str:
    """Return a stable uppercase slug without accents or punctuation."""
    if value is None or pd.isna(value):
        return ""

    text = str(value).strip()
    if not text:
        return ""

    text = (
        unicodedata.normalize("NFD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    text = text.upper().replace("&", " AND ")
    text = re.sub(r"[^A-Z0-9]+", "_", text)
    return text.strip("_")


def normalize_region(country, province) -> str | None:
    """Map a country/province pair from SABI to the local GeoJSON region key."""
    country_code = COUNTRY_CODES.get(normalize_text(country))
    province_key = normalize_text(province)

    if not country_code or not province_key:
        return None

    raw_key = f"{country_code}:{province_key}"
    return REGION_ALIASES.get(raw_key, raw_key)


@lru_cache(maxsize=1)
def load_iberia_geojson() -> dict:
    """Load the local Iberia regions GeoJSON."""
    with IBERIA_GEOJSON_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def get_region_catalog() -> pd.DataFrame:
    """Return all map regions with their canonical keys and display names."""
    geojson = load_iberia_geojson()
    records = [
        {
            "region_key": feature["properties"]["region_key"],
            "region_name": feature["properties"]["region_name"],
            "country": feature["properties"]["country"],
        }
        for feature in geojson.get("features", [])
    ]
    return pd.DataFrame(records)


def get_geo_distribution(cnae_code: str | None = None) -> pd.DataFrame:
    """Fetch company counts by province and attach normalized map keys."""
    if cnae_code:
        rows = execute_query(
            """SELECT country, province, COUNT(*) AS company_count
               FROM companies
               WHERE province IS NOT NULL
                 AND trim(province) <> ''
                 AND cnae_code = %s
               GROUP BY country, province
               ORDER BY company_count DESC""",
            (cnae_code,),
        )
    else:
        rows = execute_query(
            """SELECT country, province, COUNT(*) AS company_count
               FROM companies
               WHERE province IS NOT NULL
                 AND trim(province) <> ''
               GROUP BY country, province
               ORDER BY company_count DESC"""
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "country",
                "province",
                "region_key",
                "region_name",
                "company_count",
                "is_mapped",
            ]
        )

    df = pd.DataFrame(rows)
    df["company_count"] = df["company_count"].astype(int)
    df["region_key"] = df.apply(
        lambda row: normalize_region(row["country"], row["province"]), axis=1
    )

    catalog = get_region_catalog()
    df = df.merge(
        catalog[["region_key", "region_name"]],
        how="left",
        on="region_key",
    )
    df["is_mapped"] = df["region_name"].notna()
    df["region_name"] = df["region_name"].fillna(df["province"])

    return df
