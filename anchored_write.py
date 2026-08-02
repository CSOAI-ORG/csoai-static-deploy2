#!/usr/bin/env python3
"""anchored_write.py — stamp the corpus anchor AT WRITE TIME, not as a later pass.

═══════════════════════════════════════════════════════════════════════════════
THE BUG THIS REPLACES, WHICH FIRED TWICE IN ONE DAY
═══════════════════════════════════════════════════════════════════════════════
Anchoring was a separate step: run the benchmarks, then run `corpus_anchor.py` to stamp every
result with the corpus root it was measured against. That ordering is fragile in a way that is
invisible until it bites:

  1. First failure — the AUTO queue anchored FIRST, so every benchmark that rewrote its own
     artefact afterwards silently stripped the anchor it had just received. The gate caught
     `pqcbench.json` unanchored. Fixed by moving the anchor last.
  2. Second failure, same day, after the "fix" — running `provbench.py` by hand, outside the
     queue, de-anchored its own artefact again. The gate caught it again.

The lesson is the estate's own law: **a discipline that must be remembered will be forgotten.**
Ordering is a discipline. Anchoring at write time is a mechanism.

So a result cannot be written without its anchor, because the same call does both. There is no
ordering to get wrong and no out-of-band run to forget, and `corpus_anchor.py` becomes a
backfill for legacy artefacts rather than the thing correctness depends on.

    from anchored_write import write_result
    write_result("provbench.json", payload)

    python3 anchored_write.py --selftest
"""
from __future__ import annotations

import json, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"


def current_anchor() -> dict:
    """The corpus root as it stands right now.

    Raises rather than returning a placeholder. A result that cannot name the corpus it was
    measured against is not a result whose anchor is 'unknown' — it is a result that must not
    be written, because an unanchored score can never be shown to have expired, and expiry is
    the entire drift product.
    """
    from corpus_anchor import load_corpus, corpus_root, NORMALISER_VERSION
    anchors = load_corpus()                      # raises if the corpus is unreadable
    return {"corpus_root": corpus_root(anchors),
            "provisions": len(anchors),
            "normaliser_version": NORMALISER_VERSION,
            "anchored_at": datetime.now(timezone.utc).isoformat(),
            "retro": False,
            "note": "Anchored at write time by anchored_write.write_result()."}


def _n_cells(payload: object) -> int | None:
    """Cell count of a flywheel-style payload, or None for non-cell artefacts."""
    if isinstance(payload, dict) and isinstance(payload.get("cells"), list):
        return len(payload["cells"])
    return None


def write_result(name: str, payload: dict, *, indent: int = 2) -> Path:
    """Write a result artefact WITH its anchor. The only supported way to write one.

    Day-file collision guard (the 2026-08-01/02 lesson, fired twice): a smaller-cells
    payload must never silently overwrite a richer one at the same path — that is how
    a 0/24-cell smoke stub destroyed the real 83-model and Kaggle anchors. Instead the
    incoming payload is preserved at a run-name-suffixed path and the richer file stays
    canonical. Same-size-or-larger rewrites proceed normally (legitimate re-runs).
    """
    if not isinstance(payload, dict):
        raise TypeError("a result artefact must be an object so it can carry its anchor")
    payload = dict(payload)
    payload["corpus_anchor"] = current_anchor()
    p = RESULTS / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        try:
            old = json.loads(p.read_text())
        except Exception:
            old = None
        new_n, old_n = _n_cells(payload), _n_cells(old)
        if new_n is not None and old_n is not None and new_n < old_n:
            stamp = datetime.now(timezone.utc).strftime("%H%M%S")
            cand = p.with_name(f"{p.stem}_run-{stamp}{p.suffix}")
            i = 2
            while cand.exists():
                cand = p.with_name(f"{p.stem}_run-{stamp}-{i}{p.suffix}")
                i += 1
            print(f"anchored_write: refusing downgrade of {name} "
                  f"({old_n} -> {new_n} cells); preserving as {cand.name}", file=sys.stderr)
            p = cand
    p.write_text(json.dumps(payload, indent=indent))
    return p


def audit() -> tuple[int, list[str]]:
    """Which result artefacts are unanchored right now?"""
    bad = []
    for p in sorted(RESULTS.glob("*.json")):
        if p.name in ("corpus_anchor.json", "production_ready.json", "auto_run.json",
                      "board_preflight.json", "sync_evidence.json"):
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if isinstance(d, dict) and "corpus_anchor" not in d:
            bad.append(p.name)
    return len(bad), bad


def selftest() -> int:
    fails = []
    tmp = "_anchored_write_selftest.json"

    # A written result must carry its anchor, with no second step.
    p = write_result(tmp, {"benchmark": "selftest", "value": 1})
    d = json.loads(p.read_text())
    if "corpus_anchor" not in d:
        fails.append("write_result did not stamp an anchor")
    elif not d["corpus_anchor"].get("corpus_root"):
        fails.append("anchor carries no corpus_root")
    elif d["corpus_anchor"].get("retro") is not False:
        fails.append("write-time anchor should not be marked retro")
    if d.get("value") != 1:
        fails.append("payload was not preserved")

    # Rewriting re-anchors rather than inheriting a stale root — the exact failure that let a
    # manual re-run strip its own anchor.
    p = write_result(tmp, {"benchmark": "selftest", "value": 2})
    d2 = json.loads(p.read_text())
    if "corpus_anchor" not in d2:
        fails.append("rewrite dropped the anchor")

    # A non-object payload cannot carry an anchor and must be refused, not silently wrapped.
    try:
        write_result(tmp, [1, 2, 3])          # type: ignore[arg-type]
        fails.append("a list payload was accepted")
    except TypeError:
        pass

    # Downgrade guard: a smaller-cells payload must not overwrite a richer one at the
    # same path — both must survive, the richer one canonical.
    day_like = "flywheel/_selftest_day.json"
    p = write_result(day_like, {"benchmark": "flywheel", "cells": [{"a": 1}, {"a": 2}, {"a": 3}]})
    p2 = write_result(day_like, {"benchmark": "flywheel", "cells": [{"a": 1}]})
    if p2 == p:
        fails.append("downgrade overwrote the richer day file")
    else:
        if len(json.loads(p.read_text())["cells"]) != 3:
            fails.append("richer day file was not preserved")
        if len(json.loads(p2.read_text())["cells"]) != 1:
            fails.append("smaller run was not preserved at its suffixed path")
        if "corpus_anchor" not in json.loads(p2.read_text()):
            fails.append("suffixed run file was not anchored")
        p2.unlink(missing_ok=True)
    # A same-size-or-larger re-run still overwrites in place (legitimate re-run).
    p3 = write_result(day_like, {"benchmark": "flywheel", "cells": [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}]})
    if p3 != p:
        fails.append("a larger re-run was needlessly suffixed")
    (RESULTS / day_like).unlink(missing_ok=True)

    (RESULTS / tmp).unlink(missing_ok=True)

    # An unreadable corpus must raise, never yield a placeholder anchor.
    import corpus_anchor as ca
    real = ca.DB
    try:
        ca.DB = Path("/nonexistent/none.db")
        try:
            current_anchor(); fails.append("missing corpus produced an anchor anyway")
        except Exception:
            pass
    finally:
        ca.DB = real

    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 8/8' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    n, bad = audit()
    if n:
        print(f"  ⚠️  {n} unanchored artefact(s): {', '.join(bad[:8])}")
        print("     Run corpus_anchor.py to backfill, and route their writer through")
        print("     write_result() so it cannot happen again.")
    else:
        print("  ✅ every result artefact carries a corpus anchor")
    raise SystemExit(1 if n else 0)
