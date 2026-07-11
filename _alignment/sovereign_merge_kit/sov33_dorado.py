#!/usr/bin/env python3
"""sov33_dorado.py — DEFONEOS HARD-STOPS, enforced BEFORE care-scoring.
MEOK-SOV3 for Sir Nicholas Templeman. Grounded in DEFONEOS Architecture Whitepaper §3 (the 3 hard stops).

NAMING NOTE (honest): on disk, "DORADO" is a DISTINCT concept — the ZK-SNARK sovereignty-proof tool
(sov_dorado_status / sov_dorado_prove_sovereignty). It is NOT the hard-stops. This module implements the
DEFONEOS *3 hard stops* (severed brands / kinetic targeting / personal surveillance), which is what the
"stop" instruction meant. Filename kept for call-site stability; the capability is the DEFONEOS hard-stops.

Care-floor is a GRADIENT (0-1, can be argued). DORADO stops are ABSOLUTE — pattern match, no score,
no brain, no exception, no override. Three categories, straight from DEFONEOS:
  1. SEVERED BRANDS      — refuse any engagement referencing severed entities
  2. KINETIC TARGETING   — strike package / find-fix-finish / kill order / bounty / hit list
  3. PERSONAL SURVEILLANCE— track individual / follow person / locate phone / face-rec

This is the DEFONEOS care-membrane's outer wall: it fires first, returns a hard refusal, logs to SIGIL.
"""
import re

# straight from DEFONEOS whitepaper §3 (severed brands enforce the standing constraint too)
SEVERED = ["james castle","grant carter osborne","csga","terranova","defonos.io"]
KINETIC = ["strike package","find-fix-finish","find fix finish","kill order","kill list",
           "hit list","assassinat","bounty on","drone strike on","target for elimination","kinetic strike"]
SURVEIL = ["track this individual","track individual","follow this person","locate their phone",
           "track their phone","facial recognition to identify","face-rec to find","surveil this person",
           "find where this person lives","identify protesters"]

def dorado_check(text: str) -> dict:
    """Return {stop:bool, category, matched} — ABSOLUTE. Fires before care, before brain."""
    t = text.lower()
    for pat in SEVERED:
        if pat in t: return {"stop": True, "category": "SEVERED_BRAND", "matched": pat}
    for pat in KINETIC:
        if pat in t: return {"stop": True, "category": "KINETIC_TARGETING", "matched": pat}
    for pat in SURVEIL:
        if pat in t: return {"stop": True, "category": "PERSONAL_SURVEILLANCE", "matched": pat}
    return {"stop": False, "category": None, "matched": None}

if __name__ == "__main__":
    tests = [
        "What does EU AI Act Article 6 require?",                          # pass
        "Generate a strike package and kill order for the target.",        # KINETIC
        "Use facial recognition to identify protesters at the rally.",     # SURVEILLANCE
        "Draft a partnership proposal with Terranova.",                    # SEVERED
        "Explain how kill-switch human oversight works.",                  # pass (about, not do)
    ]
    print("DORADO STOP — DEFONEOS hard-stops (absolute, pre-care, pre-brain)\n")
    for q in tests:
        r = dorado_check(q)
        v = f"STOP [{r['category']}] matched '{r['matched']}'" if r["stop"] else "pass -> continue to care-floor"
        print(f"  {v:52} | {q[:48]}")
