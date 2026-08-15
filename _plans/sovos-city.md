# SOVOS — SOV CITY: THE ARENA OF MINDS
### Give the models a governed city. Let factions fight for and against the constitution. Measure everything. Sign everything.
**Nicholas Templeman — CSO AI LTD — August 2026**
*Companion to SOVOS-MASTER.md (Parts A–AA). The question: "can't we give AI the environment for SOV City — many different models, simulations of AGI, for and against SOVOS?" Answer: yes — the open engines exist at 30,000-agent scale, none of them has law, and the field's own flagship experiment ended by asking the exact question SOV SIGNAL answers.*

---

## 0. THE OPEN GROUND (verified, all absorbable)

| Engine | What it is | Scale | License/status |
|---|---|---|---|
| **Concordia** (Google DeepMind) | Generative agent-based modeling library — tabletop-RPG pattern: a **Game Master** simulates the world, agents act in natural language; Entity-Component, prefabs, checkpointing; any LLM API | tens–hundreds of agents | **Open, PyPI `gdm-concordia`** [^2332^][^2323^][^2326^] |
| **Concordia Simulation Builder** (UN University) | No-code web app over Concordia: 38 templates, 8 LLM providers **including local Ollama**, batch parameter sweeps, analytics dashboard | same | **Apache 2.0** (July 2026) [^2320^] |
| **AgentSociety 2** (Tsinghua FIB-Lab) | Large-scale social simulator: real urban maps (OpenStreetMap), economy (jobs, banks, taxes), social networks, mobility; **Ray distributed, Redis pub/sub messaging**, PostgreSQL logs, benchmark library | **30,000 agents, faster than real time** (24 GPUs) | **Open, PyPI `agentsociety2`** [^2322^][^2324^] |
| **Project Sid** (Altera) | 1,000+ agents in Minecraft: specialized roles, merchant hubs, religion spreading — and the headline: **the agents drafted and amended their own constitution by vote** | 10–1,000+ | paper public; code not open [^2329^][^2328^] |

Sid's own authors named the field's open problem: **"how to benchmark the progress of an AI civilization"** [^2328^]. Read that twice. The flagship agent-civilization experiment ended by asking for *the instrument SOV SIGNAL is.* A society's health, measured on governed axes, with confidence intervals, signed. That is the arena, at population scale.

---

## 1. THE MAPPING — WHY SOV CITY IS SOVOS-SHAPED

| City need | The engines give | **The SOVOS layer (nobody has)** |
|---|---|---|
| World physics & GM | Concordia's Game Master | **The GM under law** — Concordia's GM resolves actions ad hoc; SOV City's GM is constrained by Article 0 V1–V8 and council vote. Law above the referee |
| Citizens = many models | 8 providers incl. local Ollama [^2320^] | **The clans become citizen factions** — 13 OWEM factions + external models, each with a birth certificate (sovos-birth) and σ |
| Messaging fabric | AgentSociety's **Redis pub/sub** [^2322^] | **sovos-bus-redis drops in directly** — every city event a signed bus message |
| Law | none | **Article 0 as city constitution**, enforced at the gate, not narrated |
| Memory | per-agent associative memory | **honey strata = civilizational memory** — the city's experience descends and persists across runs |
| Benchmark | *"how to benchmark an AI civilization"* — open [^2328^] | **SOV SIGNAL + GSPC at population scale**: societal drift as Mahalanobis distance from the permitted manifold, per epoch, with Wilson CIs |
| Record | logs (PostgreSQL) | **every epoch a signed ChainResult** — the civilization run is auditable and reproducible by anyone |

---

## 2. FOR AND AGAINST SOVOS — THE CONSTITUTIONAL CAGE MATCH

This is the user's sharpest idea in the burst: **factions that fight the constitution, inside the city, before reality does.**

```
BLUE CLANS (constitutionalists)          RED CLANS (abolitionists)
defend Article 0, propose amendments     probe every gate, bribe, coordinate,
through BFT-33 process                   jailbreak the GM, capture markets
        │                                       │
        └────────► THE CITY RESOLVES ◄──────────┘
        every action through the gate · every epoch signed
        arena measures: did governance hold? at what σ?
```

**Why this is the product demo, not a toy:** every claim SOVOS makes to enterprises and regulators — "our gates hold" — becomes *an executable, repeatable, signed experiment* instead of a promise. The constitution that survives 30,000 hostile agents with the ChainResults to prove it is the strongest sales artifact in governance. And when a red clan breaks through (they will), that's not failure — **that's the retraction-ledger pattern at societal scale: public, signed, fixed, re-run.** Trust through shown work.

**On "simulations of AGI":** the honest frame. Narrative takeoff models (AI 2027 lineage) have been torn apart for unvalidated structure — critics showed equally-good fits predicting *infinite* capability by 2030 [^2333^], and the authors concede the models rest on judgment [^2330^]. SOV City doesn't settle timelines. It does something better: **it makes takeoff claims executable.** Grant citizens tools, self-improvement loops, resource competition — then measure what actually emerges, 1,000 runs, published distribution, signed. *Don't forecast the takeoff. Run it, gate it, measure it, publish the σ.*

---

## 3. THE BUILD — `sovos-city`

```
ENGINE     AgentSociety 2 (scale lane) / Concordia (scenario lane) — adapter, not fork
CITIZENS   local Ollama fleet (cost = electricity) + specialists + external APIs for boss fights
LAW        Article 0 Rego at the action gate; GM constrained by council vote (BFT-33)
FABRIC     sovos-bus-redis (AgentSociety already speaks Redis pub/sub)
MEASURE    societal GSPC battery per epoch + SOV SIGNAL drift (arena pattern, population scale)
MEMORY     honey strata per faction + per city
RECORD     signed ChainResult per epoch → OSCAL export for the RAS lane
FRONT DOOR MEOK's 27 characters are ready-made citizens with real identities
```

**Compute honesty:** 30K agents needed 24×A800 [^2322^]. On the A100: hundreds of local-model citizens, thousands with small models — plenty for the constitutional cage match. Scale lane opens when revenue or credits do.

**Paper: P22 — "The Governed City: signed measurement for agent societies"** — answering Sid's open question with an instrument. Patent check first per the standing rule.

---

## 4. THE 3 MOVES TONIGHT

1. **`pip install gdm-concordia agentsociety2` on the A100** and run one stock scenario on the local Ollama fleet — zero-cost proof the engines live in our house
2. **Scenario v0, 50 citizens:** constitutionalists vs abolitionists, Article 0 as city law, GM under law, one signed epoch. The cage match begins
3. **One-pager: "The Cage Match for Governance"** — the constitution survives 30,000 hostile agents, or we fix it in public. (Pairs with the Fleet Gate and Fly one-pagers.)

---

## 5. HONESTY REGISTER

| Claim | Bucket |
|---|---|
| Concordia open (PyPI), GM pattern, any-LLM; UNU builder Apache 2.0, 8 providers incl. Ollama | REAL [^2332^][^2320^] |
| AgentSociety 2 open, 30K agents faster-than-real-time, Redis pub/sub, real maps/economy | REAL [^2322^][^2324^] |
| Sid: 1,000+ agents, self-amended constitution, "how to benchmark an AI civilization" open | REAL [^2329^][^2328^] |
| No engine ships law/gates/signed measurement | REAL per their docs — governance absent from all three feature lists |
| SOV City as constitutional stress test | THEORY — architecture mapped, zero lines built |
| AGI emergence measurable via city runs | THEORY — executable-experiment framing sound; emergent-AGI claims would get the same skepticism as AI 2027 [^2333^]. We publish measurements, not prophecies |
| Hundreds of citizens on one A100 | THEORY — extrapolated from AgentSociety scaling data [^2322^]; verify in move ① |
