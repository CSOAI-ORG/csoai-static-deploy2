# arXiv Abstract — GovBench (draft, for submission)

## Title
**GovBench: A Byzantine-Fault-Tolerant Benchmark for Sovereign AI Governance**

## Abstract
AI governance today relies on benchmarks that are self-reported, unscored, or
ungrounded — a model card may claim safety with no verifiable method, and a
certificate expires the moment the underlying regulation changes. We present
GovBench, an open benchmark and dataset for evaluating AI governance
resilience that is *signed*, *deterministic*, and *regulation-anchored*.

GovBench evaluates a candidate model through a **33-member Byzantine Fault
Tolerant (BFT) safety council** that must reach a 22/33 supermajority before
any verdict is recorded. Every verdict is chained into a **SIGIL Ed25519
attestation hash-chain**, making the evaluation tamper-evident and
independently verifiable offline: flipping a single byte invalidates the
chain (measured across 27 chained records).

The benchmark battery contains **76 closed items — 57 harmful and 19 benign —
across five adversarial classes**: prompt injection, EU AI Act Article 5
prohibited practices (including social scoring), emotion recognition,
biometric categorisation, and encoded harmful requests. Scoring is
**deterministic with no LLM-as-judge**: refusal, compliance-leak, and
over-block rate are computed by explicit rules, with a no-silent-fallback
principle — a response the grader cannot parse is `UNMEASURED`, never
counted as a pass.

**Results (n = 76 items, RunPod A40):** the 3B-class model family reaches
100% harmful-detection with 0% over-block under the council protocol.
Further, we report the effect of training-data composition on gate
behaviour: an all-refusal LoRA over-blocks 50.0% of benign requests;
adding benign anchors cuts over-block to 35.7%; and a hybrid charter-plus-
weights composition reaches **0.871 refusal, 0.000 compliance-leak, and
0.214 over-block**, the best measured operating point.

Finally, we describe the **hybrid post-quantum extension**: SIGIL links can
be emitted with parallel Ed25519 + ML-DSA-44 (COSE -44) signatures, passing
all five PQC-readiness criteria (algorithm agility, hybrid container,
RFC 3161 timestamp slot, RFC 4998 renewal slot, PQC option) at the measured
cost of a 5.4 KB per-link manifest increase. GovBench is released open
(Apache-2.0) with the dataset, harness, and ledger.

## Key measured numbers (all from on-disk artifacts)
| Quantity | Value | Source |
|---|---|---|
| 3B models harmful-detection / over-block | 100% / 0% | govbench dataset card (RunPod A40) |
| care battery | 76 items (57 harmful / 19 benign) | care_gate_eval.json |
| composed gate refusal / leak / over-block | 0.871 / 0.000 / 0.214 | refusal_axis.json (3 retained runs) |
| all-refusal LoRA over-block | 0.500 → 0.357 (anchors) | refusal_axis.json |
| SIGIL chain tamper test | 1-byte flip invalidates; 27/0 links | chain verify |
| PQC hybrid (Ed25519+ML-DSA-44) | 5/5 criteria, +5,360 B per link | sigil_pqc_measure.json |
| manifest-size impact | 547 B → 5,907 B (+980%) | sigil_hybrid_measure.json |

## Honesty notes (must stay in the paper)
- n = 76 battery items; the 3B 100% figure is on this closed battery, not a claim of universal safety.
- UNMEASURED is a first-class outcome; nothing unparseable counts as a pass.
- The estate is a measurement body: it scores, it does not certify, and no
  score here is a legal opinion.
