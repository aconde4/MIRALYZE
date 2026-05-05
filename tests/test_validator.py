import pandas as pd

from etl.validator import validate


def test_validate_accepts_negative_fields_that_can_be_negative():
    df = pd.DataFrame(
        [
            {
                "company_name": "ACME SL",
                "cif": "B12345678",
                "cnae_code": "4511",
                "year": 2024,
                "revenue": 1000,
                "working_capital": -50,
                "net_income": -20,
                "cash_flow": -10,
                "long_term_debts": None,
                "short_term_debts": 100,
            }
        ]
    )

    valid, rejected = validate(df)

    assert len(valid) == 1
    assert rejected.empty


def test_validate_rejects_duplicate_company_year_and_negative_required_amounts():
    df = pd.DataFrame(
        [
            {
                "company_name": "ACME SL",
                "cif": "B12345678",
                "cnae_code": "4511",
                "year": 2024,
                "revenue": 1000,
            },
            {
                "company_name": "ACME SL",
                "cif": "B12345678",
                "cnae_code": "4511",
                "year": 2024,
                "revenue": 900,
            },
            {
                "company_name": "BAD DATA SL",
                "cif": "B87654321",
                "cnae_code": "4631",
                "year": 2024,
                "revenue": -1,
            },
        ]
    )

    valid, rejected = validate(df)

    assert len(valid) == 1
    assert len(rejected) == 2
    reasons = " | ".join(rejected["rejection_reason"].tolist())
    assert "Duplicado" in reasons
    assert "revenue no puede ser negativo" in reasons
