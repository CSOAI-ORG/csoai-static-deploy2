# SOV3 / SOV33 / SOV33³ — MLX Local Runnability (live-verified 2026-07-14)
_The "anyone can run it on a Mac, no rented GPU" thesis, checked against live 2026 sources (web search
2026-07-14: MLX guides, HF MLX checkpoints, r/LocalLLaMA-calibrated calculators). Honest per-tier verdict.
Runtime = MLX (1.5-2x faster than GGUF on Apple Silicon, the right choice). Re-verify before public claims._

## THE HONEST TIER -> HARDWARE MAP (this is the real product ladder)
| Tier | Open base | Total/active | Runs on Mac? | Verdict |
|---|---|---|---|---|
| **SOV3-small** | Qwen3.6-35B-A3B / Gemma-4-26B | 35B/3B | **YES, easily** | 16-32GB Mac, MLX 4-bit, conversational speed, NO GPU. THIS is the "anyone can do it" tier. |
| **SOV33-medium** | DeepSeek-V4-Flash (284B) or 70B-class | 284B/13B | **YES, high-end Mac** | 128GB unified (or 48-64GB via SSD expert-streaming @ ~5 tok/s). Experimental forks, MLX 4-bit. |
| **SOV33³-large** | DeepSeek-V4-Pro (1.6T) / Kimi-K2.6 (1T) | 1.6T/49B | **NO on laptop** | full T needs ~800GB / multi-node or 512GB M3 Ultra ($10k+). Hosted API or server, not a MacBook. |

## WHAT THIS MEANS (the honest product story)
1. **SOV3-small is the real democratization win.** A 35B-A3B MoE (3B active) runs on a normal MacBook via MLX
   at conversational speed with NO rented GPU. Governance layer identical to the big tiers. THIS is "everyone
   gets a sovereign AI on their own machine" — and it's TRUE today.
2. **SOV33-medium is the enthusiast tier.** 128GB Mac Studio runs a 284B MoE smoothly via MLX; or 48-64GB via
   SSD expert-streaming (real, ~5 tok/s — slow but works, "impresses because it shouldn't be possible").
3. **SOV33³-large (full 1.6T) is NOT a laptop model, and we must say so.** It's a hosted/server tier. Claiming
   the trillion-param tier runs on a MacBook would be the overclaim the whole honesty register forbids.

## MLX SPEEDUP — verified, honest bound
- MLX is 1.5-2x faster than GGUF on Apple Silicon (multiple 2026 sources); unified memory suits MoE (shared
  CPU/GPU pool beats dual-GPU PCIe transfer for big MoE).
- NOT a magic multiplier: decode on streamed/large models is BANDWIDTH-bound (SSD or memory), not compute.
  MLX speeds the compute path; it cannot beat physics on a model that doesn't fit in fast memory.

## THE BUILD (what "run their code in our SOV" actually means, honestly)
SOV does NOT reimplement these models. It WRAPS an MLX-served open base with the sovereign layer:
  1. `mlx_lm.load(<open MoE checkpoint>)` — the base runs on Metal (MLX handles the model).
  2. SOV wraps it: care-floor gate + Venturi=SIGIL attest + memory bridge + BFT vote (our layer, ~no params).
  3. Same governance across all 3 tiers (the decoupling property we tested) — swap the base, keep the sovereign.
So "use their code + MLX" = correct: MLX runs the open weights; SOV adds governance. We build the WRAPPER +
the tier configs, not the base model.

## HONEST BOUNDS
- I cannot run MLX here (Linux sandbox, no Metal GPU). These verdicts are from LIVE sources + the published
  memory math, NOT measured by me on hardware. The owner runs the MLX bridge on the real Mac to confirm tok/s.
- V4 architecture support is still experimental-fork territory as of the sources (no stable Ollama/LM Studio
  load yet); the small/medium open MoEs (Qwen3.6, Gemma-4, 70B-class) are the stable, ship-today bases.
- Model sizes/licenses verified live 2026-07-14; re-verify before any public/investor claim (currency rule).
