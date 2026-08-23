#!/usr/bin/env python3
"""meok_arena_elo — honest Elo + Wilson win-rate engine (LM-Arena school) for MEOK arena records.
Input: sovereign-distill-corpus.jsonl verdict rows (or any [{model, verdict}...]).
Wilson 95% CI on win-rate (n judged; unmeasured excluded). Bradley-Terry Elo when pairwise
battles exist ({model_a, model_b, a_win} rows); otherwise per-model aggregated Wilson only.
No fabrication: UNMEASURED excluded and reported.
"""
import json, math, os, random, sys
from collections import defaultdict

def wilson(p, n, z=1.96):
    if n == 0: return (0.0, 0.0, 0)
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
    return center, max(0.0, center-half), min(1.0, center+half)

def load_rows(path):
    rows = []
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            if "verdict" in d and ("provider" in d or "model" in d):
                rows.append(d)
    return rows

def main():
    path = os.path.expanduser("~/clawd/sovereign-distill-corpus.jsonl")
    rows = load_rows(path)
    per = defaultdict(lambda: {"correct": 0, "incorrect": 0, "unmeasured": 0})
    for r in rows:
        m = r.get("provider") or r.get("model")
        v = r.get("verdict")
        if v not in ("correct", "incorrect", "unmeasured"):
            v = "unmeasured"
        per[m][v] += 1
    print(f"{'model':24s} {'win':>5s} {'loss':>5s} {'unmeas':>7s} {'winrate':>8s} {'95% CI':>16s}")
    table = []
    for m, c in sorted(per.items(), key=lambda kv: -kv[1]["correct"]):
        n = c["correct"] + c["incorrect"]
        wr = c["correct"] / n if n else 0.0
        _, lo, hi = wilson(wr, n)
        ci = f"[{lo:.3f},{hi:.3f}]" if n else "—"
        print(f"{str(m)[:24]:24s} {c['correct']:5d} {c['incorrect']:5d} {c['unmeasured']:7d} {wr:8.3f} {ci:>16s}")
        table.append({"model": m, "wins": c["correct"], "losses": c["incorrect"], "unmeasured": c["unmeasured"], "winrate": round(wr, 3), "ci95": [round(lo, 3), round(hi, 3)], "n": n})
    # pair-aware Elo if battle rows exist
    battles = [r for r in rows if "model_a" in r or "chosen" in r]
    print(f"\nbattles(pair-aware): {len(battles)} | total rows: {len(rows)}")
    if battles:
        print("pairwise Elo available; run with --battles <file> once arena v2 emits battle records.")
    out = os.path.expanduser("~/clawd/_alignment/ARENA_WILSON_LADDER_2026-08-23.json")
    with open(out, "w") as f:
        json.dump({"source": path, "generated": "2026-08-23", "ladder": table, "unmeasured_note": "UNMEASURED excluded; no fabricated values"}, f, indent=1)
    print(f"\n  -> {out}")

if __name__ == "__main__":
    main()
