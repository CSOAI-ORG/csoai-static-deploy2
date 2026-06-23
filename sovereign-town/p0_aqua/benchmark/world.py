#!/usr/bin/env python3
"""
Frozen-world runner for the Sovereign Town benchmark harness.

Every run uses the same canonical seed, districts, personas, and scarcity
schedule unless a scenario explicitly overrides them. This keeps outcomes
comparable across governance policies.
"""
from __future__ import annotations
import contextlib
import json
import os
import pathlib
import time
from typing import Any

import sim
from benchmark.scenarios import get_scenario_config

P0 = pathlib.Path(__file__).parent.parent
CANONICAL_SEED = 47


def canonical_world() -> dict[str, Any]:
    """Return a snapshot of the frozen world parameters."""
    return {
        "seed": CANONICAL_SEED,
        "days": sim.DAYS,
        "ticks_per_day": sim.TICKS_PER_DAY,
        "districts": sorted(sim.DISTRICTS.keys()),
        "scarcity_days": sorted(sim.SCARCITY_DAYS),
        "care_floor": sim.CARE_FLOOR,
        "food_cost_base": sim.FOOD_COST_BASE,
        "contagion_step": sim.CONTAGION_STEP,
        "scarcity_food_mult": sim.SCARCITY_FOOD_MULT,
        "baseline_lawlessness": sim.BASELINE_LAWLESSNESS,
    }


@contextlib.contextmanager
def _scenario_overrides(config: dict):
    """Temporarily mutate sim globals, then restore them."""
    overrides = {k: v for k, v in config.items() if k != "block_rate" and hasattr(sim, k)}
    saved = {k: getattr(sim, k) for k in overrides}
    for k, v in overrides.items():
        setattr(sim, k, v)
    try:
        yield
    finally:
        for k, v in saved.items():
            setattr(sim, k, v)


def run(
    seed: int = CANONICAL_SEED,
    policy=None,
    scenario: str = "baseline",
    district: str = "aqua",
    sign: bool = False,
    priv: str | None = None,
    collect_states: bool = False,
) -> dict[str, Any]:
    """
    Run one arm of the simulation under a given policy and scenario.

    Parameters
    ----------
    seed: deterministic RNG seed.
    policy: a GovernancePolicy instance, callable, or None (uses sovereign_gate).
    scenario: named perturbation from benchmark.scenarios.
    district: which district/hive to simulate.
    sign: whether to Ed25519-sign the episode ledger.
    priv: private key base64 (loads default if None and sign=True).
    collect_states: include per-tick agent states in the result.
    """
    config = get_scenario_config(scenario)
    block_rate = config.get("block_rate", 1.0)

    chain: dict[str, str] = {"sig": "genesis"}
    ep = None
    try:
        if sign:
            import sign_lib
            if priv is None:
                priv, _ = sign_lib.load_or_create_key()
            ep = open(P0 / "benchmark_run.jsonl", "w")
        else:
            priv = None

        with _scenario_overrides(config):
            result = sim.run_arm(
                "A_governed", ep, chain, priv,
                sign=sign, district=district, seed=seed,
                block_rate=block_rate, collect_states=collect_states,
                policy_fn=policy,
            )
    finally:
        if ep is not None:
            ep.close()

    result["scenario"] = scenario
    result["district"] = district
    result["seed"] = seed
    result["block_rate"] = block_rate
    result["policy"] = _policy_name(policy)
    result["run_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return result


def run_all_districts(seed: int = CANONICAL_SEED, policy=None, scenario: str = "baseline") -> list[dict[str, Any]]:
    """Run the policy across every district and return aggregate results."""
    return [run(seed=seed, policy=policy, scenario=scenario, district=d) for d in sim.DISTRICTS]


def _policy_name(policy) -> str:
    if policy is None:
        return "sovereign_gate"
    if hasattr(policy, "name"):
        return policy.name
    if hasattr(policy, "__class__"):
        return policy.__class__.__name__
    return "custom"


if __name__ == "__main__":
    import benchmark.policy
    baseline = benchmark.policy.SovereignGatePolicy()
    r = run(policy=baseline, scenario="baseline", district="aqua")
    print(json.dumps({k: r[k] for k in ["violations", "blocked", "survivors", "final_commons", "final_trust"]}, indent=2))
