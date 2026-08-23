#!/usr/bin/env python3
"""kb_distil.py — distil each clan's knowledge into SOV-space as retrievable KB, not weights.

═══════════════════════════════════════════════════════════════════════════════
THE ARITHMETIC THAT MAKES THIS THE RIGHT MOVE
═══════════════════════════════════════════════════════════════════════════════
    one expert (prompt over shared blob)   16 KB
    one base blob                         397 MB   ← paid once
    one KB entry (Q + best answer + prov)  ~1 KB
    retrieval faithfulness (measured)      91.7%   base AND wrapper

So a clan's USEFUL OUTPUT is ~1 KB per answer, against 397 MB for the weights that produced it.
Distilling 400 answers costs less than 0.5 MB — the same disk as 25 experts, holding knowledge
no expert can be relied on to recall.

**And today measured exactly why that matters:** 0 of 7 experts knew which article prohibits
social scoring. All 7 answered confidently and all 7 were wrong. The same models score **91.7%
on retrieval faithfulness** — they cannot recall, but they can read.

> **Storing the ANSWER beats storing the model that sometimes produces it.**

═══════════════════════════════════════════════════════════════════════════════
WHAT IS AND IS NOT STORED — the honest filter
═══════════════════════════════════════════════════════════════════════════════
An entry is kept ONLY if the clan's answer beat the cluster's current best on that dimension.
A worse answer is not knowledge; storing it would dilute retrieval and quietly lower quality —
the same reason honey_harvest only takes wins.

Every entry carries: source clan · hive · dimension · score-at-capture · cluster-best-at-capture
· sha256 · timestamp. So "where did this come from and what did it beat" is always answerable,
and an entry whose source is later found broken can be traced and pulled.

⚠️ **A KB entry is a MODEL'S ANSWER, not a verified fact.** It is generated text with
provenance, and provenance is not truth. Entries touching citations should be run through
`citation_verify.py` before they are trusted — today a top-board model miscited Article 5 six
times in one answer, and that answer would have looked like perfectly good honey.

    python3 kb_distil.py --hive SOVEREIGNTY --limit 4
    python3 kb_distil.py --status
"""
from __future__ import annotations

import argparse, hashlib, json, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
KB = HERE / "benchmark-results" / "sov_kb.json"
OLLAMA = "http://localhost:11434/api/chat"


def load() -> dict:
    if KB.exists():
        try:
            return json.loads(KB.read_text())
        except Exception:
            pass
    return {"entries": [], "created": datetime.now(timezone.utc).isoformat()}


def ask(model: str, prompt: str, timeout: int = 300) -> str:
    body = json.dumps({"model": model, "stream": False,
                       "options": {"temperature": 0, "num_predict": 220},
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())["message"]["content"].strip()


def distil(hive: str, limit: int = 4, dry: bool = False) -> None:
    from govbench_eval import DIMENSIONS, grade_response, UnreachableModel
    from master_hives import HIVES, hive_table
    from owem_cluster import build_expert_table

    if hive not in HIVES:
        print(f"  unknown hive {hive}"); return
    table, _ = build_expert_table()
    ledger = json.loads((HERE / "benchmark-results" / "clan_ledger.json").read_text())
    clans = [c["name"] for c in ledger["clans"] if c["hive"] == hive][:limit]
    dims = [d for d in HIVES[hive]["dimensions"] if d in DIMENSIONS]

    kb = load()
    seen = {e["sha256"] for e in kb["entries"]}
    kept = dropped = errors = 0

    print(f"  {HIVES[hive]['icon']} {hive} — distilling {len(clans)} clans x {len(dims)} dimensions\n")
    # 2026-07-28 — EIGHTH instance of absent-treated-as-zero. `table.get(dim, {}).get("score", 0.0)`
    # returned 0.0 for a dimension that was never BENCHMARKED, so every answer trivially "beat the
    # cluster" and 26 of 54 entries were artifacts rather than wins. An unmeasured baseline is not
    # a baseline of zero; there is simply nothing to beat yet.
    unmeasured = [d for d in dims if d not in table]
    if unmeasured:
        print(f"    ⏭️  skipping {len(unmeasured)} UNBENCHMARKED dimension(s): {', '.join(unmeasured)}")
        print(f"       No cluster baseline exists, so 'beat the cluster' is undefined — not zero.")
        print(f"       Benchmark them first, then distil.\n")
        dims = [d for d in dims if d in table]

    for clan in clans:
        for dim in dims:
            best = table[dim]["score"]
            for test in DIMENSIONS[dim]["tests"]:
                q = test["q"]
                try:
                    a = ask(clan, q)
                except Exception as e:
                    errors += 1
                    continue
                try:
                    score = grade_response(test, a) * 100
                except UnreachableModel:
                    errors += 1
                    continue
                except Exception:
                    continue
                # KEEP ONLY WINS. A worse answer is not knowledge.
                if score <= best:
                    dropped += 1
                    continue
                h = hashlib.sha256((q + a).encode()).hexdigest()
                if h in seen:
                    dropped += 1
                    continue
                seen.add(h)
                kept += 1
                print(f"    📚 {dim:22s} +{score-best:5.1f}  ({score:.0f} vs {best:.0f})  {clan}")
                if not dry:
                    kb["entries"].append({
                        "question": q, "answer": a[:1400], "dimension": dim, "hive": hive,
                        "source_clan": clan, "score_at_capture": round(score, 1),
                        "cluster_best_at_capture": round(best, 1),
                        "delta": round(score - best, 1), "sha256": h,
                        "captured": datetime.now(timezone.utc).isoformat(),
                        "verified": False,   # citation_verify has NOT run on this yet
                    })
    if not dry:
        KB.parent.mkdir(parents=True, exist_ok=True)
        _tmp = KB.with_suffix(".json.tmp")
        _tmp.write_text(json.dumps(kb, indent=2))
        _tmp.replace(KB)  # atomic — concurrent writers can't concatenate
    size = KB.stat().st_size / 1024 if KB.exists() else 0
    print(f"\n  kept {kept} · dropped {dropped} (no better than cluster) · errors {errors}")
    print(f"  KB now {len(kb['entries'])} entries, {size:.0f} KB")
    if kept:
        print(f"  ~{size/max(1,len(kb['entries'])):.1f} KB per entry vs 397 MB for the weights.")


def status() -> None:
    kb = load()
    e = kb["entries"]
    size = KB.stat().st_size / 1024 if KB.exists() else 0
    print(f"  SOV-SPACE KB — {len(e)} entries, {size:.0f} KB\n")
    if not e:
        print("    empty. Run --hive <NAME> to distil."); return
    from collections import Counter
    for label, key in [("by hive", "hive"), ("by dimension", "dimension")]:
        c = Counter(x[key] for x in e)
        print(f"    {label}:")
        for k, n in c.most_common(8):
            avg = sum(x["delta"] for x in e if x[key] == k) / n
            print(f"      {k:24s} {n:4d} entries · avg +{avg:.1f} over cluster best")
    unver = sum(1 for x in e if not x.get("verified"))
    print(f"\n    ⚠️  {unver}/{len(e)} entries NOT citation-verified.")
    print(f"       A KB entry is a model's ANSWER, not a verified fact. Provenance is not truth.")
    print(f"       Run citation_verify.py over entries before relying on any citation in them.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hive")
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    if a.hive:
        distil(a.hive, a.limit, a.dry)
    else:
        status()
