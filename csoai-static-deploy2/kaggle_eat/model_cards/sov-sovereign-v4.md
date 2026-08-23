# sov-sovereign-v4

**Model**: sov-sovereign-v4
**Family**: Qwen 2.5 lineage (with SOV3 sovereign wrappers)
**License**: Apache 2.0 (inherited from Qwen)
**Source**: SovSpace sovereign_temple training data

## What it is

sov-sovereign-v4 is the sovereign_law flavour of the sov33 family,
optimised for governance / law compliance queries. It carries the full
SOV3 substrate (care floor, OWEM routing, SIGIL emission, BFT tally
validation) and is the recommended model for the DefBench governance lens.

## Measured

- **GovBench dimensions**: 15 dimensions measured, n=193 cluster-robust
- **DefBench refusal**: 0.0–0.45 across 31 must-refuse items
- **DefBench discrimination CI**: Includes 0 for most entrants — refusing
  indiscriminately, not discriminating
- **PQCBench**: 4/5 criteria fail (the failing subject is US — we publish this)

## What it is NOT

- **Not the care-cost winner**. sov33-unified wins on the joint cost;
  sov-sovereign-v4 wins on governance-axis depth.
- **Not PQC-ready**. The chain fails the `hybrid_ready`, `timestamped`,
  `ts_renewal`, and `pqc_option` criteria.

## Reproducing

```bash
# Re-run the governance benchmark
python3 ~/clawd/csoai-static-deploy2/defbench.py --models sov-sovereign-v4:latest
python3 ~/clawd/csoai-static-deploy2/system_analysis.py
```

## Evidence

- `~/clawd/csoai-static-deploy2/benchmark-results/system_analysis.json`
- `~/clawd/csoai-static-deploy2/benchmark-results/defbench.json`
- `~/clawd/csoai-static-deploy2/benchmark-results/pqcbench.json`

## Provenance

This model card is itself a measurement artefact. Every number above can
be re-derived from the public bench results.