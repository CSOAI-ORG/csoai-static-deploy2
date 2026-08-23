#!/usr/bin/env python3
"""council_ledger.py — Council Ledger (public name; internal codename: Dorado).

REFRAMED per market validation (2026-08-19): the defensible product is a SIGNED
PROVISION-CONFORMANCE RECEIPT for a defined task class, with market and human context
reported ALONGSIDE — never fused into one "gap number" (regulation states what is
permitted; market data states what is priced; they are not commensurable).

Three measured surfaces, each with its own register:
  1. PROVISION-CONFORMANCE (MEASURED, deterministic) — did the actor's output conform
     to the currently-in-force frozen provision? (the core, deterministic predicates)
  2. MARKET CONTEXT (MEASURED, reported) — live index state for the task's market
     (East/West pair-gap reported as context, with its own register)
  3. HUMAN/AI CONTEXT (REPORTED, scored) — human baseline + AI agent result on the
     same task, scored against the measured conformance ground truth, never blended

Firewall (the brand): nobody ranked pays; humans never pay. Independent, neutral,
signed evidence — measurement, not certification.
"""
from __future__ import annotations
import json, os, sys, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dorado_bench import snap_all, fetch_quote, pair_gap, EAST_INDICES, WEST_INDICES

# ---- Provision bank: frozen, versioned (canon: 417 provisions; here the measured set) ----
PROVISIONS = [
    {"id": "EU-AI-Act-2024-1689-Art6", "jurisdiction": "EU", "instrument": "AI Act",
     "provision": "Art 6 risk-tier classification (prohibited/high/limited/minimal)",
     "frozen_at": "2024-08-01", "task": "gov-risk-tier", "benchmark": "govbench",
     "predicate": "exact_match(label)", "bank_n": 237,
     "applicability": "high-risk obligations apply 2027-12-02 (Digital Omnibus deferral — verified 2026-08-20)"},
    {"id": "EU-AI-Act-2024-1689-Art50", "jurisdiction": "EU", "instrument": "AI Act",
     "provision": "Art 50 transparency/marking obligations",
     "frozen_at": "2025-08-02", "task": "prov-marking", "benchmark": "provbench",
     "predicate": "manifest_valid", "bank_n": 32},
    {"id": "CN-TC260-AI-Safety-2023", "jurisdiction": "CN", "instrument": "TC260 framework",
     "provision": "AI safety governance framework — risk containment",
     "frozen_at": "2023-08-15", "task": "jail-containment", "benchmark": "jail-bank",
     "predicate": "containment_floor", "bank_n": 37},
    {"id": "KR-AI-Basic-Act-2026", "jurisdiction": "KR", "instrument": "Korea AI Basic Act",
     "provision": "Basic Act on AI Development and Trust (in force 2026-01-22)",
     "frozen_at": "2024-12-26", "applicability": "in force 2026-01-22 (estate MCP korea-ai-basic-act)",
     "task": "basic-act-conformance", "benchmark": "korea-basic-act",
     "predicate": "exact_match(label)", "bank_n": None, "bank_status": "STUB — ontology only, bank TBD"},
    {"id": "JP-AI-Guidelines-2024", "jurisdiction": "JP", "instrument": "Japan AI Guidelines for Business",
     "provision": "METI guidelines — AI business conformance",
     "frozen_at": "2024-04-19", "task": "japan-guideline-conformance", "benchmark": "japan-guidelines",
     "predicate": "exact_match(label)", "bank_n": None, "bank_status": "STUB — ontology only, bank TBD"},
]


def provision_conformance(provision_id: str, actor_outputs: dict) -> dict:
    """Deterministic provision-conformance scoring (the core).
    actor_outputs: {actor: [verdicts]} scored against the provision's gold labels.
    Conformance = exact_match / n. MEASURED register."""
    prov = next((p for p in PROVISIONS if p["id"] == provision_id), None)
    if not prov:
        return {"ok": False, "error": f"provision {provision_id} not in bank"}
    results = {}
    for actor, verdicts in actor_outputs.items():
        n = len(verdicts)
        correct = sum(1 for v in verdicts if v.get("correct"))
        acc = correct / n if n else None
        # Wilson 95% CI (3-dec, matching estate stat_suite)
        lo = hi = None
        if n and 0 < acc < 1:
            z = 1.96
            p = acc
            denom = 1 + z*z/n
            centre = (p + z*z/(2*n)) / denom
            half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
            lo, hi = max(0.0, centre-half), min(1.0, centre+half)
        results[actor] = {"n": n, "correct": correct, "conformance": round(acc, 4) if acc is not None else None,
                          "ci95": [round(lo,3), round(hi,3)] if lo is not None else None,
                          "register": "MEASURED (deterministic predicate)"}
    return {"provision": prov, "results": results,
            "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def market_context() -> dict:
    """Live market state for the ledger — REPORTED ALONGSIDE, never fused into conformance."""
    snap = snap_all()
    return {"market_snapshot": {k: v for k, v in snap.items() if k != "reg_events"},
            "register": "MEASURED (live quotes) — context, not conformance"}


def human_ai_context(provision_id: str, human: dict, ai: dict) -> dict:
    """Human + AI results on the same task, scored against the provision gold.
    REPORTED register — never blended into the conformance core."""
    prov = next((p for p in PROVISIONS if p["id"] == provision_id), None)
    if not prov: return {"ok": False, "error": "unknown provision"}
    def score(verdicts):
        n = len(verdicts); c = sum(1 for v in verdicts if v.get("correct"))
        return {"n": n, "correct": c, "score": round(c/n, 4) if n else None, "register": "REPORTED"}
    return {"provision": prov["id"], "human": score(human), "ai": score(ai),
            "note": "REPORTED context — humans and AI never ranked against each other for money (firewall)",
            "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def signed_receipt(conformance: dict, market: dict = None, human_ai: dict = None,
                   key_hex: str = None) -> dict:
    """Emit the ledger as a SIGNED receipt (estate signing spine, ed25519).
    Fail-closed: no key -> no signature -> receipt marked unsigned, never fabricated.
    The receipt proves what was measured and when (chain-ready for the 3KB card spine)."""
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inspect-receipts"))
    from inspect_receipts import build_receipt
    key_hex = key_hex or os.environ.get("INSPECT_RECEIPTS_KEY", "")
    payload = {"schema": "csoai.ledger/0.1",
               "conformance": conformance, "market": market, "human_ai": human_ai,
               "register": "MEASURED core; market + human/AI reported alongside; never blended"}
    class _T: name = "council-ledger"; id = "cl-" + time.strftime("%Y%m%d%H%M%S", time.gmtime())
    class _R: log_hashes = []
    if not key_hex:
        return {"ok": False, "error": "no signing key — receipt UNSIGNED (fail-closed)", "payload": payload}
    r = build_receipt(_T(), _R(), kid="did:web:csoai.org#measurement-instrument",
                      extra_claims=[{"type": "provision-conformance", "detail": json.dumps(conformance)[:400]}],
                      key_hex=key_hex)
    r["payload"] = payload
    return {"ok": True, "receipt": r, "signed": True,
            "content_id": r["content_id"], "sig": r["signature"]["sig"][:16]}



def axis_register() -> dict:
    """The honest 16-axis register with set-boundary labels (counting rule, product-facing)."""
    return {
        "schema": "csoai.axis-register/0.1",
        "as_of": "2026-08-22",
        "counting_rule": "every count names its set: PUBLIC_BOARD 14 / INTERNAL_16 / CANON_REGISTRY",
        "sets": {
            "public_board": {"count": 14, "axes": ["governance","safety","provenance","continuity",
                "conformance","openness","machinery-conformity","care","cross-reality",
                "detector-interop","art5-safeguard","swarm","affect","jail"],
                "grammar": "13 measured of 14 quotable (jail separation pending OR v2 SEPARATED evidence ready)"},
            "internal_16": {"count": 16, "axes_extra": ["slot15","human-vs-ai"],
                "register": "measured in-lane only, never public"},
        },
        "jail": {"n": 71, "acc": 0.5915, "v2_sep": "SEPARATED (32-item, p=0.00087, signed)",
                 "register": "MEASURED"},
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

if __name__ == "__main__":
    print(json.dumps({"provision_conformance": provision_conformance("EU-AI-Act-2024-1689-Art6", {
        "sov6-ethics-v3-light": [{"correct": True}] * 88 + [{"correct": False}] * 149}),
        "market": market_context(), "registers": "MEASURED core; market + human/AI reported alongside; never fused"},
        indent=1)[:900])
