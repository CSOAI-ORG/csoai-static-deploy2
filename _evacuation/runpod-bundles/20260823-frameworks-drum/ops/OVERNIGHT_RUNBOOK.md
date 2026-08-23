# OVERNIGHT RUNBOOK — FRAMEWORKS DRUM (full night cycle)
## 2026-08-21 · owner: JEEVES lane · runs via `com.meok.frameworks-drum-overnight` (02:30 daily)

> The overnight cycle EATs the loop while the humans sleep: rebuild → verify → archive →
> mine → status. Every step is logged to `/tmp/frameworks-drum-overnight.log`; a non-zero
> exit leaves a FAILURES marker for the morning scan. Nothing in this runbook touches
> other lanes' files; it is read-mostly + writes only inside the drum pack.

## The cycle (exactly what `ops/overnight-drum.sh` does)

| # | Step | What | Fail-closed? |
|---|------|------|--------------|
| 1 | **Rebuild** | `build_catalog.py --check --lint` — fold any new `_mining/` files, regenerate catalog/cards/feeds | yes — exit non-zero on any check/lint hit |
| 2 | **E2E** | `tests/e2e_drum.py` — the full pipeline (build→cards→feeds→MCP 8-tool conversation→router on real calibration→archive→drift→ops check) | yes |
| 3 | **Archive** | the build hook already appends a Knowledge entry per fold; runbook also archives the overnight status summary | yes |
| 4 | **Mine the tray** | scan `_mining/` for files newer than `catalog.json` (folded already by step 1); report any un-folded tray file | no (report only) |
| 5 | **Measured labels** | if `signed_rounds.jsonl` grew, re-run `collect_measured.py` (append-only, id-deduped) | no |
| 6 | **Status** | write `feeds/status_overnight.json` — counts, gate results, archive size, measured labels, canary intact | no |
| 7 | **Drift** | `router/drift_monitor.py` — alarm if live scores drift beyond threshold (recalibration trigger, signed+logged) | no (alarm only) |

## Where the morning scan looks

- Overnight log: `/tmp/frameworks-drum-overnight.log`
- Status card: `feeds/status_overnight.json`
- EAT 7-box: `feeds/eat_7box.json` (measured ✅ / mirrored ✅ — the rest are the build queue)
- Standing 15-min check: `/tmp/frameworks-drum-check.log`

## What is NOT in the overnight runbook (by design)

- No deploys, no git pushes, no external sends, no other-lane edits ([GATE]/[LANE] stay out).
- No signing (EAT box 3) until the #dsh rail publishes — the overnight run records the
  unsigned state honestly, it never fakes a signature.
- No "evolve" loop execution — the promote-gate (Stage 2) must exist before the loop
  promotes anything; until then the runbook verifies and accumulates, it does not mutate.

## Morning handoff

1. Read the log tail + status card.
2. Fold any tray additions the runbook flagged (usually none — step 1 already folds).
3. If drift alarm: schedule recalibration (controlled, signed event — never continuous).
4. If measured labels grew: re-run the realized-coverage check next time the score exists.
5. Commit the overnight deltas (cards/feeds/archive entries) by name on the main branch.
