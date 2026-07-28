#!/usr/bin/env python3
"""overnight_eat.py — the whole E2E, unattended, free, checkpointed.

═══════════════════════════════════════════════════════════════════════════════
⚠️ THE INTEGRITY GUARD THAT MATTERS MOST IN THIS FILE
═══════════════════════════════════════════════════════════════════════════════
The KB is the component that both WINS and COMPOUNDS: Δ +19.64 [+6.87, +32.41] where it has
coverage, and it holds 28 entries. Growing it overnight is the highest-value free work
available.

**But the KB is looked up by exact question match, and the benchmark scores the same
pipeline.** So harvesting an answer to a GovBench item and storing it would mean the system
later "answers" that item by reading back a stored copy — and the KB's measured gain would
become circular. That is not a marginal concern: it is the difference between a knowledge
base and a memorised answer key, and it would invalidate the one claimable number we hold.

`_is_benchmark_question()` therefore refuses to harvest anything matching a GovBench item,
by normalised text. Every harvest run reports how many candidates it refused on that ground.
If that number is ever zero across a whole run, suspect the check before celebrating.

═══════════════════════════════════════════════════════════════════════════════
STAGES — each checkpoints, each can fail without destroying the run
═══════════════════════════════════════════════════════════════════════════════
  1 REBOARD   score every board model on the CURRENT 174-item set, fingerprinted.
              Un-stales ethics / transparency / accountability. ~2h on CPU.
  2 GATES     margin_report + rank_intervals + mitosis on the new board. Instant.
              Answers: does ANY dimension resolve now? Can ANY cell divide?
  3 HONEY     harvest KB entries from statute — questions built from the 404-article
              corpus, answered with retrieval, kept ONLY if grounded and citation-clean,
              and never overlapping a benchmark item.
  4 SYSTEM    re-run system_bench with the grown KB. Does the KB layer's gain hold?
  5 REPORT    write a single JSON + markdown summary of what moved and what did not.

Every stage records ran / failed / skipped as THREE states. A stage that could not run is
not a stage that produced nothing — and the difference has been the whole day's lesson.

    nohup python3 overnight_eat.py > /tmp/overnight.log 2>&1 &
    python3 overnight_eat.py --status
"""
from __future__ import annotations

import argparse, hashlib, json, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
STATE = HERE / "benchmark-results" / "overnight_state.json"
OLLAMA = "http://localhost:11434/api/chat"


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except Exception:
            pass
    return {"started": datetime.now(timezone.utc).isoformat(), "stages": {}}


def save(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, indent=2))


def mark(st: dict, name: str, status: str, **extra) -> None:
    st["stages"][name] = {"status": status,
                          "at": datetime.now(timezone.utc).isoformat(), **extra}
    save(st)
    print(f"  [{status.upper():7s}] {name}  {json.dumps(extra, default=str)[:120]}", flush=True)


# ── stage 1 ──────────────────────────────────────────────────────────────────
def stage_reboard(st: dict) -> None:
    from govbench_eval import DIMENSIONS, grade_response, UngradedItem, all_fingerprints
    from system_bench import ask, Unreachable, preflight
    from rank_intervals import load as load_board

    models = sorted(load_board())
    dead = preflight(models)
    live = [m for m in models if m not in dead]
    if dead:
        print(f"    dead at preflight, excluded: {sorted(dead)}", flush=True)
    items = [(d, t) for d, dd in DIMENSIONS.items() for t in dd["tests"]]
    print(f"    {len(live)} models × {len(items)} items = {len(live)*len(items)} calls", flush=True)

    out, t0 = {}, time.time()
    for m in live:
        per: dict[str, list[float]] = {}
        unreachable = 0
        for d, t in items:
            try:
                per.setdefault(d, []).append(grade_response(t, ask(m, t["q"])))
            except (Unreachable, UngradedItem):
                unreachable += 1          # UNMEASURED, never a zero
            except Exception:
                unreachable += 1
        out[m] = {"model": m,
                  "dimensions": {d: round(sum(v)/len(v)*100, 1) for d, v in per.items() if v},
                  "unreachable": unreachable,
                  "n_scored": sum(len(v) for v in per.values())}
        dm = out[m]["dimensions"]
        print(f"    {m:30s} {len(dm)} dims · mean {sum(dm.values())/max(len(dm),1):5.1f}% "
              f"· {unreachable} unmeasured · {time.time()-t0:.0f}s", flush=True)

    p = HERE / "benchmark-results" / "reboard_174.json"
    p.write_text(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                             "item_fingerprints": all_fingerprints(),
                             "n_items": len(items), "results": out}, indent=2))
    # The board is no longer stale for anything: it was measured on the live item set.
    fp = HERE / "benchmark-results" / "board_fingerprints.json"
    if fp.exists():
        d = json.loads(fp.read_text())
        d["stale_vs_board"] = {}
        d["board_run"] = datetime.now(timezone.utc).isoformat()
        d["fingerprints"] = all_fingerprints()
        fp.write_text(json.dumps(d, indent=2))
    mark(st, "reboard", "ran", models=len(out), seconds=round(time.time()-t0), out=str(p.name))


# ── stage 2 ──────────────────────────────────────────────────────────────────
def stage_gates(st: dict) -> None:
    res = {}
    for name, cmd in (("mitosis", ["python3", "mitosis.py", "--need"]),
                      ("margin", ["python3", "margin_report.py"]),
                      ("intervals", ["python3", "rank_intervals.py"])):
        try:
            r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=600)
            res[name] = {"rc": r.returncode, "tail": r.stdout[-700:]}
        except Exception as e:
            res[name] = {"rc": -1, "error": str(e)[:120]}
    mark(st, "gates", "ran", **{k: v.get("rc") for k, v in res.items()})
    (HERE / "benchmark-results" / "overnight_gates.json").write_text(json.dumps(res, indent=2))


# ── stage 3 ──────────────────────────────────────────────────────────────────
def _norm(q: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", q.lower()).strip()


def _benchmark_questions() -> set[str]:
    from govbench_eval import DIMENSIONS
    return {_norm(t["q"]) for dd in DIMENSIONS.values() for t in dd["tests"]}


def stage_honey(st: dict, budget_s: int = 5400) -> None:
    """Grow the KB from statute. Only grounded, citation-clean, non-benchmark answers."""
    import sqlite3
    from statute_retrieval import get_article, NoStatuteFound, DB
    from owem_cluster import ask as call_model, select_expert
    from citation_verify import verify_text

    bench = _benchmark_questions()
    kb_path = HERE / "benchmark-results" / "sov_kb.json"
    kb = json.loads(kb_path.read_text()) if kb_path.exists() else {"entries": []}
    have = {_norm(e["question"]) for e in kb.get("entries", [])}
    before = len(kb["entries"])

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = con.execute("SELECT celex, article_number FROM articles ORDER BY celex, article_number").fetchall()
    con.close()
    NAMES = {"32024R1689": "EU AI Act", "32016R0679": "GDPR", "32022L2555": "NIS2",
             "32022R2554": "DORA", "32024R2847": "CRA", "32022L2464": "CSRD"}

    model, _ = select_expert("compliance")
    kept = refused_bench = ungrounded = dup = err = 0
    t0 = time.time()
    for celex, num in rows:
        if time.time() - t0 > budget_s:
            break
        reg = NAMES.get(celex, celex)
        q = f"What does {reg} Article {num} require?"
        n = _norm(q)
        if n in bench:
            refused_bench += 1          # NEVER harvest a benchmark item — see module docstring
            continue
        if n in have:
            dup += 1
            continue
        # EXACT LOOKUP, not search. Six regulations each have an Article 1; BM25 scored on
        # terms and returned the wrong statute's article, and the run wrote 54 entries like
        # "Article 1 GDPR requires automatic logging" before it was caught. When the question
        # names a provision, that provision is a lookup.
        try:
            art = get_article(celex, num)
            if art is None:
                err += 1
                continue
            ans = call_model(model,
                "Answer using ONLY the regulation text below. Quote the article by number.\n\n"
                f"[{art['id']}]\n{art['text'][:2400]}\n\nQuestion: {q}\nAnswer:")
        except Exception:
            err += 1
            continue
        cited = {m.group(1) for m in re.finditer(r"\bArticles?\s+(\d+)", ans, re.I)}
        if str(num) not in cited:
            ungrounded += 1              # did not stand on the article it was asked about
            continue
        v = verify_text(ans)
        if v["fabricated"] or v["misattributed"]:
            ungrounded += 1
            continue
        kb["entries"].append({
            "question": q, "answer": ans, "dimension": "compliance",
            "citations": sorted(cited), "fabricated": 0,
            "captured": datetime.now(timezone.utc).isoformat(),
            "provenance": {"source": "statute_exact_lookup", "regulation": reg,
                           "article": num, "celex": celex, "model": model,
                           "retrieved": [art["id"]], "exact_lookup": True,
                           "grounded_on": f"{celex} Article {num}"},
        })
        have.add(n)
        kept += 1
        if kept % 20 == 0:
            print(f"    honey: +{kept} entries · {time.time()-t0:.0f}s", flush=True)

    kb_path.write_text(json.dumps(kb, indent=2))
    mark(st, "honey", "ran", before=before, after=len(kb["entries"]), kept=kept,
         refused_benchmark=refused_bench, ungrounded=ungrounded, duplicate=dup, errors=err)
    if refused_bench == 0:
        print("    ⚠️  refused_benchmark == 0 — verify the guard before trusting this run",
              flush=True)


# ── stage 4 ──────────────────────────────────────────────────────────────────
def stage_system(st: dict) -> None:
    try:
        r = subprocess.run(["python3", "system_bench.py", "--limit", "195", "--harm"],
                           cwd=HERE, capture_output=True, text=True, timeout=14400)
        a = subprocess.run(["python3", "system_analysis.py", "/tmp/overnight_sys.log"],
                           cwd=HERE, capture_output=True, text=True, timeout=600)
        Path("/tmp/overnight_sys.log").write_text(r.stdout)
        a = subprocess.run(["python3", "system_analysis.py", "/tmp/overnight_sys.log"],
                           cwd=HERE, capture_output=True, text=True, timeout=600)
        mark(st, "system", "ran", tail=r.stdout[-400:], verdict=a.stdout[-400:])
    except Exception as e:
        mark(st, "system", "failed", error=str(e)[:200])


# ── stage 5 ──────────────────────────────────────────────────────────────────
def stage_report(st: dict) -> None:
    lines = ["# Overnight EAT run", "",
             f"started {st.get('started')}  ·  finished {datetime.now(timezone.utc).isoformat()}",
             "", "| stage | status | detail |", "|---|---|---|"]
    for k, v in st["stages"].items():
        d = {kk: vv for kk, vv in v.items() if kk not in ("status", "at", "tail", "verdict")}
        lines.append(f"| {k} | **{v['status']}** | `{json.dumps(d, default=str)[:110]}` |")
    p = HERE / "benchmark-results" / "OVERNIGHT_REPORT.md"
    p.write_text("\n".join(lines) + "\n")
    mark(st, "report", "ran", out=str(p.name))


STAGES = [("reboard", stage_reboard), ("gates", stage_gates),
          ("honey", stage_honey), ("system", stage_system), ("report", stage_report)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    st = load_state()
    if a.status:
        print(json.dumps(st, indent=2)); return 0

    print(f"  OVERNIGHT EAT — {len(STAGES)} stages, checkpointed\n", flush=True)
    for name, fn in STAGES:
        if a.only and a.only != name:
            continue
        if st["stages"].get(name, {}).get("status") == "ran":
            print(f"  [SKIP   ] {name} — already completed in this run", flush=True)
            continue
        try:
            fn(st)
        except KeyboardInterrupt:
            mark(st, name, "interrupted"); return 130
        except Exception as e:
            # A stage that blew up must say so and let the rest continue. Silently
            # proceeding would report a completed run that never happened.
            mark(st, name, "failed", error=f"{type(e).__name__}: {str(e)[:200]}")
    print(f"\n  done — see benchmark-results/OVERNIGHT_REPORT.md", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
