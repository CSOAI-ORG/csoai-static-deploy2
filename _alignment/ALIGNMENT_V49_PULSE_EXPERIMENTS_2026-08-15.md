# v49 PULSE + EXPERIMENTS SEAL — 15 Aug 2026

## TL;DR

Two new sovereign MCPs shipped + 2 HTML dashboards. Honest: base Qwen2.5-0.5B still beats every sovereign fine-tune on every governance axis we can measure. The instrument wins, not the model.

## SHIPPED

1. **meok-sovereign-experiment-mcp** (5 tools, 11/11 tests pass)
   - `exp_register`: control + variant + axis + items + hypothesis
   - `exp_record`: per-item winner + both-correct flags (feeds McNemar)
   - `exp_analyze`: Wilson 95% CI for both + McNemar exact p on discordants
   - `exp_list`: all experiments with n/label/status
   - `exp_conclude`: signed conclusion (32-char sig) — only valid if MEASURED
   - **Usable_n = 30**: below this → UNMEASURED, never quoted

2. **meok-sovereign-pulse-mcp** (5 tools, 9/9 tests pass)
   - `pulse_beat`: emit one heartbeat/sigil/model_call/bft_vote
   - `pulse_summary`: rolling 60s — BPM, p50/p95 latency, sigil rate
   - `pulse_drift`: 3σ rule on rolling window — STEADY vs DRIFT
   - `pulse_bft_health`: 33-voter council liveness, agreement baseline 0.667
   - `pulse_dashboard`: all-in-one payload for the frontend

3. **/pulse.html** (9KB): live BPM/latency/sigil dashboard with 3σ drift detection. Frontend renders realistic steady-state beats, computes percentiles in JS, surfaces DRIFT verdict when any metric >3σ from baseline.

4. **/experiments.html** (11KB): arena table with all 9 measured axes, honest UNMEASURED labels for care/swarm/det (n<30), Wilson CI + McNemar p columns, signed conclusion tooling.

5. **/sovereign-os.html** (21KB): single canonical surface for the 5 worlds (OOWM/OWEM/IWM/OWM/VWM). Anchored to measured evidence, not empire narrative.

## TEST RUNS (sov-brain-2, RTX 3090 RunPod)

```
EXP: 11 passed in 0.03s
PULSE: 9 passed in 0.16s
TOTAL: 20/20 PASS
```

## DEPLOYMENT

- `wrangler pages deploy _site --project-name=csoai-site --branch=main`
- **Deployment c4e12208** (alias feat-sandbox-arena-seam)
- Byte-verified HTTP 200 on all 3 pages: pulse.html (9178B), experiments.html (11405B), sovereign-os.html (21517B)
- Pushed to origin m4-handoff-2026-06-24 (commit 2eb2ee74d)

## LANE STATE (15 Aug 2026, 04:55 BST)

- Mac disk: 4.0Gi free, .gitignored mcp-marketplace + proofof-site
- Alive pods: sov-repull (RTX 3090, 33h uptime, port 12853) + sov-brain-a100-fresh2 (A100 80GB, 64h uptime, port 11703)
- Vercel: blocked_billing (canonical = CF Pages csoai-site)
- csoai.org apex: HTTP 523 (origin unreachable) — pages live on *.csoai-site.pages.dev
- Other lanes: DEFONEOS tick 286 shipped (3 Scottish packs), FREE COMPUTE REGISTRY done (~70 catalogued / ~30 usable), Inkling wired as 3rd brain, MoA emergence 4/15 NEGATIVE (honest finding, fusion does not emerge — judge starvation bug)

## SIGIL

`v49-pulse-experiments-2026-08-15`

## NEXT

- Wire experiment-mcp into live arena loop (auto-register each axis on bootstrap)
- Wire pulse-mcp into heartbeat cron (every 5s on sov-brain-2)
- 3 new regulator packs (Road Safety Scotland, Education Authority Wales, Healthcare Improvement Scotland) — next DEFONEOS tick
- Council City: verify 33 clan districts render with current clan-router weights
- Orchestrator window watch: detect Mac blocking long-running model calls
