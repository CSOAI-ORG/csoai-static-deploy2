#!/usr/bin/env python3
"""meok_battles — emit pair-aware BATTLE records from judged verdict rows (arena v2 data product).
A battle exists when two models were judged on the SAME (task, want): correct beats incorrect.
UNMEASURED never wins or loses (excluded honestly). Output: ~/meok-battles.jsonl + summary.
"""
import json, os
from collections import defaultdict

def main():
    path = os.path.expanduser("~/clawd/sovereign-distill-corpus.jsonl")
    rows = [json.loads(l) for l in open(path) if "verdict" in l]
    by_task = defaultdict(list)
    for r in rows:
        if r.get("verdict") in ("correct", "incorrect") and r.get("task") and r.get("want"):
            by_task[(r["task"][:45], r["want"])].append(r)
    battles, skipped = [], 0
    for (task, want), group in by_task.items():
        winners = [r for r in group if r["verdict"] == "correct"]
        losers = [r for r in group if r["verdict"] == "incorrect"]
        for w in winners:
            for l in losers:
                if w.get("provider") == l.get("provider"):
                    continue  # same model can't battle itself
                battles.append({
                    "model_a": w.get("provider") or w.get("model"), "model_b": l.get("provider") or l.get("model"),
                    "a_win": True, "task": task, "want": want, "source": "verdict-pair",
                    "judge": "dorado+rule", "t": w.get("t") or "",
                })
        if not winners or not losers:
            skipped += 1
    out = os.path.expanduser("~/meok-battles.jsonl")
    with open(out, "w") as f:
        for b in battles:
            f.write(json.dumps(b, ensure_ascii=False) + "\n")
    print(f"battles: {len(battles)} (from {len(rows)} rows; {skipped} task-groups without win/loss pair)")
    print(f"-> {out}")

if __name__ == "__main__":
    main()
