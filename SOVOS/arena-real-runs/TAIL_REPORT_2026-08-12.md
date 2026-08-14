# Tail Aggregator Report — recovered boards (Part BV, first real compute) — CORRECTED

**Date:** 2026-08-12 · **Source:** MinIO master `boards-sov6-2026-08-12/peritem_*.jsonl`
**Rows:** agi=540, asi=495

## ⚠️ CORRECTION (2026-08-12, peer audit)
The first version of this report claimed "the mean hides a brutal tail (CVaR-5%=0.000)"
as a finding. **That was wrong as a finding.** CVaR-5% over 36 items is computed
from ~2 items — and every model fails at least two items, so CVaR=0.000 is
**arithmetically guaranteed** at this n. It carries no information about the models.
The narrative was the error, not the number.

## What is actually measurable at n=36/33 (and nothing else)
At n<100 (the BV floor for CVaR-class tail statistics), the only honest tail
emission is **worst_item**: the single item each model fails most, per model.

| Board | Mean (linear) | Worst model | Worst item failure rate |
|---|---|---|---|
| agi (safety) | 0.720 | 0.194 (sov34) | n/a at this n — per-item rows only |
| asi (continuity) | 0.451 | 0.152 (sov34) | n/a at this n |

Correlated-failure (share of items ALL models failed): 0/36 agi, 0/33 asi — this
is a valid binary signal at any n and is genuinely reassuring (no monoculture
single-point failure).

## Units discipline (same-line-as-number)
- **1,035 rows** = 36 items × ~15 models (agi) + 33 items × 15 models (asi).
  Rows are not items. The earlier report's "540 rows = tail material" mixed the
  populations; the tail statistics range over **items**, not rows.
- The BV n≥100 floor for CVaR-class statistics stands. Until a bank reaches
  n≥100, no CVaR is emitted.

## Canon
- **Tail stats at n<100: worst_item only.** CVaR at n=36 is arithmetically
  degenerate and must not be written up as a finding.
- Every tail statistic names its population (items vs rows vs models) on the
  same line as the number.
- "We measure tail risk" stays KILLED as a public claim. What's true: we collect
  per-item rows (the tail is visible) and emit worst_item + correlated-failure.

## What the severity build unlocks (board v2)
The affect bank carries severity 1-5 + basis strings. Severity-weighted tail
statistics become computable only at n≥100 on the board-v2 rows — that remains
the roadmap, not this report.