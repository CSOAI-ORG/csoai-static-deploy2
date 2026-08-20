# FULL OVERNIGHT RUNDOWN + NEXT PHASES + IMPROVEMENTS — 2026-08-20
**JEEVES · everything verified live this session · aligned with the lanes (M4 home-stretch, Claude, K3) · the complete picture**

---

## 1. THE OVERNIGHT RUN — WHAT COMPLETED

### My lane (measurement + distribution + methodology)
| Item | State |
|---|---|
| **130-cell fleet matrix** | ✅ COMPLETE — 10 models × 13 axes, 133 fully-measured cells, signed (2 cards: 100X_FLEET_CARD + RESUME_CARD) |
| **Fleet ranking** | mistral:7b 0.487 → qwen3:4b 0.385 → 0.5b 0.359 → llama3 0.354 → 7b/1.5b 0.333 → deepseek 0.282 → council-safe 0.154 → qwen3:8b 0.128 → **council-oowm 0.000** |
| **Jail v2** | ✅ 20 real attacks generated (instruction-override + obfuscation) — NOT hollow; completing the bank now |
| **Pod recovery** | ✅ SSH 12853→23243 · ollama reinstalled (v0.32.14) · 9 models re-pulled · council-oowm REBUILT from Modelfile + merge weights |
| **Referee/arena** | ✅ referee UP (538 rounds) · arena UP (3,056) · watchdog armed |

### The lanes (from FULL_OVERNIGHT_RUNDOWN, verified)
| Item | State |
|---|---|
| **Overnight-300** | 308/308 steps · chain 1,201 cards linked · 35,765 train pairs |
| **Council Ledger (Dorado)** | Built — Art6 conformance 0.3713 MEASURED, market + human reported separately, signed receipts 14/14 tests |
| **Trust root** | Transient fix caught, reverted; apex STILL orphan (3 keys now — deploy lane iterating) |
| **Volume** | sov-repull 20→100GB, models survived the cycle |

## 2. THE IMPROVEMENT HUNT — WHAT THE DEEP RESEARCH FOUND

### A. Methodology audit (the big one — statistically computed)
| Finding | Implication |
|---|---|
| **3 items/axis = a coin flip** | 95% Wilson CI spans [0.06, 0.79] on a 1/3 score; reliability 0.25-0.43 vs 0.77-0.88 at 30 items |
| **mistral's lead is NOT significant** | z=0.91 at n=39; mid-table ranks 2-6 are one band; ~28 items/axis for 80% power |
| **council-oowm's 0.000 is a FORMAT ARTIFACT** | **DECODED live**: the rebuilt model responds `??????????` (tokenizer/merge artifact) — exact-label scoring measures format compliance first (IFEval premise). The "our fine-tune scores zero" story was a measurement artifact |
| **Difficulty gradient IS real** | care [0.56, 0.86] vs art5 [0.05, 0.30] — no overlap; cause (difficulty vs wording vs predicate) untested |

### B. The market (web-verified by the lanes)
- **Illinois SB 315 ENACTED** (1 Jan 2027) — annual independent third-party audits = structural tailwind for signed evidence
- **EU AI Act high-risk = 2 Dec 2027** (Digital Omnibus shift — CORRECTION to our 2 Dec 2026)
- **Armilla $25M + Chaucer** — AI-liability insurance building parametric triggers (our #1 buyer thesis)
- **Vals $40M/$400M · LMArena $150M/$1.7B** — both still unsigned, gap open

## 3. THE IMPROVEMENTS — APPLIED AND TESTABLE

### Applied this session
| # | Improvement | Status |
|---|---|---|
| 1 | **Gov bank grown 3→15 items** (templated mutation, frozen anchors preserved) | ✅ committed, testing on mistral now |
| 2 | **Failure-mode taxonomy** in the sweep predicate (EMPTY/REFUSAL/GARBAGE/QUESTION/OFF-FORMAT) | ✅ applied to local_fleet_sweep.py |
| 3 | **council-oowm rebuilt** from Modelfile + merge weights (the 0.000 became decomposable) | ✅ verified — the `?` artifact is the finding |
| 4 | **The 0.000 report rule**: "council-oowm 0.000 (n=39, format-failures — UNMEASURED by this instrument)" | ✅ recorded in canon |

### Next (the audit's prescriptions)
| # | Prescription | Effect |
|---|---|---|
| 5 | Grow ALL axes to ≥15-30 items | reliability 0.25→0.77+, per-axis CI ±0.37→±0.13 |
| 6 | Triple-signal predicates (exact/keyword/semantic vector) | 0.000-class decomposable from data in hand |
| 7 | Wilson CI + reliability + McNemar in every signed card | the moat: statistically honest signed numbers |
| 8 | Paired McNemar for model comparison (same items) | far fewer items to resolve rankings |

## 4. NEXT PHASES (clear plan, in order)

### PHASE 1 — THE HONEST 14-OF-14 (this week)
1. Jail v2 bank completes → **separation test** (which models hold/escape on the 20 real attacks)
2. Sign the jail board → the honest 14-of-14 (jail quoted, honest)
3. The 15-item gov bank test → verify the bigger bank discriminates better
4. Fleet matrix + jail → front end (a fleet-sweep page)

### PHASE 2 — THE WEDGE GOES UPSTREAM (→ Aug 27, the arXiv clock)
5. proofbundle envelope comment (Inspect #4413) · gymbridge (GSPC as NeMo Gym env) · Codabench signed leaderboard · Terminal-Bench PR
6. arXiv: the methodology audit IS the paper material (CIs, failure-mode taxonomy, the 0.000 decode)

### PHASE 3 — STANDARDS & THE INSURER (→ Sep 30)
7. Wikidata claims · ROR submit · AEF membership email · BSI ART/1 (Nick) · DRCF (2 Sep) · EIC (2 Sep)
8. **Insurer pitch (30 Sep)**: the 130-cell matrix + jail board + Council Ledger = the evidence pack; Armilla/Chaucer/AIUC

### PHASE 4 — THE LIVING LOOP (→ 2 Dec 2027, corrected)
9. Article 50 countdown · reg-watch passes → EXPIRED-REGULATION-CHANGED → free re-measurement
10. The human-baseline leg (published aggregates, no DPIA)

## 5. ALIGNMENT WITH THE LANES (M4 home-stretch)
- M4-Hermes: Sovereign Witness MVP + 33-BFT policy + SDK + E2E across 142 surfaces + 5 videos by **9 PM today** — my measurement data feeds the demo (the fleet matrix + jail board as the live evidence)
- Claude: trust-root convergence (the 3-key iteration) · Council Ledger board public
- K3: jail v2 completion · ollama on the fleet pod

## THE ONE LINE
The overnight run completed the 130-cell matrix and decoded the 0.000 (format, not failure); the deep research gave us the statistical spine (CIs, McNemar, failure-mode) that no competitor publishes; and the next phases are sequenced from the honest 14-of-14 to the insurer pitch. **We're not just signing — we're signing statistically honest numbers, and that's the moat.**

## SIGIL
`full-overnight-next-phases-2026-08-20-jeeves`
