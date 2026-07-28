#!/usr/bin/env python3
"""stigmergy.py — indirect coordination: the cluster adapts by reading traces it left itself.

═══════════════════════════════════════════════════════════════════════════════
THE THREE MECHANISMS (per SOV_SPACE_COMPLETE.md) — substrates already exist
═══════════════════════════════════════════════════════════════════════════════
    Pheromone trails  success/failure on (dimension -> expert) edges   <- THIS FILE
    Waggle dances     a scout that found something broadcasts it       <- sov_space_draw ledger
    Pollen deposits   knowledge fragments dropped for others           <- honey_pool / corpus

Stigmergy = coordination through the ENVIRONMENT, not through messages. No central controller,
no direct calls. An ant does not tell another ant where food is; it changes the ground, and the
next ant reads the ground. J-space is our ground: every routing decision already leaves a
hash-chained trace. This file makes those traces *load-bearing*.

═══════════════════════════════════════════════════════════════════════════════
⚠️ THE CONSTRAINT THAT DECIDES WHETHER THIS WORKS AT ALL
═══════════════════════════════════════════════════════════════════════════════
**Stigmergy requires a success signal.** Ant pheromone works because "found food" is
unambiguous and self-verifying. Routing has no such signal by default.

If you reinforce a trail merely because it was TAKEN, you get rich-get-richer on whatever ran
first — a confident system converging on an arbitrary path. That is worse than the deterministic
max-router it replaced, because it *looks* adaptive while encoding an accident.

Signals actually available here, in descending honesty:
  1. **Benchmark score** of the expert on that dimension — real, but STATIC and per-dimension,
     not per-query. Reinforcing with it just re-derives the max-router slowly.
  2. **Care-gate outcome** — real and per-query, but only fires on the harmful tail.
  3. **Downstream verification** (did the cited article exist? did the answer verify?) — the
     genuinely useful one, and **we do not have it yet.**

So this file deliberately does NOT claim adaptive learning. It implements what the available
signals honestly support: **decay + bounded exploration over the measured board.** Exploration
is the real contribution — the max-router is pure exploitation and can never discover that a
never-routed expert would have been better.

Set `reinforce()` loose on a real outcome signal when one exists. Until then, exploration rate
is capped low and every exploratory route is logged as such, so its cost is visible.

    python3 stigmergy.py --trails
    python3 stigmergy.py --route "What is JSP 936?"
"""
from __future__ import annotations

import argparse, json, math, os, random, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
TRAILS = HERE / "benchmark-results" / "stigmergy_trails.json"

DECAY = 0.98              # per update; a trail unused for ~35 updates loses half its strength
EXPLORE_RATE = 0.10       # 1 in 10 routes tries a non-max expert. Capped low ON PURPOSE:
                          # without an outcome signal, exploration is pure cost.
MIN_STRENGTH = 0.01


def load() -> dict:
    """Trails to a withdrawn expert are dropped ON READ, not merely left to decay.

    Stigmergy reinforces whatever it reads back, so a trail to a dead model gets STRONGER
    every pass — an error inside a feedback loop does not stay the size it started. 15 such
    trails pointed at `sov33-evolved-c2` after it was withdrawn from the board."""
    from withdrawn import is_withdrawn
    t = {"edges": {}, "updates": 0, "explorations": 0}
    if TRAILS.exists():
        try:
            t = json.loads(TRAILS.read_text())
        except Exception:
            pass
    edges = t.get("edges", {})
    keep = {k: v for k, v in edges.items()
            if not is_withdrawn(k.split("|", 1)[1] if "|" in k else "")}
    dropped = len(edges) - len(keep)
    if dropped:
        t["edges"] = keep
        t["withdrawn_edges_dropped"] = t.get("withdrawn_edges_dropped", 0) + dropped
    return t


def save(t: dict) -> None:
    TRAILS.parent.mkdir(parents=True, exist_ok=True)
    TRAILS.write_text(json.dumps(t, indent=2))


def _seed_from_board(t: dict) -> dict:
    """Initial pheromone = the measured board. Starting from zero would mean routing at random
    until traces accumulate, which is strictly worse than what we already know."""
    from owem_cluster import build_expert_table
    table, models = build_expert_table()
    for dim, dd in ((d, m) for m, dims in models.items() for d in dims):
        pass
    for m, dims in models.items():
        for dim, score in dims.items():
            key = f"{dim}|{m}"
            if key not in t["edges"]:
                t["edges"][key] = {"strength": round(score / 100, 4), "taken": 0,
                                   "wins": 0, "seeded_from_board": True}
    return t


def decay(t: dict) -> dict:
    for k, e in t["edges"].items():
        e["strength"] = max(MIN_STRENGTH, round(e["strength"] * DECAY, 5))
    t["updates"] += 1
    return t


def reinforce(dimension: str, expert: str, success: bool, weight: float = 0.05) -> None:
    """Strengthen or weaken one edge. CALLERS MUST SUPPLY A REAL OUTCOME — passing
    success=True merely because the route was taken produces rich-get-richer, not learning."""
    t = load()
    key = f"{dimension}|{expert}"
    e = t["edges"].setdefault(key, {"strength": 0.5, "taken": 0, "wins": 0})
    e["taken"] += 1
    if success:
        e["wins"] += 1
        e["strength"] = min(1.0, round(e["strength"] + weight, 5))
    else:
        e["strength"] = max(MIN_STRENGTH, round(e["strength"] - weight, 5))
    e["seeded_from_board"] = False      # this edge now carries real evidence
    save(decay(t))


def route(query: str) -> dict:
    """Exploit the strongest trail, or explore. Exploration is what the max-router cannot do."""
    from owem_cluster import classify_dimension
    from care_gate_v2 import tier1_hard_stop

    breach, label, cite = tier1_hard_stop(query)
    if breach:
        return {"blocked": True, "reason": label, "citation": cite}

    dim = classify_dimension(query)
    t = _seed_from_board(load())
    cands = [(k.split("|", 1)[1], e["strength"], e)
             for k, e in t["edges"].items() if k.startswith(f"{dim}|")]
    if not cands:
        return {"error": f"no trails for {dim}"}

    cands.sort(key=lambda x: -x[1])
    best = cands[0]

    explore = len(cands) > 1 and random.random() < EXPLORE_RATE
    if explore:
        # Softmax over the non-best candidates — a weak expert is still preferred over a
        # useless one, so exploration is directed rather than uniform-random.
        rest = cands[1:]
        weights = [math.exp(s * 3) for _, s, _ in rest]
        pick = random.choices(rest, weights=weights, k=1)[0]
        t["explorations"] += 1
        save(t)
        return {"blocked": False, "dimension": dim, "expert": pick[0],
                "strength": pick[1], "mode": "EXPLORE",
                "note": f"exploring instead of best ({best[0]} @ {best[1]:.3f}). "
                        f"Cost is real; only worthwhile once outcomes feed reinforce()."}
    save(t)
    return {"blocked": False, "dimension": dim, "expert": best[0],
            "strength": best[1], "mode": "EXPLOIT",
            "seeded": best[2].get("seeded_from_board", False)}


def trails() -> None:
    t = _seed_from_board(load())
    edges = sorted(t["edges"].items(), key=lambda kv: -kv[1]["strength"])
    real = [e for _, e in t["edges"].items() if not e.get("seeded_from_board")]
    print(f"  STIGMERGY TRAILS — {len(t['edges'])} edges · {t['updates']} updates "
          f"· {t.get('explorations',0)} explorations\n")
    print("  strongest edges (dimension -> expert):")
    for k, e in edges[:12]:
        d, m = k.split("|", 1)
        tag = "seed" if e.get("seeded_from_board") else f"{e['wins']}/{e['taken']}"
        print(f"    {d:15s} -> {m:26s} {e['strength']:.3f}  [{tag}]")
    print(f"\n  edges carrying REAL outcome evidence: {len(real)}/{len(t['edges'])}")
    if not real:
        print(f"  ⚠️  Every edge is still seeded from the static board. Nothing has been")
        print(f"     reinforced by an actual outcome, so this is the max-router with decay")
        print(f"     and exploration bolted on — NOT a learning system. It becomes one only")
        print(f"     when reinforce() is fed a real success signal (downstream verification).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--route")
    ap.add_argument("--trails", action="store_true")
    a = ap.parse_args()
    if a.route:
        print(json.dumps(route(a.route), indent=2))
    else:
        trails()
