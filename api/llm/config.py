import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
# Load root .env if present
load_dotenv(ROOT / ".env")
DEFAULTS = {
    "LLM_URL": "http://localhost:11434/api/chat",
    "LLM_MODEL": "llama3.2:3b",
    "LLM_TEMPERATURE": 0.4,
    "LLM_KEEP_ALIVE": "30m",
    "LLM_API_KEY": "",
    "LLM_THROTTLE_DELAY": 0,
    "LLM_PROVIDER": "ollama",  # one of: openai, openrouter, ollama
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
        config["LLM_TEMPERATURE"] = float(config.get("LLM_TEMPERATURE", DEFAULTS["LLM_TEMPERATURE"]))
    except Exception:
        config["LLM_TEMPERATURE"] = DEFAULTS["LLM_TEMPERATURE"]
    try:
        config["LLM_THROTTLE_DELAY"] = int(config.get("LLM_THROTTLE_DELAY", DEFAULTS["LLM_THROTTLE_DELAY"]))
    except Exception:
        config["LLM_THROTTLE_DELAY"] = DEFAULTS["LLM_THROTTLE_DELAY"]

    return config


