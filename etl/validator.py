"""
Validation for normalized company-year rows.
"""

import pandas as pd


REQUIRED_COLUMNS = [
    "company_name", "cif", "cnae_code", "year",
]

NUMERIC_FIELDS = [
    "year", "cash_and_equivalents", "total_assets", "working_capital",
    "employees", "revenue", "cost_of_goods_sold", "ebitda",
    "long_term_debts", "short_term_debts", "equity", "net_income",
    "cash_flow",
]

NON_NEGATIVE_FIELDS = [
    "cash_and_equivalents", "total_assets", "employees", "revenue",
    "cost_of_goods_sold", "long_term_debts", "short_term_debts", "equity",
]


def validate(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return valid and rejected rows with rejection reasons."""
    if df.empty:
        return df.copy(), pd.DataFrame()

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Columnas obligatorias ausentes: {', '.join(missing_cols)}"
        )

    df = df.copy()
    for field in NUMERIC_FIELDS:
        if field not in df.columns:
            df[field] = None

    df["_row_number"] = range(2, len(df) + 2)
    rejected_rows = []

    for col in NUMERIC_FIELDS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    financial_fields = [c for c in NUMERIC_FIELDS if c != "year"]
    all_financial_na = df[financial_fields].isna().all(axis=1)
    df = df[~all_financial_na].copy()

    if df.empty:
        return df, pd.DataFrame()

    valid_year_mask = df["year"].between(1990, 2035)
    for idx in df[~valid_year_mask].index:
        rejected_rows.append((idx, f"Año fuera de rango (1990-2035): {df.at[idx, 'year']}"))

    for col in REQUIRED_COLUMNS:
        empty_mask = df[col].isna() | (df[col].astype(str).str.strip() == "")
        for idx in df[empty_mask].index:
            if idx not in {r[0] for r in rejected_rows}:
                rejected_rows.append((idx, f"{col} vacío"))

    dup_key = (
        df["company_name"].astype(str).str.strip().str.lower()
        + "_"
        + df["year"].astype(str)
    )
    dup_mask = dup_key.duplicated(keep="first")
    for idx in df[dup_mask].index:
        if idx not in {r[0] for r in rejected_rows}:
            rejected_rows.append((idx, "Duplicado empresa-año dentro del fichero"))

    for col in NON_NEGATIVE_FIELDS:
        neg_mask = df[col].notna() & (df[col] < 0)
        for idx in df[neg_mask].index:
            if idx not in {r[0] for r in rejected_rows}:
                rejected_rows.append((idx, f"{col} no puede ser negativo: {df.at[idx, col]}"))

    rejected_indices = {r[0] for r in rejected_rows}
    df_valid = df[~df.index.isin(rejected_indices)].copy()
    df_rejected = df[df.index.isin(rejected_indices)].copy()

    reason_map = {}
    for idx, reason in rejected_rows:
        reason_map[idx] = f"{reason_map[idx]} | {reason}" if idx in reason_map else reason

    if not df_rejected.empty:
        df_rejected["rejection_reason"] = df_rejected.index.map(reason_map)

    df_valid.drop(columns=["_row_number"], inplace=True, errors="ignore")
    df_rejected.drop(columns=["_row_number"], inplace=True, errors="ignore")

    return df_valid, df_rejected
