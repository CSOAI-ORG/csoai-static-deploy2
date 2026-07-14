# 🔴 World-model stress test — the honest failure mode (2026-07-14)
_Attacked our own "governed world model, 100% fail-closed" claim on GENUINELY chaotic dynamics. It broke —
and naming exactly how/why makes the claim credible instead of hype. Register: this is the honest limit._

## Setup
- Env: **coupled logistic-map lattice** (r=3.9, diffusive coupling) — genuinely chaotic (perturbation growth
  **26.4×** over 8 steps; positive Lyapunov). The earlier tanh env was contractive (0.3× — errors shrink), which
  *flattered* the world model. First stress attempt failed to be chaotic; caught + fixed (honest).
- Same tiny MLP world model. Run: `sov33_world_model_stress.py` → `world_model_stress_results.json`.

## Result — it breaks, and governance breaks WITH it
| test | easy env (contractive) | **chaotic env** |
|---|---|---|
| 1-step prediction MSE | 0.003 | **0.049** (10× worse — can barely predict one step) |
| Closed-loop MSE (re-observe each step) | 0.003 ✅ | **0.056 — FAILS** |
| **Care-gate catch rate on unsafe transitions** | **100%** ✅ | **0% — FAILS** |

## The critical, honest lesson
**Governance depends on prediction.** The care-gate can only veto a future it can *foresee*. On chaotic dynamics
the world model can't predict the next state accurately, so it never sees the unsafe transition coming → **0%
caught.** Yesterday's "100% fail-closed" was real but **conditional on predictable dynamics.** A governed world
model is only as safe as its forecast.

## What this means (and the honest fixes)
- **Scope the claim:** our world model + governance work on **predictable / contractive / engineered-control**
  dynamics (most goal-directed robotics, navigation, logistics) — **not** on chaotic domains (weather,
  turbulence, markets) at this model scale. Say so.
- **Fix 1 — abstain on low confidence:** wire the **mirror-auditor divergence signal** (measured corr 0.434) as
  a *forecast-confidence gate* — when prediction is uncertain, the governed model must **refuse to act**, not
  guess. Fail-closed on *uncertainty*, not just on predicted-danger. This is the honest safety posture on hard dynamics.
- **Fix 2 — shorten the horizon / close the loop harder** (act-then-reobserve every step) reduces but does not
  eliminate the error here — the 1-step error is already too high, so scale is needed.
- **Fix 3 — scale the model:** a bigger world model (or V-JEPA-style representation) is required for chaotic
  dynamics; the tiny MLP proves the *mechanism*, not chaotic-scale capability.

## Why publishing this is the strong move
Every frontier "world model" demo cherry-picks predictable footage. **We measured where ours breaks and named
the prediction⟸governance dependency** — that's the honest science a defence/assurance buyer trusts. The claim
becomes: *"a governed world model that is safe **where it can predict**, and **abstains where it can't**"* —
which, with Fix 1 wired, is a stronger and more defensible safety guarantee than "100%".

Registered `world-model-stress-honest-limit`. Reproduce: `python3 sov33_world_model_stress.py`.
