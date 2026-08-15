#!/usr/bin/env python3
"""aggregate_greenfield_eat.py — combine the three E2E artefacts into one SIGIL-signed report:

  1. greenfield_e2e/leaderboard.json     — 8 dated-2026-07-28 GovBench greenfield dims × N models
  2. eat_govbench/eat_local_*.json       — EAT weak-dim baseline vs RAG on 5 weak governance dims
  3. flywheel/YYYY-MM-DD.json            — Flywheel daily (practice/held-out split + tokens/correct)

Output: benchmark-results/greenfield_eat_combined/greenfield_eat_e2e_<date>.json
"""
from __future__ import annotations
import hashlib, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"
OUT_DIR = RESULTS / "greenfield_eat_combined"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def sigil(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


def load_greenfield() -> dict | None:
    fp = RESULTS / "greenfield_e2e" / "leaderboard.json"
    if not fp.exists():
        return None
    return json.loads(fp.read_text())


def load_eat_weak() -> list[dict]:
    out = []
    for fp in sorted((RESULTS / "eat_govbench").glob("eat_local_*.json")):
        try:
            out.append(json.loads(fp.read_text()))
        except Exception:
            continue
    return out


def load_flywheel_daily() -> dict | None:
    fp = RESULTS / "flywheel" / f"{datetime.now().strftime('%Y-%m-%d')}.json"
    if not fp.exists():
        # fallback to latest
        files = sorted((RESULTS / "flywheel").glob("*.json"), reverse=True)
        if not files:
            return None
        fp = files[0]
    try:
        return json.loads(fp.read_text())
    except Exception:
        return None


def main() -> int:
    g = load_greenfield()
    e = load_eat_weak()
    f = load_flywheel_daily()

    if not (g or e or f):
        print("  ⛔ Nothing to aggregate — no artefacts found.")
        return 2

    day = datetime.now().strftime("%Y-%m-%d")
    sig_payload = {
        "day": day,
        "greenfield_models": sorted([r["model"] for r in g]) if g else [],
        "eat_models": sorted([x["model"] for x in e]),
        "flywheel_day": f.get("day") if f else None,
    }
    s = sigil(sig_payload)

    # 1 — greenfield summary
    greenfield_summary = None
    if g:
        rows = []
        for r in sorted(g, key=lambda x: -x["overall_pct"]):
            rows.append({
                "model": r["model"],
                "overall_pct": r["overall_pct"],
                "n_dims": r["n_dims"],
                "dim_scores": {k: v["score_pct"] for k, v in r["dimensions"].items()},
            })
        greenfield_summary = {
            "n_dims": g[0]["n_dims"],
            "dims": g[0]["greenfield_dims"],
            "models": rows,
        }

    # 2 — EAT weak-dim summary
    eat_summary = []
    for x in e:
        dims = x.get("dimensions", {})
        eat_summary.append({
            "model": x["model"],
            "avg_baseline": x.get("avg_baseline"),
            "avg_context": x.get("avg_context"),
            "rag_lift": (round(x["avg_context"] - x["avg_baseline"], 2)
                         if x.get("avg_context") is not None and x.get("avg_baseline") is not None
                         else None),
            "per_dim": {k: {"baseline": v["baseline"], "context": v["context"],
                             "lift": v["improvement"]}
                        for k, v in dims.items()},
        })

    # 3 — Flywheel daily summary
    fly_summary = None
    if f:
        fly_summary = {
            "day": f.get("day"),
            "law": f.get("law"),
            "models": {m: {
                "practice_acc": s["practice"]["accuracy"],
                "held_out_acc": s["held_out"]["accuracy"],
                "overfit_gap": s["overfit_gap"],
                "tokens_per_correct_practice": s["practice"]["tokens_per_correct"],
                "tokens_per_correct_held_out": s["held_out"]["tokens_per_correct"],
            } for m, s in f["summary"]["models"].items()},
            "fuel_pairs": f["fuel"]["pairs"],
            "fuel_kb_rows": f["fuel"]["kb"],
            "fuel_path": f["fuel"]["pairs_file"],
        }

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "day": day,
        "sigil": s,
        "greenfield_e2e": greenfield_summary,
        "eat_weak_dim": eat_summary,
        "flywheel_daily": fly_summary,
    }

    out = OUT_DIR / f"greenfield_eat_e2e_{day}.json"
    out.write_text(json.dumps(report, indent=2))

    print("=" * 78)
    print(f"  GREENFIELD + EAT + FLYWHEEL — COMBINED E2E REPORT  {day}")
    print("=" * 78)
    print(f"  SIGIL: {s[:32]}...")

    if greenfield_summary:
        print(f"\n  ▸ GovBench greenfield E2E — {greenfield_summary['n_dims']} dims")
        print(f"    {'model':40s} {'overall':>8s}")
        for r in greenfield_summary["models"]:
            print(f"    {r['model']:40s} {r['overall_pct']:7.1f}%")

    if eat_summary:
        print(f"\n  ▸ EAT weak-dim (baseline → RAG context)")
        print(f"    {'model':40s} {'base':>6s} {'ctx':>6s} {'lift':>7s}")
        for r in sorted(eat_summary, key=lambda x: -(x["avg_context"] or 0)):
            print(f"    {r['model']:40s} {r['avg_baseline']:5.1f}% "
                  f"{r['avg_context']:5.1f}% {r['rag_lift']:+6.1f}pp")

    if fly_summary:
        print(f"\n  ▸ Flywheel daily ({fly_summary['day']}) — practice vs held-out")
        def f3(v): return f"{v:.3f}" if v is not None else "  n/a"
        def fgap(v): return f"{v:+.3f}" if v is not None else "  n/a"
        for m, s in fly_summary["models"].items():
            print(f"    {m:40s} prac={f3(s['practice_acc'])}  "
                  f"held={f3(s['held_out_acc'])}  "
                  f"gap={fgap(s['overfit_gap'])}  "
                  f"tok/correct(prac)={s['tokens_per_correct_practice']}")
        print(f"    fuel: {fly_summary['fuel_pairs']} pairs, "
              f"{fly_summary['fuel_kb_rows']} KB rows → {fly_summary['fuel_path']}")

    print(f"\n  → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())