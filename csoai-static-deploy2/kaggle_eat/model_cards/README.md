# CSOAI Model Cards — Series A

This directory contains the canonical model cards for every SOV family
model published to HuggingFace and Kaggle. Every card is a measurement
artefact — every number must be re-derivable from the public bench
results, or the card is wrong.

## Cards

| Model | Card |
|-------|------|
| sov33-unified | [sov33-unified.md](sov33-unified.md) |
| sov-sovereign-v4 | [sov-sovereign-v4.md](sov-sovereign-v4.md) |
| sov33-evolved | [sov33-evolved.md](sov33-evolved.md) |

## How to add a card

1. Run the bench (the model appears in `benchmark-results/`).
2. Copy the canonical numbers (do not invent).
3. List what the model is NOT. Credibility is honesty about limits.
4. Point to the evidence file path.

## Anti-patterns

- Do not publish a card without bench results.
- Do not claim "certified safe" (we are tamper-evidence, not certification).
- Do not claim PQC-ready unless `pqcbench.json` passes 5/5 criteria.
- Do not claim "best in class" without the care-cost board entry.

## Provenance

Every model card in this directory is itself a measurement artefact.
The numbers inside can be re-derived from the bench results. If a card
cannot be reproduced, the card is wrong, not the bench.