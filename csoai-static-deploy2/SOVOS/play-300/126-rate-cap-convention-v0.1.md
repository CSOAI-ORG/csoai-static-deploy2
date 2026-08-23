# 126 — RATE-CAP CONVENTION v0.1 (👑 CROWN JEWEL · OPEN · H8/D02 §1B)

Date: 2026-08-21 · lane: K3 · velocity-only (spend caps owned by EP-BOUNDED-CAP-04 — REAL, H8).
Kill criteria: credible rate-cap standard ships elsewhere → adopt + extend.

**Thesis:** 2026 competition rules use latency/token budgets, NOT action-rate. "Effective actions"
per unit time is the unclaimed axis; engine-side enforcement makes caps verifiable.

## 1. Multi-window caps (count EFFECTIVE actions only)
| Window | Cap (draft) | Notes |
|---|---|---|
| Sustained | TBD (calibration) | long-run average |
| Burst | /5s | spike ceiling |
| Perception floor | 350 ms | min inter-action, human-comparable |

## 2. Latency-budget vs velocity-cap (distinction binds)
- Latency budget = wall-clock response deadline (AIIDE 42 ms; Planet Wars 50 ms) — NOT a rate.
- Velocity cap = actions per window, the axis we standardize. Do not conflate (D02 §1B).

## 3. AlphaStar annex (sourced, D02 §1B)
- 22 actions / 5s ladder cap.
- ≤600 / 5s · ≤400 / 15s · ≤300 / 60s · + 350 ms floor.
- 900–1500 burst backlash documented.

## 4. Enforcement & provenance
- Engine-side enforcement (not post-hoc audit).
- Per-window utilization logged INTO the signed replay envelope (Mvt 4, step 121) → verifiable caps.
- Stay out of spend budgets: cite EP-BOUNDED-CAP-04, link, remain velocity-only (D01 §4c).

## 5. Open items
Public consultation: organizers, engine maintainers, pro calibration (step 137). Feeds Mvt 8
preregistration of arena-fairness methodology (step 252). UNSIGNED until POD key in harness.
