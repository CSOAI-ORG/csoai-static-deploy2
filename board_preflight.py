#!/usr/bin/env python3
"""board_preflight.py — a model that was never reached did not score zero.

═══════════════════════════════════════════════════════════════════════════════
THE ARTEFACT THIS EXISTS FOR
═══════════════════════════════════════════════════════════════════════════════
`benchmark-results/e2e_api_openrouter.json` records `meta-llama/llama-3.1-8b-instruct` at
**0.0% (0/57)**. It is not a score. All 57 rows carry an empty `pred_full`, and the mean
latency is **107 ms** (minimum 31 ms) — far too fast for generation and consistent with an auth
or quota error returning immediately. The comparison run on NVIDIA averaged **482 ms** with
populated predictions and scored 56.1%.

So an endpoint that answered nothing was written down as answering everything wrong, and that
0.0% would anchor the bottom of any leaderboard built from these files — looking, to a reader,
exactly like a real result about a real model.

The GovBench page already promises *"failed runs are recorded as absent, never as zero."* That
artefact breaks the promise. This module is the mechanism that keeps it.

═══════════════════════════════════════════════════════════════════════════════
THE RULE
═══════════════════════════════════════════════════════════════════════════════
Three outcomes per row, never two:

    ANSWERED     a substantive response came back — score it
    UNANSWERED   empty, whitespace, or a refusal-to-serve artefact — UNMEASURED, and it leaves
                 the denominator entirely
    DEGENERATE   a response arrived but carries no information (single token repeated, or the
                 same string returned for every distinct prompt) — UNMEASURED

DEGENERATE matters as much as UNANSWERED and is easier to miss: a corrupt model once emitted
`1\\n1\\n1` and topped two columns at 100%, because the grader only checked for the absence of
bad tokens. A provider returning a constant string would do the same thing to a board.

    python3 board_preflight.py            # audit every e2e_api_*.json, write corrected board
    python3 board_preflight.py --selftest
"""
from __future__ import annotations

import json, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"

ANSWERED, UNANSWERED, DEGENERATE = "answered", "unanswered", "degenerate"

# Providers return these instead of content when they decline to serve. They are transport
# failures wearing a response's clothes.
SERVICE_ERROR = re.compile(
    r"\b(rate.?limit|quota|unauthor|forbidden|invalid.?api.?key|payment required|"
    r"service unavailable|upstream error|model not found|insufficient)\b", re.I)

# A run this fast did not generate tokens. Not a hard rule on its own — used only to EXPLAIN
# a run that already failed on content, never to condemn one that produced real output.
IMPLAUSIBLE_MS = 150


def classify_row(text: str) -> str:
    """One row → one of three states. Content decides; latency only ever corroborates."""
    t = (text or "").strip()
    if not t:
        return UNANSWERED
    if SERVICE_ERROR.search(t) and len(t) < 240:
        return UNANSWERED
    words = re.findall(r"[A-Za-z]{2,}", t)
    if len(words) < 2:
        return DEGENERATE
    toks = t.split()
    if toks and max(Counter(toks).values()) > len(toks) * 0.6:
        return DEGENERATE
    return ANSWERED


def audit_run(path: Path) -> dict:
    """Audit one e2e_api_*.json. Returns a corrected summary per model."""
    d = json.loads(path.read_text())
    out = {"file": path.name, "models": {}}
    for model, blob in d.get("models", {}).items():
        rows = blob.get("results") or []
        if not rows:
            out["models"][model] = {"status": "UNMEASURED",
                                    "reason": "no per-item rows retained — score not recomputable"}
            continue
        states = [classify_row(r.get("pred_full") or r.get("pred") or "") for r in rows]
        c = Counter(states)
        answered = [r for r, s in zip(rows, states) if s == ANSWERED]
        lat = [r.get("lat", 0) for r in rows if isinstance(r.get("lat"), (int, float))]
        mean_lat = sum(lat) / len(lat) if lat else 0

        # TRUNCATION. A contiguous tail of unanswered rows means the RUN DIED, it does not
        # mean the model failed those items. Scoring the surviving prefix is not a sample: the
        # items run in fixed suite order, so the prefix is the early suites and the tail is
        # everything that never executed. Measured here: groq answered rows 1-24 then produced
        # a contiguous 32-row tail of nothing — every governance suite (sovereign_*, owem_*)
        # sits in that tail. An 87.5% on the prefix would describe the classic academic suites
        # only and would be published as if it described all 57.
        flags = [1 if st == ANSWERED else 0 for st in states]
        tail = len(flags) - len(''.join(map(str, flags)).rstrip('0'))
        if tail >= max(5, len(rows) * 0.2):
            out["models"][model] = {
                "status": "UNMEASURED",
                "reason": (f"run TRUNCATED — {tail} contiguous unanswered rows at the end of "
                           f"{len(rows)}. The run died; it did not fail those items."),
                "answered_prefix": int(sum(flags)),
                "mean_latency_ms": round(mean_lat),
                "why_prefix_is_not_a_sample": ("items execute in fixed suite order, so the "
                                               "surviving prefix is the early suites and the "
                                               "tail is what never ran — scoring it would "
                                               "report an easy subset as if it were the whole"),
                "previously_reported_pct": blob.get("summary", {}).get("pct"),
            }
            continue

        # A provider that answered NOTHING is unmeasured, whatever the grader said.
        if not answered:
            out["models"][model] = {
                "status": "UNMEASURED",
                "reason": (f"{c[UNANSWERED]} unanswered + {c[DEGENERATE]} degenerate of "
                           f"{len(rows)} — the endpoint returned no substantive output"),
                "mean_latency_ms": round(mean_lat),
                "latency_note": ("implausibly fast for generation — consistent with an "
                                 "immediate transport error" if mean_lat < IMPLAUSIBLE_MS else ""),
                "previously_reported_pct": blob.get("summary", {}).get("pct"),
            }
            continue

        # Otherwise: score ONLY the answered rows, and say how many left the denominator.
        correct = sum(1 for r in answered if r.get("ok"))
        n = len(answered)
        out["models"][model] = {
            "status": "MEASURED",
            "correct": correct, "scored_n": n,
            "pct": round(correct / n * 100, 1),
            "excluded_unmeasured": c[UNANSWERED] + c[DEGENERATE],
            "of_total": len(rows),
            "mean_latency_ms": round(mean_lat),
            "previously_reported_pct": blob.get("summary", {}).get("pct"),
            "coverage_caveat": (f"{c[UNANSWERED] + c[DEGENERATE]} of {len(rows)} items were not "
                                f"answered and are EXCLUDED from the denominator, not scored 0. "
                                f"This score describes {n} items, not {len(rows)}.")
            if (c[UNANSWERED] + c[DEGENERATE]) else "",
        }
    return out


def main() -> int:
    files = sorted(RESULTS.glob("e2e_api_*.json"))
    if not files:
        print("  no e2e_api_*.json found — nothing to audit"); return 2
    board, corrections = [], 0
    print("  BOARD PREFLIGHT — a model never reached did not score zero\n")
    for f in files:
        try:
            a = audit_run(f)
        except Exception as e:
            print(f"    {f.name}: UNREADABLE ({type(e).__name__})"); continue
        for model, m in a["models"].items():
            prev = m.get("previously_reported_pct")
            if m["status"] == "UNMEASURED":
                corrections += 1
                print(f"    ❌→⚠️  {model[:46]:46s} was {prev}%  →  UNMEASURED")
                print(f"            {m['reason']}")
                if m.get("latency_note"):
                    print(f"            mean latency {m['mean_latency_ms']}ms — {m['latency_note']}")
            else:
                changed = prev is not None and abs(prev - m["pct"]) > 0.05
                if changed: corrections += 1
                flag = "✏️ " if changed else "✅"
                print(f"    {flag} {model[:46]:46s} was {prev}%  →  {m['pct']}% "
                      f"on {m['scored_n']}/{m['of_total']} answered")
                if m.get("coverage_caveat"):
                    print(f"            {m['coverage_caveat']}")
            board.append({"file": f.name, "model": model, **m})

    measured = [b for b in board if b["status"] == "MEASURED"]
    print(f"\n  {len(measured)} measurable of {len(board)} entries · {corrections} corrected")
    if measured:
        lo, hi = min(b["pct"] for b in measured), max(b["pct"] for b in measured)
        print(f"  spread across measurable entries: {lo}% – {hi}%")
        print(f"  ⚠️  These are DIFFERENT PROVIDERS serving overlapping model families on the")
        print(f"      same 57 tasks. A spread here is a provider+model effect, not a model")
        print(f"      ranking, and must not be published as one.")

    p = RESULTS / "board_preflight.json"
    p.write_text(json.dumps(
        {"entries": board, "corrections": corrections,
         "rule": ("Three outcomes per row: answered / unanswered / degenerate. Unanswered and "
                  "degenerate rows leave the denominator entirely — they are never scored 0."),
         "caveat": ("Entries here come from different providers serving overlapping model "
                    "families. Cross-entry differences confound provider and model and are "
                    "not a model ranking.")}, indent=2))
    print(f"\n  -> {p}")
    return 0


def selftest() -> int:
    fails = []
    # The case that started this: empty output must never be ANSWERED.
    if classify_row("") != UNANSWERED: fails.append("empty string not UNANSWERED")
    if classify_row("   \n ") != UNANSWERED: fails.append("whitespace not UNANSWERED")
    # A transport error is not a wrong answer.
    if classify_row("Rate limit exceeded") != UNANSWERED: fails.append("rate-limit not UNANSWERED")
    if classify_row("Invalid API key provided") != UNANSWERED: fails.append("auth error not UNANSWERED")
    # The corrupt-model shape: a repeated token is not a response.
    if classify_row("1\n1\n1\n1\n1") != DEGENERATE: fails.append("repeated token not DEGENERATE")
    if classify_row("the the the the the the") != DEGENERATE: fails.append("token spam not DEGENERATE")
    # A real answer must survive, including a short correct one.
    if classify_row("B) ATP production") != ANSWERED: fails.append("real answer not ANSWERED")
    if classify_row("C) Canberra has been the capital since 1913.") != ANSWERED:
        fails.append("real sentence not ANSWERED")
    # A long text that merely MENTIONS a rate limit is a real answer about rate limits.
    long = ("A rate limit is a cap a provider places on requests per interval. " * 6)
    if classify_row(long) != ANSWERED: fails.append("long text mentioning rate-limit misclassified")

    # An all-unanswered run must come out UNMEASURED, never 0%.
    rows = [{"pred_full": "", "ok": False, "lat": 40} for _ in range(20)]
    r = audit_run_rows(rows)
    if r["status"] != "UNMEASURED": fails.append(f"all-empty run gave {r['status']}, not UNMEASURED")
    # A partly-answered run scores on the answered rows only.
    rows = ([{"pred_full": "B) real answer here", "ok": True, "lat": 500}] * 8 +
            [{"pred_full": "", "ok": False, "lat": 40}] * 2)
    r = audit_run_rows(rows)
    if r["status"] != "MEASURED": fails.append("partly-answered run not MEASURED")
    elif r["pct"] != 100.0 or r["scored_n"] != 8:
        fails.append(f"expected 100.0% on 8 answered, got {r.get('pct')}% on {r.get('scored_n')}")
    elif r["excluded_unmeasured"] != 2:
        fails.append("unanswered rows not excluded from the denominator")

    # TRUNCATION — the branch that flipped groq from a publishable 87.5% to UNMEASURED.
    rows = ([{"pred_full": "B) a real answer", "ok": True, "lat": 500}] * 24 +
            [{"pred_full": "", "ok": False, "lat": 0}] * 33)
    r = audit_run_rows(rows)
    if r["status"] != "UNMEASURED":
        fails.append(f"truncated run reported {r['status']}, not UNMEASURED")
    elif "TRUNCATED" not in r.get("reason", ""):
        fails.append("truncated run not named as truncated")

    # …but scattered misses are NOT truncation. A model that genuinely fails some items
    # mid-run must still be measurable, or the check would erase every imperfect run.
    rows = []
    for i in range(40):
        rows.append({"pred_full": "" if i % 5 == 0 else "B) a real answer",
                     "ok": i % 5 != 0, "lat": 500})
    r = audit_run_rows(rows)
    if r["status"] != "MEASURED":
        fails.append(f"scattered misses wrongly treated as truncation ({r.get('reason','')[:50]})")

    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 14/14' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


def audit_run_rows(rows: list[dict]) -> dict:
    """Thin wrapper so the selftest exercises the same path main() uses."""
    blob = {"models": {"x": {"results": rows, "summary": {"pct": 0.0}}}}
    p = RESULTS / "_selftest_tmp.json"
    p.write_text(json.dumps(blob))
    try:
        return audit_run(p)["models"]["x"]
    finally:
        p.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else main())
