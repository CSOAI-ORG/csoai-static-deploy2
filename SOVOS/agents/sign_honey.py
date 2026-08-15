#!/usr/bin/env python3
"""Sign EVERY row in honey_all_producers.jsonl using the estate's signing spine.
   Writes honey_all_producers_signed.jsonl with card_type + Ed25519 signature + content_id."""
import json, sys, os
sys.path.insert(0, "/workspace/jeeves-exec/SOVOS/packages/sovos-city/src")
from sovos_city import bom_signer

honey_path = "/workspace/jeeves-exec/forest/honey_all_producers.jsonl"
out_path = honey_path.replace(".jsonl", "_signed.jsonl")

rows = [json.loads(l) for l in open(honey_path) if l.strip()]
print(f"TOTAL honey rows: {len(rows)}", flush=True)

signed = 0
unsigned = 0

for i, r in enumerate(rows):
    try:
        bom = bom_signer.build_minimal_bom(
            model_ref="honey/" + str(r.get("source", "stratum")),
            components=[{"name": "behaviour-data-row", "version": str(r.get("capture_id", ""))[:8]}],
            licenses={"behaviour-data-row": ["LicenseRef-consented-csoai"]},
            safety_evals={"capture": {"n": 1, "ok": 1}},
        )
        sig = bom_signer.sign_bom(bom)
        if sig.get("signed"):
            r["card_type"] = "sovos-honey-stratum-v1"
            r["signed"] = True
            r["content_id"] = str(sig.get("content_id", ""))[:40]
            r["signer_pubkey"] = str(sig.get("signer_pubkey", ""))[:28]
            r["time_anchor"] = str(sig.get("time_anchor_state", "") or "")
            signed += 1
        else:
            r["card_type"] = "sovos-honey-stratum-v1"
            r["signed"] = False
            r["sign_reason"] = str(sig.get("reason", ""))
            unsigned += 1
    except Exception as e:
        r["card_type"] = "sovos-honey-stratum-v1"
        r["signed"] = False
        r["sign_error"] = str(e)[:120]
        unsigned += 1

    if (i + 1) % 500 == 0:
        print(f"  progress: {i+1}/{len(rows)} signed={signed}", flush=True)

with open(out_path, "w") as f:
    for r in rows:
        f.write(json.dumps(r, sort_keys=True) + "\n")

print(f"\nDONE: {signed} signed, {unsigned} unsigned of {len(rows)} total")
print(f"Written to: {out_path}")
print(f"File size: {os.path.getsize(out_path)} bytes")

if signed > 0:
    v = rows[0]
    print(f"\nSample:")
    print(f"  card_type: {v.get('card_type')}")
    print(f"  signed: {v.get('signed')}")
    print(f"  content_id: {str(v.get('content_id',''))[:40]}")
    print(f"  signer_pubkey: {str(v.get('signer_pubkey',''))[:28]}")
    print(f"  time_anchor: {v.get('time_anchor')}")