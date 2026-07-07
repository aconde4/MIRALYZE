"""
Shared helper functions.
"""

import pandas as pd

from database.db_manager import execute_query


def format_euros(value) -> str:
    """Format values stored in thousands of euros."""
    if value is None or pd.isna(value):
        return "-"
    return f"{value:,.0f}"


def format_pct(value) -> str:
    """Format a decimal ratio as a percentage."""
    if value is None or pd.isna(value):
        return "-"
    return f"{value * 100:.1f}%"


def get_available_years() -> list[int]:
    rows = execute_query("SELECT DISTINCT year FROM financials ORDER BY year DESC")
    return [r["year"] for r in rows]


def get_available_countries() -> list[str]:
    rows = execute_query(
        "SELECT DISTINCT country FROM companies WHERE country IS NOT NULL ORDER BY country"
    )
    return [r["country"] for r in rows]


def get_available_provinces() -> list[str]:
    rows = execute_query(
        """SELECT DISTINCT province
           FROM companies
           WHERE province IS NOT NULL
             AND trim(province) <> ''
           ORDER BY province"""
    )
    return [r["province"] for r in rows]


def get_available_cnaes() -> list[str]:
    rows = execute_query("SELECT DISTINCT cnae_code FROM companies ORDER BY cnae_code")
    return [r["cnae_code"] for r in rows]
