import pytest

from metrics.calculator import _compute_metrics


def _financial_row(**overrides):
    row = {
        "revenue": 100.0,
        "ebitda": 20.0,
        "net_income": 10.0,
        "total_assets": 200.0,
        "equity": 80.0,
        "cash_and_equivalents": 5.0,
        "long_term_debts": 40.0,
        "short_term_debts": 10.0,
        "employees": 10.0,
        "cash_flow": 12.0,
    }
    row.update(overrides)
    return row


def test_compute_metrics_calculates_debt_margins_growth_and_productivity():
    data_by_year = {
        2023: _financial_row(revenue=100.0, ebitda=20.0),
        2024: _financial_row(
            revenue=120.0,
            ebitda=30.0,
            net_income=12.0,
            cash_and_equivalents=5.0,
            long_term_debts=50.0,
            short_term_debts=10.0,
            cash_flow=15.0,
        ),
    }

    metrics = _compute_metrics(data_by_year[2024], 2024, data_by_year)

    assert metrics["gross_debt"] == 60.0
    assert metrics["net_debt"] == 55.0
    assert metrics["ebitda_margin"] == pytest.approx(0.25)
    assert metrics["net_income_margin"] == pytest.approx(0.10)
    assert metrics["cash_flow_margin"] == pytest.approx(0.125)
    assert metrics["revenue_growth_yoy"] == pytest.approx(0.20)
    assert metrics["ebitda_growth_yoy"] == pytest.approx(0.50)
    assert metrics["net_debt_ebitda"] == pytest.approx(55.0 / 30.0)
    assert metrics["revenue_per_employee"] == pytest.approx(12.0)
    assert metrics["ebitda_per_employee"] == pytest.approx(3.0)
    assert metrics["cash_flow_per_employee"] == pytest.approx(1.5)
    assert metrics["cash_conversion"] == pytest.approx(0.5)
    assert metrics["equity_ratio"] == pytest.approx(0.4)


def test_compute_metrics_respects_partial_and_missing_debt_rules():
    partial_debt = _compute_metrics(
        _financial_row(
            long_term_debts=None,
            short_term_debts=25.0,
            cash_and_equivalents=5.0,
        ),
        2024,
        {2024: _financial_row()},
    )
    missing_debt = _compute_metrics(
        _financial_row(
            long_term_debts=None,
            short_term_debts=None,
            cash_and_equivalents=5.0,
        ),
        2024,
        {2024: _financial_row()},
    )
    missing_cash = _compute_metrics(
        _financial_row(
            long_term_debts=10.0,
            short_term_debts=None,
            cash_and_equivalents=None,
        ),
        2024,
        {2024: _financial_row()},
    )

    assert partial_debt["gross_debt"] == 25.0
    assert partial_debt["net_debt"] == 20.0
    assert missing_debt["gross_debt"] is None
    assert missing_debt["net_debt"] is None
    assert missing_cash["gross_debt"] == 10.0
    assert missing_cash["net_debt"] is None
