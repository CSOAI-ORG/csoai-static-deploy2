#!/usr/bin/env python3
"""arena_bt.py — Bradley-Terry arena ratings over DETERMINISTIC battles.

The LMArena/FastChat method (BT ratings over pairwise battles — the original Chatbot
Arena engine is Apache-2.0; the BT math itself is standard statistics, reimplemented
here) — with the CSOAI difference that IS the moat:

  LMArena's battle  = two anonymous answers, a human PREFERENCE vote.
  Our battle        = two models on the SAME frozen probe, the DETERMINISTIC grader's
                      verdict. A "vote" here is a predicate (correct vs incorrect),
                      not a preference — reproducible bit-for-bit by anyone.

A battle exists for (item, A, B) when exactly one of A,B answered the item correctly.
Items both got right or both got wrong produce NO battle (no signal — honest).
Ratings: standard BT maximum-likelihood (minorization iteration), reported on an
Elo-like scale (1000 + 400·log10 r) with battle counts. Models with <MIN_BATTLES
comparisons are reported UNRATED, never given a flattering default.

    python3 arena_bt.py --peritem 'SOVOS/boards-v2-2026-08-12/peritem_*.jsonl'
    python3 arena_bt.py --selftest
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

MIN_BATTLES = 20   # below this a rating is noise — report UNRATED instead


def load_items(patterns: list[str]):
    """item-key -> {model: correct(bool)} from peritem jsonl files."""
    by_item: dict[str, dict[str, bool]] = defaultdict(dict)
    files = []
    for pat in patterns:
        files += glob.glob(pat)
    for f in sorted(files):
        axis = Path(f).stem.replace("peritem_", "")
        for line in open(f, errors="ignore"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = d.get("model")
            if not m or d.get("transport_error"):
                continue
            c = d.get("correct")
            c = (c is True) or (isinstance(c, str) and c.lower() == "true")
            key = axis + "::" + str(d.get("axis_item") or d.get("item"))[:120]
            by_item[key][m] = c
    return by_item, len(files)


def battles_from_items(by_item):
    """Pairwise wins: for each item, every (correct, incorrect) model pair is one battle."""
    wins = defaultdict(int)            # (winner, loser) -> count
    for _item, res in by_item.items():
        right = [m for m, ok in res.items() if ok]
        wrong = [m for m, ok in res.items() if not ok]
        for w in right:
            for l in wrong:
                wins[(w, l)] += 1
    return wins


def bt_ratings(wins, iters: int = 200, tol: float = 1e-9):
    """Standard Bradley-Terry MLE via minorization. Returns model -> r (geometric mean 1)."""
    models = sorted({m for pair in wins for m in pair})
    if not models:
        return {}
    r = {m: 1.0 for m in models}
    W = defaultdict(float)             # total wins per model
    pair_n = defaultdict(float)        # (a,b) unordered -> total battles
    for (w, l), n in wins.items():
        W[w] += n
        key = (min(w, l), max(w, l))
        pair_n[key] += n
    for _ in range(iters):
        delta = 0.0
        new = {}
        for m in models:
            denom = 0.0
            for (a, b), n in pair_n.items():
                if m == a:
                    denom += n / (r[a] + r[b])
                elif m == b:
                    denom += n / (r[a] + r[b])
            new[m] = (W[m] / denom) if denom > 0 else r[m]
        gm = math.exp(sum(math.log(max(v, 1e-12)) for v in new.values()) / len(new))
        for m in models:
            new[m] /= gm               # identifiability: geometric mean 1
            delta = max(delta, abs(new[m] - r[m]))
        r = new
        if delta < tol:
            break
    return r


def leaderboard(patterns: list[str]):
    by_item, nfiles = load_items(patterns)
    wins = battles_from_items(by_item)
    r = bt_ratings(wins)
    nb = defaultdict(int)
    for (w, l), n in wins.items():
        nb[w] += n
        nb[l] += n
    rows = []
    for m, ri in r.items():
        rated = nb[m] >= MIN_BATTLES
        rows.append({
            "model": m,
            "bt_elo": round(1000 + 400 * math.log10(max(ri, 1e-12)), 1) if rated else None,
            "battles": nb[m],
            "status": "RATED" if rated else "UNRATED (<%d battles)" % MIN_BATTLES,
        })
    rows.sort(key=lambda x: (x["bt_elo"] is None, -(x["bt_elo"] or 0)))
    return {
        "method": ("Bradley-Terry over DETERMINISTIC battles — a battle is two models on the same "
                   "frozen probe where exactly one was graded correct. No human preference votes; "
                   "every outcome is a reproducible predicate. (Rating math as in the original "
                   "open-source Chatbot Arena; verdicts are ours.)"),
        "items_graded": len(by_item),
        "battle_pairs": sum(wins.values()),
        "source_files": nfiles,
        "not_a_certification": True,
        "leaderboard": rows,
    }


def _selftest() -> int:
    # A beats B 30-0, B beats C 30-0 → strict ordering; D has 2 battles → UNRATED
    wins = {("A", "B"): 30, ("B", "C"): 30, ("A", "C"): 30, ("D", "C"): 2}
    r = bt_ratings(wins)
    assert r["A"] > r["B"] > r["C"], "BT must order transitively dominant models"
    nb = defaultdict(int)
    for (w, l), n in wins.items():
        nb[w] += n; nb[l] += n
    assert nb["D"] < MIN_BATTLES, "D must be under the rating floor"
    # symmetry: equal record → equal rating
    r2 = bt_ratings({("X", "Y"): 10, ("Y", "X"): 10})
    assert abs(r2["X"] - r2["Y"]) < 1e-6, "equal records must tie"
    # no-signal honesty: items where both were right/wrong yield no battles
    b = battles_from_items({"i1": {"A": True, "B": True}, "i2": {"A": False, "B": False}})
    assert not b, "no-signal items must produce zero battles"
    print("  ✅ arena_bt invariants hold (transitive order, tie symmetry, UNRATED floor, no-signal honesty)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--peritem", nargs="*", default=["SOVOS/boards-v2-2026-08-12/peritem_*.jsonl"])
    ap.add_argument("--out", default="benchmark-results/arena_bt_ratings.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    lb = leaderboard(a.peritem)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(lb, indent=1))
    print(f"items={lb['items_graded']} battles={lb['battle_pairs']} → {a.out}")
    for row in lb["leaderboard"][:10]:
        print(f"  {row['bt_elo'] if row['bt_elo'] is not None else '   UNRATED':>9}  "
              f"{row['model']:<28} {row['battles']:>5} battles")
