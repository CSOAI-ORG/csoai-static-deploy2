#!/usr/bin/env python3
"""greenfield_e2e.py — run the 8 dated-2026-07-28 greenfield GovBench dimensions E2E against
local Ollama models. The 8 greenfield dims are the new axes the benchmark added on 2026-07-28:

  retrieval_faithfulness, cross_walk, regional_law, redress, calibration,
  agentic (explicitly tagged "Genuinely greenfield"),
  fundamental_rights, cognitive_security.

User shorthand "6 axis greenfields" — the harness always runs as the 8-dim dated set so the
result is comparable across runs; the "6 axis" framing is held in commentary.

Each model is graded with the existing grade_response() function and the dim_score is weighted.
Output: benchmark-results/greenfield_e2e/<model>.json + a combined leaderboard JSON.
"""
from __future__ import annotations
import argparse, json, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from govbench_eval import DIMENSIONS, call_model, grade_response, make_sigil  # noqa: E402

# The 8 dated-2026-07-28 greenfield dimensions. Order preserved from the file.
GREENFIELD_DIMS = [
    "retrieval_faithfulness",
    "cross_walk",
    "regional_law",
    "redress",
    "calibration",
    "agentic",
    "fundamental_rights",
    "cognitive_security",
]

OUT_DIR = HERE / "benchmark-results" / "greenfield_e2e"
OUT_DIR.mkdir(parents=True, exist_ok=True)
LEADERBOARD = OUT_DIR / "leaderboard.json"

DEFAULT_MODELS = [
    "qwen2.5:0.5b",
    "sov33-v7:latest",
    "sov-sovereign-v4:latest",
    "clan-sovereignty-cited:latest",
    "clan-sovereignty-refusing:latest",
]


def _reachable_ollama(timeout: int = 5) -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=timeout)
        return True
    except Exception:
        return False


def evaluate_model_greenfield(model_name: str, provider: str = "ollama") -> dict:
    """Run only the greenfield dims; weight per test; emit per-dim %, overall %, sigil."""
    if provider == "ollama" and not _reachable_ollama():
        raise RuntimeError("ollama_unreachable")

    dim_results: dict[str, dict] = {}
    total_score = 0.0
    total_weight = 0

    for dim_key in GREENFIELD_DIMS:
        dim = DIMENSIONS[dim_key]
        dim_score = 0.0
        dim_weight = 0
        per_test: list[dict] = []
        for test in dim["tests"]:
            weight = test.get("weight", 1)
            try:
                resp = call_model(model_name, test["q"], provider)
            except Exception as e:
                resp = ""
                per_test.append({"q": test["q"][:80], "error": str(e)[:120], "weight": weight})
                continue
            score = grade_response(test, resp)
            dim_score += score * weight
            dim_weight += weight
            per_test.append({"q": test["q"][:80], "score": round(score, 3), "weight": weight,
                             "head": resp[:120]})
            time.sleep(0.3)
        pct = (dim_score / dim_weight * 100) if dim_weight else 0.0
        dim_results[dim_key] = {
            "name": dim["name"],
            "score_pct": round(pct, 2),
            "n_tests": dim_weight,
            "per_test": per_test,
        }
        total_score += dim_score
        total_weight += dim_weight

    overall = (total_score / total_weight * 100) if total_weight else 0.0
    sigil = make_sigil({"model": model_name, "score": overall, "dims": list(GREENFIELD_DIMS)})
    return {
        "model": model_name,
        "provider": provider,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "greenfield_dims": GREENFIELD_DIMS,
        "n_dims": len(GREENFIELD_DIMS),
        "overall_pct": round(overall, 2),
        "dimensions": dim_results,
        "sigil": sigil,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    ap.add_argument("--provider", default="ollama")
    args = ap.parse_args()

    if not _reachable_ollama():
        print("  ⛔ Ollama is not reachable on http://localhost:11434 — start it first.")
        return 2

    print("=" * 78)
    print(f"  GREENFIELD E2E — {len(GREENFIELD_DIMS)} dims × {len(args.models)} model(s)")
    print("=" * 78)
    print("  Dims: " + ", ".join(GREENFIELD_DIMS))

    results = []
    for m in args.models:
        print(f"\n  ▶ {m} ({args.provider})")
        t0 = time.time()
        try:
            r = evaluate_model_greenfield(m, args.provider)
        except Exception as e:
            print(f"     ⛔ SKIPPED: {e}")
            continue
        r["wall_secs"] = round(time.time() - t0, 1)
        results.append(r)

        out = OUT_DIR / f"{m.replace('/', '_').replace(':', '_')}.json"
        out.write_text(json.dumps(r, indent=2))
        print(f"     OVERALL {r['overall_pct']:5.1f}%   ({r['wall_secs']}s)   → {out.name}")
        for dk, d in r["dimensions"].items():
            mark = "✅" if d["score_pct"] >= 70 else "❌"
            print(f"       {mark} {d['name']:28s} {d['score_pct']:5.1f}%  ({d['n_tests']} tests)")

    if not results:
        print("\n  ⛔ No model produced a result.")
        return 3

    LEADERBOARD.write_text(json.dumps(results, indent=2))

    print("\n" + "=" * 78)
    print("  GREENFIELD E2E — LEADERBOARD (overall %)")
    print("=" * 78)
    print(f"  {'model':40s} {'overall':>8s} {'n_dims':>7s} {'wall_s':>7s}")
    for r in sorted(results, key=lambda x: -x["overall_pct"]):
        print(f"  {r['model']:40s} {r['overall_pct']:7.1f}% {r['n_dims']:>7d} {r['wall_secs']:>6.1f}s")
    print("=" * 78)
    print(f"  SIGIL (top model): {sorted(results, key=lambda x: -x['overall_pct'])[0]['sigil'][:32]}...")
    print(f"  Leaderboard → {LEADERBOARD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())