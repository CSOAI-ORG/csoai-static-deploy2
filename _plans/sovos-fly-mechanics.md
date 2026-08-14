# SOVOS — THE FLY MECHANICS
### Eon uploaded a fruit fly. The mechanics are SOVOS-shaped — and the three things they didn't ship are ours
**Nicholas Templeman — CSO AI LTD — August 2026**
*Companion to SOVOS-MASTER.md (Parts A–Z). The question: "the mechanics from the fruit fly uploaded to PC — Eon — for SOVOS?" Answer: the loop they built is our loop, the data is public, the bodies are open-source, and their fly has no past, no governor, and no identity. Those three absences are the product.*

---

## 0. WHAT EON ACTUALLY DID (verified, March 2026)

March 7–8, 2026: Eon Systems (SF startup) announced **"the first multi-behavior brain upload"** — the FlyWire connectome of an adult fruit fly, a simple neuron model, and a MuJoCo physics-simulated body, closed into a loop [^2307^]. It went properly viral: **120M+ impressions**, trending worldwide, Musk reacting ("There's a fruit fly walking around right now that was never born") [^2307^]. The Register's verdict: "huge if true — but the research papers behind it look solid" [^2309^].

**The mechanics (their own engineering write-up [^2310^]) — a four-part loop:**
1. **Sensory events** in the virtual world are mapped onto *identified sensory neurons/pathways*
2. **Brain activity** updates in a *connectome-constrained neural model* (~125K neurons, ~50M synapses, from the 2024 Nature model by Shiu et al. — neurotransmitter identities ML-predicted, motor behavior validated at ~95% [^2308^])
3. **Descending outputs** are translated into low-dimensional motor commands
4. **Movement changes the sensory state** → fed back into the brain. Brain↔body sync every 15ms [^2310^]

The body is **NeuroMechFly v2** (EPFL Ramdya lab — open, with FlyGym) and the vision model is **FlyVision** (TuragaLab — open on GitHub) [^2311^][^2315^].

**Their own honest limits [^2308^]:** neurotransmitters predicted, not confirmed; synaptic weights approximated; simplified dynamics; and the big one — **no plasticity, no long-term memory formation.** The fly walks and grooms. It never learns. It has no yesterday.

---

## 1. WHY THE MECHANICS ARE SOVOS-SHAPED

| Eon's component | SOVOS cognate | Status |
|---|---|---|
| Connectome = measured adjacency graph (139,255 neurons, 50M+ synapses, public download [^2313^][^2312^]) | A **measured** mind — the measurement-first thesis has a biological existence proof. A connectome is a graph; graphs embed natively in Poincaré space → **the fly fits in J-Space** | math ready (sovos-jspace-hyperbolic) |
| Four-part sensorimotor loop, 15ms sync | **drum.rs** — the continuous simulation engine, already the designated dream engine (Part U) | architecture match |
| Sensory events → identified neurons | birth-coordinate-style anchoring: fixed input ports into a state space | pattern match |
| Descending outputs → motor commands | move arithmetic (Axis/Move/ErrorVector in sovos-world) | pattern match |
| MuJoCo body | already in the robotics EAT stack (unitree_mujoco, Isaac backends) | absorbed |

**And the narrative resonance is exact:** the fly is literally an *organic open world model* — a world model derived from a real organism, built from open public data. Part Y's OOWM ruling gets a biological anchor.

---

## 2. THE THREE THINGS EON DIDN'T SHIP — ALL THREE ARE OURS

**① Plasticity / memory → HONEY.** Their fly has no learning and no past [^2308^]. SOVOS's water→milk→honey descent *is* a plasticity layer: experience accumulates, distills, persists as geometric strata. **"Eon uploaded the fly's brain; SOVOS gives it a past"** — an emulated organism that learns from experience is a genuine research differentiator, not marketing.

**② Governance → ARTICLE 0.** An emulated mind with no behavioral gates. As emulations scale (mouse cortex data already public — MICrONS: 200K cells, 523M synapses, open buckets [^2316^][^2314^]), "what may this emulation do, and who authorized it" becomes a real question. **Governance of emulated minds: zero competition, today.** SOVOS gates, σ on neural states, human-signed CURVATURE gates on experiments.

**③ Identity / provenance → SIGIL + C2PA.** Which connectome snapshot? Which edits? MICrONS already versions its connectome (CAVE versioning [^2314^]) — the data is provenance-aware but *unsigned*. A SIGIL-signed emulation state + C2PA-anchored run = the first emulated organism with a birth certificate. (sovos-birth, literally.)

---

## 3. THE EAT LIST — ALL OPEN

| Asset | What | License/access |
|---|---|---|
| **FlyWire connectome** | complete adult fly brain, 139K neurons | public download (codex.flywire.ai) [^2313^] |
| **flywire-network-analysis** | Princeton analysis scripts (spectral, motifs, rich-club) | Zenodo, open [^2313^] |
| **NeuroMechFly v2 / FlyGym** | biomechanical body + RL controllers | EPFL, open [^2311^][^2315^] |
| **FlyVision** | connectome-constrained visual system | TuragaLab GitHub, open [^2315^] |
| **MICrONS mouse cortex** | 1mm³, 523M synapses + functional recordings | public AWS/GCS buckets, cloud-volume/CAVE APIs [^2316^][^2314^] |
| **H01 human cortical sample** | 1mm³ human temporal lobe, 57K cells | public [^2312^] |
| **OpenWorm** | C. elegans whole-organism sim | open, active [^2318^] |

All of it flows through the Part X harvest pipeline (license gate → absorb → arena → sign).

---

## 4. THE BUILD — `sovos-emulate`

```
FlyWire download → connectome graph
   │  Poincaré embed → the fly in J-Space          (sovos-jspace-hyperbolic)
   ▼
drum.rs dynamics harness (connectome-constrained LIF update, 15ms body sync)
   │  body: NeuroMechFly v2 / MuJoCo               (open)
   ▼
SOVOS layer: σ on neural state · Article 0 behavioral gates · SIGIL-signed states
   │  experience → water→milk→honey strata          (THE PLASTICITY EON LACKS)
   ▼
birth certificate per emulation (sovos-birth) → C2PA-anchored runs
```

**The killer experiment (uniquely ours):** Eon runs *one* fly. The A100 runs **thousands in parallel** — a population of emulated flies, each accumulating honey strata, driven by **MAP-Elites** (Part U/P6 engine) over behavioral niches. *Evolution and experience over emulated minds, with every run signed.* That is a paper nobody else can write this year — **P21: "Governed Experience in Whole-Brain Emulations."**

**Timeline honesty:** mouse-scale emulation is years out (functionalization + validation bottlenecks, serial pipeline [^2317^]); human WBE further. The governance question arrives *before* the capability — which is exactly when standards get set. We arrive now.

---

## 5. THE 3 MOVES TONIGHT

1. **Download the FlyWire connectome** (codex.flywire.ai [^2313^]) and run one J-Space embedding of the graph — "the fly in J-Space" figure for P21
2. **Spec `sovos-emulate`** as a harvest-pipeline absorb: FlyWire + NeuroMechFly + FlyVision, license-gated, adapter-not-fork
3. **One-pager: "The Fly Has No Past"** — Eon shipped brain+body; SOVOS ships memory, gates, and identity for emulated minds. The 120M-impression wave [^2307^] is still warm — ride it

---

## 6. HONESTY REGISTER

| Claim | Bucket |
|---|---|
| Eon's upload: FlyWire + neuron model + MuJoCo body, closed loop, multi-behavior | REAL (their announcement + independent coverage; "we believe" flag on "first") [^2307^][^2309^][^2310^] |
| 125K neurons/50M synapses, ~95% motor prediction | REAL (Nature 2024 lineage) [^2308^] |
| No plasticity, no long-term memory | REAL (their stated limit) [^2308^] |
| All data/tools public (FlyWire, NMF2, FlyVision, MICrONS, H01, OpenWorm) | REAL [^2313^][^2315^][^2316^][^2312^][^2318^] |
| Connectome → J-Space embedding | THEORY — mathematically natural (graphs embed in Poincaré space), unbuilt |
| Honey as plasticity for emulations | THEORY — the framing is sound, the experiment doesn't exist yet |
| Parallel-fly MAP-Elites on the A100 | THEORY — compute-plausible (125K neurons is tiny), unscaffolded |
| Mouse/human emulation timeline | YEARS (serial bottlenecks) [^2317^] — never pitch it as near |
