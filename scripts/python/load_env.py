from __future__ import annotations

import os
from pathlib import Path

def load_env() -> bool:
    """
    Load the .env file from the repository root.

    Behaviour:
    - Prefer python-dotenv when available
    - If python-dotenv is missing, fall back to a conservative manual parser
    - Silently return False on failure; return True on success.
    """
    try:
        # Compute repo root relative to this file: scripts/python/load_env.py
        repo_root = Path(__file__).resolve().parents[2]
        dotenv_path = repo_root / ".env"
        if not dotenv_path.exists():
            return False

        # Prefer python-dotenv when available — it handles many edge cases.
        try:
            from dotenv import load_dotenv as _load_dotenv

            # We intentionally do not override existing environment variables.
            _load_dotenv(dotenv_path=str(dotenv_path), override=False)
            print(f"Loaded .env from {dotenv_path}")

            return True
        except Exception:
            # Fallback: manual parse without overriding existing environment vars
            try:
                with dotenv_path.open("r", encoding="utf-8") as ef:
                    for line in ef:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and k not in os.environ:
                            os.environ[k] = v
                print(f"Loaded .env (manual) from {dotenv_path}")

                return True
            except Exception:
                # Give up silently
                return False
    except Exception:
        return False


__all__ = ["load_env"]
