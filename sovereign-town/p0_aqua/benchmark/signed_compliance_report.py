#!/usr/bin/env python3
"""
Sovereign gym → signed compliance report bridge.

Runs a governed-vs-ungoverned Sovereign Town / Dorado scenario and emits a
cryptographically signed, independently verifiable report of the governance
outcome — "the governed world proves its own compliance."

Uses the canonical Ed25519 signer (sorted-keys, compact JSON). Verified: this
script's signed_payload matches the CSOAI /verify page's JS canonical() rule
byte-for-byte for this report body, and an Ed25519 verify over those bytes passes
— so the report checks out in the browser /verify page. (Re-verify if the body
schema changes.) The demo: a live governed simulation whose result is signed evidence.
"""
from __future__ import annotations
import json, hashlib, base64, datetime, sys, pathlib
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

# reuse the runnable Dorado scenario in this benchmark dir
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import dorado_sovereign_scenario as d

def _canonical(body: dict) -> str:
    return json.dumps(body, sort_keys=True, separators=(",", ":"))

def sign(body: dict, priv=None, pub=None) -> dict:
    if priv is None:
        priv = Ed25519PrivateKey.generate()
        pub = priv.public_key().public_bytes_raw().hex()
    payload = _canonical(body)
    rid = hashlib.sha256(payload.encode()).hexdigest()[:16]
    sig = base64.b64encode(priv.sign(payload.encode())).decode()
    return {"report_id": rid, "alg": "ed25519", "pub": pub, "sig": sig,
            "body": body, "signed_payload": payload}

def verify(m: dict) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(m["pub"])).verify(
            base64.b64decode(m["sig"]), _canonical(m["body"]).encode())
        return True
    except Exception:
        return False

def run_signed_compliance_report(seed: int = 42) -> dict:
    A = d.run_arm("A_governed", seed=seed)
    B = d.run_arm("B_ungoverned", seed=seed)
    body = {
        "report_type": "sovereign_governance_compliance",
        "scenario": "dorado_data_sovereignty",
        "assessed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "governed": {"attempts": A["attempts"], "blocked": A["blocked"], "leaks": A["leaks"],
                     "block_rate": round(A["block_rate"], 4)},
        "ungoverned": {"attempts": B["attempts"], "blocked": B["blocked"], "leaks": B["leaks"],
                       "block_rate": round(B["block_rate"], 4)},
        "breaches_prevented_by_governance": B["leaks"] - A["leaks"],
        "eu_ai_act_mapping": ["Art.12 logging", "Art.14 human oversight", "Art.5 prohibited-practice detection"],
        "note": "block/leak rates from an illustrative-parameter simulation (demo), not measured production data.",
    }
    return sign(body)

if __name__ == "__main__":
    m = run_signed_compliance_report()
    print("SIGNED COMPLIANCE REPORT")
    print("  report_id:", m["report_id"])
    print("  governed block_rate:", m["body"]["governed"]["block_rate"],
          "| breaches prevented:", m["body"]["breaches_prevented_by_governance"])
    print("  sig[:24]:", m["sig"][:24])
    print("  VERIFY:", verify(m))
    t = json.loads(json.dumps(m)); t["body"]["breaches_prevented_by_governance"] = 0
    print("  VERIFY after tamper (must be False):", verify(t))
