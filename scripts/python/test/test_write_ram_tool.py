#!/usr/bin/env python3
"""
CLI helper to test the `write_addresses_tool` from `api/nes/write.py`.

Usage:
  python scripts/python/test/test_write_ram_tool.py '[{"0x006BE4": 50}, {"0x006BE5": 0}]'

The script accepts a single JSON string (or multiple args which will be joined)
and calls the tool exactly like LangChain would pass it.
"""
from __future__ import annotations

import sys
import json
from pathlib import Path

# Ensure repo root is on sys.path so `api` package can be imported when running
# this script from the repository root or from this scripts directory.
repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

try:
    # import the tool we want to exercise
    from api.nes.write import write_addresses_tool
except Exception as e:  # pragma: no cover - helpful error when import fails
    print(f"Failed to import write_addresses_tool: {e}", file=sys.stderr)
    sys.exit(2)


def call_tool(input_str: str) -> str:
    """Call the write_addresses_tool with the provided input string.

    The LangChain `@tool` decorator may return a Tool-like object with a
    `.run()` method, or a callable. Support both.
    """
    tool_obj = write_addresses_tool

    if hasattr(tool_obj, "run") and callable(getattr(tool_obj, "run")):
        return tool_obj.run(input_str)
    if callable(tool_obj):
        return tool_obj(input_str)

    raise RuntimeError("write_addresses_tool is not callable and has no .run()")


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv)
    if len(argv) < 2:
        print("Usage: python test_write_ram_tool.py '<json-string>'")
        return 1

    # Join all provided CLI args into a single string so quoting isn't sensitive
    input_str = " ".join(argv[1:])
    print(f"Calling write_addresses_tool with input:\n{input_str}\n")

    try:
        result = call_tool(input_str)
    except Exception as e:
        print(f"Error calling write_addresses_tool: {e}", file=sys.stderr)
        return 3

    # The tool returns a JSON string in normal cases; try to pretty-print it.
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2))
    except Exception:
        # Not JSON — print raw
        print(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
