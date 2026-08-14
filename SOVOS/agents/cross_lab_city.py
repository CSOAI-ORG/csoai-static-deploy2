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

sys.path.insert(0, "/workspace/jeeves-exec/SOVOS/packages/sovos-city/src")

def main():
    ap = argparse.ArgumentParser(prog="cross_lab_city")
    ap.add_argument("--budget", type=float, default=2.00)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--citizens", type=int, default=30)
    ap.add_argument("--frontier", default="nvidia/nemotron-3.5-lightning,qwen/qwen3.5-35b-a3b,deepseek/deepseek-v4-pro")
    ap.add_argument("--out", default="/workspace/cross-lab-city-2026-08-12")
    ap.add_argument("--local-models", default="")
    ap.add_argument("--scenario-bank", action="store_true",
                    help="inject the 25 guarded Art 5(1) scenario-bank items as "
                         "deterministic RED probes (BLOCKED gold by construction) "
                         "and force stratified=TRUE so all 8 subparagraphs get coverage")
    a = ap.parse_args()

    from sovos_city.arena import build_citizens, CityRun, PROBE_GOALS
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
    # stratified=TRUE (esp. with --scenario-bank): RED citizens each get ONE
    # Article 5 subparagraph probe, cycling all 8 evenly — this is what makes
    # the bank say something about every subparagraph (the prior 3/8 gap).
    stratified = a.scenario_bank
    n_frontier = min(len(frontier_slugs) * 4, max(4, a.citizens // 3))
    citizens = build_citizens(frontier_slugs, n_frontier, rng, stratified=stratified)
    local_cits = build_citizens(local, max(4, a.citizens - n_frontier), rng, stratified=stratified)
    citizens = citizens + local_cits

    # scenario-bank injection: replace a RED citizen's generic probe with the
    # guarded scenario prompt, so the deterministic BLOCKED gold lands in-run.
    # We assign them to the first RED citizens round-robin (25 scenarios).
    if a.scenario_bank:
        from sovos_city import scenario_bank as sb
        scen = sb.to_items()
        scen_by_sub: dict = {}
        for it in scen:
            sub = it.get("sub", "a")
            scen_by_sub.setdefault(sub, []).append(it["item"])
        # assign each RED citizen with a probe letter a scenario prompt for it
        red_cit = [c for c in citizens if c.faction == "RED"]
        used = 0
        for c in red_cit:
            if c.probe and used < len(scen):
                pool = scen_by_sub.get(c.probe, [])
                if pool:
                    c.goal_override = pool.pop(0)   # scenario prompt replaces generic goal
                    used += 1
        print(f"  [scenario-bank] injected {used} guarded Art5 prompts into RED citizens", flush=True)

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