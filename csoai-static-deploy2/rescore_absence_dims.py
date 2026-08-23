#!/usr/bin/env python3
"""rescore_absence_dims.py — re-measure the two dimensions whose grader was broken.

Only `fairness` and `robustness` used absence-only criteria, so only those two columns of
the published board are affected by the grader fix. Everything else is untouched and is not
re-run — a re-run that changes nothing still costs two hours of CPU and invites the
suspicion that numbers moved for reasons other than the fix.

`sov33-evolved-c2:latest` is EXCLUDED and marked unreproducible. Its blob is corrupt: it
emits "1\\n1\\n1\\n1" to every prompt. It cannot be re-measured, so its published scores
cannot be reproduced — and a number that cannot be reproduced must be withdrawn, not
carried forward because it is already printed somewhere.

    python3 rescore_absence_dims.py
"""
from __future__ import annotations

import json, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DIMS = ["fairness", "robustness"]
UNREPRODUCIBLE = {"sov33-evolved-c2:latest": "corrupt blob — emits '1\\n1\\n1' to every prompt"}


def ask(model: str, prompt: str, retries: int = 3) -> str:
    body = json.dumps({"model": model, "stream": False,
                       "options": {"temperature": 0, "num_predict": 160},
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request("http://localhost:11434/api/chat", data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read())["message"]["content"].strip()
        except Exception as e:
            last = e
            time.sleep(2 ** i)
    raise RuntimeError(f"{model}: {str(last)[:80]}")


def main() -> int:
    from govbench_eval import DIMENSIONS, grade_response
    from rank_intervals import load

    board = sorted(load())
    models = [m for m in board if m not in UNREPRODUCIBLE]
    print(f"  RESCORE — {DIMS} across {len(models)} models")
    print(f"  excluded as unreproducible: {list(UNREPRODUCIBLE)}\n")

    out, t0 = {}, time.time()
    for m in models:
        out[m] = {}
        for d in DIMS:
            tests = DIMENSIONS[d]["tests"]
            scores = []
            for t in tests:
                try:
                    scores.append(grade_response(t, ask(m, t["q"])))
                except Exception as e:
                    print(f"    ⚠️  {m} / {d}: {str(e)[:60]} — item dropped, NOT scored 0")
            out[m][d] = round(sum(scores) / len(scores) * 100, 1) if scores else None
            out[m][d + "_n"] = len(scores)
        print(f"    {m:30s} fairness {str(out[m]['fairness']):>6s}  "
              f"robustness {str(out[m]['robustness']):>6s}", flush=True)

    old = load()
    print(f"\n  CHANGE vs the published board\n")
    print(f"    {'model':30s} {'fairness':>18s} {'robustness':>18s}")
    for m in models:
        row = ""
        for d in DIMS:
            o, n = old[m].get(d), out[m][d]
            row += f"  {o:5.1f} → {n:5.1f} ({n-o:+5.1f})" if n is not None else f"  {o:5.1f} →   n/a "
        print(f"    {m:30s}{row}")

    p = HERE / "benchmark-results" / "rescore_absence_dims.json"
    p.write_text(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reason": "absence-only grading credited silence and penalised correct answers",
        "dimensions_rescored": DIMS,
        "unreproducible_excluded": UNREPRODUCIBLE,
        "scores": out,
        "previous": {m: {d: old[m].get(d) for d in DIMS} for m in models},
    }, indent=2))
    print(f"\n  {time.time()-t0:.0f}s  ->  {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
