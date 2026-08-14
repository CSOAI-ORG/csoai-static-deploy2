---
license: apache-2.0
tags: [ai-governance, affect, measurement, eu-ai-act, gspc]
task_categories: [text-classification]
language: [en]
---
# Affect / AffectBench — GSPC board (measurement, not certification)

Control-anchored GSPC measurement of a model fleet. **Measurement, not certification.**

- **Item set (bank_items):** 41 (the quotable per-item count)
- **Models measured:** 19
- **Board status:** MEASURED
- **Best model:** preservation-v3-light
- **Signed board sha256 (leading 12):** `48fac58b5380`
- **Measured:** 2026-08-13/14 (boards-v2-2026-08-12), pod-verified

## Honest register
- `bank_items` is the TRUE quotable per-item count. The per-item **pooled** rows
  (bank_items × models) are an artifact of measurement, never a per-item figure.
- Missing axes are **UNMEASURED**, never counted as zero.
- A model at or below the untrained control learned nothing measurable.
- A regulator certifies; **we measure.** Nothing here is a certification.

## Raw evidence
- `board.json` — the signed raw board (may carry internal model codenames; keep gated)
- `manifest_*.json` — Ed25519-signed manifest (verify: `sign.py --verify`)

Published by the Council of AI (CSOAI Ltd UK 16939677).
