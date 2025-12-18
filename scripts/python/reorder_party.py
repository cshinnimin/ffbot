#!/usr/bin/env python3
"""
Simple CLI test script to call `api.nes.order.order_party`.

Usage:
  python reorder_party.py 2 4 3 1

The script will load environment variables from the repo `.env`, ensure the
repository root is on `sys.path`, import `order_party`, call it, and print
the result.
"""
import sys
import argparse
from pathlib import Path

from load_env import load_env

def main():
    load_env()

    # Ensure repo root is on sys.path so `api` package is importable
    repo_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(repo_root))

    try:
        from api.nes.order import order_party
    except Exception as e:
        print(f"Failed to import api.nes.order.order_party: {e}", file=sys.stderr)
        sys.exit(2)

    parser = argparse.ArgumentParser(description='Call order_party(slot1,slot2,slot3,slot4)')
    parser.add_argument('s1', type=int, help='destination slot 1 <- source slot N')
    parser.add_argument('s2', type=int, help='destination slot 2 <- source slot N')
    parser.add_argument('s3', type=int, help='destination slot 3 <- source slot N')
    parser.add_argument('s4', type=int, help='destination slot 4 <- source slot N')

    args = parser.parse_args()

    s = (args.s1, args.s2, args.s3, args.s4)
    print(f"Calling order_party{tuple(s)}")

    result, status = order_party(*s)

    print(f"Status: {status}")
    print("Result:")
    try:
        import json
        print(json.dumps(result, indent=2))
    except Exception:
        print(result)

    if status != 200:
        sys.exit(3)


if __name__ == '__main__':
    main()
