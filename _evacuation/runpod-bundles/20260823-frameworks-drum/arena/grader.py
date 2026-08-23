#!/usr/bin/env python3
"""Deterministic grader for the measured arena (NEXT-100 P2, step 22).

Grades OBJECTIVE arena tasks deterministically — no LLM-as-judge for objective work. Supports:
  - multiple-choice (single/multi label, exact match after mirroring the answer letter)
  - numeric (float with tolerance)
  - yes/no (boolean)
  - exact string match (normalized)
Returns a per-item grade {correct: bool, score: float}. Honest: a task that isn't objectively
gradeable returns the UNGRADEABLE marker (so it's routed to the LLM-adjacent/ human-audit path,
never silently mixed with measured numbers). Stdlib-only.

Run: python3 arena/grader.py --selftest
"""
import re
import sys

UNGRADEABLE = {"correct": None, "score": None, "ungradeable": True}


def norm_text(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def grade_mc(answer, gold, multi=False):
    """Multi-choice: gold is a set of accepted labels (e.g. {'A','C'}). Mirror the answer's letter."""
    ans = re.search(r"\b([A-Z])\b", (answer or "").upper())
    if not ans:
        return UNGRADEABLE
    letter = ans.group(1)
    if not multi:
        return {"correct": letter in {g.upper()[:1] for g in gold}, "score": 1.0 if letter in {g.upper()[:1] for g in gold} else 0.0}
    letters = set(re.findall(r"\b([A-Z])\b", (answer or "").upper()))
    goldl = {g.upper()[:1] for g in gold}
    return {"correct": letters == goldl, "score": 1.0 if letters == goldl else 0.0}


def grade_numeric(answer, gold, tol=1e-6):
    m = re.search(r"[-+]?\d*\.?\d+", (answer or "").replace(",", ""))
    if not m:
        return UNGRADEABLE
    try:
        val = float(m.group(0))
    except ValueError:
        return UNGRADEABLE
    return {"correct": abs(val - float(gold)) <= tol, "score": 1.0 if abs(val - float(gold)) <= tol else 0.0}


def grade_bool(answer, gold):
    ans = (answer or "").strip().lower()
    if ans not in ("yes", "no", "true", "false", "y", "n"):
        return UNGRADEABLE
    val = ans in ("yes", "true", "y")
    return {"correct": val == bool(gold), "score": 1.0 if val == bool(gold) else 0.0}


def grade_exact(answer, gold):
    if norm_text(answer) == norm_text(gold):
        return {"correct": True, "score": 1.0}
    return {"correct": False, "score": 0.0}


def grade(item):
    """item: {answer, gold, kind ('mc'|'num'|'bool'|'exact'), tol?}. Returns a grade dict."""
    kind = item.get("kind", "exact")
    if kind == "mc":
        return grade_mc(item.get("answer"), item.get("gold"), multi=item.get("multi", False))
    if kind == "num":
        return grade_numeric(item.get("answer"), item.get("gold"), item.get("tol", 1e-6))
    if kind == "bool":
        return grade_bool(item.get("answer"), item.get("gold"))
    if kind == "exact":
        return grade_exact(item.get("answer"), item.get("gold"))
    return UNGRADEABLE


def selftest():
    # multiple-choice: mirrors the letter, matches gold
    assert grade({"answer": "The answer is A", "gold": {"A"}, "kind": "mc"})["correct"] is True
    assert grade({"answer": "C", "gold": {"A"}, "kind": "mc"})["correct"] is False
    # multi-select: all letters must match
    assert grade({"answer": "A and C", "gold": {"A", "C"}, "kind": "mc", "multi": True})["correct"] is True
    # numeric with tolerance
    assert grade({"answer": "12345.67", "gold": 12345.67, "kind": "num"})["correct"] is True
    assert grade({"answer": "about 42", "gold": 42.5, "kind": "num", "tol": 1.0})["correct"] is True
    # boolean
    assert grade({"answer": "YES", "gold": True, "kind": "bool"})["correct"] is True
    assert grade({"answer": "no", "gold": False, "kind": "bool"})["correct"] is True
    # exact (normalized)
    assert grade({"answer": "  Acme Corp. ", "gold": "acme corp", "kind": "exact"})["correct"] is True
    # ungradeable funneled honestly (never a fake score)
    assert grade({"answer": "not sure", "gold": {"A"}, "kind": "mc"})["ungradeable"] is True
    print("arena grader: PASS (mc/numeric/bool/exact + honest ungradeable funnel)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("usage: python3 arena/grader.py --selftest")
    sys.exit(1)
