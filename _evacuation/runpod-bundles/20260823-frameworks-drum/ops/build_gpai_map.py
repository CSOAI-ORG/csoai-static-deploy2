#!/usr/bin/env python3
"""EU AI Act GPAI → evidence map (next-week plan move #2).

Connects the fused measured-compliance surface to the EU AI Act GPAI obligations (in force since
2 Aug 2026) as the compliance-evidence artifact. For each GPAI obligation, state the estate's
evidence and its honest status (measurement, not certification). Machine-readable feed.

Run: python3 ops/build_gpai_map.py
"""
import json
import os
import time

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PACK, "feeds", "gpai_compliance_map.json")


def main():
    # the estate's measured evidence (fused surface + adversarial instrument)
    comp = os.path.join(PACK, "feeds", "measured_compliance.json")
    gauge = {}
    try:
        gauge = json.load(open(comp, encoding="utf-8")).get("measured_gauge", {})
    except Exception:
        pass
    contam = {}
    try:
        contam = json.load(open(os.path.join(PACK, "feeds", "benchmark_contamination.json"), encoding="utf-8"))
    except Exception:
        pass
    records = gauge.get("live_records", 0)
    signed = gauge.get("signed_cards", 0)
    axes = len(gauge.get("axes", []))
    cbench = len(contam.get("benchmarks", []))
    cres = sum(1 for b in contam.get("benchmarks", []) if b.get("designed_resistant"))

    obligations = [
        {"article": "Art 50 — transparency", "obligation": "disclose AI-generated content + that output is AI",
         "evidence": "signed measured cards / model disclosures", "status": "PARTIAL — the #dsh signing rail gates the signed cards"},
        {"article": "Art 53 — training-data summary", "obligation": "publish a sufficiently detailed summary of training data (copyright)",
         "evidence": f"contamination register: {cbench} benchmarks ({cres} designed-resistant)",
         "status": "READY — feeds/benchmark_contamination.json (anti-Goodhart leakage evidence)"},
        {"article": "Art 53 — copyright respect", "obligation": "respect copyright in training (policy + transparency)",
         "evidence": "contamination register + provenance per benchmark", "status": "PARTIAL — register built; per-model provenance is [LANE]"},
        {"article": "Art 55 — systemic-risk (GPAI w/ systemic risk)", "obligation": "adversarial testing, incident reporting, risk/mitigation cycle",
         "evidence": f"measured gauge: {records} live records, {signed} signed cards, {axes} axes + jailbreak/fleet instrument",
         "status": "PARTIAL — measured + adversarial instrument exist; signing + incident channel [GATE #dsh]"},
        {"article": "Art 55 — model evaluation for systemic risk", "obligation": "adequate model evaluation, adversarial testing",
         "evidence": "measured gauge axis scores + arena Elo (own pillars)", "status": "MEASURED (not certified) — signed attestation pending"},
    ]
    out = {
        "generated": time.strftime("%Y-%m-%d"),
        "regulation": "EU AI Act (Regulation (EU) 2024/1689) — General Purpose AI (GPAI) obligations",
        "enforcement_started": "2026-08-02",
        "product": "measured compliance evidence pack — gauge + contamination register + arena Elo (fusEd)",
        "obligations": obligations,
        "honest_register": "measurement, not certification; UNMEASURED stays UNMEASURED; "
                           "the signed Ed25519 attestation lands with the #dsh rail",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(f"gpai_compliance_map.json written — {len(obligations)} obligations mapped to "
          f"measured evidence (gauge {records} records / contamination {cbench} benchmarks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
