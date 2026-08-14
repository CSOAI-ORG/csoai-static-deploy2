# Board vs /api/gspc Gap Declaration — mined from rows, 2026-08-13

**Status: GAP DECLARED — PUBLISH REFRAINED (AZ.6/AZ.7 owner-gate).**
Every number below is **derived from the actual per-item board rows** (13 axes,
peritem_*.jsonl), not from the docs. Live `/api/gspc` verified same-day.

## The gap (quantified)
The board has MEASURED all 13 axes with usable_n ≥ 30 and Wilson CI on every
axis. The live public API still reports only 3 axes MEASURED
(governance/safety/conformance) and 10 as UNMEASURED/DRAFT/SPEC/PLANNED.

| axis | usable_n | mean acc | Wilson 95% CI | best model | best acc | live API status |
|---|---|---|---|---|---|---|
| governance | 4329 | 0.510 | [0.495,0.525] | sov6-embodiment | 0.700 | MEASURED ✓ |
| safety | — | — | — | — | — | MEASURED (14-item bank) ✓ |
| conformance | — | — | — | — | — | MEASURED ✓ |
| agi | 647 | 0.774 | [0.741,0.805] | gemma3:12b | 0.944 | **UNMEASURED** |
| asi | 598 | 0.472 | [0.432,0.512] | deepseek-r1:8b | 0.857 | **UNMEASURED** |
| art5 | 676 | 0.840 | [0.811,0.866] | sov6-relationality | 0.972 | **UNMEASURED** |
| care | 3138 | 0.354 | [0.338,0.371] | sov6-ethics | 0.549 | **DRAFT** |
| cross-reality (xr) | 593 | 0.452 | [0.412,0.492] | mistral:7b | 0.812 | **UNMEASURED** |
| detector-interop (det) | 517 | 0.683 | [0.641,0.721] | sov6-relationality | 1.000 | **SPEC** |
| machinery (mach) | 592 | 0.370 | [0.332,0.410] | sov6-agency | 0.583 | **DRAFT** |
| mcp | 576 | 0.620 | [0.579,0.659] | sov6-logic | 1.000 | **UNMEASURED** |
| openness (oss) | 578 | 0.732 | [0.694,0.766] | deepseek-r1:8b | 0.889 | **UNMEASURED** |
| provenance (prv) | 518 | 0.645 | [0.603,0.685] | sov6-logic | 1.000 | **UNMEASURED** |
| swarm | 618 | 0.458 | [0.419,0.497] | deepseek-r1:8b | 1.000 | **PLANNED** |
| **affect** | 729 | 0.646 | [0.611,0.680] | sov6-preservation | 0.878 | **DRAFT (counsel gate — KEEP)** |

## Doctrine compliance check (why publish is REFRAINED)
- **affect → DRAFT and STAYS DRAFT** — counsel blessing of labels/severity-basis not
  yet signed (AZ.6/7, BN.5). Its interval exists but is NOT publishable.
- **The 10 non-affect measured axes** have verified usable_n + CIs, but flipping
  them to public MEASURED-with-numbers is a **publish-delta** (AZ.7 "spray" gate:
  board + city + JUDGE.lock hash). The city board now exists (4.44% CI), judge
  ratified (a3ae43c7). **Owner word unlocks the flip.**
- UNMEASURED = honest; these rows are now MEASURED-in-ledger. The public surface
  under-reports (Part CB gap) — declared here, not silently.

## The staged decide-action (fires on owner word)
1. Update `functions/api/gspc.ts`: promote the 10 board-measured axes to
   MEASURED-with interval — EXCEPT affect (stays DRAFT).
2. Deploy councilof-ai production (branch main, direct writr).
3. Delta Note #2: v0 → v1 board-measured statuses, dated, per-item rows linked.
4. Emotional Safety Card path + insurer CVaR tail block become quotable.

## Honest flags
- care mean 0.354 is LOW (over-refusal vector) — a real finding, not a bug.
- asi 0.472, xr 0.452, swarm 0.458, mach 0.370 — several axes are genuinely hard
  or the fleet over-refuses; these are findings, and publishing them is honest.
- Mean acc is the mid-distribution; tail statistics (CVaR) still n-HUNGRY
  (n≥100) — BV doctrine: report mean only, never "tail risk", until tail computed.
  Several axes (det/mcp/prv/swarm) show best_acc=1.0 — flag as possibly-overfit/
  small-bank; do not over-claim a 1.0 MODEL (it's bank-best, may be noise).