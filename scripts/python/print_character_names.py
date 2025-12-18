#!/usr/bin/env python3
"""Simple test script to call /nes/names/get and print the JSON result."""
import json
import os
import urllib.request
import urllib.error


def main():
    port = os.environ.get('NES_API_PORT', '5000')
    url = f'http://localhost:{port}/nes/names/get'

    data = json.dumps({}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json'
    }, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8')
            try:
                parsed = json.loads(body)
                print(json.dumps(parsed, indent=2))
            except Exception:
                # Not JSON? print raw
                print(body)
    except urllib.error.HTTPError as e:
        print(f'HTTPError: {e.code} {e.reason}')
        try:
            print(e.read().decode())
        except Exception:
            pass
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
