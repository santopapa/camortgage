from typing import Optional
import typer
from rich.prompt import FloatPrompt, IntPrompt

from camortgage.models import MortgageInput
from camortgage.rates import get_rates
from camortgage.qualify import assess_qualification
from camortgage.compare import compare_scenarios
from camortgage.lenders import fetch_lender_rates
from camortgage.display import (
    display_rates_table,
    format_rates_json,
    display_qualification_table,
    format_qualification_json,
    display_compare_table,
    format_compare_json,
    display_lenders_table,
    format_lenders_json,
    console,
)
from camortgage.constants import CA_DEFAULT_PROPERTY_TAX_RATE, CA_DEFAULT_HOME_INSURANCE

app = typer.Typer(help="California mortgage rate checker and qualification calculator.")


@app.command()
def rates(
    refresh: bool = typer.Option(False, "--refresh", help="Force refresh cached rates"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Fetch and display current California mortgage rates."""
    rate_data = get_rates(refresh=refresh)
    if json_output:
        console.print(format_rates_json(rate_data))
    else:
        display_rates_table(rate_data)


def _collect_input(
    income: Optional[float],
    debt: Optional[float],
    down: Optional[float],
    credit: Optional[int],
    price: Optional[float],
) -> MortgageInput:
    if income is None:
        income = FloatPrompt.ask("Annual income ($)")
    if debt is None:
        debt = FloatPrompt.ask("Monthly debts ($)", default=0.0)
    if down is None:
        down = FloatPrompt.ask("Down payment ($)")
    if credit is None:
        credit = IntPrompt.ask("Credit score (300-850)")
    if price is None:
        price = FloatPrompt.ask("Target home price ($)")

    return MortgageInput(
        annual_income=income,
        monthly_debts=debt,
        down_payment=down,
        credit_score=credit,
        home_price=price,
    )


@app.command()
def qualify(
    income: Optional[float] = typer.Option(None, "--income", help="Annual income"),
    debt: Optional[float] = typer.Option(None, "--debt", help="Monthly debts"),
    down: Optional[float] = typer.Option(None, "--down", help="Down payment"),
    credit: Optional[int] = typer.Option(None, "--credit", help="Credit score"),
    price: Optional[float] = typer.Option(None, "--price", help="Target home price"),
    tax_rate: Optional[float] = typer.Option(None, "--tax-rate", help="Property tax rate"),
    hoa: Optional[float] = typer.Option(None, "--hoa", help="Monthly HOA"),
    insurance: Optional[float] = typer.Option(None, "--insurance", help="Annual insurance"),
    employment: Optional[float] = typer.Option(None, "--employment", help="Employment years"),
    rate: Optional[float] = typer.Option(None, "--rate", help="Override interest rate"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Assess mortgage qualification (interactive or flags)."""
    mi = _collect_input(income, debt, down, credit, price)
    if tax_rate is not None:
        mi.property_tax_rate = tax_rate
    if hoa is not None:
        mi.monthly_hoa = hoa
    if insurance is not None:
        mi.annual_insurance = insurance
    if employment is not None:
        mi.employment_years = employment

    if rate is None:
        rate_data = get_rates()
        interest = rate_data["30yr_fixed"]
    else:
        interest = rate

    results = assess_qualification(mi, interest_rate=interest)

    if json_output:
        console.print(format_qualification_json(results))
    else:
        display_qualification_table(results)


@app.command()
def compare(
    income: Optional[float] = typer.Option(None, "--income", help="Annual income"),
    debt: Optional[float] = typer.Option(None, "--debt", help="Monthly debts"),
    down: Optional[float] = typer.Option(None, "--down", help="Down payment"),
    credit: Optional[int] = typer.Option(None, "--credit", help="Credit score"),
    price: Optional[float] = typer.Option(None, "--price", help="Target home price"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Compare mortgage scenarios across rates and terms."""
    mi = _collect_input(income, debt, down, credit, price)

    rate_data = get_rates()
    base_rate = rate_data["30yr_fixed"]
    rates_list = [base_rate - 0.5, base_rate, base_rate + 0.5]

    scenarios = compare_scenarios(mi, rates=rates_list, terms=[15, 30])

    if json_output:
        console.print(format_compare_json(scenarios))
    else:
        display_compare_table(scenarios)


@app.command()
def lenders(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Compare mortgage rates from top US lenders (Loaning.ai, SoFi, Rocket, Chase, Wells Fargo)."""
    data = fetch_lender_rates()
    if json_output:
        console.print(format_lenders_json(data))
    else:
        display_lenders_table(data)
