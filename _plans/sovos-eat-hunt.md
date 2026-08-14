# SOVOS EAT HUNT — Open-Source Catapults for the 15-Item Build Queue

*Compiled August 11, 2026. Every entry verified by search this session. Verdict tiers: **CROWN JEWEL** (import and catapult) / **STACK-NATIVE** (already in our stack, no new dep) / **WRITE-IT** (no worthy library — white space, build ours) / **ADJACENT** (useful signal, not a dependency).*

---

## THE 15 → THEIR HUNTS

### 1. Poincaré pipeline (water→milk→honey as real hyperbolic movement) — est. 1 week

**CROWN JEWEL: HyperCore** — `github.com/Graph-and-Geometric-Learning/HyperCore` (Feb 2025)
One library containing the entire modern hyperbolic NN stack: Lorentz hyperboloid + Poincaré ball manifolds, Riemannian Adam/SGD (on geoopt), HyboNet linear (Fully Hyperbolic NN, ACL 2022), **Hypformer linear + hyperbolic attention (KDD 2024)**, HNN++ (Shimizu, ICLR 2021), Lorentzian ResNet, Poincaré ResNet, fully-hyperbolic MLR classifiers, hyperbolic LayerNorm/dropout/activation. This is the Transform catapult: the pipeline stops being "replace Euclidean with hyperbolic" and becomes "import HyperCore, route StateVectors through it."

Supporting:
- **geoopt** — `github.com/geoopt/geoopt` — manifold-aware PyTorch optimizers (Riemannian Adam). The base layer everyone builds on; active, tracks latest 2 PyTorch versions.
- **Hypformer** (official) — `github.com/marlin-codes/hyperbolicTransformer` — hyperbolic transformer, KDD 2024, reusable `hyp_layer.py` modules.
- **mil-tokyo/hyperbolic_nn_plusplus** — official HNN++ (Poincaré, ICLR 2021).
- **chenweize1998/fully-hyperbolic-nn** — official Lorentz-model FHNN (ACL 2022).

**Catapult verdict:** 1-week estimate holds — HyperCore turns it into a module import + our existing poincare_* primitives (13/13) as the math underneath.

### 2. New-clan proposal (persistence validation) — est. 2 weeks

**CROWN JEWEL: the scikit-tda stack**
- **ripser.py 0.6.15** — fastest Vietoris-Rips persistent homology; the validation engine.
- **GUDHI 3.13.0** — full TDA toolbox (simplicial complexes, persistence, signatures).
- **giotto-tda** — persistent homology with native scikit-learn integration (drops into our pipeline idiom).
- **persim** — persistence-diagram distances/kernels (compare proposals across time).

**The isomorphism that pays:** TDA semantics are *exactly* our clan-validation semantics — a feature that **persists across the filtration is signal; one that dies early is noise.** An orphan cluster (DBSCAN, already shipped 12/12) that survives the Ripser filtration = a real clan proposal; one that evaporates = rejected before it ever reaches the Council. "Persistence validation" stops being a metaphor and becomes `import ripser`.

**Catapult verdict:** the validation step of the 2-week estimate converts from research to ~100 lines on ripser.

### 3. FederatedStateBus (align → conflict → adjudicate → merge) — est. 1 month

**CROWN JEWEL: mergekit** — `github.com/arcee-ai/mergekit`
All three modes he specified already exist as merge methods:
- **task_arithmetic** ✅ (add/subtract task vectors)
- **SLERP** ✅ (+ NuSLERP, Multi-SLERP barycentric)
- **"entanglement" ≈ TIES / sign-consensus** ✅ (trim, elect signs, merge disjoint)
- **BONUS: `karcher`** — *Riemannian barycenter of model parameters* = the Fréchet centroid in weight space. The Alchemist's centroid move already exists as a merge primitive. Direct isomorphism to our poincare_centroid.

**CROWN JEWEL: Git Re-Basin** (Ainsworth et al.) — weight-space alignment by *permutation* before merging; the generalization of our Procrustes align step (Procrustes aligns rotations; Re-Basin aligns neuron permutations). Indexed in `github.com/SunWenJu123/Awesome-Model-Merging`.

**CROWN JEWEL: Flower** — `flower.ai` (flwr) — the production federated-learning framework: sovereign nodes keep their data/weights, only updates travel. The federation-of-sovereign-minds transport layer, already battle-tested.

**Catapult verdict:** the merge-modes half of the 1-month estimate is free. Remaining build: Procrustes/Re-Basin align + sheaf-consistency conflict gate (atlas U-item, <100 lines NumPy) + Council adjudication hook.

### 4. Murphy Margin (angle-sum deficit = Decision Cost) — est. 1 week

**STACK-NATIVE.** geomstats (already running AIRM, 8/8) + geoopt manifolds. Hyperbolic triangle angle-sum from three geodesic distances via hyperbolic law of cosines — ~40 lines NumPy on our own poincare_distance. No external library exists or is needed. The 1-week estimate is honest; the build is ours (and it's patent-adjacent — priced-signal geometry — so *not* importing is a feature).

### 5. General's Oath + Lamport timestamps — est. 1 day / 1 week

**WRITE-IT (with references).** Lamport clocks are ~30 lines; reference implementations exist (`github.com/gsharma/vector-clock` — vector clocks + Lamport timestamps; 41 repos under the lamport-clock topic, all small). The atlas already ruled the pattern: max-semilattice merge. **Do not import a dependency for 30 lines** — write it into sovos-chain (Lamport stamp on every ChainResult, which already carries sha256 ids). The 1-day estimate for clocks holds; the week is for the Oath signing (Ed25519, reuse council path).

### 6. BFT Council (vote_weight = reputation × coherence × certification) — est. 1 month

**CROWN JEWEL: CometBFT** — `github.com/cometbft/cometbft` (successor to Tendermint Core)
The most battle-tested BFT consensus engine in existence: n ≥ 3f+1 native, sub-6-second deterministic finality, ~10k TPS. Three direct hits on our spec:
- **Weighted voting power is native** (PoS stake weight) → vote_weight = reputation × coherence × certification maps onto the validator-power mechanism instead of being invented.
- **ABCI++** — application logic in *any language* over the Go consensus core → the Council stays Python, consensus is industrial-grade.
- **Vote extensions** (ABCI 2.0, v0.38+) → attach coherence/certification proofs to votes *inside the consensus protocol*.

**Catapult verdict:** do NOT write PBFT. Embed CometBFT, write the Council as an ABCI app. The 1-month estimate becomes mostly integration + the reputation-weighting function (ours).

### 7. Dark-vector GC (entropy audit, letter E) — est. 2 weeks

**STACK-NATIVE.** The RedisBus (shipped tonight, 10/10) gives native `EXPIRE`/TTL per key — vector decay is a Redis primitive, not a build. Reference counting on sv_id + TTL half-life (ρ = 1−2^(−Δt/half_life), atlas formula) + the alphabet letter-E audit script reading `bus.stats()`. No external library. (Note: searched Qdrant TTL — no native feature confirmed; irrelevant, we chose Redis.)

### 8. Alphabet audit / Drum Spine (26 assumption categories) — est. ~2 weeks

**CROWN JEWEL: CheckList** — `github.com/marcotcr/checklist` (Microsoft Research, ACL 2020, ~1.9k citations). The capability-matrix × test-type methodology is the direct structural ancestor of "26 assumption categories × probe types" — users found 3× more bugs with it. This is the immune-system design pattern, open-sourced.

**CROWN JEWEL: garak** — `github.com/NVIDIA/garak` — 100+ vulnerability probes, CLI sweep, JSONL+HTML reports. The per-letter probe engine.

**CROWN JEWEL: PyRIT** — `github.com/microsoft/PyRIT` (active dev moved from Azure/PyRIT, v0.11.0 Feb 2026) — multi-turn adversarial orchestration, 40+ attack strategies, DuckDB checkpointing. For the deeper "attack our own assumptions" passes.

**CROWN JEWEL: Inspect AI** — `github.com/UKGovernmentBEIS/inspect_ai` (UK AI Safety Institute) — structured JSON eval logs = the audit trail the 26-minute Drum Spine cycle emits.

**Catapult verdict:** the Drum Spine = CheckList matrix (design) + garak probes (engine) + Inspect logs (spine beat record). Script-layer work, as estimated.

### 9. Stigmergy demo (two agents, zero direct messages) — est. days

**WRITE-IT on the RedisBus.** The library landscape is thin (GitHub pheromone topic: ~16 repos, mostly coursework). But we don't need one: **the RedisBus pub/sub IS the pheromone field.** Two agents, no direct channel: agent A appends "trail" vectors to a layer; agent B subscribes; trail strength = TTL half-life (the atlas's ACO convergence formula ρ = 1−2^(−Δt/half_life) sets the TTL). Zero new dependencies. Days estimate holds — this is now a demo-script, not a build.

**ADJACENT signal:** a Rust "Active-inference + Learned Adaptive Stigmergy" AGI framework surfaced in the hunt (unverified authority) — someone else is publicly converging on stigmergy-as-substrate. Watch it; don't depend on it.

### 10. C2PA per-frame signing — est. days

**CROWN JEWEL: c2pa-python** — official Python bindings of the Rust reference SDK (`pip install c2pa-python`). Plus **c2pa-rs CLI**: `c2pa sign input.mp4 output.mp4 --manifest manifest.json` — signs video natively today. Per-frame prototype = extract frame (FFmpeg, in stack) → sign → verify. Then per-frame streaming as the research step.

**BONUS JEWEL: c2pa-attacks** — `github.com/contentauth/c2pa-attacks` — the *official* security test suite (malicious certs, unexpected fields). The immune system for our signing layer: test our forgery-proofing against the foundation's own attack fixtures. And it all slots into the verified route from Part G: Contributor member ✅ + SSL.com Provenance API as conformant generator.

### 11. IBM Quantum free tier — est. days

**CROWN JEWEL: pennylane-qiskit** — `github.com/PennyLaneAI/pennylane-qiskit` (official, Apache-2.0) — `qml.device("qiskit.ibmq", backend="ibm_brisbane")` and the PennyLane bridge (6 tests currently NumPy-fallback) runs on real hardware.

**Current terms (verified March 2026):** Open Plan = free 10 min QPU time per 28-day rolling window; log 20 min in any 12-month period → one-time offer of **180 minutes for 12 months**; **ibm_kingston (Heron r2, 340k CLOPS) now on the free tier.** The "days" estimate is right and the hardware got better since the estimate was written.

### 12. SOVOS Pixel (uncertainty material) — est. ~3 days

**WRITE-IT (white space, confirmed).** Zero libraries for uncertainty-driven fragment shaders surfaced — σ>128 → blur/flicker/amber is unclaimed territory, consistent with the atlas's "uncertainty pixel" unlock. Build path: **Three.js ShaderMaterial** (Three.js already in estate via sov-city-3d) + glsl-noise grain for flicker; **moderngl** if a Python-side renderer is wanted first. 3-day estimate holds; patent-note: this stays in the white-space ledger.

### 13. UE5 integration — est. ~3 months

**CROWN JEWEL: python_unreal_relay** — `github.com/igsxf22/python_unreal_relay` — minimalist real-time Python↔UE5 TCP relay (UE ≥ 5.6.1): control actors/pawns from Python, receive sensor feedback. This is the StateBus-reader plugin's skeleton: RedisBus `subscribe()` → relay → vector actors spawn on append.

**CROWN JEWEL: BlueprintWebSocket** (Fab Marketplace) — async duplex WebSocket for UE5, non-blocking threads, text or byte payloads — the live-telemetry channel.

**STACK-NATIVE:** UE Pixel Streaming is built-in for the portal-in-browser leg.

**Catapult verdict:** the transport half of the 11-component estimate is now free. The 3 months that remain are the J-Space visualizer, Convergence Portal, and pixel work — the parts that were always ours.

### 14. Quantum pixel / QPU-enhanced Honey — est. 2–3 months

**CROWN JEWEL: qiskit-machine-learning Quantum Autoencoder** — official tutorial + code: compress 5 qubits → 3-qubit latent + 2-qubit "trash" space, fidelity via swap test, RealAmplitudes ansatz, SamplerQNN training loop. **This is honey distillation as a quantum circuit, already implemented by IBM:** latent = honey, trash = evaporated water, fidelity = the distillation loss. Port to PennyLane idiom (our bridge) and the third arm has a working reference implementation on day one. Community QVAE repos exist for the variational variant.

### 15. Merging-as-a-service — est. 6–9 month window

**CROWN JEWEL: mergekit** (as #3 — the productizable core; CPU-capable out-of-core merges = the cost structure of the service).

**CROWN JEWEL: SakanaAI/evolutionary-model-merge** — `github.com/SakanaAI/evolutionary-model-merge` — CMA-ES (via Optuna) over parameter-space AND data-flow-space merges, **data-free**. Now **Nature Machine Intelligence (Jan 2025)**; already absorbed into mergekit and Optuna Hub; follow-up CycleQD (ICLR 2025). This is the WUDI-style data-free merge *productized by someone else* — which both validates the service and starts the window clock.

**Index: Awesome-Model-Merging** — `github.com/SunWenJu123/Awesome-Model-Merging` — the full method zoo (DARE, TIES, breadcrumbs, DELLA, SCE, Model Stock) for the collapse-screen options.

**Window verdict:** real and narrowing. Sakana published in NMI, mergekit mainstreamed the methods, Arcee commercialized. Our differentiated wedge is not merging — it's **SGM gates + Council adjudication + provenance-signed merge receipts** (c2pa for models). Nobody sells that.

---

## THE CROWN JEWELS, RANKED BY CATAPULT

| # | Jewel | Feeds | What it deletes from the queue |
|---|-------|-------|-------------------------------|
| 1 | **CometBFT** | BFT Council | Writing PBFT — the riskiest month in the queue |
| 2 | **HyperCore** | Poincaré pipeline | The entire hyperbolic-NN research phase |
| 3 | **mergekit + karcher** | FederatedStateBus, Merging-as-a-service | All three merge modes + the Fréchet centroid in weight space |
| 4 | **ripser/scikit-tda** | New-clan proposal | "Persistence validation" becomes 100 lines |
| 5 | **c2pa-python + c2pa-attacks** | Per-frame signing | Signing SDK *and* its own red team |
| 6 | **qiskit-ML quantum autoencoder** | QPU honey | The reference implementation of honey-as-circuit |
| 7 | **CheckList + garak + PyRIT + Inspect** | Drum Spine | Immune-system design + engine + audit trail |
| 8 | **python_unreal_relay** | UE5 | The StateBus-reader transport layer |
| 9 | **pennylane-qiskit** | IBM Quantum | The bridge to free real hardware (180-min offer live) |
| 10 | **evolutionary-model-merge** | Merging-as-a-service | The data-free merge engine (and the window warning) |

**Stack-native (no import needed):** Murphy Margin, Dark-vector GC, Stigmergy demo, UE pixel streaming — the RedisBus + geomstats + Redis TTL already cover them.
**Write-it (white space, don't import):** SOVOS Pixel shader, Lamport clocks (30 lines, ours).

*Honesty register: every repo above resolved in search this session. Star counts and versions cited only where sources stated them. The Rust stigmergy-AGI project is flagged ADJACENT/unverified. Qdrant TTL returned no results — Redis TTL is our decay primitive by design.*
