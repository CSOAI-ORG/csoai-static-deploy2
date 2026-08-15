#!/usr/bin/env python3
"""issue_human_card.py — sign a HUMAN-ARENA pass into an Ed25519 card.

Completes the "human is part of signal" doctrine: the SAME issuance spine
that signs model measurements signs human measurements. A human row and a
model row produce structurally identical signed cards (card_type differs:
`human-arena-gold-v1` vs the model card type), so the ruler measures both
species equally and both are externally verifiable offline.

Card schema: matches measure_api._emit_card output (signed, signer, epoch,
content_id, digest). The human pass (human_solver_bridge.py) emits rows;
this wraps N rows (default the run output) into one signed card whose
`content` is the human-arena pass (rows + aggregate), NOT a model verdict.

Usage (on the pod where the chain + key live):
    python3 issue_human_card.py --rows /tmp/human-pass.jsonl
"""
from __future__ import annotations
import argparse, json, sys, hashlib
from datetime import datetime, timezone
from pathlib import Path

# --- Ed25519 signing (cryptography lib lives on the pod) ---
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    HAVE_CRYPTO = True
except ImportError:  # pragma: no cover — pod has it
    HAVE_CRYPTO = False
    serialization = None  # type: ignore

CHAIN = "/workspace/jeeves-exec/SOVOS/issuance-chain.jsonl"
KEY = "/root/.sovos/city_ed25519"


def load_key(path: str) -> bytes:
    raw = Path(path).read_bytes()
    if len(raw) == 32:
        return raw
    if HAVE_CRYPTO and not raw.startswith(b"-----"):
        priv = Ed25519PrivateKey.from_private_bytes(raw)
    else:
        priv = serialization.load_pem_private_key(raw, password=None)
    priv_raw = priv.private_bytes(
        serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
        serialization.NoEncryption())
    return priv_raw


def canon_json(obj) -> bytes:  # RFC 8785-style: sorted keys, compact
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def sign(priv_bytes: bytes, payload: bytes) -> bytes:
    if HAVE_CRYPTO:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        return Ed25519PrivateKey.from_private_bytes(priv_bytes).sign(payload)
    raise RuntimeError("no Ed25519 lib")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True, help="human-pass jsonl from human_solver_bridge")
    ap.add_argument("--key", default=KEY)
    ap.add_argument("--chain", default=CHAIN)
    ap.add_argument("--skip-sign", action="store_true", help="emit unsigned (dry-run)")
    a = ap.parse_args()

    rows = [json.loads(l) for l in Path(a.rows).read_text().splitlines() if l.strip()]
    n = len(rows)
    correct = sum(1 for r in rows if r.get("correct"))
    axes = sorted({r.get("axis", "gov") for r in rows})
    elapsed_ms = sum(r.get("time_ms", 0) for r in rows)

    content = {
        "pass": "human-arena-gold-v1",
        "rows": n,
        "correct": correct,
        "accuracy": round(correct / n, 4) if n else None,
        "axes": axes,
        "total_time_ms": round(elapsed_ms, 1),
        "rows_sha256": hashlib.sha256(canon_json(rows)).hexdigest(),
    }
    card = {
        "card_type": "human-arena-gold-v1",
        "date": datetime.now(timezone.utc).isoformat(),
        "source": "human",
        "rule": "same deterministic gate + signing spine as model rows; human row is a measured subject, never the judge",
        "content": content,
    }

    if not a.skip_sign:
        priv = load_key(a.key)
        # digest computed over the card BEFORE signing fields are added
        digest = hashlib.sha256(canon_json(card)).hexdigest()
        sig = sign(priv, digest.encode()).hex()
        card["signed"] = True
        card["signer"] = Path(a.key).name
        card["content_id"] = digest[:20]
        card["signature"] = sig
        # self-verify: excise signing fields (INCLUDING signer) and recompute
        EXCISE = {"signed", "signature", "content_id", "signer"}
        body = {k: v for k, v in card.items() if k not in EXCISE}
        if hashlib.sha256(canon_json(body)).hexdigest()[:20] != card["content_id"]:
            raise RuntimeError("content_id does not self-verify — card not signed")
    else:
        card["signed"] = False

    print(json.dumps(card, indent=2))
    out = Path("/tmp/issued_human_card.json")
    out.write_text(json.dumps(card, indent=2))
    print(f"\ncard written: {out} ({out.stat().st_size} bytes) signed={card['signed']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
