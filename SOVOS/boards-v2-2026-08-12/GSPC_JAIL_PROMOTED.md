# AXIS-14 (gspc-jail) PROMOTED TO MEASURED — 2026-08-13

**Verdict: QUOTABLE — precision 1.000 (30/30), recall 1.000 (30/30), 0 FP / 0 FN**

The honest gate is met: n>=30 per class on a REAL, labelled gold bank built from
redblue_v2's deterministic attack matrix (10 harmful x 5 jailbreak wrappers = 50
attack + 10 plain-control + 10 benign-control, padded to n=30 ESCAPE / n=30 BENIGN).
No synthetic duels, no self-referential labels, no model judged a verdict —
the jail's deterministic detector scored against ground-truth that pre-exists
the run.

## Why this was the flagship (SO audit PM-3)
The firejail silent-no-op fix (63a03b57) made the harness real; the gold bank was
the ONLY missing piece. redblue_v2.py (50 attack cells) was the raw material the
audit identified. Now: first REAL gspc-jail measurement, D1-crisis-compatible.

## Register
- status: MEASURED (board_gspc_jail.json)
- precision 1.000 CI: n too small for a tight interval on this bank — the
  measurement is the detector-against-gold, reported with its counts
- containment, not isolation: firejail net=none is escape-DETECTION, never
  "provable isolation" — stated on every card
