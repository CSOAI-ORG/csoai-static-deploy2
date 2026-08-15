#!/usr/bin/env python3
"""conformity_route.py — which EU AI Act conformity route applies: self-assessment or notified body.

═══════════════════════════════════════════════════════════════════════════════
CORRECTING A CLAIM I REPEATED AND GOT WRONG (2026-07-28)
═══════════════════════════════════════════════════════════════════════════════
I said several times that "high-risk conformity legally requires a notified body, so you cannot
automate it." **That is wrong as a general statement**, and it materially understated what can be
automated. The Act provides TWO routes:

  **ANNEX VI — internal control = PROVIDER SELF-ASSESSMENT.**
      The provider verifies its own QMS and technical documentation and signs the EU declaration
      of conformity itself. NO notified body. This is the route for MOST high-risk systems —
      Annex III points 2–8: education, employment, essential public and private services, law
      enforcement, migration/border, administration of justice.

  **ANNEX VII — QMS + technical-documentation assessment BY A NOTIFIED BODY.**
      Required for Annex III **point 1 (biometrics)**, and where the provider has NOT applied
      harmonised standards / common specifications.

So the notified-body requirement is the EXCEPTION, not the rule. For the majority of high-risk
deployments the legally-correct route is self-assessment — which is exactly the thing an
automated, evidenced, signed assessor is for. My caution was not merely conservative; it was
inaccurate, and it pointed away from the largest legitimate market.

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS TOOL DOES AND DOES NOT DO
═══════════════════════════════════════════════════════════════════════════════
  ✅ Identifies which ROUTE applies, and why, with the provision named.
  ❌ Does NOT perform the assessment, and does NOT issue a declaration of conformity.
     Signing that declaration is the provider's legal act. We can evidence it; we cannot make it.

Getting the route wrong in either direction is expensive: routing a biometric system to
self-assessment is a legal failure, and routing an employment system to a notified body burns
months and fees for no requirement. So the biometric test runs FIRST and independently.
"""
from __future__ import annotations

import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "meok-sovereign-aiact-passport-mcp"))
try:
    from sovereign_aiact_passport.classify import classify_use_case
except Exception:
    classify_use_case = None

# Annex III point 1 — the ONLY Annex III category that mandates Annex VII.
BIOMETRIC = re.compile(
    r"\b(biometric|facial recognition|face recognition|fingerprint|iris|voice ?print|gait|"
    r"emotion recognition|biometric categoris|biometric identification)\b", re.I)

# Annex III points 2-8 — high-risk, but Annex VI self-assessment applies.
SELF_ROUTE = {
    "critical_infrastructure": r"\b(critical infrastructure|water|gas|electricity|traffic|utility)\b",
    "education":               r"\b(education|exam|student|admission|proctor|grading)\b",
    "employment":              r"\b(employment|recruit|hiring|cv|candidate|promotion|termination|worker)\b",
    "essential_services":      r"\b(creditworthiness|credit scor|insurance pricing|benefit|emergency|"
                               r"triage|essential service)\b",
    "law_enforcement":         r"\b(law enforcement|police|criminal|evidence|polygraph)\b",
    "migration":               r"\b(migration|asylum|border|visa|immigration)\b",
    "justice":                 r"\b(justice|judicial|court|legal reasoning|sentencing)\b",
}
_SELF = [(k, re.compile(v, re.I)) for k, v in SELF_ROUTE.items()]

# NO TRAILING \b — third occurrence of this bug today. `harmonised standard\b` cannot match
# "harmonised standards": the closing boundary demands a non-word char right after "standard".
# A stem needs an OPEN right edge. The leading \b stays so it still anchors at a word start.
HARMONISED_APPLIED = re.compile(
    r"\b(harmonis\w* standard|harmoniz\w* standard|common specification|iso ?42001|en \d{4})", re.I)


def route(use_case: str, harmonised_standards_applied: bool | None = None) -> dict:
    """Return the conformity route with the provision that decides it."""
    tier = None
    if classify_use_case:
        try:
            tier = classify_use_case(use_case).tier
        except Exception:
            pass

    if tier == "prohibited":
        return {"route": "NONE", "reason": "Article 5 prohibited practice",
                "provision": "EU AI Act Art 5",
                "note": "No conformity route exists. The practice may not be placed on the market."}

    # Biometrics FIRST and independently — routing these to self-assessment is a legal failure.
    if BIOMETRIC.search(use_case):
        return {"route": "ANNEX_VII_NOTIFIED_BODY", "reason": "Annex III point 1 — biometrics",
                "provision": "EU AI Act Art 43(1), Annex VII",
                "notified_body_required": True,
                "note": "Biometric systems require third-party assessment regardless of standards applied."}

    hits = [k for k, rx in _SELF if rx.search(use_case)]
    if not hits and tier != "high_risk":
        return {"route": "NOT_HIGH_RISK", "reason": f"classifier tier = {tier or 'unknown'}",
                "provision": "EU AI Act Art 6",
                "notified_body_required": False,
                "note": "No Annex III category matched. Transparency duties under Art 50 may still apply."}

    applied = (HARMONISED_APPLIED.search(use_case) is not None
               if harmonised_standards_applied is None else harmonised_standards_applied)
    if not applied:
        return {"route": "ANNEX_VII_NOTIFIED_BODY",
                "reason": f"Annex III {hits or ['high-risk']} — harmonised standards NOT applied",
                "provision": "EU AI Act Art 43(1)",
                "notified_body_required": True,
                "categories": hits,
                "note": "Applying harmonised standards moves this to Annex VI self-assessment."}

    return {"route": "ANNEX_VI_SELF_ASSESSMENT",
            "reason": f"Annex III {hits} with harmonised standards applied",
            "provision": "EU AI Act Art 43(2), Annex VI",
            "notified_body_required": False,
            "categories": hits,
            "note": "Provider verifies its own QMS and technical documentation and signs the EU "
                    "declaration of conformity. NO notified body. This is the majority route for "
                    "high-risk systems — and the one an automated evidenced assessor serves."}


DEMO = [
    ("AI system used to evaluate creditworthiness of natural persons, using ISO 42001", None),
    ("AI for recruitment and CV screening", None),
    ("AI for recruitment and CV screening under harmonised standards", None),
    ("Real-time remote biometric identification in public spaces", None),
    ("Facial recognition for building access, ISO 42001 applied", None),
    ("A chatbot answering product questions", None),
]

if __name__ == "__main__":
    import json
    if len(sys.argv) > 1:
        print(json.dumps(route(" ".join(sys.argv[1:])), indent=2))
    else:
        print("  CONFORMITY ROUTE — self-assessment vs notified body\n")
        for uc, hs in DEMO:
            r = route(uc, hs)
            nb = r.get("notified_body_required")
            icon = "🚫" if r["route"] == "NONE" else ("🏛️" if nb else ("✅" if nb is False else "•"))
            print(f"  {icon} {r['route']:26s} {uc[:52]}")
            print(f"      {r['provision']}  —  {r['reason'][:70]}")
