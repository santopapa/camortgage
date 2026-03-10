from pydantic import BaseModel, field_validator, model_validator
from camortgage.constants import CA_DEFAULT_PROPERTY_TAX_RATE, CA_DEFAULT_HOME_INSURANCE


class MortgageInput(BaseModel):
    annual_income: float
    monthly_debts: float
    down_payment: float
    credit_score: int
    home_price: float
    property_tax_rate: float = CA_DEFAULT_PROPERTY_TAX_RATE
    monthly_hoa: float = 0.0
    annual_insurance: float = CA_DEFAULT_HOME_INSURANCE
    employment_years: float | None = None

    @field_validator("credit_score")
    @classmethod
    def credit_score_range(cls, v: int) -> int:
        if not 300 <= v <= 850:
            raise ValueError(f"Credit score must be 300-850, got {v}")
        return v

    @field_validator("annual_income", "home_price")
    @classmethod
    def must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Value must be positive")
        return v

    @model_validator(mode="after")
    def down_payment_within_price(self) -> "MortgageInput":
        if self.down_payment >= self.home_price:
            raise ValueError("Down payment must be less than home price")
        return self
