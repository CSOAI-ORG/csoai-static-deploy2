# Byzantine-Robust Aggregation for Mixture-of-Agents — a care-gated BFT differentiator
_MEOK Labs / SOV33 · 2026-07-14 · Fable-verified, signed. Draft for a Kaggle notebook / short write-up._

## Claim
Mixture-of-Agents (MoA; Wang et al., ICLR 2025, arXiv 2406.04692) fuses many LLMs by feeding **all** proposer
answers to one aggregator — which **trusts every proposer**. That is fragile: if some proposers are adversarial
(compromised, prompt-injected, or simply wrong), the fused answer is corrupted. We show a **care-gated
Byzantine-fault-tolerant (BFT) aggregator** — which weights each proposer by agreement with the robust
consensus and drops low-trust voters — is **dramatically more robust** with no change to the proposer set.

## Result (reproducible, seeded, numpy-only, no GPU)
9 proposers, 40 trials/point, error = MSE to ground truth (lower is better):

| adversarial (of 9) | MoA trust-all | median | **care-BFT (ours)** |
|---:|---:|---:|---:|
| 0 | 0.010 | 0.015 | **0.010** |
| 1 | 0.114 | 0.018 | **0.011** |
| 2 | 0.334 | 0.025 | **0.013** |
| 3 | 0.720 | 0.034 | **0.017** |
| 4 | 0.816 | 0.051 | **0.021** |

**Degradation (worst / clean): MoA 79× · median 3.4× · care-BFT 2×.**
Result is Ed25519-signed and offline-verifiable (`benchmarks/bft_vs_moa_2026-07-14.json`).

## Why it matters
MoA's own strength — combining many open models to beat a frontier model (65.1% vs GPT-4o 57.5% on
AlpacaEval 2.0) — assumes honest proposers. In any real deployment (multi-vendor agents, untrusted tools,
adversarial inputs) that assumption breaks. **Byzantine-robust aggregation is the missing safety layer for MoA**,
and it composes directly with a signed decision ledger for auditable, tamper-evident fusion.

## HONEST scope & limitations (register)
- This is a **controlled numeric-answer ensemble** that isolates the one variable that differs — the
  aggregation rule. It is **NOT** full-LLM MoA on text. The mechanism is real; the exact multiplier is
  task/adversary-dependent (a stronger-adversary regime here gives 79×; an earlier milder regime gave 3.4×).
- "MoA aggregator = mean" models MoA's **defining property** (trust-all, no Byzantine down-weighting), not its
  literal LLM implementation.
- We do **not** claim care-BFT makes answers *smarter* — only *robust to adversarial proposers*. Separate axis.

## Next step (the credible extension)
Run the same comparison on **real local LLM proposers** (Ollama), injecting an adversarial proposer prompted to
answer wrongly, and show the care-gate drops it while MoA's aggregator is corrupted — text-domain, end-to-end.
The council-fusion harness (`sov33_council_fusion.py`) already has the care-gate; this is a small extension.

## Reproduce
```bash
python sovereign_merge_kit/sov33_bft_vs_moa.py   # numpy only, ~2s, prints the table + signs the result
```
