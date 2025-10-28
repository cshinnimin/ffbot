#!/usr/bin/env python3
"""
CLI helper to POST a JSON payload to the /nes/write endpoint.

Usage:
  python scripts/python/write_ram.py '{"addresses": [{"0x006BE4":"0x05"}]}'

The script expects a JSON string on the command line (or read from stdin if '-' is provided).
It parses the string into JSON and posts it as the request body (Content-Type: application/json).
On success it prints 'NES RAM successfully updated'.
"""
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests

# Ensure repository root is on sys.path so imports like `from load_env import load_env`
# work regardless of the current working directory. We look upward from this
# script and stop when we find a marker that indicates the repo root.
repo_root = Path(__file__).resolve()
for _ in range(6):
    if (repo_root / ".env").exists() or (repo_root / "README.md").exists() or (repo_root / "api").exists():
        break
    if repo_root.parent == repo_root:
        break
    repo_root = repo_root.parent
sys.path.insert(0, str(repo_root))

from load_env import load_env
load_env()

def load_payload_from_arg(arg: str) -> Any:
    if arg == '-':
        raw = sys.stdin.read()
    else:
        raw = arg
    try:
        payload = json.loads(raw)
    except Exception as e:
        print(f"Failed to parse JSON input: {e}")
        sys.exit(2)
    return payload


def main():
    parser = argparse.ArgumentParser(description='POST JSON to /nes/write')
    parser.add_argument('json', help='JSON string to send (use - to read from stdin)')
    parser.add_argument('--host', default=os.environ.get('NES_API_HOST', 'localhost'))
    parser.add_argument('--port', default=os.environ.get('NES_API_PORT', '5000'))
    args = parser.parse_args()

    payload = load_payload_from_arg(args.json)

    url = f"http://{args.host}:{args.port}/nes/write"

    try:
        resp = requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(3)

    if resp.ok:
        print('NES RAM successfully updated')
        sys.exit(0)
    else:
        try:
            print('Error:', resp.json())
        except Exception:
            print('Error:', resp.status_code, resp.text)
        sys.exit(4)


if __name__ == '__main__':
    main()
