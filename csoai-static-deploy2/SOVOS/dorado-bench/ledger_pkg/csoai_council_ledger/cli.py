#!/usr/bin/env python3
"""council CLI — signed provision-conformance receipts."""
import json, sys, os, time
from . import provision_conformance, market_context, human_ai_context, signed_receipt

def main():
    if len(sys.argv) < 2:
        print("usage: council conformance <provision_id>  |  market  |  humanai <provision_id>")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "conformance" and len(sys.argv) > 2:
        c = provision_conformance(sys.argv[2], {"agent": [{"correct": True}] * 1})
        print(json.dumps(c, indent=1))
    elif cmd == "market":
        print(json.dumps(market_context(), indent=1))
    elif cmd == "humanai":
        h = human_ai_context("EU-AI-Act-2024-1689-Art6", human=[{"correct":True}]*3, ai=[{"correct":True}]*2+[{"correct":False}])
        print(json.dumps(h, indent=1))
    elif cmd == "receipt":
        key = os.environ.get("COUNCIL_KEY", "")
        print(json.dumps(signed_receipt(provision_conformance("EU-AI-Act-2024-1689-Art6", {"agent":[{"correct":True}]*1}), key_hex=key), indent=1))
    else:
        print("unknown command")
        sys.exit(1)

if __name__ == "__main__":
    main()
