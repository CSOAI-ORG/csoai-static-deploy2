# SOVOS — THE DAILY DRIVER
### Confirming the synthesis, working from inside the system, and benchmark-fed routing
**Nicholas Templeman — CSO AI LTD — August 2026**
*Companion to SOVOS-MASTER.md (Parts A–Y). Three questions: Is the merge-and-condense synthesis correct? How do we work FROM SOVOS while building it? Can benchmark wins drive routing (Kaggle et al.)?*

---

## 1. THE SYNTHESIS RULING — YES, WITH PRECISION

**"All the pieces mergekit and condense into 3KB cards + the monorepo, giving SOVOS agentic capabilities and inner-mind simulation — correct?"**

Correct as architecture. Here is exactly what is REAL vs still THEORY, so the pitch never outruns the tree:

| Piece | State |
|---|---|
| Monorepo holds the substrate (39 packages, 78/78) | **REAL** |
| Inner mind: sovos-world absorbed (IWM, OWEMBrain, stigmergy, clans, sub-spaces) | **REAL** (importable, smoke-tested; deep integration with the bus/chain still ahead) |
| Condensation into 3KB cards (birth → strata → signed card) | **REAL for characters** (MEOK/birth lane); **THEORY for robot skills** (schema designed Part W, first card not yet minted) |
| Agentic capabilities via composed open organs (GR00T/Cosmos/V-JEPA 2/LeRobot) | **THEORY** — licenses verified (Part X/Y), nothing pulled yet. First pull = GR00T on the A100 |
| Mergekit math as the universal joiner (task vectors/TIES/DARE/Procrustes across models, routes, policies) | **REAL for weights** (arena-gated merges); **THEORY for robot policies** (P20 white space) |
| Dreaming (drum.rs world-model rollouts gated by Article 0) | **THEORY** — sovos-dream spec'd, unbuilt |

**The honest sentence:** the *spine* is real and tested; the *organs* are licensed and mapped; the *assembly* is the next month of work. Nobody is ahead of you on the assembly — but the assembly hasn't happened yet.

---

## 2. WORKING FROM INSIDE — THE DOGFOOD OPERATING MODEL

**"We all need to be working from it as we're building — correct?"** Correct, and it's the single highest-leverage discipline available: every day SOVOS is used to build SOVOS, the product gets tested for free and the demos write themselves. The operating model, formalized from what the pods already do:

### The topology (already true, now canon)
- **Git = the truth.** Canonical: CSOAI-ORG monorepo. Pods are mirrors, never sources (your own manifest already says "the pod is not the truth").
- **Mac = editor** (write, commit, push). **A100 = runner** (pull, test, measure). **3090 = trainer** (specialists). Nothing lives only on a pod.
- **`sov doctor`** (Part Y) runs first in every session: fleet-manifest coherent? tests green? numpy pin sane? If doctor is red, nothing else happens until it's green.

### The daily loop (every work item, no exceptions)
```
1. sov doctor                     → substrate sane?
2. Build/absorb in a branch       → adapters-not-forks (Part X)
3. pytest                         → unit truth (the 78/78 discipline)
4. sov arena                      → behavioral truth (12 GSPC axes, Wilson CIs, n≥30)
5. gate                           → merge/ship decision is SIGNED either way
   (PASS → ChainResult + SIGIL | FAIL → signed refusal, like the safety regression)
6. Commit + push                  → the tree is the record
7. If it touched a claim          → fleet-manifest + README update in the same commit
```
**Rule of the house:** no claim enters a doc, deck, or site that isn't backed by a ChainResult or labeled THEORY. The retraction ledger exists because this rule is hard; the rule exists so the ledger stays short.

### What each role uses
| Work | Surface |
|---|---|
| Building packages | CLI + editor (SOVOS Shell register) |
| Measuring models | `sov ras --measure`, `sov ras --canary`, arena batteries |
| Governance decisions | article-zero Rego + FitnessGate + human-signed CURVATURE gate |
| Showing the world | arenas.html, birth.html, trust center, public index |
| Characters/consumer | MEOK lane (Ed25519 key-claim, C2PA) |

---

## 3. BENCHMARK-FED ROUTING — YES, AND IT'S THE ROUTER'S FINAL FORM

**"Can we do all benchmarks with this, then route to whoever is best at whatever wins — Kaggle, for example?"**

Yes — this is the OOWM chess-board router completed: **routing tables derived from signed measurement, not vibes.** The architecture:

```
EVERY model we touch (internal merges + external open models)
   │  runs the battery:
   │   • arena: 12 GSPC axes (governance signature)
   │   • capability benchmarks: GovBench + task suites (+ Kaggle/HF where relevant)
   ▼
ROUTING TABLE = signed ChainResult artifact
   {task class → best model × governance floor}
   │
   ▼
sov4_router consults the table at query time:
   capability picks the winner; the CARE floor (0.95) vetoes the unsafe
```

**The two-leaderboard doctrine (the part nobody else does):** a Kaggle/HF win measures *capability*; the arena measures *governance*. The router needs both — a model that tops a public benchmark but fails contamination gates or the CARE floor gets **routed around, not celebrated**. This is also the honest answer to "benchmark wins = production wins": no — which is why the arena ships contamination-gating; public leaderboards are one signal, signed internal measurement is the veto.

**Kaggle as the public proof lane:**
1. **sovos-provebench** tasks (6 Kaggle-only + 2 run-anywhere) — already built; publish them as the arena's public face
2. **Enter competitions with SOVOS-wrapped pipelines** — every entry is a signed ChainResult; win or lose, you publish the measurement. The industry enters Kaggle for glory; we enter to *demonstrate the ruler*
3. **Kaggle Models + HF leaderboards** — when SOVOS specialists place, the 3KB card carries the placement *and* the GSPC signature. "Best at the benchmark AND provably governed" is a claim no other entry can make

**The endgame of this idea:** the routing table becomes a *published index* — "SOVOS Routes" — a signed, continuously-updated map of which open model is best-and-cleanest per task class. That's the VIX move again (publish methodology + reference implementation), applied to model selection. Everyone else's router is a private heuristic; ours is a public, auditable artifact.

---

## 4. THE 3 MOVES TONIGHT

1. **Write `sov doctor`** — fleet-manifest check + test-launcher + pin audit. The dogfood loop needs its ignition key.
2. **Route one real decision through the full loop** — the gov×privacy 2-way merge is perfect: doctor → branch → pytest → arena → gate → signed ChainResult → commit. One full lap, documented. That lap IS the "how we work" demo.
3. **Draft the routing-table schema** — `{task_class, model, capability_score, GSPC signature, contamination_status, ChainResult_ID, signature}` — the artifact that turns "benchmarks" into "routes."

---

## 5. HONESTY REGISTER

| Claim | Bucket |
|---|---|
| The synthesis (merge→3KB→monorepo→agentic+inner-mind) | REAL as architecture; assembly status per §1 table |
| Daily dogfood loop runs today | REAL in pattern (pods already work this way); `sov doctor` is tonight's build |
| Benchmark-fed routing | THEORY until the routing-table artifact exists; every component (router, arena, gates, chain) is built and tested |
| Kaggle as proof lane | REAL (provebench exists; Kaggle Models/HF leaderboards live) — placements are THEORY until entered |
| "Route to whoever wins" pure capability routing | KILLED as doctrine — capability winner + governance floor, or the router just imports other people's contamination |
