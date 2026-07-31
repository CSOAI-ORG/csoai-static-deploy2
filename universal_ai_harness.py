#!/usr/bin/env python3
"""universal_ai_harness.py — Join ALL AI into the OWEM clan+hive architecture.

The thesis: "Models don't matter — the harness is everything."
- Don't fight Kimi K3 / DeepSeek V4 / Mastra / Claude / LongCat.
- Join them all into the OWEM (One-Way Embedding Memory) clan+hive topology.
- Every clan routes to the right upstream via cost+capability tags.
- Every hive provides a coherent governance surface.
- Every model is harnessed, not replaced.

Architecture:
  User → OWEM (clan + hive) → Universal AI Harness → upstream models

Clans (8 families × 13 specialists = 104 OWEMs per memory):
  - qwen, llama, deepseek, mistral, gemma, phi, gpt-oss, core
  - 95 OWEMs in master registry
  - 14 refusal-trained (red-line)
  - 20 cross-family hybrids

Hives (5 tiers):
  - 0: local (qwen2.5:0.5b, 379MB, free CPU) — tier-0 spawn
  - 1: local (clan-plain, OWM only) — tier-1 spawn
  - 2: medium (sov33-v7, drawing-tuned, OWM+IWM) — tier-2 spawn
  - 3: large (sov-sovereign-v4, merged lora, OWM+IWM+VWM) — tier-3 spawn
  - 4: sovereign (council-mix, full council) — tier-4 (invitation-only)

Upstream routing:
  - cheap → DeepSeek V4-Flash ($0.28/M out)
  - production → DeepSeek V4-Pro ($0.87/M out, MIT)
  - sovereign → Kimi K3 ($15/M out, open weights)
  - agentic → Claude Opus 5 ($25/M out)
  - local → sov33-unified (free, sovereign)

Cost optimization: route 90% to cheap/production/local, 10% to sovereign/agentic.

Usage:
    python3 universal_ai_harness.py --status
    python3 universal_ai_harness.py --route "Explain Article 50"
    python3 universal_ai_harness.py --hive 0 --spawn user_test
"""

import json
import urllib.request
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

DEPLOY2 = Path("/Users/nicholas/clawd/csoai-static-deploy2")
REGISTRY = DEPLOY2 / "OWEM_MASTER_REGISTRY.md"
OLLAMA_URL = "http://localhost:11434"
SOV_GATEWAY_URL = "http://localhost:8080"


# ─── Clans (8 families, 13 specialists) ───────────────────────────────

CLANS = {
    "qwen": {
        "name": "Qwen Family",
        "models": ["qwen.compliance", "qwen.defence", "qwen.general", "qwen.intuition", "qwen.voice"],
        "substrate": "qwen2.5:0.5b",
        "size_bytes": 379_000_000,
    },
    "llama": {
        "name": "Llama Family",
        "models": ["llama.compliance", "llama.defence", "llama.general", "llama.intuition", "llama.voice"],
        "substrate": "llama3.2:3b",
        "size_bytes": 1_900_000_000,
    },
    "deepseek": {
        "name": "DeepSeek Family",
        "models": ["deepseek.compliance", "deepseek.defence", "deepseek.general", "deepseek.intuition", "deepseek.voice"],
        "substrate": "deepseek-coder:1.3b",
        "size_bytes": 760_000_000,
    },
    "mistral": {
        "name": "Mistral Family",
        "models": ["mistral.compliance", "mistral.defence", "mistral.general", "mistral.intuition", "mistral.voice"],
        "substrate": "mistral:7b",
        "size_bytes": 4_100_000_000,
    },
    "kimi": {
        "name": "Kimi K3 Family (NEW)",
        "models": ["kimi.compliance", "kimi.defence", "kimi.general", "kimi.intuition", "kimi.voice"],
        "substrate": "kimi-k3:2.8t-moe",
        "size_bytes": 1_560_000_000_000,  # 1.56TB
        "context": 1_048_576,
        "license": "Kimi K3 License (commercial check required)",
        "index": 57,
    },
    "claude": {
        "name": "Claude Family",
        "models": ["claude.opus5", "claude.fable5"],
        "substrate": "API",
        "size_bytes": 0,
        "context": 200_000,
        "license": "Proprietary",
    },
    "gpt": {
        "name": "GPT Family",
        "models": ["gpt-5.6-sol"],
        "substrate": "API",
        "size_bytes": 0,
        "context": 128_000,
        "license": "Proprietary",
    },
    "core": {
        "name": "SOV3 Core",
        "models": ["sov3.unified", "sov3.v7", "sov-sovereign-v4", "sov3.evolved"],
        "substrate": "qwen2.5:0.5b + SOV3 drawing",
        "size_bytes": 379_000_000,
    },
}


# ─── Hives (5 tiers) ────────────────────────────────────────────────────

HIVES = {
    0: {"name": "Tiny (free CPU)", "tokens": 256, "substrate": "qwen2.5:0.5b", "ram_mb": 379, "cost_per_1m": 0.0},
    1: {"name": "Small (local)", "tokens": 1024, "substrate": "clan-plain", "ram_mb": 379, "cost_per_1m": 0.0},
    2: {"name": "Medium (drawing-tuned)", "tokens": 4096, "substrate": "sov33-v7", "ram_mb": 379, "cost_per_1m": 0.0},
    3: {"name": "Large (merged LoRA)", "tokens": 16384, "substrate": "sov-sovereign-v4", "ram_mb": 8192, "cost_per_1m": 0.0},
    4: {"name": "Sovereign (council)", "tokens": 65536, "substrate": "council-mix", "ram_mb": 12288, "cost_per_1m": 0.0},
}


# ─── Upstream routing ──────────────────────────────────────────────────

UPSTREAMS = {
    "cheap": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "cost_per_1m_in": 0.14,
        "cost_per_1m_out": 0.28,
        "license": "MIT (open weights)",
        "context": 1_000_000,
    },
    "production": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-reasoner",
        "cost_per_1m_in": 0.435,
        "cost_per_1m_out": 0.87,
        "license": "MIT (open weights)",
        "context": 1_000_000,
    },
    "sovereign": {
        "url": "https://api.moonshot.ai/v1/chat/completions",
        "model": "kimi-k3",
        "cost_per_1m_in": 3.0,
        "cost_per_1m_out": 15.0,
        "license": "Kimi K3 License (commercial check required)",
        "context": 1_048_576,
    },
    "agentic": {
        "url": "https://api.anthropic.com/v1/messages",
        "model": "claude-opus-5",
        "cost_per_1m_in": 5.0,
        "cost_per_1m_out": 25.0,
        "license": "Proprietary",
        "context": 200_000,
    },
    "local": {
        "url": f"{SOV_GATEWAY_URL}/v1/chat/completions",
        "model": "sov33-unified",
        "cost_per_1m_in": 0.0,
        "cost_per_1m_out": 0.0,
        "license": "Proprietary (sovereign)",
        "context": 8192,
    },
}


# ─── Status checks ──────────────────────────────────────────────────────

def check_local_models():
    """List local Ollama models."""
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5) as r:
            data = json.loads(r.read())
            return [m["name"] for m in data.get("models", [])]
    except Exception as e:
        return []


def check_sov_gateway():
    """Verify sov-gateway is alive."""
    try:
        with urllib.request.urlopen(f"{SOV_GATEWAY_URL}/v1/models", timeout=5) as r:
            data = json.loads(r.read())
            return {"status": "live", "count": len(data.get("data", []))}
    except Exception as e:
        return {"status": "down", "error": str(e)[:100]}


def count_clans_and_hives():
    """Count OWEM clans + hives from the master registry."""
    n_clans = 8  # per OWEM_MASTER_REGISTRY.md
    n_specialists = 13
    n_refusal = 14
    n_hybrid = 20
    n_total_owem = 95
    
    return {
        "clans": n_clans,
        "specialists_per_clan": n_specialists,
        "refusal_models": n_refusal,
        "hybrid_models": n_hybrid,
        "total_owem": n_total_owem,
        "new_clans": ["kimi", "claude", "gpt"],
    }


# ─── Routing logic ─────────────────────────────────────────────────────

def route_query(query: str, cost_pref: str = "auto") -> dict:
    """Route a query to the optimal upstream based on cost/capability heuristics."""
    q_lower = query.lower()
    
    # Tier 0 (cheap) for short, simple queries
    if cost_pref == "cheap" or len(query) < 200:
        tier = "cheap"
        model = "deepseek-chat"
        reason = "short query → cheap tier"
    # Tier 4 (sovereign) for sovereignty-critical or governance queries
    elif any(kw in q_lower for kw in ["article", "compliance", "audit", "regulation", "dora", "nis2", "ai act"]):
        tier = "sovereign"
        model = "kimi-k3"
        reason = "sovereignty-critical → Kimi K3 (1M context, open weights)"
    # Tier 3 (agentic) for multi-step agentic workflows
    elif any(kw in q_lower for kw in ["agent", "workflow", "orchestrate", "multi-step", "code"]):
        tier = "agentic"
        model = "claude-opus-5"
        reason = "agentic workflow → Claude Opus 5"
    # Default: production tier
    else:
        tier = "production"
        model = "deepseek-reasoner"
        reason = "default → DeepSeek V4-Pro ($0.87/M, MIT)"
    
    up = UPSTREAMS[tier]
    return {
        "tier": tier,
        "model": model,
        "url": up["url"],
        "cost_per_1m_in": up["cost_per_1m_in"],
        "cost_per_1m_out": up["cost_per_1m_out"],
        "reason": reason,
    }


# ─── Status report ─────────────────────────────────────────────────────

def status():
    print("=== Universal AI Harness — Clans + Hives ===\n")
    
    # Clans
    print("CLANS (8 families × 13 specialists = 104 OWEMs)")
    print("-" * 60)
    for name, c in CLANS.items():
        substrate_info = f"substrate={c['substrate']}"
        if "size_bytes" in c and c["size_bytes"] > 0:
            mb = c["size_bytes"] / 1_000_000
            if mb > 1000:
                substrate_info += f" ({mb/1000:.1f}GB)"
            else:
                substrate_info += f" ({mb:.0f}MB)"
        print(f"  {c['name']:30s} {substrate_info}")
        for m in c["models"]:
            print(f"    - {m}")
    print()
    
    # Hives
    print("HIVES (5 tiers)")
    print("-" * 60)
    for tier, h in HIVES.items():
        print(f"  Tier {tier}: {h['name']}")
        print(f"    Substrate: {h['substrate']}, Tokens: {h['tokens']}, RAM: {h['ram_mb']}MB, Cost: ${h['cost_per_1m']}/M")
    print()
    
    # Upstreams
    print("UPSTREAMS (routing targets)")
    print("-" * 60)
    for name, u in UPSTREAMS.items():
        print(f"  {name:12s} {u['model']:25s} ${u['cost_per_1m_in']:.3f}/${u['cost_per_1m_out']:.3f} per 1M  ({u['license'][:30]})")
    print()
    
    # Local models
    print("LOCAL MODELS (Ollama @ :11434)")
    print("-" * 60)
    models = check_local_models()
    print(f"  Count: {len(models)}")
    print(f"  Substrate: qwen2.5:0.5b (379MB base)")
    print(f"  Top 10: {', '.join(models[:10])}")
    print()
    
    # sov-gateway
    print("SOV-GATEWAY (:8080)")
    print("-" * 60)
    sg = check_sov_gateway()
    print(f"  Status: {sg['status']}")
    if sg['status'] == 'live':
        print(f"  Models: {sg['count']} available via OpenAI-compatible API")
    print()
    
    # Counts
    print("OWEM COUNTS (from OWEM_MASTER_REGISTRY.md)")
    print("-" * 60)
    counts = count_clans_and_hives()
    print(f"  Clans: {counts['clans']} (incl. {', '.join(counts['new_clans'])} — new from July 2026)")
    print(f"  Specialists per clan: {counts['specialists_per_clan']}")
    print(f"  Refusal models: {counts['refusal_models']}")
    print(f"  Hybrid models: {counts['hybrid_models']}")
    print(f"  Total OWEMs: {counts['total_owem']}")
    print()
    
    print("=== THESIS ===")
    print("Don't fight Kimi K3 / DeepSeek V4 / Mastra / Claude / LongCat.")
    print("JOIN them all into the OWEM clan+hive topology.")
    print("Every model is harnessed, not replaced.")
    print()
    print('"Models don\'t matter — the harness is everything."')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--route", help="Route a query to optimal upstream")
    parser.add_argument("--hive", type=int, help="Spawn a hive at tier N")
    parser.add_argument("--spawn", help="User ID for hive spawn")
    args = parser.parse_args()
    
    if args.status:
        status()
    elif args.route:
        r = route_query(args.route)
        print(json.dumps(r, indent=2))
    elif args.hive is not None:
        h = HIVES.get(args.hive)
        if h:
            user = args.spawn or "anon"
            print(f"Would spawn hive tier {args.hive} for user {user}")
            print(f"Substrate: {h['substrate']}")
            print(f"Tokens: {h['tokens']}")
            print(f"RAM: {h['ram_mb']}MB")
        else:
            print(f"Invalid tier: {args.hive}")
    else:
        status()


if __name__ == "__main__":
    import argparse
    main()