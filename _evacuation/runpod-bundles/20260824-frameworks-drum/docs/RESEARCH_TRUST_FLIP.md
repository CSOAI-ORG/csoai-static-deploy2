# TRUST FLIP — deep research: the nonconformity score that can clear coverage

> The #1 gap. The drum's 90/10 conformal router is `trusted:false` because no nonconformity
> score passed realized-coverage (3× negative: ensemble-disagreement 0.53/0.37, text-hedge no
> signal, Gemini confidence 429). This note records the **research-validated signals** that were
> never tried, and why they fit the drum's existing conformal framework. Doctrine: [BET] until a
> score actually clears coverage.

## What failed (and why)

| Attempt | Result | Why it failed |
|---|---|---|
| 3-model ensemble disagreement | 0.53 / 0.37 (≥ α=0.05) | disagreement ≠ probability of being right; it's an *uncertainty proxy*, not a correctness score |
| Text-hedge lexicon | no signal | terse verdicts ("YES" ≤8 chars); no hedging to detect |
| Gemini raw confidence | quota-429 | never scored; also raw confidence is poorly calibrated |

## The research-validated candidates (never tried)

### 1. Token-entropy conformal prediction (TECP) — best fit
Learned a token-entropy (predictive-uncertainty) nonconformity score and apply split-conformal
calibration. This is the **canonical conformal-nonconformity score** for generative outputs and
maps directly onto the drum's existing `router/conformal_router.py` — swap the score, not the
framework. `s(x) = -Σ_t log p(x_t | x_<t)` (mean per-token negative-log-likelihood / entropy).
Source: [TECP: Token-Entropy Conformal Prediction for LLMs](https://www.semanticscholar.org/paper/TECP%3A-Token-Entropy-Conformal-Prediction-for-LLMs-Xu-Lu/1b32e08949b23866a1fe7c7895f615bc7e4bf425).

### 2. Confidence-weighted self-consistency
Confidence (per-response prob) multiplied into the self-consistency majority vote outperforms
plain self-consistency at predicting correctness — a direct correctness correlate.
Source: [Confidence Improves Self-Consistency in LLMs](https://research.google/pubs/confidence-improves-self-consistency-in-llms/).

### 3. Lachesis — structural properties of reasoning paths
Predicts inference accuracy from the *structure* of the reasoning path (not the answer), which is
model-agnostic and needs no reference label.
Source: [Lachesis: Predicting LLM Inference Accuracy](https://conf.researchr.org/details/icse-2025/deeptest-2025-papers/6/Lachesis-Predicting-LLM-Inference-Accuracy-using-Structural-Properties-of-Reasoning-).

### 4. Learned correctness models
A calibrated, model-agnostic predictor of whether an answer is correct, trained from historical
patterns — the cleanest "score" if a labeled set exists.
Source: [Generalized Correctness Models](https://huggingface.co/papers?q=answer%20phrasing).

## Recommendation

The **TECP token-entropy nonconformity score** is the highest-value next attempt: it's a
conformal-native score (drop into the existing router), it's computable from a single model's
token probabilities (no 3-model fleet needed), and it directly targets the quantity the router
must bound — `Pr[auto AND wrong] ≤ α`. Requires a decoder that exposes per-token logprobs for the
80 labeled probes (local MLX or a fleet model on the pod). The trust flip stays `trusted:false`
and honest until this score (or confidence-weighted self-consistency) clears realized-coverage.

## Status
- [GATE] execution needs a decoder with token logprobs (pod fleet, or local 3090 model).
- [BET] token-entropy will clear coverage — *disconfirming evidence*: token-entropy is a
  measure of *uncertainty*, and uncertainty does not always equal *wrongness* (a model can be
  confidently wrong). The test is empirical: it only flips trust if the realized-error bound
  actually ≤ α on the 80 measured labels. No claim made until it does.

## Experiment log (2026-08-23 — both attempts blocked, honestly)

| Attempt | Signal | Result |
|---|---|---|
| #3 — Gemini calibrated confidence | s = 1 − confidence | **quota-429** after 17/79 calls → only 17 scored (< 20 → coverage inconclusive). NOT trusted. |
| #4 — token-entropy (TECP) | s = mean per-token −log p | **`responseLogprobs` → 400 "Logprobs is not enabled for this model"** — the signal is NOT computable on the available Gemini model. |

**Conclusion: the trust flip is NOT achieved.** Both new signals are blocked by model-capability
gates (quota-429 for confidence; logprobs disabled for token-entropy), not by the signal being
wrong. `feeds/router_trust.json` stays `trusted:false` (last valid realized-error 0.3684 from the
2021 ensemble attempt — the marker is never re-decided, only written by a passing coverage check).
The calibration set was fully recovered (80 measured labels, ledger #14/#15 safety-net restore)
— no data lost. Next: a decoder that exposes per-token logprobs (a local open model via MLX, or a
pod Ollama/3090 model) to actually compute token-entropy.
