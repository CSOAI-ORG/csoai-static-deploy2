# SOV333 GPU Build Spec — from the measured CPU blueprint to real qwen experts (2026-07-14)
_The CPU model (sov33_full_model.py) proved the architecture + design laws E2E. This spec maps each measured
piece to its GPU/LLM form so the owner's Kaggle/Colab notebook builds the SAME structure with real weights.
Every parameter below is set by a MEASURED result this session, not a guess._

## THE BLUEPRINT (measured on CPU, ready to scale)
| Piece | CPU proof | GPU/LLM form (what the owner builds) |
|---|---|---|
| Brain | OWEMPredictorV2 (numpy MLP) | a qwen expert (QLoRA fine-tune on free T4) |
| Layer = 4 brains | pyramid-4brain +48% vs 1-brain | 4 QLoRA experts (Compliance/Defense/Intuition/Voice), vote=mean logits |
| Depth = 8 | fluid-pyramid: 8 optimal, 9-12 overfit | 8 residual layers; STOP at 8 (measured overfit past it) |
| Residual cascade | each layer learns residual below | Branch-Train-MiX: expert n trains on task, n+1 on n's errors |
| Seam = Venturi=SIGIL | 481us/hop, tamper-caught | hash-chain the router decision per hop (real: add TOPLOC activation-LSH) |
| Auditor = quantum mirror | divergence corr 0.33 w/ error | 2nd decorrelated stack; high divergence -> escalate to bigger model |
| Governance = care-veto | care<0.35 collapses emit | care-divergence scorer gates the emit (already built, cloud+local) |
| Mixing ratio | flat-1.0 BEAT 90/10 in test | equal expert weighting to start; sweep only if a layer dominates |

## HONEST CONDITIONS (when to add structure — the measured law)
- Add DEPTH only while residual remains -> stop at 8 (past that = overfit).
- 4-brain layers ALWAYS help (decorrelated vote) -> keep 4 per layer.
- STACK a 2nd expert only if the 1st is capacity-limited (leaves residual).
- NEST (pyramid-of-pyramids / 4-around-1) ONLY with genuine regional/domain structure AND accurate routing
  (measured: wins +60% at moderate region separation, LOSES when regions trivially separable or routing
  starves sub-pyramids). For a single-domain task, ONE deep pyramid beats 4-around-1.

## THE £0 BUILD ORDER (owner's notebook)
1. QLoRA fine-tune 4 experts (Compliance/Defense/Intuition/Voice) on the estate's 4 expert_data sets, free T4.
2. Stack 8 residual layers (Branch-Train-MiX merge; router = mean-vote to start).
3. Wrap each layer hand-off in the Venturi throat (sov33_venturi_throat.py already runs — add TOPLOC LSH
   over the real activations to replace the SHA256 placeholder).
4. Add the mirror auditor (a 2nd decorrelated stack); route high-divergence queries up to a bigger model.
5. Gate the emit with the care-divergence scorer (already built).
6. Grade on a real Kaggle benchmark -> sov33_live_gsm8k.json -> auto-wires the capability number into canonical.

## HONEST BOUNDS
- The CPU model proves TOPOLOGY + DESIGN LAWS, not LLM-scale performance. The GPU run is what produces a
  real graded number. Until it lands, capability_benchmark stays PENDING.
- TOPLOC / Branch-Train-MiX are literature LEADS (unverified from this sandbox — no browser); the owner/CC
  confirms the exact libraries before building to them.
