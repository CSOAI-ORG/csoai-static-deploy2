# NIGHT PIPELINE LEDGER — 2026-08-24 ~03:05 UTC
_All numbers measured. UNMEASURED listed as such. Provenance in each row._

## P1 — VERIFY NIGHT PIPELINE (honest account)

| Item | Measured | Verdict |
|---|---|---|
| Corpus size | **257** (188→214→237→257 via live `distill_multi.py` passes) | ✅ GROWING (deepseek tier-1 + local policy); mistral/perplexity/openai/groq/together keys 401 (stale) — only deepseek contributes |
| train-v3 output | **NONE** — no `sov-minimal-output-v3/` dir | 🔴 FAILED through the night |
| train-v3 root cause | driver used ephemeral `/tmp/sovtrain/bin/python` → **purged** → every launch died instantly (`no such file or directory`) → relaunch loop each pass | 🔴 FOUND |
| train-v3 status (now) | persistent `~/clawd/.venv-sovtrain/bin/python` (py3.11.15, torch 2.8.0, tf 4.57.6 = proven) patched in + re-launched via `launchctl submit -l com.sovos.train` (OMP=4, -u) ~04:00 UTC | ⏳ RUNNING — UNMEASURED until it writes output-v3 |
| eval_student verdicts (v3/v4) | **NONE** | 🔴 chained after train, which never completed; will fire when v3 completes |
| EAT proof cycles (21:21 + 03:00) | sink pod `sz0duht9e5bbov` **EXITED by user 23 Aug 18:37 UTC** → its EAT crons (`0 3 * * *` + `21 21 * * *`) are NOT firing → proof logs on the volume UNVERIFIED | 🔴 EAT loop broken (sink down) — UNMEASURED |
| corpus-214 sync | driver rsyncs to sink `213.173.105.83:25804` → **"connection unexpectedly closed, code 255"** on every pass | 🔴 pod-side copy NOT synced (sink down); Mac corpus=257 |
| monorepo remote HEAD | **`e9910602999826d10389614ba8a98b894cd2ec74`** on `main` (CSOAI-ORG/sovos-harness) | ✅ advanced from d3b3460e |
| gateway v2 | `eunomia-gateway-v2.cjs` LIVE on :8878, `/v1/models` returns provider list (runpod + local fallback) | ✅ up |

**P1 one-liner:** the corpus grew to 257 and the monorepo advanced, but the *training* pipeline was hard-broken by the ephemeral `/tmp` venv being purged; a concurrent lane has patched the persistent venv in and re-launched v3 (running). The **EAT loop and corpus sync are dead because the sink pod is EXITED** — that is the single biggest P1 state change.

## P2 — CEO MONDAY OPS (done this round)

| Action | Result | Evidence |
|---|---|---|
| Refresh `~/.grokbot/harness/fleet.json` | ✅ Rewritten to live state | 2 RUNNING pods = **$1.61/hr**; sink EXITED; 5 network volumes; 23 serverless endpoints; `currentSpendPerHr` **$5.32**; `clientBalance` **$96.33**; `spendLimit` **$80** |
| Fix `~/.ssh/config` sovos-light-a100 port | ✅ `Port 23166 → 14954` | runpodctl `ssh_command` authoritative; `ssh -G` resolves 14954; `OPSCONNECT_OK` (load ~12/29/29) |
| Reconcile spend | 🔴 **$5.32/hr vs $1.61/hr** | delta ~$3.71/hr ≈ **warm RunPod serverless workers** (workersMin=1 → billed per-second + per-worker disk; one endpoint alone `$20.86`/7.6h, disk billed up to 6600GB) — NOT the 2 pods |

**P2 key finding — SINK POD DOWN:** `sz0duht9e5bbov` (sov-volume-sink-cpu) was **EXITED by user 23 Aug 18:37 UTC**. It was the offload mirror, EAT-cron host, and pod-retrain host. Its 5 network volumes persist (can be remounted), but the pod is gone → **offload sync, EAT proof, and pod retrain are all dead.** This is the root cause of the P1 sync/EAT failures.

## P3-D — MODEL LOOP (no duplicate launched)
- Verified root cause + confirmed the persistent venv fix landed by a concurrent lane. **Training v3 is running now** (launched ~04:00 via `launchctl submit -l com.sovos.train`, OMP=4, unbuffered). Do NOT launch a second concurrent Mac training (rule: never two).

## P4 — FREE OWEM ROUTER (Block 1)
- `sov_router_fast.py` (23-axis) **RUNNING** on 3090 (`194.26.196.156:23243`); `free_sov_router.json` **NOT yet written**. In-progress; do not duplicate.

## GATES (owner = Nick) — FLAG ONLY, never decide
1. **Sink pod `sz0duht9e5bbov` is EXITED** — restart to restore offload/EAT/retrain, or leave down (owner call). P1-P2 depend on it.
2. **Mine A100 `l7g747oivyq6ab` RUNNING** against fleet `do_not_start` (resumed 23 Aug 23:45) — keep or stop ($1.39/hr ≈ $33/day).
3. **RunPod serverless redeploy** — 23 endpoints, several workersMin=1 warm (billing ~$3.71/hr unaccounted); workers reported 500/cold per 23 Aug.
4. **API key rotation** — openai/groq/together/mistral/perplexity stale 401; google+anthropic 401.
5. **Balance $96.33 < spendLimit $80** — already over the limit threshold; runway decision.
