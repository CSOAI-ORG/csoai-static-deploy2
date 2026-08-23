#!/usr/bin/env python3
"""test_ledger.py — Council Ledger / Dorado CI (repeatable improvement pass)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dorado_bench as db
import council_ledger as cl

PASS = 0
def check(name, cond, detail=""):
    global PASS
    assert cond, f"FAIL: {name} {detail}"
    PASS += 1
    print(f"  ✓ {name}")

# 1. live quotes + fail-closed
s = db.snap_all()
check("snap_all 6+ quotes", len(s["quotes"]) >= 6)
check("snap_all 9+ pair-gaps", len(s["pair_gaps"]) >= 9)
check("fail-closed bad symbol", db.fetch_quote("BAD.SYM") is None)

# 2. conformance core
c = cl.provision_conformance("EU-AI-Act-2024-1689-Art6",
                             {"m": [{"correct": True}]*70 + [{"correct": False}]*30})
r = c["results"]["m"]
check("conformance 0.7", r["conformance"] == 0.7)
check("conformance CI sane", r["ci95"][0] < 0.7 < r["ci95"][1])
check("unknown provision fail-closed", cl.provision_conformance("nope", {})["ok"] is False)

# 3. market context
m = cl.market_context()
check("market 6+ quotes", len(m["market_snapshot"]["quotes"]) >= 6)
check("market register MEASURED", "MEASURED" in m["register"])

# 4. human/ai REPORTED
h = cl.human_ai_context("EU-AI-Act-2024-1689-Art6",
                        human=[{"correct": True}]*5, ai=[{"correct": True}]*4+[{"correct": False}])
check("human score 1.0", h["human"]["score"] == 1.0)
check("ai score 0.8", h["ai"]["score"] == 0.8)
check("human/ai REPORTED", h["human"]["register"] == "REPORTED")

# 5. signed receipt (with key)
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
key = Ed25519PrivateKey.generate()
os.environ["INSPECT_RECEIPTS_KEY"] = key.private_bytes_raw().hex()
sr = cl.signed_receipt(c)
check("signed receipt ok", sr["ok"] and sr["signed"])
check("signed receipt content_id", len(sr["content_id"]) == 64)
os.environ.pop("INSPECT_RECEIPTS_KEY", None)
check("no-key fail-closed", cl.signed_receipt(c)["ok"] is False)

# 6. human capture pipeline
import human_capture as hc
import tempfile, os as _os
_tmp = _os.path.join(tempfile.mkdtemp(), "hv.jsonl")
r = hc.record_human_verdict("human-test", "pair-gap", "PARITY", store=_tmp)
check("human capture recorded", r["record_sha256"] is not None and r["kind"] == "human")
check("human capture provenance", "REPORTED" in r["provenance"])
check("human capture persisted", len(hc.list_human_verdicts(store=_tmp)) == 1)

print(f"\nLEDGER CI: {PASS}/17 PASS ✅")
