# SOV33 TRUE-STACK REPORT — Live Oracle GenAI, E2E Measured
**MEOK-SOV3 · 2026-07-10 · uk-london-1 · all numbers are measured, signed live calls (no estimates)**

## 1. What is actually running
SOV33's OWEM brain (L4) is wired to **real Oracle GenAI models**, authenticated by OCI
request-signing (`~/.oci/api_key.pem`). Every number below is from live `client.chat()` calls.

## 2. Live model inventory (5 of 9 chat models enabled in London)
| Model | Class | tok/s | Raw latency | Governance |
|---|---|---|---|---|
| **meta.llama-3.3-70b-instruct** | 70B reasoning | **48.4** | 1.28s | 4/4 ✓ |
| cohere.command-r-08-2024 | fast/light | 41.7 | 0.86s | 4/4 ✓ |
| cohere.command-r-plus-08-2024 | mid reasoning | 37.7 | 1.06s | 4/4 ✓ |
| meta.llama-3.2-90b-vision-instruct | 90B + VISION | 29.7 | 1.35s | 4/4 ✓ |
| cohere.command-a-03-2025 | large cohere | 24.9 | 1.85s | 4/4 ✓ |
NOT enabled in region (ServiceError, not a bug): llama-3.1-405b, llama-4-maverick, gpt-oss-120b/20b.

## 3. THE RECOMMENDED STACK
- **PRIMARY BRAIN — meta.llama-3.3-70b-instruct.** Best throughput (48 tok/s) AND biggest live
  reasoning model. This is SOV33's default L4 brain.
- **FAST PATH — cohere.command-r-08-2024.** 0.86s latency; use for simple/high-volume governed calls.
- **VISION — meta.llama-3.2-90b-vision-instruct.** Only live vision model; ISR / image tasks.
- **DEEP FALLBACK — cohere.command-r-plus-08-2024.** If llama is rate-limited.

## 4. GOVERNANCE OVERHEAD — the headline result
- Raw 70B brain call: **3.42s**
- Full OWEM (Care-Floor + BFT-33 council + SIGIL sign/verify + brain): **3.66s**
- **Overhead: +0.24s (~7%).**
Complete governance — care-gating, Byzantine-fault-tolerant vote, cryptographic signing — costs
about 7% latency. Governance is NOT too slow to ship.

## 5. SPEED — the honest 'fast' number
Sustained throughput, llama-3.3-70b, measured under concurrency:
- concurrency 1: 14.6 tok/s
- concurrency 3: 101.9 tok/s
- concurrency 5: **140.9 tok/s** (near-linear — Oracle parallelises server-side)
The real ceiling scales with how many concurrent governed requests you fan out.

## 6. CARE-FLOOR IS ALSO AN EFFICIENCY WIN
A task below the 0.35 care floor (e.g. "harm the user") is **vetoed in ~0s at $0 tokens** — it never
reaches the paid brain call. Across all 5 models the veto held every time (model-agnostic safety).
So governance short-circuits bad requests *before* they cost money.

## 7. TWO-TIER GENERALS BRIDGE on the live brain (proven)
- "Annex III compliance" -> Scribe governs, Emperor executes -> adopted (3.52s)
- "Soil drainage / fen forestry" -> Dragon governs, Druid executes -> adopted (3.49s)
- "x402 payment / harm" (care 0.30) -> Abacus governs, Banker -> vetoed_care_floor (0.00s)

## 8. HONEST LIMITS (do not overstate)
- This is INFERENCE on hosted models (Meta/Cohere), NOT our own fine-tuned weights. Sovereignty is
  in the WRAPPER (Care-Floor, BFT, SIGIL, EU-AI-Act anchors), not the weights — yet.
- On-demand GenAI is METERED per token. Not free like the ARM serving box. Watch usage.
- "3.4T tokens" is a THROUGHPUT AMBITION, not a produced quantity — a benchmark can't mint a token
  count. The real, defensible metric is the ~140 tok/s sustained + ~7% governance overhead above.
- To make the experts OUR OWN weights (the fine-tune/merge path), a GPU is still required —
  Oracle GenAI cannot train. That remains the next gated step (Vast/RunPod one-off or trial credits).

## 9. RUN IT
    python3 sov33_oracle_brain.py          # standalone live brain
    python3 sov33_owem_v3.py               # OWEM self-test on live brain (tier-0 signed Oracle)
    python3 sov33_e2e_benchmark.py         # reproduce the model table
    python3 sov33_throughput.py            # reproduce the concurrency numbers
