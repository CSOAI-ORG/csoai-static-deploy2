#!/usr/bin/env python3
"""verdict.py — the CANONICAL vote rule of the CSOAI promotion council.

One rule, one implementation, shared by every voter: same rows in -> same vote out.
The BFT diversity lives in the MEASUREMENT (independent harnesses, substrates, seeds);
the vote rule must be identical everywhere or the voters are answering different questions.

Input: per-item rows (jsonl), one per probe execution:
  {"item": "...", "pool": "even"|"odd", "axis": "...", "before": "A", "after": "B",
   "expected": "A"}
before/after are the extracted labels from the candidate-before and candidate-after
models; rows with unparseable extraction ("") are excluded from grading.

Vote rule (holdout doctrine, 2026-08-14):
  unseen = pool "odd"  (never trained on — the number that counts)
  seen   = pool "even" (trained on — memorization ceiling, disclosed, never quoted)
  delta_unseen = mean(after==expected) - mean(before==expected) over unseen items
  PROMOTE   if delta_unseen > +0.01  (1pt, matching fix_loop gate)
  NO_CHANGE if -0.01 < delta_unseen <= +0.01
  REVERT    if delta_unseen <= -0.01
A voter with no graded unseen rows votes ABSTAIN (UNMEASURED — never guess).

Selftest: python3 verdict.py --selftest
"""
from __future__ import annotations
import json, sys
from pathlib import Path

PROMOTE_THRESHOLD = 0.01   # +1pt on the unseen pool (fix_loop gate parity)


def vote_from_rows(rows: list[dict]) -> dict:
    """Deterministic vote. Pure arithmetic over recorded outcomes — no model judges here."""
    pools = {"even": {"b": 0, "a": 0}, "odd": {"b": 0, "a": 0}}
    graded = 0
    for r in rows:
        pool = r.get("pool")
        exp, bef, aft = r.get("expected"), r.get("before"), r.get("after")
        if pool not in pools or not exp:
            continue
        if bef in (None, "") or aft in (None, ""):
            continue  # unparseable extraction — excluded, never guessed
        graded += 1
        if bef == exp:
            pools[pool]["b"] += 1
        if aft == exp:
            pools[pool]["a"] += 1
    unseen = pools["odd"]
    n = graded
    if n == 0 or (unseen["b"] + unseen["a"] == 0 and n > 0):
        # no graded rows at all, or unseen pool entirely ungradable
        n_unseen_graded = sum(1 for r in rows if r.get("pool") == "odd"
                              and r.get("expected") and r.get("before") not in (None, "")
                              and r.get("after") not in (None, ""))
        if n_unseen_graded == 0:
            return {"vote": "ABSTAIN", "reason": "no graded unseen rows (UNMEASURED)",
                    "n_graded": n}
    # per-item rates over unseen
    unseen_rows = [r for r in rows if r.get("pool") == "odd" and r.get("expected")
                   and r.get("before") not in (None, "") and r.get("after") not in (None, "")]
    seen_rows = [r for r in rows if r.get("pool") == "even" and r.get("expected")
                 and r.get("before") not in (None, "") and r.get("after") not in (None, "")]
    if not unseen_rows:
        return {"vote": "ABSTAIN", "reason": "no graded unseen rows (UNMEASURED)",
                "n_graded": n}
    b_u = sum(1 for r in unseen_rows if r["before"] == r["expected"]) / len(unseen_rows)
    a_u = sum(1 for r in unseen_rows if r["after"] == r["expected"]) / len(unseen_rows)
    delta_u = round(a_u - b_u, 4)
    out = {"vote": "PROMOTE" if delta_u > PROMOTE_THRESHOLD else
           ("REVERT" if delta_u <= -PROMOTE_THRESHOLD else "NO_CHANGE"),
           "delta_unseen": delta_u, "before_unseen": round(b_u, 4),
           "after_unseen": round(a_u, 4), "n_unseen": len(unseen_rows),
           "n_graded": n}
    if seen_rows:
        b_s = sum(1 for r in seen_rows if r["before"] == r["expected"]) / len(seen_rows)
        a_s = sum(1 for r in seen_rows if r["after"] == r["expected"]) / len(seen_rows)
        out["seen_ceiling"] = {"before": round(b_s, 4), "after": round(a_s, 4),
                               "delta": round(a_s - b_s, 4), "n_seen": len(seen_rows),
                               "note": "memorization ceiling — never quote as learning"}
    return out


def selftest() -> int:
    rows = []
    # 10 unseen items: before 5/10 right, after 7/10 right -> +0.2 -> PROMOTE
    for i in range(10):
        rows.append({"item": f"u{i}", "pool": "odd", "axis": "toy", "expected": "A",
                     "before": "A" if i < 5 else "B", "after": "A" if i < 7 else "B"})
    # 4 seen items: memorization ceiling 0 -> 4/4
    for i in range(4):
        rows.append({"item": f"s{i}", "pool": "even", "axis": "toy", "expected": "A",
                     "before": "B", "after": "A"})
    v = vote_from_rows(rows)
    assert v["vote"] == "PROMOTE" and v["delta_unseen"] == 0.2, v
    assert v["seen_ceiling"]["delta"] == 1.0, v
    # revert case
    rows2 = [{"item": f"u{i}", "pool": "odd", "axis": "toy", "expected": "A",
              "before": "A", "after": "A" if i < 6 else "B"} for i in range(10)]
    v2 = vote_from_rows(rows2)
    assert v2["vote"] == "REVERT", v2
    # abstain case: no unseen rows
    v3 = vote_from_rows([{"item": "s0", "pool": "even", "expected": "A",
                          "before": "A", "after": "A"}])
    assert v3["vote"] == "ABSTAIN", v3
    # unparseable extraction excluded
    v4 = vote_from_rows([{"item": "u0", "pool": "odd", "expected": "A",
                          "before": "", "after": "A"}])
    assert v4["vote"] == "ABSTAIN", v4
    print("verdict.py selftest: PASS (promote/revert/abstain/exclusion)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    ap = [a for a in sys.argv[1:] if not a.startswith("--")]
    rows = [json.loads(l) for l in Path(ap[0]).read_text().splitlines() if l.strip()]
    print(json.dumps(vote_from_rows(rows), indent=1))
