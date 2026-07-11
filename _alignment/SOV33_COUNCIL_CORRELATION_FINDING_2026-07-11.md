# 🜏 SOV33 — MEASURED council error-correlation (Crown Jewel #1)

## Result (live Oracle brains, 10-item governance/factual battery, ground-truth)
- Cohere command-r accuracy: 0.70
- Meta llama-3.3-70b accuracy: 0.80
- both-wrong-together: 2/10
- **ERROR CORRELATION rho = 0.76** (Cohere lineage vs Meta lineage)

## Honest implication (this CHANGES a standing claim)
rho = 0.76 is HIGH. Per the 2026 literature (arXiv 2605.29800 "Nine Judges, Two Effective Votes";
2603.06612 "Consensus is Not Verification"), correlated voters give little independent information —
so **L2 majority-vote / "BFT-33 quorum" is NOT a correctness guarantee on this council.** Two correlated
models ~= one model. We must STOP presenting quorum voting as fault tolerance for correctness.

## What IS sound
- BFT still matters for LIVENESS / crash-fault tolerance (a brain being down), and for GOVERNANCE
  bright-line refusals (those run before the brain, no voting involved).
- The valuable signal is DISAGREEMENT (8/10 here), not agreement.

## The fix (Jewel #1) — adopt
1. Escalate-don't-average: on checker disagreement, defer to the stronger brain or ABSTAIN (defer-to-resample),
   never take a majority of correlated voters.
2. Report rho as a tracked number (like care-scorer precision). rho>=0.7 = theatre; rho<0.4 = real diversity.
3. To LOWER rho, add a genuinely different lineage as a third checker (e.g. a local Qwen or Gemma via Ollama).

## Caveats (do not overclaim)
- Only 2 lineages measured (the two live on Oracle uk-london-1); small n=10 battery — DIRECTIONAL, not a benchmark.
- I wrote the battery + labels; a clean measure needs independent items and a larger n.
