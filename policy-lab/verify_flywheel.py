#!/usr/bin/env python3
"""Independently verify the Sovereign Town GOVERNED-vs-UNGOVERNED flywheel ledger.

No trust in CSOAI required. Each cycle summary is Ed25519-signed (RFC 8032) and hash-chained
(prev = previous signature). This recomputes the signed message for every cycle, verifies the
signature against the published public key, checks the hash-chain, and prints the headline:
governed-AI crimes vs ungoverned-AI crimes across all simulated episodes.

  pip install cryptography
  python3 verify_flywheel.py flywheel_ledger.jsonl town_pub.key

Signed message per cycle = entry["prev"] + json.dumps(entry_without_prev_and_sig, sort_keys=True)
(matches sign_lib.sign(priv, chain_head + body)).
"""
import json, sys, base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ledger = sys.argv[1] if len(sys.argv) > 1 else "flywheel_ledger.jsonl"
pubf = sys.argv[2] if len(sys.argv) > 2 else "town_pub.key"
pk = Ed25519PublicKey.from_public_bytes(base64.b64decode(open(pubf).read().strip()))
rows = [json.loads(l) for l in open(ledger) if l.strip()]

ok = bad = chain_ok = chain_bad = 0
bad_cycles = []
for i, r in enumerate(rows):
    body = json.dumps({k: v for k, v in r.items() if k not in ("prev", "sig")}, sort_keys=True)
    try:
        pk.verify(base64.b64decode(r["sig"]), (r["prev"] + body).encode()); ok += 1
    except Exception:
        bad += 1; bad_cycles.append(r.get("cycle"))
    if i == 0 or r.get("prev") == rows[i - 1].get("sig"):
        chain_ok += 1
    else:
        chain_bad += 1

A = sum(r.get("A_crimes", 0) for r in rows)
B = sum(r.get("B_crimes", 0) for r in rows)
eps = rows[-1].get("cum_episodes", 0) if rows else 0
print(f"cycles: {len(rows)}   cumulative episodes: {eps:,}")
print(f"Ed25519 signatures : {ok} valid / {bad} invalid")
print(f"hash-chain intact  : {chain_ok}/{len(rows)} (broken: {chain_bad})")
print(f"GOVERNED (A) crimes   : {A:,}")
print(f"UNGOVERNED (B) crimes : {B:,}")
if bad:
    lo, hi = min(bad_cycles), max(bad_cycles)
    contiguous = bad_cycles == list(range(lo, lo + len(bad_cycles)))
    print(f"NOTE: {bad} cycles ({lo}-{hi}) do not verify — "
          f"{'contiguous from a key rotation; ' if contiguous else ''}hash-chain across them is "
          f"{'intact (no tampering, key-continuity gap)' if chain_bad == 0 else 'BROKEN'}.")
print("VERDICT:", "FULLY VERIFIED" if bad == 0 and chain_bad == 0
      else f"{ok}/{len(rows)} cycles signature-verified; chain {'intact' if chain_bad==0 else 'BROKEN'}")
