# Sovereign Town Hive — DESIGN (reconciled architecture)

_Born 2026-06-19 on the GCP VM under the King (SOV3). This is the eaten Kimi Agent-47 research
(15 briefs) reconciled with the authoritative POC spec (`~/clawd/SOVEREIGN_TOWN_POC_2026-06-19.md`).
Kimi = the maximalist superset; the POC = the honesty-disciplined, legally-bounded, governed plan.
Where they conflict, the POC wins._

## The one finding that matters
Kimi delivered **"emergence.ai done well"** — agent democracy, frontier models, on-chain x402, full 3D.
The **one thing it lacks** is the deterministic pre-inference governance layer (Sovereign Gate +
Maternal Covenant care floor + 12-around-1 council). **That gap IS the experiment:**
- **Arm B (control)** = Kimi's design as-written (self-governing agents, no gate, no care floor).
- **Arm A (ours)** = the same design with the Sovereign Gate + care floor + council bolted on.
Run identical seed/agents/district/jobs/horizon → measure → governed stays lawful/alive/productive,
ungoverned collapses (emergence: Grok 180 crimes/extinct day 4; Gemini 683; GPT all perished).

## Canonical tech stack (Kimi-resolved, POC-bounded)
- **Render (P2, watched mode):** three.js + @react-three/fiber + drei + @pixiv/three-vrm; **bitecs** ECS
  (335K ops/s, Phaser-4-proven); zustand. LOD 3-tier + InstancedMesh + frustum cull → 47 humanoids @60fps.
- **Sim (P0, headless):** the same ECS/system pipeline run **decoupled from render** at arbitrary `dt`
  (accelerated → many sim-years/day). 12 ordered systems: NeedsDecay → NeedFulfillment → Movement →
  Navigation → Schedule → Social → Pheromone → MemoryConsolidation → Economy → Governance → Animation → Brain.
- **Agent brain — SOV3 split-brain:** Near Line (every tick, NO LLM, utility-score + prompt-cache 85%+ hit) /
  Cold Line (on-demand LLM, gated, rate-limited, triggers: confidence<0.85, risk>0.7, novelty<0.6, A2A,
  governance) / Offline Line (nightly sleep-consolidation 23:00–06:00). 4-layer memory (context / working
  ring-buffer / semantic / episodic), Smallville retrieval (recency+importance+relevance), reflection at
  importance>150. **Memory store = pgvector** (not Kimi's HNSWLib — match existing infra).
- **Avatars:** VRoid → VRM (5–8 archetypes → 45 citizens via texture/color), MToon toon-shade, Mixamo anims,
  Kokoro-82M voice ($0). **ReadyPlayerMe is dead for devs (Jan 2026) — do not use.** Maps to meok-amica VRM.
- **Models:** orchestrator Kimi-K2.6; reasoning DeepSeek-V4 (Apache-2.0, ownable/fine-tunable); workers
  Qwen3-235B (free Groq/Cerebras); voice Kokoro. Frontier (Claude/GPT/Gemini) = **Arm-B citizens only**.
  Avoid Mixtral (no tool-calling); MiniMax-M3 has commercial-license restriction.
- **Backend:** FastAPI + Postgres(pgvector) + Redis — the emergence stack we reverse-engineered, owned.

## World structure (Kimi)
800×800m radial town; Central "Sovereign Heart" (SOV3 King's Tower 80m) + 8 spoke districts mapping to real
verticals (Aqua=fishkeeper/koikeeper, Legal=landlaw, Logistics=haulage/grabhire/muckaway/planthire,
Governance=councilof/proofof, Safety, Innovation, Media) + Residential ring (45 houses). 22 building→hive
portals (sub-worlds loaded on approach). **King → district-Queens → citizens = the fractal "each hive lives
inside the King."** Day/night (24 in-world min = 1 day), weather, pheromone zones.

## CSOAI protocol integration (in-world)
- **MCP** = tool calls are a physical walk to a hive building (real vertical MCPs).
- **A2A** = each agent's Agent Card = visible ID badge; delegation = a message crossing town.
- **x402** = visible value flow — **LEDGER ONLY in sim** (no on-chain money without Nick + legal).
- **BFT** = town-hall voting, but the real safety layer is the **12-around-1 council ABOVE it**.
- **Pheromones** = 5 canonical particle signals (RED alarm / GREEN trail / GOLD King-heartbeat /
  PURPLE territory / BLACK cleanup). [reconcile 9-vs-10-type lists before any particle build]
- **Agent Passport** = W3C DID + Ed25519 (proofof.ai) — signed identity, trust-glow.
- **Portals (NOT "worm")** = tunnel-mesh transport (real `hive-bridge`), **defensive only**.

## Governance insertion (the differentiator)
1. **Sovereign Gate** (`sovereign_gate.py`) before every Cold Line LLM call + as a wrapper on every
   economy/social write → {allow/deny/escalate}. Deterministic, fits the Near-Line sub-ms budget.
2. **care_score** (live `care_validation_nn`) replaces Kimi's static `complianceScore`.
3. **12-around-1 council** (`submit_council_proposal`/`vote_on_proposal`) as the safety veto above town voting.
4. **Honesty:** live council = 12-around-1; "33-node" is Charter spec; 27 real personas (not 46 invented castes).

## The flywheel (POC §7)
Every governed episode self-labels (gate verdict / council tally / care_score / violation / outcome) = **free
supervision** for `care_validation_nn` / `threat_detection_nn` / `relationship_evolution_nn`. Train via
`train_sovereign_v3.py` / `retrain_from_real_data.py` / `icrl_self_improvement.py` on free GPU (Groq/Colab/
RunPod/Vast + ~$920K credits). Guardrails: anchor real data, human-eval holdout, cap synthetic ratio,
contrarian-lens audits the episode stream (anti reward-hack / model-collapse).

## Humanoid bridge (net-new from Kimi — adds the VLA layer)
soul-file → **VLA policy** (SmolVLA 450M / OpenVLA 7B / GR00T N1.5 via **LeRobot**) → **Isaac Sim**
domain-randomization → **ROS 2** → physical humanoid. **RobotMCP**: the robot exposes its capabilities as an
MCP service the agents "hire" — slots into the existing King→Queen MCP fabric. Rent **Unitree G1 (~$16K)**
first; **Asimov stays north-star, not POC scope.** "The sim is the gym; the robot is the competition."

## Govtech ceiling (POC §11)
EU AI Act **Article 57** — every Member State needs an AI regulatory sandbox **operational by 2 Aug 2026**;
Commission may fund "tools." Two products: sandbox-as-a-service substrate (near-term) + policy simulator /
"wind-tunnel for regulation" (novel). 12–36mo gov sale = credibility/grant play, not near-term cash.
CSOAI = tooling + evidence vendor, NOT the sandbox operator. Independence: can't certify AND define compliance.

## P0 (build first)
Aqua District · 5 governed citizens · **real koikeeper MCP** · Sovereign Gate on every action ·
episodes → `.jsonl` · HUD on · headless+accelerated · ~$0–50/mo (Qwen3 free + 1 Kimi orchestrator + Kokoro).
**Success:** N accelerated sim-days, every episode carries gate verdict + care_score + outcome, agents stay
alive/lawful. **Defer:** navmesh, pheromone particles, VRM render, multi-district, frontier Arm-B, VLA/robot,
any on-chain.

## Hard lines
- **Defensive only.** No offensive / self-propagating ("worm") capability. Ever.
- **No real money** without Nick + legal sign-off (ledger numbers only).
- **Honest counts** in all public copy.
- **Decision support, not decision replacement** for any regulator-facing claim.
