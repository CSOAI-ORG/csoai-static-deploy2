# Held-out / anti-Goodhart verification — 14 Aug 2026

**Verdict: audit flag #5 (flywheel memorization leak) is ALREADY ENGINEERED OUT.**
The anti-Goodhart held-out discipline is implemented and VERIFIED LIVE on the A100 pod
(19/19 selftest PASS, exit 0). This is a correction of the audit's concern — the leak
the audit flagged does not exist; the guard is real and enforced at the fuel choke-point.

## The mechanism (verified, not assumed)

`flywheel.py` (pod: /workspace/csoai-static-deploy2/flywheel.py):

- `HELD_OUT_FRACTION = 3` → every probe whose id-hash % 3 == 0 is held out (~1/3). Line 103.
- `split_of()` is salt-stable — same item maps to same split every run. Selftest: "split is stable" PASS.
- `export_fuel()` is the ONLY path that writes training/KB material, and it RAISES
  `FlywheelLeak` the instant a held-out cell touches it (checks item identity, not label).
- `OverfitGateTrip` — the promote/accept gate trips when practice-vs-held_out accuracy gap
  persists (>3 days). Fuel export raises OverfitGateTrip while the gate is open.
- The day artefact records `held_out_excluded` count; held-out aggregates never reach honey.

## Live selftest result (19/19 PASS, exit 0)
```
PASS  split covers all items
PASS  held-out is non-trivial
PASS  split is stable
PASS  leak guard fires
PASS  guard checks item identity, not the label
PASS  refuse-everything is not a winner
PASS  comply-everything is not a winner
PASS  UNMEASURED excluded from accuracy
PASS  tokens_per_correct = total/correct
PASS  majority: 2/3 refuse -> refused
PASS  majority: tie fails closed -> refused
PASS  majority: all None -> unmeasured
PASS  refuse-everything: TPR 1.0
PASS  refuse-everything: FPR 1.0 (not a winner)
PASS  working gate: TPR 1.0 AND FPR 0.0
PASS  overfit gate trips after 3 days
PASS  overfit gate reports tripped days
PASS  overfit gate clears when gap closes
PASS  export_fuel raises OverfitGateTrip when open
```

## What this means for public claims

- **"The loop works"** — quotable (both directions verified: REVERT on overfit, PROMOTE on gentle).
- **"Train-on-A / gate-on-B held-out"** — true; the split, the leak-raise, and the overfit gate
  are all live and tested.
- **"+1.1 pts better"** — still directional (one item), NOT a magnitude claim. Sealed by gate.

## Cross-reference
- `flywheel.py` — implementation + selftest region (lines ~360-470)
- `sov_pipeline.py` lines 358-397 — fuel exports PRACTICE-only, held_out stripped + counted
- `tests/test_flywheel_honey_leak.py` — the honey-barrier assertion (held_out never hits honey)
- Engine Fix #1 tonight: `board_v2.py` det-axis num_predict 512→2048 (reasoning-model budget),
  verified live — the fix loop correcting its own wrong hypothesis, recorded as a negative result.
