# OOWM Seed v30.1 — balanced (balanced_v31 config)

**86,182 → 68,450 docs after domain-balance passes.** The seed that powers
`csoai.org/api/eat-tick` oowm_score (KV `EAT_OWEM`/`owem_seed`).

## Why this config
Two balance passes reclassified ~3.9K docs to their correct sovereign-axis domain
(man/big-moe/free/small-moe/bridge/queen were under-represented and getting drowned
by mom/oowm/king noise) and capped the three heavies at 2.2× mean.

## Layout
- `balanced_v31/data.jsonl` — 68,450 rows: `{source, domain, text}` (FULL text)
- domains: king/oowm/mom 13,465 each (cap) · sovereign 7,813 · quant 6,383 ·
  council 3,595 · small-moe 2,966 · free 2,336 · big-moe 1,346 · bridge 1,279 ·
  man 1,221 · queen 1,116 (corpus floor — maternal text genuinely rarer, no fabrication)

## Lineage
v7 MMR 1,273 → v14 3,358 → v21 23,096 → v27 69,196 → v29 75,087 →
v30 86,182 (DEFONEOS packs) → **v30.1 balanced 68,450**

## Related
- Pre-balance snapshot: `csoai/oowm-ground-truth-v9` configs (train / sov_signal)
- Live serve: KV EAT_OWEM/owem_seed (t[:200] for 25MiB ceiling); this config = full text

_Owned by CSOAI. Signed/timestamped lineage in oowm-v9/oowm_receipt_v31.json._
