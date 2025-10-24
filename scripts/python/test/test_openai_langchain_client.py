#!/usr/bin/env python3
"""
Test script for OpenAILangchainClient

Usage:
  From the /scripts/python/test folder containing this script:
  set -o allexport; source ../../../.env; set +o allexport; python test_openai_langchain_client.py "Hi"

This script will try to load a .env file from the repository root using python-dotenv if available,
build a config dict from environment variables, instantiate the client, and print the response.
"""

import os
import sys
from pathlib import Path

# Ensure repo root is on sys.path so package imports work when run from repo root
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

# Try to load .env if present
env_path = ROOT / ".env"
if env_path.exists():
    try:
        from dotenv import load_dotenv

        load_dotenv(dotenv_path=str(env_path))
        print(f"Loaded .env from {env_path}")
    except Exception:
        print("python-dotenv not installed; skipping .env load")

# Import the OpenAILangchainClient
try:
    from api.llm.clients.openai_langchain_client import OpenAILangchainClient
except Exception as e:
    print("Failed to import OpenAILangchainClient:", e)
    sys.exit(1)

message = sys.argv[1] if len(sys.argv) > 1 else "Hello from CLI, respond briefly."

# Build config from environment variables
def _maybe_float(val):
    try:
        return float(val) if val is not None and val != "" else None
    except Exception:
        return None

config = {
    "LLM_API_KEY": os.environ.get("LLM_API_KEY"),
    "LLM_MODEL": os.environ.get("LLM_MODEL"),
    "LLM_URL": os.environ.get("LLM_URL"),
    "LLM_TEMPERATURE": _maybe_float(os.environ.get("LLM_TEMPERATURE")),
}

client = OpenAILangchainClient(config)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": message},
]

print("Sending message:", message)

try:
    response = client.chat(messages)
    print("\nResponse:\n", response)
except Exception as e:
    print("Error calling chat:", e)
    sys.exit(2)
