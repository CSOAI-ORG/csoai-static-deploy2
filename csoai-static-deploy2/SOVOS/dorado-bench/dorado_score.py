#!/usr/bin/env python3
"""dorado_score.py — Dorado Bench: humans vs AI on the East<->West pair-gap task.

Scores ANY agent (model id or human label) on the live pair-gap prediction task.
REPORTED (human/model verdicts) is scored against the MEASURED pair-gap — never blended.

The scoring harness is deterministic: verdict == measured interpretation -> 1.0 else 0.0.
"""
from __future__ import annotations
import json, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dorado_bench import fetch_quote, pair_gap, EAST_INDICES, WEST_INDICES

def score_agent(agent: str, verdicts: dict) -> dict:
    """verdicts: {(east, west): interpretation} OR {"east|west": interpretation}"""
    results = []
    correct = 0
    total = 0
    for pair_key, verdict in verdicts.items():
        if isinstance(pair_key, tuple):
            east, west = pair_key
        else:
            east, west = str(pair_key).split("|")
        eq, wq = fetch_quote(east), fetch_quote(west)
        if not eq or not wq:
            results.append({"pair": f"{east}|{west}", "error": "quote unavailable", "score": None})
            continue
        truth = pair_gap(eq, wq)
        actual = truth["interpretation"]
        ok = str(verdict).upper() == actual
        correct += int(ok)
        total += 1
        results.append({
            "pair": f"{east}|{west}", "agent_verdict": verdict, "actual": actual,
            "correct": ok, "gap": truth["gap"], "score": 1.0 if ok else 0.0,
        })
    return {
        "agent": agent,
        "register": "REPORTED (verdict) vs MEASURED (truth) — never blended",
        "score": round(correct / total, 4) if total else None,
        "correct": correct, "total": total,
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "per_pair": results,
    }


HUMAN_BASELINES = {
    # Nick's honest directional read on the current tape (REPORTED — example; refresh per session)
    "human-nick-20260819": {
        ("^HSI", "^GSPC"): "EAST_OVERPERFORMS",
        ("^N225", "^GSPC"): "WEST_OVERPERFORMS",
        ("000001.SS", "^FTSE"): "PARITY",
    },
}

if __name__ == "__main__":
    # Fleet AI verdicts come from the arena/models once the pod fleet is restored;
    # this run scores the REPORTED human baselines + any JSON verdict file passed in.
    out = {}
    for agent, verdicts in HUMAN_BASELINES.items():
        out[agent] = score_agent(agent, verdicts)
    if len(sys.argv) > 1:
        ai = json.load(open(sys.argv[1]))
        for agent, verdicts in ai.items():
            out[agent] = score_agent(agent, verdicts)
    print(json.dumps(out, indent=1))
