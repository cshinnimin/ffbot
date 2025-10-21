import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
# Load root .env if present
load_dotenv(ROOT / ".env")
DEFAULTS = {
    "NES_API_PORT": 5000,
    "RAMDISK_DIR": "/tmp/ramdisk/",
}

def _load_env_overrides() -> Dict[str, Any]:
    overrides: Dict[str, Any] = {}
    for key in DEFAULTS.keys():
        env_key = key
        if env_key in os.environ:
            overrides[key] = os.environ[env_key]
    return overrides


def get_config() -> Dict[str, Any]:
    config: Dict[str, Any] = DEFAULTS.copy()
    config.update(_load_env_overrides())

    # Coerce types
    try:
        config["NES_API_PORT"] = int(config.get("NES_API_PORT", DEFAULTS["NES_API_PORT"]))
    except Exception:
        config["NES_API_PORT"] = DEFAULTS["NES_API_PORT"]

    return config
