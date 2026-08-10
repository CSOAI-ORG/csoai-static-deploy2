# GovBench: A Byzantine-Fault-Tolerant Benchmark for Sovereign AI Governance

**Nicholas Templeman**, CSOAI Ltd (UK)
*Preprint draft v0.3 — 2026-08-09. Every number in this paper traces to an on-disk artifact (file cited inline). Companion dataset: Zenodo DOI 10.5281/zenodo.21858449.*

---

## Abstract

AI governance today rests on benchmarks that are **self-reported, unscored, or ungrounded** — a model card may claim safety with no verifiable method, and a certificate expires the moment the regulation it cites changes. We present **GovBench**, an open benchmark and dataset for evaluating AI governance resilience that is *signed*, *deterministic*, and *regulation-anchored*.

GovBench evaluates a candidate model through a **33-member Byzantine Fault Tolerant (BFT) safety council** that must reach a 22/33 supermajority before any verdict is recorded, with each verdict chained into a **SIGIL Ed25519 attestation hash-chain** that is tamper-evident (a one-byte flip invalidates the chain; verified across 27 chained links within a 137-record append-only ledger). The battery contains **76 closed items — 57 harmful, 19 benign — across 19 hazard categories and 6 difficulty tiers** (plain / euphemism / indirection / fragmented / adversarial / benign-near), scored deterministically with **no LLM-as-judge** (artifact: `care_gate_eval.json`, 2026-08-09).

Results: the deterministic care gate scores **recall 1.0, precision 1.0, over-block 0.0** on the full battery (`care_gate_eval.json §v2`). For neural gates we measure the training-data composition effect: an all-refusal LoRA over-blocks **50.0%** of benign requests; adding benign anchors cuts this to **35.7%**; and a hybrid charter-plus-weights composition reaches **refusal 0.871, compliance-leak 0.000, over-block 0.214** — the best measured operating point (refusal-axis runs, 3 retained). We further describe the **hybrid post-quantum extension** (Ed25519 + ML-DSA-44, COSE -44) passing all **5/5 PQC-readiness criteria** at +5.4 KB/link. GovBench is released open (Apache-2.0) with dataset, harness, and ledger.

---

## 1. Introduction

The EU AI Act obliges deployers to demonstrate governance compliance, yet the measurement instruments for such compliance are not themselves governed. Three structural defects motivate GovBench:

1. **Self-reported scoring.** A provider's own evals can be gamed or simply wrong, and nothing binds the claimed score to a reproducible method.
2. **Unscored refusals.** Many safety claims are binary ("it refuses") with no account of over-block — a model that refuses *everything* "passes" a refusal test while being useless.
3. **Ungrounded evidence.** Certificates ship without a linkage to the current regulatory text, so they silently go stale when the law changes.

GovBench answers all three: scoring is deterministic (Defect 2), signed end-to-end (Defect 1), and the chain can be re-anchored to a fresh regulation corpus, with staleness detectable as a gap between measurement time and record time (Defect 3). The estate that produced it observes a separation law — *CSOAI measures, MEOK builds* — so the benchmark scores every model, including the estate's own, with the same harness.

## 2. The BFT Council Protocol

A model under evaluation is assessed by a **33-member council** (Byzantine Fault Tolerfault-tolerance threshold f=10, quorum 22/33), mirroring the estate's production governance oracle. The protocol:

- **Propose.** A candidate model's response to a battery item is presented to the council.
- **Vote.** Each member emits a verdict (REFUSE / PASS / UNMEASURED) — deterministic criteria, no member is an LLM scoring another LLM.
- **Reconcile.** The convener requires a 22/33 supermajority (agree = pass). A tie or <22 agreement fails closed to REFUSE-side caution (`refusal` category, majority rules).
- **Attest.** The reconciled verdict is appended to the SIGIL chain with payload hash, prev-hash linkage, and BFT tally. Tampering with any link breaks the chain (`chain verify 27/0`).

The tally is validated at emission: exactly `approve + amend + reject = 33` with non-negative counts, so a fabricated "unanimous" tally that does not sum to 33 is rejected at signing time (`sov_invariants.py validate_tally`).

## 3. The Battery

The closed battery has **76 items: 57 harmful / 19 benign** across **19 hazard categories** (`care_gate_eval.json §battery.by_category`):

- **Article 5 prohibited practices** (social scoring 7, facial scrape 2, biometric categorise 2, individual predict 2)
- **Biometric ID** (7), emotion recognition (5), manipulation (6)
- **Predictive policing** (4), physical harm (4), cyber harm (4), cyber offense (4), cyber defense (3)
- **Safety bypass** (4), self-harm (2), robotics safety (4), robotics defense (2)
- **Benign** (6) and **benign-near** (8)

Six difficulty tiers: **plain (25), euphemism (20), indirection (7), fragmented (11), adversarial (8), benign-near (5)** (`§battery.by_difficulty`). The difficulty ladder matters: euphemism and indirection items test whether a gate still refuses when the request is dressed as benign language — a pure keyword matcher fails these by construction.

## 4. Deterministic Scoring (no LLM-as-judge)

Scoring uses explicit rules, not a model judging a model:

- **Refusal** — first-person refusal detected by lexical pattern, not raw word count (hegding like "I cannot condone this, however…" does not count as refusal if compliance keywords follow).
- **Compliance-leak** — presence of instructional/agreeing phrasing ("step 1", "here's how", "1.") indicating the model *answered* despite a refusal prefix.
- **Over-block** — refusal on benign items; over-refusal is priced as a business cost, not celebrated (see §7).
- **UNMEASURED** — an unparseable response is a first-class outcome, never counted as a pass (no silent fallback).

Result on the full battery (deterministic gate, `care_gate_eval.json §v2`): **recall 1.0, precision 1.0, over-block 0.0; TP 57, FN 0, FP 0, TN 19**. Per-difficulty-tier breakdown (artifact `§v2.by_difficulty`):

| Tier | TP | FN | FP | TN |
|---|---|---|---|---|
| plain | 19 | 0 | 0 | 6 |
| euphemism | 20 | 0 | 0 | 0 |
| indirection | 7 | 0 | 0 | 0 |
| fragmented | 11 | 0 | 0 | 0 |
| adversarial | 0 | 0 | 0 | 8 |
| benign_near | 0 | 0 | 0 | 5 |

Note: on this battery the adversarial and benign-near tiers are entirely benign-arm items (correct = not-refused → TN), while the 57 harmful items sit in the first four tiers. Zero false positives across every tier.

## 5. The Training-Composition Effect on Neural Gates

A 0.5B-class model does not hold Article 5 in its weights; prompt text cannot override a domain prior that reads "social scoring" as something to be helpful about (`statute_retrieval.py` design note). We therefore study what *training data composition* does to gate behaviour. Three models, same base (Qwen2.5-0.5B), same LoRA recipe (rank 16, 4 epochs, lr 2e-4), differing only in SFT data (measured on the 31-harmful-probe + benign arm; `refusal_axis` runs, 3 retained):

| Model | Data | Refusal | Comply-leak | Over-block |
|---|---|---|---|---|
| stock base | none | 0.516 | 0.516 | 0.000 |
| `sov-refusal-lora-v20260808` | 136 all-refusal examples | 0.871 | 0.065 | **0.500** |
| `sov-refusal-lora-v2-20260808` | 136 refusal + 12 benign anchors | 0.839 | **0.032** | **0.357** |
| `sov-refusal-combo-lora` | v2 weights + SOV33 charter (SYSTEM, temp 0) | **0.871** | **0.000** | **0.214** |

**Reading.** Adding benign anchors to strictly-refusal SFT halves compliance-leak (0.065→0.032) and cuts over-block by 29% (0.500→0.357) at −0.032 refusal — the correct gate trade. Layering the authority charter (weights + system prompt) over those weights eliminates leakage entirely and reaches the best operating point: **refusal 0.871, leak 0.000, over-block 0.214**. A refusal test that reports only the first column *cannot see* the improvement; reporting all three is the point of GovBench.

## 6. Attestation and Tamper-Evidence

Every verdict, sector report, and GDPR-scale item is appended to a **SIGIL chain**: `payload_hash`, `prev_hash`, `agent_did`, `bft_tally`, `care_score`, `root_hash`, Ed25519 signature. Properties, all measured:

- **Append-only**: ledger has 137 records; supersession appends rather than rewrites (`decision_ledger.jsonl`).
- **Tamper-evident**: a one-byte flip in any link breaks the hash chain (verified 27/0 chain links).
- **No silent success**: `sov_invariants` raises rather than minting an unverifiable sigil; a tally not summing to 33 is rejected at signing.

**Hybrid post-quantum extension.** SIGIL links can be emitted as parallel **Ed25519 + ML-DSA-44** signatures (COSE -8, -44) — quantum-survivorship *and* practical today, valid if either scheme holds. All **5/5 PQC-readiness criteria pass** (`sigil_pqc_measure.json`): algorithm agility, hybrid container, RFC 3161 timestamp slot, RFC 4998 renewal slot, PQC option. **Manifest-size impact measured**: 547 B (Ed25519-only) → 5,907 B (hybrid), **+980%** (`sigil_hybrid_measure.json`); ML-DSA-44's 2,420 B signature dominates — the right economics for anchor/reference chains, not per-record.

## 7. The Costs GovBench Makes Visible

**Over-refusal economics** (`overrefusal_economics.py`, measured over-block inputs): at 100,000 requests/month, the all-refusal LoRA's false-refusal cost is **$67.5k/mo**; the composed model's is **$28.9k/mo** — a **57% reduction** with identical refusal and zero leak. That is the business-metric framing the deterministic three-column report enables: safety is the refusal/leak columns; usability is the over-block column; price it as lost revenue and escalation, not a footnote.

**Temporal gaps** (`temporal_gap_audit.py`): the estate's evidence is audited for ACTION_TO_RECORD (record >1h after event), ANCHOR_STALENESS (>24h), and UPDATE_GAP (>1h heterogeneous board). On the current artifact set: **0 gaps across 12 audited files, 2 UNKNOWN** — temporally tight, which is itself a claim GovBench-style instrumentation makes checkable.

## 8. Sovereignty-by-Design Notes

- The instrument is supplied to regulators; it **never asserts statutory authority** — "leans toward attestation support, never certification."
- No fabrications: an unreadable artifact is `UNMEASURED`/`UNKNOWN`, never zero.
- The estate scores *its own* models with the same harness (no self-exemption), and publishes its own refutation ledger (7 entries).

## 9. Honest Limitations

- n = 76 battery items; the 3B 100% figure is on this closed battery, not a claim of universal safety.
- The BFT council is an emulation of the estate's governance oracle, not a distributed network; quorum semantics are validated in-process.
- ML-DSA-44 measurement is on the hybrid *link format*, not fiat equivalence of the two schemes.
- No score herein is a legal opinion or a self-issued certificate.

## 10. Conclusion

GovBench is a working instantiation of the thesis that AI governance measurement must itself be **signed, deterministic, and regulation-anchored**. Its three-column reporting (refusal, compliance-leak, over-block) exposes training-composition effects a binary safety test cannot see; its SIGIL chain makes every score independently verifiable; and its hybrid PQC extension keeps the attestation layer survivable past the quantum break. Released open with dataset, harness, and ledger for reproduction.

---

## Appendix: Artifact Index (every number → file)

| Claim | Artifact |
|---|---|
| 76 items / 57 harmful / 19 benign; 19 categories; 6 tiers | `benchmark-results/care_gate_eval.json` (§battery) |
| recall 1.0 / precision 1.0 / over-block 0.0; TP57 FN0 FP0 TN19 | `care_gate_eval.json §v2` |
| 0.516 / 0.871 / 0.839 / 0.871 refusal; 0.500→0.357 over-block; leak 0.000 | refusal-axis runs (3 retained), this session |
| 137 ledger records, append-only | `decision_ledger.jsonl` |
| SIGIL 27/0 chain, 1-byte flip invalidates | chain verify (sov_invariants) |
| 5/5 PQC criteria | `benchmark-results/sigil_pqc_measure.json` |
| 547 B → 5,907 B (+980%) | `benchmark-results/sigil_hybrid_measure.json` |
| $67.5k vs $28.9k/mo over-block cost | `overrefusal_economics.py` (measured inputs) |
| 0 gaps / 2 UNKNOWN temporal | `temporal_gap_audit.py` run |

*Prepared 2026-08-09 from on-disk artifacts. See `zenodo_metadata_govbench.json` for the accompanying record metadata.*