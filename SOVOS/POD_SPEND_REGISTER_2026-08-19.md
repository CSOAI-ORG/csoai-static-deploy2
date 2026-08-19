# POD-SPEND REGISTER (2026-08-19) — tracked live, drift-flagged
**Lane:** JEEVES (K3) · **Source:** runpodctl pod list, live

| Pod | GPU | $/h | $/day (if running) | machineId | Actually billing? |
|---|---|---|---|---|---|
| sov-repull-20260808 (3090) | RTX 3090 | $0.22 | $5.28 | ✅ live | ✅ YES — the worker |
| sov-brain-a100-fresh-20260811 | A100 | $1.19 | $28.56 | ❌ None | no (unscheduled) |
| sovos-light-master-mine-20260816 | A100 | $1.39 | $33.36 | ❌ None | no |
| council-ring-a100-20260818 | A100 | $1.39 | $33.36 | ❌ None | no |
| sov-volume-sink-cpu | CPU | $0.06 | $1.44 | ❌ None | no |
| **TOTAL** | | **$2.86/h** | **$69/day** | | **~$5.28/day actual** |

## The truth (checking, not assuming)
- **Nominal $69/day** if all 4 A100s came online — but all show machineId:None (volume-pinned, RunPod can't schedule them). **Actual burn ≈ $5.28/day** (3090 only).
- **The risk:** if RunPod infra recovers and schedules the A100s, burn jumps to $69/day instantly. The A100s are `desiredStatus: RUNNING` — they WILL bill when a machine frees.
- **Owner action (Nick, from K3 plan #57):** copy-then-pause the A100s (`desiredStatus: STOPPED`) to kill the $63/day landmine. Highest-value fleet action.

## Drift flag
- 3090 load avg 34 (sibling overnight_axes.py saturating) — the only live worker is overloaded.
- DeepSeek V4 pricing 4.55× peak (16 Aug) — off-peak scheduling monitor active.

## SIGIL
`pod-spend-register-2026-08-19-jeeves`
