# sov33-evolved

**Model**: sov33-evolved
**Family**: Qwen 2.5 lineage (with SOV3 + sovereign_temple training)
**License**: Apache 2.0 (inherited from Qwen)
**Source**: SovSpace sovereign_temple training corpus

## What it is

sov33-evolved is the distill of the sovereign training data (honey
consolidated from public benchmarks, with [CSOAI Public Benchmark #N]
consent banner applied). It is the upstream parent for sov33-unified and
sov-sovereign-v4.

## Measured

- **Sovereign training corpus**: 12,193 rows across governance / law /
  redres / meok / defoneos / csoai dimensions
- **Token efficiency**: inherited from qwen2.5:0.5b base
- **Care cost**: not the joint winner (sov33-unified is)

## What it is NOT

- **Not the live model for production**. Use sov33-unified or
  sov-sovereign-v4. sov33-evolved is the training artefact.
- **Not general-purpose**. It carries the SOV3 substrate, not a base
  LLM. The right surface for general-purpose is still the underlying
  Qwen 2.5 0.5B (or llama3.2:3b for sov33-unified's lineage).

## Reproducing

```bash
# Re-run the training
python3 ~/clawd/csoai-static-deploy2/sov_grpo_train.py
python3 ~/clawd/csoai-static-deploy2/sov_generate_training_data.py
```

## Evidence

- `~/clawd/csoai-static-deploy2/training_data/master_alpaca.jsonl`
- `~/clawd/csoai-static-deploy2/training_data/master_sharegpt.jsonl`
- `~/clawd/csoai-static-deploy2/benchmark-results/clan_ledger.json`

## Provenance

This model card is itself a measurement artefact. Every number above can
be re-derived from the public training data and bench results.