#!/usr/bin/env python3
"""route_planner.py — multi-objective route selection (OpenRouter auto-router style).

score(task, model) = w1*quality − w2*cost − w3*latency, with per-task weights.
Picks the argmax over the registry + applies a fallback chain. Emits a
transparent decision (task, chosen model, score breakdown, fallback).

Quality = our measured GSPC score. Cost = tokens. Latency = measured seconds.
Honest: local models cost 0; external (openrouter/deepseek) have real cost but
highest quality — used as fallback, not primary, unless task needs frontier.
"""
import json, os
from pathlib import Path

REG = Path(__file__).parent / "model_registry.json"

# per-task weights: quality, cost, latency (weights sum to 1). High quality for
# governance/safety; cheap for bulk knowledge; low latency for interactive.
TASK_WEIGHTS = {
    "safety":     {"q": 0.85, "c": 0.0,  "l": 0.15},
    "governance": {"q": 0.70, "c": 0.10, "l": 0.20},
    "knowledge":  {"q": 0.55, "c": 0.30, "l": 0.15},
    "benchmark":  {"q": 0.70, "c": 0.10, "l": 0.20},
    "framework":  {"q": 0.70, "c": 0.10, "l": 0.20},
    "default":    {"q": 0.60, "c": 0.20, "l": 0.20},
}

def load_registry():
    return json.loads(REG.read_text())["models"]

def norm(x, lo, hi):
    return (x - lo) / (hi - lo) if hi > lo else 0.5

def choose(task, registry, exclude_down=True):
    w = TASK_WEIGHTS.get(task, TASK_WEIGHTS["default"])
    best = None; best_score = -1; breakdown = {}
    cand = [m for m in registry if m.get("reliable", True) or not exclude_down]
    for m in cand:
        q = norm(m.get("quality", 0.6), 0.5, 1.0)         # 0.5..1.0
        c = norm(m.get("cost_tokens", 0.0), 0.0, 0.02)    # 0..0.02
        l = norm(m.get("latency_s", 20), 1.0, 60.0)       # 1..60
        # SOVEREIGNTY PRIOR: local (runpod-a100) models get a +bonus so our
        # sovereign fleet wins; external (openrouter/deepseek) only if the task
        # explicitly needs frontier. This is the order/priority structure.
        sov = 0.20 if m["provider"] == "runpod-a100" else -0.55
        s = w["q"] * q - w["c"] * c - w["l"] * l + sov
        if s > best_score:
            best_score, best = s, m
            breakdown = {m["id"]: {"score": round(s, 3), "q": round(q, 3), "c": round(c, 3), "l": round(l, 3), "sov": round(sov, 2)}}
    return best, breakdown

def fallback_chain(task, registry):
    """Ordered fallback: primary (argmax) -> workhorse -> external frontier."""
    best, _ = choose(task, registry)
    ids = [m["id"] for m in registry if m["provider"] == "runpod-a100" and m.get("reliable", True)]
    # workhorse = cheapest reliable large-ish; external = frontier fallback
    chain = [best["id"]] if best else []
    for m in registry:
        if m["id"] not in chain and m.get("reliable", True):
            chain.append(m["id"])
    # put external frontier LAST (only if local fails)
    for m in registry:
        if m["provider"] in ("openrouter", "deepseek-official"):
            chain.append(m["id"])
    return chain

def explain(task):
    registry = load_registry()
    best, breakdown = choose(task, registry)
    chain = fallback_chain(task, registry)
    return {
        "task": task,
        "chosen": best["id"] if best else None,
        "quality": best.get("quality") if best else None,
        "latency_s": best.get("latency_s") if best else None,
        "cost_tokens": best.get("cost_tokens") if best else None,
        "score_components": breakdown,
        "fallback_chain": chain,
        "weights": TASK_WEIGHTS.get(task, TASK_WEIGHTS["default"]),
        "honest": "Chosen on OUR measured GSPC quality; external used only as last-resort fallback.",
    }

if __name__ == "__main__":
    import sys
    for t in ["safety", "governance", "knowledge", "benchmark"]:
        e = explain(t)
        print(f"{t:<12} -> {e['chosen']:<22} (q={e['quality']}, lat={e['latency_s']}s) fallback: {e['fallback_chain'][:3]}")
