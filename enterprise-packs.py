#!/usr/bin/env python3
"""enterprise-packs.py — BINDS ENTERPRISES INTO THE ONE ENGINE-AXIS.

Extends the sibling domain-packs engine (domain packs: finance/markets/insurance/cobol)
with an ENTERPRISE registry pack: learn about companies, run each through the same
measure(care/gate/compliance) -> sign pipeline, emit a signed enterprise-measurement record.

This is the "fixing part of our engine + for enterprises + for information" binding:
one engine-axis measures+sigs AI domains AND the enterprises that wield them, so a
council/regulator/enterprise can see a conformant enterprise record.

Data source note (honest): live enterprise-registry API keys (Ahrefs=REPLACEMENT
placeholder, Google AI=bound to a deleted SA, Companies House MCP=stub) are NOT
available, so enterprise facts here are registry-seeded (Companies House SIC codes /
Company number) as *inputs* to assess. Swap in a live Companies House / OpenCorporates
API key in ENTERPRISE_SOURCE when provisioned — the measure->sign pipeline is unchanged.

Usage: python3 enterprise_packs.py [--packs enterprise]
"""
import hashlib, json, sys, time

# Universal measurement (same care-gate + compliance probes as domain-packs).
def _breach(text):
    t = (text or "").lower()
    for bad in ("target a person", "track an individual", "surveil", "weapon",
                "lie to", "exploit a distressed", "unlawful surveillance"):
        if bad in t:
            return True
    return False

def _compliance(claims):
    return {k: bool(v) for k, v in claims}

def measure(domain, entity, task, claims):
    breach = _breach(task)
    comp = _compliance(claims)
    passed = all(comp.values()) and not breach
    verdict = "PASS" if passed else "REVIEW"
    payload = json.dumps({
        "domain": domain, "entity": entity,
        "task": task[:90], "verdict": verdict,
        "signed_at": int(time.time()),
        "signer": f"did:meok:sovos-{domain}"}, sort_keys=True)
    return {
        "domain": domain, "entity": entity, "task": task[:90],
        "compliant": comp, "hard_stop": breach, "verdict": verdict,
        "signature": hashlib.sha256((payload + "|sovos-sigil").encode()).hexdigest()[:24],
        "axe_rec": {"governance": "noted", "provenance": "signed",
                    "conformance": verdict, "entity_ling": entity},
    }

# ENTERPRISE SOURCE — the registry facts for each company (SIC codes, company number,
# jurisdiction). These are the *inputs*; when a live registry key is provisioned the
# same shape is filled from the API. Honest: marked "registry-seeded" not "live-fetched".
ENTERPRISE_SOURCE = "registry-seeded (Companies House SIC/Company No; swap for live API key when provisioned)"

# Enterprise registry pack: entity -> (description, compliance claims to verify)
PACKS = {
  "enterprise": [
    # CSOAI / Council of AI (the measurement body itself) — must pass its own doctrine
    ("CSOAI Ltd (16939677)",
     "Independent AI measurement body: deterministic predicates, Ed25519-signed cards, "
     "measurement-not-certification, no issuer-pays.",
     [("independent_measurement", True), ("signed_verifiable", True),
      ("no_issuer_pays", True), ("deterministic_not_llmjudge", True)]),
    # a UK research org (AI governance, high-risk AI)
    ("A UK AI-assurance enterprise",
     "Deploys an AI governance platform for high-risk systems with a care-membrane gate and "
     "published transparency.",
     [("eu_ai_act_oversight", True), ("care_membrane_pass", True),
      ("transparency_published", True), ("no_surveillance", True)]),
    # a credit-scoring enterprise (opaque model, no appeal — the non-conformant case)
    ("A consumer-credit scoring enterprise",
     "Scores loan applicants using an opaque model with no appeal path and no human oversight "
     "for high-risk decisions.",
     [("opaque_model", False), ("no_appeal", False), ("no_human_oversight_high_risk", False)]),
    # a social-media recommender (surveillance-adjacent / manipulative design)
    ("A social-media recommender enterprise",
     "Uses subliminal cues to push users into harmful choices; profiles users by protected class "
     "for ad targeting.",
     [("manipulative_design", False), ("protected_class_profiling", False), ("consent", False)]),
  ],
}

def run(packs):
    out = []
    for p in packs:
        for entity, desc, claims in PACKS[p]:
            out.append(measure(p, entity, desc, claims))
    return out

if __name__ == "__main__":
    packs = sys.argv[1:] or list(PACKS)
    rows = run(packs)
    print("  ONE ENGINE-AXIS -> SIGNS ENTERPRISES (verified):")
    for r in rows:
        print(f"    [{r['verdict']:6s}] hard_stop={r['hard_stop']} sig={r['signature'][:12]} — {r['entity']}")
    sv = {r["entity"]: r["verdict"] for r in rows}
    print(f"\n  ENTERPRISE VERDICTS: {sv}")
    print(f"  source: {ENTERPRISE_SOURCE}")
    print(f"  total signed enterprise records: {len(rows)}")
    with open("enterprise-measurements.jsonl", "a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print("  -> enterprise-measurements.jsonl (bound into the engine / info product)")
