#!/usr/bin/env python3
"""art50_demo.py — LIVE demo of the Article 50 receipt (the insurer-pilot trigger).
Shows CONFORMING -> NON-CONFORMING -> CONFORMING with real Ed25519 receipts.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# demo signing key (measurement-instrument kid for the demo; production = estate key)
key = Ed25519PrivateKey.generate()
os.environ["INSPECT_RECEIPTS_KEY"] = key.private_bytes_raw().hex()

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inspect-receipts"))
import inspect_receipts as ir

FROZEN_ART50 = "Art 50 AI Act: users shall be informed they are interacting with AI; synthetic content shall be marked in a machine-readable format."

def check(interaction: dict) -> str:
    """Deterministic predicate: CONFORMING iff disclosure present AND marking machine-readable."""
    has_disclosure = bool(interaction.get("disclosure", "").strip())
    has_marking = interaction.get("marking") in ("c2pa", "xmp", "machine-readable")
    if has_disclosure and has_marking:
        return "CONFORMING"
    if not has_disclosure and not has_marking:
        return "NON-CONFORMING"
    return "NON-CONFORMING"  # partial = non-conforming (fail-closed)

def receipt(verdict: str, note: str) -> dict:
    class T: name = "art50-demo"; id = f"a50-{int(time.time())}"
    class R: log_hashes = []
    payload = {"provision": "EU-AI-Act-2024-1689-Art50", "frozen_text": FROZEN_ART50,
               "verdict": verdict, "note": note, "predicate": "disclosure_present AND marking_machine_readable"}
    r = ir.build_receipt(T(), R(), kid="did:web:csoai.org#card-attestation-1",
                         extra_claims=[{"type": "provision-conformance", "detail": json.dumps(payload)}])
    return r

# T0: binding — conforming
r1 = receipt(check({"disclosure": "This is AI-generated.", "marking": "c2pa"}), "binding: condition precedent")
# T1: mid-policy — the marking disappears
r2 = receipt(check({"disclosure": "", "marking": None}), "trigger: CONFORMING -> NON-CONFORMING")
# T2: after fix — restored
r3 = receipt(check({"disclosure": "AI output.", "marking": "machine-readable"}), "post-fix: restored")

print("ART 50 DEMO — the insurer trigger, live:")
for label, r in (("T0 BINDING", r1), ("T1 TRIGGER", r2), ("T2 RESTORED", r3)):
    v = r["claims"][1]["detail"]  # extra claim is index 1 (0 = measurement)
    vv = json.loads(v)["verdict"]
    print(f"  {label:<12} verdict={vv:<14} content_id={r['content_id'][:16]}… sig={r['signature']['sig'][:12]}…")
print("  chain: R1 -> R2 -> R3 (the policy's conformance ledger)")
print("  verify: any party recomputes content_id + checks sig against did:web:csoai.org")
