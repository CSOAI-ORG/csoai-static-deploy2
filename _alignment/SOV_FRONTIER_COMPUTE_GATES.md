# SOV FRONTIER COMPUTE GATES — canonical, in-memory. Bleeding-edge roster ONLY. No smallest-first.
# Confirmed HF params 2026-07-16. This is the map so we are NEVER lost in time on compute again.

## THE ROSTER (bleeding edge, confirmed, nothing else)
| Expert | Model | Total params (HF-confirmed) | License |
|---|---|---|---|
| MoE-1 | Kimi-K2      | 1.03T  | "other" (read terms) |
| MoE-2 | DeepSeek-V3  | 684.5B | (read card) |
| MoE-3 | GLM-4.5      | 358.3B | MIT ✓ |

## THE GATE THAT SETS COST (weights-in-memory, int4)
| Model | int4 GB | GPUs @80GB | Path |
|---|---|---|---|
| Kimi-K2     | 513 GB | 7 (multi-node) | HOST = biggest $ |
| DeepSeek-V3 | 342 GB | 5              | HOST = real $ |
| GLM-4.5     | 179 GB | 3              | HOST = smallest of the three |

## THE REAL FORK — two ways to use a frontier model (memorize this, stop re-deriving it)
### PATH 1 — CALL (token API). Someone else hosts weights. NO GPU on our side.
  - GOVERN a frontier model TODAY: send prompt -> their endpoint -> our care-gate+SIGIL wraps the answer.
  - Reachable NOW: NVIDIA NIM (connected, remote), DeepSeek API, Kimi/Moonshot API, GLM API.
  - Cost: ~$0.15-2 / M tokens. This is how SOV4 governs the top-3 with ZERO GPU rental.
  - BLOCKER: renting the brain per call. Cannot LoRA / edit inner weights this way. Governance-only.
### PATH 2 — HOST (own the weights on rented GPUs). Needed ONLY to LoRA/edit inner weights.
  - Modal paygo multi-GPU: DeepSeek 5-GPU, Kimi 7-GPU nodes. Real money, reachable.
  - Lightning free A100/H200: limited hours — fits GLM (3-GPU), tight for 684B+.
  - BLOCKER: SSH micro boxes (owem/oracle, 1-2GB RAM) CANNOT host or spread these. Mac unreachable+too small.
    SSH-spreading a 300GB+ model across tiny boxes = physically impossible (RAM + interconnect). Dead path, stop asking.

## THE DECISION (alphabet-framework binding)
- To GOVERN the top-3 NOW (no GPU spend): PATH 1 — wire NVIDIA NIM + native APIs into SOV4's shim. Care-gate+sign their frontier output. REACHABLE TODAY.
- To OWN/EDIT weights (LoRA the frontier on our 4,645-corpus): PATH 2 — Modal multi-GPU. GLM-4.5 (3-GPU) is the cheapest FRONTIER host, NOT a downgrade — it IS bleeding-edge (MIT, 358B).
- Kimi-K2 (1.03T) = the trillion-param flagship. Highest host cost (7-GPU). Govern via API first, host last.

## STANDING (anti-drift)
- Confirm params+license from HF card before any GPU $ (done for all 3 above).
- "Govern via API" and "host+LoRA" are DIFFERENT deliverables — never conflate.
- Dead paths (memorize, never re-propose): SSH-spread big models on micro boxes; Mac hosting 300GB+; from-scratch pretrain.
