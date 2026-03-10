import json
from rich.console import Console
from rich.table import Table
from camortgage.constants import DISCLAIMER

console = Console()

RESULT_ICONS = {
    "LIKELY": "[green]LIKELY[/green]",
    "BORDERLINE": "[yellow]BORDERLINE[/yellow]",
    "UNLIKELY": "[red]UNLIKELY[/red]",
}


def display_rates_table(rates: dict) -> None:
    table = Table(title="California Average Mortgage Rates")
    table.add_column("Type", style="cyan")
    table.add_column("Rate", style="green")
    table.add_column("Updated", style="dim")
    table.add_row("30-yr Fixed", f"{rates['30yr_fixed']:.2f}%", rates["date"])
    if rates.get("15yr_fixed") is not None:
        table.add_row("15-yr Fixed", f"{rates['15yr_fixed']:.2f}%", rates["date"])
    console.print(table)
    source = rates.get("source", "")
    if "cache" in source:
        console.print(f"[dim]Source: Freddie Mac Primary Mortgage Market Survey (PMMS) — cached data[/dim]")
    else:
        console.print(f"[dim]Source: Freddie Mac Primary Mortgage Market Survey (PMMS) — official weekly survey[/dim]")
    console.print("[dim]These are national averages published weekly (Thursdays).[/dim]")
    console.print("[dim]Actual rates vary by county, lender, credit score, and loan type.[/dim]")
    console.print("[dim]Use 'camortgage lenders' to compare rates from specific lenders.[/dim]")


def format_rates_json(rates: dict) -> str:
    return json.dumps(
        {k: v for k, v in rates.items() if k not in ("source", "fetched_at")},
        indent=2,
    )


def display_qualification_table(results: dict) -> None:
    table = Table(title="Mortgage Qualification Assessment")
    table.add_column("Loan Type", style="cyan")
    table.add_column("Front DTI", justify="right")
    table.add_column("Back DTI", justify="right")
    table.add_column("LTV", justify="right")
    table.add_column("Monthly Payment", justify="right")
    table.add_column("Result")
    for data in results.values():
        table.add_row(
            data["label"],
            f"{data['front_dti']:.1%}",
            f"{data['back_dti']:.1%}",
            f"{data['ltv']:.1%}",
            f"${data['monthly_payment']:,.0f}",
            RESULT_ICONS.get(data["result"], data["result"]),
        )
    console.print(table)
    for data in results.values():
        if data["reasons"]:
            console.print(f"\n[bold]{data['label']}[/bold]:")
            for reason in data["reasons"]:
                console.print(f"  [dim]- {reason}[/dim]")
        if data.get("pmi_note"):
            console.print(f"  [yellow]Note: {data['pmi_note']}[/yellow]")
    console.print(f"\n[dim italic]{DISCLAIMER}[/dim italic]")


def format_qualification_json(results: dict) -> str:
    return json.dumps(results, indent=2)


def display_compare_table(scenarios: list[dict]) -> None:
    table = Table(title="Mortgage Scenario Comparison")
    table.add_column("Rate", style="cyan", justify="right")
    table.add_column("Term", justify="right")
    table.add_column("Monthly Payment", style="green", justify="right")
    table.add_column("Monthly P&I", justify="right")
    table.add_column("Total Interest", style="red", justify="right")
    for s in scenarios:
        table.add_row(
            f"{s['rate']:.2f}%",
            f"{s['term']}yr",
            f"${s['monthly_payment']:,.0f}",
            f"${s['monthly_pi']:,.0f}",
            f"${s['total_interest']:,.0f}",
        )
    console.print(table)
    console.print(f"\n[dim italic]{DISCLAIMER}[/dim italic]")


def format_compare_json(scenarios: list[dict]) -> str:
    return json.dumps(scenarios, indent=2)


def display_lenders_table(lenders: list[dict]) -> None:
    if not lenders:
        console.print("[yellow]No lender data available.[/yellow]")
        return
    date = lenders[0].get("date", "N/A")
    loan_amt = lenders[0].get("loan_amount", 0)
    home_price = lenders[0].get("home_price", 0)
    # Show savings summary above table
    if len(lenders) >= 2:
        best = lenders[0]
        worst = lenders[-1]
        monthly_diff = worst["monthly_payment"] - best["monthly_payment"]
        total_diff = monthly_diff * 30 * 12
        rate_diff = worst["rate"] - best["rate"]
        console.print()
        console.print(f"  Lowest rate:  [bold green]{best['lender']}[/bold green] at [green]{best['rate']:.3f}%[/green]")
        console.print(f"  Highest rate: [bold red]{worst['lender']}[/bold red] at [red]{worst['rate']:.3f}%[/red]")
        console.print(f"  Rate gap:     [bold]{rate_diff:.3f}%[/bold]")
        console.print()
        console.print(f"  Between [bold]{best['lender']}[/bold] and [bold]{worst['lender']}[/bold], choosing the lower rate saves you:")
        console.print(f"    Monthly payment difference  [bold green]Up to ${monthly_diff:,.2f}/mo[/bold green]")
        console.print(f"    Total over 30 years         [bold green]Up to ${total_diff:,.0f}[/bold green]")
        console.print()

    table = Table(title="Top Lender Rate Comparison (30-yr Fixed)")
    table.add_column("Lender", style="cyan")
    table.add_column("Rate", style="green", justify="right")
    table.add_column("APR", justify="right")
    table.add_column("Points", justify="right")
    for i, l in enumerate(lenders):
        style = "bold" if i == 0 else None
        table.add_row(
            l["lender"],
            f"{l['rate']:.3f}%",
            f"{l['apr']:.3f}%",
            f"${l['points']:,.0f} ({l['points_rate']:.3f}%)",
            style=style,
        )
    console.print(table)
    console.print(f"[dim]Based on: Home ${home_price:,.0f} / Loan ${loan_amt:,.0f} | Updated {date}[/dim]")
    console.print(f"[dim]Source: loaning.ai/tools/compare-rates[/dim]")


def format_lenders_json(lenders: list[dict]) -> str:
    return json.dumps(lenders, indent=2)
