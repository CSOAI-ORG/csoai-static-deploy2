# Fleet Roster — 2026-08-12

**Canonical.** RunPod GPU estate + roles + jobs. Precondition for any future pod
mutation (register V7 / incident doctrine). Verify before scaling or killing a pod.

## Live GPUs (RunPod)

| GPU | Pod | IP:port | Cost/hr | $/mo | Role | Status |
|---|---|---|---|---|---|---|
| **A100 80GB** | `1dldzposn7ssuu` sov-brain-a100-fresh2 | 104.255.9.187:11703 | $1.19 | ~$860 | **Heavy-lift + 13-axis board v2** | Board: gov/agi/asi/prv done, xr/safety in flight; MinIO master :9000 (private buckets) |
| **RTX 3090 24GB** | `fpowppss5ngtkw` sov-repull-20260808 | 194.26.196.156:17446 | $0.22 | ~$160 | **24/7 arena worker** (cheap grinding) | Arena loop across 13 axes, R27+, 5 sov models |

**Not provisioned / retired:**
- `qdigrzjp5na1ek` (2nd A100) — never provisioned (stuck machineId:None), terminated
- `2oe71t1kzm145r` (A100 clone) — boot-failure, abandoned
- `69kojdgdxe1b3` (3090 sov-brain-2) — predecessor, retired

## Jobs running

| Job | Pod | Runs | Notes |
|---|---|---|---|
| **13-axis board v2** (`board_v2.py`) | A100 | 19 models × 13 banks | gov,agi,asi,prv MEASURED; wip-flush hardening committed |
| **24/7 arena loop** (`arena_24x7_loop.py`) | 3090 | 5 models × 13 axes, forever | real Glicko, league.json persists each round |
| **Nemotron auto-pull** (`stage_nemotron.sh`) | A100 | waits for board ALL13 | pulls nemotron-3-nano:30b post-board |
| **Cross-lab post-board** (`postboard_unblock.sh`) | A100 | fires after board | full quotable East-vs-West city (n≥30, $3 cap) |
| **Board monitor** (`board_monitor.sh`) | A100 | polls 5 min | logs axis summary at ALL13 |
| **Cross-lab governed city** (staging) | 3090 | done | 12 turns, self-gated n<30 |

## Models on pods
- **A100 (20)**: 13 sov6-v3-light + gemma3:12b, llama3.2:3b, qwen2.5:3b, qwen2.5:0.5b, mistral:7b, deepseek-r1:8b (+ qwen during board)
- **3090 (5)**: sov-safety-v1, sov-merge-slerp-gguf, sov-merge-dare-gguf, s.refusal-combo-lora, qwen2.5:0.5b

## Volume fit (for scaling — owner-gated attach)
- `sovos-merge-800` (800GB, EU-RO-1) → fits the **3090** (EU/Czechia) for arena data growth
- `sov-workspace-mtl4` (200GB, CA-MTL-4) / `sov-models` (300GB, CA-MTL-3) / `sov-artifacts` (200GB, CA-MTL-3) → North America, for A100-scale if needed
- Volume attach is **web-UI / owner** (CLI blocked). Precondition met the moment data needs it.

## Budget posture
- A100 $1.19/h (~$860/mo if always-on) — keep for active heavy-lift, not idle
- 3090 $0.22/h (~$160/mo) — cheap, intended always-on 24/7
- OpenRouter: rotating key, hard Budget cap per run (pre-check before each call)

## Doctrine
- Never kill a sibling's running job (board owns A100 GPU, arena owns 3090)
- MinIO master buckets private (C5 sealed); per-axis board rows durable on /runpod
- Verify GPU liveness via `runtime.uptimeInSeconds` or SSH, NOT `uptimeSeconds:0`
## 2026-08-12 late — arena persist durability fix (sync discrepancy)
- **Bug found:** pod's arena_24x7_loop.py was a STALE copy — fell back to `repr(lt)`
  when persisting league.json (wrote a Python repr string, not JSON).
- **Root cause:** repo had the fix (league_data dict → JSON, `sovos-league/v1`);
  pod was running a pre-fix copy. Sync drift, not a new bug.
- **Fix:** pushed the clean repo version to the pod, restarted the loop.
  Verified live: league.json = `{schema: sovos-league/v1, generated, defender,
  axes:13, factions:10}` — machine-readable.
- **Doctrine:** before trusting a pod's runtime behavior, diff the pod's file
  against the repo (git status / diff) — the pod can drift silently.
