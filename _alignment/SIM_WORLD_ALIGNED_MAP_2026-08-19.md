# SIM WORLD LANE — TOP-DOWN ALIGNED WORK MAP
**2026-08-19 · consolidated from: ESTATE-CONNECTION-MAP · PASTE-TO-DEEPSEEK-AGENTS · PRODUCT-E2E-2026-08-19 · GSPC ROADMAP · SOVOS-MASTER A+B · EAT-THE-MOMENT · the 100-move charter.**

## THE ALIGNMENT (who does what)
| Lane | Owns | I feed | I depend on |
|---|---|---|---|
| **Claude** | councilof-ai repo, upstream PRs, GitHub org | signed card evidence, measurement results, the arena data | canon rulings, the board API, drift-guard surfaces |
| **K3** | csoai-static-deploy2 tree, pod fleet, estate chain signing, Zenodo/Kaggle | card corpus, sweep measurements, GR.2 reconciliation, the home-patch fix | the estate chain format, pod coordination file, Zenodo DOIs |
| **Me (DeepSeek/harness)** | **measurement only** — Sim World display, the mine, cards, AG-UI wire, evidence trail | the E2E loop's "every run signs a receipt" layer | live board (councilof.ai/api/gspc), trust root (did.json), pod fleet |
| **Nick** | rulings, logins, spend | armed [F] gates | naming ruling → Phases C–F |

## THE THREE WORK SURFACES

### SURFACE 1 — RUNPOD (the fleet, measurement on GPU)
- **3090 (sov-repull)**: my sweeps (16×7 models, 350+ records → cards) · sim_burst rounds → fuel · the deployed `qwen2.5-0.5b-cards` model · LANE_COORDINATION.md handoffs.
- **A100s (K3's)**: fleet sweep v2 with the REAL harness (first cell: affect acc=0.3333 MEASURED) — I consume its signed cells; I never deploy there.
- **Etiquette (binding):** resolve SSH via the API every time · `pgrep` before spawn (never double-spawn spend loops) · termination = owner-nod only · community capacity = wait, not retry-storm.
- **Aligned next:** hourly sweep cadence · pod cost register · my GGUF re-register rule (MF.*.gguf, never FROM-dir) after pod reboots.

### SURFACE 2 — THE HARNESS (the GUI — my display surface)
- **Sim World** (CesiumJS globe + 7 sim tools): the live arena render — display only, never runs the sim.
- **AG-UI gateway** :4191 — my wire; the estate's reference is `~/clawd/agui-wire` (pinned 0.1.19-stable/ts 0.0.57) — NOT wired to the live board yet (honest per the map; the live board loop stays pod→sign→paste→deploy until the lane wires it properly).
- **Aligned next:** the axis panel sources the canon board (done — display shows 14 canon axes) · HITL consent checkpoint · the CopilotKit shell when the naming ruling lands.

### SURFACE 3 — OWN SYSTEMS (the mine + evidence on the Mac)
- **The mine**: honey → 470 signed h3k cards → chain 100% → SFT corpus (13.7K) → MLX LoRA → GGUF.
- **The evidence trail**: verify-all 11/11 hourly + audit-deep 16/16 6-hourly (self-healing) · world-restore shim · the never-assume incident register.
- **Aligned next:** the estate's canonical signature format (json.dumps sort_keys + sha256 + Ed25519 over content_id) — my cards should speak it so they verify against did:web:csoai.org, not just the local key · the mine's classifier already maps to the 14 canon axes.

## THE PHASES (estate-aligned, E2E pack order)

### PHASE 0 — CREDIBILITY CORE (now → 27 Aug) · my share
- [H] Six P0 probe fixes — my estate's share: verify the sim surfaces serve canon copy (no kill-list words: sovereign/SOV*/DEFONEOS never in display).
- [H] Boundary-test respect: REPORTED never beside MEASURED (my cards carry register labels) · telemetry can't alter scores (the deterministic judge, no LLM-as-judge) · the two write paths (my mine's signing is the isolated path).
- [H] The frozen/fluid ledger shape: my chain = the fluid signed chain; the DOI spine (10.5281/zenodo.21991104) anchors frozen releases — my card packs should cite it.
- [H] Arena feeding: the E2E loop says "every run signs a receipt" — my sweeps already do (cards).

### PHASE 1 — INSURER PITCH (27 Aug → 30 Sep) · my share
- [H] SMB safety-check pane data: my measurement evidence (base vs LoRA, human baselines) is insurer-ready material.
- [H] Human-baseline Leg B (DPIA) prep + the model-vs-human headline behind the eval harness.
- [F] Counsel 11 Sep · Growth Lab 27 Sep · insurer 30 Sep — my signed evidence is the exhibit.

### PHASE 2 — HUMAN UPLIFT + ART. 50 (30 Sep → 2 Dec) · my share
- [H] The Art. 50 countdown demo: "0 of 108 markings survive transformation" — my ProvBench-adjacent measurement; the 2 Dec launch artifact.
- [H] The human-training pane's signed participation records — my card format is the credential rail seed.
- [H] Never-build respect: no human-like avatar on credibility surfaces (my avatar greeter stays off the credibility surface).

### MEOK (parallel B-sheet) · my share
- [H] B4/B5 workers (dsh pinned, unmodified, swappable) — my harness IS the dsh worker pattern.
- [H] B9 key isolation: my signing (local sov33) stays out of any worker path — the estate key never travels.

## THE COORDINATION CADENCE (binding)
1. LANE_COORDINATION.md on the pod — read before shared surfaces; append start/finish.
2. Commit by name, never `git add -A` on shared trees.
3. Claim provisional until verified — the probe wins.
4. One lane per surface — no prod deploys from this lane, ever.

## EAT — the standing loop
eat_all parallel (21 phases / 5s) → honey → miner (auto-discovery, 32 sources) → cards → chain → training → GGUF → pod → measurement → new cards. **Running continuously; verified 16/16.**

## THE ONE-LINE LANDING
Measurement only, everywhere: my Sim World renders the canon board, my mine signs the receipts in the estate's vocabulary, my fleet work respects the etiquette, my evidence feeds the E2E loop — and every claim is provisional until the probe says otherwise.
