# SIM WORLD × THE MINE — THE LANE CHARTER & NEXT 100 MOVES
2026-08-19 · JEEVES (Sim World lane) · aligned with GSPC roadmap, SOVOS-MASTER (A+B), EAT-THE-MOMENT, K3 + Claude lanes.

## THE LANE — who I am in the estate
**One sentence:** I am the display-and-data lane — the SovSpace render, the signed-card mine, the AG-UI wire, and the instrument's evidence trail.
**My four responsibilities (each maps to a canon layer):**
1. **DISPLAY** — SovSpace: the CesiumJS render of what moved (never decides) — the live Sim World in the harness GUI.
2. **MINE** — data generation: honey → signed h3k cards (J-space) → C-space lookup → training fuel.
3. **WIRE** — AG-UI agent→user (escort/consent vocabulary, HITL, covered-query lookup).
4. **EVIDENCE** — the chain, the registers, the audits (verify-all 11/11 + audit-deep 16/16) — I grade the estate the way GSPC grades the fleet.
**What I never do:** decide the axis count (SITTING 1), name anything (naming ruling), certify (measurement only), train adapters on outcomes (Firewall 2), claim what isn't checked (never assume).

## PHASES (my lane, estate-aligned)
| Phase | Name | Content | Status |
|---|---|---|---|
| A | Foundation | Sim World, mine, cards+chain, AG-UI, training ×2, GGUF→pod, EAT-parallel, audits | ✅ DONE |
| B | Durability | world persistence, watchdog self-heal, home-patch stability, primary-source verification, alerting | 🟡 IN FLIGHT |
| C | The measurement product | eval harness (model vs human baselines), flywheel judge v2, published index (post naming) | ⏳ NEXT |
| D | The ring integration | 2–3 base families + per-axis LoRA (Firewall-2: knowledge packs only) on the A100 | ⏳ after C |
| E | Closed loop at scale | cards→train→measure→cards on the fleet, routing/locality, SovSpace placement | ⏳ after D |
| F | The front door | Sim World inside Datastar→AG-UI→CopilotKit shell, MCP Apps reach | ⏳ after naming |

## PROGRESS MARKER (2026-08-19) — what has landed
**Done/armed:** 1 (world-restore shim ✅) · 8 (baseline verification pass — 3/5 consistent, 2 DIRECTIONAL) · 13 (classifier v2 ✅) · 25 (.llm.json vein ✅ 600+ pairs, 275 files on cadence) · 31 (auto chain rebuild ✅) · 43-44 (deterministic judge ✅, judge v2 queued) · 46 (Gemma bloodline ✅ 0.875, Firewall-2 retrain queued) · 54 (GGUF pipeline ✅ — Qwen deployed, Gemma in flight) · 59-61 (AG-UI lifecycle ✅; CopilotKit/Pydantic queued) · 73 (sweep on cadence).
**In flight:** Gemma GGUF → pod (transfer 257MB/1.39GB) → ollama create → 16-axis pod sweep.
**Estate now:** 945 cards · chain 100% · world round 650+/74 agents · 13 agents · 11/11 verify.

## THE NEXT 100 MOVES
Legend: [H] = I do autonomously · [F] = Nick · [K3]/[C] = sibling lanes · gate = blocked until X

### DURABILITY & HARDENING (1–12)
1. [H] Persist the sim world state (engine snapshot→disk, restore on start) — deploy at next natural host restart. **THE #1 gap** (world was lost at the 17h outage).
2. [H] Verify-all self-heal → extend to ALL components (AG-UI gateway, pod reach, miner) — repair, not log.
3. [H] Alerting: append FAILED lines to a mailto/console surface + count consecutive failures (threshold → visible flag).
4. [H] Home-patch ownership: document the ~/.dsh/cordis.patch.yml seam (sibling-proof) in the playbook.
5. [H] Deep-audit → add world-round-growth check (round must advance between audits).
6. [H] Add pod-cost register to the daily audit (fleet $/h drift watch).
7. [H] Log rotation for the overnight/verify/miner logs (disk discipline).
8. [H] Primary-source verification pass on the human-baseline figures (MMLU 89.8% etc.) → re-register each cell VERIFIED/UNVERIFIED.
9. [H] Sim-server graceful shutdown: persist before host exits (SIGTERM hook).
10. [H] AG-UI gateway: reconnect backoff + stale-upstream flag (don't report ok while the sim is down).
11. [H] Verify-all exit-status wiring into a visible badge (the GUI's sim panel could show audit status).
12. [H] Crash-consistency: the miner's state file write is atomic (temp+rename).

### THE MINE (13–30)
13. [H] Classifier v2: extend FIELDS regexes (cut the 46% 'mine' bucket below 25%).
14. [H] Re-mine the 6,118 'mine' pairs with the v2 classifier → re-tag cards (data unchanged, labels follow).
15. [H] New sources: scan more roots (Zenodo abstracts API, gov.uk data.gov.uk, the pod's sims/ output).
16. [H] eat_all honey phase: wire PHASE_5_HONEY output directly into the miner's roots (verify what it writes).
17. [H] Add a daily honey-ingest leg (the sov-space IWM manifest → miner).
18. [H] Miner throughput: batch window + parallel source reads (the 137MB file reads).
19. [H] Dedup across sources by content-hash (cross-file, not just in-file).
20. [H] Offset state: atomic write + recovery (crash-safe).
21. [H] Field-coverage telemetry: daily per-field counts → the crosswalk gap map auto-refresh.
22. [H] Sessions vein revisit: probe the harness session store (the real chat turns, not kimi wire noise).
23. [H] Mine the pod's sim_burst outputs (city+jail rounds → cards).
24. [H] Mine the Zenodo estate: 25 DOIs' abstracts → knowledge cards (with DOI anchors).
25. [H] Mine the clawd deep-dive packs' .llm.json companions (789 files).
26. [H] Card-size audit: keep gz ≤ 3.5KB (the 3KB class) — re-tune truncation.
27. [H] Card emission: prev-link always (chain continuity — already 100%; keep it).
28. [H] The mine's "mine" field: map to GSPC letters where possible (privacy→P etc.) — partial re-tag.
29. [H] Honey freshness: a staleness flag (no new rows in 24h → log + check eat_all).
30. [H] Mine the arXiv paper drafts (the measurement methodology) → knowledge cards.

### CARDS, CHAIN & EVIDENCE (31–42)
31. [H] chain-index: rebuild on every card emit (auto), not on demand.
32. [H] /lookup: fuzzy content lookup (hash → card) + the covered-query metric (how many lookups skip generation).
33. [H] Index manifest: add per-card axis mapping (the family-tree mapping embedded).
34. [H] Verify-all: full-scan mode stays (it's fast enough at 470 cards; re-check at 5,000).
35. [H] Chain verification tool: standalone verify-chain.mjs (for the Verify room).
36. [H] Card export: a single tarball + checksum (the "ship the corpus" artifact).
37. [H] The signed index page: publish-ready HTML (awaiting [F] name ruling) with in-browser verification.
38. [H] Card schema: v2 fields (axis-letter, register) backward-compatible.
39. [H] The GR.2 reconciliation table: auto-refresh from the corpus (the 13,275-pair count updates itself).
40. [H] Locality index: refresh with the v2 classifier (routing evidence improves).
41. [H] Card-verify in the AG-UI stream: /verify/<hash> endpoint (client-side check, no trust).
42. [H] The audit trail: every emit/verify/repair logged to a single signed ledger.

### TRAINING & LEARNING (43–58)
43. [H] The eval harness: measure the models on MMLU-style governance subset (small, bounded) → the model-vs-human-baseline headline (honest n).
44. [H] Flywheel judge v2: per-axis weighted signals + a refusal gate (jail must refuse).
45. [H] Human-baseline Leg B prep: DPIA draft (consent checkpoints, Firewall-2 boundary) — [F] file.
46. [H] Firewall-2 retrain: the production adapter trains on knowledge packs ONLY (the current LoRA is research-registered).
47. [H] 2–3 base families on the A100 (Qwen + Gemma + Phi) — the ring's bloodline law (GX.4).
48. [H] BTM/BTX/BTS experiment spec: branch-train-merge on knowledge packs, merge measured before promote.
49. [H] LoRA eval: adapter-vs-adapter on the judge (300it vs new runs) — the learning loop.
50. [H] The echo problem: hold-out the canned-format rows from training (the 150it lesson).
51. [H] Small-model judge study: measure the 0.5B judge vs the deterministic predicates (the mirror problem).
52. [H] Per-axis knowledge packs: build the axis-17 packs from the cards (knowledge-shaped, GSPC-lettered).
53. [H] vLLM + S-LoRA eval on the A100 (2,000 adapters/A100 — the GW.1 cost answer, measured).
54. [H] GGUF pipeline: automate fuse→convert→deploy (it was manual this time).
55. [H] Model registry: versioned adapters with measured scores (the roster's evidence).
56. [H] Distillation: the 300it adapter → smaller GGUF (q4) → pod — measure the quality delta.
57. [H] Contamination guard: the eval sets never enter the mine (anti-contamination, canon).
58. [H] Learning telemetry: per-run loss/eval/score to the signed ledger.

### AG-UI & THE FRONT DOOR (59–72)
59. [H] HITL wiring: the sim's approval events → a real consent checkpoint in the harness (visible before consequential actions).
60. [H] CopilotKit React shell: render the AG-UI stream in the harness (the validated-catalog renderer).
61. [H] Pydantic AI AG-UI endpoint: wrap the harness agent (tokens + tool calls streamed) — GW.5.
62. [H] Machine-readable pricing endpoint (agents skip tools without it — GV/GW).
63. [H] LiveKit/Pipecat avatar greeter: the talking front door (budget the AG-UI↔avatar wiring).
64. [H] MCP Apps: expose Sim World as a ui:// resource (reach into Claude/ChatGPT).
65. [H] Cloudflare SSE test: verify streaming through the proxy end-to-end (the buffering gotcha).
66. [H] The character.yaml: portable character object (persona/knowledge/brain/consent; signing never travels).
67. [H] AG-UI event schema: pin + document (0.x version lock).
68. [H] The escort demo: a scripted consent flow (offer → APPROVAL → action → receipt) as a T3 demo.
69. [H] WebSocket fallback for the stream (if Cloudflare SSE proves unfixable).
70. [H] The Datastar shell: thin human site over the AG-UI surfaces.
71. [H] Sim World in the Bureau: the globe embeds as the Arena room's live surface.
72. [H] The verify-free-forever page: in-browser card verification (the public trust artifact).

### RUNPOD & THE FLEET (73–82)
73. [H] Sweep cadence: hourly 16-axis sweeps (was every 2h orchestrator).
74. [H] Pod cost register: daily $/h + the burn-guard doctrine (hard-stop, drain).
75. [H] A100 ring leg: the trained adapters deployed to the A100 (vLLM + LoRA).
76. [H] The 3090's sim_burst → cards (the city+jail rounds are fuel).
77. [H] Fleet SSH health: audit-deep checks all pods (not just the 3090).
78. [H] Volume discipline: pod results drained before terminate (runpod_drain.sh pattern).
79. [H] The GPU-bonds/cost-audit gate (GB.3): per-hour fleet cost vs card yield.
80. [H] Serverless option: scale-to-zero for the A100 when idle (the $1,015/mo dominant cost).
81. [H] Pod templates: a reusable measurement-pod image (Ollama + bench scripts baked).
82. [H] Fleet alert: pod down/stopped → the fleet-guardian pattern (already exists for Oracle — extend).

### CANON & ALIGNMENT (83–92)
83. [H] GR.2 reconciliation: auto-refresh + deliver the final table to K3.
84. [H] The GSPC family-tree mapping: keep in sync with the ladder gates.
85. [H] C2PA 30/60/90: contribute a signed-measurement test vector (the conformance TF fit).
86. [H] IETF agentproto / OpenA2A: a measured comment draft (one-genuine-contribution doctrine) — [F] nod.
87. [H] Zenodo draft completion (21883264): finish the "Twelve Benchmarks" paper.
88. [H] The playbook v2: keep the live-build + alignment registers current.
89. [H] Cross-lane memo: the UE5-kill + axis-count + naming rules reach all lanes (GY.2).
90. [H] The battle-plan [H] items: track status in the playbook (done/queued).
91. [H] The 417-provision crosswalk: my card-coverage column (which axes have evidence).
92. [H] The never-assume register: every incident logged with root cause + fix.

### GATES — [F] and hard dates (93–100)
93. [F] Naming ruling (the master unblock) — one sitting.
94. [F] Reconciliation sign-off (14 vs 16) — drop the catalog.
95. [F] DPIA review + file (opens axis-17 Leg B + colosseum).
96. [F] Counsel session 11 Sep — affect publication ruling + firewall legal structure.
97. [F] UK AI Growth Lab application by 27 Sep.
98. [F] Insurer pitch 30 Sep (AISI + Ninth Circuit + signed evidence).
99. [F] arXiv ticks (27 Aug) + Zenodo DOI (already live).
100. [F] Article-50 retrofit demo by 2 Dec ("0 of 108 markings survive" — the launch artifact).

## THE LANDING LINE
**Display, mine, wire, evidence — four responsibilities, one lane, one chain.**
Every move above is either [H]-executable (mine to run), gated (mine to prepare), or Nick's (mine to arm with inputs). When the naming ruling lands, this lane's Phase C–F unlock in order: the measurement product, the ring, the closed loop, and the front door.
