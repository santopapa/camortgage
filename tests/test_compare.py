from camortgage.compare import compare_scenarios
from camortgage.models import MortgageInput


def test_compare_two_scenarios():
    mi = MortgageInput(
        annual_income=120000,
        monthly_debts=500,
        down_payment=80000,
        credit_score=740,
        home_price=400000,
    )
    scenarios = compare_scenarios(mi, rates=[6.0, 6.5, 7.0], terms=[15, 30])
    assert len(scenarios) == 6  # 3 rates x 2 terms
    assert all("monthly_payment" in s for s in scenarios)
