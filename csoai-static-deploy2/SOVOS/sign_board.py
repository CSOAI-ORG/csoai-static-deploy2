#!/usr/bin/env python3
"""sign_board.py — canonical living-board signing (one-signer doctrine).

The board must ALWAYS be signed over its canonical form: the full board with
signature/signer/signed/sig_input STRIPPED, so re-signing is idempotent and
verifiable (the bug: a second merge hashed a board already containing a
signature, then overwrote it — making the sig unverifiable).

Usage:
  python3 sign_board.py PATH [--json-out PATH] [--ts-module PATH]
"""
from __future__ import annotations
import json, sys, hashlib
from datetime import datetime, timezone
from pathlib import Path

SIG_FIELDS = ("signature", "signer", "signed", "sig_input")


def canonical(board: dict) -> dict:
    """Board minus signature fields — the object the digest covers."""
    return {k: v for k, v in board.items() if k not in SIG_FIELDS}


def sign_board(board: dict, key) -> dict:
    """Return a copy of board with fresh signature over the canonical form."""
    out = dict(board)
    digest = hashlib.sha256(json.dumps(canonical(out), sort_keys=True).encode()).digest()
    out["signature"] = key.sign(digest).hex()
    out["signer"] = key.public_key().public_bytes(
        encoding=__import__("cryptography").hazmat.primitives.serialization.Encoding.Raw,
        format=__import__("cryptography").hazmat.primitives.serialization.PublicFormat.Raw).hex()
    out["signed"] = True
    out["sig_input"] = "sha256(canonical board minus signature fields, sort_keys)"
    return out


def verify(board: dict, key) -> bool:
    digest = hashlib.sha256(json.dumps(canonical(board), sort_keys=True).encode()).digest()
    try:
        key.public_key().verify(bytes.fromhex(board["signature"]), digest)
        return True
    except Exception:
        return False


def load_key():
    sys.path.insert(0, str(Path.home() / "clawd/councilof-ai-monorepo/packages/csoai-city/src"))
    from csoai_city.keystone import load_signing_key
    return load_signing_key()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    path = Path(sys.argv[1])
    board = json.loads(path.read_text())
    key = load_key()
    if verify(board, key):
        print(f"ALREADY VALID — no re-sign needed ({path.name})")
        return 0
    before = {k: v for k, v in board.items() if k in SIG_FIELDS}
    signed = sign_board(board, key)
    path.write_text(json.dumps(signed, indent=2) + "\n")
    print(f"RE-SIGNED {path.name}: {verify(signed, key) and 'VERIFY PASS' or 'VERIFY FAIL'}")
    if before.get("signature"):
        print(f"  (was signed with a broken chain — signature replaced)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
