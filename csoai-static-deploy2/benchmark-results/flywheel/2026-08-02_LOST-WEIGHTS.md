# LOST-WEIGHTS Register — ollama fleet wipe 2026-08-02 (~07:03 BST)

The local ollama blob store was wiped mid-spread on 2026-08-02 (47/103 models
measured and checkpointed before the loss; see
`2026-08-02_full-local-spread-103models.json` and commit `1cf9f5e`).

Most of the fleet was rebuilt from surviving recipes (spawn_clans.py,
Kaggle notebook personas, on-disk `Modelfile_*_mined`, sov_space_draw.py,
honey_miner). The following models had **custom-trained weights with no
surviving recipe or artefact** and are declared honestly LOST — they must
never be silently substituted by a same-named persona model, because a
model NAME is not a model (join on weights, not names — registered lesson).

## Lost models (8)

| Model | Why lost |
|---|---|
| `sov33-dist-c1` | Distilled custom weights; no checkpoint survived the wipe |
| `sov33-dist-c2` | " |
| `sov33-dist-c3` | " |
| `sov33-evolved-c1` | Evolved-run weights; Modelfile referenced a blob that no longer exists |
| `sov33-evolved-c3` | " |
| `sov33-evolved` | Base evolved weights lost (see `Modelfile.sov33-evolved-v6` dangling blob ref) |
| `sov33-v6` | Byte-identical to evolved lineage per prior alignment; blob lost |
| `sov33-evolved-patched` | FROM sov33-evolved (lost) + mined patch — base gone, unrebuildable |

## Rebuilt-with-register-note (measurement-integrity preserved, provenance noted)

- `clan-redress-*` (12 postures): regenerated 2026-08-02 with the spawn_clans
  SPINE+posture pattern and a redress-dimension remit. Original remit text was
  lost with the wipe; these models were **never previously measured**, so no
  measurement-integrity break — first measurement is their canonical baseline.
- `*-patched` variants (clan-sovereignty-cited/refusing, sov-sovereign-v4,
  sov33-v7): rebuilt from the current on-disk mined-policy Modelfiles. The
  earlier patched-generation policy snapshots were lost; the corpus grew
  between generations, so policy content is closest-available, not identical.

## Rule going forward

Any future spread run must treat these 8 names as UNMEASURABLE-LOST, not as
"missing → recreate". If the underlying distill/evolve pipeline is re-run and
produces new weights under these names, that is a NEW model generation and
must be recorded as such in the run manifest.
