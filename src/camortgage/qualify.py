from camortgage.models import MortgageInput
from camortgage.constants import LOAN_TYPES


def calculate_monthly_payment(
    loan_amount: float, annual_rate_pct: float, term_years: int
) -> float:
    monthly_rate = (annual_rate_pct / 100) / 12
    n_payments = term_years * 12
    if monthly_rate == 0:
        return loan_amount / n_payments
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / (
        (1 + monthly_rate) ** n_payments - 1
    )


def assess_qualification(
    mi: MortgageInput, interest_rate: float, term_years: int = 30
) -> dict[str, dict]:
    loan_amount = mi.home_price - mi.down_payment
    monthly_pi = calculate_monthly_payment(loan_amount, interest_rate, term_years)
    monthly_tax = (mi.home_price * mi.property_tax_rate) / 12
    monthly_insurance = mi.annual_insurance / 12
    monthly_housing = monthly_pi + monthly_tax + monthly_insurance + mi.monthly_hoa
    monthly_income = mi.annual_income / 12
    front_dti = monthly_housing / monthly_income
    back_dti = (monthly_housing + mi.monthly_debts) / monthly_income
    ltv = loan_amount / mi.home_price

    results: dict[str, dict] = {}

    for loan_key, thresholds in LOAN_TYPES.items():
        reasons: list[str] = []

        # Credit check
        min_credit = thresholds["min_credit"]
        if mi.credit_score < min_credit:
            reasons.append(f"Credit score {mi.credit_score} below minimum {min_credit}")

        # FHA special: 500-579 needs 10% down
        if loan_key == "fha" and 500 <= mi.credit_score < 580:
            if mi.down_payment / mi.home_price < 0.10:
                reasons.append("FHA with score 500-579 requires 10% down payment")

        # Front-end DTI
        front_max = thresholds["front_dti_max"]
        if front_max is not None and front_dti > front_max:
            reasons.append(
                f"Front-end DTI {front_dti:.1%} exceeds {front_max:.0%} max"
            )

        # Back-end DTI
        back_max = thresholds["back_dti_max"]
        if back_dti > back_max:
            reasons.append(
                f"Back-end DTI {back_dti:.1%} exceeds {back_max:.0%} max"
            )

        # LTV
        max_ltv = thresholds["max_ltv"]
        if ltv > max_ltv:
            reasons.append(f"LTV {ltv:.1%} exceeds {max_ltv:.0%} max")

        # Determine result
        if not reasons:
            result = "LIKELY"
        elif len(reasons) == 1:
            result = "BORDERLINE"
        else:
            result = "UNLIKELY"

        pmi_note = None
        if loan_key == "conventional" and ltv > 0.80:
            pmi_note = "PMI required (LTV > 80%)"

        results[loan_key] = {
            "label": thresholds["label"],
            "result": result,
            "front_dti": front_dti,
            "back_dti": back_dti,
            "ltv": ltv,
            "monthly_payment": monthly_housing,
            "reasons": reasons,
            "pmi_note": pmi_note,
        }

    return results
