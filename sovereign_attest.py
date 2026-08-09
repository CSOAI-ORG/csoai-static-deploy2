#!/usr/bin/env python3
"""sovereign_attest.py — living-attestation bundle over today's measured artefacts. (Moves 31-45)

measure → sign → verify, applied to the daily measurement outputs:
  1. MEASURE — read care_gate_eval.json + flywheel day artefact + provbench from disk
  2. SIGN    — SHA-256 over each artefact body (integrity), Ed25519 where the estate
               signing-node key is present (authorship); NEVER fabricate a signature.
  3. VERIFY  — re-hashing bodies at emit time proves the numbers in the bundle are the
               numbers on disk right now.

Honest signer state (per sign.py discipline): the Mac is a dev host — no private key
lives here. If SOVOS_SIGNING_NODE=1 and a key exists, this module Ed25519-signs; otherwise
it emits sha256 + "unsigned_on_this_host": true. An unsigned attestation is labelled
unsigned, never dressed as signed.

    python3 sovereign_attest.py                 # emit benchmark-results/attestations/YYYY-MM-DD.json
    python3 sovereign_attest.py --verify        # re-verify the latest bundle
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"
OUT_DIR = RESULTS / "attestations"

# (filename-relative-to-benchmark-results, human label)
SOURCES = [
    ("care_gate_eval.json", "EAT refusal suite — deterministic care gate (moves 41-45)"),
    ("flywheel/2026-08-09.json", "Flywheel day artefact — two-sided refusal, token efficiency"),
    ("provbench-canonical-bound.json", "ProvBench — Article 50 provenance survival"),
]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _ed25519_sign(body: bytes):
    """Attempt real Ed25519 signature. Returns (sig_b64, pub_b64) or (None, None)."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PrivateKey, Ed25519PublicKey)
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        return None, None
    if __import__("os").environ.get("SOVOS_SIGNING_NODE") != "1":
        return None, None
    key_dir = Path(__import__("os").environ.get("SOVOS_KEY_DIR", "~/.sovos_keys")).expanduser()
    priv = key_dir / "sovos_ed25519.key"
    pubf = key_dir / "sovos_ed25519.pub"
    if not priv.exists():
        return None, None
    try:
        sk = serialization.load_pem_private_key(priv.read_bytes(), password=None)
        sig = sk.sign(body)
        pub = pubf.read_text().strip() if pubf.exists() else None
        import base64
        return base64.b64encode(sig).decode(), pub
    except Exception:
        return None, None


def collect() -> dict:
    artefacts = []
    for rel, label in SOURCES:
        p = RESULTS / rel
        if not p.exists():
            artefacts.append({"path": rel, "present": False, "label": label})
            continue
        raw = p.read_bytes()
        artefacts.append({
            "path": rel, "present": True, "label": label,
            "sha256": _sha256(p), "bytes": len(raw),
        })
    return {"artefacts": artefacts}


def emit() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = {
        "kind": "living-training-attestation",
        "timestamp": stamp,
        "scope": "flywheel daily measurement artefacts",
        "artefacts": collect()["artefacts"],
    }
    canonical = json.dumps(body, sort_keys=True).encode()
    sig_b64, pub = _ed25519_sign(canonical)
    bundle = {
        "kind": "living-training-attestation",
        "timestamp": stamp,
        "unsigned_on_this_host": sig_b64 is None,
        "signature_scheme": "ed25519" if sig_b64 else "sha256-integrity-only",
        "ed25519_signature": sig_b64,
        "ed25519_public_key": pub,
        "canonical_body_sha256": hashlib.sha256(canonical).hexdigest(),
        **{f"artefact_{i}": a for i, a in enumerate(body["artefacts"])},
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    day = stamp[:10]
    out = OUT_DIR / f"{day}.json"
    out.write_text(json.dumps(bundle, indent=2))
    return out


def verify(latest: bool = False) -> int:
    files = sorted(OUT_DIR.glob("*.json"))
    if not files:
        print("no attestations to verify")
        return 1
    target = files[-1] if latest else files[-1]
    b = json.loads(target.read_text())
    print(f"attestation: {target.name} · scheme {b.get('signature_scheme')} · "
          f"unsigned_on_this_host {b.get('unsigned_on_this_host')}")
    bad = 0
    present = 0
    for k, art in b.items():
        if not k.startswith("artefact_") or not art.get("present"):
            continue
        present += 1
        p = RESULTS / art["path"]
        if p.exists() and _sha256(p) == art["sha256"]:
            print(f"  ✓ {art['path']} unchanged")
        else:
            print(f"  ✗ {art['path']} MISMATCHED (or missing)")
            bad += 1
    print(f"{present - bad}/{present} artefacts verified · {'OK' if bad == 0 else 'MISMATCH'}")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    if args.verify:
        return verify()
    out = emit()
    print(f"attestation written: {out}")
    print(json.dumps(json.loads(out.read_text()), indent=2)[:1200])
    return 0


if __name__ == "__main__":
    sys.exit(main())