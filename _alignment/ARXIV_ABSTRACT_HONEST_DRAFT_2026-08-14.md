# arXiv abstract — HONEST reframe (draft for owner + counsel review)

**Why this file exists:** the prior draft (`ARXIV_ABSTRACT_GOVBENCH.md`) is titled
*"A Byzantine-Fault-Tolerant Benchmark…"* and leads with a **33-member BFT / 22-of-33
supermajority** claim. That claim was **retracted** — measured effective independence is
**n_eff ≈ 1.21 of 3 nominal legs** (`_alignment/QUORUM_RETRACTION_2026-07-29.md`; CLAUDE.md:
"Council info — NOT Byzantine fault tolerant"). **Submitting the BFT framing would publish a
known-false claim.** This reframe leads with the result that is actually measured and defensible:
the price of over-refusal, on a signed, deterministic, self-refuting benchmark.

> ⚠️ OWNER/COUNSEL GATE — do not submit until: (1) the over-block cost figures are confirmed as
> *modeled from measured inputs*, not observed market outcomes; (2) the word "benchmark/index" is
> cleared against IOSCO/EU-BMR scope if the paper is later tied to a commercial signal; (3) no
> "certified/compliant" language anywhere.

---

## Title (proposed)
**GovBench: Deterministic, Signed Measurement of AI-Governance Behaviour, and the Measured Price of Over-Refusal**

## Abstract (draft)
AI-governance benchmarks today are largely self-reported, unscored, or ungrounded: a model card
may assert safety with no verifiable method, and a compliance claim can outlive the regulation it
rests on. We present **GovBench**, an open benchmark that measures model behaviour on
control-anchored governance axes with three properties that current benchmarks lack. **(1)
Deterministic grading** — no judge model; every item is scored by exact rule, so results are
reproducible bit-for-bit. **(2) A first-class UNMEASURED state** — items the model refuses or
answers uninterpretably are reported as UNMEASURED, never silently coerced to zero, so the score
cannot flatter the system by counting non-answers as failures or successes. **(3) Grounded legal
claims** — every statutory citation is checked against an exact registry, and an answer that cites
a non-existent or mis-attributed article cannot pass as verified (a wrong answer cannot carry a
clean receipt). Results are Ed25519-signed and independently re-computable.

Using GovBench we quantify **over-refusal as a business cost** rather than a footnote. A safety
tuned model that refuses benign requests incurs measurable lost-revenue and escalation cost.
Modeled from measured over-block rates at 100,000 requests/month, an all-refusal baseline carries
a **$67.5k/month** false-refusal cost, while a composed model achieves the **same refusal rate and
zero harmful leakage at $28.9k/month — a 57% reduction**. We further show the measurement resists
Goodharting: improvement is gated on a held-out probe split the model never trains on
(anti-Goodhart discipline; leak-free on a 19/19 live self-test).

We release the harness, the frozen probe banks, and the signed result cards, so any party can
re-compute and verify every number in this paper.

## Explicitly REMOVED from the prior draft (do not reintroduce)
- The "33-member Byzantine-Fault-Tolerant safety council" and "22/33 supermajority" framing.
  Measured n_eff ≈ 1.21 of 3 → the council is **not** BFT; a voting-independence claim is false.
- Any "certificate / certified / guarantees compliance" language.

## Honest hedges to keep in the paper
- The $67.5k / $28.9k figures are **modeled** from measured over-block rates, not observed P&L.
- "Composed model" gains attribute to deterministic layers; per-dimension routing and statute
  retrieval were measured and did **not** beat a single good model — report that, it strengthens
  credibility.
