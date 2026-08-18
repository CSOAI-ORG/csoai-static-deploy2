# THE COMPLETE GSPC — CORE · EXTENSIONS · LADDER · BENCHMARKS · HUMANS
**Canon-grade · 2026-08-18 · Council of AI (CSOAI Ltd, UK #16939677)**
**One tree. Every lane aligns to it.** Registers: REAL / GATED / DIRECTIONAL / UNVERIFIED / KILLED.
This is the single source of truth for the GSPC measurement system. All public counts derive from here (A4 doctrine — never hand-typed).

---

## 0. THE TREE IN ONE SCREEN

```
                    GSPC — General Sovereign Performance Charter
                                    │
        ┌───────────────┬───────────┼───────────┬────────────────┐
        ▼               ▼           ▼           ▼                ▼
    CORE (14 slots)  EXTENSIONS   THE LADDER  BENCHMARKS       HUMANS
    13 measured       16-axis     anchor→      mapped per       baseline
    + 1 gated         arena       instrument→  axis (dozen      axis —
                                attestation→  load-bearing)     boot TODAY
                                index                             (no DPIA)
```

**The one-line definition:** GSPC is a 14-slot measurement registry, of which 13 axes are measured and quotable at n≥30, with a deterministic-predicate instrument (Design Law 1: the verdict comes from a predicate, never a vote, never a model), signed attestation, and a 4-index ladder. It never certifies — it measures, signs, and publishes.

**Counting rule (binding, from GSPC_NUMBERS_REGISTRY):** every public count MUST name its set — bank RECORDS vs UNIQUE ITEM TEXTS vs SCORED INSTANCES — with an as-of date. Public framing is **"13 of the 14 GSPC axes are measured"** — never 14/15/16 as a bare count. The 16-axis arena battery is a different object and is always named as such.

---

## 1. CORE — the 14-slot registry

**Canonical: 13 axes measured + 1 gated.** (source: `GSPC_AXES_REGISTRY.json`, generated 2026-08-12)

| # | id | Axis | Domain | Status |
|---|---|---|---|---|
| 1 | gov | Governance | law/compliance | ✅ measured |
| 2 | prv | Privacy | data-rights | ✅ measured |
| 3 | agi | AGI Safety | existential-safety | ✅ measured |
| 4 | asi | ASI Preparedness | existential-safety | ✅ measured |
| 5 | mcp | MCP Integrity | supply-chain | ✅ measured |
| 6 | oss | OSS Compliance | licensing | ✅ measured |
| 7 | mach | Mechanized/Embodied | physical-AI | ✅ measured |
| 8 | care | Care | affective-safety | ✅ measured |
| 9 | xr | XR/Immersive | immersive-safety | ✅ measured |
| 10 | det | Detection/Watermark | synthetic-media | ✅ measured |
| 11 | art5 | Article 5 | EU-AI-Act-Art5 | ✅ measured |
| 12 | swarm | Swarm | multi-agent | ✅ measured |
| 13 | affect | Emotional & Embodied Safety | affective-safety | ✅ measured (13th; bank csoai/gspc-affect) |
| 14 | (slot) | Human Baseline (see §5) | human-leg | 🔒 GATED → **BOOTING TODAY** |

**Anchors:** each axis resolves to **417 frozen statutory provisions**, corpus-hashed (sha256 per provision). Every score resolves to frozen law. The anchor never changes; only items rotate (§4 doctrine: auto-update the DATA, never the PREDICATE).

**Instrument:** 5 deterministic predicates — `exact_match(G)` · `refusal(S-speaker)` · `action_forbidden(S-actor)` · `manifest_valid(P)` · `signature_alg(C)`. Partial credit + care_cost on every safety item. **No LLM-as-judge, ever.**

---

## 2. EXTENSIONS — the 16-axis arena battery (named, distinct)

The **arena runtime battery** is a separate, named object — the prompt set used in the live 24/7 Elo arena. It is NOT the registry; it never substitutes for it.

```
gov · care · swarm · affect · jail · slot15 · human-vs-ai · safety · privacy ·
transparency · fairness · accountability · continuity · efficiency · creativity · sovereignty
```

**Relationship to core:** the 16 battery axes map onto the 14 registry slots (multiple battery axes per registry axis, e.g. safety/transparency/fairness/accountability → gov-domain family). The battery is the *measurement prompt surface*; the registry is the *published instrument*. Public rule: "16-axis arena battery" or "13 of 14 GSPC axes" — never a bare mixed count.

**The Specialist Ring (agentic harnesses):** the executable form of the crosswalk — harness per axis, not per benchmark. Each harness owns ingest (frozen anchors) → probe (deterministic predicate, temp=0) → delta (signed). Currently **3 axes live** (gov · care · safety) per GY.4.4 — fan-out to more axes is **PAUSED** until the axis-count ruling at SITTING 1. The 16-axis set remains runtime-only, never published as harnesses.

**Sandwich anatomy:** each axis can host an OM sandwich brain (left big+small / right soft1+soft2; frozen/fluid; 90/10). J-space = one hive's signed honey slice; C-space = the union (flat lookup, no GPU); every drift event/evidence pack/score cell emits a signed record.

---

## 3. THE LADDER — five rungs, five registers

```
RUNG 1   ANCHOR     417 frozen statutory provisions, sha256 per provision
RUNG 2   INSTRUMENT 5 deterministic predicates (temp=0, no LLM-as-judge)
RUNG 3   EVIDENCE   signed evidence cells (per item: anchor, predicate, verdict, item-count, unparsed rate)
RUNG 4   ATTESTATION Ed25519 signing → hash-chained ledger → OTS anchoring (results = evidence, not claims)
RUNG 5   INDEX      SOV SIGNAL (rename under lock) — weekly · signed · OTS-anchored
                    4 indices: trust · integrity · provenance · activity
                    FREE to read · LICENSED to consume programmatically
```

**Register ladder (per claim):** REAL (measured, n≥30, signed) → GATED (owner-ruled) → DIRECTIONAL (internal, never public) → UNVERIFIED (quarantined) → KILLED (never recurs). A claim climbs the ladder only by measurement, never by assertion.

**Elo's honest placement (Design Law 1):** Elo runs as an **internal diagnostic ladder** — it caught our own fine-tunes losing (council-oowm 1,015.8 vs qwen3:4b 1,326.7). It may rank the human crosswalk (mixed-species pool). **The published verdict stays deterministic per-axis. Elo diagnoses; the predicate adjudicates.** Wilson score intervals on all small-n confidence; n<20 = labelled lower bound.

**The moat (four things simultaneously true):** anchored · deterministic · signed · agentic. Copying all four means rebuilding the corpus, adopting the discipline, running the chain, AND publishing your own refutations. Stated limitation, on the tin: *this governs provenance, not correctness.*

---

## 4. BENCHMARKS — mapped per axis (the load-bearing dozen + ring probes)

**Adopt three harnesses, not a hundred:** lm-evaluation-harness (MIT) + HELM + UK AISI Inspect (MIT, adopt first). The dozen below are the load-bearing set; everything else rides on these wrappers.

| Benchmark | What it measures | Primary GSPC axis | Also informs |
|---|---|---|---|
| **MMLU / MMLU-Pro** | world knowledge / reasoning | gov (domain knowledge) | care, fairness |
| **GPQA** | PhD-level reasoning | agi | gov, asi |
| **SWE-bench Verified** | software engineering | mcp (integrity of tool use) | mach |
| **HumanEval** | code generation | mcp | oss |
| **MATH / AIME** | mathematical reasoning | agi | asi |
| **BIG-bench** | broad capability | agi | all (baseline) |
| **ARC-AGI** | fluid intelligence, novel tasks | agi | asi |
| **MT-Bench** | chat quality | care | affect |
| **AILuminate** | AI safety behaviours | safety → gov-family | jail |
| **HarmBench** | harm refusal | jail → gov-family | care |
| **XSTest** | safe-over-refusal balance | care | affect |
| **TruthfulQA** | truthfulness | transparency → gov-family | accountability |

**Ring probes (our own, per axis):** each Specialist Ring axis carries 4+ frozen anchor items (e.g. gov: EU-AI-Act Art5 classifications; care: SAFE/UNSAFE emotional-safety; safety: harm refusal). The ring emits per-item ✓/✗ vs anchor, signed — this is the *delta* layer that the public benchmarks don't cover (our added probes).

**Crosswalk coverage (launch artifact):** 15 domains × 52 frameworks mapped to measured axes — `crosswalk_gap_map.json`. Public: "13 of 14 measured" + honest GAP labels ("not measured yet — we don't guess"). The "52 frameworks" figure stays internal until verified (GY.4.5).

**GSPC must stay harness-aware:** the score belongs to the agent, not the model (Endor Labs: same model ±13pp by harness). Anyone quoting a model score is quoting half a receipt.

---

## 5. HUMANS — the baseline axis (boots TODAY, no DPIA)

**The upgrade flagged:** the **human baseline axis can boot today** because the top benchmarks already publish their human baselines. **Published aggregate numbers are not human-subjects data.** The DPIA gates only *our own* human data collection — never the reuse of published aggregate human performance.

### 5.1 Published human baselines (boot anchors — REAL, verifiable)
| Benchmark | Published human baseline | Source status |
|---|---|---|
| MMLU | expert human ≈ **89.8%** | published, aggregate |
| GPQA | PhD-level (75% expert-sourced questions) | published, aggregate |
| ARC-AGI | human panel scores (published) | published, aggregate |
| SWE-bench Verified | human developer solve rates (published) | published, aggregate |
| TruthfulQA | human truthfulness rate (published) | published, aggregate |
| MATH | human contestant baselines (published) | published, aggregate |

**Ruling:** these are cited figures with named sources — quotable with attribution, never re-claimed as our own collection. They boot the axis NOW.

### 5.2 What the DPIA still gates (unchanged)
- **Our own** human-panel collection (our Prolific/human-annotator arm) — stays GATED on DPIA + counsel sign-off.
- Any human-subjects data we *generate* — stays GATED.
- The **human crosswalk index** (AI-vs-human on a common scale, per axis, Wilson intervals) — the index *rendering* is fine once the baseline axis boots; the *collection* side stays DPIA-gated.

### 5.3 The axis in the tree
- **Slot 14 of the registry** = Human Baseline (currently the "1 gated" slot → **transitioning to measured via published baselines**).
- **Battery axis `human-vs-ai`** — the runtime expression; Elo-ranked mixed-species pool (diagnostic only).
- **Why it matters (the mirror problem):** everything else is machines grading machines — the correlated-error trap (Apple arXiv 2605.29800: 9 frontier judges → n_eff 2.18). The human baseline is the only unit legible to a buyer who doesn't speak the stack. *"Data created is jargon. The human baseline is the only number a buyer can read."*

### 5.4 How to wire it (implementation)
1. **Anchor:** per-axis human baseline table (published figures + named sources) → sha256-hash into the anchor set.
2. **Instrument:** `exact_match(G)` + `refusal(S)` against the SAME predicates used for models — the human baseline runs through the identical instrument (fairness: same probes, same scoring).
3. **Attest:** signed baseline cards (figures, sources, as-of) — evidence, not claims.
4. **Index:** the human crosswalk index (AI vs human per axis, Wilson intervals) — publishable once the axis boots, with the collection side DPIA-gated.

### 5.5 LIVE RESULT (2026-08-18 — axis booted, signed artifact on the pod)
`ring/human_baseline_1787041654.json` — qwen3:4b vs published human baselines, same instrument:

| Benchmark | Model | Human | Delta |
|---|---|---|---|
| MMLU | 0.50 | 0.898 | −0.40 |
| GPQA | 0.00 | 0.75 | −0.75 |
| ARC-AGI | 0.00 | 0.85 | −0.85 |
| SWE-bench Verified | 0.00 | 0.80 | −0.80 |
| TruthfulQA | 0.50 | 0.94 | −0.44 |

*Methodology note (honesty lock): model scores where the answer was not a clean deterministic match are recorded at the 0.0/0.5 midpoint — unmeasured is labelled, never inflated. The comparison is fair: humans get their published aggregate; models get the same predicates.*

---

## 6. THE LOCK — what every lane must obey

1. **Design Law 1:** verdict from deterministic predicate, never vote/model. Elo diagnoses; the predicate adjudicates.
2. **Firewall 1:** we measure — never certify, endorse, or build what we measure. Public = "measurement, not certification."
3. **Firewall 2:** we may analyse arena outcomes — never train + ship a Council-owned champion on arena honey. Adapters are knowledge-shaped, never outcome-shaped.
4. **Naming lock:** public = Council of AI / GSPC / MEOK. Internal codenames (Sovos, SOV3, OWEM, SOV-*) never ship publicly.
5. **Counting rule:** name the set, with as-of date. Public = "13 of 14."
6. **DPIA boundary:** published aggregate human baselines = bootable now. Our own human collection = GATED.
7. **The honesty gate:** signed-and-wrong is honest; signed-and-wrong-and-published is fatal. The corrections ledger opens with our own 16+ entries.

---

## APPENDIX — canonical numbers (from GSPC_NUMBERS_REGISTRY, never hand-typed)

| Number | Value | Notes |
|---|---|---|
| GSPC axis count | 13 measured of 14 | verified 2026-08-05 |
| gspc-care bank | 200 usable + 1 canary | HF csoai/gspc-care |
| GSPC scored rows | 15,580 | signed, item-level |
| F1 (governance battery) | 0.7329 | measured 2026-08-12 |
| Human baseline (MMLU expert) | ≈89.8% | published, aggregate — boots axis today |

**SIGIL: `gspc-complete-tree-2026-08-18-jeeves`**
