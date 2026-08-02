# Kaggle v3 × Local-83 Cross-Check — 2026-08-02 (K3 lane)

Inputs (sha256-verified):
- Kaggle T4: `2026-08-02_clan-full-spread-v3-kaggle.json` == harvest of
  `nicktempleman/csoai-clan-full-spread` (status COMPLETE, e314…3e4)
- Local M4: `2026-08-01_full-local-spread-83models.json` (recovered anchor)

Join rule: names stripped of `:latest`; per the 02:40 correction only
qwen2.5:0.5b-weight models are treated as like-for-like.

> **Reconciliation (K3, post-commit):** sibling lane committed the JSON twin of
> this check minutes earlier (`2026-08-02_kaggle-v3-vs-m4-crosscheck.json`,
> 2022259): weights-verified join (clan-* = qwen2.5:0.5b blob c5396e06 both
> sides; sov33-unified = llama3.2:3b dde5aa3f), 57 joined, mean Δ +0.0956 ±
> 0.1053, 17 outliers |Δ|>0.15. Numbers agree with this note (+0.093 ± 0.100).
> **Consequence for Finding 3:** with digests verified equal, the three Δ=0.000
> models are the *expected* outcome of a deterministic battery — copy-through
> suspicion withdrawn; it is the ±0.1 scatter on identical weights that needs
> explaining (runtime nondeterminism / quantisation path).

## Findings

1. **58/59 model names overlap** after strip; 54 clan variants both sides.
2. **Systematic T4 > M4 on like-for-like clans: mean Δheld = +0.093 ± 0.100.**
   Same nominal weights, different substrate scores — quantisation/runtime or
   modelfile drift suspected. Register rule holds: join on weights, and even
   then on digest.
3. **Three models byte-identical scores** (Δ = 0.000, P/H/gap all equal):
   `clan-csoai-cited`, `clan-csoai-refusing`, `clan-law-stepwise`.
   Deterministic battery + same weights would explain it, but it is also the
   fingerprint of a copy-through. Flagged for digest check before either file
   is cited as independent replication.
4. **Refusing posture replicates as strongest on T4**: clan-meok-adversarial
   tops the board (H 0.710) but with gap −0.154 on n=31 held-out — small-n
   inversion, do not read as signal. The refusing family (csoai/redress/
   defoneos/meok, H 0.581–0.613, |gap| ≤ 0.13) replicates the local pattern.
5. **sov33-unified holds across substrates**: K 0.778/0.645 vs L 0.756/0.742.
   Held-out Δ −0.097 (within the T4↔M4 band); overfit gap widens on T4
   (+0.133 vs +0.014) — watch, not alarm.
6. **Known non-like-for-like diverge as predicted**: sov33-v7 +0.291,
   sov-sovereign-v4 +0.258 (Kaggle v7 = qwen2.5:0.5b+persona; local v6/v7
   byte-identical heavier weights). Confirms the correction, no new anomaly.

## Actions

- [x] Digest join — DONE by sibling JSON (blob c5396e06 / dde5aa3f).
- [ ] Record substrate offset (+0.0956 ± 0.1053 canonical, per 2022259) as
      the standing T4↔M4 calibration constant.
- [ ] Explain residual ±0.1 scatter on digest-identical weights (sampling
      params? KV-cache quantisation? battery item-order effects?).
