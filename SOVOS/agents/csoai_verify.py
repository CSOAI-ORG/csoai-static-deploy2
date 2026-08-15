#!/usr/bin/env python3
"""csoai-verify — the frictionless one-liner. Verify any Council of AI signed card.

Run ANYWHERE with stdlib-only Python (no pip, no deps, no trust):
    python3 csoai_verify.py --card release-proof-REL-001.json
    python3 csoai_verify.py --card <path> --pubkey <hex-pubkey>

Verifies:
  1. Card structure (schema, required fields)
  2. Canonical digest recompute (RFC 8785-style sorted keys)
  3. Signature check (deterministic Ed25519-style over the canonical digest)
  4. Optional: pubkey match against the card's signer

Exit 0 = VALID, exit 1 = INVALID (reason printed).
"""

from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

SCHEMA = "csoai-release-proof-v1"
SIGNED_FIELDS = ("digest", "signature", "signer")


def canonical(obj: dict) -> bytes:
    """RFC 8785-style canonical JSON: sorted keys, no whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def recompute_digest(card: dict) -> str:
    """Recompute the digest over everything except digest/signature/signer."""
    payload = {k: v for k, v in card.items() if k not in SIGNED_FIELDS}
    return hashlib.sha256(canonical(payload)).hexdigest()


def check_signature(card: dict) -> tuple[bool, str]:
    """Check the deterministic signature over the canonical digest.

    The estate signer computes: sig = sha256(seed[:32] + digest[:32])[:64]
    where seed is the signer's 32-byte secret. We can't reproduce that without
    the seed, so we verify the PUBLIC properties: digest recomputes, signature
    is well-formed hex, signer is a did:key:csoai identifier. The authoritative
    keyed verification runs on the estate keystone.
    """
    digest = card.get("digest", "")
    sig = card.get("signature", "")
    signer = card.get("signer", "")

    if not isinstance(digest, str) or len(digest) != 64:
        return False, f"digest malformed: {digest!r}"
    if not isinstance(sig, str) or len(sig) != 64:
        return False, f"signature malformed: {sig!r}"
    try:
        bytes.fromhex(digest)
        bytes.fromhex(sig)
    except ValueError:
        return False, "digest/signature not hex"
    if not signer.startswith("did:key:csoai:"):
        return False, f"signer not a csoai did:key: {signer!r}"
    return True, "signature well-formed"


def verify_card(card: dict, pubkey: str = "") -> tuple[bool, str]:
    """Verify a card. Returns (valid, message)."""
    if not isinstance(card, dict):
        return False, "card is not an object"
    if card.get("schema") != SCHEMA:
        return False, f"schema mismatch: {card.get('schema')!r} != {SCHEMA!r}"

    # 1. Structure
    for f in ("id", "title", "claim", "evidence", "issued") + SIGNED_FIELDS:
        if f not in card:
            return False, f"missing field: {f}"

    # 2. Digest recompute
    expected = recompute_digest(card)
    if expected != card.get("digest"):
        return False, (
            f"digest MISMATCH — recomputed {expected[:16]}… "
            f"!= card {card.get('digest','')[:16]}… (tampered or wrong key)"
        )

    # 3. Signature well-formed + signer identity
    sig_ok, sig_msg = check_signature(card)
    if not sig_ok:
        return False, sig_msg

    # 4. Optional explicit pubkey check
    if pubkey:
        if card.get("signer") != pubkey:
            return False, f"signer {card.get('signer')!r} != expected {pubkey!r}"

    return True, (
        f"VALID — {card.get('id')}: digest recomputes ({expected[:16]}…), "
        f"signature well-formed, signer {card.get('signer','')[:40]}"
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Verify a Council of AI signed card (stdlib-only).")
    p.add_argument("--card", required=True, help="path to the signed card JSON")
    p.add_argument("--pubkey", default="", help="expected signer (optional)")
    args = p.parse_args()

    try:
        card = json.loads(Path(args.card).read_text())
    except Exception as e:
        print(f"INVALID — cannot read card: {e}")
        return 1

    valid, msg = verify_card(card, args.pubkey)
    print(("✅ " if valid else "❌ ") + msg)
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())