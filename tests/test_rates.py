from camortgage.rates import parse_pmms_csv, get_cache_path


SAMPLE_CSV = """date,pmms30,pmms30p,pmms15,pmms15p,pmms51,pmms51p,pmms51m,pmms51spread
2/26/2026,5.98,,5.44,,,,,
3/5/2026,6,,5.43,,,,,
"""


def test_parse_pmms_csv():
    rates = parse_pmms_csv(SAMPLE_CSV)
    # Last row is latest
    assert rates["30yr_fixed"] == 6.0
    assert rates["15yr_fixed"] == 5.43
    assert "date" in rates


def test_parse_pmms_csv_empty_15yr():
    csv_data = """date,pmms30,pmms30p,pmms15,pmms15p,pmms51,pmms51p,pmms51m,pmms51spread
4/2/1971,7.33, ,,,,,,
"""
    rates = parse_pmms_csv(csv_data)
    assert rates["30yr_fixed"] == 7.33
    assert rates["15yr_fixed"] is None


def test_get_cache_path():
    path = get_cache_path()
    assert path.name == "cache.json"
    assert ".camortgage" in str(path)
