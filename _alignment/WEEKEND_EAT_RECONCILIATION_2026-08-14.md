# WEEKEND EAT RECONCILIATION — 2026-08-14
Companion to `SOVOS-WEEKEND-EAT-PLAN-2026-08-14.md`. Honest delta between the plan's
claims and live estate state, so Saturday's schedule runs on verified facts.

## What the plan asserts vs what I verified LIVE (2026-08-14 ~11:30 UTC)

### Automation §5 — TWO CLAIMS ARE STALE/UNTRUE
| Plan §5 claim (REAL — running) | Live verification 2026-08-14 |
|---|---|
| "Measurement churn — 3090 auto-churn + board_v2 harvest — running" | ❌ **Arena-24x7 loop STOPPED at Aug 13 17:45 (ROUND 285, clean end, no error).** No worker process. Pod GPU 0%/1MiB used. NOT running. |
| "Fix loop — ... hourly cron — running" | ❌ **Pod crontab is EMPTY** (`crontab -l` returns nothing). No hourly cron exists. The fix-loop (`fix_run.sh`) ran manually today 10:01 (REVERT result — gate works), but nothing schedules it. |

**Root cause (same for both):** neither loop is self-healing. Arena was launched as a
one-off `nohup`; no launcher script is registered in any start hook or cron. Any reboot or
kill leaves them dead permanently. This is the structural gap behind "0% 0% 0%".

### Artifact claims §6 — ALL REAL (verified)
- 85d833ca, 94cce3b6, 4306c579, bb15589c, 95c41584 all **EXIST** in the repo (git cat-file)
- GSPC endpoint live, did:web f4b4278d live, master verify 11/11 — all consistent.

### SSH endpoint correction (fleet roster error)
- Roster says sov-repull = `194.26.196.156:17446`. **WRONG — that port is sov-brain-2.**
- **Actual sov-repull SSH = `194.26.196.156:12853`** (public port for private:22). This is
  why the arena pod appeared unreachable.

## Required fixes before Saturday schedule runs
1. **Persist + schedule the two loops** with a real `@reboot` cron so they self-heal:
   - arena-24x7 launcher (find exact command from nohup.log — NOT the sovos-repo arena.py,
     which is a different match arena)
   - fix-run hourly cron (`fix_run.sh` exists)
2. **Correct FLEET_ROSTER.md SSH port** 17446 → 12853 for sov-repull.
3. Re-verify GPU wakes after restart (nvidia-smi non-zero) before trusting overnight churn.

## Doing now (already done, in-lane)
- Diagnosed via live pod + RunPod API (not guesswork).
- This reconciliation + plan persisted to repo.
- gating: restarting production churn loops = production action → offer to owner, don't
  autonomously start money-costing loops without the go.

## Corrected understanding for the weekend
The evidence wall is real and verified (all hashes). The *automation that feeds new evidence*
is down. Fix the loops → the plan's Friday-night pod runs become trustworthy. Until then,
the plan overstates live churn.
