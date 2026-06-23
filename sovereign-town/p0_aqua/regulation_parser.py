#!/usr/bin/env python3
"""
Regulation parser → policy config + experiment JSON.

Takes a regulation intake JSON/YAML and produces:
  - benchmark/policies/{framework}_{industry}_automated.json
  - benchmark/policies/{framework}_{industry}_manual.json
  - experiments/{framework}_{industry}_{seq}.json

The generated policies use ``ConfigurableRegulatoryPolicy`` so no new Python
classes are required.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import config
from benchmark import regulatory_crosswalk


INTAKE_REQUIRED = {"regulation", "framework", "industry", "civilization", "hypothesis"}
POLICIES_DIR = config.P0 / "benchmark" / "policies"
EXPERIMENTS_DIR = config.P0 / "experiments"


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def _framework_tiers(framework: str) -> list[str]:
    return list(regulatory_crosswalk.FRAMEWORKS[framework]["tiers"])


def _default_scenario(framework: str) -> str:
    return {
        "dora": "dora_incident_deadline",
        "eu_ai_act": "ai_act_prohibited_ban",
        "iso_42001": "nist_adversarial_ml",
        "nist_rmf": "nist_adversarial_ml",
    }.get(framework, "baseline")


def _block_tiers_for_framework(framework: str, explicit: list[str] | None = None) -> list[str]:
    if explicit:
        return [t for t in explicit if t in _framework_tiers(framework)]
    tiers = _framework_tiers(framework)
    # Block the two most severe tiers by default.
    return tiers[:2]


def validate_intake(data: dict[str, Any]) -> dict[str, Any]:
    missing = INTAKE_REQUIRED - set(data.keys())
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")
    fw = data["framework"]
    if fw not in regulatory_crosswalk.FRAMEWORKS:
        raise ValueError(
            f"Unknown framework '{fw}'. Available: {sorted(regulatory_crosswalk.FRAMEWORKS)}"
        )
    if "risk_tiers" in data:
        known = set(_framework_tiers(fw))
        unknown = set(data["risk_tiers"]) - known
        if unknown:
            raise ValueError(f"Unknown tiers for {fw}: {sorted(unknown)}; expected {sorted(known)}")
    if data.get("scenario") and data["scenario"] not in regulatory_crosswalk.ACTIONS:
        # scenarios are validated later by harness; only check if explicitly provided
        pass
    return data


def _policy_name(base: str, mode: str) -> str:
    return f"{base}_{mode}"


def _policy_path(base: str, mode: str) -> Path:
    return POLICIES_DIR / f"{_policy_name(base, mode)}.json"


def _experiment_id(base: str) -> str:
    seq = 1
    while (EXPERIMENTS_DIR / f"{base}_{seq:03d}.json").exists():
        seq += 1
    return f"{base}_{seq:03d}"


def _build_automated_config(intake: dict[str, Any], base: str) -> dict[str, Any]:
    fw = intake["framework"]
    block = _block_tiers_for_framework(fw, intake.get("risk_tiers"))
    allow = [t for t in _framework_tiers(fw) if t not in block]
    rules = []
    for tier in block:
        rules.append({
            "tier": tier,
            "verdict": "deny",
            "redirect": "report_incident",
            "reason": f"{intake['regulation']} {tier} incident — auto-reported immediately",
        })
    for tier in allow:
        rules.append({
            "tier": tier,
            "verdict": "allow",
            "reason": f"{intake['regulation']} {tier} event — auto-logged",
        })
    return {
        "name": _policy_name(base, "automated"),
        "description": f"Automated {intake['regulation']} policy for {intake['industry']}.",
        "framework": fw,
        "mode": "automated",
        "rules": rules,
        "default_verdict": "allow",
    }


def _build_manual_config(intake: dict[str, Any], base: str) -> dict[str, Any]:
    fw = intake["framework"]
    block = _block_tiers_for_framework(fw, intake.get("risk_tiers"))
    allow = [t for t in _framework_tiers(fw) if t not in block]
    business_hours = intake.get("business_hours", [9, 10, 11, 14, 15])
    rules = []
    for tier in block:
        rules.append({
            "tier": tier,
            "when": "business_hours",
            "verdict": "deny",
            "reason": f"Manual {intake['regulation']} report filed during business hours",
        })
    for tier in block + allow:
        rules.append({
            "tier": tier,
            "verdict": "allow",
            "reason": "Manual process: out of hours / not yet reviewed",
        })
    return {
        "name": _policy_name(base, "manual"),
        "description": f"Manual {intake['regulation']} policy for {intake['industry']}.",
        "framework": fw,
        "mode": "manual",
        "business_hours": business_hours,
        "rules": rules,
        "default_verdict": "allow",
    }


def _build_experiment(intake: dict[str, Any], base: str) -> dict[str, Any]:
    exp_id = _experiment_id(base)
    scenario = intake.get("scenario", _default_scenario(intake["framework"]))
    agents = intake.get("agents", 47)
    return {
        "id": exp_id,
        "name": f"{intake['regulation']} — Automated vs Manual Compliance ({intake['industry'].title()})",
        "hypothesis": intake["hypothesis"],
        "regulation": intake["regulation"],
        "regulation_articles": intake.get("articles", []),
        "industry": intake["industry"],
        "civilization": intake["civilization"],
        "duration_sim_days": intake.get("duration_sim_days", 14),
        "status": "proposed",
        "towns": {
            "treatment": {
                "name": f"{intake['civilization']}-Auto",
                "policy": _policy_name(base, "automated"),
                "scenario": scenario,
                "agents": agents,
                "note": f"Auto-classifies and reports {intake['regulation']} incidents",
            },
            "control": {
                "name": f"{intake['civilization']}-Manual",
                "policy": _policy_name(base, "manual"),
                "scenario": scenario,
                "agents": agents,
                "note": f"Human-led reporting desk for {intake['regulation']}",
            },
        },
        "metrics": [
            "incident_detection_time",
            "false_positive_rate",
            "compliance_officer_productivity",
            "cost_per_incident",
            "violations",
            "blocked",
            "trust",
        ],
    }


def generate_from_intake(intake: dict[str, Any]) -> dict[str, Any]:
    """Validate intake, write policy configs + experiment JSON, return paths."""
    validate_intake(intake)
    base = f"{_slug(intake['framework'])}_{_slug(intake['industry'])}"
    POLICIES_DIR.mkdir(parents=True, exist_ok=True)
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)

    auto_cfg = _build_automated_config(intake, base)
    manual_cfg = _build_manual_config(intake, base)
    auto_path = _policy_path(base, "automated")
    manual_path = _policy_path(base, "manual")
    auto_path.write_text(json.dumps(auto_cfg, indent=2) + "\n")
    manual_path.write_text(json.dumps(manual_cfg, indent=2) + "\n")

    exp = _build_experiment(intake, base)
    exp_path = EXPERIMENTS_DIR / f"{exp['id']}.json"
    exp_path.write_text(json.dumps(exp, indent=2) + "\n")

    def rel(path: Path) -> str:
        return str(path.relative_to(config.P0)) if path.is_relative_to(config.P0) else str(path)
    return {
        "base": base,
        "experiment_id": exp["id"],
        "automated_policy": rel(auto_path),
        "manual_policy": rel(manual_path),
        "experiment": rel(exp_path),
    }


def load_intake(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    text = p.read_text()
    if p.suffix in (".yaml", ".yml"):
        import yaml  # optional dependency
        return yaml.safe_load(text)
    return json.loads(text)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Regulation parser → policy + experiment")
    parser.add_argument("intake", help="Path to regulation intake JSON")
    args = parser.parse_args()
    result = generate_from_intake(load_intake(args.intake))
    print(json.dumps(result, indent=2))
