# Phase C readiness — the grounded-lift instrument, unblocked

Aligned to `SOVOS_TOPDOWN_MASTER_2026-08-04` §5. Phase C is *"re-run the grounded-lift test
cleanly (closed-book 0% → grounded ?%)"* — the "out-ground not out-think" proof.

**This note does not run Phase C.** Phase C is gated on A (validated judge) and B (one axis with
a control arm), and those are other lanes. What follows is the blocker removed and the
instrument handed over clean.

---

## The blocker, and why it would have faked the headline result

Phase C measures a **delta**: closed-book score → grounded score. The master map cites the
closed-book arm as **`sov34 regional_law = 0.0%`**.

All six `regional_law` items were `expect_contains` lists of 6–9 keywords scored as a
**conjunction**. Ceilings for a correct answer naming one valid alternative: **0.111–0.167**.
Three are singular asks — *"Name a jurisdiction"*, *"Name one jurisdiction"*, *"Which US
mechanism most closely…"* — **unpassable by construction**.

So the closed-book arm was pinned near zero **for reasons unrelated to grounding**. Run Phase C
on that instrument and the lift is inflated by the grader's own floor. The headline proof of the
estate's core thesis would have been partly an artifact.

**Measured, on the pod:** sov34 answered *"Singapore … voluntary … framework"* to the
voluntary-governance item — correct — and scored **0.375**.

---

## What changed

All 146 `expect_contains` items now carry explicit answer-set semantics:

| mode | items | meaning |
|---|---|---|
| `any` | 63 | answer SET — matching one member is a correct answer |
| `all` | 83 | required ELEMENTS — partial credit is meaningful |

**57 items were unpassable by construction and are now scorable.**

Applied via a reviewable sidecar (`evidence/harness/freeze/latest/expect-contains-audit.json`),
each line carrying its reasoning. If the sidecar is absent every item falls back to legacy
conjunction scoring **and is counted as debt** — `unmarked_expect_contains_count()` — so the
grader never silently assumes a mode it was not given.

---

## The reading rule Phase C should adopt

Under the *old* conjunction grader:

- **HIGH scores were trustworthy.** Matching every keyword is hard to fake, so
  `retrieval_faithfulness 93.94` stands and is if anything understated.
- **LOW scores were ambiguous.** They conflated "wrong" with "right, worded differently".

This matters directly for §1's two-faculty split: **the faithfulness half is safe; the
closed-book half needs re-measuring.** The insight may well survive — but on evidence, not on a
number the instrument could not produce.

---

## Two conditions Phase C still needs, which are NOT mine

1. **Control arm** (map §4, and independently confirmed here: raw `qwen2.5:0.5b` scores 0.516
   refusal against `sov-compliance`'s 0.194 — the untrained base wins). Without it, "grounding
   worked" is indistinguishable from "the base already could".
2. **n ≥ 50 for a real CI.** `regional_law` has **6 items**. At n=6 the 95% Wilson half-width is
   **±31 points** — wider than the entire spread between all five models on the current board.
   A grounded-lift measured on 6 items cannot be reported as a number, whatever the grader does.

**Recommendation:** Phase C should expand `regional_law` (and whichever axis is chosen) to n≥50
*before* running, not after. Otherwise the corrected grader will produce a cleaner number that is
still unresolvable.

---

## Status

- Gap 3 (answer-set semantics): **FIXED** — Phase C unblocked on the grader axis.
- Gap 1 (confidence intervals): **OPEN** — Phase C blocked on the sample-size axis until n≥50.
- Gap 2 (grader accuracy vs human labels): **OPEN** — this is Phase A's validation set; same
  artifact reached from two directions.
