# ASSETS MANIFEST — SOVOS single source of truth

**Every external projection (HF, Kaggle, PyPI, arenas) is generated from this file.**

If you want to change a model card, dataset description, or pricing — you
change THIS file (or the asset files it points at), then run `make project`.
No hand-editing on external platforms. Ever.

---

## Models

| Asset ID | Source file | Type | Status |
|---|---|---|---|
| `sov33-ultimate-sovereign` | `assets/models/sov33-ultimate-sovereign.model-card.md` | model_card | REAL (cloned from HF user `csoai/sov34-1p5b` lineage) |

## Datasets

| Asset ID | Source file | Type | Status |
|---|---|---|---|
| `govbench` | `assets/benchmarks/sovos-etsi-304-223-benchmark-v0.1.json` | benchmark | REAL (3 items in scaffold; full 479-item corpus needs migration) |
| `govbench-card` | `assets/datasets/metadata/govbench_dataset_card.md` | card_template | REAL |
| `leaderboard-space` | `assets/datasets/metadata/space_card.md` | space_card | REAL |

## Benchmark cards

| Asset ID | Source file | Type |
|---|---|---|
| `etsi-304-223` | `assets/benchmarks/sovos-etsi-304-223-benchmark-v0.1.json` | dataset (3 items, scaffold corpus) |

## 3KB Sigils

| Asset ID | Source file | Type |
|---|---|---|
| `sovos_GOV` | `assets/cards/sovos_GOV.3kb` (3072 bytes) + `.json` | sigil |
| `fish_CARE` | `assets/cards/fish_CARE.3kb` (3072 bytes) + `.json` | sigil |

## Tick sigils (DEFONEOS sprints)

Source: `_site/tick-*.json` (73 sigils from tick-100 to tick-247+)
Status: REAL, exported via `_site/` allowlist during sprint runs.

---

## Pipeline rule

1. Every external projection (HF model card, Kaggle dataset metadata, PyPI
   README) is generated from this manifest + the files it references.
2. To update: edit this file (or the asset), run `make project`.
3. `make project` regenerates `exports/{huggingface,kaggle,pypi,arenas}/*`.
4. Intake (arena results, eval logs, error vectors) lands in `intake/` and
   updates the manifest's `intake_sources` field.

## Honesty footer

This manifest contains ONLY what is real on disk in `assets/`. Claims that
exist only in briefs/marketing material (e.g. "479-item GovBench" when the
JSON on disk has 3 items) are marked `REAL` or `SCAFFOLD` so projection
outputs don't accidentally over-claim.

---

*CSOAI Ltd · UK Companies House #16939677 · Sovereign by Design*
