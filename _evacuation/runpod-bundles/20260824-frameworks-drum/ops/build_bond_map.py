#!/usr/bin/env python3
"""BOND MARKET MAP — the finance instance of the measured-compliance layer (NEXT-100 Phase A).

Connects the 5 bond layers (sovereign/corp/high-yield/muni/ABS) to the applicable regulations the
drum indexes, and to the Phase-0 signed router (eunomia-bond-router: COBOL→JSON→Ed25519→A2A).
Phase 2 (tokenization / atomic-DvP) stays compliance-gated. Doctrine: measurement, not certification.

Run: python3 ops/build_bond_map.py
"""
import json
import os
import time

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PACK, "feeds", "bond_market_map.json")

# bond layer -> the estate instruments (regulations/frameworks) that govern it
LAYERS = {
    "sovereign": ["Basel III/IV", "N/A (self-cleared)"],
    "corporate": ["Basel III/IV", "MiFID II", "EMIR", "Dodd-Frank"],
    "high-yield": ["Basel III/IV", "MiFID II", "Dodd-Frank", "SEC/financial"],
    "municipal": ["SEC MSRB", "Dodd-Frank", "regulatory"],
    "structured-ABS": ["Basel III/IV", "EMIR", "Dodd-Frank", "SEC Reg AB"],
}


def main():
    cat = json.load(open(os.path.join(PACK, "catalog.json"), encoding="utf-8"))
    # the drum's financial instruments (names)
    fin = {i["name"] for i in cat["items"] if any(k.lower() in i["name"].lower()
           for k in ("basel", "mifid", "emir", "dodd", "sox", "finra", "dora", "solvency"))}
    layers = []
    for layer, regs in LAYERS.items():
        matched = [r for r in regs if any(r.lower().split()[0] in f.lower() for f in fin)]
        layers.append({"layer": layer, "regulations": regs,
                       "indexed_in_drum": bool(matched), "matched": matched,
                       "measured": {"gauge": "gauge covers the axis (provenance/liquidity/opacity)",
                                    "status": "REFERENCE-INDEXED (measured where a signed attestation exists)"},
                       "gap": "live E-W pairing is [LANE] (DORADO); signed bond attestation is [GATE #dsh]"})
    out = {
        "generated": time.strftime("%Y-%m-%d"),
        "domain": "bond markets (~$130T, 5 stacked layers)",
        "layers": layers,
        "router": {"name": "eunomia-bond-router (Bridge 1)", "phase": "Phase 0 (measured+signed, no token)",
                   "pipeline": "COBOL COPYBOOK → JSON → Ed25519-signed → A2A agent card",
                   "signing": "did:web:csoai.org#estate-chain-1"},
        "east_west": {
            "east": ["China (PFAS/bond market rules)", "Japan (JGB)", "Korea", "Singapore", "Hong Kong"],
            "west": ["US (SEC/CFTC)", "EU (MiFID II/EMIR)", "UK (FCA/PRA)"],
            "thesis": "the cross-border compliance 'corpus callosum' — a Chinese insurer can underwrite a UK SME bond only when both trust the CSOAI attestation; measured, not market. East↔West data is the DORADO [LANE] (over-the-wire, never fused).",
            "measured": "UNMEASURED until live East/West bond pairing (DORADO lane), honest"},
        "gpai_lens": {
            "applies": "EU AI Act GPAI obligations apply where AI is used in bond pricing/credit risk (a high-risk deployment)",
            "mapped": ["Art 50 transparency (AI-generated pricing/compliance outputs)", "Art 53 training-data summary (credit models)", "Art 55 systemic-risk (systemically-important bank models)"],
            "evidence": "feeds/gpai_compliance_map.json (2/5 READY/MEASURED today)",
        },
        "measured_compliance": "gauge + contamination register + GPAI map (the compliance evidence the attestation consumes)",
        "phase2_gate": "tokenization / atomic-DvP / smart-contract settlement — compliance-gated, NOT built",
        "honest": "measurement, not certification; the market is a REFERENCE + MEASURED layer, never a trading signal",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(f"bond_market_map.json written — {len(layers)} layers, router Phase 0 signed, "
          f"phase2 gated; indexed layers: {sum(1 for l in layers if l['indexed_in_drum'])}/{len(layers)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
