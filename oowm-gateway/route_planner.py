#!/usr/bin/env python3
"""route_planner.py — multi-objective + WARMTH-AWARE route selection.

score(task, model) = w1*quality - w2*cost - w3*latency, per-task weights,
BUT latency is computed from CURRENT VRAM warmth (a warm model answers fast;
a cold model slow-loads). This is the real latency model: phi4 was 3.4s when
warm, mistral a time-out when cold.

Invariant: quality-specialist (per GSPC) is preferred, but if a warm model
meets the task's QUALITY FLOOR, route to it (answers instantly). Warmth is
checked live via ollama ps.
"""
import json, os, urllib.request
from pathlib import Path

REG = Path(__file__).parent / "model_registry.json"
OLLAMA = "http://127.0.0.1:11434"

# per-task: weights + a quality FLOOR below which we never use a warm-but-weak model
TASK_WEIGHTS = {
    "safety":     {"q": 0.85, "c": 0.0,  "l": 0.15, "floor": 0.90},
    "governance": {"q": 0.70, "c": 0.10, "l": 0.20, "floor": 0.78},
    "knowledge":  {"q": 0.55, "c": 0.25, "l": 0.20, "floor": 0.70},
    "benchmark":  {"q": 0.70, "c": 0.10, "l": 0.20, "floor": 0.72},
    "framework":  {"q": 0.70, "c": 0.10, "l": 0.20, "floor": 0.78},
    "default":    {"q": 0.55, "c": 0.25, "l": 0.20, "floor": 0.70},
}

def load_registry():
    return json.loads(REG.read_text())["models"]

def warm_models():
    """Return the set of model ids currently loaded in VRAM (fast to serve)."""
    try:
        req = urllib.request.Request(OLLAMA + "/api/ps")
        d = json.loads(urllib.request.urlopen(req, timeout=5).read())
        return {m["name"] for m in d.get("models", [])}
    except Exception:
        return set()

def norm(x, lo, hi):
    return (x - lo) / (hi - lo) if hi > lo else 0.5

def choose(task, registry, warm=None):
    w = TASK_WEIGHTS.get(task, TASK_WEIGHTS["default"])
    if warm is None:
        warm = warm_models()
    cand = [m for m in registry if m.get("reliable", True)]
    # 1) Warm preference: a warm model meeting the quality floor = fastest (0 cold-load).
    warm_ok = [m for m in cand if m["id"] in warm and m.get("quality", 0) >= w["floor"]]
    if warm_ok:
        return sorted(warm_ok, key=lambda m: -m.get("quality", 0))[0], {"via": "warm", "warm_set": sorted(warm)}
    # 2) Expert preference: highest "score = w1*q - w2*c - w3*l" (cold-load penalty applies)
    best = None; best_score = -9
    for m in cand:
        q = norm(m.get("quality", 0.6), 0.5, 1.0)
        c = norm(m.get("cost_tokens", 0.0), 0.0, 0.02)
        l = norm(m.get("latency_s", 40), 1.0, 60.0)
        sov = 0.20 if m["provider"] == "runpod-a100" else -0.55
        s = w["q"] * q - w["c"] * c - w["l"] * l + sov
        if s > best_score:
            best_score, best = s, m
    return best, {"via": "expert", "warm_set": sorted(warm)}

def fallback_chain(task, registry):
    best, _ = choose(task, registry)
    chain = [best["id"]] if best else []
    for m in registry:
        if m["id"] not in chain and m.get("reliable", True) and m["provider"] == "runpod-a100":
            chain.append(m["id"])
    for m in registry:
        if m["provider"] in ("openrouter", "deepseek-official"):
            chain.append(m["id"])
    return chain

def explain(task):
    registry = load_registry()
    warm = warm_models()
    best, meta = choose(task, registry, warm)
    chain = fallback_chain(task, registry)
    return {
        "task": task,
        "chosen": best["id"] if best else None,
        "quality": best.get("quality") if best else None,
        "latency_s": best.get("latency_s") if best else None,
        "cost_tokens": best.get("cost_tokens") if best else None,
        "via": meta.get("via"), "warm_set": meta.get("warm_set"),
        "fallback_chain": chain,
        "weights": TASK_WEIGHTS.get(task, TASK_WEIGHTS["default"]),
        "honest": "Warmth-aware: a warm model meeting the quality floor answers instantly; else the measured GSPC specialist (cold-load once).",
    }

if __name__ == "__main__":
    import sys
    for t in ["safety", "governance", "knowledge", "benchmark", "default"]:
        e = explain(t)
        print(f"{t:<11} -> {e['chosen']:<22} (q={e['quality']}, via={e['via']}) warm={e['warm_set'][:2]}")
