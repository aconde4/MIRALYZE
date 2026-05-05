"""
Automatic calculation of derived financial metrics.
"""

import math
from decimal import Decimal

from database.db_manager import get_connection


METRICS_UPSERT_SQL = """
    INSERT INTO metrics
       (company_id, year, gross_debt, net_debt, ebitda_margin,
        net_income_margin, cash_flow_margin, revenue_growth_yoy,
        ebitda_growth_yoy, revenue_cagr_3y, revenue_cagr_5y,
        net_debt_ebitda, revenue_per_employee, ebitda_per_employee,
        cash_flow_per_employee, cash_conversion, equity_ratio)
       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
       ON CONFLICT (company_id, year) DO UPDATE SET
        gross_debt = EXCLUDED.gross_debt,
        net_debt = EXCLUDED.net_debt,
        ebitda_margin = EXCLUDED.ebitda_margin,
        net_income_margin = EXCLUDED.net_income_margin,
        cash_flow_margin = EXCLUDED.cash_flow_margin,
        revenue_growth_yoy = EXCLUDED.revenue_growth_yoy,
        ebitda_growth_yoy = EXCLUDED.ebitda_growth_yoy,
        revenue_cagr_3y = EXCLUDED.revenue_cagr_3y,
        revenue_cagr_5y = EXCLUDED.revenue_cagr_5y,
        net_debt_ebitda = EXCLUDED.net_debt_ebitda,
        revenue_per_employee = EXCLUDED.revenue_per_employee,
        ebitda_per_employee = EXCLUDED.ebitda_per_employee,
        cash_flow_per_employee = EXCLUDED.cash_flow_per_employee,
        cash_conversion = EXCLUDED.cash_conversion,
        equity_ratio = EXCLUDED.equity_ratio
"""

COMPANY_BATCH_SIZE = 500
METRICS_BATCH_SIZE = 1000


def calculate_metrics(company_ids: list[int], progress_callback=None):
    """Recalculate metrics for the selected companies."""
    company_ids = _unique_ids(company_ids)
    if not company_ids:
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            total = len(company_ids)
            processed = 0
            for company_chunk in _chunks(company_ids, COMPANY_BATCH_SIZE):
                metric_records = _build_metrics_for_companies(cur, company_chunk)
                for metric_chunk in _chunks(metric_records, METRICS_BATCH_SIZE):
                    cur.executemany(METRICS_UPSERT_SQL, metric_chunk)
                processed += len(company_chunk)
                if progress_callback:
                    progress_callback(processed, total)


def recalculate_all():
    """Recalculate metrics for every company."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM companies")
            company_ids = [row["id"] for row in cur.fetchall()]
    calculate_metrics(company_ids)


def _calculate_for_company(cur, company_id: int):
    metric_records = _build_metrics_for_companies(cur, [company_id])
    for metric_chunk in _chunks(metric_records, METRICS_BATCH_SIZE):
        cur.executemany(METRICS_UPSERT_SQL, metric_chunk)


def _build_metrics_for_companies(cur, company_ids: list[int]) -> list[tuple]:
    if not company_ids:
        return []

    placeholders = ",".join(["%s"] * len(company_ids))
    cur.execute(
        f"""SELECT company_id, year, revenue, ebitda, net_income, total_assets, equity,
                  cash_and_equivalents, long_term_debts, short_term_debts,
                  employees, cash_flow
           FROM financials
           WHERE company_id IN ({placeholders})
           ORDER BY company_id, year""",
        tuple(company_ids),
    )
    rows = cur.fetchall()

    if not rows:
        return []

    data_by_company = {}
    for row in rows:
        company_id = row["company_id"]
        data_by_company.setdefault(company_id, {})
        data_by_company[company_id][row["year"]] = {
            key: _to_float(value)
            for key, value in dict(row).items()
            if key != "company_id"
        }

    metric_records = []
    for company_id, data_by_year in data_by_company.items():
        for year, data in data_by_year.items():
            metrics = _compute_metrics(data, year, data_by_year)
            metric_records.append(_metric_params(company_id, year, metrics))
    return metric_records


def _compute_metrics(d: dict, year: int, data_by_year: dict) -> dict:
    revenue = d["revenue"]
    ebitda = d["ebitda"]
    net_income = d["net_income"]
    total_assets = d["total_assets"]
    equity = d["equity"]
    cash = d["cash_and_equivalents"]
    long_term_debts = d["long_term_debts"]
    short_term_debts = d["short_term_debts"]
    employees = d["employees"]
    cash_flow = d["cash_flow"]

    gross_debt = _safe_sum(long_term_debts, short_term_debts)
    net_debt = None
    if not _is_missing(gross_debt) and not _is_missing(cash):
        net_debt = gross_debt - cash

    return {
        "gross_debt": gross_debt,
        "net_debt": net_debt,
        "ebitda_margin": _safe_div(ebitda, revenue),
        "net_income_margin": _safe_div(net_income, revenue),
        "cash_flow_margin": _safe_div(cash_flow, revenue),
        "revenue_growth_yoy": _growth_yoy(revenue, year, "revenue", data_by_year),
        "ebitda_growth_yoy": _growth_yoy(ebitda, year, "ebitda", data_by_year),
        "revenue_cagr_3y": _cagr(revenue, year, 3, "revenue", data_by_year),
        "revenue_cagr_5y": _cagr(revenue, year, 5, "revenue", data_by_year),
        "net_debt_ebitda": _safe_div(net_debt, ebitda) if not _is_missing(ebitda) and ebitda > 0 else None,
        "revenue_per_employee": _safe_div(revenue, employees),
        "ebitda_per_employee": _safe_div(ebitda, employees),
        "cash_flow_per_employee": _safe_div(cash_flow, employees),
        "cash_conversion": _safe_div(cash_flow, ebitda),
        "equity_ratio": _safe_div(equity, total_assets),
    }


def _safe_div(numerator, denominator):
    if _is_missing(numerator) or _is_missing(denominator) or denominator == 0:
        return None
    return numerator / denominator


def _safe_sum(*args):
    non_null = [arg for arg in args if not _is_missing(arg)]
    if not non_null:
        return None
    return sum(non_null)


def _growth_yoy(current_value, year, field, data_by_year):
    prev_year = year - 1
    if prev_year not in data_by_year:
        return None
    prev_value = data_by_year[prev_year].get(field)
    if _is_missing(prev_value) or prev_value == 0 or _is_missing(current_value):
        return None
    return (current_value / prev_value) - 1


def _cagr(current_value, year, n_years, field, data_by_year):
    base_year = year - n_years
    if base_year not in data_by_year:
        return None
    base_value = data_by_year[base_year].get(field)
    if _is_missing(base_value) or base_value <= 0 or _is_missing(current_value) or current_value <= 0:
        return None
    return (current_value / base_value) ** (1 / n_years) - 1


def _is_missing(value) -> bool:
    if value is None:
        return True
    try:
        return bool(math.isnan(value))
    except (TypeError, ValueError):
        return False


def _to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    return value


def _upsert_metrics(cur, company_id: int, year: int, m: dict):
    cur.execute(METRICS_UPSERT_SQL, _metric_params(company_id, year, m))


def _metric_params(company_id: int, year: int, m: dict) -> tuple:
    return (
        company_id, year, m["gross_debt"], m["net_debt"],
        m["ebitda_margin"], m["net_income_margin"], m["cash_flow_margin"],
        m["revenue_growth_yoy"], m["ebitda_growth_yoy"],
        m["revenue_cagr_3y"], m["revenue_cagr_5y"],
        m["net_debt_ebitda"], m["revenue_per_employee"],
        m["ebitda_per_employee"], m["cash_flow_per_employee"],
        m["cash_conversion"], m["equity_ratio"],
    )


def _unique_ids(company_ids: list[int]) -> list[int]:
    return list(dict.fromkeys(int(company_id) for company_id in company_ids if company_id))


def _chunks(values: list, size: int):
    for start in range(0, len(values), size):
        yield values[start:start + size]
