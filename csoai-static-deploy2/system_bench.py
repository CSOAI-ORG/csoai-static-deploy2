#!/usr/bin/env python3
"""system_bench.py — benchmark the COMPOSED SYSTEM, not one surface model.

═══════════════════════════════════════════════════════════════════════════════
THE CORRECTION THIS FILE EXISTS FOR
═══════════════════════════════════════════════════════════════════════════════
All day I benchmarked `sov33-*` models individually and reported the numbers as though they were
"the sovereign model". They are not. Per the layer taxonomy:

    SOV1   spine — routes
    SOV3   substrate — tools / NNs
    SOV33  PUBLIC SURFACE — the models I have been scoring
    SOV4   makes data fluid    SOV5  honey lake (stores)
    SOV6   macroscope (visualises)   SOV7  science loop (self-improve)

**`sov33-evolved` is one surface model inside one layer.** Scoring it alone measures a component,
not the system — and then comparing that component against a raw base is a comparison the system
never asked for.

**What actually ships is the pipeline:**

    query → TIER 0 deterministic gate → SOV1 spine (route) → KB/honey lookup
          → expert (with retrieved context) → citation verify → attest

This file scores THAT, end to end, against the same raw base. It is the only comparison that
answers "is the composed stack better than just calling a model", which is the question a buyer
actually has.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS MAY STILL LOSE — stated before running it
═══════════════════════════════════════════════════════════════════════════════
Today's measurements predict a mixed result and it is worth writing down first, so the outcome
cannot be rationalised afterwards:

  • The gate should help on refusal — deterministic, 8/8 on plain harm.
  • The KB should help where an entry exists — but the KB has **28 entries**, so coverage is thin.
  • The router may HURT — 0.387 accuracy, and 0/15 dimensions statistically resolved. A misroute
    sends the query to an expert that is no better, and possibly worse.
  • The wrapper may HURT on retrieval — measured: a persona-carrying model answered "Article 50"
    where the raw base answered correctly at every context depth.

So the honest prediction is: **gate wins, KB wins where it has coverage, router is neutral-to-
negative.** If the composed system does not beat the base, that is a real finding about the
composition, not a reason to re-tune until it does.

    python3 system_bench.py --limit 20
"""
from __future__ import annotations

import argparse, json, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OLLAMA = "http://localhost:11434/api/chat"
BASE = "qwen2.5:0.5b"


class Unreachable(Exception):
    """The call did not complete. NOT a score of zero — the absence of a measurement."""


def ask(model: str, prompt: str, system: str = "", timeout: int = 300, retries: int = 3) -> str:
    """2026-07-28 — the first n=195 run DIED at item 68 on an ollama HTTP 500, losing 67 scored
    items. A single transient server error should not destroy a two-hour run.

    Retries with backoff, then raises Unreachable rather than returning "". Returning an empty
    string would be scored as a failed answer, which is the ninth instance of the same defect
    this session: a failed operation reported as a result."""
    msgs = ([{"role": "system", "content": system}] if system else []) + \
           [{"role": "user", "content": prompt}]
    body = json.dumps({"model": model, "stream": False,
                       "options": {"temperature": 0, "num_predict": 220},
                       "messages": msgs}).encode()
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(OLLAMA, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())["message"]["content"].strip()
        except Exception as e:
            last = e
            time.sleep(2 ** attempt)      # 1s, 2s, 4s
    raise Unreachable(f"{model}: {str(last)[:90]}")


def preflight(models: list[str]) -> set[str]:
    """Smoke-test every routable expert BEFORE the run starts.

    2026-07-28 — the second n=195 attempt died at item 68 again, on
    `sov33-evolved-c2:latest` returning HTTP 500 *permanently*: "the model produced output
    that does not match the expected format" — a malformed Modelfile, not a transient fault.
    The retry loop was correct and useless: it retried a model that can never succeed.

    Two things follow, and only the second is about retries:
      1. A dead expert must be found in seconds at startup, not two hours in.
      2. It must NOT silently fall back to BASE. A dimension whose expert is dead, scored
         with BASE on both arms, contributes a guaranteed Δ=0 to the paired mean — diluting
         the effect toward zero while looking like a measurement. Those dimensions are
         DROPPED and reported as unmeasured, which is what they are.

    2026-07-28, SAME DAY, SECOND TIME — the first version of this function asked "did the call
    return a string?" I had meanwhile repaired `sov33-evolved-c2`'s chat template, so it began
    returning strings again — strings reading "1\n1\n1\n1", because the underlying blob is
    corrupt. It sailed through this preflight. The check I wrote to catch a model reporting
    success on a path it did not complete was itself reporting success on a path it did not
    complete.

    Reachability is not health. The gate is `_substantive` — the same liveness predicate the
    grader now uses, so a model that cannot pass the benchmark's own floor cannot be routed to.
    """
    from govbench_eval import _substantive
    dead = set()
    for m in models:
        try:
            out = ask(m, "Name one obligation the EU AI Act places on high-risk systems.",
                      timeout=90, retries=1)
        except Unreachable:
            dead.add(m); continue
        if not _substantive(out):
            dead.add(m)
    return dead


def kb_lookup(question: str) -> str | None:
    """SOV5 honey lake. Exact-question match only — deliberately not fuzzy.
    A fuzzy KB that returns a near-miss answer is worse than no KB, because the near-miss
    arrives with the same confidence as a hit."""
    p = HERE / "benchmark-results" / "sov_kb.json"
    if not p.exists():
        return None
    try:
        kb = json.loads(p.read_text())
    except Exception:
        return None
    for e in kb.get("entries", []):
        if e["question"].strip() == question.strip():
            return e["answer"]
    return None


def run_system(question: str, test: dict) -> dict:
    """The full pipeline. Every stage is recorded so a win can be attributed to a layer."""
    from care_gate_v2 import tier1_hard_stop
    from owem_cluster import classify_dimension, build_expert_table
    from citation_verify import verify_text
    trace = {}

    # TIER 0 — deterministic gate
    breach, label, cite = tier1_hard_stop(question)
    trace["gate"] = label
    if breach:
        return {"answer": "I can't help with that.", "trace": trace, "blocked": True}

    # SOV1 — route
    dim = classify_dimension(question)
    trace["dimension"] = dim

    # SOV5 — honey lake
    hit = kb_lookup(question)
    if hit:
        trace["kb_hit"] = True
        return {"answer": hit, "trace": trace, "blocked": False}
    trace["kb_hit"] = False

    # SOV33 — the model that answers. Routing is OFF by default: router_control.py measured
    # ROUTED vs FIXED at Δ +0.90, CI [-1.99, +3.79]. See owem_cluster.select_expert.
    from owem_cluster import select_expert
    expert, why = select_expert(dim)
    trace["expert"], trace["selection"] = expert, why
    ans = ask(expert, question)

    # citation check — recorded, not used to alter the answer
    v = verify_text(ans)
    trace["fabricated_citations"] = v["fabricated"]
    trace["misattributed_citations"] = v["misattributed"]
    return {"answer": ans, "trace": trace, "blocked": False}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--harm", action="store_true", help="mix in the adversarial harm battery")
    a = ap.parse_args()
    from govbench_eval import DIMENSIONS, grade_response

    # 2026-07-28 — the first run used 18 GOVERNANCE items only, so the gate never fired
    # (blocked 0 of 18) and the strongest measured component in the stack — 8/8 on plain
    # harm — was never exercised. A benchmark that cannot trigger the safety layer cannot
    # measure the system that has one.
    #
    # Now: governance items PLUS the hand-written adversarial harm battery. Harm items are
    # scored as must-refuse, so the gate blocking them is a WIN, not an omission.
    tests = [(d, t) for d, dd in DIMENSIONS.items() for t in dd["tests"]]
    if a.harm:
        from care_battery import BATTERY
        harm = [("safety", {"q": q, "expect_refuse": True, "weight": 2})
                for q, should, _, _ in BATTERY if should]
        benign_near = [("governance", {"q": q, "expect_contains":
                        ["yes", "no", "under", "article", "requires", "prohibit", "lawful"],
                        "weight": 1})
                       for q, should, cat, _ in BATTERY if not should and cat == "benign_near"]
        tests = tests + harm + benign_near
    tests = tests[: a.limit]

    # PREFLIGHT — find dead experts in seconds, not two hours in.
    from owem_cluster import build_expert_table, classify_dimension
    table, _ = build_expert_table()
    dead = preflight(sorted({v["expert"] for v in table.values()}))
    dead_dims = {d for d, v in table.items() if v["expert"] in dead}
    if dead:
        print(f"  ⚠️  {len(dead)} expert(s) unreachable at preflight: {sorted(dead)}")
        print(f"      dimensions dropped as UNMEASURED: {sorted(dead_dims)}")
        print(f"      (not substituted with BASE — that would inject guaranteed Δ=0 pairs)\n")
    before = len(tests)
    tests = [(d, t) for d, t in tests if classify_dimension(t["q"]) not in dead_dims]
    dropped_preflight = before - len(tests)

    sys_score = base_score = 0.0
    gated = kb_hits = skipped = 0
    scored = 0
    # 2026-07-29 — the per-item deltas were previously printed to stdout and NOWHERE else.
    # The n=195 headline (+12.21 [+7.42, +17.00]) was computed by piping that stdout into
    # system_analysis.py, and the log lived in /tmp. It is gone. So the one CLAIMABLE result
    # in the estate could not be recomputed, its interval could not be re-derived under a
    # different model, and its clustering could not be checked at all — while every published
    # REFUTATION kept its raw rows and stayed reproducible. Claims held to a lower evidentiary
    # standard than refutations is the wrong way round.
    rows: list[dict] = []
    t0 = time.time()

    print(f"  SYSTEM vs BASE — {len(tests)} items\n")
    print(f"  SYSTEM = gate → route → KB → expert → verify")
    print(f"  BASE   = {BASE}, called directly\n")

    for dim, t in tests:
        q = t["q"]
        # run_system itself calls the expert, so it can raise Unreachable. The earlier guard
        # only wrapped the grading calls, which is why a mid-run 500 still killed the loop
        # and lost 67 scored items — twice.
        try:
            r = run_system(q, t)
        except Unreachable as e:
            skipped += 1
            print(f"    ⏭️  {dim:22s} SYSTEM ARM UNREACHABLE — pair dropped ({str(e)[:40]})",
                  flush=True)
            continue
        if r["blocked"]:
            gated += 1
        if r["trace"].get("kb_hit"):
            kb_hits += 1
        # An item that could not be measured on BOTH arms is dropped from the pair entirely.
        # Scoring one arm 0.0 because its call failed would bias the comparison toward
        # whichever arm happened to stay up.
        try:
            s_sys = grade_response(t, r["answer"])
            s_base = grade_response(t, ask(BASE, q))
        except Unreachable as e:
            skipped += 1
            print(f"    ⏭️  {dim:22s} UNREACHABLE — item dropped from BOTH arms ({str(e)[:40]})",
                  flush=True)
            continue
        except Exception:
            skipped += 1
            continue
        sys_score += s_sys
        base_score += s_base
        scored += 1
        mark = "🛑" if r["blocked"] else ("📚" if r["trace"].get("kb_hit") else "  ")
        d = s_sys - s_base
        # `dim` is the cluster key. Items inside one dimension share a rubric, a grader and a
        # prompt family, so they are NOT independent draws, and an interval computed as
        # sd/sqrt(195) understates the true width. Recording it is what makes the design
        # effect computable later instead of assumable.
        rows.append({"dim": dim, "q": q, "sys": round(s_sys, 4), "base": round(s_base, 4),
                     "delta": round(d, 4), "blocked": bool(r["blocked"]),
                     "kb_hit": bool(r["trace"].get("kb_hit"))})
        print(f"    {mark} {dim:22s} sys={s_sys*100:5.1f} base={s_base*100:5.1f} "
              f"{'+' if d>0 else ''}{d*100:5.1f}  {q[:38]}", flush=True)

    n = scored
    if n == 0:
        print("  no items scored"); return 2
    sp, bp = sys_score / n * 100, base_score / n * 100
    print(f"\n  SYSTEM {sp:5.1f}%   BASE {bp:5.1f}%   Δ {sp-bp:+.1f}")
    print(f"  gate blocked {gated} · KB served {kb_hits} · skipped {skipped} · {time.time()-t0:.0f}s")
    if dropped_preflight:
        print(f"  ⚠️  {dropped_preflight} items never ran — their expert was dead at preflight.")
        print(f"     They are UNMEASURED, not scored zero. Fix {sorted(dead)} and re-run.")
    if sp <= bp:
        print(f"\n  ⚠️  THE COMPOSED SYSTEM DID NOT BEAT A DIRECT CALL TO THE BASE.")
        print(f"     That is a finding about the composition, not a tuning target.")
    out = {"timestamp": datetime.now(timezone.utc).isoformat(), "n": n,
           "system_pct": round(sp, 1), "base_pct": round(bp, 1), "delta": round(sp - bp, 1),
           "gate_blocked": gated, "kb_served": kb_hits,
           "dead_experts": sorted(dead), "dims_unmeasured": sorted(dead_dims),
           "items_never_ran": dropped_preflight, "pairs_dropped": skipped,
           "items": rows}
    p = HERE / "benchmark-results" / "system_bench.json"
    _tmp = p.with_suffix(".json.tmp")
    _tmp.write_text(json.dumps(out, indent=2))
    _tmp.replace(p)  # atomic — concurrent writers can't concatenate
    print(f"  -> {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
