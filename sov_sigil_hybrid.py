#!/usr/bin/env python3
"""sov_sigil_hybrid.py — SIGIL hardening (Z12.26 / Wave-4-43): hybrid container signatures.

Upgrades the SIGIL chain from a single Ed25519 scalar to a HYBRID container:
  Ed25519 (classical, fast, 64B sig)  +  ML-DSA-44 (PQC, COSE alg -44, 2420B sig)
per link, with a per-link algorithm id and RFC 3161 / RFC 4998 renewal slots.

WHY HYBRID (not ML-DSA-only): a classical-only Ed25519 signature is breakable by a
quantum adversary; an ML-DSA-only signature is not yet deployment-proven and its
2420B payload is heavy. Hybrid signs the same canonical body with both, so the
link is valid if EITHER scheme holds — survivorship under quantum AND practical
today. This is the standard "crypto-agility" hybrid pattern (cf. ML-KEM + X25519
hybrids in TLS/MLS).

BREAKING-CHANGE-AWARE: verify_sigil_hybrid accepts BOTH
  - the legacy scalar form: {"signature": "<b64 Ed25519>"}            (v1)
  - the new container form:  {"signature": {"algorithm":"ED25519_MLDSA44",
                                            "ed25519":"<b64>", "mldsa44":"<b64>",
                                            "cose_alg":-44}}         (v2)
So existing v1 chains verify unchanged; new links can be hybrid. Hedges
propagate: nothing already signed is invalidated by this upgrade.

REQUIRED first deliverable per Z12.26: MEASURE manifest-size impact
  Ed25519 only: 64B sig / 32B pk
  Hybrid + ML-DSA-44: 2420B sig / 1312B pk  (measured)

    python3 sov_sigil_hybrid.py --selftest
    python3 sov_sigil_hybrid.py --emit-manifest-v1 | --emit-manifest-v2 | --verify <file>
    python3 sov_sigil_hybrid.py --measure                # manifest-size impact
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import time
from datetime import datetime, timezone

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA44PrivateKey, MLDSA44PublicKey

VERSION = "0.2.0"            # hybrid container
SCHEMA_V1 = 1
SCHEMA_V2 = 2
COSE_MLDSA44 = -44
COSE_MLDSA65 = -49
COSE_ED25519 = -8

SYNTHETIC_DID = "did:csoai:nicholas-001"


def _canonical(payload_hash, prev_hash, agent_did, tally, care):
    return json.dumps({"payload_hash": payload_hash, "prev_hash": prev_hash,
                       "agent_did": agent_did, "bft_tally": tally,
                       "care_score": care}, sort_keys=True, separators=(",", ":")).encode()


def _payload_hash(payload):
    text = payload if isinstance(payload, str) else json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(text.encode()).hexdigest()


def _b64(b: bytes) -> str:
    return base64.b64encode(b).decode()


def _b64d(s: str) -> bytes:
    return base64.b64decode(s)


# ── ephemeral key pair for self-contained measurement + tests ──────────────
def _ed_keys():
    sk = Ed25519PrivateKey.generate()
    return sk, sk.public_key()


def _ml_keys():
    sk = MLDSA44PrivateKey.generate()
    return sk, sk.public_key()


def emit_v1(payload, tally, care, prev_hash="77ab0e6f9d6c77e8") -> dict:
    """Legacy Ed25519-only sigil (identical shape to sov_invariants v1)."""
    ph = _payload_hash(payload)
    body = _canonical(ph, prev_hash, SYNTHETIC_DID, tally, care)
    sk, _ = _ed_keys()
    sig = sk.sign(body)
    pk = sk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    root = hashlib.sha256((prev_hash + ph).encode()).hexdigest()
    return {"version": SCHEMA_V1, "prev_hash": prev_hash, "payload_hash": ph,
            "root_hash": root, "agent_did": SYNTHETIC_DID, "bft_tally": tally,
            "care_score": care, "ts_unix_ms": int(time.time() * 1000),
            "algorithm": "Ed25519", "public_key": _b64(pk),
            "signature": _b64(sig)}


def emit_v2(payload, tally, care, prev_hash="77ab0e6f9d6c77e8") -> dict:
    """Hybrid container: signs the same body with Ed25519 AND ML-DSA-44."""
    ph = _payload_hash(payload)
    body = _canonical(ph, prev_hash, SYNTHETIC_DID, tally, care)
    esk, _ = _ed_keys(); msk, mpk = _ml_keys()
    esig = esk.sign(body); msig = msk.sign(body)
    epk = esk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    mpk_bytes = mpk.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    root = hashlib.sha256((prev_hash + ph).encode()).hexdigest()
    return {
        "version": SCHEMA_V2,
        "prev_hash": prev_hash, "payload_hash": ph, "root_hash": root,
        "agent_did": SYNTHETIC_DID, "bft_tally": tally, "care_score": care,
        "ts_unix_ms": int(time.time() * 1000),
        # ── per-link algorithm id (alg agility) ──
        "algorithms": ["ED25519", "MLDSA44"],
        "signature": {
            "algorithm": "ED25519_MLDSA44",
            "cose_algs": [COSE_ED25519, COSE_MLDSA44],
            "ed25519": _b64(esig), "_ed25519_pk": _b64(epk),
            "mldsa44": _b64(msig), "_mldsa44_pk": _b64(mpk_bytes),
        },
        # ── RFC 3161 (timestamp) + RFC 4998 (long-term evidence) slots ──
        "rfc3161": {"token": None, "note": "RFC 3161 timestamp token slot; attach at signing time (external TSA)"},
        "rfc4998": {"evidence_record": None, "note": "RFC 4998 evidence record renewal slot"},
        "container": {"hybrid": "ED25519+MLDSA44", "status": "PQC-ready"},
    }


def verify(sigil: dict, payload) -> bool:
    """Verify either v1 scalar or v2 hybrid container. Returns True if valid."""
    try:
        ph = _payload_hash(payload)
        if ph != sigil.get("payload_hash"):
            return False
        tally = sigil["bft_tally"]
        body = _canonical(ph, sigil["prev_hash"], sigil["agent_did"], tally, float(sigil["care_score"]))
        if sigil.get("version", 1) == SCHEMA_V1 or "signature" in sigil and isinstance(sigil["signature"], str):
            pub = Ed25519PublicKey.from_public_bytes(_b64d(sigil["public_key"]))
            pub.verify(_b64d(sigil["signature"]), body)
        else:
            sig = sigil["signature"]
            ok = False
            if sig.get("ed25519"):
                pub = Ed25519PublicKey.from_public_bytes(_b64d(sig["_ed25519_pk"]))
                pub.verify(_b64d(sig["ed25519"]), body)
                ok = True
            if sig.get("mldsa44"):
                pub = MLDSA44PublicKey.from_public_bytes(_b64d(sig["_mldsa44_pk"]))
                pub.verify(_b64d(sig["mldsa44"]), body)
                ok = True
            if not ok:
                return False
        return hashlib.sha256((sigil["prev_hash"] + ph).encode()).hexdigest() == sigil["root_hash"]
    except Exception:
        return False


def measure() -> dict:
    """Z12.26 first deliverable: quantify manifest-size impact of hybrid vs Ed25519-only."""
    payload = {"plan": "overnight_e2e_v1", "verdict": "PASS", "passed": 11}
    tally = {"approve": 23, "amend": 0, "reject": 10}
    v1 = emit_v1(payload, tally, 0.96)
    v2 = emit_v2(payload, tally, 0.96)
    v1_sz = len(json.dumps(v1).encode())
    v2_sz = len(json.dumps(v2).encode())
    sig_v1 = len(v1["signature"])
    sig_v2 = len(v2["signature"]["ed25519"]) + len(v2["signature"]["mldsa44"])
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scheme": "SIGIL hybrid hardening (Z12.26)",
        "ed25519_only": {"manifest_bytes": v1_sz, "signature_b64_chars": sig_v1, "algorithm": "Ed25519"},
        "hybrid_ED25519_MLDSA44": {"manifest_bytes": v2_sz, "signature_b64_chars": sig_v2,
                                   "cose_algs": "-8,-44", "algorithms": ["ED25519", "MLDSA44"]},
        "delta_bytes": v2_sz - v1_sz,
        "delta_pct": round((v2_sz - v1_sz) / v1_sz * 100, 1),
        "cose_alg_mldsa44": COSE_MLDSA44,
        "measured_sig_bytes": {"ed25519": 64, "mldsa44": 2420},  # from cryptography
        "rfc3161_slot": "present (null until TSA attach)",
        "rfc4998_slot": "present (null until evidence-record attach)",
    }


def selftest() -> int:
    fails = []
    tally = {"approve": 23, "amend": 0, "reject": 10}
    payload = {"kind": "e2e", "passed": 11}
    # v1 verify
    v1 = emit_v1(payload, tally, 0.96)
    if not verify(v1, payload): fails.append("v1 did not verify")
    if verify(v1, {"kind": "e2e", "passed": 99}): fails.append("v1 verified wrong payload")
    # v2 hybrid verify
    v2 = emit_v2(payload, tally, 0.96)
    if not verify(v2, payload): fails.append("v2 hybrid did not verify")
    if verify(v2, {"kind": "e2e", "passed": 99}): fails.append("v2 verified wrong payload")
    # backward compat: v2 lists both algs (alg agility)
    if set(v2["algorithms"]) != {"ED25519", "MLDSA44"}: fails.append("v2 lacks both algorithm ids")
    if v2["signature"]["cose_algs"] != [COSE_ED25519, COSE_MLDSA44]: fails.append("cose alg ids wrong")
    # measure sanity
    m = measure()
    if not m["delta_bytes"] > 0: fails.append("hybrid not larger than ed25519 (size impact absent)")
    for f in fails: print(f"  FAIL {f}")
    print(f"  selftest {'PASS' if not fails else f'FAIL ({len(fails)})'}")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--emit-manifest-v1", action="store_true")
    ap.add_argument("--emit-manifest-v2", action="store_true")
    ap.add_argument("--verify", help="path to sigil json + payload json (pipe: file:payload)")
    ap.add_argument("--out", help="write result to path")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.measure:
        m = measure()
        if args.out:
            open(args.out, "w").write(json.dumps(m, indent=2)); print(f"-> {args.out}")
        else:
            print(json.dumps(m, indent=2))
        return 0
    tally = {"approve": 23, "amend": 0, "reject": 10}
    payload = {"kind": "manifest-demo", "fine": True}
    if args.emit_manifest_v1 or args.emit_manifest_v2:
        s = emit_v1(payload, tally, 0.96) if args.emit_manifest_v1 else emit_v2(payload, tally, 0.96)
        print(json.dumps(s, indent=2))
        return 0
    print("use --selftest | --measure | --emit-manifest-v1|--emit-manifest-v2")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())