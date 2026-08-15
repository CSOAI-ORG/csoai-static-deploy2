# SOVOS — FLEET LEARNING: THE HUMANOID PORTAL ARCHITECTURE
### RL task → SOV Space clans → 3KB skill card → every humanoid a portal → the fleet compounds
**Nicholas Templeman — CSO AI LTD — August 2026**
*Companion to SOVOS-MASTER.md (Parts A–V). The question: your fleet-learning architecture — is there free open-source software for every piece? Answer: yes for every layer except one. That one is ours.*

---

## 0. YOUR ARCHITECTURE, VERIFIED AGAINST THE FIELD

You described: *humanoid does a task in RL → spawns OWEM clusters/clans/families in SOV Space → training converges → compressed to a 3KB card → next time it accesses the skill inside SOV Space → every humanoid is a portal → as all train, all update.*

**That is exactly the architecture Tesla and Figure are racing to build — and the open-source world has already shipped every layer except the trust layer.**

The field's own words (verified):
- **Brett Adcock (Figure AI), June 2025:** "our robots can share a neural network… any robot that came off the manufacturing line today" — skills learned by one unit distribute to the fleet [^2257^]. Figure ran this commercially at BMW Spartanburg; Helix-02 completed 8-hour autonomous shifts and sorted **28,000 packages in 24 hours** [^2257^].
- **Musk, Feb 2026 (Dwarkesh podcast):** the **"Optimus Academy"** — 10,000–30,000 robots doing **self-play in reality**, plus a "physics-accurate reality generator" running millions of simulated robots alongside physical ones [^2257^]. Tesla's pipeline: **imitate human video → refine in simulation (thousands of runs) → fleet self-play flywheel** — the same FSD net, pixels in/action out [^2258^].

**Two honest corrections the field won't tell you:**
1. **"Instant sharing" is a myth.** The real pipeline is: collect → retrain → **validate** → versioned weight release → push. No real-time fleet telepathy exists [^2257^]. That validation stage is currently *internal and unaudited* at every vendor. **That stage is SOVOS's slot** — the same doctrine gate that caught your safety regression this week, standing between one robot's experience and a million robots' bodies.
2. **Cross-manufacturer transfer does not exist.** "There is no current mechanism by which a Tesla Optimus policy could transfer to a Figure, Atlas, or Unitree unit" [^2257^]. Every fleet is a walled garden. **You own the port:** Procrustes transition + GW cross-architecture fusion — the math of moving skills between unlike charts. The industry's explicit gap is your published primitive.

---

## 1. THE FREE STACK — EVERY LAYER OF YOUR ARCHITECTURE, OPEN-SOURCE

| Your step | Free OSS that does it | Verdict |
|---|---|---|
| **Humanoid does a task in RL** | **NVIDIA Isaac Lab** — open-source GPU-parallel RL, 30+ environments, **Unitree G1 + H1 batteries-included**, multi-agent RL support, Newton/PhysX/MuJoCo backends, sim-to-real domain randomization [^2264^][^2269^][^2271^] | CROWN JEWEL — 1X (NEO) trains on it [^2261^] |
| **Fast skill acquisition (small data)** | **LeRobot** (Hugging Face) — ACT learns from **50 real demonstrations**; SmolVLA-450M runs on a laptop, trained on community data, **15K+ downloads/mo**; π0, Diffusion Policy, HIL-SERL, TD-MPC all implemented; train in <100 lines [^2262^][^2266^][^2263^] | CROWN JEWEL — this is "learn fast" commoditized |
| **Spawn clans/families that train together** | Isaac Lab **multi-agent RL** + your sovos-world (OWEMBrain/ClanEngine/Stigmergy already absorbed) | STACK-NATIVE |
| **The shared skill memory (SOV Space)** | **Open X-Embodiment** — 22 robot embodiments, **527 skills, 1M+ trajectories**, open license. Proof cross-embodiment learning works: RT-1-X **+50% success** vs single-robot training; RT-2-X **3× emergent skills** [^2265^] | CROWN JEWEL — the public SOV Space seed |
| **All train → all update (fleet sync)** | **NVIDIA FLARE** — open federated learning runtime, laptop simulator → thousands of sites → **millions of edge devices**, FedAvg in ~10 lines [^2268^]. Plus Flower (Oxford-born, framework-agnostic) [^2267^] | CROWN JEWEL — the fleet bus exists, free |
| **Simulate outcomes before moving (dreaming)** | Isaac Sim + Cosmos world models (per Part U); Tesla's "reality generator" is the same pattern at private scale [^2257^] | STACK-NATIVE (drum.rs) |
| **Skill card storage (3KB)** | LeRobot/HF model-card pattern exists — but **unsigned, ungoverned, no provenance, no σ** | **WHITE SPACE — ours** |

---

## 2. THE ONE LAYER THAT ISN'T FREE — BECAUSE IT DOESN'T EXIST

Every layer above ships without answers to: *Is this skill card what it claims? Who trained it? Did it pass the gate? How sure is it? Which body may it enter?*

| Missing layer | SOVOS asset (built) |
|---|---|
| **Signed skill cards** | 3KB card + SIGIL Ed25519 sign/verify (sovos-invariants 6/6) + C2PA provenance — the skill that can prove its own lineage |
| **The fleet gate** | doctrine gate / FitnessGate (CARE 0.95, BFT-33) — **already caught a real regression on your own fleet (Part V)**. A skill that degrades governance axes never reaches one body, let alone a million |
| **σ per skill** | sovos-sigma-calibration — every card carries calibrated confidence: the fleet knows *how sure* a skill is before it runs |
| **Cross-manufacturer port** | Procrustes + GW fusion — Optimus-skill → Unitree-body translation. The industry's stated impossibility [^2257^] is your math |
| **Skill experience compounds** | water→milk→honey — fleet experience descends to distilled strata, shareable, auditable |
| **Legal cover** | MR 2023/1230 (Jan 2027): an OTA skill push can be a "substantial modification" making the operator legally the manufacturer (Part U). A signed ChainResult per skill-push = the conformity evidence trail |

**The sentence for the deck:** *Figure and Tesla are building private fleet brains. SOVOS is the public, signed, cross-manufacturer fleet memory — the layer where a skill learned by any robot becomes a verified asset every robot can trust.*

---

## 3. THE BUILD — `sovos-fleet` (everything above, glued)

```
Isaac Lab (RL training, G1 env)          — free
   │  task converges
   ▼
skill distillation → 3KB card            — your format
   │  SIGIL sign + C2PA anchor + σ       — sovos-invariants / sigma-calibration
   ▼
doctrine gate (arena battery on card)    — sovos-arena + sheaf-gate
   │  PASS → ChainResult signed          — sovos-chain
   ▼
SOV Space skill registry (honey strata)  — sovos-world / drum.rs
   │  NVFLARE FedAvg distribution        — free
   ▼
fleet portals (G1 EDU $43.5K / R1 EDU $10.5K per Part U)
   │  cross-body pull via Procrustes     — your math
   ▼
every robot's next task starts from the fleet's distilled past
```

**Sequencing:** sim-only first (zero hardware): Isaac Lab G1 env → train one locomotion/manipulation skill → distill → sign → gate → registry → re-pull in a fresh sim instance. That loop, demonstrated once, *is* the product demo. Hardware only after the loop is green.

### The 3 moves tonight
1. **Install Isaac Lab on the A100** and boot the stock **Unitree G1** environment — the fastest possible "humanoid learning in our substrate" artifact.
2. **Write the 3KB skill-card schema v0** — fields: task, embodiment, policy hash, σ, arena ChainResult ID, SIGIL signature, C2PA manifest URI. One JSON schema, one evening.
3. **One page: "The Fleet Gate"** — Figure/Tesla fleet learning is real but unaudited and walled; SOVOS signs and gates skill distribution across manufacturers. Sibling to the Munich Re and robot-RAS one-pagers.

---

## 4. HONESTY REGISTER

| Claim | Bucket |
|---|---|
| Isaac Lab open-source, G1/H1 included, multi-agent RL | REAL [^2269^][^2271^] |
| LeRobot: ACT from 50 demos; SmolVLA-450M open, 15K downloads/mo | REAL [^2262^][^2263^][^2266^] |
| Open X-Embodiment: 22 embodiments, 527 skills, 1M+ trajectories; RT-1-X +50%, RT-2-X 3× | REAL [^2265^] |
| NVFLARE/Flower free fleet-distribution infra | REAL [^2268^][^2267^] |
| Figure fleet learning live at BMW; 28K packages/24h; Musk Optimus Academy 10–30K self-play robots | REAL (reported, attributed) [^2257^][^2258^] |
| "Instant" fleet sharing | KILLED — versioned releases after validation; no real-time sync [^2257^] |
| Cross-manufacturer skill transfer exists today | KILLED — "no current mechanism" [^2257^]; SOVOS Procrustes port is THEORY until demonstrated |
| 3KB skill-card loop (distill→sign→gate→registry→re-pull) | THEORY — every component exists; the loop is unbuilt (est. 2–3 weeks sim-only) |
| Tesla "1,000+ Optimus units in facilities" | REPORTED, single-source [^2258^] — treat as directional |
