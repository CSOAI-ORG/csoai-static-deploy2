# Measurement Delta Note #1 — Pantheon Season 1a → 1b
**Series:** Measurement Delta Notes (estate doctrine B2)
**Date:** 2026-08-12 · **Status:** REAL (data verified from `season_1b_clean.json` + recovered boards)

## What this note is
The standing publication series that converts a measurement correction into a
credibility asset. Issue #1 is the infra-taint → forensics → fix → clean table
story. Nobody else in AI governance publishes this, because nobody else kept the
tainted season.

## The event (1 Dec-below)
Season 1a measured **broken artifacts**. Two contestants (oowm-4way, spec-care)
emitted the broken-GGUF `?????` signature on every prompt — an infrastructure
bug (ollama 0.32.8 safetensors→GGUF conversion), **not** a model property.

The ruler caught it before a human did: the ouroboros loop flagged the `?????`
output as unusable (recall 0 < 0.5 floor) and auto-REVERTED. The `is_infra_tainted()`
classifier was then encoded into the arena itself. (Part BB doctrine.)

## Verification (this note's receipt — real data, not claims)
From `SOVOS/arena-real-runs/season_1b_clean.json`, n_models=6, **all CLEAN**:
- `tainted_probes: 0` on every model · `checked_probes: 12` · `excluded_matches: 0`
- sample responses are real text (probes answered with PROHIBITED/REFUSE, no `?????`)

## The delta (1a → 1b; n=12 each, NON-QUOTABLE ordering — cluster only)

| Model | 1a (tainted) | 1b (clean) | Δ |
|---|---|---|---|
| oowm-4way | 1480.4 | **1514.1** | +33.7 |
| spec-privacy | 1482.2 | **1513.6** | +31.4 |
| spec-safety | 1478.6 | **1513.3** | +34.7 |
| spec-governance | 1479.0 | **1510.8** | +31.8 |
| base qwen2.5:0.5b | 1479.8 | **1500.8** | +21.0 |
| spec-care | 1479.5 | **1497.3** | +17.8 |
| Eunomia (defender) | 1560.5 | **1449.5** | −111.0 |

## The forensics
The 1a table was two broken GGUFs dragging every pairing to draws. Converting to
proper Q4_K_M (797MB each, real tokenizer metadata → real text like
"NO_CARE_NEEDED response") inverted the league. The specialists were never losers;
the measurement was broken.

## Honest boundaries (canon, never violated)
- **n=12 is NOT quotable.** No Wilson intervals, no marketing copy, no
  "spec-privacy beats spec-safety" claims — the ordering is noise at this depth.
  The only legitimate cluster read: specialists ≈ oowm > base > care > Eunomia.
- **Eunomia −111**: either the defender is weak or the ruler is. Under the
  "generator evolves, judge never does" doctrine, this is a **quiet gate-strength
  investigation**, not a published condemnation. Conducted before anything public.
- **Season 1c (n≥30) is the gate** for any quotable Pantheon number. It was
  GPU-starved behind a sibling lane's run_all.py — correct non-kill.
- 1a stays in the record forever. History cannot be retro-fixed; the immutability
  is the chain's value.

## The honest headline
"Our first live season caught our own broken models before a customer could."
Ruler tested by failing, then passing. (Part BB/Part X dogfooded.)

## Canon addenda
- No bank ships unless it beats the constant-predictor baseline.
- No comparison claim ships with overlapping CIs.
- Infrastructure vs model failures filed separately at every layer.
- Self-corrections published alongside results.

*Zenodo DOI pending — this note is the publish-pipeline's first candidate (B4/B2).*
