from typing import Any


def safe_int(v: Any) -> int:
    """
    Safely coerce a value to int.

    Returns 0 when `v` is None or when conversion fails. This mirrors the
    behaviour previously provided by `_safe_int` methods in several LLM
    client modules.
    """
    try:
        return int(v) if v is not None else 0
    except Exception:
        return 0
