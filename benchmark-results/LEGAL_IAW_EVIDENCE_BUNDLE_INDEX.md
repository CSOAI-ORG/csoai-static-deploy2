# LEGAL / IAW EVIDENCE BUNDLE INDEX — 2026-08-09 (JEEVES)
**Purpose:** one manifest of the discipline evidence that exists for human/legal
sign-off (Phase D of the 100-move plan). Nothing here claims legal approval —
it indexes what a reviewer can recompute/verify. Sign-off is a human gate.

## 1. Measurement-not-certification stance (the discipline firewall)
- Live on: `/about`, `/arena`, `/govbench` — "measurement, not certification"
  is the stated, deployed position (quotable, published).
- Red lines published in `llms.txt` (§Red lines) and arena pages.

## 2. Measured arena (12/13 greenfield axes)
- `arena-build/arena.json` — generated 2026-08-06; each axis carries: bench,
  n, score (acc), status, instrument, globe seat, provenance.
- 12/12 axes MEASURED with Wilson CIs where applicable; jail (13th) UNMEASURED
  (n=18<30, honest gap, no fabricated score).
- Live surface: `/arena` (GSPC Training Arenas) — every number recomputable.

## 3. Signed change/evidence chain
- 19+ `tick-*-sigil.json` files in estate root — Ed25519-signed EAT ticks
  (each carries chain position + signature; `/audit` documents the SIGIL
  verification method).
- `forest/honey_*.jsonl` — append-only honey ledger (all producers / downloads /
  layer0), the raw measurement trail.

## 4. Data-protection posture
- corpus-watch: C2PA, EUR-Lex, NIST IR 8547 freshness watched by
  `csoai-gspc-api` anchor Worker (live watchers, status-coded on the globe).
- No personal data in arena measurements: bench items are public statutory
  instruments + model outputs; no PII collection on these surfaces.

## 5. Honest non-claims (what this bundle does NOT assert)
- NOT a legal opinion, NOT certification, NOT "IAW" attestation.
- The discipline docs (measurement-not-adjudication, 3HONEY flags) live in the
  sandbox/VM estate (`/home/claude/estate` per the arena readiness doc).
- sov34 SFT set (236 label-only pairs) + board_sov34 live there too — gated on
  GCP billing + sandbox access.

## Gated items + one-command unblocks
| item | lever | owner |
|---|---|---|
| Legal/IAW formal sign-off | human review of this bundle | Nick/legal |
| Sandbox discipline docs (3HONEY etc.) | GCP billing re-enable → fetch from VM | Nick |
| sov34 SFT fire (236 pairs) | `sov_sft_train.py` on GPU | GPU/Modal (Nick spend) |