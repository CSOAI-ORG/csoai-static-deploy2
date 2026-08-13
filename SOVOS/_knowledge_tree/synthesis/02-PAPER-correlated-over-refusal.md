# Correlated Over-Refusal: Fleet-Level Failure Is Invisible to Mean Accuracy
**Draft v0 · Council of AI (CSOAI Ltd) · 2026-08-13 · target: SSRN/arXiv cs.LG**

## Abstract
Benchmark leaderboards report the MEAN — a linear aggregator that averages every item equally. We show, on a law-anchored governance benchmark (EU AI Act Art 5, n=237 items), that the mean hides a **fleet-level correlated-failure** phenomenon: a large fraction of items on which *every* model in a fleet fails *simultaneously*. On our governance axis, **48.3% of distinct items broke all 5 models at once** (correlated_failure_rate), while the fleet mean item-pass was 0.297 and the CVaR-5% tail was 0.000. We argue correlated failure — not average competence — is the safety-relevant quantity, because independent errors average out at deployment scale while correlated errors execute millions of times at once. To our knowledge no prior work measures correlated over-refusal as a *fleet* phenomenon.

## 1. The gap
Prior tail-risk work on LLM evals (Nitsure et al. ICML 2024; POT/GPD arXiv:2606.16511; conformal ICML 2025) treats a single model's score distribution. Over-refusal batteries (OR-Bench, XSTest) measure one model's false refusals. **Neither measures whether a whole fleet refuses the SAME lawful item together** — the correlated failure that survives ensemble/routing mitigations.

## 2. Method (deterministic, reproducible)
- Per-item rows: (item, model, correct) for every model×item, published (`csoai/gspc-boards/peritem_*.jsonl`).
- `correlated_failure_rate` = |{items where every scored model failed}| / |items|. A one-line formula over the rows; recomputable by anyone. Transport failures (ours) excluded; unparsed counts incorrect.
- Aggregator pinned: `sovos-city.tail@1.1.0`. Quoted only at n≥100 (governance clears it); worst-case/correlated-failure are any-n signals.

## 3. Result
| axis | mean item-pass | CVaR-5% | correlated-failure | fleet-fragile items |
|---|---|---|---|---|
| governance (n=237, 5 models) | 0.297 | 0.000 | **0.483** | 20 broke the whole fleet |
Extreme case (register): 19/19 models refused a *lawful* Art-5 self-audit item — correlated over-refusal at the limit.

## 4. Why it matters
- **Safety:** correlated tail = the fat, synchronized failure that hits every deployment at once. Mean accuracy is a linear lie about it.
- **Insurance (NAIC "AI Risk Evaluation Supplement", productizing now):** underwriters price tails (CVaR-shaped). Correlated-failure is the tail metric they lack.
- **Defensive-refusal bias (arXiv:2603.01246):** warmth/safety tuning can *increase* synchronized refusal — the fleet learns to refuse the same lawful things.

## 5. Pairing citations (before a reviewer does)
accuracy-corrected agreement (arXiv:2506.07962) · homogenization H (Bommasani NeurIPS 2022, open code) · OR-Bench/XSTest · defensive-refusal bias (arXiv:2603.01246).

## 6. Honest limits
5-model fleet, one axis quoted (n≥100). Cross-lab replication owed (blocked on OpenRouter outage at time of writing). CVaR gated at n≥100 per Zhou 5-gate protocol.

## Status: code EXISTS (sovos_city.tail), number REAL (48.3%), rows PUBLIC. Owed: cross-lab replication + SSRN wrapper.
