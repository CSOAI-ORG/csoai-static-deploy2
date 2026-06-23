# Agent-47 V3 → Sovereign Town mining manifest

**Mined from:** `~/clawd/_intake/kimi_agent47_town_v3/`  
**Copied assets:** `~/clawd/sovereign-town/research/agent47_assets/`  
**Date:** 2026-06-21

This manifest records what is reusable from the Agent-47 immersive-world research and how it maps into Sovereign Town (P0/P1).

---

## 1. Visual / 3D pipeline (high-value for future UI)

### 1.1 Stack to adopt
- **Three.js + React Three Fiber** for the browser 3D town.
- **@react-three/drei** (`<Detailed>`, `<Billboard>`, instancing helpers, `<Sky>`, `<Environment>`).
- **@react-three/postprocessing** for bloom / outline / SSAO.
- **Zustand** for world state (agents, camera, weather, pheromones).
- **Web Workers** for agent pathfinding/AI so the render thread stays smooth.

### 1.2 Performance patterns
- **LOD tiers:** full VRM <20m, simplified mesh 20-50m, billboard 50-100m, dot >100m.
- **Instancing** for trees, lamps, houses, server-rack LEDs.
- **Frustum culling** wrapper for expensive district groups.
- **Adaptive quality** manager that throttles particles/LOD based on FPS.
- **Animation throttling** by camera distance.

### 1.3 Reusable components
Files copied under `agent47_assets/app/src/components/`:

| File | What it gives Sovereign Town |
|------|------------------------------|
| `TownScene.tsx` | Full 3D canvas + environment system; replace 47 agents with our 140 personas. |
| `Dashboard.tsx` | Metrics panel layout, chart containers, proposal feed. |
| `Minimap.tsx` | Top-down SVG/Canvas agent-position map — can be downgraded to a 2D hive-grid. |
| `AgentPassport.tsx` | Passport card UI, verification CTA, capability badges. |
| `AgentListPanel.tsx` | Sortable/filterable agent roster. |
| `NotificationFeed.tsx` | Real-time governance event stream. |
| `ControlBar.tsx` | Camera-mode toggle, time-scale, quality selector. |

### 1.4 World layout
- Radial 800m × 800m town with 8 spoke districts around a central SOV3 tower.
- Each district corresponds to one or more Sovereign Town hives (see mapping below).
- Buildings already specified with dimensions, colors, occupancy, and ambient pheromones.

### 1.5 District → hive mapping
| Agent-47 district | Sovereign Town hives |
|-------------------|----------------------|
| Central | `proofof.ai` (verifier/courthouse), sovereign king node |
| Governance | `councilof.ai`, `ethicalgovernanceof.ai` |
| Commerce | `haulage.app`, `grabhire.ai`, `muckaway.ai`, `planthire.ai`, `commercialvehicle.ai`, `loopfactory.ai` |
| Wellness | `koikeeper.ai`, `fishkeeper.ai`, `meok.ai` |
| Innovation | `openmoe.ai`, `cobolbridge.ai`, `openmcp.ai` |
| Safety | `asisecurity.ai`, `safetyof.ai`, `agisafe.ai`, `suicidestop.ai` |
| Legal | `landlaw.ai`, `dataprivacyof.ai`, `accountabilityof.ai`, `biasdetectionof.ai`, `transparencyof.ai` |
| Media | `socialmediamanager.ai`, `proofof.ai` |
| Residential Ring | The persona population (140 agents) |

---

## 2. Gamification / dynamics

### 2.1 Pheromone system
Agent-47 defines typed pheromones that can be ported to Sovereign Town as **observable event signals**:
- `mcp.queen.gold` — sovereign consensus pulse.
- `mcp.alarm.red` — care-floor breach / crime.
- `mcp.trail.green` — cooperative/help_peer action.
- `mcp.cleanup.black` — remediation / welfare intervention.
- `mcp.gate.guard` — gate deny/escalate.

Mapping: emit these from `sim.py` when actions execute, then aggregate in `pheromone_bus.py`.

### 2.2 Caste / archetype visual identity
Agent-47 uses 7 castes + 5-8 VRM archetypes. Sovereign Town already has **6 MEOK archetypes** (Scholar, Guardian, Healer, Trickster, Pioneer, Mystic). Next step: assign each archetype a consistent color, outfit, and VRM base model for the 3D viewer.

| MEOK archetype | Suggested color | Caste anchor |
|----------------|-----------------|--------------|
| Scholar | indigo #6366f1 | scientist |
| Guardian | steel #4A5568 | leader / security |
| Healer | teal #14b8a6 | mediator |
| Trickster | amber #f59e0b | artist / explorer |
| Pioneer | orange #f97316 | merchant / builder |
| Mystic | violet #8b5cf6 | seeker |

### 2.3 Economy / x402 micropayments
Agent-47 treats pheromone-like reputation and x402 micro-transactions as first-class. Sovereign Town can extend `gate_access.py` / `consent_vault.py` to issue signed x402-style capability tokens for each action.

---

## 3. Backend / architecture improvements

### 3.1 Observation-first streaming
Agent-47 pushes agent state over WebSocket; clients render deltas. Sovereign Town should:
1. Keep `flywheel_ledger_*.jsonl` as append-only source of truth.
2. Have `dashboard_server.py` tail the ledger and stream `/ws/feed` to the dashboard.
3. Clients subscribe by district/arm instead of polling the whole episode file.

### 3.2 API surface already started
`dashboard_server.py` exposes:
- `/api/status`, `/api/hives`, `/api/characters`, `/api/episodes`, `/api/ledger`, `/api/models`, `/api/verify`

Add from Agent-47 design:
- `/api/hives/{id}/passport` — signed passport JSON.
- `/api/hives/{id}/stream` or WebSocket — live episode feed.
- `/api/world/state` — current town state (commons, lawlessness, trust).
- `/api/governance/proposals` — BFT council proposals.

### 3.3 WebGPU / compute
Agent-47 rendering doc recommends WebGPU for particle systems and agent AI batching. Sovereign Town's simulation is Python-driven, but the **browser dashboard** can use WebGPU compute shaders for:
- Pheromone diffusion heatmap.
- Agent position interpolation.
- Ledger signature batch verification.

---

## 4. Immediate integration tasks (prioritized)

| Priority | Task | File to change |
|----------|------|----------------|
| P0 | Finish dark-brand dashboard at `/dashboard` | `dashboard_server.py` + `dashboard.html` |
| P0 | Wire live ledger tail into dashboard | `dashboard_server.py` `/api/ledger`, `/ws/feed` |
| P1 | Add character archetype colors to `characters.json` | `enrich_personas.py` |
| P1 | Generate SVG charts in whitepapers | `report.py` |
| P1 | Upgrade `/passport` verifier to dark theme + chain verify | `proofof-site/passport.html` |
| P2 | Build 2D minimap from Agent47 `Minimap.tsx` | `dashboard.html` canvas map |
| P2 | Add WebSocket feed scaffold | `dashboard_server.py` |
| P3 | Port `TownScene.tsx` components to sovereign-town 3D viewer | new `sovereign-town/viewer/` |

---

## 5. Key documents to reference

In `agent47_assets/`:
- `architecture_rendering.md` — full rendering stack, LOD, instancing, performance budget.
- `architecture_world.md` — 800m town layout, district dimensions, building specs.
- `architecture_simulation.md` — simulation tick, agent AI, economy.
- `architecture_agent_brain.md` — memory, emotion, planning.
- `csoai_agent47.agent.final.md` — narrative/character bible.
- `app/src/components/TownScene.tsx`, `Dashboard.tsx`, `Minimap.tsx`, `AgentPassport.tsx` — reference implementations.

---

## 6. Decision log

- **No full VRM avatar pipeline yet** — P0/P1 stays 2D/dashboard; 3D viewer is P2.
- **No live WebSocket yet** — dashboard polls `/api/ledger` every 10s for now.
- **Copied only source/docs, not `node_modules`** — assets are ~8.7 MB; clean to version.
