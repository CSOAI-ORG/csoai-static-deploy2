"""
Free-GPU Swarm Orchestrator
Routes SOV work across free/cheap GPU tiers.
Tracks costs, savings, and work completion.

Usage:
  python3 free_gpu/orchestrator.py status
  python3 free_gpu/orchestrator.py deploy kaggle-capability
  python3 free_gpu/orchestrator.py deploy kaggle-govbench
  python3 free_gpu/orchestrator.py deploy oracle-synth
  python3 free_gpu/orchestrator.py deploy runpod-master
  python3 free_gpu/orchestrator.py costs
"""
import json
import hashlib
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FREE_GPU_DIR = ROOT / "free_gpu"
BENCH_DIR = ROOT / "benchmark-results"
STATE_FILE = FREE_GPU_DIR / "swarm_state.json"

TIERS = {
    "local_m4": {"cost_hr": 0.0, "gpu": "Apple M4", "vram_gb": 0, "status": "available", "tab": "tab1_m4_local.py"},
    "m2_lan": {"cost_hr": 0.0, "gpu": "Apple M2", "vram_gb": 0, "status": "available", "tab": "tab2_m2_lan.py"},
    "modal_t4_1": {"cost_hr": 0.0, "gpu": "Modal T4 #1", "vram_gb": 16, "status": "spend_limit_exceeded", "tab": "tab3_modal_t4_1.py"},
    "modal_t4_2": {"cost_hr": 0.0, "gpu": "Modal T4 #2", "vram_gb": 16, "status": "spend_limit_exceeded", "tab": "tab4_modal_t4_2.py"},
    "kaggle_t4_a": {"cost_hr": 0.0, "gpu": "Kaggle T4 #1", "vram_gb": 16, "status": "available", "limit": "30h/week", "tab": "tab5_kaggle_t4_a.py"},
    "kaggle_t4_b": {"cost_hr": 0.0, "gpu": "Kaggle T4 #2", "vram_gb": 16, "status": "available", "limit": "30h/week", "tab": "tab6_kaggle_t4_b.py"},
    "colab_t4": {"cost_hr": 0.0, "gpu": "Colab T4", "vram_gb": 16, "status": "available", "limit": "12h/day", "tab": "tab7_colab_t4.py"},
    "oracle_arm_1": {"cost_hr": 0.0, "gpu": "Oracle ARM #1", "vram_gb": 0, "status": "available", "tab": "tab8_oracle_arm_1.py"},
    "oracle_arm_2": {"cost_hr": 0.0, "gpu": "Oracle ARM #2", "vram_gb": 0, "status": "available", "tab": "tab9_oracle_arm_2.py"},
    "runpod_3090": {"cost_hr": 0.22, "gpu": "RTX 3090", "vram_gb": 24, "status": "available"},
    "runpod_a40": {"cost_hr": 0.44, "gpu": "A40", "vram_gb": 48, "status": "available"},
    "runpod_h100": {"cost_hr": 3.50, "gpu": "H100", "vram_gb": 80, "status": "available"},
}

WORKLOADS = {
    "tab1-m4-local": {"tier": "local_m4", "duration_h": 0.5, "description": "Local M4 — E2E + inference"},
    "tab2-m2-lan": {"tier": "m2_lan", "duration_h": 0.5, "description": "LAN M2 — distributed eval"},
    "tab3-modal-t4-1": {"tier": "modal_t4_1", "duration_h": 1.0, "description": "Modal T4 #1 — small training"},
    "tab4-modal-t4-2": {"tier": "modal_t4_2", "duration_h": 1.0, "description": "Modal T4 #2 — eval"},
    "tab5-kaggle-t4-a": {"tier": "kaggle_t4_a", "duration_h": 0.5, "description": "Kaggle T4 #1 — capability matrix"},
    "tab6-kaggle-t4-b": {"tier": "kaggle_t4_b", "duration_h": 2.0, "description": "Kaggle T4 #2 — GovBench V6"},
    "tab7-colab-t4": {"tier": "colab_t4", "duration_h": 1.0, "description": "Colab T4 — notebook runs"},
    "tab8-oracle-arm-1": {"tier": "oracle_arm_1", "duration_h": 4.0, "description": "Oracle ARM #1 — data synthesis"},
    "tab9-oracle-arm-2": {"tier": "oracle_arm_2", "duration_h": 4.0, "description": "Oracle ARM #2 — corpus building"},
    "runpod-master": {"tier": "runpod_h100", "duration_h": 2.0, "description": "55-model master stage on H100"},
    "runpod-grpo": {"tier": "runpod_a40", "duration_h": 4.0, "description": "GRPO training on A40"},
    "distributed-evolve": {"tier": "local_m4", "duration_h": 0.5, "description": "Distributed evolution across all free tiers"},
}


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"runs": [], "total_cost": 0.0, "total_savings": 0.0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def estimate_cost(workload):
    wl = WORKLOADS.get(workload)
    if not wl:
        return 0.0
    tier = TIERS.get(wl["tier"], {})
    return tier.get("cost_hr", 0.0) * wl["duration_h"]


def estimate_savings(workload):
    wl = WORKLOADS.get(workload)
    if not wl:
        return 0.0
    h100_cost = TIERS["runpod_h100"]["cost_hr"] * wl["duration_h"]
    actual_cost = estimate_cost(workload)
    return h100_cost - actual_cost


def status():
    state = load_state()
    print("=== FREE-GPU SWARM STATUS ===\n")
    print("Tiers:")
    for name, tier in TIERS.items():
        status_icon = "✓" if tier["status"] == "available" else "✗"
        print(f"  {status_icon} {name:20s} {tier['gpu']:25s} ${tier['cost_hr']}/hr  {tier.get('limit','')}")
    print(f"\nWorkloads completed: {len(state.get('runs', []))}")
    print(f"Total cost: ${state.get('total_cost', 0.0):.2f}")
    print(f"Total savings vs H100: ${state.get('total_savings', 0.0):.2f}")
    return state


def deploy(workload):
    state = load_state()
    wl = WORKLOADS.get(workload)
    if not wl:
        print(f"Unknown workload: {workload}")
        return
    cost = estimate_cost(workload)
    savings = estimate_savings(workload)
    print(f"Deploying {workload} to {wl['tier']}...")
    print(f"  Estimated cost: ${cost:.2f}")
    print(f"  Savings vs H100: ${savings:.2f}")
    
    if workload == "distributed-evolve":
        dist_script = FREE_GPU_DIR / "distributed_evolution.py"
        if dist_script.exists():
            print(f"  Running distributed evolution across all free tiers...")
            result = subprocess.run(
                ["python3", str(dist_script), "run"],
                capture_output=True, text=True, timeout=7200
            )
            out = result.stdout + result.stderr
            print(f"  Script output:\n{out[:2000]}")
            # Sync and merge after run
            subprocess.run(
                ["python3", str(dist_script), "sync"],
                capture_output=True, text=True, timeout=60
            )
            subprocess.run(
                ["python3", str(dist_script), "merge"],
                capture_output=True, text=True, timeout=120
            )
        else:
            print(f"  Distributed evolution script not found: {dist_script}")
    else:
        tier_info = TIERS.get(wl["tier"], {})
        tab_script = tier_info.get("tab")
        if tab_script:
            tab_path = FREE_GPU_DIR / tab_script
            if tab_path.exists():
                print(f"  Running {tab_script}...")
                result = subprocess.run(
                    ["python3", str(tab_path)],
                    capture_output=True, text=True, timeout=3600
                )
                ok = result.returncode == 0
                out = result.stdout + result.stderr
                print(f"  Script output:\n{out[:1000]}")
            else:
                print(f"  Tab script not found: {tab_path}")
    
    entry = {
        "workload": workload,
        "tier": wl["tier"],
        "started": datetime.now(timezone.utc).isoformat(),
        "cost": cost,
        "savings": savings,
    }
    state.setdefault("runs", []).append(entry)
    state["total_cost"] = state.get("total_cost", 0.0) + cost
    state["total_savings"] = state.get("total_savings", 0.0) + savings
    save_state(state)
    print(f"  State saved to {STATE_FILE}")
    return entry


def costs():
    state = load_state()
    print("=== COST REPORT ===\n")
    print(f"Total runs: {len(state.get('runs', []))}")
    print(f"Total cost: ${state.get('total_cost', 0.0):.2f}")
    print(f"Total savings: ${state.get('total_savings', 0.0):.2f}")
    by_tier = {}
    for run in state.get("runs", []):
        tier = run.get("tier", "unknown")
        by_tier.setdefault(tier, {"cost": 0.0, "savings": 0.0, "runs": 0})
        by_tier[tier]["cost"] += run.get("cost", 0.0)
        by_tier[tier]["savings"] += run.get("savings", 0.0)
        by_tier[tier]["runs"] += 1
    print("\nBy tier:")
    for tier, data in by_tier.items():
        print(f"  {tier:20s} {data['runs']} runs  ${data['cost']:.2f} cost  ${data['savings']:.2f} savings")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "status":
        status()
    elif args[0] == "deploy" and len(args) > 1:
        deploy(args[1])
    elif args[0] == "costs":
        costs()
    else:
        print("Usage: orchestrator.py [status|deploy <workload>|costs]")
