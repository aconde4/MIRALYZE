from io import BytesIO

import pandas as pd
import pytest

from etl.loader import load_file


def _to_xlsx_buffer(df: pd.DataFrame) -> BytesIO:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    return buffer


def test_load_file_converts_sabi_wide_export_to_long_rows():
    source = pd.DataFrame(
        [
            {
                "Company Name": "ACME SL",
                "NIF Code": "B12345678",
                "BvD ID": "ES123456",
                "Date of Establishment": "21/10/1870",
                "Web site": "https://example.com",
                "Country": "SPAIN",
                "Province": "Madrid",
                "GUO - Name": "ACME GROUP",
                "CAE Rev.3 Primary Code": "4511",
                "Last available year": "2024-12-31",
                "Native trade description": "Venta, mantenimiento",
                "English trade description": "Sale and maintenance",
                "Operating revenue / turnover\nth EUR\nLast avail. yr": 1000,
                "Operating revenue / turnover\nth EUR\nYear - 1": 800,
                "EBITDA\nth EUR\nLast avail. yr": 200,
                "EBITDA\nth EUR\nYear - 1": 120,
                "Cash flow\nth EUR\nLast avail. yr": "n.a.",
            }
        ]
    )

    result = load_file(_to_xlsx_buffer(source), "sabi_sample.xlsx")

    assert list(result["year"]) == [2024, 2023]
    assert result.loc[0, "company_name"] == "ACME SL"
    assert result.loc[0, "cif"] == "B12345678"
    assert result.loc[0, "cnae_code"] == "4511"
    assert result.loc[0, "revenue"] == 1000
    assert result.loc[1, "revenue"] == 800
    assert result.loc[0, "ebitda"] == 200
    assert result.loc[1, "ebitda"] == 120
    assert result.loc[0, "cash_flow"] is None


def test_load_file_rejects_csv_input():
    with pytest.raises(ValueError, match="Formato de archivo no soportado"):
        load_file(BytesIO(b"company_name,year\nACME,2024\n"), "sample.csv")
