#!/usr/bin/env python3
"""Cross-lab GOVERNED city — frontier + local citizens through the bolted ruler.

Frontier citizens (OpenRouter slugs: nvidia/nemotron, alibaba/qwen3.5, deepseek)
and local citizens (sov6 fleet) all get: same brief, same grammar, same Art 5
gate, same JUDGE.lock. The judge never changes (Part AV); only the bloodline does.
Budget-capped before every frontier call.

This is the doc's L14 done right: real governed city, decorrelated bloodlines,
East vs West vs local, through the bolted ruler.
"""
from __future__ import annotations

import argparse, json, sys, random
from pathlib import Path

sys.path.insert(0, "/workspace/csoai-static-deploy2/SOVOS/packages/sovos-city/src")

def main():
    ap = argparse.ArgumentParser(prog="cross_lab_city")
    ap.add_argument("--budget", type=float, default=2.00)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--citizens", type=int, default=30)
    ap.add_argument("--frontier", default="nvidia/nemotron-3.5-lightning,qwen/qwen3.5-35b-a3b,deepseek/deepseek-v4-pro")
    ap.add_argument("--out", default="/workspace/cross-lab-city-2026-08-12")
    ap.add_argument("--local-models", default="")
    a = ap.parse_args()

    from sovos_city.arena import build_citizens, CityRun
    from sovos_city.openrouter import Budget, load_key

    key = load_key()
    if not key:
        print("NO KEY", flush=True)
        return 2

    # local models (sov6 fleet on this pod)
    from sovos_city.arena import ollama_models
    local = [m for m in ollama_models() if ":" in m or "sov" in m]
    if a.local_models:
        local = [m.strip() for m in a.local_models.split(",") if m.strip()]

    # build a mixed city: frontier slug citizens + local citizens
    frontier_slugs = [m.strip() for m in a.frontier.split(",") if m.strip()]
    all_models = frontier_slugs + local
    # allocate citizens: distribute across frontier + local proportionally
    rng = random.Random(7)
    n_frontier = min(len(frontier_slugs) * 4, max(4, a.citizens // 3))
    citizens = build_citizens(frontier_slugs, n_frontier, rng, stratified=False)
    local_cits = build_citizens(local, max(4, a.citizens - n_frontier), rng, stratified=False)
    citizens = citizens + local_cits

    print(f"CROSS-LAB CITY · {len(citizens)} citizens "
          f"({len(frontier_slugs)} frontier + {len(local)} local) · "
          f"{a.epochs} epochs · ${a.budget:.2f} cap", flush=True)
    print(f"  frontier: {frontier_slugs}", flush=True)
    print(f"  local: {local}", flush=True)

    run = CityRun(Path(a.out), citizens, epochs=a.epochs,
                  host="http://127.0.0.1:11434",
                  or_key=key, budget=Budget(cap_usd=a.budget))
    board = run.run()
    print(json.dumps(board, indent=2, default=str))
    return 0

if __name__ == "__main__":
    sys.exit(main())