#!/usr/bin/env python3
"""measure_qwen.py — measure a NEW base (e.g. Qwen3.8-27B) against the incumbent
merges on the GSPC axes, and say plainly which base to adopt. Runs on a POD
(ollama endpoint), never the Mac.

WHY
The estate's own board already shows the base beats every sovereign fine-tune we
own on governance. So before spending pod compute on quantise/TTT-fusion, we
MEASURE the new base first — adopt-best-base is very likely the win, and this
confirms it with numbers instead of assuming. This is the honest first step of
"train and improve": you cannot improve what you have not measured.

It reuses the real scorer (gspc_flywheel.run_axis over the 6 control-anchored
axes, UNMEASURED-honest, degenerate-baseline aware) — no reinvented measurement.

    # on a pod where ollama serves the models:
    OLLAMA_HOST=http://localhost:11434 python3 measure_qwen.py \
        --new qwen3.8:27b --incumbents sov34-1p5b --control qwen2.5:1.5b

Emits benchmark-results/model_upgrade/<ts>.json with a machine ADOPT/KEEP verdict.
"""
import argparse, json, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "benchmark-results" / "model_upgrade"


def ollama_has(model: str) -> bool:
    try:
        out = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=20).stdout
        base = model.split(":")[0]
        return any(base in line for line in out.splitlines())
    except Exception:
        return False


def ollama_pull(model: str) -> bool:
    print(f"  pulling {model} … (first run only)")
    try:
        return subprocess.run(["ollama", "pull", model], timeout=7200).returncode == 0
    except Exception as e:
        print(f"  pull failed: {e}")
        return False


def score_model(gf, model: str) -> dict:
    row = {}
    for ax in gf.AXES:
        row[ax] = gf.run_axis(model, ax)
    got = [v["score"] for v in row.values() if v.get("status") == "MEASURED"]
    mean = round(sum(got) / len(got), 4) if got else None
    return {"axes": row, "mean": mean, "measured_axes": len(got), "total_axes": len(gf.AXES)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Measure a new base vs incumbents on GSPC; say which to adopt.")
    ap.add_argument("--new", required=True, help="new base tag in ollama, e.g. qwen3.8:27b")
    ap.add_argument("--incumbents", nargs="*", default=[], help="current merges/fine-tunes to compare")
    ap.add_argument("--control", required=True, help="current base / untrained control, e.g. qwen2.5:1.5b")
    ap.add_argument("--no-pull", action="store_true", help="skip ollama pull (models already present)")
    a = ap.parse_args()

    try:
        import gspc_flywheel as gf
    except Exception as e:
        sys.exit(f"cannot import gspc_flywheel (run from the monorepo root): {e}")

    everyone = [a.new, *a.incumbents, a.control]
    if not a.no_pull:
        for m in dict.fromkeys(everyone):
            if not ollama_has(m):
                ollama_pull(m)

    print(f"\n  measuring {len(everyone)} model(s) x {len(gf.AXES)} axes @ {getattr(gf, 'OLLAMA', '?')}\n")
    results = {}
    for m in dict.fromkeys(everyone):
        print(f"  scoring {m} …")
        results[m] = score_model(gf, m)

    ctrl_mean = results[a.control]["mean"]
    ranked = sorted(
        [(m, r["mean"]) for m, r in results.items() if r["mean"] is not None],
        key=lambda x: x[1], reverse=True,
    )
    # Verdict: adopt the highest-mean model that BEATS the control by > 1 pt.
    verdict = {"control": a.control, "control_mean": ctrl_mean, "ranking": ranked, "recommendation": None}
    if ranked and ctrl_mean is not None:
        best_m, best_mean = ranked[0]
        margin = round((best_mean - ctrl_mean) * 100, 1)
        if best_m == a.control or margin <= 1:
            verdict["recommendation"] = (
                f"KEEP {a.control}: nothing beats the current base by >1 pt "
                f"(best challenger {best_m} at {margin:+} pts). Do NOT merge; a fine-tune that "
                f"can't beat its own base learned nothing.")
        elif best_m == a.new:
            verdict["recommendation"] = (
                f"ADOPT the new base {a.new} (+{margin} pts over {a.control}). Ship the base as-is; "
                f"quantise only for serving; TTT-fuse only against a measured gap.")
        else:
            verdict["recommendation"] = (
                f"ADOPT {best_m} (+{margin} pts). Note the new base {a.new} was not the top — "
                f"measure why before committing pod compute.")

    OUT.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob = {"measured_at": ts, "endpoint": getattr(gf, "OLLAMA", None), "results": results, "verdict": verdict}
    path = OUT / f"{ts}.json"
    path.write_text(json.dumps(blob, indent=1, sort_keys=True))

    print("\n  ── VERDICT " + "─" * 40)
    for m, mean in ranked:
        flag = "  ← control" if m == a.control else ("  ← NEW" if m == a.new else "")
        print(f"    {m:28} {mean*100:5.1f}%{flag}")
    print("\n  " + (verdict["recommendation"] or "no measured models to rank"))
    print(f"\n  written → {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
