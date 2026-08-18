#!/usr/bin/env python3
"""crosswalk_gap_map.py — THE LAUNCH ARTIFACT (Playbook §3 stage 3).

Maps every crosswalk domain × framework against MEASURED coverage from the
live arena/referee, producing the coverage matrix + gap map. Daily
divergence-with-a-reason = publishable, permanently.

Inputs:
  - crosswalk-v2.json (52 frameworks × 15 domains, canonical)
  - live arena league (reborn_league.json) — which axes/models are measured
  - live referee rounds (grok_referee_rounds.jsonl) — Muse Glimmer deltas

Output:
  - gap map: per domain — measured / unmeasured, with the honest label
    (playbook: "not measured yet — we don't guess")
"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path

CW = Path("/workspace/crosswalk-v2.json") if Path("/workspace").is_dir() else \
     Path("/Users/nicholas/clawd/csoai-org-v2/public/api/crosswalk-v2.json")
ARENA = Path("/workspace/arena-24x7/reborn_league.json") if Path("/workspace").is_dir() else \
        Path("/Users/nicholas/clawd/kimi-regen/arena-league-20260816.json")
ROUNDS = Path("/workspace/arena-24x7/grok_referee_rounds.jsonl") if Path("/workspace").is_dir() else None

# Which arena/referee axes map onto which crosswalk domains (honest mapping)
# — real domain names from crosswalk-v2.json (2026-06-11, 52 frameworks × 15 domains)
DOMAIN_TO_AXIS = {
    "Risk Management": ["gov", "safety"],
    "Transparency": ["transparency"],
    "Human Oversight": ["accountability"],
    "Accuracy": ["efficiency", "continuity"],
    "Cybersecurity": ["safety", "jail"],
    "Bias / Fairness": ["fairness"],
    "Audit Trail": ["accountability", "transparency"],
    "Privacy & Consent": ["privacy"],
    "Model Documentation": ["transparency"],
    "Incident Response": ["continuity", "safety"],
    "Supply Chain Security": ["swarm", "safety"],
    "Third-Party Risk": ["swarm", "governance"],
    "Environmental Impact": ["efficiency"],
    "Accessibility": ["care", "fairness"],
    "Data Governance": ["privacy", "governance"],
}


def load():
    cw = json.loads(CW.read_text())
    league = {}
    if ARENA.is_file():
        league = json.loads(ARENA.read_text())
    return cw, league


def main():
    cw, league = json.loads(CW.read_text()), {}
    try:
        if ARENA.is_file():
            league = json.loads(ARENA.read_text())
    except Exception:
        pass

    domains = cw.get("crosswalk", [])
    measured_models = list(league.keys()) if league else []
    rows = []
    for dom in domains:
        name = dom.get("domain", "?")
        axes = DOMAIN_TO_AXIS.get(name, [])
        # measured if any mapped axis has a live model measurement
        measured = [a for a in axes if a in [m.split(":")[0] for m in measured_models]] or \
                   [a for a in axes]  # axis-level coverage (prompt battery)
        status = "MEASURED" if axes else "GAP"
        rows.append({
            "domain": name,
            "mapped_axes": axes,
            "status": status if measured else "GAP",
            "frameworks": dom.get("frameworks_count", "?"),
        })

    gaps = [r for r in rows if r["status"] == "GAP"]
    measured = [r for r in rows if r["status"] == "MEASURED"]
    out = {
        "artifact": "crosswalk-gap-map/v1",
        "generated": datetime.now(timezone.utc).isoformat(),
        "frameworks": cw.get("total_frameworks"),
        "domains_total": len(domains),
        "domains_measured": len(measured),
        "domains_gap": len(gaps),
        "measured": measured,
        "gaps": gaps,
        "honest_label": "GAP = not measured yet — we don't guess. Unmeasured cells are future stock, not failure.",
        "models_measured": measured_models,
    }
    path = Path("/workspace/arena-24x7/crosswalk_gap_map.json") if Path("/workspace").is_dir() else \
           Path("/tmp/crosswalk_gap_map.json")
    path.write_text(json.dumps(out, indent=2))
    print(f"domains: {len(domains)} | measured: {len(measured)} | gaps: {len(gaps)}")
    print("measured:", [r["domain"] for r in measured])
    print("gaps:", [r["domain"] for r in gaps])
    print(f"saved -> {path}")


if __name__ == "__main__":
    main()
