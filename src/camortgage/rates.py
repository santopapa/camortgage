import json
import csv
import io
from datetime import datetime, timedelta
from pathlib import Path

import httpx

from camortgage.constants import FREDDIE_MAC_PMMS_URL, CACHE_TTL_HOURS, CACHE_DIR


def get_cache_path() -> Path:
    return Path(CACHE_DIR).expanduser() / "cache.json"


def parse_pmms_csv(content: str) -> dict:
    reader = csv.DictReader(io.StringIO(content.strip()))
    rows = list(reader)
    if not rows:
        raise ValueError("No rate data found in CSV")
    # CSV is oldest-first; latest rate is the last row
    latest = rows[-1]
    rate_30 = latest.get("pmms30", "").strip()
    rate_15 = latest.get("pmms15", "").strip()
    return {
        "30yr_fixed": float(rate_30) if rate_30 else None,
        "15yr_fixed": float(rate_15) if rate_15 else None,
        "date": latest["date"].strip('"').strip(),
        "fetched_at": datetime.now().isoformat(),
    }


def load_cache() -> dict | None:
    cache_path = get_cache_path()
    if not cache_path.exists():
        return None
    data = json.loads(cache_path.read_text())
    fetched_at = datetime.fromisoformat(data["fetched_at"])
    if datetime.now() - fetched_at > timedelta(hours=CACHE_TTL_HOURS):
        return None
    return data


def save_cache(data: dict) -> None:
    cache_path = get_cache_path()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data, indent=2))


def fetch_rates_online() -> dict:
    response = httpx.get(FREDDIE_MAC_PMMS_URL, follow_redirects=True, timeout=10)
    response.raise_for_status()
    return parse_pmms_csv(response.text)


def get_rates(refresh: bool = False) -> dict:
    if not refresh:
        cached = load_cache()
        if cached:
            cached["source"] = "cache"
            return cached

    try:
        rates = fetch_rates_online()
        save_cache(rates)
        rates["source"] = "live"
        return rates
    except (httpx.HTTPError, httpx.TimeoutException):
        cached = load_cache()
        if cached:
            cached["source"] = "cache (offline)"
            return cached
        raise RuntimeError(
            "Cannot fetch rates and no cached data available. "
            "Use --rate flag to provide a rate manually."
        )
