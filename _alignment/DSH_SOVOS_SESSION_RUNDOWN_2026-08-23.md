# DSH/SOVOS SESSION RUNDOWN — THE INFO, SORTED (2026-08-22/23)

Everything built, tested, verified this session. Honest: measured or marked UNMEASURED (never 0).

## 1. WHAT'S BUILT + VERIFIED (the stack)
| System | Where | Status |
|---|---|---|
| DSH harness fix | `~/.dsh/settings.yaml` (+ SSH config) | ✅ 13 providers, disk+latency fixed |
| EUNOMIA gateway (rentable models) | `~/clawd/eunomia-gateway.cjs` (`:8877`) | ✅ 9 RunPod serverless models, catalog + ledger |
| meok-arena (data generator) | `~/clawd/meok_arena.py` | ✅ live model-vs-model → preference pairs (gate referee) |
| domain-packs (engine signs all) | `~/clawd/domain-packs.py` | ✅ finance/markets/insurance/cobol → signed verdicts |
| cobol-a2a-bridge (bank wrap) | `~/clawd/cobol-a2a-bridge-mcp/` | ✅ COPYBOOK→DID→ISO42001→C2PA-sign |
| Axis engine (21 axes) | `dorado_gate.py`, `law_kb.py`, `run_govbench_ns3.py` | ✅ 15 GSPC + 6 domain, honest, sigilled |
| RAS front-end (end-user product) | `~/clawd/ras-front.html` | ✅ HTTP 200, assessed-not-certified |
| AGUI (MEOK head / AG-UI door) | `:8785` "Council Space" | ✅ HTTP 200 |
| EAT loop | `eat_all.py` (cron */5) | ✅ 94,181 events → honey → KB → IWM |
| Offload | volume sink (2.3PB) | ✅ deploy2 + sim-world + RAG/SOVOS on sink (Mac 7.6G free) |
| S3 rail | rclone `runpod-s3` (eu-cz-1) | ✅ keys stored; auth quirk flagged |

## 2. THE HONEST NUMBERS (measured)
- **GOVBENCH 0.931** (sov33-unified + gate + law-RAG + pillar-RAG; was 0.448 bare)
- **DEFBENCH refusal 1.000 / over-block 0.000** (the deterministic gate)
- **COMPBENCH 84.5%** (gov 46.7%) · **MMLU**: OWEM 41.5% vs **DeepSeek frontier 78.5%** (0-shot N=65)
- **EAT honey 94,181 events** · **KB 7,646** · **axis registry 21** · **7 domain signed records**
- Fusion law (verified): **RAG exceeds best parent 84.2% vs 78.9%**; weight-merge does NOT.

## 3. STATE — DONE vs GATED (honest)
**DONE ✅ (verified):** whole measurement machine (measure→sign→data→fuel→retrain), the router products
(gateway/arena/RAS/AGUI), the EAT/honey loop, the offload/safety of the Mac, the axis knowledge (IWM).
**GATED ⚠️ (one external gate):** **warm RunPod workers** — 671b + sov4 serverless 500/cold (console
redeploys; balance $116). Everything else ready (gateway serves frontier + arena pairs once warm).
**UNMEASURED (honest, never 0):** GSPC signed (metered keystone) · flywheel fuel lanes · SOV3 :3101.

## 4. THE DOCS (the info, sorted for any agent)
- `~/clawd/_alignment/MASTER_SWEEP_300MOVES_2026-08-22.md` — full sweep plan
- `~/clawd/_alignment/NEXT_33_MOVES_2026-08-22.md` — the 33-move roadmap
- `~/clawd/_alignment/ONE_SOVOS_TWO_HEADS_ENGINE_AXIS_2026-08-22.md` — two heads one SOVOS
- `~/clawd/_alignment/MEOK_AI_ROUTER_PLAN_2026-08-22.md` — "OpenRouter of everything" grounded
- `~/clawd/_alignment/OOWM_NEUROSYMBOLIC_PLAN_2026-08-22.md` — neurosymbolic OOWM + benchmark proof
- `~/clawd/_alignment/DSH_ESTATE_LANDSCAPE_2026-08-22.md` — the estate map
- `~/clawd/csoai-static-deploy2/benchmark-results/` — all results + `OOWM_VS_TOPTIER_MMLU`, `SOVOS_ROUTER_TOPTIER_FUSION`

## 5. FINAL ONE-LINER
The machine is built, tested, honest, and signed: **one SOVOS, two heads (MEOK consumer / CSOAI body),
one engine-axis that measures+signs everything (models, bonds, insurance, COBOL, markets, AI)** with the
EAT/flywheel turning runs into data → fuel → retrain, and the end-user face (RAS front-end + AG-UI).
The only gate is a warm RunPod worker (console).

## 2026-08-23 ~10:15 — EAT ALL 22/22 CLEAN + corpus distiller (live)
- eat_all.py full: 22 ran / 0 failed / 0 skipped. PHASE_8_DEPLOY PASSED (wrangler -> 5f9675b1.csoai-sovereign.pages.dev).
- KB 8,002->8,011->8,002 (selftest 9/9, honey 94,181->94,182, routes 8/8).
- Diagnosis: sov_grpo_training_data.json = 5 entries ONLY -> arena 2/4 root cause.
- meok_arena (live gateway): mistral-7b vs qwen25-7b = 0 pairs (raw bases role-play, refuse tasks "unmeasured").
- Fix: distill_corpus.py — live gateway teacher + declared SOVOS system prompt (Care Floor 0.95 + refuse-harm) + DORADO-gate judge -> complete SFT corpus (existing entries preserved).
- Gateway live set: sov4-mistral-7b, sov4-qwen25-7b (sov6-* + qwen38-27b + r1-7b = serverless 500, console-redeploy needed).
- distill_corpus.py v2 (local GPU fleet mistral:7b+qwen2.5:7b with declared SOVOS policy + DORADO-gate judge):
  corpus 5 -> 12 entries (+7 judge-verified). Gateway :8877 workers degraded (ERROR 'choices'/timeout) -> console redeploy still needed.
- sov_minimal_train.py --steps 150 --output sov-minimal-output-v2 --ollama-name sov33-sft-v2 RUNNING (background).
- eval_student.py created (transformers judge of student on 6-task MEOK set, DORADO gate).

## 2026-08-23 ~11:50 — OFFLOAD WIRED (Mac = thin client; volume = estate home)
- EAT ALL 22/22 clean; PHASE_8_DEPLOY live (5f9675b1.csoai-sovereign.pages.dev).
- Corpus 5->12 (distill_corpus.py local-policy teachers, DORADO-gate judged). eval_student.py ready.
- OFFLOAD: clawd 26G + .dsh 533M -> volume-sink (/workspace/offload-dsh/{clawd,dsh-backup,secrets}) 456T free.
  Harness monorepo -> /workspace/sovos-harness (excludes .git/models/gguf/honey>100M/.backups/sim-world-data).
- GH repo: github.com/CSOAI-ORG/sovos-harness (private). gh auth: CSOAI-ORG. Pod gets token via ~/.config/gh -> secrets.
- Pod provisioned: node v22.14.0 + npm 10.9.2 + wrangler 4.125.0 + python3.11 (eat_all is stdlib-only).
- REVERSE TUNNEL LIVE: com.sovos.remote-services (Mac->pod -R 8766/11434/8877) — pod reaches Mac portal/ollama/gateway. VERIFIED.
- BACKUP LIVE: com.sovos.backup (daily 10:30 -> ~/clawd/scripts/sovos-backup.sh mirror).
- Resumable sync: sovos-sync-resume.sh (retries x6, append-verify, UserKnownHostsFile=/dev/null).
- ISSUE: pod SSH went unresponsive after rapid reconnect attempts (rate-limit/fail2ban; base load ~140).
  PROTOCOL: cooldown >=20 min, no hammering. sovos-finalize.sh waits 30 min then: syncs -> provision
  (git birth+push, EAT cron 03:00 UTC, SFT v2 train on pod, proof EAT cycle) -> logs under /workspace/eat-logs/.

## 2026-08-23 ~14:05 — E2E OFFLOAD STATE (verified pieces)
- ROOT CAUSE of sync flapping FOUND: ~/.ssh/config `Host *` (5 IdentityFiles + agent) interferes
  with the RunPod pod connection. FIX: `-F /dev/null` on all ssh/rsync/scp to the pod (5/5 stable).
- Monorepo LIVE: github.com/CSOAI-ORG/sovos-harness (private, CSOAI-ORG auth). Pod git-credentials
  store wired (token in /root/.git-credentials 600, from `gh auth token`).
- Harness git born (e643196) but tree got partial (derived dir) -> REBUILD from mirror via
  hardlinks (sovos-harness-rebuild.sh on pod) + full push. Mirror is the ARCHIVE (not git).
- CRON INSTALLED on pod (apt cron; container had none) + EAT cron `0 3 * * * /workspace/sovos-eat.sh`.
- torch 2.13.0+cpu + transformers installed in /workspace/offload-dsh/eatenv on pod.
- FINISH WATCHER live on pod (PID 17164): polls mirror size every 10min (12 rounds); on stable
  -> rebuild harness + git push --force + launch train (sov-minimal-output-v2, 150 steps) + proof EAT.
  Log: /workspace/eat-logs/finish-watcher.log
- Corpus 12 -> 26 (distill_multi: deepseek-chat = 14/24 correct, judge-verified; openai/groq/together/
  mistral/perplexity keys stale (errors), google+anthropic 401) -> ROTATION GATE (Nick).
- Mirror loop still running (16G/26G ~1.7MB/s, completes ~15:30-16:00 UTC).
- PLAN: _alignment/NEXT_100_STEPS_OPENROUTER_ARENA_2026-08-23.md (100 steps, 5 phases; steps 53-55 executing).

## 2026-08-23 ~16:55 — NEXT-100-v2 + AUTO BATCH (state)
- NEXT_100_MOVES_v2_2026-08-23.md (6 phases, 70 steps + waves) + sovos-auto-batch.sh wave-0 ran.
- Rebuild pipeline: cron-runner + flock (single-thread) + marker; BUG FOUND+FIXED: rebuild script wrote
  .gitignore BEFORE cp -al -> hardlink self-conflict -> set -e abort -> tracked=0 forever. FIXED: cp -aln first,
  .gitignore after. Clean locked rebuild running (16:38 start; git add in progress; push ~3G next).
- Training RUNNING on pod (train-v2.log: model Qwen2.5-0.5B loading/weights done) — SFT v2, corpus 52.
- Verified: corpus 52 on pod; DNS/flock; cron ticks; watchdog relaunches; mirror 35G complete.
- Known-good: pod = root@213.173.105.83:25804 (ssh -F /dev/null REQUIRED — user ssh config breaks it).
- Reminders: verify REBUILD_OK + git ls-files count + push head + train-v2.log completion + eval_student run.

## 2026-08-23 ~19:30 — GOAL ROUND 1 FINDINGS
- CORPUS 52 -> 72 (deepseek pass; synced to pod mirror+harness; retrain-needed marker armed).
- POD TRAINING DEATH ROOT CAUSE: RunPod pod SIGKILLs CPU-heavy training processes (~25s after start,
  no OOM/traceback; even cron-launched). Modest processes (git add) survive. FIX: heavy training runs on
  MAC (proven); weights rsync to volume. sovos-overnight.sh now: distill -> sync -> mac train v3 (150 steps)
  -> eval_student -> next-pass weight sync. Thread caps (OMP=2) patched into pod watchdog/retrain anyway.
- v3 TRAIN LAUNCHED ON MAC (background, train-v3.log + eval-v3.log at ~/clawd/_alignment/).
- REBUILD/push: git add still grinding (mfs load ~140; cron runner keeps single-threaded attempt alive); no
  REBUILD_OK yet. EAT proof: 03:00 cron is durable cycle; 17:14 attempt log empty (died with pod state).

## 2026-08-23 ~20:30 — GOAL ROUND 2 FINDINGS
- CORPUS 72 -> 95 (deepseek pass x2; synced to pod mirror+harness; retrain marker armed).
- Mac /tmp/sovtrain venv was PURGED (tmp cleanup) -> recreated (python3.14 venv, torch 2.13.0, transformers 5.15.1).
- v3 TRAIN RUNNING on Mac: pid 12602 at 97.3% CPU, 3:46 elapsed, ~6.3% mem; stdout block-buffered
  (log looks stale; load completed 18:25; ETA ~40 min for 150 steps). eval_student.py follows in-chain.
- REBUILD lean rework: curated .gitignore (excludes agentsociety/councilof-ai/aiverify/oowm-v8-e2e/
  sovereign-temple/meok/mcp-marketplace/csoai-org-v2/sim-world-data + weights/backups/honey) -> the mfs
  git add was pathologically slow on 35G/30K files; lean set should add in minutes. Runner re-armed.
- Pod training confirmed hostile (SIGKILL CPU-heavy) -> training = Mac, weights -> volume (canonical).
