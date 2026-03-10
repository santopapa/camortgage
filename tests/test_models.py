import pytest
from camortgage.constants import LOAN_TYPES
from camortgage.models import MortgageInput


def test_loan_types_has_three_types():
    assert set(LOAN_TYPES.keys()) == {"conventional", "fha", "va"}


def test_conventional_thresholds():
    conv = LOAN_TYPES["conventional"]
    assert conv["front_dti_max"] == 0.28
    assert conv["back_dti_max"] == 0.36
    assert conv["max_ltv"] == 0.80
    assert conv["min_credit"] == 620


def test_valid_input():
    mi = MortgageInput(
        annual_income=120000,
        monthly_debts=500,
        down_payment=80000,
        credit_score=740,
        home_price=400000,
    )
    assert mi.annual_income == 120000
    assert mi.property_tax_rate == 0.011  # CA default


def test_invalid_credit_score():
    with pytest.raises(ValueError):
        MortgageInput(
            annual_income=120000,
            monthly_debts=500,
            down_payment=80000,
            credit_score=200,
            home_price=400000,
        )


def test_down_payment_exceeds_price():
    with pytest.raises(ValueError):
        MortgageInput(
            annual_income=120000,
            monthly_debts=500,
            down_payment=500000,
            credit_score=740,
            home_price=400000,
        )
