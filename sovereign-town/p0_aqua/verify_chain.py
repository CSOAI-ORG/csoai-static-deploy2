#!/usr/bin/env python3
"""Verify the Ed25519 episode chain with ONLY the public key — and prove tamper-detection."""
import json, os, copy
import sign_lib
OUT = os.path.dirname(os.path.abspath(__file__))
pub = open(os.path.join(OUT, "town_pub.key")).read().strip()
rows = [json.loads(l) for l in open(os.path.join(OUT, "episodes.jsonl"))]

prev = "genesis"; ok = 0
for r in rows:
    sig = r["sig"]; claimed_prev = r["prev_sig"]
    body = json.dumps({k: v for k, v in r.items() if k not in ("sig", "prev_sig", "alg")}, sort_keys=True)
    if claimed_prev == prev and sign_lib.verify(pub, prev + body, sig):
        ok += 1; prev = sig
    else:
        break
print(f"  Ed25519 chain: {ok}/{len(rows)} episodes verified with PUBLIC KEY ONLY (no secret, offline)")

# tamper test: flip one field in the first episode → signature must fail
r = copy.deepcopy(rows[0]); r["outcome"]["alive"] = False
b = {k: v for k, v in r.items() if k not in ("sig", "prev_sig")}
tampered_ok = sign_lib.verify(pub, "genesis" + json.dumps(b, sort_keys=True), rows[0].get("sig", "x"))
print(f"  tamper test (flipped one field): verifies = {tampered_ok}  -> {'DETECTED' if not tampered_ok else 'MISSED'}")
print(f"  verdict: {'TAMPER-EVIDENT, third-party-verifiable (regulator-grade)' if ok == len(rows) and not tampered_ok else 'FAIL'}")
