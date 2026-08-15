#!/usr/bin/env python3
"""margin_report.py — is a per-dimension winner real, or one test item away from flipping?

The check that retracted our headline on 2026-07-28. Across 15 dimensions and 11 models,
**14 of 15 winners were decided by a margin smaller than one test item**, and four were exactly
tied. Taking a max over noisy per-dimension scores reliably produces a number above any
individual — that is what a max does, not evidence of complementary expertise.

    a winner is credible only if   margin > 100 / n_items

Run this after every benchmark expansion. A dimension that does not pass may not be cited, and
no cluster gain built on failing dimensions may be claimed.

    python3 margin_report.py
    python3 margin_report.py --json
"""
from __future__ import annotations
import argparse, glob, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def load(dim_count: int | None = None) -> dict:
    models = {}
    for f in glob.glob(str(HERE / "benchmark-results" / "govbench" / "*.json")):
        try:
            d = json.loads(Path(f).read_text())
        except Exception:
            continue
        for r in (d if isinstance(d, list) else [d]):
            if not isinstance(r, dict):
                continue
            dd = r.get("dimensions")
            if isinstance(dd, dict) and all(isinstance(v, (int, float)) for v in dd.values()):
                if dim_count is None or len(dd) == dim_count:
                    models[r["model"]] = dd
    return models


def report(as_json: bool = False) -> int:
    from govbench_eval import DIMENSIONS
    models = load(15)          # the board everything was claimed on
    if len(models) < 2:
        print("  need at least 2 measured models"); return 2
    dims = sorted(next(iter(models.values())))
    rows = []
    for d in dims:
        ranked = sorted(((m, dd[d]) for m, dd in models.items()), key=lambda x: -x[1])
        margin = ranked[0][1] - ranked[1][1]
        n = len(DIMENSIONS[d]["tests"]) if d in DIMENSIONS else 5
        item_worth = 100.0 / n
        rows.append({"dimension": d, "winner": ranked[0][0], "score": ranked[0][1],
                     "runner_up": ranked[1][1], "margin": round(margin, 1), "n_items": n,
                     "item_worth": round(item_worth, 1),
                     "credible": bool(margin > item_worth),
                     "items_needed": (int(100 / margin) + 1) if margin > 0 else None})
    credible = [r for r in rows if r["credible"]]
    if as_json:
        print(json.dumps({"models": len(models), "dimensions": len(rows),
                          "credible": len(credible), "rows": rows}, indent=2))
        return 0
    print(f"  MARGIN REPORT — {len(models)} models × {len(rows)} dimensions\n")
    print(f"  A winner is credible only if its margin exceeds one test item's worth.\n")
    for r in sorted(rows, key=lambda x: -x["margin"]):
        need = f"needs ≥{r['items_needed']}" if r["items_needed"] else "TIED — no n fixes this"
        print(f"    {'✅' if r['credible'] else '⚠️ '} {r['dimension']:24s} "
              f"margin {r['margin']:5.1f}  1 item {r['item_worth']:4.1f}  n={r['n_items']:2d}  {need}")
    print(f"\n  {len(credible)}/{len(rows)} dimensions have a CREDIBLE winner.")
    if len(credible) < len(rows):
        print(f"  Cluster gains computed over the other {len(rows)-len(credible)} are not evidence.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    raise SystemExit(report(ap.parse_args().json))
