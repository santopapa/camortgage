import httpx

LOANING_API_URL = "https://api.loaning.ai/v1/admin/rate-compare"

HEADERS = {
    "accept": "application/json",
    "origin": "https://loaning.ai",
    "referer": "https://loaning.ai/",
}


def fetch_lender_rates() -> list[dict]:
    response = httpx.get(
        LOANING_API_URL,
        headers=HEADERS,
        follow_redirects=True,
        timeout=10,
    )
    response.raise_for_status()
    raw = response.json()

    lenders = []
    for entry in raw:
        lenders.append({
            "lender": entry["lender"],
            "rate": float(entry["interestRate"]),
            "apr": float(entry["apr"]),
            "points": float(entry["discountPoint"]),
            "points_rate": float(entry["discountPointRate"]),
            "monthly_payment": float(entry["monthlyPrincipal"]),
            "closing_cost": float(entry["closingCost"]),
            "loan_amount": entry["loanAmount"],
            "home_price": entry["homePrice"],
            "date": entry["date"],
        })

    # Sort by rate ascending
    lenders.sort(key=lambda x: x["rate"])
    return lenders
