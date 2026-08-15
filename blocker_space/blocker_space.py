#!/usr/bin/env python3
"""BLOCKER SPACE — The Data Feed Layer for SOV Clan Evolution

All data feeds SOV needs to evolve clans:
  Kaggle      — GPU training, competitions, datasets
  HuggingFace — Models, datasets, leaderboards
  Oracle      — Always-free CPU/storage
  Ollama      — Local inference
  APIs        — Qwen, Gemini, DeepSeek, Groq
  GitHub      — Code, CI/CD
  Cloudflare  — Deployment, CDN

Each feed is a NODE inside BLOCKER SPACE.
SOV auto-routes across all nodes — never goes down.
All nodes train GNN/NN — win-win pipeline.
"""

import json
import hashlib
import time
import urllib.request
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent


# ─── BLOCKER SPACE NODES ────────────────────────────────────────────────────

NODES = {
    "kaggle": {
        "id": "kaggle",
        "type": "gpu",
        "provider": "Kaggle",
        "status": "active",
        "cost": "$0",
        "capabilities": ["training", "competitions", "datasets", "leaderboard"],
        "endpoint": "kaggle CLI",
        "env_var": "KAGGLE_API_TOKEN",
        "check": lambda: _check_kaggle(),
    },
    "huggingface": {
        "id": "huggingface",
        "type": "model_hub",
        "provider": "HuggingFace",
        "status": "active",
        "cost": "$0",
        "capabilities": ["models", "datasets", "leaderboard", "spaces"],
        "endpoint": "HF API",
        "env_var": "HUGGINGFACE_TOKEN",
        "check": lambda: _check_hf(),
    },
    "oracle": {
        "id": "oracle",
        "type": "cpu",
        "provider": "Oracle Cloud",
        "status": "active",
        "cost": "$0",
        "capabilities": ["inference", "training", "storage", "always-on"],
        "endpoint": "SSH oracle-micro",
        "check": lambda: _check_oracle(),
    },
    "ollama_local": {
        "id": "ollama_local",
        "type": "inference",
        "provider": "Local",
        "status": "active",
        "cost": "$0",
        "capabilities": ["inference", "local_models"],
        "endpoint": "localhost:11434",
        "check": lambda: _check_ollama(),
    },
    "qwen_api": {
        "id": "qwen_api",
        "type": "api",
        "provider": "Alibaba Cloud",
        "status": "active",
        "cost": "$0",
        "capabilities": ["inference", "reasoning", "code", "vision"],
        "endpoint": "Alibaba MAAS",
        "env_var": "QWEN_API_KEY",
        "check": lambda: _check_qwen(),
    },
    "gemini_api": {
        "id": "gemini_api",
        "type": "api",
        "provider": "Google",
        "status": "active",
        "cost": "$0",
        "capabilities": ["inference", "reasoning", "vision"],
        "endpoint": "Google AI",
        "env_var": "GEMINI_API_KEY",
        "check": lambda: _check_gemini(),
    },
    "deepseek_api": {
        "id": "deepseek_api",
        "type": "api",
        "provider": "DeepSeek",
        "status": "needs_billing",
        "cost": "$0.14/M tokens",
        "capabilities": ["inference", "reasoning", "code"],
        "endpoint": "DeepSeek API",
        "env_var": "DEEPSEEK_API_KEY",
        "check": lambda: _check_deepseek(),
    },
    "github": {
        "id": "github",
        "type": "code",
        "provider": "GitHub",
        "status": "active",
        "cost": "$0",
        "capabilities": ["code", "ci_cd", "storage"],
        "endpoint": "github.com/CSOAI-ORG/csoai-static-deploy2",
        "check": lambda: _check_github(),
    },
    "cloudflare": {
        "id": "cloudflare",
        "type": "deployment",
        "provider": "Cloudflare",
        "status": "active",
        "cost": "$0",
        "capabilities": ["deployment", "cdn", "functions"],
        "endpoint": "csoai-sovereign.pages.dev",
        "check": lambda: _check_cloudflare(),
    },
}


# ─── NODE CHECKS ────────────────────────────────────────────────────────────

def _check_kaggle() -> Dict:
    """Check Kaggle status."""
    try:
        result = subprocess.run(
            ["kaggle", "kernels", "list", "--mine", "--sort-by", "dateCreated"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            return {"ok": True, "kernels": len(lines) - 2, "status": "active"}
        return {"ok": False, "error": result.stderr[:100]}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def _check_hf() -> Dict:
    """Check HuggingFace status."""
    token = os.environ.get("HUGGINGFACE_TOKEN", "")
    if not token:
        return {"ok": False, "error": "No token"}
    try:
        req = urllib.request.Request(
            "https://huggingface.co/api/whoami-v2",
            headers={"Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
            return {"ok": True, "user": data.get("name", "?"), "status": "active"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def _check_oracle() -> Dict:
    """Check Oracle Cloud status."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
             "oracle-micro", "echo ok"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return {"ok": True, "status": "active"}
        return {"ok": False, "error": "Connection failed"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def _check_ollama() -> Dict:
    """Check local Ollama status."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
            models = data.get("models", [])
            return {"ok": True, "models": len(models), "status": "active"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def _check_qwen() -> Dict:
    """Check Qwen API status."""
    key = os.environ.get("QWEN_API_KEY", "")
    base = os.environ.get("QWEN_API_BASE", "")
    if not key or not base:
        return {"ok": False, "error": "No key"}
    try:
        payload = json.dumps({"model": "qwen-max", "messages": [{"role": "user", "content": "hi"}],
                             "max_tokens": 5, "temperature": 0}).encode()
        req = urllib.request.Request(base, data=payload,
                                    headers={"Content-Type": "application/json",
                                            "Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return {"ok": True, "models": 151, "status": "active"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def _check_gemini() -> Dict:
    """Check Gemini API status."""
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return {"ok": False, "error": "No key"}
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return {"ok": True, "models": len(data.get("models", [])), "status": "active"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def _check_deepseek() -> Dict:
    """Check DeepSeek API status."""
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        return {"ok": False, "error": "No key"}
    try:
        payload = json.dumps({"model": "deepseek-chat", "messages": [{"role": "user", "content": "hi"}],
                             "max_tokens": 5}).encode()
        req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",
                                    data=payload,
                                    headers={"Content-Type": "application/json",
                                            "Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return {"ok": True, "status": "active"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def _check_github() -> Dict:
    """Check GitHub status."""
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True, text=True, timeout=5, cwd=str(ROOT)
        )
        if "origin" in result.stdout:
            return {"ok": True, "remote": result.stdout.strip().split("\n")[0], "status": "active"}
        return {"ok": False, "error": "No remote"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def _check_cloudflare() -> Dict:
    """Check Cloudflare status."""
    try:
        req = urllib.request.Request("https://csoai-sovereign.pages.dev", method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as r:
            return {"ok": True, "status": "active"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


# ─── BLOCKER SPACE ──────────────────────────────────────────────────────────

class BlockerSpace:
    """The data feed layer for SOV clan evolution."""

    def __init__(self):
        self.nodes = NODES
        self.status = {}
        self.data_feeds = {}

    def check_all(self) -> Dict:
        """Check status of all nodes."""
        results = {}
        for node_id, node in self.nodes.items():
            check_fn = node.get("check")
            if check_fn:
                try:
                    result = check_fn()
                    results[node_id] = result
                except Exception as e:
                    results[node_id] = {"ok": False, "error": str(e)[:100]}
            else:
                results[node_id] = {"ok": False, "error": "No check function"}

        self.status = results
        return results

    def get_active_nodes(self) -> List[str]:
        """Get all active nodes."""
        return [node_id for node_id, status in self.status.items() if status.get("ok")]

    def get_best_node(self, capability: str) -> str:
        """Get the best node for a given capability."""
        candidates = []
        for node_id, node in self.nodes.items():
            if capability in node.get("capabilities", []):
                status = self.status.get(node_id, {})
                if status.get("ok"):
                    candidates.append(node_id)

        if not candidates:
            return None

        # Prefer free resources
        free = [n for n in candidates if self.nodes[n].get("cost", "").startswith("$0")]
        return free[0] if free else candidates[0]

    def route_task(self, task: str) -> Dict:
        """Route a task to the best available node."""
        # Determine capability needed
        task_lower = task.lower()
        if "train" in task_lower or "finetune" in task_lower:
            capability = "training"
        elif "infer" in task_lower or "generate" in task_lower:
            capability = "inference"
        elif "deploy" in task_lower:
            capability = "deployment"
        elif "benchmark" in task_lower:
            capability = "competitions"
        else:
            capability = "inference"

        best_node = self.get_best_node(capability)
        if not best_node:
            return {"error": f"No node available for {capability}"}

        return {
            "task": task,
            "node": best_node,
            "provider": self.nodes[best_node]["provider"],
            "capability": capability,
            "cost": self.nodes[best_node]["cost"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def get_state(self) -> Dict:
        """Get full BLOCKER SPACE state."""
        active = self.get_active_nodes()
        return {
            "total_nodes": len(self.nodes),
            "active_nodes": len(active),
            "active_list": active,
            "status": {k: v.get("ok", False) for k, v in self.status.items()},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  BLOCKER SPACE — Data Feed Layer for SOV                ║")
    print("║  All Nodes · Auto-Route · Never Down                    ║")
    print("╚══════════════════════════════════════════════════════════╝")

    blocker = BlockerSpace()

    # Check all nodes
    print(f"\n─── CHECKING ALL NODES ───")
    results = blocker.check_all()
    for node_id, result in results.items():
        status = "✓" if result.get("ok") else "✗"
        node = NODES[node_id]
        print(f"  {status} {node_id:20s} {node['provider']:15s} {node['type']:12s} {node['cost']}")

    # Show active nodes
    active = blocker.get_active_nodes()
    print(f"\n─── ACTIVE NODES ({len(active)}/{len(NODES)}) ───")
    for node_id in active:
        node = NODES[node_id]
        print(f"  {node_id:20s} {node['provider']:15s} {node['capabilities']}")

    # Route example tasks
    print(f"\n─── TASK ROUTING ───")
    tasks = [
        "Train visual reasoning model",
        "Generate sovereign knowledge",
        "Deploy to production",
        "Run benchmark competition",
    ]
    for task in tasks:
        result = blocker.route_task(task)
        print(f"  {task:35s} → {result.get('node', '?'):20s} ({result.get('provider', '?')})")

    # Show state
    state = blocker.get_state()
    print(f"\n─── BLOCKER SPACE STATE ───")
    print(f"  Total nodes: {state['total_nodes']}")
    print(f"  Active: {state['active_nodes']}")
    print(f"  Status: {state['status']}")

    # Save
    output = {
        "state": state,
        "nodes": {k: {"provider": v["provider"], "type": v["type"], "cost": v["cost"],
                      "capabilities": v["capabilities"]}
                  for k, v in NODES.items()},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out_path = ROOT / "blocker_space" / "blocker_state.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
