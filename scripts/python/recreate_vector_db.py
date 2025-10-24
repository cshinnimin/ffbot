#!/usr/bin/env python3
"""
Script to (re)create the LangChain Chroma vector DB.

This script instantiates the concrete LangChain client which will
load configuration (including the OpenAI API key) and then calls
create_vector_db() to build the persisted vector store.

Usage:
    export LLM_API_KEY="sk-..."
    python3 scripts/python/recreate_vector_db.py

The script will exit with a non-zero status if the API key is not set
or if an error occurs while creating the DB.
"""
import os
import sys
from typing import Dict, Any

# Ensure the repository root is on sys.path so `from api...` imports work
# even when this script is executed from a different working directory.
# scripts/python is two levels down from the repo root, so go up twice.
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Try to load .env from the repository root (if present) using python-dotenv.
# This allows users to keep secrets in the repo .env and run the script without
# exporting variables manually. If python-dotenv isn't installed we simply skip
# this step and rely on the environment already having the variables.
try:
    from pathlib import Path

    env_path = Path(repo_root) / ".env"
    if env_path.exists():
        try:
            from dotenv import load_dotenv

            load_dotenv(dotenv_path=str(env_path))
            print(f"Loaded .env from {env_path}")
        except Exception:
            # dotenv not installed; skip loading but continue
            print("python-dotenv not installed; skipping .env load")
except Exception:
    # Any failure here is non-fatal; continue and let later checks handle missing vars
    pass

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
        client = OpenAILangchainLlmClient(config)
        # Explicitly recreate the vector DB
        client.create_vector_db()
        print("Vector DB created successfully.")
    except Exception as exc:
        print(f"Failed to create vector DB: {exc}")
        sys.exit(3)

if __name__ == "__main__":
    main()
