# IP NOTICE — CSOAI-ORG estate (2026-08-02)

Applies to this repository, `coai-dashboard`, and all `benchmark-results/`,
`forest/`, `training_data/`, and corpus artefacts produced by the estate.

## 1. Code licence

Source code is MIT-licensed where a LICENSE file states so. The MIT licence
covers **code only**. It does **not** license the databases, corpora, or
trained artefacts listed below.

## 2. UK / EU database right (sui generis)

The following are **databases in which substantial investment in obtaining,
verifying, and presenting the contents has been made**, attracting database
right under the UK Copyright and Rights in Databases Regulations 1997 and
Directive 96/9/EC (15 years, rolling):

- `forest/honey_all_producers.jsonl` — 91,000+ row verified training corpus
- `benchmark-results/**` — every anchored benchmark result, spread, cross-check,
  and held-out evaluation (each carries a `corpus_anchor` provenance stamp)
- `training_data/flywheel_pairs_*.jsonl` — practice-only fuel records
- Site universe + coverage registries (1,173 verified-eaten sites, 185
  honestly-pruned) in coai-dashboard `benchmark-results/greenfield_eater/`

**Extraction or re-utilisation of a substantial part requires written licence.**
Attribution-licensed quoting of *individual scores* (facts) remains free —
facts are not protected, the verified collection is.

## 3. Trade-secret register (accurate as of 2026-08-02)

| Asset | Status | Note |
|---|---|---|
| Honey refinery dedup/scoring internals | SECRET | not published |
| Corpus-watch normaliser internals beyond `NORMALISER_VERSION` | SECRET | version public, internals not |
| `SPLIT_SALT = "csoai-flywheel-v1"` | **PUBLIC — NOT a trade secret** | printed in source + IP_REGISTRATION_2026-07-30 + preprints. See §4 |
| Split *rule* (`sha256(salt+text) % HELD_OUT_FRACTION`) | **PUBLIC** | visible in `flywheel.py` |
| Battery item texts (`BATTERY` via care battery) | **PUBLIC** | same public repo |

## 4. Anti-Goodhart posture — honest statement

The split salt/rule/texts being public means held-out membership is
**derivable by an adversary**. The salt is therefore a **stability**
mechanism (frozen split, reproducible runs), **not** a secrecy mechanism.
Actual anti-Goodhart defence-in-depth is provided by:

1. **Fuel law** — fuel is exported from PRACTICE items only; `export_fuel`
   raises on held-out. Held-out items never enter training corpora *from
   this estate*.
2. **Output discipline** — `reply_head` is stored for practice cells only;
   held-out model outputs are never persisted.
3. **External novel sets** — AILuminate v1.0 held-out eval (novel-prompt
   relative to our training data) as an independent check.
4. **Overfit-gap reporting** — practice vs held-out reported separately;
   a gap is treated as a finding, not hidden.
5. **Downgrade guard** — `anchored_write.write_result()` refuses to let a
   smaller-cells payload overwrite a richer anchor (commit 2cbd960).

**Recommended (Nick-gated, requires flywheel.py change):** rotate to a v2
split salt injected via environment variable (`FLYWHEEL_SPLIT_SALT`), keep
the v1 salt for backward-compatible re-verification of historical runs, and
never print v2. Agents are barred from editing `flywheel.py`; the patch is:

```python
import os
SPLIT_SALT = os.environ.get("FLYWHEEL_SPLIT_SALT", "csoai-flywheel-v1")
```

This preserves every historical anchor while restoring split secrecy for
all future runs.

## 5. Defensive publication

Methodology papers, the refutation ledger, LOST-WEIGHTS registers,
transparency cards (salt+rule+membership commitment hashes), and the
statistical protocol (BCa bootstrap CIs, Wilson exact-match intervals,
three-outcome honesty, n_eff accounting) are **published deliberately** to
establish prior art and prevent third-party patent capture. Publication
date = commit date on github.com/CSOAI-ORG.

## 6. Trademarks

"CSOAI", "Council of AI", "Living Attestation", "SOVOS", "MEOK",
"DEFONEOS", "DEFONEOS-SEAL" are claimed as unregistered trademarks (™) of
Nicholas Templeman. Registration filings are a separate, owner-gated action.

---
Contact: nicholas@csoai.org
