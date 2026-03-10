from camortgage.models import MortgageInput
from camortgage.qualify import assess_qualification, calculate_monthly_payment


def test_likely_qualified_conventional():
    mi = MortgageInput(
        annual_income=150000,
        monthly_debts=500,
        down_payment=100000,
        credit_score=760,
        home_price=400000,
    )
    results = assess_qualification(mi, interest_rate=6.5)
    conv = results["conventional"]
    assert conv["result"] == "LIKELY"
    assert conv["front_dti"] < 0.28
    assert conv["back_dti"] < 0.36


def test_unlikely_low_credit():
    mi = MortgageInput(
        annual_income=150000,
        monthly_debts=500,
        down_payment=100000,
        credit_score=550,
        home_price=400000,
    )
    results = assess_qualification(mi, interest_rate=6.5)
    conv = results["conventional"]
    assert conv["result"] in ("UNLIKELY", "BORDERLINE")
    assert "credit" in conv["reasons"][0].lower()


def test_borderline_high_dti():
    mi = MortgageInput(
        annual_income=60000,
        monthly_debts=800,
        down_payment=40000,
        credit_score=700,
        home_price=350000,
    )
    results = assess_qualification(mi, interest_rate=6.5)
    conv = results["conventional"]
    assert conv["result"] in ("BORDERLINE", "UNLIKELY")


def test_calculates_monthly_payment():
    payment = calculate_monthly_payment(300000, 6.5, 30)
    assert 1890 < payment < 1900  # ~$1896
