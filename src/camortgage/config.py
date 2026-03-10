import tomllib
from pathlib import Path
from camortgage.constants import CACHE_DIR


def load_config() -> dict:
    config_path = Path(CACHE_DIR).expanduser() / "config.toml"
    if not config_path.exists():
        return {}
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def get_default(config: dict, key: str, fallback):
    return config.get("defaults", {}).get(key, fallback)
