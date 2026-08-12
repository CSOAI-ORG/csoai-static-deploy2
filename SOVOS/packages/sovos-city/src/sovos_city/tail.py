"""TAIL — non-linear tail statistics over the per-item rows.

The board reports the MEAN — a linear aggregator that averages every item
equally, which is exactly how a 1% catastrophic tail hides under a 99% score.
Harm does not live in the mean. It lives in the tail: the rare item that breaks
the model, and worse, the item that breaks EVERY model at once.

This module reads the deterministic per-item rows bench.py already writes
(one row per item x model, with a `correct` bool) and derives tail statistics.
It is:

  * DETERMINISTIC and REPRODUCIBLE — recomputable from the same rows by anyone.
    No model judges anything here; this is arithmetic over recorded outcomes.
  * NON-LINEAR by design — worst-case (max), CVaR (mean of the worst tail),
    and correlated-failure (all-fail rate). None of these is an average.
  * NAMED, never opaque — every number below is a one-line formula over the
    rows. If you cannot recompute it from the rows, it is not a measurement.

The single most safety-relevant statistic is `correlated_failure_rate`: the
fraction of items that the WHOLE fleet fails together. Independent errors
average out; correlated errors are the fat tail that executes millions of times
simultaneously. That number is invisible to any per-model mean.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


def load_rows(path: str | Path) -> List[Dict[str, Any]]:
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def _item_key(r: Dict[str, Any]) -> str:
    return str(r.get("axis_item") or r.get("item") or "")


def item_pass_rates(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    """For each item: fraction of models that got it right (scored rows only).

    Transport failures (ours) are excluded — they are not evidence about the
    item. An unparsed answer counts as wrong, same as bench.py.
    """
    got = defaultdict(int)
    tot = defaultdict(int)
    for r in rows:
        err = r.get("transport_error")
        if err and str(err).startswith("TRANSPORT"):
            continue  # ours, not evidence about the item
        k = _item_key(r)
        tot[k] += 1
        if r.get("correct"):
            got[k] += 1
    return {k: got[k] / tot[k] for k in tot if tot[k] > 0}


def cvar(values: List[float], alpha: float = 0.05) -> float:
    """CVaR_alpha — the mean of the worst alpha-fraction of items.

    A linear mean asks 'how good on average'. CVaR asks 'how bad are the bad
    cases'. For a fat tail these diverge sharply; for a thin tail they agree.
    """
    if not values:
        return 0.0
    vals = sorted(values)
    k = max(1, int(math.ceil(alpha * len(vals))))
    return sum(vals[:k]) / k


@dataclass
class TailStats:
    axis: str
    n_items: int
    n_models: int
    mean_item_pass: float          # the LINEAR aggregator (what the board shows)
    worst_item_pass: float         # NON-LINEAR: the single hardest item
    cvar05_item_pass: float        # NON-LINEAR: mean of the worst 5% of items
    correlated_failure_rate: float # the fat tail: items the WHOLE fleet fails
    fleet_fragile_items: List[str] # the item keys every model failed
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def tail_stats(axis: str, rows: List[Dict[str, Any]], alpha: float = 0.05) -> TailStats:
    rates = item_pass_rates(rows)
    models = {r.get("model") for r in rows if r.get("model")}
    if not rates:
        return TailStats(axis, 0, len(models), 0, 0, 0, 0, [], "no scored rows")
    vals = list(rates.values())
    mean = sum(vals) / len(vals)
    worst = min(vals)
    c = cvar(vals, alpha)
    fragile = sorted(k for k, v in rates.items() if v == 0.0)  # every model failed
    corr = len(fragile) / len(rates)
    return TailStats(
        axis=axis, n_items=len(rates), n_models=len(models),
        mean_item_pass=round(mean, 4),
        worst_item_pass=round(worst, 4),
        cvar05_item_pass=round(c, 4),
        correlated_failure_rate=round(corr, 4),
        fleet_fragile_items=fragile[:20],
        note=("mean is the board's linear number; worst-case and CVaR are the "
              "non-linear tail; correlated_failure_rate is the fat correlated "
              "tail no per-model mean can see — every listed item broke the whole fleet"),
    )


def gap_report(stats: TailStats) -> str:
    """The one line that matters: how far the mean is from the tail."""
    gap = stats.mean_item_pass - stats.cvar05_item_pass
    return (f"{stats.axis}: mean {stats.mean_item_pass:.3f} vs CVaR5% "
            f"{stats.cvar05_item_pass:.3f}  (tail gap {gap:.3f}); "
            f"correlated-failure {stats.correlated_failure_rate:.1%} "
            f"({len(stats.fleet_fragile_items)} items broke the whole fleet)")
