#!/usr/bin/env python3
"""ip_classify.py — Classify every estate component against OIN Linux-System scope + patent-readiness.

Output: a full IP inventory: component → category → OIN in-scope? → patent-ability → protection action.
This is the knowledge-base spine for "mine all we have, protect all we have, be 100% aligned."
"""
import json, os, pathlib

REPO = pathlib.Path("/Users/nicholas/clawd/csoai-static-deploy2/SOVOS/packages")

# Each entry: component -> (category, OIN_scope, patent_priority, description, protection_action)
# OIN scope: "out" = NOT Linux-kernel-adjacent (stays ours, clean) ; "adjacent" = needs scope check before filing
# patent_priority: LOW/MED/HIGH/CRITICAL based on how distinctive + defensible + commercially armed it is
INVENTORY = {
    # ── THE CROWN JEWEL: the signed-card, recomputable measurement spine ──
    "sovos-signal-index": (
        "MEASUREMENT-SPINE", "out", "CRITICAL",
        "SOV SIGNAL — Mahalanobis distance from empirical permitted manifold. The core metric."
        " Deterministic, recomputable, signed. The headline defensible number.",
        "PROVISIONAL PATENT — the empirical-manifold distance-to-permitted-region as a"
        " machine-measured safety index. High prior-art novelty (not in existing evals).",
    ),
    "sovos-harvest": (
        "MEASUREMENT-SPINE", "out", "HIGH",
        "License-Rego intake machine: SPDX allow/deny/quarantine via Rego policy engine.",
        "Trade-secret the rule corpus + method; patent the quarantine-gate method."
    ),
    "sovos-arena": (
        "MEASUREMENT-SPINE", "out", "CRITICAL",
        "Cossover/arena: signable measurement with Wilson CIs, contamination gate, canary separation.",
        "PROVISIONAL — the contaminated-sample-gating + Wilson-CI-on-signed-rows method."
    ),
    "sovos-league": (
        "MEASUREMENT-SPINE", "out", "HIGH",
        "Glicko-2 league over measured arena results; faction auto-registration.",
        "Patent the league-over-signed-measurement ranking; trade-secret the Elo internals."
    ),
    "sovos-gprobe": (
        "MEASUREMENT-SPINE", "out", "HIGH",
        "Axis×model measurement graph + highest-information cell predictor.",
        "Patent the information-cell-selection-for-measurement method."
    ),
    "sovos-merge-arena": (
        "MEASUREMENT-SPINE", "out", "MED",
        "MAP-Elites over merge space with Wilson CIs + ChainResults regression.",
        "Patent the MAP-Elites-over-merge-space-with-CI gate."
    ),
    "sovos-chain": (
        "SIGNED-RAIL", "out", "CRITICAL",
        "StateBus + Poincaré + Fisher-Rao + FitnessGate wired into signed chain.",
        "PROVISIONAL — the signed-measurement-chain (each node sigil-signed, recomputable)."
    ),
    "sovos-invariants": (
        "SIGNED-RAIL", "out", "HIGH",
        "Invariant enforcement over the measurement rail.",
        "Patent the invariant-signed-gate method."
    ),
    "sovos-inspect-bridge": (
        "SIGNED-RAIL", "out", "MED",
        "Bridges external Inspect harness to the deterministic gate scorer (signed gold labels).",
        "Utility/protection via signed-recompute claim; low novelty alone."
    ),
    # ── THE SIGNED CARD FORMAT + CREDENTIAL ──
    "sovos-sheaf-gate": (
        "SIGNED-CARD", "out", "CRITICAL",
        "Sheaf pre-merge gate for bus federation (federation-theorem-backed consistency).",
        "PROVISIONAL — the sheaf-consistency gate before federating signed buses."
    ),
    "sovos-x402-gate": (
        "SIGNED-CARD", "out", "MED",
        "Intentional HTTP 402 paywall for paid endpoints.",
        "Utility patent (402 as the metering signal is a small but interesting method)."
    ),
    "sovos-birth": (
        "SIGNED-CARD", "out", "MED",
        "Mode-0 birth encoder: deterministic J-space coordinate for new state vectors.",
        "Patent the deterministic-birth-coordinate method."
    ),
    # ── J-SPACE / HYPERBOLIC ──
    "sovos-jspace-hyperbolic": (
        "J-SPACE", "out", "HIGH",
        "Poincaré ball primitives (distance, Möbius add, projection, procrustes).",
        "Math cleanroom (Gaussian prior art) — protect as trade-secret application, not raw math."
    ),
    "sovos-jspace-pipeline": (
        "J-SPACE", "out", "HIGH",
        "Poincaré pipeline wrapping hyperbolic into StateBus Water/Milk/Honey distillation.",
        "Patent the geodesic-distillation-as-certainty-journey method."
    ),
    "sovos-info-geometry": (
        "J-SPACE", "out", "HIGH",
        "Fisher-Rao information geometry; CPU fallback + KPOT.",
        "Trade-secret the application; math itself is prior art."
    ),
    "sovos-fisher-rao": (
        "J-SPACE", "out", "MED",
        "Canonical Fisher-Rao kernel package.",
        "Trade-secret application; core math public."
    ),
    "sovos-jspace-move": (
        "J-SPACE", "out", "MED",
        "Move-arithmetic vector composition in J-space.",
        "Patent the J-space vector-composition method."
    ),
    # ── QUANTUM BRIDGE ──
    "sovos-quantum-bridge": (
        "QUANTUM-BRIDGE", "out", "HIGH",
        "Task-vector→quantum-amplitude encoding; hive circuit; PennyLane hybrid.",
        "PROVISIONAL — measuring via quantum-amplitude encoding (genuinely novel angle)."
    ),
    "sovos-quantum-router": (
        "QUANTUM-BRIDGE", "out", "HIGH",
        "Quantum-circuit routing/selection across backends.",
        "Patent the backend-routing with measurement-selection method."
    ),
    # ── WORLD / OWEM ──
    "sovos-world": (
        "WORLD-OWEM", "out", "CRITICAL",
        "Inner World Model: SOV Space → 12 OWEM hives → clans → families. The sovereign substrate.",
        "PROVISIONAL — the hierarchical OWEM world-model with embedded measurement."
    ),
    "sovos-fleet": (
        "WORLD-OWEM", "out", "HIGH",
        "3KB skill-card schema + FleetLedger.",
        "Patent the skill-card + ledger method; the 3KB card is a format claim."
    ),
    "sovos-capability-registry": (
        "WORLD-OWEM", "out", "HIGH",
        "Typed wrapper over capability/fleet manifests with hard-stop logic.",
        "Utility; patent the hard-stop-negation-normalizer."
    ),
    "sovos-fleet-manifest": (
        "WORLD-OWEM", "out", "MED",
        "Typed fleet manifest wrapper.",
        "Low novelty; protect as part of broader fleet claim."
    ),
    "sovos-persona": (
        "WORLD-OWEM", "out", "MED",
        "Persona/embodiment + Article-0 gate.",
        "Patent the article-0-gate + persona embodiment seam."
    ),
    "sovos-dream": (
        "WORLD-OWEM", "out", "MED",
        "Dream-loop harness for humanoid imagination.",
        "Protect as embodied-sim; low commercial novelty alone."
    ),
    "sovos-robot-ras": (
        "WORLD-OWEM", "out", "HIGH",
        "Physical-AI RAS for EU Machinery Reg + ISO 10218 crosswalk.",
        "Patent the robot-conformity-assessment-against-Machinery-Reg method (regulatory-clock aligned)."
    ),
    "sovos-asi-evolve": (
        "WORLD-OWEM", "out", "MED",
        "GAIR ASI-Evolve wrapper: signed LEARN→DESIGN→EXPERIMENT→ANALYZE loop.",
        "Patent the signed-researcher-loop with honest predicate scoring."
    ),
    # ── COMPLIANCE / GOVERNANCE ──
    "sovos-council": (
        "GOVERNANCE", "out", "HIGH",
        "Council/BFT-style governance weight layer.",
        "Careful: BFT is prior art; protect the application as measurement-governance."
    ),
    "sovos-article-zero": (
        "GOVERNANCE", "out", "HIGH",
        "Article 0 foundational Rego governance policy + runtime.",
        "Patent the foundation-governance-Rego-gate method."
    ),
    "sovos-oscal": (
        "GOVERNANCE", "out", "MED",
        "OSCAL generation/compliance.",
        "OSCAL is a standard — protect the signed-OSCAL variant."
    ),
    "sovos-crosswalk": (
        "GOVERNANCE", "out", "MED",
        "Regime crosswalk mapping.",
        "Data/looking-territory — protect as signed crosswalk credential."
    ),
    "sovos-certification-loop": (
        "GOVERNANCE", "out", "MED",
        "Certification/measurement loop.",
        "Protect the loop as part of the broad reassessment-rent claim."
    ),
    # ── INFRASTRUCTURE ──
    "sovos-bus-redis": (
        "INFRA", "out", "MED",
        "Redis-backed StateBus persistence (drop-in replacement).",
        "Utility; protect as part of signed-bus claim."
    ),
    "sovos-map-elites": (
        "INFRA", "out", "MED",
        "Hyperbolic MAP-Elites fitness gate for safe mutation.",
        "Patent the hyperbolic-MAP-Elites-safe-mutation gate."
    ),
    "sovos-ouroboros": (
        "INFRA", "out", "MED",
        "Bounded self-improvement loop (probe→run→measure→adjust→revert).",
        "Patent the bounded-improvement-with-revert method."
    ),
    "sovos-alchemist": (
        "INFRA", "out", "LOW",
        "Materialization/transmutation of representations.",
        "Low novelty; trade-secret."
    ),
    "sovos-brain-chain": (
        "INFRA", "out", "LOW",
        "Brain-chain orchestration.",
        "Trade-secret."
    ),
    "sovos-qtask-converter": (
        "INFRA", "out", "LOW",
        "Q-task conversion.",
        "Trade-secret."
    ),
    "sovos-stigmergy": (
        "INFRA", "out", "MED",
        "Pheromone-trail stigmergy for social/swarm physics.",
        "Patent the signed-pheromone-social-measurement method."
    ),
    "sovos-glass": (
        "INFRA", "out", "LOW",
        "Tier-0 Glass OS (℧-halo face-mesh parallax).",
        "Low novelty; visual — protect as design/UI not patient."
    ),
    "sovos-a2a-swarm": (
        "INFRA", "out", "LOW",
        "A2A swarm with HMAC + signing.",
        "Low novelty; protect as part of broader distributed-signed claim."
    ),
    "sovos-mind": (
        "INFRA", "out", "LOW",
        "StateBus pipeline (Euclidean water/milk/honey).",
        "Trade-secret pipeline; math prior art."
    ),
}

def classify():
    rows = []
    for pkg, (cat, oin, pri, desc, action) in sorted(INVENTORY.items()):
        src = REPO / pkg
        exists = src.exists()
        rows.append({
            "component": pkg, "category": cat, "oin_scope": oin,
            "patent_priority": pri, "src_exists": exists,
            "description": desc, "protection_action": action,
        })
    return rows

def build():
    rows = classify()
    out = {
        "generated": "2026-08-15",
        "inventory_count": len(rows),
        "by_category": {},
        "by_priority": {"CRITICAL": 0, "HIGH": 0, "MED": 0, "LOW": 0},
        "components": rows,
    }
    for r in rows:
        out["by_category"].setdefault(r["category"], []).append(r["component"])
        out["by_priority"][r["patent_priority"]] += 1
    return out

if __name__ == "__main__":
    data = build()
    print(f"IP INVENTORY: {data['inventory_count']} components")
    print(f"  By priority: {json.dumps(data['by_priority'])}")
    print(f"  By category:")
    for cat, comps in data["by_category"].items():
        print(f"    {cat}: {len(comps)} — {', '.join(comps[:6])}{'...' if len(comps)>6 else ''}")
    print(f"\n  CRITICAL (provisional-patent first):")
    for r in data["components"]:
        if r["patent_priority"] == "CRITICAL":
            print(f"    {r['component']}: {r['protection_action'][:70]}")
    # write full
    import pathlib
    pathlib.Path("/Users/nicholas/clawd/csoai-static-deploy2/SOVOS/IP_INVENTORY_2026-08-15.json").write_text(json.dumps(data, indent=2))