# SOV3 / SOV33 / SOV33³ — MLX Local Runnability (2026-07-14)
_The "anyone can run it on a Mac, no rented GPU" thesis. CORRECTION 2026-07-14: an earlier version of this
doc asserted specific model figures (1.6T/49B/Kimi-K2.6) under a "live-verified" claim — those were NOT
supported by the web search (which returned TITLES only) and have been REMOVED. What the search titles
genuinely support: "DeepSeek V4 is a ~1-trillion-parameter open MoE." Everything else below marked
[UNVERIFIED] is a LEAD to confirm against a primary source (model card) before any public/investor claim.
Runtime = MLX (reported 1.5-2x faster than GGUF on Apple Silicon — snippet-level, treat as lead)._

## THE HONEST TIER -> HARDWARE MAP (this is the real product ladder)
| Tier | Open base (all sizes [UNVERIFIED] — confirm on model card) | Runs on Mac? | Verdict |
|---|---|---|---|
| **SOV3-small** | a small open MoE (laptop-scale, e.g. ~30B-class, few-B active) [UNVERIFIED name/size] | **YES, easily** | 16-32GB Mac, MLX 4-bit, NO GPU. THIS is the "anyone can do it" tier — small MoEs genuinely run on a MacBook. |
| **SOV33-medium** | a mid open MoE (~100-300B-class) or 70B-class dense [UNVERIFIED] | **high-end Mac** | 128GB unified, or less via SSD expert-streaming (slow). Experimental forks. |
| **SOV33³-large** | a real ≥1T open MoE (search titles support DeepSeek V4 ~1T; exact size/active/license [UNVERIFIED]) | **NO on laptop** | a genuine trillion-param model needs server/multi-node RAM. Hosted tier, NOT a MacBook. |

## WHAT THIS MEANS (the honest product story)
1. **SOV3-small is the real democratization win.** A small open MoE (few-B active) runs on a normal MacBook via
   MLX with NO rented GPU. Governance layer identical to the big tiers. THIS is "everyone gets a sovereign AI on
   their own machine" — and small-MoE-on-a-Mac is genuinely true today. (Exact base name/size [UNVERIFIED].)
2. **SOV33-medium is the enthusiast tier.** A high-end Mac (128GB) runs a mid-size MoE via MLX; smaller RAM via
   SSD expert-streaming (real technique, slow — tok/s figures [UNVERIFIED], owner to measure on the real Mac).
3. **SOV33³-large (a real ≥1T model) is NOT a laptop model, and we must say so.** It's a hosted/server tier.
   Claiming the trillion-param tier runs on a MacBook would be the overclaim the whole honesty register forbids.

## MLX SPEEDUP — reported (treat as lead, not measured)
- MLX is *reported* 1.5-2x faster than GGUF on Apple Silicon (2026 snippets — [UNVERIFIED] exact figure);
  unified memory is well-suited to MoE (shared CPU/GPU pool avoids the PCIe transfer a dual-GPU rig pays).
- NOT a magic multiplier (this is a reasoning claim, not a stat): decode on streamed/large models is
  BANDWIDTH-bound (SSD or memory), not compute — MLX speeds the compute path, it cannot beat memory physics.

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
- V4 architecture support is *reported* experimental-fork territory (no stable Ollama/LM Studio load yet) —
  [UNVERIFIED]; small/mid open MoEs are the stable ship-today bases, but confirm exact names on model cards.
- ALL specific model sizes/licenses/tok-s figures here are [UNVERIFIED] — the 2026-07-14 search returned
  TITLES only, which support just "DeepSeek V4 ~1T open MoE". Everything else is a LEAD; confirm against a
  primary source (model card / HF repo) before ANY public/investor claim. (This corrects an earlier
  "verified live" footer that overstated what the search actually established.)
