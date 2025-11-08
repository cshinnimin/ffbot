#!/usr/bin/env python3
"""
Script to (re)create the LangChain Chroma vector DB.

This script instantiates the concrete LangChain client which will
load configuration (including the OpenAI API key) and then calls
recreate_vector_db() to build the persisted vector store.

Usage:
    python3 scripts/python/recreate_vector_db.py

The script will exit with a non-zero status if the API key is not set
or if an error occurs while creating the DB.
"""
import os
import sys
import shutil
from typing import Dict, Any
from pathlib import Path

# Add folders where imports live to sys.path so package imports work
API_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(API_DIR))

from load_env import load_env
load_env()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PERSIST_DIRECTORY = str(PROJECT_ROOT / 'data' / 'chroma')

# Import the concrete client after attempting to load .env so module-level code
# can pick up environment variables if needed.
try:
    from api.llm.llm_client.langchain_client.openai_langchain_client import OpenAILangchainLlmClient
except Exception as e:
    print(f"Failed to import OpenAILangchainLlmClient: {e}")
    sys.exit(2)


def main() -> None:
    # Read required config from environment
    llm_api_key = os.environ.get("LLM_API_KEY")
    if not llm_api_key:
        print("Environment variable LLM_API_KEY is not set. Please add it and retry.")
        sys.exit(1)

    config: Dict[str, Any] = {
        "LLM_API_KEY": llm_api_key,
    }

    try:
        if os.path.exists(CHROMA_PERSIST_DIRECTORY):
            shutil.rmtree(CHROMA_PERSIST_DIRECTORY)

        client = OpenAILangchainLlmClient(config)
        # Explicitly recreate the vector DB
        client.recreate_vector_db()
        print("Vector DB created successfully.")
    except Exception as exc:
        print(f"Failed to create vector DB: {exc}")
        sys.exit(3)

if __name__ == "__main__":
    main()
