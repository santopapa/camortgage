from camortgage.models import MortgageInput
from camortgage.qualify import calculate_monthly_payment


def compare_scenarios(
    mi: MortgageInput,
    rates: list[float],
    terms: list[int] | None = None,
) -> list[dict]:
    if terms is None:
        terms = [15, 30]
    loan_amount = mi.home_price - mi.down_payment
    monthly_tax = (mi.home_price * mi.property_tax_rate) / 12
    monthly_insurance = mi.annual_insurance / 12
    results = []
    for rate in rates:
        for term in terms:
            monthly_pi = calculate_monthly_payment(loan_amount, rate, term)
            total_housing = monthly_pi + monthly_tax + monthly_insurance + mi.monthly_hoa
            total_paid = monthly_pi * term * 12
            total_interest = total_paid - loan_amount
            results.append({
                "rate": rate,
                "term": term,
                "monthly_payment": round(total_housing, 2),
                "monthly_pi": round(monthly_pi, 2),
                "total_interest": round(total_interest, 2),
                "total_paid": round(total_paid, 2),
            })
    return results
