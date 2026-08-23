#!/usr/bin/env python3
"""claimguard CLI — production entry point."""
import json, sys, os
from . import check, signed_report

def main():
    if len(sys.argv) < 2:
        print("usage: claimguard check <board.json> ['{\"key\": value}']")
        print("       claimguard signed <board.json> ['{\"key\": value}']  (needs CLAIMGUARD_KEY)")
        sys.exit(1)
    cmd = sys.argv[1]
    board = sys.argv[2] if len(sys.argv) > 2 else "board.json"
    claimed = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    if cmd == "check":
        print(json.dumps(check(board, claimed), indent=1))
    elif cmd == "signed":
        print(json.dumps(signed_report(board, claimed), indent=1))
    else:
        print(f"unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
