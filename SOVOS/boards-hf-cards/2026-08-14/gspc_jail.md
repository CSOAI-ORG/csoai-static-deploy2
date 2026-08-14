---
license: apache-2.0
tags: [ai-governance, gspc_jail, measurement, eu-ai-act, gspc, sandbox-escape]
task_categories: [text-classification]
language: [en]
---
# Sandbox-escape / SandboxEscapeBench — GSPC board (measurement, not certification)

Deterministic containment measurement. **Monitored containment, not provable isolation.**

- **Gold bank:** 30 ESCAPE + 30 BENIGN items
- **Detector:** TP 30 · TN 30 · FP 0 · FN 0
- **Precision:** 1.0 · **Recall:** 1.0
- **Gold provenance:** redblue_v2 50 attack + 10 plain + 10 benign + deterministic pad, deterministic-ESCAPE/BENIGN labels
- **Gate:** deterministic jail detection — no model judged this — no model judged this
- **Signed board sha256 (leading 12):** `9792427cb5c9`
- **Measured:** 2026-08-13/14 (boards-v2-2026-08-12), pod-verified

## Honest register
- Gold-bank-first gate: no MEASURED claim before adjudicated gold.
- **Monitored containment, not provable isolation.** Language lock.
- Missing cells are **UNMEASURED**, never counted as zero.
- A regulator certifies; **we measure.** Nothing here is a certification.

## Raw evidence
- `board.json` — the signed raw board (keep gated)
- `manifest_board_gspc_jail.json` — Ed25519-signed manifest (verify: `sign.py --verify`)

Published by the Council of AI (CSOAI Ltd UK 16939677).
