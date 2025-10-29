#!/usr/bin/env python3
"""
CLI helper to POST a JSON payload to the /nes/read endpoint and pretty-print the response.

Usage:
  python scripts/python/read_ram.py '{"addresses": ["0x006BE4","0x006BE5"]}'

The script expects a JSON string on the command line (or read from stdin if '-' is provided).
It parses the string into JSON and posts it as the request body (Content-Type: application/json).
On success it pretty-prints the returned JSON.
"""
import argparse
import requests
import json
import os
import sys
from typing import Any
from pathlib import Path

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
    parser = argparse.ArgumentParser(description='POST JSON to /nes/read and pretty-print the response')
    parser.add_argument('json', help='JSON string to send (use - to read from stdin)')
    parser.add_argument('--host', default=os.environ.get('NES_API_HOST', 'localhost'))
    parser.add_argument('--port', default=os.environ.get('NES_API_PORT', '5000'))
    args = parser.parse_args()

    payload = load_payload_from_arg(args.json)

    url = f"http://{args.host}:{args.port}/nes/read"

    try:
        resp = requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(3)

    try:
        data = resp.json()
    except Exception:
        print('Non-JSON response:')
        print(resp.status_code, resp.text)
        sys.exit(4)

    if resp.ok:
        print(json.dumps(data, indent=2))
        sys.exit(0)
    else:
        print('Error response:')
        print(json.dumps(data, indent=2))
        sys.exit(5)


if __name__ == '__main__':
    main()
