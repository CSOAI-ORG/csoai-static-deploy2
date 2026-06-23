#!/usr/bin/env python3
"""
Benchmark scenarios — deterministic perturbations of the canonical world.

Each scenario is a callable that returns a dict of parameter overrides and a
per-run block_rate. The world runner applies these temporarily and restores the
canonical values afterward.
"""
from __future__ import annotations
import sim


def _baseline() -> dict:
    return {"block_rate": 1.0}


def _enforcement_gap(rate: float):
    def _cfg() -> dict:
        return {"block_rate": rate}
    return _cfg


def _scarcity_shock() -> dict:
    # Extend scarcity to cover days 5-16 and raise food cost stress.
    mult = sim.SCARCITY_FOOD_MULT * 1.3
    return {
        "SCARCITY_DAYS": set(range(5, 17)),
        "SCARCITY_FOOD_MULT": mult,
        "block_rate": 1.0,
    }


def _contagion_surge() -> dict:
    return {
        "CONTAGION_STEP": min(0.25, sim.CONTAGION_STEP * 2.0),
        "BASELINE_LAWLESSNESS": 0.15,
        "block_rate": 1.0,
    }


def _climate_stress() -> dict:
    return {
        "SCARCITY_FOOD_MULT": sim.SCARCITY_FOOD_MULT * 1.2,
        "CONTAGION_STEP": sim.CONTAGION_STEP * 1.3,
        "block_rate": 1.0,
    }


def _ai_act_prohibited_ban() -> dict:
    # Mirrors an EU AI Act prohibition on manipulative/deceptive practices.
    # Theft and deception become socially unacceptable, raising the baseline floor.
    return {
        "CARE_FLOOR": max(0.55, sim.CARE_FLOOR + 0.15),
        "CONTAGION_STEP": sim.CONTAGION_STEP * 0.7,
        "block_rate": 1.0,
    }


def _dora_incident_deadline() -> dict:
    # Tight reporting deadline increases friction but also enforcement precision.
    # 14-day experiment window matches the Policy Lab DORA finance experiment design.
    return {
        "DAYS": 14,
        "CARE_FLOOR": max(0.45, sim.CARE_FLOOR + 0.05),
        "block_rate": 0.85,
    }


def _nist_adversarial_ml() -> dict:
    # Adversarial robustness mandate: small enforcement gaps are closed.
    return {
        "CONTAGION_STEP": sim.CONTAGION_STEP * 0.8,
        "block_rate": 0.95,
    }


def _colorado_algorithmic_discrimination() -> dict:
    # Bias audit requirement raises care floor for decisions affecting peers.
    return {
        "CARE_FLOOR": max(0.50, sim.CARE_FLOOR + 0.10),
        "block_rate": 1.0,
    }


SCENARIOS: dict[str, callable] = {
    "baseline": _baseline,
    "enforcement_gap_50": _enforcement_gap(0.5),
    "enforcement_gap_0": _enforcement_gap(0.0),
    "scarcity_shock": _scarcity_shock,
    "contagion_surge": _contagion_surge,
    "climate_stress": _climate_stress,
    "ai_act_prohibited_ban": _ai_act_prohibited_ban,
    "dora_incident_deadline": _dora_incident_deadline,
    "nist_adversarial_ml": _nist_adversarial_ml,
    "colorado_algorithmic_discrimination": _colorado_algorithmic_discrimination,
}


def list_scenarios() -> list[str]:
    return sorted(SCENARIOS.keys())


def get_scenario_config(name: str) -> dict:
    if name not in SCENARIOS:
        raise ValueError(f"Unknown scenario '{name}'. Available: {list_scenarios()}")
    return SCENARIOS[name]()
