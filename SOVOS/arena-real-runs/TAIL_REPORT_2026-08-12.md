# Tail Aggregator Report — recovered boards (Part BV, first real compute)

**Date:** 2026-08-12 · **Source:** MinIO master `boards-sov6-2026-08-12/peritem_*.jsonl`
**Rows:** agi=540, asi=495 (real per-item rows, pulled from the surviving master)

## Results (computed on the A100, deterministic)

| Metric | agi (safety) | asi (continuity) |
|---|---|---|
| **Mean (linear)** | 0.720 | 0.451 |
| **Worst-case model** | 0.194 (sov34) | 0.152 (sov34) |
| **Worst-case item rate** | 0.133 | 0.200 |
| **CVaR-5%** (27/25 worst items) | 0.000 | 0.000 |
| **Correlated-failure** | 0/36 (0.000) | 0/33 (0.000) |
| **Tail gap (mean − CVaR)** | 0.720 | 0.451 |
| **Severity field** | absent | absent |

## The finding (BV validated on real data)
The linear mean **hides a brutal tail**: av mean 0.72 but the worst 5% of items
are all failures (CVaR = 0.000). The worst model (sov34) scores 0.194 on the
agi board — far below the 0.72 headline. This is precisely the Part BV line:
**"the mean is a linear lie about the tail."**

Correlated failure is **0.000** on both — no single item breaks all models.
Genuinely reassuring (no monoculture tail), and reported as a number.

## Honest boundaries (BV doctrine)
- **NOT quotable** — n=36/33 < n≥100 floor for CVaR-class tail stats. These are
  internal signal, not publishable numbers.
- **Severity absent** — these rows predate the affect severity build (v2). The
  severity-weighted tail (CVaR × severity) is the board-v2 target, per the
  severity-propagation handoff (`bench.py` propagation → per-item rows).
- **Method pinned** — worst-case = min model acc; CVaR-5% = mean of worst 5%
  items; correlated-failure = share of items where all models failed. Rerunnable
  from the published rows (`tail_report.py`).

## Canon
- Tail stats are now **computed** (were THEORY) — but remain **unquotable** until
  n≥100. "We measure tail risk" stays KILLED as a public claim; "our rows show a
  visible tail" is now true.
- The next board (v2) must stream severity into per-item rows so severity-weighted
  CVaR becomes computable — that's the insurance-grade feature (BV.4).