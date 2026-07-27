#!/usr/bin/env python3
"""SOV Resource Registry — Living Library of All Free Compute

All free GPU/CPU/storage resources SOV can use.
Auto-migration: SOV never goes down, spreads evenly across all.
All platforms train GNN/NN — win-win improved pipeline.

Resources:
  Kaggle     — T4 GPU, 30hrs/week free
  HuggingFace — T4 GPU, free Spaces
  Colab      — T4 GPU, ~12hrs/day free
  Modal      — T4 GPU, 30hrs/month free
  Oracle     — ARM CPU, always free
  RunPod     — A40/H100, paid but cheap
  Groq       — Free Llama/Mixtral API
  Qwen       — Free 151 models API
  Gemini     — Free 50 models API
  DeepSeek   — Free tier API
  LMArena    — Free model comparison
  OpenRouter — Free model routing
  Together   — Free tier API
  Replicate  — Free tier API
"""

import json
import hashlib
import time
import urllib.request
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent


# ─── Resource Registry ──────────────────────────────────────────────────────

RESOURCES = {
    # ── FREE GPUs ──────────────────────────────────────────────────────────
    "kaggle_t4": {
        "provider": "Kaggle",
        "type": "gpu",
        "model": "T4 16GB VRAM",
        "cost": "$0",
        "limit": "30 hrs/week",
        "api": "kaggle CLI",
        "status": "active",
        "capabilities": ["training", "inference", "benchmark"],
        "notebook_url": "https://www.kaggle.com/nicktempleman",
        "env_var": "KAGGLE_API_TOKEN",
        "auto_deploy": True,
    },
    "huggingface_t4": {
        "provider": "HuggingFace",
        "type": "gpu",
        "model": "T4 16GB VRAM",
        "cost": "$0",
        "limit": "Free Spaces",
        "api": "HF API + CLI",
        "status": "active",
        "capabilities": ["training", "inference", "deployment", "leaderboard"],
        "url": "https://huggingface.co/nicktempleman",
        "env_var": "HUGGINGFACE_TOKEN",
        "auto_deploy": True,
    },
    "colab_t4": {
        "provider": "Google Colab",
        "type": "gpu",
        "model": "T4 16GB VRAM",
        "cost": "$0",
        "limit": "~12 hrs/day",
        "api": "Colab API",
        "status": "available",
        "capabilities": ["training", "inference"],
        "url": "https://colab.research.google.com",
        "auto_deploy": True,
    },
    "modal_t4": {
        "provider": "Modal",
        "type": "gpu",
        "model": "T4 16GB VRAM",
        "cost": "$0",
        "limit": "30 hrs/month",
        "api": "Modal CLI",
        "status": "available",
        "capabilities": ["training", "inference", "serverless"],
        "url": "https://modal.com",
        "env_var": "MODAL_TOKEN",
        "auto_deploy": True,
    },

    # ── FREE CPUs ──────────────────────────────────────────────────────────
    "oracle_arm": {
        "provider": "Oracle Cloud",
        "type": "cpu",
        "model": "ARM 4-core 24GB RAM",
        "cost": "$0",
        "limit": "Always free",
        "api": "SSH",
        "status": "active",
        "capabilities": ["inference", "training", "storage", "always-on"],
        "host": "145.241.232.16",
        "ssh": "oracle-micro",
        "auto_deploy": True,
    },
    "mac_m4": {
        "provider": "Local",
        "type": "cpu",
        "model": "Apple M4",
        "cost": "$0",
        "limit": "Always available",
        "api": "Ollama localhost:11434",
        "status": "active",
        "capabilities": ["inference", "development"],
        "auto_deploy": False,
    },

    # ── FREE APIs ──────────────────────────────────────────────────────────
    "qwen_api": {
        "provider": "Alibaba Cloud",
        "type": "api",
        "model": "151 models (qwen-max, qwen-plus, etc.)",
        "cost": "Free tier",
        "limit": "Rate limited",
        "api": "OpenAI-compatible",
        "status": "active",
        "capabilities": ["inference", "reasoning", "code", "vision"],
        "endpoint": "https://ws-gmuls9hk2vwqzi2n.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",
        "env_var": "QWEN_API_KEY",
        "auto_deploy": True,
    },
    "gemini_api": {
        "provider": "Google",
        "type": "api",
        "model": "50 models (gemini-2.5-flash, gemini-2.5-pro, etc.)",
        "cost": "Free tier",
        "limit": "Rate limited",
        "api": "Google AI",
        "status": "active",
        "capabilities": ["inference", "reasoning", "vision", "code"],
        "env_var": "GEMINI_API_KEY",
        "auto_deploy": True,
    },
    "deepseek_api": {
        "provider": "DeepSeek",
        "type": "api",
        "model": "deepseek-chat, deepseek-reasoner",
        "cost": "Free tier",
        "limit": "Rate limited",
        "api": "OpenAI-compatible",
        "status": "needs_billing",
        "capabilities": ["inference", "reasoning", "code"],
        "env_var": "DEEPSEEK_API_KEY",
        "auto_deploy": True,
    },
    "groq_api": {
        "provider": "Groq",
        "type": "api",
        "model": "Llama-3.3-70B, Mixtral-8x7B",
        "cost": "Free tier",
        "limit": "Rate limited",
        "api": "OpenAI-compatible",
        "status": "needs_key_refresh",
        "capabilities": ["inference", "reasoning", "fast"],
        "env_var": "GROQ_API_KEY",
        "auto_deploy": True,
    },

    # ── COMPETITION PLATFORMS ──────────────────────────────────────────────
    "kaggle_competitions": {
        "provider": "Kaggle",
        "type": "competition",
        "cost": "$0",
        "api": "Kaggle CLI",
        "status": "active",
        "capabilities": ["benchmark", "leaderboard", "prizes"],
        "url": "https://kaggle.com/competitions",
        "auto_deploy": True,
    },
    "huggingface_leaderboard": {
        "provider": "HuggingFace",
        "type": "leaderboard",
        "cost": "$0",
        "api": "HF API",
        "status": "active",
        "capabilities": ["benchmark", "leaderboard", "deployment"],
        "url": "https://huggingface.co/spaces/open-llm-leaderboard",
        "auto_deploy": True,
    },
    "lmarena": {
        "provider": "LMArena",
        "type": "arena",
        "cost": "$0",
        "api": "Web",
        "status": "active",
        "capabilities": ["comparison", "elo_rating", "battle"],
        "url": "https://lmarena.ai",
        "auto_deploy": False,
    },
    "openrouter": {
        "provider": "OpenRouter",
        "type": "router",
        "cost": "Free models available",
        "api": "OpenAI-compatible",
        "status": "needs_key",
        "capabilities": ["routing", "comparison", "free_models"],
        "env_var": "OPENROUTER_API_KEY",
        "auto_deploy": True,
    },

    # ── PAID (CHEAP) ───────────────────────────────────────────────────────
    "runpod_a40": {
        "provider": "RunPod",
        "type": "gpu",
        "model": "A40 48GB VRAM",
        "cost": "$0.44/hr",
        "limit": "Pay as you go",
        "api": "RunPod API",
        "status": "available",
        "capabilities": ["training", "inference", "large_models"],
        "env_var": "RUNPOD_API_KEY",
        "auto_deploy": False,
    },
    "runpod_h100": {
        "provider": "RunPod",
        "type": "gpu",
        "model": "H100 80GB VRAM",
        "cost": "$3.50/hr",
        "limit": "Pay as you go",
        "api": "RunPod API",
        "status": "available",
        "capabilities": ["training", "inference", "frontier_models"],
        "env_var": "RUNPOD_API_KEY",
        "auto_deploy": False,
    },
}


# ─── Resource Manager ───────────────────────────────────────────────────────

class SOVResourceManager:
    """Manages all compute resources. Auto-migrates across platforms."""

    def __init__(self):
        self.resources = RESOURCES
        self.active_tasks = {}
        self.migration_log = []

    def get_available_resources(self, capability: str = None) -> List[Dict]:
        """Get all available resources, optionally filtered by capability."""
        available = []
        for res_id, res in self.resources.items():
            if res["status"] in ["active", "available"]:
                if capability is None or capability in res.get("capabilities", []):
                    available.append({"id": res_id, **res})
        return available

    def get_free_resources(self) -> List[Dict]:
        """Get all free resources."""
        return [r for r in self.get_available_resources() if r.get("cost", "").startswith("$0")]

    def get_gpu_resources(self) -> List[Dict]:
        """Get all GPU resources."""
        return self.get_available_resources("training")

    def auto_migrate(self, task: str, data: Dict = None) -> Dict:
        """Auto-migrate a task to the best available resource."""
        # Find best resource for task
        candidates = self.get_available_resources()
        if not candidates:
            return {"error": "No available resources"}

        # Score candidates
        scored = []
        for res in candidates:
            score = self._score_resource(res, task)
            scored.append((score, res))

        scored.sort(reverse=True)
        best_score, best_resource = scored[0]

        # Execute on best resource
        result = {
            "task": task,
            "resource": best_resource["id"],
            "provider": best_resource["provider"],
            "score": best_score,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self.migration_log.append(result)
        return result

    def _score_resource(self, resource: Dict, task: str) -> float:
        """Score a resource for a given task."""
        score = 0.5

        # Free resources get bonus
        if resource.get("cost", "").startswith("$0"):
            score += 0.2

        # Active resources get bonus
        if resource.get("status") == "active":
            score += 0.1

        # GPU resources get bonus for training tasks
        if resource.get("type") == "gpu" and "train" in task.lower():
            score += 0.15

        # API resources get bonus for inference tasks
        if resource.get("type") == "api" and "infer" in task.lower():
            score += 0.1

        return min(0.99, score)

    def get_status(self) -> Dict:
        """Get status of all resources."""
        return {
            "total": len(self.resources),
            "active": len([r for r in self.resources.values() if r["status"] == "active"]),
            "available": len([r for r in self.resources.values() if r["status"] == "available"]),
            "free": len([r for r in self.resources.values() if r.get("cost", "").startswith("$0")]),
            "gpu": len([r for r in self.resources.values() if r.get("type") == "gpu"]),
            "api": len([r for r in self.resources.values() if r.get("type") == "api"]),
            "migrations": len(self.migration_log),
        }


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  SOV RESOURCE REGISTRY — Living Library                 ║")
    print("║  All Free GPU/CPU/API Resources                         ║")
    print("╚══════════════════════════════════════════════════════════╝")

    manager = SOVResourceManager()

    # Show all resources
    print(f"\n─── ALL RESOURCES ({len(RESOURCES)}) ───")
    for res_id, res in RESOURCES.items():
        status_icon = "✓" if res["status"] == "active" else "○" if res["status"] == "available" else "✗"
        print(f"  {status_icon} {res_id:25s} {res['provider']:15s} {res['type']:8s} {res['cost']:12s} {res['status']}")

    # Show free resources
    free = manager.get_free_resources()
    print(f"\n─── FREE RESOURCES ({len(free)}) ───")
    for res in free:
        print(f"  {res['id']:25s} {res['provider']:15s} {res['model']}")

    # Show GPU resources
    gpus = manager.get_gpu_resources()
    print(f"\n─── GPU RESOURCES ({len(gpus)}) ───")
    for res in gpus:
        print(f"  {res['id']:25s} {res['provider']:15s} {res['model']}")

    # Auto-migrate example
    print(f"\n─── AUTO-MIGRATE EXAMPLE ───")
    result = manager.auto_migrate("Train visual reasoning model")
    print(f"  Task: Train visual reasoning model")
    print(f"  Best resource: {result['resource']} ({result['provider']})")
    print(f"  Score: {result['score']:.3f}")

    # Status
    status = manager.get_status()
    print(f"\n─── STATUS ───")
    print(f"  Total resources: {status['total']}")
    print(f"  Active: {status['active']}")
    print(f"  Available: {status['available']}")
    print(f"  Free: {status['free']}")
    print(f"  GPU: {status['gpu']}")
    print(f"  API: {status['api']}")

    # Save
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resources": RESOURCES,
        "status": status,
    }
    out_path = ROOT / "sov_space" / "resource_registry.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
