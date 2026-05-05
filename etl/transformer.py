"""
Transform validated rows and persist them in Supabase/PostgreSQL.
"""

import pandas as pd

from database.db_manager import get_connection


COMPANY_FIELDS = [
    "company_name", "cif", "bvd_id", "date_of_establishment", "website",
    "country", "province", "guo_name", "cnae_code",
    "native_trade_description", "english_trade_description",
]

FINANCIAL_FIELDS = [
    "cash_and_equivalents", "total_assets", "working_capital", "employees",
    "revenue", "cost_of_goods_sold", "ebitda", "long_term_debts",
    "short_term_debts", "equity", "net_income", "cash_flow",
]

FINANCIAL_UPSERT_SQL = """
    INSERT INTO financials
       (company_id, year, cash_and_equivalents, total_assets, working_capital,
        employees, revenue, cost_of_goods_sold, ebitda, long_term_debts,
        short_term_debts, equity, net_income, cash_flow)
       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
       ON CONFLICT (company_id, year) DO UPDATE SET
        cash_and_equivalents = EXCLUDED.cash_and_equivalents,
        total_assets = EXCLUDED.total_assets,
        working_capital = EXCLUDED.working_capital,
        employees = EXCLUDED.employees,
        revenue = EXCLUDED.revenue,
        cost_of_goods_sold = EXCLUDED.cost_of_goods_sold,
        ebitda = EXCLUDED.ebitda,
        long_term_debts = EXCLUDED.long_term_debts,
        short_term_debts = EXCLUDED.short_term_debts,
        equity = EXCLUDED.equity,
        net_income = EXCLUDED.net_income,
        cash_flow = EXCLUDED.cash_flow
"""

BATCH_SIZE = 500


def transform_and_load(
    df_valid: pd.DataFrame,
    df_rejected: pd.DataFrame,
    file_name: str,
    file_type: str,
    load_mode: str,
    total_rows_read: int,
    progress_callback=None,
) -> dict:
    """Normalize validated data, upsert it, and register the import."""
    df_valid = df_valid.copy()
    df_valid["company_name"] = df_valid["company_name"].astype(str).str.strip()
    df_valid["cnae_code"] = (
        df_valid["cnae_code"].astype(str).str.strip().str.replace(r"[^\d]", "", regex=True)
    )
    if "cif" in df_valid.columns:
        df_valid["cif"] = df_valid["cif"].map(_clean_text).str.upper()
    if "bvd_id" in df_valid.columns:
        df_valid["bvd_id"] = df_valid["bvd_id"].map(_clean_text).str.upper()
    if "date_of_establishment" in df_valid.columns:
        df_valid["date_of_establishment"] = df_valid["date_of_establishment"].map(_parse_date)
    df_valid["_company_key"] = df_valid.apply(_company_key, axis=1)

    affected_company_ids = set()

    with get_connection() as conn:
        with conn.cursor() as cur:
            company_rows = df_valid.drop_duplicates("_company_key")
            company_ids_by_key = {}
            total_steps = len(company_rows) + len(df_valid)
            completed_steps = 0

            for _, row in company_rows.iterrows():
                company_id = _upsert_company(cur, row)
                company_ids_by_key[row["_company_key"]] = company_id
                affected_company_ids.add(company_id)
                if progress_callback:
                    completed_steps += 1
                    progress_callback(completed_steps, total_steps)

            financial_records = [
                _financial_params(company_ids_by_key[row["_company_key"]], row)
                for _, row in df_valid.iterrows()
            ]
            for chunk in _chunks(financial_records, BATCH_SIZE):
                cur.executemany(FINANCIAL_UPSERT_SQL, chunk)
                if progress_callback:
                    completed_steps += len(chunk)
                    progress_callback(completed_steps, total_steps)

            import_id = _log_import(
                cur, file_name, file_type, load_mode,
                total_rows_read, len(df_valid), len(df_rejected),
            )

            if not df_rejected.empty:
                _log_errors(cur, import_id, df_rejected)

    return {
        "import_id": import_id,
        "rows_accepted": len(df_valid),
        "rows_rejected": len(df_rejected),
        "affected_company_ids": list(affected_company_ids),
    }


def _upsert_company(cur, row) -> int:
    values = {field: _db_value(row.get(field)) for field in COMPANY_FIELDS}

    company_id = _find_company_id(
        cur,
        values.get("bvd_id"),
        values.get("cif"),
        values.get("company_name"),
    )

    if company_id:
        cur.execute(
            """UPDATE companies
               SET company_name = COALESCE(%s, company_name),
                   cif = COALESCE(%s, cif),
                   bvd_id = COALESCE(%s, bvd_id),
                   date_of_establishment = COALESCE(%s, date_of_establishment),
                   website = COALESCE(%s, website),
                   country = COALESCE(%s, country),
                   province = COALESCE(%s, province),
                   guo_name = COALESCE(%s, guo_name),
                   cnae_code = COALESCE(%s, cnae_code),
                   native_trade_description = COALESCE(%s, native_trade_description),
                   english_trade_description = COALESCE(%s, english_trade_description)
               WHERE id = %s""",
            (
                values["company_name"], values["cif"], values["bvd_id"],
                values["date_of_establishment"], values["website"], values["country"],
                values["province"], values["guo_name"], values["cnae_code"],
                values["native_trade_description"], values["english_trade_description"],
                company_id,
            ),
        )
        return company_id

    cur.execute(
        """INSERT INTO companies
           (company_name, cif, bvd_id, date_of_establishment, website, country,
            province, guo_name, cnae_code, native_trade_description,
            english_trade_description)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           RETURNING id""",
        (
            values["company_name"], values["cif"], values["bvd_id"],
            values["date_of_establishment"], values["website"], values["country"],
            values["province"], values["guo_name"], values["cnae_code"],
            values["native_trade_description"], values["english_trade_description"],
        ),
    )
    return cur.fetchone()["id"]


def _find_company_id(cur, bvd_id, cif, company_name):
    if bvd_id:
        cur.execute("SELECT id FROM companies WHERE bvd_id = %s", (bvd_id,))
        row = cur.fetchone()
        if row:
            return row["id"]
    if cif:
        cur.execute("SELECT id FROM companies WHERE upper(cif) = upper(%s)", (cif,))
        row = cur.fetchone()
        if row:
            return row["id"]
    if company_name:
        cur.execute(
            "SELECT id FROM companies WHERE lower(company_name) = lower(%s)",
            (company_name,),
        )
        row = cur.fetchone()
        if row:
            return row["id"]
    return None


def _upsert_financial(cur, company_id: int, row):
    cur.execute(FINANCIAL_UPSERT_SQL, _financial_params(company_id, row))


def _financial_params(company_id: int, row) -> tuple:
    values = [_db_value(row.get(field)) for field in FINANCIAL_FIELDS]
    return (company_id, int(row["year"]), *values)


def _log_import(cur, file_name, file_type, load_mode,
                rows_read, rows_accepted, rows_rejected) -> int:
    cur.execute(
        """INSERT INTO import_log
           (file_name, file_type, load_mode, rows_read, rows_accepted, rows_rejected)
           VALUES (%s, %s, %s, %s, %s, %s)
           RETURNING id""",
        (file_name, file_type, load_mode, rows_read, rows_accepted, rows_rejected),
    )
    return cur.fetchone()["id"]


def _log_errors(cur, import_id: int, df_rejected: pd.DataFrame):
    records = []
    for i, (_, row) in enumerate(df_rejected.iterrows()):
        row_num = row.get("_row_number", i + 2)
        reason = row.get("rejection_reason", "Error desconocido")
        records.append(
            (import_id, int(row_num) if pd.notna(row_num) else i + 2, "validation", reason)
        )
    cur.executemany(
        """INSERT INTO import_errors
           (import_id, row_number, error_type, error_description)
           VALUES (%s, %s, %s, %s)""",
        records,
    )


def _company_key(row) -> tuple:
    bvd_id = _clean_text(row.get("bvd_id"))
    if bvd_id:
        return ("bvd_id", str(bvd_id).upper())
    cif = _clean_text(row.get("cif"))
    if cif:
        return ("cif", str(cif).upper())
    return ("name", str(row.get("company_name", "")).strip().lower())


def _db_value(value):
    value = _clean_text(value)
    if value is None:
        return None
    return value


def _clean_text(value):
    if value is None or pd.isna(value):
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else None
    return value


def _parse_date(value):
    value = _clean_text(value)
    if value is None:
        return None
    if hasattr(value, "date") and not isinstance(value, str):
        return value.date()
    text = str(value).strip()
    if "/" in text:
        parsed = pd.to_datetime(text, errors="coerce", dayfirst=True)
    else:
        parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.date()


def _chunks(values: list[tuple], size: int):
    for start in range(0, len(values), size):
        yield values[start:start + size]
