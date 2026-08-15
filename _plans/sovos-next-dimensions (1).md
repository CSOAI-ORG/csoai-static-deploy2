# SOVOS — THE NEXT DIMENSIONS
### What the stack unlocks now: Glass OS, immersive characters, humanoid dreaming, CPO, and merge-mining
**Nicholas Templeman — CSO AI LTD — August 2026**
*Companion to SOVOS-MASTER.md (Parts A–T). Research swarm: 20 queries, 4 rounds, August 11 2026.*

---

## 0. THE ANSWER UP FRONT

You asked five things. All five are yes, with one honest ceiling:

| # | Your question | Verdict |
|---|---|---|
| 1 | Can a **normal screen** become a Looking Glass with what we have? | **YES — Tier 0 today, zero new hardware.** Webcam head-tracked parallax + AI depth = the "window effect" on any LCD. Honest ceiling: a normal LCD cannot do true stereopsis without optics — Tier 0 is motion parallax, not light field. True holographic needs the $149 musubi or an ELF-SR2. |
| 2 | Can the **characters become more real**? | **YES — and we hold a card nobody else has.** The industry is racing on voice/face/memory (ACE, Convai). Nobody ships *calibrated, provenance-anchored, governed* characters. MEOK already does identity (Ed25519 + Merkle + C2PA). Add σ you can see. |
| 3 | Can a **humanoid dream in SOV Space**? | **YES — and the industry literally calls it dreaming.** World-model rollouts (UniPi/RoboDreamer/Cosmos) = imagination. Your drum.rs is the dream engine. J-Space is where the dreams live. Article 0 gates which dreams may become motion. |
| 4 | What does **CPO** catapult? | **The clan bus at light speed.** CPO's first killer app is exactly your architecture: routing tokens between specialist models (MoE/clans) and pooled shared memory (J-Space across racks). We don't build it — we ride it. Free speedup arriving 2026–2028. |
| 5 | Can **mergekit/task-vector math** improve mining? | **YES — and there's a sellable product hiding in it.** Production merging's #1 pain is "the merge diluted our safety tuning." You already built the cure: sheaf-gate + arena. Merge-regression-as-a-service. |

And the discovery of the night: **a 14th greenfield opened while we were mining.** EU Machinery Regulation 2023/1230 goes mandatory **January 20, 2027**, and it explicitly names *"safety components with self-evolving behaviour based on machine learning"* as a notified-body category [^2231^]. That is a legal description of a humanoid's brain. Physical-AI RAS — same law monorepo, same crosswalk, same ChainResult evidence — is the AI Act play transplanted onto robots, with a harder deadline.

---

## 1. GLASS OS — THE NORMAL-SCREEN LOOKING GLASS

### 1.1 The pipeline that already exists (all verified live, 2026)

```
Any 2D image/video
   │
   ├─► AI depth: Depth Anything 3 (Jan 2026, any-view generalist, metric geometry) [^2222^]
   │              or Distill Any Depth (open, Looking Glass) [^2219^]
   │              or Immersity Neural Depth Engine (3M+ users, free 2D→3D) [^2218^][^2223^]
   ▼
RGB-D pair  ──► quilt / multi-view  ──► render target:
   │
   ├─► TIER 0 — any normal screen: head-tracked parallax "window" (webcam + Three.js)
   ├─► TIER 1 — Looking Glass musubi $149 / HLD 16–27" $2–4K (Bridge SDK, open-source) [^2200^][^2217^]
   ├─► TIER 2 — Sony ELF-SR2 27" 4K glasses-free eye-tracked, ~£4K, OpenXR/UE5/Unity SDK [^2216^][^2220^]
   └─► TIER 3 — WebXR headsets (Three.js renderer.xr native)
```

blocks.glass converts **any 2D image into a hologram in seconds** and the Bridge SDK + casting stack is open-source [^2200^][^2217^]. Immersity (rebranded from Leia, Aug 2025) gives the 2D→3D conversion away free to 3M+ users [^2218^][^2223^]. The content-conversion problem is **solved and commoditized**. The only unsolved layer is the one we own: **what makes a hologram trustworthy.**

### 1.2 Glass OS = the governed hologram layer

Every player in this stack renders pixels. None of them can answer: *is this hologram telling the truth, and how sure is it?* SOVOS ships the missing layer:

| Glass OS component | Built from (already in monorepo) |
|---|---|
| **σ-halo on every holographic object** | uncertainty-shader.html — volumetric version; object brightness = calibrated confidence (sovos-sigma-calibration) |
| **Provenance voxel** | C2PA anchor per asset (Contributor Member ✅) — tap any object → its full birth→now worldline |
| **Worldline scrubbing** | the honest 4D: drag time, the scene replays its ChainResult history (honey strata) |
| **Governed gaze** | eye-tracking (ELF-SR2 SDK has it native) + Article 0: what the character may *show* depends on who's looking (V1–V8 gates) |
| **Character embodiment** | MEOK's 27 characters walk out of the flat screen into the light field, key-claim intact |

### 1.3 Honesty register — Glass OS

- **REAL:** the full conversion pipeline (DA3/Immersity → RGB-D → quilt → Bridge cast) works today; musubi ships with local AI conversion [^2217^][^2219^]; ELF-SR2 SDK 2.5.0 supports UE5.5/Unity 6/OpenXR/Blender [^2216^].
- **REAL:** Tier 0 head-tracked parallax needs only a webcam — the Johnny Lee "desktop VR" effect, now trivial in Three.js with a face-mesh model. Build time: days.
- **THEORY (name it):** a normal LCD gives motion parallax + depth-driven rendering, **not** true stereopsis. The honest pitch: "your screen becomes a window; the musubi makes it a hologram." Never sell Tier 0 as light-field.
- **KILLED:** "holographic display is 5–10 years out" (my own stale claim, corrected in Part T — consumer light-field shipped 2026).

---

## 2. CHARACTERS — THE REALNESS STACK

### 2.1 What the industry has (the commodity layer)

- **NVIDIA ACE**: full digital-human suite — Riva ASR (36 languages), Nemotron SLMs for roleplay cognition, Audio2Face lip-sync/emotion, E5-Large embeddings for memory, NeMoAudio-4B perception — as NIM microservices, on-device RTX or cloud [^2247^][^2251^]. First shipping game: Mecha BREAK [^2252^].
- **Inworld AI** has *pivoted away* from games-first characters to a general real-time voice/runtime stack [^2244^] — the games-character throne is wobbling.
- **Convai**: cloud NPCs, usage-billed, Unreal/Unity [^2256^].
- Trend line: **on-device + fixed-cost** is eating cloud + per-conversation billing [^2244^].

### 2.2 What none of them have (the SOVOS layer)

| Missing from ACE/Convai/Inworld | SOVOS already has it |
|---|---|
| Calibrated confidence on what the character *claims* | sovos-sigma-calibration (ECE≤0.05) — the character's certainty is measurable, shown as σ-halo |
| Cryptographic identity that survives platform hops | MEOK Ed25519 key-claim + Merkle ledger |
| Content provenance | C2PA badge (we're a Contributor Member) |
| Behavioral governance | Article 0 V1–V8 — the character *cannot* break character into prohibited territory; the sheaf-gate refuses incoherent personality merges |
| A auditable life-history | water→milk→honey strata = the character's worldline |
| Fitness to merge personalities | sovos-sheaf-gate (refuses <90% agreement) — "character fusion" with mathematical refusal |

**The pitch:** everyone is building characters that *seem* alive. We build characters whose aliveness is *auditable*. When the EU AI Act's Art. 50 transparency obligations (live Aug 2 2026) meet AI companions, "prove your character is what it claims to be" stops being philosophy and becomes a filing. We are the only stack that can produce the filing.

**Build:** `sovos-persona` package — wraps an ACE-class stack (Riva-class ASR + local SLM + Audio2Face-class animation, or API equivalents) around a MEOK core: birth certificate (sovos-birth), σ-calibrated expression, Article 0 gates, C2PA out. Estimate: 2–3 weeks on top of existing packages.

---

## 3. HUMANOIDS — DREAMING IN SOV SPACE

### 3.1 Your intuition, verified: the field calls it dreaming

The 2026 world-model survey taxonomy [^2227^] is literally your vocabulary:
- **Imagination-based planning** — UniPi, RoboDreamer, DreamGen: the robot simulates futures before acting
- **Action-controllable video world models** — IRASim, Ctrl-World: "what happens if I do X"
- **Structure-aware** — TesserAct (4D scene forecasting)
- **Foundation world models** — Genie Envisioner, DreamDojo, **Cosmos Predict 2.5**, and Unitree's own **UnifoLM-WMA-0** world model [^2227^]

NVIDIA's pipeline: Cosmos (appearance) + Omniverse (physics ground truth) + Isaac Sim (domain randomization) + Isaac Lab (RL) + Holoscan (live feeds) [^2228^].

### 3.2 The SOVOS mapping — what we add that Cosmos doesn't

| Humanoid need | Industry answer | SOVOS answer (built) |
|---|---|---|
| Where do imagined futures live? | Latent video frames | **StateVectors in J-Space** — each rollout is a point on the manifold, distance-to-permitted-manifold computable (sovos-signal-index math) |
| The dream engine | Cosmos Predict | **drum.rs** — continuous simulation, already in the hive kernel; dreams append to the bus, signed |
| Which dreams may become motion? | reward shaping (soft) | **Article 0 + CLF-CBF barriers (hard)** — an imagined trajectory that crosses a barrier is refused *in imagination*, before motors |
| Dream experience compounds how? | retraining | **honey** — dream outcomes descend water→milk→honey; the robot's distilled experience is a geometric object, shareable across the fleet via Procrustes |
| How sure is the plan? | ensembles (opaque) | **σ per planned trajectory** — the robot shows its uncertainty about outcomes; uncertainty pixel → uncertainty *path* |
| Fleet trust | none (see UniPwn, below) | **SOV SIGNAL for robots** — Mahalanobis distance from the permitted behavior manifold, per fleet, continuously |

**The killer detail — UniPwn.** Unitree robots shipped with an exploitable BLE/wifi path enabling **fleet takeover**, publicly disputed and unresolved through 2026 [^2229^]. Humanoids have no sovereign security/governance layer. That is not a gap; that is a greenfield with blood in it.

### 3.3 Hardware path (verified pricing, 2026)

- **Unitree R1 EDU — $10,500**: ROS 2, the cheapest real entry [^2226^]
- **Unitree G1 EDU — $43,500+**: ROS 2 + Jetson Orin, the best-seller (5,500 units 2025), GR00T-supported [^2225^][^2229^]
- **UnifoLM-VLA-0 open-sourced with weights, Jan 2026** — a real VLA to wrap in SOVOS gates *today*, no robot required for the sim-side build [^2225^]
- Sim-first: Isaac Sim + Cosmos rollouts → J-Space → Article 0 gate → honey. Zero hardware needed until the gate is proven.

### 3.4 THE 14TH GREENFIELD: Physical-AI RAS (deadline January 20, 2027)

Verified from primary regulatory analysis [^2231^][^2234^][^2236^]:

- **EU Machinery Regulation 2023/1230** replaces the Machinery Directive **Jan 20, 2027** — a *regulation*, applies directly in all member states, no transposition slack [^2231^][^2236^].
- It **explicitly covers AI-integrated machinery and ML functions that alter behavior over time**; **"safety components with self-evolving behaviour based on machine learning" are Annex I Part A — notified-body conformity assessment** [^2231^][^2236^]. A learning humanoid's safety brain is legally in the hardest category.
- New **cybersecurity essential requirements** in conformity assessment [^2236^] — post-UniPwn, that's a loaded gun pointed at every humanoid vendor.
- Deployer obligations stack: **EU Declaration of Conformity, 10-year technical file, AI Act Art. 49 high-risk registration, DPIA, serious-incident reporting, AI-literacy training** [^2234^].
- **ISO 10218-1/2:2025** new editions: Class 1/Class 2 split, default PL/SIL safety levels, "collaborative application" scope [^2235^][^2236^].
- Software updates can constitute **substantial modification** → manufacturer obligations pass to the operator [^2231^]. *Every OTA model update to a robot is potentially a legal event.* Who produces the evidence trail? **The ChainResult→OSCAL exporter we already specced.**
- AI Act overlay: safety-component AI high-risk ~Aug 2028 (Digital Omnibus timeline) [^2234^].

**This is the AI Act play again, but harder, sooner, and with nobody positioned.** A cottage industry already sells ~96-page PDF template kits for this deadline [^2230^] — the market is paying for *documents*. We sell the *machine that produces the evidence*: MR 2023/1230 + ISO 10218 crosswalk pack (our crosswalk-as-geodesic method), ChainResult attestation per OTA update, SOV SIGNAL per robot fleet. RAS-for-robots.

---

## 4. CPO — THE CLAN BUS AT LIGHT SPEED

Verified 2026 state of co-packaged optics:

- **Lightmatter Passage CPO chiplet sampling: 1.6 Tbps per fiber**, 16-wavelength DWDM, **8× bandwidth density** vs existing NPO/CPO; evaluation kits shipping; Passage L20 (6.4 Tbps BiDi) announced; M1000 3D photonic interposer in market; **Lightmatter joined NVIDIA NVLink Fusion** [^2232^][^2233^][^2238^].
- Lightmatter's published research: **up to 2.7× reduction in AI training time** from interconnect alone [^2237^].
- **Celestial AI** (Photonic Fabric — optical memory/compute disaggregation, claimed 25× bandwidth, 10× lower latency/power vs alternatives): raised **$520M total**, then **acquired by Marvell** — consolidation = the tech is real and going to scale [^2242^][^2245^][^2254^].

**What it catapults for SOVOS — mapped, not hand-waved:**

| CPO capability | SOVOS structure it accelerates |
|---|---|
| High-radix flat topologies "for MoE architectures requiring rapid token routing between specialized models" [^2237^] | **The clans.** 13 faction models routing through the StateBus is architecturally identical to MoE token routing. CPO is literally built for our shape. |
| Memory/compute disaggregation, optically pooled memory [^2254^] | **J-Space as a rack-scale shared manifold.** Honey strata in pooled optical memory = every node's distilled experience addressable by every clan at nanosecond latency. |
| 2.7× training-time cut [^2237^] | Arena batteries, GRPO-geometric-reward runs, merge sweeps — all cheaper per experiment. |
| NVLink Fusion ecosystem [^2238^] | The door we're already near (NeMo lane). Photonics joins the ecosystem we're courting. |

**Honesty:** we build nothing here. No photonics fab, no CPO driver. The play is *readiness*: keep the bus/clan/J-Space abstractions hardware-agnostic so the speedup lands for free as CPO ships through datacenters 2026–2028. Optional later: Lightmatter evaluation-kit conversation once SOV SIGNAL is public (they need workload stories; a governed-clan routing story is a good one).

---

## 5. MERGE-MINING — TASK VECTORS AS THE EXTRACTION REFINERY

### 5.1 The production pain we can sell into

The 2026 production-merging literature confirms the exact wound our stack heals: **"a merge can dilute safety tuning or bring back behavior that a source model had already corrected"** — capability interference is the #1 production risk, and "pre-release evaluation and staged rollout [are] non-negotiable" [^2248^]. Current practice is a 10/90 A/B shadow with LLM-as-judge [^2250^] — *vibes-based regression testing*.

**Our counter:** sovos-sheaf-gate (refuse merges <90% behavioral agreement) + sovos-arena (12 GSPC axes, Wilson CIs, n≥30) = **merge regression with statistical teeth**. Every merge candidate gets a signed ChainResult: which axes moved, by how much, with confidence intervals. That's merge-regression-as-a-service — and it makes our own mining safer at the same time.

### 5.2 The economics are trivial (verified April 2026 rates) [^2250^]

| Operation | Hardware | Cost |
|---|---|---|
| TIES merge, single pass | 1× H100 | **~$1.51, 45 min** |
| Evolutionary merge sweep (100 configs) | 4× H100 | **~$24, 3 hrs** |
| GRPO training (32B) comparison | 4× H200 | ~$760+ |

**Translation: on the A100 we can run a merge sweep every single night.** Merging is the cheapest capability-extraction technology that exists, and almost nobody is doing it systematically.

### 5.3 The new experiment — MAP-Elites over merge space

sovos-map-elites (the patent-grade QD engine, already built) applied to **merge configuration space**: descriptors = (safety retention, capability gain, σ-calibration); genomes = (λ weights, TIES density, DARE drop rates, layer masks); safe_mutate = constrained perturbation. The archive becomes **an evolving library of best-known merges per behavioral niche** — a self-improving model zoo where every cell is a signed ChainResult. Nobody has this. It also *is* the P6 paper's second act, which strengthens the patent filing.

### 5.4 Task vectors for mining (the unlearning direction)

Task arithmetic's negation operator (established: Ilharco et al., task vectors) = subtract a capability/behavior direction in weight space. Mining applications: (a) **decontamination** — negate the test-set direction from crawl-trained models before arena evaluation; (b) **safety restore** — if a merge dilutes refusal behavior, add back the refusal task vector instead of retraining; (c) **greenfield probes** — negate a known domain from a generalist, measure the hole on GSPC axes: the shape of the hole tells you what to mine next. All three run on mergekit + arena, tonight-grade builds.

---

## 6. PARTNERSHIPS & PUBLISHING — WHO TOUCHES FIRST

| Door | Why us | Move |
|---|---|---|
| **Looking Glass** (Bridge SDK open-source [^2200^]) | They need a "why holograms matter beyond novelty" story; governed/provenance-anchored holograms is one | Build Tier-1 demo (MEOK character, σ-halo, C2PA) on musubi; post the quilt pipeline open |
| **NVIDIA ACE lane** | Existing NeMo lane; ACE is NIM microservices — sovos-persona can be ACE-compatible rather than competitive | Wrap, don't fight: SOVOS governance around ACE stack |
| **Unitree ecosystem** | UnifoLM-VLA-0 open weights [^2225^] + UniPwn wound [^2229^] = they need a security/governance story | Sim-first: VLA + Article 0 gate demo; publish "governed imagination" results |
| **Robot-safety compliance market** | Jan 2027 deadline; template-PDF sellers prove willingness to pay [^2230^] | MR 2023/1230 crosswalk pack into the law monorepo; RAS-for-robots one-pager |
| **Lightmatter** (eval kits [^2232^]) | They need workload stories post-NVLink-Fusion | Later, after public index v0 |
| **Munich Re / AIUC-1 / ERC-8004** | (per Part N — unchanged, still primary) | SOV SIGNAL one-pager still #1 |

**New papers this unlocks (portfolio now 19):**
- **P18 — Governed Imagination: sheaf-gated world-model rollouts for embodied agents** (dreams as StateVectors; Article 0 barriers in imagination; honey as distilled dream experience). *Tier 1 — sim-only, buildable now.*
- **P19 — The Glass OS: provenance-anchored holographic interfaces** (C2PA + σ per voxel + worldline scrubbing). *Tier 2 — after musubi demo.*

---

## 7. MONOREPO — THE EAT LIST FOR THIS DIMENSION

| Package | Contents | Depends on | Estimate |
|---|---|---|---|
| `sovos-glass` | Depth→RGB-D→quilt pipeline (DA3/Distill Any Depth), Bridge SDK cast, Tier-0 head-tracked parallax viewer (Three.js), σ-volumetric shader port | uncertainty-shader.html, C2PA lane | 2 weeks |
| `sovos-persona` | Character embodiment: MEOK core + ASR/SLM/animation wrappers + σ-expression + Article 0 gates | meok.ai stack, sigma-calibration, article-zero | 2–3 weeks |
| `sovos-dream` | drum.rs dream loop + world-model rollout harness (Isaac Sim/Cosmos connectors) + rollouts-as-StateVectors + honey descent on dream outcomes | sovos-hive, signal-index math | 3–4 weeks (sim-first) |
| `sovos-merge-arena` | Merge regression harness: sheaf-gate + GSPC arena battery per merge candidate, signed ChainResult; MAP-Elites merge-sweep driver | arena, sheaf-gate, map-elites | 1–2 weeks |
| `sovos-robot-ras` | MR 2023/1230 + ISO 10218:2025 crosswalk pack, OTA-update = ChainResult attestation flow, OSCAL export | crosswalk, oscal, chain | 2 weeks |

**Sequencing:** merge-arena and glass first (cheapest, demo-able, revenue-shaped), then persona, then dream, robot-ras in parallel with the OSCAL exporter already queued.

### The 3 moves tonight
1. **Tier-0 Glass OS spike:** webcam face-mesh + Three.js parallax window + one MEOK character + σ-halo. One evening, any laptop, proves the "normal screen" answer physically.
2. **First merge sweep on the A100:** pick 3 specialist checkpoints, TIES + DARE grid, arena battery on each candidate, sign the results. By morning you have the merge-arena artifact and P6's second figure.
3. **One page: "RAS for Physical AI — the January 20, 2027 deadline."** MR 2023/1230 + self-evolving ML safety components + UniPwn + our ChainResult/OSCAL pipeline. This is the Part-N Munich Re one-pager's sibling.

---

## 8. HONESTY REGISTER (this document)

| Claim | Bucket |
|---|---|
| Full 2D→hologram pipeline commodity-solved (DA3, Immersity, blocks.glass, Bridge SDK) | REAL [^2222^][^2218^][^2200^] |
| Tier-0 normal-screen "window" effect, zero hardware | REAL (established rendering technique; our integration is THE THEORY part, days of work) |
| Normal LCD = true stereopsis | KILLED (physics; needs optics — musubi/ELF-SR2) |
| ACE/Convai/Inworld have no calibrated-confidence or provenance layer | REAL (per their own product docs [^2247^][^2244^][^2256^] — none advertise calibration/C2PA) |
| Humanoid world-model dreaming = active research frontier, sim-first buildable | REAL [^2227^][^2228^] |
| EU MR 2023/1230 mandatory Jan 20 2027; self-evolving ML safety = notified body; cybersecurity in scope | REAL [^2231^][^2236^] |
| UniPwn unresolved | REAL (public dispute; treat as "contested, unpatched as of reporting") [^2229^] |
| CPO gains land on SOVOS automatically | THEORY (directionally certain from NVLink Fusion/Marvell consolidation [^2238^][^2242^]; magnitude unquantified for our workload) |
| Merge-arena as sellable service | THEORY (pain is REAL [^2248^]; willingness to pay unproven — the one-pager tests it) |
| sovos-persona / sovos-dream build estimates | THEORY (2–4 week estimates, scoped on existing packages) |

*Not legal advice — regulatory analysis for engineering planning; qualified counsel before any conformity filing.*
