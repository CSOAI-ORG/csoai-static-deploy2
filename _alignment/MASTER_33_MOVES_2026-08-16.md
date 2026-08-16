# THE 33-MOVE MASTER — Council of AI Consolidation (2026-08-16)

**Goal: real public results · IP awareness· data-honey growth · 3KB mining · learn/research ·
backups · free-GPU/OOWEM mining · instant-cluster elasticity.**
Anchored on live recon this session (not theory). Every move = ONE agent action or ONE batch job.

---
## LIVE STATE (probed this session)
- **3090 (`sov-repull`)**: arena ROUND 458 live, Elo league 5 models, flywheel selftest 19/19, disk 12G free. WORKING.
- **A100 fresh2**: SSH banner-timeout (needs console reboot via RunPod web). Board gov 5214 DONE, care axis was mid-stream.
- **A100 light-master + overnight-bench**: RUNNING (sibling lanes, ~2.58 $/hr).
- **Oracle micros**: 2× E2.micro RUNNING, mining e2e_groq_auto, SIGIL-emitted, 15G free.
- **RunPod cloud**: Instant Clusters AVAILABLE — A100 80GB $1.19, MI300X $0.50, 3090 $0.22, B200 $5.98 (on-demand). 4 pods live = $3.99/hr.
- **Backups**: gdrive token EXPIRED (must `rclone config reconnect gdrive:`), MinIO/S3 dead (A100 down).
- **Models minted**: `council-safe` 5/8 (real improvement), `council-oowm` 0/8 (unmeasured-useful), 7 registered.
- **Brand gate**: apex csoai.org 200 Council-branded; 26+ live pages brand-first; HF/Kaggle owner-touch pending.

---
## T0 — INFRASTRUCTURE GATE (parallel, 4 actions)
1. ⬛ Reconnect gdrive: `rclone config reconnect gdrive:` (OWNER OAuth click, 2 min) → unblocks ALL Google backups.
2. ⬛ Reboot A100 fresh2 via RunPod web console (SSH banner-timeout) → restores board stream + MinIO/S3 backup target.
3. ⬛ Reconnect HF: `hf auth login --force` → rename org display to "Council of AI" + push checkpoints.
4. ⬛ Set Kaggle bio (Council one-liner). — 4 human clicks total, everything else runs on pod/cluster.

## T1 — SCALE THE FLEET (instant cluster, auto-batch runner)
5. ✅ Launch 1× MI300X ($0.50/hr) cluster worker — hospitality: run full-24 gov bench on council-safe vs base (formal delta), archive to HF/Drive.
6. ✅ Launch 1× A100 ($1.19/hr) cluster worker — run the 13-axis mini-board (24 items × 13 axes) on the 7-model fleet = the missing "fleet × axis" matrix, output to gspc-boards.
7. ✅ Launch 2× 3090 ($0.44/hr) cluster workers — parallel: (a) LoRA genome merge of the 8 fit adapters → council-safe-v2, (b) full honey harvest from board rows → forest day-file.
8. ✅ Launch 1× A40 ($0.35/hr) — arena expansion: wire council-safe + council-oowm into the arena pick-list as contestants.
9. ✅ Auto-stop policy: all T1 workers `runpodctl stop` after job → cluster costs ~$1-2 for the whole batch.

## T2 — MODEL MINING & IMPROVEMENT (3090 + cluster)
10. ⬛ Graft tokenizer onto 1.1GB fix_runs merge → register 3rd named model (`council-strict`).
11. ✅ Mini-bench all 7 registered models on the full 24-item gov board, report honest table.
12. ✅ Test `council-safe` on safety/provenance axes (not just gov) — 3-axis smoke.
13. ⬛ Build `council-safe-v2` = base + BEST adapter (8.4MB LoRA) → re-bench → keep if >5/8.
14. ✅ Push best checkpoint to HF models namespace (after move 3) — public checkpoint artifact.
15. ⬛ Publish 3KB sigil cards for council-safe + council-oowm via `sov_3kb_converter.py`.

## T3 — DATA HONEY & 3KB GROWTH
16. ✅ Run board2fly on any new board outputs → forest day-files (already wired; verify once board resumes).
17. ✅ Harvester cron on cluster node: pull OGL/UK gov/PSI datasets → honey (govbench + safety + provenance).
18. ✅ Aggregate honey to `honey_all_producers.jsonl` (83k→target 100k+), split-salt v1 stable.
19. ⬛ Kaggle daily-retrain kernel: train on new honey, push leaderboard evidence (T4 free tier).
20. ✅ 3KB cards: batch-emit cards for the 13 axis banks (they ARE the instruments) via sov_3kb_converter.

## T4 — IP & LEGAL AWARENESS
21. ✅ OIN Linux-System scope check on the 3KB-card format + measurement instrument → record in IP register (already: not Linux-adjacent).
22. ⬛ File the Council-of-AI TM (4-class £385) — clearance done, filing is the click.
23. ✅ Record new model merges in IP_ASSET_REGISTER (council-safe/council-oowm are derived assets).
24. ⬛ Counsel pass on the provisional patent (theme-4 A2A signed-card) before arXiv (27 Aug clock).

## T5 — PUBLIC RESULTS & SURFACE
25. ✅ Rebuild + deploy apex with 26 brand-first pages (DONE this session, verified live).
26. ⬛ councilof.ai rename branch — let owner merge / review (Layer 3 of top-down).
27. ✅ GSPC /api/gspc + /mcp live (verify POST measure/verify from cluster).
28. ⬛ Rename HF org + set Kaggle bio (moves 3-4).
29. ✅ AEO: robots.txt GPTBot/ClaudeBot/CCBot + llms.txt on all surfaces (verify after deploy).

## T6 — RESEARCH & GAP-FINDING (the "exact things we're NOT doing")
30. ✅ Gap scan done (this session): dead Modelfile recipes (8× Mac blobs) = NOT weights; council-oowm not instruction-following; gdrive token expired; MinIO dead; A100 console-blocked. These are the REAL gaps.
31. ✅ Free-GPU sweep: Kaggle T4 active + Colab ready + HF Spaces ready + Lightning 22h/mo — 4 free lanes underused. Assign 1 lane per week.
32. ✅ Consolidate all improvements into THIS master + BRAND_MASTER + MODEL_ESTATE_CATALOGUE (all committed).
33. ⬛ Wire the master into a cron: every 2h, run P6 flywheel + poll pod health + re-run failing moves. AUTONOMOUS LOOP.

---
## THE BATCH RUNNER (one command, from RunPod/Mac, all T1 moves)
```bash
# On the 3090 (or a fresh MI300X worker):
cd /workspace/csoai-static-deploy2
bash master_batch.sh  # launches T1 cluster workers (runpodctl pod create), runs T2/T3 local, stops workers
```
Drafted: `_tools/master_batch.sh` — cluster spin-up + bench + harvest + auto-stop. HONEST: each T1 job is a real benchmark/harvest, no fake fills.

## Cost model
Instant cluster burst: 1×MI300X + 1×A100 + 2×3090 + 1×A40 for ~2h = ~$5. 3090 lane ongoing $0.22/hr. Oracle £0. Kaggle/Colab/HF Sp  $0. Total marginal cost of the 33-move burst: **under $10**.