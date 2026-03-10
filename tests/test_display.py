import json
from camortgage.display import format_rates_json, format_qualification_json, format_compare_json


def test_format_rates_json():
    rates = {"30yr_fixed": 6.42, "15yr_fixed": 5.68, "date": "03/06/2026"}
    result = format_rates_json(rates)
    parsed = json.loads(result)
    assert parsed["30yr_fixed"] == 6.42


def test_format_qualification_json():
    results = {
        "conventional": {
            "label": "Conventional",
            "result": "LIKELY",
            "front_dti": 0.25,
            "back_dti": 0.30,
            "ltv": 0.75,
            "monthly_payment": 2500.0,
            "reasons": [],
            "pmi_note": None,
        }
    }
    result = format_qualification_json(results)
    parsed = json.loads(result)
    assert parsed["conventional"]["result"] == "LIKELY"


def test_format_compare_json():
    scenarios = [{"rate": 6.5, "term": 30, "monthly_payment": 2500.0, "monthly_pi": 2000.0, "total_interest": 420000.0, "total_paid": 720000.0}]
    result = format_compare_json(scenarios)
    parsed = json.loads(result)
    assert parsed[0]["rate"] == 6.5
