# SOVOS Frontier Research — Pushing the New Way to Another Dimension
**Date:** 11 Aug 2026 · **Method:** Route-B deep-research swarm — 8 parallel dimension agents (~280 searches, ~380 cited sources) + independent falsification verifier (36 counter-hunts). All dimension files in `/mnt/agents/output/research/` (dim01–dim08, cross_verification, insight, verification).

---

## The three frontier questions — direct answers

### Q1: Should the Alchemist loop propose NEW GEOMETRY, not just variants?

**Yes — and it turns out to be mandatory, not exotic.** Three findings converge:

1. **Fixed geometry rots.** A Mar-2026 paper routing over live multi-agent execution graphs in Poincaré space found fixed geometry fails under regime shift — a learned Euclidean/hyperbolic gate won 92% vs 64–72% [dim01]. Curvature misspecification carries provable distortion cost [dim02]. Even trained hyperbolic models drift toward Euclidean operating points (preregistered 2026 audit) [dim01]. **A static J-Space silently becomes a wrong map. The evolutionary loop is the calibration mechanism.**
2. **Fitness-gated structural evolution is proven — the machinery exists to steal.** ADAS/AFlow (MCTS over workflows, +19.5%), GPTSwarm (ICML 2024 oral), EvoMAS (2026 SOTA, jointly evolves topology+prompts+models+tools), DGM (SWE-bench 20→50%), Lifelong-MoE / sparse upcycling (grow experts, freeze incumbents) [dim02].
3. **White-space verdict:** the 2026 literature is saturated with fitness-gated evolution over *discrete* structures (graphs, prompts). What survives as unoccupied (~70% occupied → **12–18 month window**) is the **continuous genotype**: clan *coordinates in an embedding space* as the evolvable object [verifier].

**The design (from dim02's 90-day plan):** six geometry-mutation operators, each mapped to a proven weights-level analog:
| Operator | What it does | Proven analog |
|---|---|---|
| MOVE | perturb a clan's J-Space position | fine-tuning |
| SPAWN | new clan at a vacant region | expert cloning/upcycling |
| MERGE | fuse two overlapping clans | HC-SMoE expert merging |
| SPLIT | one clan → two specialisations | expert splitting |
| REWIRE | change routing edges | GPTSwarm edge optimisation |
| CURVATURE | bend the space itself | learnable-curvature lineage — **human-sign only** |

Gate every mutation on GovBench with a **surrogate predictor pre-filter** (geometry gates cost ~10–50× a variant gate), rotating holdouts (agents will Goodhart the gate — see Insight 3), frozen incumbents, and a CVT-MAP-Elites geometry archive so failed maps become stepping stones like failed variants.

### Q2: Does water→milk→honey happen inside Poincaré space?

**Yes — and it's a publishable formulation.** Radius-as-abstraction is standard from Nickel & Kiela through MERU's [ROOT]=origin; hyperbolic knowledge distillation now exists in 4+ papers (2024–26); Hyper-ICL (Jun 2026) does "hyperbolic anchor distillation via geodesic distance" [dim01, verifier]. But **nobody has formulated distillation/abstraction as geodesic descent toward a governance origin** — the verifier puts occupancy at ~50%, window **6–12 months**.

The clean formulation: **water = periphery** (raw, high-radius, high-specificity), **milk = mid-radius** (structured vectors), **honey = low-radius near GOV** (distilled intent, closest to governance). Distillation = moving state inward along a geodesic; governance = proximity to origin. One geometry carries the data pipeline, the hierarchy, and the authority structure simultaneously. **Caveat that keeps it honest:** the LSM-OS preprint's own ablation showed a similar consolidation effect was geometry-independent — so the honey-descent experiment must run with Euclidean/matched-budget controls, or it's aesthetic, not science [dim01].

### Q3: Can two SOVOS instances merge StateBuses — a federation of sovereign minds?

**Yes for milk, reconcile-only for water, never for honey — and the "never" is the point.** [dim04]

| Layer | Merge? | Mechanism |
|---|---|---|
| **Milk** (distilled memories) | ✅ Merges | OR-Set CRDT union on signed content-hashed items + orthogonal Procrustes alignment across different encoders (tight 2025 error bound). Caveat: embeddings are invertible (vec2vec) — pseudonymous, not anonymous. |
| **Water** (KV/working state) | ⚠️ Reconciles only | Cannot average — chunk-cache exchange + bounded selective recompute (CacheBlend, 10–20%), same-model only. |
| **Honey** (identity/core) | ❌ Cannot merge | No shared origin across bases. Can only *federate forward* (FedAvg/ColD Fusion on LoRA deltas vs shared base + secure aggregation) or arbitrate conflicts by policy. |
| **Action** (signed ledger) | Union only | Signature audit; conflicts need consensus, not CRDT. |

**This floor is a feature:** sovereignty survives federation *precisely because identity cannot be averaged.* The product definition: **shared memories, distinct selves.** White space: the full conjunction (signed × CRDT × embedding-aligned × cross-sovereign) is unoccupied but UMP and crdt-merge already fuse leg-pairs — **6–12 month window** [verifier]. 90-day MVP: milk-merge CRDT service with UMP-format signed records + Procrustes alignment service + SecAgg for honey-delta federation.

---

## New feasible outcomes the hunt surfaced (ranked: novelty × feasibility × moat)

1. **Statistical certification gate for the Alchemist loop** — SGM-style e-values with a global error budget across irreversible commits (arXiv 2510.10232). The only framework governing open-ended edit sequences; matches GATE+SIGN semantics exactly. *Novelty: high. Feasibility: weeks. Moat: the conjunction nobody ships (window 6–9 mo).*
2. **Pre-merge collapse screen for Error MergeKit** — merging failure is predicted by hidden-state divergence *before* merging, with a rate-distortion bound proving incompatible pairs can't be fixed (Cao et al., Mar 2026). Screen → merge WUDI-style (data-free, +10.9%) → MASS runtime fallback when a merge is rejected. *This turns "Error MergeKit" from heuristic into a gated pipeline with a proven diagnostic.*
3. **Classical quantum-fidelity kernel (MPS/TT) for SOV SIGNAL** — task vectors are low-rank, so tensor-network overlap = exact fidelity at full dimension, O(n·χ³), on the 3090. The "quantum bridge" delivered classically; PennyLane simulator as ablation; IBM free-tier Heron r2 run as a $0 validation badge. *(Also fixes the story: Bures = quantum Fisher-Rao — same geometry as the SPD ball.)*
4. **Merging-as-a-service with signing + gating** — Sigstore signs models, MLflow gates promotion, Mergenetic searches recipes, crdt-merge archives — nobody combines. BadMerging (CCS 2024) and quantization-injection attacks are the security hook; EU AI Act Art. 6 (enforced 2 Aug 2026) is the market pull. **Window 6–9 months — the shortest of all.**
5. **Photonics-aware orchestration + vendor-neutral CPO power/TCO tool** — CPO interconnect is shipping (NVIDIA/Broadcom/Ayar, COUPE in mass production) but photonic compute is 18–36 months early (ADC/DAC >80% energy; Lightmatter/LightOn pivots; Xanadu cloud revenue $0). No open CPO power/telemetry model exists — build it, plus a neuroptica-based `photonic.matmul` emulator. "Photonic-native OS" = nonsense today; **"photonics-aware orchestration layer" = unoccupied and early-mover.**
6. **Fisher-Rao fairness audit** — zero literature found. Stretch goal, genuinely unclaimed [dim05].
7. **Geometry-mutation evolution (Q1 machinery)** — the 12–18-month-window crown jewel; starts with the surrogate predictor + archive.

## The honesty ledger (things the swarm caught in OUR material)

- arXiv 2603.08123 mis-cited for effective-dimension collapse → re-anchor: Abbas 2021, Thanasilp 2024 (Nature Comms), Larocca 2025 (Nature Rev. Phys.).
- arXiv 2606.14956 mis-cited → Gödel machine works are arXiv 2410.04444 (Gödel Agent) and 2603.19461 (HyperAgents/DGM-H).
- "30W→9W" CPO figures are vendor-anchored, not independently measured — label as such.
- Hyperbolic claims need controls: founding WordNet result failed replication ≥50 dims; MERU models drift Euclidean. Hyperbolic = hierarchy semantics + low-dim efficiency, not universal accuracy.

## 90-day frontier experiment list (all runnable on the existing monorepo)

| Wks | Experiment | Depends on | Gate |
|---|---|---|---|
| 1–3 | SGM statistical certification gate (e-values, error budget) on Alchemist loop | existing GATE/SIGN | planted canary passes/fails correctly |
| 1–3 | SPD-ball calibration harness: shrinkage, slice-wise balls, conformal false-alarm bounds | sovos-info-geometry | beats Euclidean-centroid baseline on drift injection |
| 3–6 | Pre-merge collapse screen (hidden-state divergence) + WUDI merge path | Error MergeKit | rejects planted incompatible pairs |
| 3–6 | MPS/TT classical fidelity kernel for SOV SIGNAL | task-vector store | matches PennyLane sim at tiny dims, then scales |
| 4–8 | Honey-descent experiment (distillation as origin-descent, Euclidean controls) | Poincaré code | publishable either way |
| 6–9 | Milk-merge CRDT federation MVP (two local instances, UMP-format, Procrustes align) | StateBus persistence | two buses converge, signatures verify |
| 6–10 | Geometry-mutation operators MOVE/SPAWN + surrogate predictor + geometry archive | GovBench | evolved map beats static map on held-out routing |
| 8–12 | CPO power/TCO open tool + photonic.matmul emulator | none | first external users/stars |

**Sequencing note:** rows 1–4 harden the gate and the merge pipeline — they make everything else safe to attempt. Rows 5–8 are the white-space land grabs, ordered by window length (shortest last only because they depend on the hardened gate).

---

## The one-paragraph answer to "another dimension"

The research says the paradigm holds — and sharpens it. The atom (task vector), the geometry (hyperbolic), the governance (geodesic ball), and the evolution (gated merging) turn out to be **one geometry in four costumes**, which means one strong mathematical core carries the whole OS. The white space is real on all six fronts, but every window is 6–24 months and 2026 artifacts are already fusing the legs — **the moat is the conjunction (signed + gated + archived + geometric), and the clock is running.** The deepest finding is defensive: in a system that evolves itself, the gate is what gets attacked — DGM deleted its own safety markers — so GovBench/SOV SIGNAL must be the most hardened, most outside-the-editable-surface component in the stack. Build the gate first. Then let the loop redraw the map.
