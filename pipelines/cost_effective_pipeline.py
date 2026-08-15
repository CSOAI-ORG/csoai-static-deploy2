#!/usr/bin/env python3
"""
Cost-Effective Pipeline — Use free GPU sites
"""
import json, os
from pathlib import Path

STACK = {
    "offline": {
        "model": "qwen2.5:0.5b",
        "accuracy": "90%",
        "cost": "$0.00",
        "location": "Mac M4"
    },
    "kaggle": {
        "gpu": "T4",
        "hours": 30,
        "cost": "$0.00",
        "use": "Training"
    },
    "huggingface": {
        "gpu": "T4",
        "hours": 30,
        "cost": "$0.00",
        "use": "Inference"
    },
    "oracle": {
        "gpu": "ARM",
        "hours": 999,
        "cost": "$0.00",
        "use": "Testing"
    }
}

def get_strategy():
    """Get cost-effective strategy"""
    return {
        "inference": "Use offline model (Mac, $0)",
        "training": "Use Kaggle free GPU (30hrs/month)",
        "heavy": "Use RunPod only when needed ($2.89/hr)",
        "testing": "Use Oracle ARM (always free)"
    }

if __name__ == "__main__":
    print("Cost-Effective Stack")
    print("=" * 50)
    
    print("\nStack Components:")
    for name, info in STACK.items():
        print(f"  {name}:")
        for k, v in info.items():
            print(f"    {k}: {v}")
    
    print("\nStrategy:")
    strategy = get_strategy()
    for k, v in strategy.items():
        print(f"  {k}: {v}")
    
    print("\nCost Savings:")
    print("  Current: $69/day (RunPod A40)")
    print("  Optimized: $0/day (free GPU sites)")
    print("  Savings: $69/day = $2,070/month")
