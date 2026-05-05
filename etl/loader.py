"""
File loading for SABI exports.

The supported SABI format is wide: one row per company, one column per
metric/relative year. The loader converts it to the app's normalized long
format: one row per company-year.
"""

from datetime import date, datetime
import os
import re

import pandas as pd


HEADER_FIELDS = [
    "company_name",
    "cif",
    "bvd_id",
    "date_of_establishment",
    "website",
    "country",
    "province",
    "guo_name",
    "cnae_code",
    "native_trade_description",
    "english_trade_description",
]

FINANCIAL_FIELDS = [
    "cash_and_equivalents",
    "total_assets",
    "working_capital",
    "employees",
    "revenue",
    "cost_of_goods_sold",
    "ebitda",
    "long_term_debts",
    "short_term_debts",
    "equity",
    "net_income",
    "cash_flow",
]

SABI_HEADER_MAP = {
    "company name": "company_name",
    "nif code": "cif",
    "bvd id": "bvd_id",
    "date of establishment": "date_of_establishment",
    "web site": "website",
    "country": "country",
    "province": "province",
    "guo - name": "guo_name",
    "cae rev.3 primary code": "cnae_code",
    "last available year": "last_available_year",
    "native trade description": "native_trade_description",
    "english trade description": "english_trade_description",
}

SABI_FINANCIAL_MAP = {
    "cash & cash equivalent": "cash_and_equivalents",
    "total assets": "total_assets",
    "working capital": "working_capital",
    "number of employees": "employees",
    "operating revenue / turnover": "revenue",
    "cost of goods sold": "cost_of_goods_sold",
    "ebitda": "ebitda",
    "long term debts": "long_term_debts",
    "short term debts": "short_term_debts",
    "shareholders' equity": "equity",
    "p/l for period": "net_income",
    "cash flow": "cash_flow",
}

PERIOD_OFFSETS = {
    "last avail. yr": 0,
    "year - 1": 1,
    "year - 2": 2,
    "year - 3": 3,
    "year - 4": 4,
    "year - 5": 5,
    "year - 6": 6,
}

MISSING_VALUES = {"", "n.a.", "na", "n/a", "nan", "none", "-"}


def load_file(file_path_or_buffer, file_name: str = "") -> pd.DataFrame:
    """
    Read a CSV/Excel file and return normalized long-form rows.

    SABI exports are detected by their original headers. The previous internal
    long format is still accepted to keep tests and hand-made CSVs usable.
    """
    name = file_name if file_name else str(file_path_or_buffer)
    ext = os.path.splitext(name)[1].lower()

    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(file_path_or_buffer, dtype=object, engine="openpyxl")
    else:
        raise ValueError(
            f"Formato de archivo no soportado: {ext}. Sube un Excel .xlsx o .xls."
        )

    df = df.dropna(axis=1, how="all")
    original_columns = list(df.columns)
    normalized_columns = [_normalize_header(c) for c in original_columns]

    if "last available year" in normalized_columns:
        return _load_sabi_wide(df, normalized_columns)

    df.columns = [_slug(c) for c in original_columns]
    if "year" not in df.columns:
        raise ValueError(
            "El archivo no tiene columna 'year' ni parece una exportación SABI "
            "con 'Last available year'."
        )
    return df.where(pd.notna(df), None)


def _load_sabi_wide(df_wide: pd.DataFrame, normalized_columns: list[str]) -> pd.DataFrame:
    """Convert the SABI wide export to normalized company-year rows."""
    column_map = _build_sabi_column_map(normalized_columns)
    rows = []

    for _, row in df_wide.iterrows():
        base_year = _extract_year(_value(row, column_map.get("last_available_year")))
        if base_year is None:
            continue

        header = {
            field: _clean_value(_value(row, column_map.get(field)))
            for field in HEADER_FIELDS
        }

        for offset in range(7):
            year = base_year - offset
            financial = {}
            all_empty = True

            for field in FINANCIAL_FIELDS:
                value = _clean_value(_value(row, column_map.get((field, offset))))
                financial[field] = value
                if value is not None:
                    all_empty = False

            if all_empty:
                continue

            rows.append({**header, "year": year, **financial})

    return pd.DataFrame(rows, columns=HEADER_FIELDS + ["year"] + FINANCIAL_FIELDS)


def _build_sabi_column_map(normalized_columns: list[str]) -> dict:
    """Map normalized SABI headers to internal fields."""
    mapping = {}

    for index, header in enumerate(normalized_columns):
        if header in SABI_HEADER_MAP:
            mapping[SABI_HEADER_MAP[header]] = index
            continue

        base_name, offset = _parse_financial_header(header)
        if base_name is None:
            continue

        field = SABI_FINANCIAL_MAP.get(base_name)
        if field is not None:
            mapping[(field, offset)] = index

    return mapping


def _parse_financial_header(header: str) -> tuple[str | None, int | None]:
    parts = [p.strip() for p in header.split("\n") if p.strip()]
    if not parts:
        return None, None

    period = parts[-1]
    if period not in PERIOD_OFFSETS:
        return None, None

    return parts[0], PERIOD_OFFSETS[period]


def _value(row, index):
    if index is None:
        return None
    return row.iloc[index]


def _clean_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return None if stripped.lower() in MISSING_VALUES else stripped
    if isinstance(value, (datetime, date)):
        return value.date() if isinstance(value, datetime) else value
    return value


def _extract_year(value) -> int | None:
    value = _clean_value(value)
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.year
    try:
        return int(float(str(value)[:4]))
    except (TypeError, ValueError):
        return None


def _normalize_header(column) -> str:
    if column is None:
        return ""
    return re.sub(r"[ \t]+", " ", str(column).strip().lower())


def _slug(column) -> str:
    text = _normalize_header(column)
    text = text.replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")
