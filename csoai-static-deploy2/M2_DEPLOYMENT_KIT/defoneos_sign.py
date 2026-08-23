#!/usr/bin/env python3
"""
defoneos_sign.py — SIGIL signing utility for DEFONEOS outputs.

Usage:
  python3 defoneos_sign.py --payload "output text"
  python3 defoneos_sign.py --file output.json --verify
"""
import json, sys, hashlib, argparse, time

SIGIL_ROOT = "77ab0e6f9d6c77e8"

def sign(payload: str, agent_did: str = "did:csoai:nicholas-001") -> dict:
    payload_hash = hashlib.sha512(payload.encode()).hexdigest()
    prev_hash = hashlib.sha512(SIGIL_ROOT.encode()).hexdigest()
    ts = int(time.time() * 1000)
    sig_payload = f"{payload_hash}|{prev_hash}|{agent_did}|{ts}".encode()
    signature = hashlib.sha256(sig_payload).hexdigest()
    return {
        "version": 1,
        "payload_hash": payload_hash,
        "prev_hash": prev_hash,
        "agent_did": agent_did,
        "ts_unix_ms": ts,
        "signature": signature
    }

def main():
    parser = argparse.ArgumentParser(description="DEFONEOS SIGIL Signer")
    parser.add_argument("--payload", help="Payload to sign")
    parser.add_argument("--file", help="File to sign")
    parser.add_argument("--verify", action="store_true", help="Verify signature")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            content = f.read()
    elif args.payload:
        content = args.payload
    else:
        print("Error: --payload or --file required")
        sys.exit(1)

    result = sign(content)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
