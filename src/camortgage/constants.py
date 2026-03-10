LOAN_TYPES: dict[str, dict] = {
    "conventional": {
        "label": "Conventional",
        "front_dti_max": 0.28,
        "back_dti_max": 0.36,
        "max_ltv": 0.80,
        "min_credit": 620,
        "pmi_required_above_ltv": 0.80,
    },
    "fha": {
        "label": "FHA",
        "front_dti_max": 0.31,
        "back_dti_max": 0.43,
        "max_ltv": 0.965,
        "min_credit": 580,
        "min_credit_high_down": 500,
        "high_down_threshold": 0.10,
    },
    "va": {
        "label": "VA",
        "front_dti_max": None,
        "back_dti_max": 0.41,
        "max_ltv": 1.0,
        "min_credit": 620,
    },
}

CA_DEFAULT_PROPERTY_TAX_RATE = 0.011
CA_DEFAULT_HOME_INSURANCE = 1500
CACHE_TTL_HOURS = 24
CACHE_DIR = "~/.camortgage"
FREDDIE_MAC_PMMS_URL = "https://www.freddiemac.com/pmms/docs/PMMS_history.csv"

DISCLAIMER = (
    "This tool is for informational purposes only and does not guarantee "
    "actual loan approval. Consult a licensed mortgage professional."
)
