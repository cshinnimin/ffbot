#!/usr/bin/env python3
"""
Script to print contents of RAMDisk ram_contents.json that relate to ememy data, for debugging

Usage:
    python print_monster_data.py
"""
import json
import os
import sys
from pathlib import Path

def main():
    from load_env import load_env
    load_env()

    ramdisk = os.environ.get("RAMDISK_DIR")
    if not ramdisk:
        print("RAMDISK_DIR environment variable is not set", file=sys.stderr)
        sys.exit(2)

    path = os.path.join(ramdisk, "ram_contents.json")
    if not os.path.exists(path):
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(3)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # keys are hex addresses like "0x006BD3" sorted low to high in the file
    # We'll construct the list of keys in sorted order to be safe.
    keys = sorted(data.keys(), key=lambda k: int(k, 16))

    # Build a mapping from integer address to value (strip leading 0x)
    addr_to_val = {}
    for k in keys:
        v = data[k]
        if isinstance(v, str) and v.startswith("0x"):
            addr_to_val[int(k, 16)] = v[2:]
        else:
            # If value doesn't match expected pattern, still coerce to two-char hex
            s = str(v)
            if s.startswith("0x"):
                s = s[2:]
            addr_to_val[int(k, 16)] = s[-2:]

    # Start address for first line
    start = int("0x006BD3", 16)
    lines = []
    cur = start
    for line_idx in range(9):
        tokens = []
        for i in range(20):
            val = addr_to_val.get(cur)
            if val is None:
                # If missing, use two spaces placeholder
                token = "  "
            else:
                token = val.zfill(2)[-2:]
            tokens.append(token)
            cur += 1
        lines.append(" ".join(tokens))

    # Print exactly 9 lines
    for l in lines:
        print(l)


if __name__ == "__main__":
    main()
