# ENGINE FIX CYCLE #1 — det @ 0.000 (2026-08-14)

**Engine:** sovos-engine · **Axis:** det (Detector-interop) · **Node:** A100 signing node

## The gap (diagnosed from live data, not asserted)
`sovos-engine diagnose det` flagged: **sov6-logic-v3-light at 0.000** — the
weakest engine on the det board (33 items, 0 correct, 33 unparsed).

## Fix cycle — with an honest self-correction (the engine loop working as designed)

### Hypothesis 1 (recorded, then REJECTED)
"0.000 = broken GGUF, same class as the oowm-4way `?????` infra-taint; fix =
rebuild/requantize."
- Live probe of sov6-logic on a det prompt → **empty content (0 chars)**
- BUT the same model scored **0.83 on art5** (30/36 correct) with real raw output
  (len 9-10) in the peritem file
- → The GGUF is NOT broken. Hypothesis 1 rejected. (`fix_det_20260814_041353.json`)

### Hypothesis 2 (current, evidence-backed)
"0.000 = **axis-specific silence**: a DIVERGENT/INTEROPERABLE grammar on dense
provenance-detector prompts trips sov6-logic to empty output; sov6-synthesis and
sov6-relationality show the same class (malformed/empty on det but real output
elsewhere)."
- det items are dense: "Provenance asset (genuinely C2PA-signed). Detector-A
  (C2PA-Reader)=PROV, Detector-B(marker)=PROV. GT=SIGNED." — notation-heavy
  prompts that this model class fails to answer under the grammar.
- **Fix candidate:** tune the det prompt/grammar for the sov6-logic family
  (simplify the Detector-A/B notation, add a plain-language preamble), then
  re-measure. Do NOT pad the bank; do NOT rebuild a healthy GGUF.
  (`fix_det_20260814_041540.json`, signed VALID)

## Why this is the point of the beast
The engine loop **self-corrected a wrong fix hypothesis in minutes** using
per-item evidence — no silent re-scoring, no bank padding, no wasted GPU
rebuild. The signed fix trail (3 records) is the honest audit: what we thought,
what the data said, what we'll do.

## Evidence
- `benchmark-results/engine-fixes/fix_det_20260814_040839.json` (first cycle)
- `benchmark-results/engine-fixes/fix_det_20260814_041353.json` (hypothesis 1, rejected)
- `benchmark-results/engine-fixes/fix_det_20260814_041540.json` (hypothesis 2, current — signed VALID)
- peritem_det.jsonl / peritem_art5.jsonl (the raw-content evidence)
