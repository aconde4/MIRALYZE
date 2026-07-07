import pandas as pd

from views.screener import _apply_numeric_filters


def _screener_row(company, revenue, ebitda):
    return {
        "company_name": company,
        "revenue": revenue,
        "ebitda": ebitda,
        "ebitda_margin": 0.1,
        "revenue_growth_yoy": 0.05,
        "net_debt_ebitda": 2.0,
        "employees": 10,
    }


def test_apply_numeric_filters_accepts_optional_ebitda_range():
    df = pd.DataFrame(
        [
            _screener_row("Negative EBITDA SL", 1000, -50),
            _screener_row("Target EBITDA SL", 1000, 250),
            _screener_row("High EBITDA SL", 1000, 900),
            _screener_row("Missing EBITDA SL", 1000, None),
        ]
    )

    result = _apply_numeric_filters(
        df,
        rev_min=0,
        rev_max=0,
        ebitda_min=-100,
        ebitda_max=300,
        ebitda_margin_min=-100,
        rev_growth_min=-100,
        nd_ebitda_max=0,
        emp_min=0,
    )

    assert result["company_name"].tolist() == [
        "Negative EBITDA SL",
        "Target EBITDA SL",
    ]
