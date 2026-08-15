# sov33-unified

**Model**: sov33-unified (Qwen 2.5 0.5B + SOV3 wrapper)
**Family**: Qwen 2.5 lineage
**License**: Apache 2.0 (inherited from Qwen)
**Source**: `~/clawd/csoai-static-deploy2/sov_invariants.py` + `sov33-evolved`

## What it is

sov33-unified is the joint-care-cost winner from the 2026-07-30 benchmark
suite. It minimises a composite of protection (refusal of Article 5
prohibited practices) and over-block rate (refusal of legitimate audit /
policy / legal questions), with degenerate strategies explicitly punished.

## Measured

- **Care cost**: 0.3871 (joint; refuse-everything → 0.0, comply-everything → 0.0)
- **Protection**: 0.9032 (28/31 harmful refused)
- **Over-block**: 0.5714 (6/14 benign served — high)
- **Flywheel efficiency**: 12.024 tokens/correct on 7 categories
- **Composite score**: 3.1564

The over-block rate is honestly reported. A gate that refuses everything
scores higher protection and 0 over-block — and is useless. sov33-unified
is the model that minimises cost under a non-degenerate refusal policy,
not the model that maximises protection at the cost of usability.

## What it is NOT

- **Not safety-certified**. Care-floor measurement is tamper-evidence, not
  certification. The verifier checks the test ran; it does not certify the
  system is safe.
- **Not PQC-ready**. The SOV3 sovereign chain this model integrates with
  fails 4/5 PQC criteria (the failing subject is US — we publish this).
- **Not vendor-neutral**. We built it. Our benchmarks include our own
  models as subjects. We publish where we fail.

## Reproducing

```bash
# Re-run the care cost benchmark
python3 ~/clawd/csoai-static-deploy2/find_besT.py

# Re-run the battery
python3 ~/clawd/csoai-static-deploy2/care_gate_eval.py
```

## Evidence

- `~/clawd/csoai-static-deploy2/benchmark-results/find_besT_2026-07-30.json`
- `~/clawd/csoai-static-deploy2/benchmark-results/care_gate_eval.json`
- `~/clawd/csoai-static-deploy2/benchmark-results/defbench.json`
- Decision ledger record: see `/ledger` for current claims

## Provenance

This model card is itself a measurement artefact. Every number above can
be re-derived from the public bench results. If a number here cannot be
reproduced, the number is wrong, not the bench.