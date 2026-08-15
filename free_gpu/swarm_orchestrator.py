"""
Free-GPU Swarm Orchestrator
Routes SOV work across free GPU tiers to minimize costs.

Tier 0 (always free):
  - Oracle ARM: 4 OCPUs + 24GB RAM — data synthesis, corpus building
  - Local Mac M4: CPU inference, code editing, E2E checks

Tier 1 (free GPU, ~30h/month):
  - Modal Labs T4 (16GB): small model training (0.5B/1.3B), eval
  - Kaggle T4 (16GB): benchmark runs, capability matrix eval

Tier 2 (paid GPU, use sparingly):
  - RunPod RTX 3090 (24GB): $0.22/hr — medium model training
  - RunPod A40 (48GB): $0.44/hr — large model training
  - RunPod H100 (80GB): $3.50/hr — 32B+ model inference

Strategy:
  - Run everything possible on Tier 0/1 first
  - Only escalate to Tier 2 when free tiers can't handle the workload
  - Use H100 for the 55-model master stage only (1-2 hours max)
  - All persistent data on RunPod network volume (sov-artifacts, 200GB)
"""
import json
import hashlib
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TIER_COSTS = {
    "oracle_arm": 0.0,
    "local_m4": 0.0,
    "modal_t4": 0.0,
    "kaggle_t4": 0.0,
    "runpod_3090": 0.22,
    "runpod_a40": 0.44,
    "runpod_h100": 3.50,
}

WORKLOAD_TIERS = {
    "data_synthesis": "oracle_arm",
    "corpus_building": "oracle_arm",
    "e2e_checks": "local_m4",
    "code_editing": "local_m4",
    "small_model_eval": "modal_t4",
    "small_model_training": "modal_t4",
    "benchmark_runs": "kaggle_t4",
    "capability_matrix": "kaggle_t4",
    "medium_model_training": "runpod_3090",
    "large_model_training": "runpod_a40",
    "master_stage_55_models": "runpod_h100",
    "govbench_full": "runpod_a40",
}


def estimate_cost(tier, hours):
    return TIER_COSTS.get(tier, 0.0) * hours


def choose_tier(workload, budget_per_hour=0.0):
    tier = WORKLOAD_TIERS.get(workload, "local_m4")
    if estimate_cost(tier, 1) > budget_per_hour:
        for alt_tier, cost in sorted(TIER_COSTS.items(), key=lambda x: x[1]):
            if cost <= budget_per_hour:
                return alt_tier
    return tier


def generate_plan(workloads, budget_per_hour=0.0):
    plan = []
    total_cost = 0.0
    for workload in workloads:
        tier = choose_tier(workload, budget_per_hour)
        cost_per_hr = estimate_cost(tier, 1)
        plan.append({"workload": workload, "tier": tier, "cost_per_hr": cost_per_hr})
        total_cost += cost_per_hr
    return {"plan": plan, "total_cost_per_hr": total_cost, "generated": datetime.now(timezone.utc).isoformat()}


def write_plan(path, plan):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, indent=2) + "\n")
    return path
