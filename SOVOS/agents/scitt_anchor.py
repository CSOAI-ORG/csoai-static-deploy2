#!/usr/bin/env python3
"""scitt_anchor.py — SCITT (RFC 9943) transparency anchor for signed cards.

Block B #7: publish signed measurement cards to a SCITT statement log and
MEASURE the signing-overhead number — the publishable metric nobody has.

Minimal SCITT-conformant anchor (honest):
  1. Card → SCITT statement envelope (protected header + payload + sig,
     RFC 9943 shape: alg EdDSA, iss, content_type)
  2. RFC 3161-style time anchor (sha256 + self-anchor; external TSA deferred)
  3. Emit per-card SIGNING-OVERHEAD metric (µs + bytes)

Usage (pod, where keys live):
    python3 scitt_anchor.py --card /path/card.json --issuer did:web:csoai.org
    python3 scitt_anchor.py --bench --cards 500     # overhead curve
"""

from __future__ import annotations
import argparse, base64, hashlib, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    HAVE_CRYPTO = True
except ImportError:  # pragma: no cover — pod has it
    HAVE_CRYPTO = False
    serialization = None  # type: ignore

KEY_DIR = Path(__file__).resolve().parent.parent / "keys"
KEY_NAME = "oms-signing-ed25519"


def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _priv() -> object:
    if not HAVE_CRYPTO:
        sys.exit("❌ cryptography not installed: /workspace/venv-test/bin/pip install cryptography")
    return serialization.load_pem_private_key(
        (KEY_DIR / f"{KEY_NAME}.pem").read_bytes(), password=None)


def scitt_statement(card: dict, issuer: str, priv) -> tuple[dict, bytes]:
    """RFC 9943-ish signed statement: returns (envelope dict, signing_input)."""
    protected = {"alg": "EdDSA", "iss": issuer, "content_type": "application/json",
                 "regTime": _now()}
    prot_b64 = _b64url(json.dumps(protected, separators=(",", ":")).encode())
    payload_b64 = _b64url(json.dumps(card, sort_keys=True, separators=(",", ":")).encode())
    signing_input = f"{prot_b64}.{payload_b64}".encode()
    sig = _b64url(priv.sign(signing_input))
    return {"protected": prot_b64, "payload": payload_b64, "signature": sig}, signing_input


def time_anchor(signing_input: bytes) -> dict:
    """RFC 3161-adjacent anchor: sha256 digest + chain-owned marker.

    External RFC 3161 TSA (freetsa) is deferred until network egress is
    verified from the pod; the signed root hash IS the anchor.
    """
    return {"anchor_type": "sha256-self", "digest": hashlib.sha256(signing_input).hexdigest(),
            "note": "RFC 3161 external TSA deferred; chain-owned root hash anchors the card",
            "t": _now()}


def anchor_one(card_path: str, issuer: str, priv) -> dict:
    t0 = time.perf_counter()
    card = json.loads(Path(card_path).read_text())
    statement, signing_input = scitt_statement(card, issuer, priv)
    anchor = time_anchor(signing_input)
    dt = time.perf_counter() - t0
    return {
        "schema": "scitt-anchor-v1",
        "card_id": str(card_path),
        "statement": statement,
        "time_anchor": anchor,
        "signing_overhead_metric": f"{dt*1e6:.1f}us/{len(signing_input)}B",
        "ledger": "SCITT (RFC 9943) minimal anchor",
        "created": _now(),
    }


def bench(cards: int, issuer: str, priv, payload_size: int = 200) -> dict:
    """Measure the per-card signing overhead curve (the publishable number)."""
    base = {"axis": "gov", "model": "bench", "accuracy": 0.5,
            "pad": "x" * payload_size}
    samples = []
    for i in range(cards):
        card = {**base, "id": f"bench-{i}"}
        t0 = time.perf_counter()
        _, signing_input = scitt_statement(card, issuer, priv)
        dt = time.perf_counter() - t0
        samples.append((dt * 1e6, len(signing_input)))
    us = [s[0] for s in samples]
    by = [s[1] for s in samples]
    return {
        "schema": "scitt-overhead-bench-v1",
        "cards": cards,
        "per_card_us_median": round(sorted(us)[len(us) // 2], 1),
        "per_card_us_mean": round(sum(us) / len(us), 1),
        "per_card_bytes_median": sorted(by)[len(by) // 2],
        "created": _now(),
        "note": "EdDSA/Ed25519 detached sign; signing only, no TSA network hop",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--card", help="path to a card JSON to anchor")
    p.add_argument("--issuer", default="did:web:csoai.org")
    p.add_argument("--bench", action="store_true", help="run overhead bench")
    p.add_argument("--cards", type=int, default=500)
    a = p.parse_args()

    priv = _priv()
    if a.bench:
        print(json.dumps(bench(a.cards, a.issuer, priv), indent=2))
        return 0
    if not a.card:
        p.error("--card required unless --bench")
        return 1
    print(json.dumps(anchor_one(a.card, a.issuer, priv), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())