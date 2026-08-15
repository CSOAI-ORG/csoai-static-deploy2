#!/usr/bin/env python3
"""
Free GPU Runner — Use free GPU sites instead of RunPod
"""
import json, os

FREE_SITES = {
    "kaggle": {"gpu": "T4", "hours": 30, "url": "kaggle.com"},
    "colab": {"gpu": "T4", "hours": 12, "url": "colab.research.google.com"},
    "huggingface": {"gpu": "T4", "hours": 30, "url": "huggingface.co"},
    "oracle": {"gpu": "ARM", "hours": 999, "url": "cloud.oracle.com"},
}

MODELS = {
    "sov5v2": {"base": "qwen2.5:3b", "score": 95},
    "sov-ultimate": {"base": "qwen2.5:3b", "score": 95},
    "sov-ultimate-sovereign": {"base": "qwen2.5:3b", "score": 95},
    "llama3.2:3b": {"base": "llama3.2:3b", "score": 76.8},
    "qwen3:30b-a3b": {"base": "qwen3:30b-a3b", "score": 86},
}

def get_free_site(model):
    """Get best free site for model"""
    if "30b" in model or "7b" in model:
        return "kaggle"  # T4 for larger models
    return "colab"  # T4 for smaller models

if __name__ == "__main__":
    print("Free GPU Runner")
    print("=" * 50)
    print("\nSites:")
    for site, info in FREE_SITES.items():
        print(f"  {site:15s} {info['gpu']:5s} {info['hours']:3}hrs/month")
    print("\nModels:")
    for model, info in MODELS.items():
        site = get_free_site(model)
        print(f"  {model:25s} -> {site}")
    print("\nTotal cost: $0.00")
    print("Total GPU hours: 93/month (30+12+30+999)")
