from camortgage.lenders import fetch_lender_rates


def test_fetch_lender_rates_returns_list():
    lenders = fetch_lender_rates()
    assert isinstance(lenders, list)
    assert len(lenders) >= 1


def test_lender_data_has_required_fields():
    lenders = fetch_lender_rates()
    required = {"lender", "rate", "apr", "points", "monthly_payment", "date"}
    for l in lenders:
        assert required.issubset(l.keys()), f"Missing fields in {l['lender']}"


def test_lenders_sorted_by_rate():
    lenders = fetch_lender_rates()
    rates = [l["rate"] for l in lenders]
    assert rates == sorted(rates)
