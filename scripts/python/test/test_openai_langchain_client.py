#!/usr/bin/env python3
"""
Test script for OpenAILangchainLlmClient

Usage:
  python test_openai_langchain_client.py "Hi"

This script will instantiate the client, and print the response
"""

import os
import sys
from pathlib import Path

# Add folders where imports live to sys.path so package imports work
API_DIR = Path(__file__).resolve().parents[3]
LOAD_ENV_DIR = Path(__file__).resolve().parents[1];
sys.path.insert(0, str(API_DIR))
sys.path.insert(0, str(LOAD_ENV_DIR))

from load_env import load_env
load_env()

# Import the OpenAILangchainLlmClient
try:
    from api.llm.llm_client.langchain_client.openai_langchain_client import OpenAILangchainLlmClient
except Exception as e:
    print("Failed to import OpenAILangchainLlmClient:", e)
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
    "LLM_TEMPERATURE": _maybe_float(os.environ.get("LLM_TEMPERATURE")),
}

client = OpenAILangchainLlmClient(config)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": message},
]

print("Sending message:", message)

temperature = 0

try:
    response = client.chat(messages, temperature=temperature)
    print("\nResponse:\n", response)
except Exception as e:
    print("Error calling chat:", e)
    sys.exit(2)
