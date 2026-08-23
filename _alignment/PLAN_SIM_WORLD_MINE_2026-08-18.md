# SIM WORLD × THE MINE — MASTER PLAN (2026-08-18)

Commanded by JEEVES. One display, one mine, one fuel loop: the harness GUI shows
the live world; the mine converts the empire's data into signed 3KB h3k cards;
the cards train the models that measure the world that feeds the mine.

---

## PHASE 0 — Sim World live in the harness GUI ✅ DONE
- Cordis plugin `@deepseek-ai/dsh-client-ui-sim-world` in the harness tree,
  hot-applied via the web profile patch (no restart; YAML bug found + fixed).
- Zero-token Cesium globe (12 hive-cities), live agents (AI gold ◆ / human blue ●),
  duel arcs, 16-axis GSPC profiles; 🌍 sidebar toggle + full-screen overlay.
- Chat is the command surface: 7 tools (`sim_scene/spawn/step/control/benchmark/
  emit_card/runpod`), SSE data plane on :4190, sov-space Rust core syncing
  (34 agents = 24 seeded + 10 sov nodes), world evolved ~18,000 rounds.
- Data plane smoke-tested end-to-end; cards signature-verified.

## PHASE 1 — The Mine (honey → signed cards) ✅ DONE, SELF-SUSTAINING
- `honey-miner.mjs` v3: auto-discovers Q&A sources across 8 data roots, tracks
  offsets (clamped to live file length), dedups by body hash, signs every card
  (ed25519, sov33 key), writes raw + gz. Runs every 5 min via LaunchAgent
  `com.meok.sim-world-miner` (continuous — no 04:00 gate).
- Swept so far: 161,926-row honey forest (training_pair/fuel/flywheel-fuel/
  chatml), dark-axis factory outputs (human-vs-ai/slot15/swarm/art5/det/mcp),
  flywheel_pairs 08-08..12 (2,847), sft_recipe, eat_results trio,
  .sov3 training stack (finetune_jarvis 989, train/train_split/curated/splits),
  defence/ethics/sovereignty corpora. **>5,177 pairs → 315 signed cards (5.3 MB).**
- Harvest loops restored: `eat_all.py` (cron every 5 min) + `trigger_3090_sims.sh`
  (keeper) both resurrected from the grokbot/kimi-regen mirrors — the "missing
  script" disease that was silently starving the flywheel is fixed.

## PHASE 2 — RunPod GPU measurement ✅ STARTED, EXTEND NOW
- **BREAKTHROUGH:** the lane's "Mac can't SSH to RunPod" note is WRONG —
  `runpodctl ssh info <pod>` + `~/.runpod/ssh/runpodctl-ssh-key` works.
  RTX 3090 pod `fpowppss5ngtkw` (sov-repull) live, sim_burst + Ollama running.
- First real sweep: **16 GSPC axes × 7 models** (council-oowm, council-safe,
  mistral:7b, qwen3:4b, qwen2.5 7b/1.5b/0.5b) measured on the pod GPU →
  `{axis, model, prompt, response}` JSONL → pulled into the forest → mined.
- NEXT: (a) list the whole pod fleet (`runpodctl pod list`) and sweep every
  live pod; (b) schedule the sweep on the keeper cadence (hourly); (c) wire the
  pod's `sim_burst` history (16 rounds of city+jail sim data) into the mine.

## PHASE 3 — Cards → Training (the "3KB works for training" proof) ⏳ NEXT
- Target: 1,000 signed cards → first training run.
- Options (pick one): (a) LoRA on the 3090 pod (Ollama + mlx/torch on the pod's
  GPU, bounded ≤10 min per run); (b) Kaggle T4 kernel consuming the card JSONL
  (lane pattern exists: owem_kaggle_cluster); (c) lambda-GRPO step-based
  distillation on the pod.
- Each training run's model → joins the pod's Ollama roster → measured on the
  16 axes → new cards. The flywheel closes: **cards train models that measure
  the world that emits cards.**

## PHASE 4 — Live-data simulations (benchmark → new sims) ⏳ NEXT
- The user's core ask: "benchmarks recording into new simulations against live
  data". Wire: every card pack (25 records) → seeds new Sim World agents/axes
  (cards = agent knowledge); the sim's duel outcomes + agent axes → new probe
  targets → next benchmark sweep. The display shows this loop live.
- sovd integration deepens: scene nodes from IWM, which ingests honey (the
  sov-space C1 leg) — Rust core becomes the sim's brain, cards its memory.

## PHASE 5 — Mesh restoration (owner: Nick) 🚧 GATED
- GCP billing re-enable → SOV3 :3101 → record_memory MCP + full EAT loop +
  6 tunnels + OLM brain. Until then: local mine + RunPod fleet carry the loop.
- Oracle evac watcher armed; A1 hunter running; macOS stays the terminal.

## PHASE 6 — The Bureau surface (alignment with the sibling spec) ⏳ AFTER P0
- Rooms doctrine: Verify room shows every card (sig + hash, "verify it free
  forever"); Arena room embeds the Sim World overlay; GSPC Ladder reads the
  living DB + pod measurements; Containment/Sim City = the live town.
- Gate: the naming ruling (P0) + the Clerk persona naming.

## PHASE 7 — AG-UI: the agent-to-user leg ✅ WIRE LIVE, RENDERER NEXT
- **Adopted (not invented):** AG-UI (github.com/ag-ui-protocol/ag-ui, MIT) is the standard
  agent→user wire. RAS stack = MCP (tools, harness ctx.tools + MetaMCP spine) +
  A2A (agents, sov ring/pods) + **AG-UI (user, this phase)**.
- **Live now:** `agui-gateway.mjs` (LaunchAgent `com.meok.sim-world-agui`) subscribes to
  the sim plane and re-emits standard AG-UI events on `:4191/agui/stream`:
  STATE_SNAPSHOT / STATE_DELTA (JSON Patch) / CUSTOM (duel/benchmark/card/runpod).
  Verified: STATE_DELTA `{op:replace, path:/agents/...}` frames flowing live.
- **Boundary (swappable by design):** sandbox = runtime · AG-UI = wire ·
  renderer = whoever subscribes (CopilotKit React / assistant-ui next) ·
  Datastar/HTMX = outer shell. Cloudflare SSE gotcha handled (`no-transform`).
- **Governance watch-item (JEEVES flag):** AG-UI is 0.x, single-vendor
  (CopilotKit) — NOT foundation-governed like MCP (AAIF) / A2A (LF). Mitigation:
  pin SDK versions (python 0.1.20, TS 0.0.57), keep the wire decoupled (done),
  upgrade posture if donated to a foundation.
- NEXT: Pydantic AI AG-UI endpoint wrapping the harness agent (tokens + tool
  calls streamed to a CopilotKit shell), then LiveKit/Pipecat avatar greeter.

---

## WHAT ELSE IS NEEDED (gates / owners)

| # | Need | Owner | Unblocks |
|---|---|---|---|
| 1 | GCP billing re-enable (brief) | Nick | SOV3 :3101, record_memory, tunnels, OLM |
| 2 | Naming ruling | Nick | Bureau P0, Clerk persona |
| 3 | RunPod fleet sweep + pod budget | JEEVES (now) | Phase 2 scale-out |
| 4 | Training consumer decision (LoRA/Kaggle/GRPO) | JEEVES + Nick | Phase 3 first run |
| 5 | 1,000-card milestone | JEEVES (mine) | Phase 3 go |
| 6 | Card → sim seeding (Phase 4 wire) | JEEVES | closed loop |
| 7 | Overnight supervisor window expiry | auto (04:00) | next night's config |

## PHASE 3c — LoRA → GGUF → POD ROSTER ✅ DONE
- Fused 300-it LoRA → fp16 (mlx fuse --dequantize) → GGUF q8_0 (525MB, llama.cpp)
- Shipped to 3090 pod → `ollama create qwen2.5-0.5b-cards:latest` → **on the measured roster**
- 16-axis GPU sweep of the trained model COMPLETE → records → mine → **signed cards**
- The flywheel now trains models that join the fleet that measures them — loop closed at fleet level.

## EAT ALL — PARALLEL (new)
- `eat_all_parallel.py` (LaunchAgent `com.meok.eat-all-parallel`, 15 min, lock-guarded):
  fires every phase CONCURRENTLY (per-phase hard timeouts), REPORT last.
  **17 phases in 5.1s wall** (serial was the sum). Honest failures surface per-phase.
- Stock 5-min serial cron still runs; the lock prevents collision.

## BATTLE PLAN EXECUTION STATUS (EAT THE MOMENT, 2026-08-18)
| Plan item | Status | Evidence |
|---|---|---|
| Phase 0 #2 axis reconciliation | [H] DONE | GR2_RECONCILIATION_INPUT (13,275 pairs counted; 16-axes tension flagged; ruling stays Nick's) |
| Phase 0 #3 Zenodo/arXiv | [H] DONE | 25 DOIs live incl. 417-Provision paper (10.5281/zenodo.21991105, TODAY) + signed-cards paper — arXiv clock defused |
| Phase 1 #5 signed index | [H] PREPARED | INDEX_MANIFEST.json (458 cards, chain true) — awaits [F] name ruling |
| Phase 1 #6 self-critical arena | [H] DONE | base 0.688 vs 300it-LoRA 0.938 on deterministic 16-axis judge (no LLM-as-judge, canon GY.0#2); 150it echo failure documented |
| Phase 1 #7 crosswalk gap map | [H] DONE | 16 core axes covered; N = 10 thin fields + 46% 'mine' unclassified |
| Phase 0 #4 apex fixes | [F]-adjacent | title/404 work tracked by the site lane (k3) |
| Phase 2+ money legs | [F] | counsel 11 Sep · Growth Lab 27 Sep · insurer 30 Sep — demand evidence banked (AISI, Ninth Cir., 417 paper) |

## RUNNING NOW (agents)
- `com.meok.sim-world-overnight` — sim evolution + benchmarks + cards (till 04:00)
- `com.meok.sim-world-miner` — continuous mine (every 5 min, auto-discovery)
- `com.meok.sim-world-watch` — GUI plugin HMR
- cron `eat_all.py` (restored) + `trigger_3090_sims.sh` (restored) + eat-autopilot
- 3090 pod: sim_burst + Ollama + 16×7 sweep (in flight)

## METRICS TO WATCH
- Cards: 315 (target 1,000 → Phase 3)
- Living DB records: ~3,200 (target 10,000)
- Pod sweep records: 112/full sweep (target: every pod, hourly)
- World rounds: ~18,000 (target: continuous)
