# SOV FRONTIER COMPUTE GATES — canonical, in-memory. ACTUAL 2026 frontier. Confirmed HF params 2026-07-16.
# CORRECTION: an earlier version used one-generation-old ids (V3/K2/GLM-4.5). This is the real current frontier.

## THE ROSTER (bleeding-edge, current-generation, confirmed from HF)
| Expert | Model | Total params (HF-confirmed) | License | int4 GB | GPUs@80GB |
|---|---|---|---|---|---|
| flagship MoE | Kimi-K2.6           | 1.059T | other (read terms) | 529 | 7 (multi-node) |
| frontier MoE | DeepSeek-V4-Pro     | 861.6B | MIT ✓ | 431 | 6 |
| frontier MoE | GLM-5.2             | 753.3B | MIT ✓ | 377 | 5 |
| efficient    | DeepSeek-V4-Flash   | 158.1B | MIT ✓ | 79  | 1×80GB ✓ |
| efficient    | Qwen3.6-35B-A3B     | 35.9B  | Apache-2.0 ✓ | 18 | 1 GPU ✓ |

## THE FORK (memorize — stop re-deriving)
### PATH 1 — CALL (token API). Govern frontier NOW, ZERO GPU on our side.
  - Prompt -> their hosted endpoint -> our care-gate+SIGIL wraps+signs. ~$0.15-2/M tokens.
  - Reachable: NVIDIA NIM (connected, remote) hosts DeepSeek-V4/Kimi-K2.6/GLM-5.2/Qwen3.6 (all appeared as nvidia/*-NVFP4 repos).
  - This governs the TOP-3 today with no GPU rental. LIMIT: rent-per-call, cannot edit inner weights.
### PATH 2 — HOST (own weights, rented GPUs). To LoRA/edit inner weights.
  - Kimi-K2.6 529GB->7GPU · DeepSeek-V4-Pro 431GB->6GPU · GLM-5.2 377GB->5GPU (all multi-GPU, real $).
  - DeepSeek-V4-Flash (158B->1×80GB) + Qwen3.6-35B (18GB->1GPU) = FRONTIER-FAMILY, SINGLE-GPU, LoRA-able cheap.
  - Modal paygo does all. Lightning free hours fit the single-GPU ones.
  - DEAD: SSH micro boxes (1-2GB RAM) cannot host/spread these. Mac unreachable+too small. From-scratch pretrain infeasible.

## THE DECISION (alphabet-binding)
- GOVERN top-3 NOW (no GPU $): PATH 1 — wire NVIDIA NIM + APIs into SOV4 shim, care-gate+sign V4-Pro/K2.6/GLM-5.2 output.
- OWN/EDIT weights cheap+frontier-family: LoRA DeepSeek-V4-Flash (158B, MIT, 1-GPU) or Qwen3.6-35B on the 4,645-corpus. Modal single-GPU.
- OWN/EDIT the full flagships (V4-Pro/K2.6/GLM-5.2): Modal multi-GPU (5-7 GPU), real $, do after the single-GPU proof.

## STANDING (anti-drift)
- Confirm params+license from HF card before GPU $ (done for all above).
- CALL(govern) vs HOST(LoRA) are DIFFERENT deliverables — never conflate.
- Use CURRENT-generation ids only: V4 not V3, K2.6 not K2, GLM-5.2 not 4.5, Qwen3.6 not Qwen3.
- Dead paths (never re-propose): SSH-spread big models on micro boxes; Mac host 300GB+; from-scratch pretrain.
