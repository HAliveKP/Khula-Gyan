"""Read Member 3 settings from config.yaml (one place for every threshold)."""

from functools import lru_cache
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def get_config() -> dict:
    with open(REPO_ROOT / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def setting(name: str, default=None):
    """Return one config value, or the default if it is missing."""
    return get_config().get(name, default)
