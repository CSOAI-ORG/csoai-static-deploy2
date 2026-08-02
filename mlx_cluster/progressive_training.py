#!/usr/bin/env python3
"""progressive_training.py — Phase 4: Progressive model expansion (1B → 3B → 7B → 13B).

Tohoku University paper (2026): Train a 1B model, expand to 2B, expand to 4B,
expand to 8B. 25% less total compute than training each independently.
Plus the models behave more consistently across sizes.

For SOV3 path:
1. Train 1B parameter SOV agent on farm/pond/construction data
2. Expand to 3B (add layers)
3. Expand to 7B (add more layers)
4. Expand to 13B (production SOV model)
5. Total cost: 25% less than training 13B from scratch
6. Each intermediate model is deployable — product at every stage

Usage:
    python3 progressive_training.py --plan --target 13B
    python3 progressive_training.py --estimate --target 13B
"""

import argparse
import json
import math
import sys
from pathlib import Path
from datetime import datetime, timezone

DEPLOY2 = Path("/Users/nicholas/clawd/csoai-static-deploy2")
OUT = DEPLOY2 / "mlx_cluster" / "progressive_plan.json"


# Sizes in billions of parameters (B)
TIERS = [
    {"name": "SOV-1B (Tier-0 spawn)", "params_b": 1.0, "ram_gb": 2.0, "training_hours_m4": 4.0},
    {"name": "SOV-3B (Tier-1 spawn)", "params_b": 3.0, "ram_gb": 4.0, "training_hours_m4": 8.0},
    {"name": "SOV-7B (Tier-2 spawn)", "params_b": 7.0, "ram_gb": 9.0, "training_hours_m4": 16.0},
    {"name": "SOV-13B (Tier-3 spawn)", "params_b": 13.0, "ram_gb": 13.0, "training_hours_m4": 24.0},
    {"name": "SOV-30B+ (Tier-4 sovereign)", "params_b": 30.0, "ram_gb": 26.0, "training_hours_m4": 48.0},
]


def estimate_progressive_training(target_b: float, m4_only: bool = True) -> dict:
    """Estimate progressive training cost vs from-scratch.
    
    The Tohoku paper claims ~25% reduction in total compute when training
    progressively from smaller → larger vs training each independently.
    
    Also: each intermediate model is deployable (a product at every stage).
    """
    # Find the tier
    target = None
    for t in TIERS:
        if t["params_b"] >= target_b:
            target = t
            break
    if target is None:
        target = TIERS[-1]
    
    # Progressive path: cumulative training hours
    progressive_hours = 0.0
    intermediate_models = []
    for t in TIERS:
        if t["params_b"] > target["params_b"]:
            break
        progressive_hours += t["training_hours_m4"]
        intermediate_models.append(t["name"])
    
    # From-scratch: estimated hours proportional to params
    # Rough estimate: 1 hour per billion parameters for 4-bit + LoRA
    from_scratch_hours = target["params_b"] * target["training_hours_m4"] / 1.0
    
    # Apply 25% reduction
    savings = from_scratch_hours * 0.25
    
    return {
        "target_model": target["name"],
        "target_params_b": target["params_b"],
        "ram_required_gb": target["ram_gb"],
        "intermediate_models": intermediate_models,
        "intermediate_count": len(intermediate_models),
        "progressive_training_hours": round(progressive_hours, 1),
        "from_scratch_hours": round(from_scratch_hours, 1),
        "compute_savings_hours": round(savings, 1),
        "compute_savings_percent": "25%",
        "training_platform": "M4 alone" if m4_only else "M2+M4 cluster (MLX distributed)",
        "deployment_strategy": "Each intermediate model is deployable — product at every stage",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--target", type=float, default=13.0, help="Target parameter count (B)")
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--cluster", action="store_true", help="Use M2+M4 cluster instead of M4 alone")
    args = parser.parse_args()
    
    print("=== Progressive Training Plan (Phase 4) ===\n")
    
    est = estimate_progressive_training(args.target, m4_only=not args.cluster)
    
    print(f"Target: {est['target_model']} ({est['target_params_b']}B)")
    print(f"RAM required: {est['ram_required_gb']} GB")
    print(f"Platform: {est['training_platform']}")
    print()
    
    print("Progressive path:")
    for name in est['intermediate_models']:
        print(f"  → {name}")
    print()
    
    print(f"Compute:")
    print(f"  Progressive (1B → ... → {args.target}B): {est['progressive_training_hours']} hours")
    print(f"  From scratch ({args.target}B): {est['from_scratch_hours']} hours")
    print(f"  Savings: {est['compute_savings_hours']} hours ({est['compute_savings_percent']})")
    print()
    
    print(f"Deployment strategy:")
    print(f"  {est['deployment_strategy']}")
    print()
    
    if args.estimate:
        # Cost estimate using free APIs for data generation
        api_costs = {
            "data_generation_usd": 350.0,  # Groq + Kimi K3 + DeepSeek V4
            "training_compute_usd": 0.0,  # local M4 + M2
            "mlx_setup_usd": 0.0,  # free
            "total_usd": 350.0,
        }
        print(f"Estimated cost (local-first):")
        print(f"  Data generation: ${api_costs['data_generation_usd']}")
        print(f"  Training: ${api_costs['training_compute_usd']} (local)")
        print(f"  Setup: ${api_costs['mlx_setup_usd']} (free)")
        print(f"  Total: ${api_costs['total_usd']}")
        print(f"  Equivalent cloud GPU cost (Kaggle T4): ~$150/month if we used cloud instead")
    
    plan = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reference": "Tohoku University 2026 — Progressive training saves 25% compute",
        "tiers": TIERS,
        "estimate": est,
    }
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(plan, indent=2))
    print(f"\n-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())