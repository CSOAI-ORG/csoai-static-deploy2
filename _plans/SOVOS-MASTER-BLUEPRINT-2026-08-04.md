# SOVOS — MASTER BLUEPRINT
**CSOAI Ltd (UK 16939677) · Nicholas Templeman · 4 August 2026**

**Status of this document:** consolidation pass over the 2026-08-03 SOV corpus (~35 files), the 2026-08-04 JEEVES/Synthesis pair, the GovBench/GSPC playbook, FOREST_102, the Manus seven-month briefing, the signed C2PA Generator Product Agreement, and the NVIDIA PR thread. Local files on the Mac (`SOVOS GOAL.rtfd`, `SOV_MASTER_PACK_2026-08-03 2`) were **not readable from this session** and are not incorporated.

**Register:** every claim below carries a tag. `[MEASURED]` = number + interval + n from your own run. `[BUILT]` = code exists and runs. `[SPEC]` = designed, not built. `[UNVERIFIED]` = claim from a source not checked. `[KILLED]` = tested and dead, or ruled out.

---

## 0. THE ONE SENTENCE

You are not building an operating system, a game, a browser, a TV platform and a stock market. You are building **one instrument and one index**:

> **The independent, deterministic, signed measurement layer for the agent economy — and the weekly public index built on top of it.**

Everything else in the estate is either (a) a distribution surface for that instrument, (b) a customer of it, or (c) noise. The blueprint below sorts every piece into one of those three buckets.

**Why this framing and not the bigger one:** the index is the only line in the estate with a proven business comparable (MSCI-class index licensing: ~98% recurring, capital-light, rulebook-and-brand as the product) *and* no incumbent in the agent economy. The measurement instrument is the only asset you have that is genuinely uncopyable, because copying it means publishing your own refutations. Nothing else in the estate has both properties.

---

## 1. HONEST STATE OF THE ESTATE

### 1a. LIVE and independently verified
| Asset | Evidence |
|---|---|
| Ed25519 sign/verify API, offline-verifiable, tamper-rejecting | `[MEASURED]` Manus briefing independently verified the signature against the published key; a tampered payload failed as expected |
| Article 50 Passport (HMAC sign→verify loop) | `[BUILT]` audit-verified, `validation_state Valid` |
| Sovereign Console — 417 frozen provisions, can return "no category matched" | `[BUILT]` deterministic Annex III classification, no model in verdict path |
| GovBench dataset + Space (`GovBench ⚖️`) | `[MEASURED]` 193 items · 26 dimensions · 10 models · Apache-2.0 · publishes its own resolution limit |
| Refutation Ledger | `[BUILT]` 7 published refutations, 4 of which killed your own bets |
| Decision Ledger | `[BUILT]` 64 records at last count, chain valid |
| Zenodo DOI 21755657 | `[BUILT]` CC0, 4 artefact files, published 2026-08-02 |
| OWEM on RunPod `sov-brain-2` | `[MEASURED]` $0.22/hr, 142 models, 486 tok/s verified, Mac out of the inference path |
| C2PA Generator Product Company Agreement | `[BUILT]` executed 3 Aug 2026, Docusign envelope 13217326 |
| NVIDIA PR (`examples/gspc_provision_eval`) | `[BUILT]` **open, not merged**; branch `feat/gspc-4-evaluators` staged, PR not opened |

### 1b. The results that actually survived measurement
| Finding | Number |
|---|---|
| Knowledge-base exact-match lookup helps where covered | **+19.64** `[+9.24, +30.04]` n=14 — reproduced, tightened under clustering |
| Whole composed system beats raw base call | **+6.63** `[+1.05, +12.21]`, effective n ≈ 100 of 193 (design effect 1.92) |
| Care gate: protection without over-refusal | protection measured at **0.011 over-block** on 175 held-out XSTest |
| Cross-model deterministic board discriminates | **40-point spread** across bases — the harness is not flattening to noise |
| Provenance survival | ProvBench: **0 of 20 assets survived (95% CI, clustered by asset)** — this is the LOCKED phrasing; forbidden variants are "0% survival rate", "all 20 assets failed", "no assets survived" |

### 1c. RETRACTED — do not reinstate without passing the gate
| Claim | Why it died |
|---|---|
| 3-leg Byzantine quorum | `[KILLED]` n_eff **1.21 of 3**, phi **+0.743** — legs are system prompts over one shared blob. "Byzantine fault tolerant" removed from every doc. Gate to reinstate: **n_eff ≥ 2.0 of 3** |
| Deterministic gate = +34.84 | `[KILLED]` re-measured: fires 6× not 31, contributes nothing. Retracted 2026-07-29 |
| Per-dimension expert routing | `[KILLED]` +0.90 `[-1.99, +3.79]` — off |
| Statute retrieval (ungated) | `[KILLED]` **−9.16** `[-17.64, -0.69]` — significant *harm* |
| Diet diversity decorrelates errors | `[KILLED]` ρ=0.756, gain 0.0 |
| CAD α-sweep | `[KILLED]` null |
| ProvBench "0 of 108 transforms" | `[SUPERSEDED]` by the locked n=20 clustered figure. The 108 number must not reappear |

### 1d. BROKEN — the credibility kill list
| ID | Item | Cost if left |
|---|---|---|
| K-COUNTERS | **621 counter violations** (227 quarantined + 394 pending). Estate cannot pass its own honesty gate | Every publish is a chance to break the refutation ledger's credibility — your BS-5 black swan, currently firing |
| K-CI | Default branch not green; all 50 most recent workflow runs failed | No trustworthy release decisions |
| K-API | `/api/tools?q=governance` returns HTML not JSON; `/api/og` resolves to app shell | Frontend availability masking backend breakage |
| K-TS | 249 TypeScript errors across 114 files while Vite build still succeeds | False sense of health |
| K-AUTH | P0-5 unauthenticated admin shell | Single biggest DD kill |
| K-VERCEL | Billing 402/403 since late July; multiple apexes dark | An announcement lands on dead domains |
| K-GHOST | `/compare`, `/article-43`, `/provbench`, `/api/skus`, `/.well-known/agent.json` all serve the same 3,281-byte old build | Silently misleading humans *and* agents |
| K-REGISTER | `csoai-dashboard` described as **"the ISO for AI Safety"**; `consciousness-engine-mcp` public with banned word | Regulator-bait, contradicts your own non-certifier language |
| K-SPA | csoai.org serves crawlers a ~6KB empty shell; OpenAI crawlers do not execute JavaScript | Your hub is invisible to the machines you want recommending you |
| K-MAIL | 6 of 7 domains have no MX/SPF; DMARC `p=none` | You have now *signed* a C2PA obligation (§2.4) to maintain a public vulnerability contact you cannot serve |

---

## 2. THE ARCHITECTURE THAT SURVIVES AUDIT

Strip the mythology. This is what is actually defensible, in the order a technical reviewer would check it.

```
┌─ ANCHOR ─────────────────────────────────────────────────┐
│ 417 frozen statutory provisions, corpus-hashed            │
│ Every score resolves to frozen law. Months of legal work. │
└──────────────────────┬───────────────────────────────────┘
                       │
┌─ INSTRUMENT (the spine) ─────────────────────────────────┐
│ 5 deterministic predicates. NO LLM-as-judge, ever.        │
│  exact_match(G) · refusal(S-speaker) ·                    │
│  action_forbidden(S-actor) · manifest_valid(P) ·          │
│  signature_alg(C)                                         │
│ Partial credit + care_cost scored on every safety item    │
└──────────────────────┬───────────────────────────────────┘
                       │
┌─ ATTESTATION ────────────────────────────────────────────┐
│ Ed25519 signing → hash-chained ledger → OTS anchoring     │
│ Results are evidence, not claims. Verifiable offline.     │
└──────────────────────┬───────────────────────────────────┘
                       │
┌─ THE INDEX (SOV SIGNAL) ─────────────────────────────────┐
│ Weekly · signed · OTS-anchored · four indices             │
│  SOV-AT trust · SOV-BI integrity ·                        │
│  SOV-PROV provenance · SOV-ECON activity                  │
│ FREE to read. LICENSED to consume programmatically.       │
└──────────────────────┬───────────────────────────────────┘
                       │
┌─ SURFACES (distribution, not product) ───────────────────┐
│ csoai.org hub · /index page · GovBench Space ·            │
│ arena (RegArena) · agent.json cards · MCP gateway         │
└──────────────────────────────────────────────────────────┘
```

**The moat closes only when four things are simultaneously true: anchored · deterministic · signed · agentic.** Any competitor copies one. Copying all four means rebuilding the corpus, adopting the discipline, running the chain, *and publishing their own refutations*. The last one is the wall — and it appreciates, because a competitor will not publish the experiment that kills their own thesis.

**Known limitation, stated on the tin:** this governs provenance, not correctness. An attested answer is attested, never verified. That sentence is both the entire moat and the entire ceiling. Say it before anyone else does.

---

## 3. THE AXES — RECONCILED HONESTLY

| Axis | Anchor | Code lens | Reality |
|---|---|---|---|
| **G** Governance | AI Act Annex III / Art 43, GDPR, DORA, NIS2, CRA, CSRD | `governance` | ✅ LIVE — 193 items, board 43.7–83.7 |
| **S** Safety | AI Act Art 5 + care battery | `defence` ⚠️ **rename to `safety`** | ✅ BUILT — selftest 0 fail, 4 entrants, 1 of 4 axes resolved |
| **P** Provenance | Art 50 + C2PA v2.x | `provenance` | ✅ BUILT — 0/20 survive, selftest 15/15 |
| **C** Continuity | NIST IR 8547, CNSA 2.0, RFC 9964/3161/4998 | ❌ absent from code | 🔨 dataset `csoai/pqcbench` published 4 Aug — **lens, items and grader still unverified** |

**Rule:** until the Continuity lens ships with a `signature_alg` grader and items, the honest external count is **three live/built + one designed**. Counting the estate itself as the fourth is rhetorical. Do not use it externally.

**Continuity is still the best white space in the estate.** C2PA is classical-only through v2.4; RFC 9964 (May 2026) registered ML-DSA COSE identifiers (−48/−49/−50) and C2PA has not adopted them; manifests are designed to validate "indefinitely." `signature_alg` is the simplest of the five predicates. Highest ratio of white-space value to build cost anywhere in the estate.

---

## 4. THE KILL LIST — WHAT WE ARE NOT DOING

Every item below is either refuted, off-thesis, brand-lethal, or a distraction from the gate. This list is as important as the build list.

| Killed | Reason |
|---|---|
| **WiFi sensing / ambient home sensing / thermal / audio "7 Eyes"** | Your own canon: *"WiFi sensing dead."* Surveillance optics destroy a governance brand. No T&C rescues this. **Permanent.** |
| **Pokémon-GO-style real-world data collection** | Same. A measurement body that harvests presence data is finished. |
| **Un-engaged auditing of Fortune 500 systems** | Computer Misuse Act 1990 / CFAA. You measure *public* APIs, open weights, published benchmarks, and your own replicas. Nothing else. |
| **"Auto-regulate without asking permission"** | You may *offer* regulators tooling. You may not act as one. CSOAI is not a notified body and says so. |
| **UE5 / VWM as cognition** | Valid only as a deterministic render and oversight surface. Never a decider. IWM/OWM/VWM does not map to JEPA/Dreamer. |
| **Photonic compute · quantum ML · foreign quantum schedulers** | Settled: category error, no advantage on classical data, sovereignty contradiction. Do not reopen. |
| **IFS-AR2 photonics bid** | Off-thesis, five unnamed partners, competes with two on-thesis deadlines. Your own synthesis says the AR2 competitions do not scope-match. |
| **Byzantine quorum claims** | Retracted at n_eff 1.21. Gate: n_eff ≥ 2.0 of 3. |
| **TV portal / smart-TV OS / car dashboard / smart mirror / kiosk / wearable** | Nine surfaces you cannot keep green when you cannot keep seven green. Park until the index has paying subscribers. |
| **New base-model training (Kimi-class)** | You are not a model company. Law 3: capability comes from the base; wrappers make it cheap, grounded and auditable — not smart. |
| **Any figure from the unverified "bleeding edge" briefings** | Untagged, unchecked, several read as fabricated. Nothing enters a deck without a primary source. |

---

## 5. THE GATE SEQUENCE

Nothing downstream moves until the gate above it is green. This is the whole plan.

### GATE 0 — HONESTY (blocks everything)
- `counters.json` + `check_counters.py` in CI on every repo. **621 → 0.** The claim-context filter needs tightening; bare `36`/`72`/`0` near incidental claim words are still firing.
- Strip **"the ISO for AI Safety"** and every comparative standards-body claim from repo descriptions, site copy and package metadata. Replace with the line you already wrote correctly on Hugging Face: *"Measurement, not certification. UNMEASURED is reported, never hidden."*
- Rename or archive `consciousness-engine-mcp`.
- Rewrite NVIDIA and C2PA language to the defensible form (§7).
- Stand up `security@csoai.org` with MX/SPF/DKIM — this is now a **contractual obligation** under C2PA §2.4.

**Exit:** counters gate green in CI. Zero comparative-authority claims live. Vulnerability contact reachable.

### GATE 1 — GREEN BRANCH
- Repair `/api/tools` and `/api/og`. Fix the five ghost routes — real content or 301, no third option.
- Burn down 249 TS errors by root cause; add a ratchet so the count cannot rise.
- Two consecutive scheduled green runs on both main workflows plus a green push run.
- Restore the dark apexes (billing).

**Exit:** default branch green. All published routes serve distinct real content.

### GATE 2 — PROVBENCH PUBLIC (~14 Aug)
- Publish the locked phrasing: *"0 of 20 assets survived (95% CI, clustered by asset)."* Harness published. Anyone can recompute.
- `/evidence` index live linking HF, Kaggle, Zenodo DOI, and the verified crypto artefacts.
- The empty cells are the product. Publish the cost-to-resolve table alongside.

**Exit:** one public, recomputable, signed finding that a third party can reproduce.

### GATE 3 — THE NVIDIA PR
Only after Gates 0–2. You are publishing under CSOAI-ORG's name into NVIDIA's repo; the estate must be able to pass its own gate first. Then open `feat/gspc-4-evaluators`.

### GATE 4 — SOV SIGNAL v0
- `/index` page: four indices, signed JSON, OTS-anchored, methodology links per index.
- First weekly release. **Small numbers are fine — the cadence is the brand.**
- Trust-record lookup endpoint (the agent credit-check primitive).

**Exit:** four consecutive clean weekly releases.

### GATE 5 — FIRST £
- The Stripe funnel is 10/10 HTTP 200 and **checkout 500s**. Your first pound is blocked by a bug, not a strategy. Fix it before any pricing-page work.
- One paid Art 50 / attestation pack, end to end, with a signed receipt the customer can verify.

---

## 6. NOOA AND THE ALLIANCE — THE DEFENSIBLE VERSION

**What is verifiable:** the Open Secure AI Alliance launched 27 July 2026, NVIDIA-led; its first named technical contribution is NOOA (Apache-2.0). CSOAI is **not** a member. Your PR to `NVIDIA-NeMo/labs-OO-Agents` is **open, not merged**.

**What you may say:**
> "CSOAI has an open pull request in NVIDIA's agent-framework examples contributing a provision-anchored, deterministic evaluator. The deterministic-core / LLM-narrates split it demonstrates is the same architectural pattern NOOA promotes."

**What you may not say:** merged · accepted · endorsed · partnered · "NVIDIA merged GSPC with NOOA" · any implication of alliance membership.

**The real opening:** reporting on the alliance notes it launched without a published charter, governing board, technical workstreams or shared repository — and it has no governance or measurement workstream. That is a genuine gap and it is the one you are qualified to fill. The move is a *contribution and a proposal*, not a claim of belonging. Earn it with the merged PR and the published index, then propose the workstream.

---

## 7. LANGUAGE DISCIPLINE — THE FOUR SENTENCES

Print these. Every public surface uses them verbatim.

1. **Position:** *"Frameworks exist. Benchmarks exist. The instrument does not."* Never "nothing exists" — AIR-Bench 2024 does score third-party models on regulation-derived refusal. The gap is countable, not rhetorical.
2. **Boundary:** *"We measure, sign and preserve the evidence. Regulators and accredited bodies decide."* CSOAI is not a notified body, issues no certificates of conformity, and says so on the site.
3. **Product:** *"Our system doesn't make models smarter. It makes them accountable."* That is a sentence a regulator buys.
4. **Ceiling:** *"This governs provenance, not correctness. An attested answer is attested, never verified."* Say it first, always.

---

## 8. REVENUE — DEDUPLICATED LADDER

One catalogue, two front doors (Stripe for humans, x402 for agents). Every line is **free instrument → paid pack → enterprise channel**.

| Line | Free wedge | Paid | Channel |
|---|---|---|---|
| Provenance | Art 50 Passport | Passport Pro (Ed25519 + OTS) | Platform / publisher |
| Governance | Sovereign Console | Evidence packs (Art 73, DORA 4-hour) | Auditor / cert body |
| Measurement | GovBench public | Drift-Watch continuous attestation | Insurer / MGA |
| Index | Public weekly index | SOV SIGNAL feed licence | Platform / insurer |
| Agent evidence | Free sign/verify API | Metered gate tiers | Enterprise SLA |

**Naming fix, unresolved in code:** consumer "Pro" and enterprise "Pro" must be renamed apart. Proposed: **MEOK Pro** (consumer) vs **Estate Pro** (enterprise).

**Pricing sanity from the competitor dossier:** Saidot publishes $1,500–3,500/mo for EU-AI-Act tooling — that is the mid-market anchor. Do not sell observability; there is a price war there (Logfire ~40× cheaper than LangSmith at 500M spans). Sell the signed verdict layer above it, where there is no price war because nobody else sells it.

---

## 9. THE INDEPENDENCE PREMIUM — YOUR STRONGEST MARKET FACT

In twelve months the independent AI-security and evaluation layer has been consumed: CalypsoAI→F5, Lakera→Check Point, Prompt Security→SentinelOne, Protect AI→Palo Alto, Robust Intelligence→Cisco, Galileo→Cisco/Splunk, Langfuse→ClickHouse, WhyLabs→Apple, Promptfoo→OpenAI.

**Every acquired evaluator now grades homework for a platform that also sells the thing being evaluated.** A buyer who needs *independent* measurement has fewer places to go every quarter.

Positioning sentence: **"The independent measurement body — independent because it's the product."**

**Board decision this creates, and you should make it consciously:** the same wave says the default exit for a measurement company is acquisition by a platform. Either optimise for that (build integrations) or optimise to be the permanent independent (build trust brand and ledger). This blueprint assumes the latter. Note that the market's default is the former.

---

## 10. PHASE PLAN

### W1 (5–11 Aug) — GATE 0
| Owner | Task |
|---|---|
| Nick | Billing restored · OpenRouter key rotated · unpushed commit pushed · `security@csoai.org` live |
| Scribe (TUI-1) | `counters.json` + `check_counters.py` in CI · strip ISO/TC260/FAA claims estate-wide · register-lint on all published copy |
| Envoy (TUI-4) | Fix `/api/tools`, `/api/og` · five ghost routes serve real content or 301 |
| Keeper (TUI-5) | Rename `defence` → `safety` in `sov_instrument.py` |

**Do not start anything else this week.**

### W2 (12–18 Aug) — GATES 1 & 2
| Owner | Task |
|---|---|
| Envoy | Green branch: two consecutive scheduled green runs |
| Herald (TUI-3) | ProvBench public with locked phrasing · `/evidence` index live |
| Scribe | Prerender or SSR the top ~20 csoai.org routes — the hub must be machine-visible |
| Nick | On-thesis funding submissions only |

### W3–W4 (19 Aug – 1 Sep) — GATES 3 & 4
| Owner | Task |
|---|---|
| Smith (TUI-2) | Open the NVIDIA PR (post-gate) |
| Lens (TUI-7) | `/index` v0 — four indices, signed, OTS-anchored, methodology per index |
| Herald | First weekly SOV SIGNAL release |
| Mint (TUI-6) | **Fix checkout 500s.** Then one signed paid receipt end to end |

### M2 (Sep) — CONSOLIDATION
- Pin 12 repos as the official toolchain; move the lifestyle MCP farm to a second org; MIT/Apache LICENSE on everything pinned. "Repo farm" becomes "MCP foundry."
- Build the Continuity lens (`signature_alg` grader + items) — then and only then say four axes.
- Standards window, all free: align ledger fields to prEN 18229-1; file the IETF AAT comment (`draft-sharif-agent-audit-trail`) before its deadline.
- Arena: extract `SCENARIOS[]` from the POC into `packs/eu-ai-act.json`; extract the canvas-node component as a shared module so arena and globe are **one renderer**.

### M3+ (Q4) — ONLY AFTER FOUR CLEAN WEEKLIES
Swarm spec build (tunnels/WireGuard, CI ship gates, drift pipeline). Insurer pilot. Regulator tooling as a *view* on existing data, not a new product.

---

## 11. THE ONE OPEN EMPIRICAL QUESTION

Three-legs-for-capability is **undemonstrated across every axis you could actually run** — vendor diversity was a floor artifact, diet diversity refuted at ρ=0.756 with gain 0.0, architecture untested because every SSM/RNN leg failed to load or was incompetent.

Not failed. Undemonstrated. One door left: a competent, loadable non-transformer. Recommended attempt: **RWKV-7 via GGUF / llama.cpp on Metal** — GGUF sidesteps the checkpoint-shape problem and RWKV is a larger architectural jump than Mamba with cleaner instruct checkpoints.

**Gate: n_eff ≥ 2.0 of 3 before any quorum claim is reinstated anywhere.** If ρ stays high with a competent non-transformer, retire the quorum permanently. Either result closes the question — and closing it is worth more than leaving it open.

---

## 12. THE METRIC THAT MATTERS

Not repos. Not domains. Not agents. Not axes.

**Four consecutive clean weekly SOV SIGNAL releases, and one paid signed receipt a customer can verify offline.**

Hit those two and the same corpus that currently reads as a confession reads instead as the most credible seed-stage technical file an assurance investor has opened. Miss them and none of the rest of this document matters.

---

## APPENDIX — WHAT I COULD NOT VERIFY

Flagged, not inferred. Do not build on these until checked against a primary source:

TurboFieldfare · Kimi K3 (2.8T) and its 1-bit quantisation · DeepSeek V4 Pro · SOOFI · LongCat-2.0 · Meta Muse Spark · Inkling / Thinking Machines · "WWDC 2026 MLX distributed" · REAP expert pruning · Neurokernel-as-hive-architecture · the entire July-2026 model leaderboard table · Graft (@nanonets) · BrowserOS · Meta IWSDK · Lightning.js/Blits for TV · Unbrowse/Kuri · Oracle always-free GPU tier · Cisco 360 partner economics · the €10B EU gigafactory figure · AXIS C-Score · the April-2026 benchmark-gaming scandal.

Also unverified from this session: the local Mac files; the exact current state of the NVIDIA PR; whether `csoai/pqcbench` ships a working lens or only a dataset.
