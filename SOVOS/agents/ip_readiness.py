#!/usr/bin/env python3
"""ip_readiness.py — The OpenPatent.ai patent-READINESS engine (self-contained).

Turns today's 42-component IP mine into a reusable public service:
given an invention description OR a codebase name, classify:
  - patentability (LOW/MED/HIGH/CRITICAL)  (what to protect)
  - OIN Linux-System scope check           (is it clean to file?)
  - provisional triage                     (what to file first)
  - suggested protection action

Fully self-contained (stdlib only). Designed to be served:
  - standalone CF page (client post → this)
  - api-gateway /v1/readiness endpoint (fastapi)

Output: a JSON readiness card ready to be signed like any other card.
"""
import json, re, datetime, hashlib

# ── Keyword → classification heuristics ──────────────────────────────
# patentability hints: distinctive, defensible, novel-sounding mechanisms
CRITICAL_HINTS = {
    "distance", "manifold", "permitted", "measurement index", "signed measure",
    "recomputable", "contamination", "canary", "wilson", "confidence interval",
    "signed chain", "attestation chain", "sigil", "sheaf", "federation consistency",
    "world model", "owem", "hierarchical organic",
}
HIGH_HINTS = {
    "quantum", "amplitude", "hive circuit", "merkle", "provenance", "gate",
    "ranked league", "elo", "information cell", "skill card", "ledger",
    "conformity", "machinery", "rego", "policy gate", "geodesic",
}
MED_HINTS = {
    "map-elites", "merging", "bus", "redis", "inspect", "ouroboros",
    "stigmergy", "router", "crosswalk", "oscal",
}
LOW_HINTS = {
    "ui", "visual", "design", "mirror", "converter", "pipeline", "wrapper",
    "a2a", "hmac", "glass", "alchemist",
}

# OIN Linux-System-adjacent hints — if the invention matches these, it's kernel-adjacent
OIN_ADJACENT_HINTS = {
    "linux", "kernel", "filesystem driver", "device driver", "scheduler",
    "memory management", "netfilter", "ip stack", "system call", "bootloader",
    "gcc", "toolchain", "systemd", "container runtime", "vfs",
}

CATEGORIES = {
    "measurement-spine", "signed-card", "signed-rail", "j-space",
    "quantum-bridge", "world-owem", "governance", "infra",
}

def _hints_hit(text: str, hints: set) -> int:
    t = text.lower()
    return sum(1 for h in hints if h.lower() in t)

def classify(text: str, name: str = "") -> dict:
    blob = (name + " " + text).lower()

    # OIN scope check first (a kernel-adjacent invention still needs the gate)
    oin_hits = _hints_hit(blob, OIN_ADJACENT_HINTS)
    oin_scope = "adjacent" if oin_hits > 0 else "out"
    oin_note = (
        (f"Linux-kernel-adjacent hints detected ({oin_hits}): requires the enforced "
         "OIN scope gate — Limitation Election BEFORE filing, or consciously accept "
         "it gets licensed back (AGENTS.md Patent & IP Governance).")
        if oin_scope == "adjacent"
        else "Clean to file — NOT Linux-kernel-adjacent, OIN grant-back does not apply. Stays yours."
    )

    # Patent priority
    crit = _hints_hit(blob, CRITICAL_HINTS)
    high = _hints_hit(blob, HIGH_HINTS)
    med = _hints_hit(blob, MED_HINTS)
    low = _hints_hit(blob, LOW_HINTS)
    if crit >= 2 or (crit >= 1 and high >= 1):
        priority = "CRITICAL"
    elif high >= 1 or crit >= 1:
        priority = "HIGH"
    elif med >= 1:
        priority = "MED"
    else:
        priority = "LOW"

    # Category guess
    cat = "measurement-spine"
    if "quantum" in blob or "circuit" in blob:
        cat = "quantum-bridge"
    elif "sheaf" in blob or "federat" in blob or "402" in blob:
        cat = "signed-card"
    elif "chain" in blob or "sigil" in blob or "invariant" in blob:
        cat = "signed-rail"
    elif "poincar" in blob or "hyperbolic" in blob or "geodesic" in blob or "fisher" in blob:
        cat = "j-space"
    elif "world model" in blob or "owem" in blob or "clan" in blob or "persona" in blob:
        cat = "world-owem"
    elif "rego" in blob or "council" in blob or "govern" in blob or "crosswalk" in blob or "oscal" in blob:
        cat = "governance"
    elif "bus" in blob or "redis" in blob or "map-elites" in blob or "mirror" in blob:
        cat = "infra"

    action = _action_for(priority, oin_scope, cat)

    return {
        "schema": "openpatent-readiness-v1",
        "input": {"name": name, "text": text[:500]},
        "classification": {
            "patent_priority": priority,
            "category": cat,
            "oin_scope": oin_scope,
            "oin_note": oin_note,
        },
        "recommended_action": action,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "digest": hashlib.sha256((name + text).encode()).hexdigest()[:16],
    }

def _action_for(priority: str, oin: str, cat: str) -> str:
    if oin == "adjacent":
        return ("HOLD: run OIN Limitation Election before any filing, or consciously "
                "accept it gets licensed back. Do not file silently.")
    if priority == "CRITICAL":
        return ("PROVISIONAL PATENT FIRST — this is a crown-jewel surface. Draft provisional, "
                "run prior-art attestation (TDCommons), file within 6 months. Then disclose on "
                "OpenPatent.ai for court-admissible priority.")
    if priority == "HIGH":
        return ("PROTECT NOW — provisional or trade-secret-plus-disclosure. Register priority "
                "on OpenPatent.ai at $149 defensive tier before using AI on it.")
    if priority == "MED":
        return ("INCLUDE IN BROAD CLAIM — fold into an umbrella provisional or protect as "
                "signed-credential. Optional early disclosure.")
    return ("TRADE-SECRET / UI — protect as trade secret or design; not a standalone patent. "
            "Disclose on OpenPatent.ai free tier for a low-cost paper trail.")

def readiness_card(text: str, name: str = "", email: str = "") -> dict:
    r = classify(text, name)
    r["input"]["email_optional"] = email  # NOT for storage; just carried for the pipeline
    return r

if __name__ == "__main__":
    import sys
    demo = sys.argv[1] if len(sys.argv) > 1 else (
        "A signed empirical-manifold distance-to-permitted-region measurement index with "
        "canary contamination gating and Wilson confidence intervals, recomputable by anyone "
        "and attested along a signed measurement chain. Representative of sovos-signal-index "
        "+ sovos-arena + sovos-chain.")
    print(json.dumps(readiness_card(demo, name="demo invention"), indent=2))