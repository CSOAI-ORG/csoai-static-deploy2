#!/usr/bin/env python3
"""
hive_pack.py — give every hive the ability to "eat its own industry" (self-contained governance pack).

For a hive, this packages the full stack scoped to ITS vertical:
  • its regulation/framework set (what its industry must comply with)
  • a per-hive Looking Glass — simulate the industry under regulatory regimes (EU/US/UK/none) -> outcomes
  • its per-hive sovereign model (accuracy from moat_models.json, trained by train_all_hives.py)
  • an Ed25519-signed industry attestation (proofof.ai-verifiable)
  • a MEOK Labs industry digest published to the research index

Bright line (carried from spec §16): a hive eats its industry's REGULATIONS + DYNAMICS + PUBLIC ARCHETYPES.
It does NOT profile named real firms, assert any named firm is non-compliant, or surveil. All outputs are
labelled simulation/decision-support. python3 hive_pack.py [hive_key ...]   (default: all hives)
"""
import json, os, sys, time
import sim, sign_lib

OUT = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.expanduser("~/clawd/meok-labs-engine/research/sovereign-town/industry-packs")
os.makedirs(LABS, exist_ok=True)

# per-hive regulation set — what each industry actually faces (illustrative, public frameworks only)
FRAMEWORKS = {
    "aqua":      ["EU AI Act", "RSPCA Assured", "CEFAS/FHI fish-health", "GDPR"],
    "legal":     ["EU AI Act", "HM Land Registry", "SRA conduct", "GDPR"],
    "logistics": ["EU AI Act", "DVSA earned recognition", "EU mobility/tachograph", "DORA (if FS cargo)"],
    "optical":   ["EU AI Act", "GOC standards", "MHRA medical-device", "GDPR"],
}
DEFAULT_FW = ["EU AI Act", "GDPR", "NIST RMF"]
REGIMES = [("EU (strict)", 1.0), ("US (NIST)", 0.7), ("UK (light)", 0.4), ("none", 0.0)]
SEEDS = [47, 48, 49]

def looking_glass(hive):
    idx = list(sim.DISTRICTS.keys()).index(hive)
    sim.CONTAGION_STEP = 0.05; sim.SCARCITY_DAYS = set(range(7, 14))
    out = {}
    for label, rate in REGIMES:
        runs = [sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False,
                            district=hive, seed=s + idx * 1000, block_rate=rate) for s in SEEDS]
        n = len(runs)
        out[label] = {"crimes": sum(r["violations"] for r in runs),
                      "resilience": round(sum(r["final_commons"] for r in runs) / n, 3),
                      "productivity": round(sum(r["work_accuracy"] for r in runs) / n, 3)}
    return out

def pack(hive, priv, models):
    meta = sim.DISTRICTS[hive]
    glass = looking_glass(hive)
    bundle = {"hive": meta["hive"], "district": hive, "generated": time.strftime("%Y-%m-%d"),
              "frameworks": FRAMEWORKS.get(hive, DEFAULT_FW),
              "looking_glass": glass,
              "sovereign_model": {"acc": models.get(hive, {}).get("test_acc"),
                                  "f1": models.get(hive, {}).get("f1")},
              "note": "SIMULATION / decision-support — public archetypes only, not claims about named firms"}
    body = json.dumps(bundle, sort_keys=True)
    bundle["sig"] = sign_lib.sign(priv, body); bundle["alg"] = "ed25519"
    json.dump(bundle, open(os.path.join(LABS, f"{hive}.json"), "w"), indent=2)
    # human-readable industry digest for MEOK Labs
    eu, none = glass["EU (strict)"], glass["none"]
    md = f"""# {meta['hive']} — industry governance pack (hive eats its own industry)

*MEOK Labs · auto-generated {bundle['generated']} · SIMULATION (public archetypes, not named firms)*

**Industry frameworks:** {', '.join(bundle['frameworks'])}
**Looking Glass (this industry under regulatory regimes):**

| regime | crimes | resilience | productivity |
|---|---|---|---|
""" + "\n".join(f"| {k} | {v['crimes']} | {v['resilience']} | {v['productivity']} |" for k, v in glass.items()) + f"""

**Headline:** under a strict regime this industry runs at **{eu['crimes']} crimes / {eu['resilience']} resilience**;
ungoverned it runs at **{none['crimes']} crimes / {none['resilience']} resilience**.
**Sovereign model:** acc {bundle['sovereign_model']['acc']} / F1 {bundle['sovereign_model']['f1']}.
**Attestation:** Ed25519-signed ({bundle['sig'][:24]}…), proofof.ai-verifiable.
"""
    open(os.path.join(LABS, f"{hive}.md"), "w").write(md)
    return bundle

def main():
    priv, pub = sign_lib.load_or_create_key()
    models = {}
    try: models = json.load(open(os.path.join(OUT, "moat_models.json")))["models"]
    except Exception: pass
    hives = sys.argv[1:] or list(sim.DISTRICTS.keys())
    print(f"\n  HIVE PACKS — each hive eats its own industry ({len(hives)} hives)")
    print("  " + "-" * 70)
    print(f"  {'hive':<18}{'frameworks':<10}{'EU crimes':>10}{'none crimes':>12}{'model acc':>11}")
    print("  " + "-" * 70)
    done = 0
    for h in hives:
        if h not in sim.DISTRICTS: continue
        b = pack(h, priv, models); done += 1
        g = b["looking_glass"]
        print(f"  {b['hive']:<18}{len(b['frameworks']):<10}{g['EU (strict)']['crimes']:>10}"
              f"{g['none']['crimes']:>12}{str(b['sovereign_model']['acc']):>11}")
    print("  " + "-" * 70)
    print(f"  {done} hive industry packs (Ed25519-signed) -> {LABS}\n")

if __name__ == "__main__":
    main()
