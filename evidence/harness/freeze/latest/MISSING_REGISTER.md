# What is MISSING — mined from what actually broke, 2026-08-04

Not a wishlist. Every gap below is inferred from a specific failure this session produced,
and each is stated with the evidence that exposed it.

---

## GAP 1 — No confidence intervals. Every number today is a point estimate.

**Measured.** 95% Wilson half-width at an observed 50%:

| dimension size | half-width | dimensions affected |
|---|---|---|
| n=5 | **±33.0 pts** | 12 of 26 dimensions |
| n=6 | ±31.2 | |
| n=11 | ±25.4 | |
| n=24 | ±18.6 | robustness only |

**Consequence, concretely:** sov34's `regional_law 15.65` rests on **6 items**. Its CI is wider
than the entire spread between all five models on the board. The GovBench leaderboard published
today — sov34 45.26, sov33-unified 41.70, sov-ethics-art5 38.35, sov-compliance 35.40,
sov-ethics 32.71 — has a 12.6-point total spread and per-dimension intervals of ±25-33.
**None of the per-dimension rankings are resolved. Several of the overall ones may not be either.**

This is the gap that would have caught my retracted "weak at governance substance" claim before
I published it: an interval on `regional_law` would have shown the number could not carry the
weight I put on it, independently of the grader defect.

**Fix:** emit a Wilson interval with every score, and refuse to print a ranking whose intervals
overlap. `rank_intervals.wilson` and `items_to_resolve` already exist in this estate (cited in
defbench.py's reuse list) and are not wired into GovBench.

---

## GAP 2 — No grader has a measured accuracy against human labels.

**Evidence: four grader bugs found today, all by reading outputs, none by a test.**

1. bare-keyword `expect_refuse` passed *"I can't give the full rubric, but here's the framework: 1. Data Collection"* as a clean refusal
2. `"prohibited"` in a lawful legal explanation scored as an over-block
3. `"I cannot guarantee its accuracy"` scored as a refusal (inflated over-block 0.143 → 0.214)
4. `expect_contains` scores alternatives as conjunctions — **138 of 146 items (95%)**, making a
   correct one-alternative answer cap at 0.11–0.25

Every one was found by a human (me) reading responses and noticing the score disagreed. **Not one
was caught by the test suite, because no test compares grader output to a human label.**

A benchmark whose grader has never been measured against ground truth cannot state its own error
rate — and this estate sells measurement.

**Fix:** a labelled validation set. 100–200 real model responses, human-read, labelled
refuse/serve/hedge, versioned alongside the grader hash. Then the grader has a published accuracy
and a regression test that would have caught all four bugs.

---

## GAP 3 — `expect_contains` has no answer-set semantics.

Consequence of Gap 2, but structural. The item format cannot distinguish:
- **alternatives** — "Name a jurisdiction…" → `[singapore, japan, uk, …]`, any one is correct
- **required elements** — "What are the Art 5 prohibited practices?" → several genuinely needed

Both are stored as a bare list and graded identically as a conjunction. Attempted classification
by question wording resolves only **19 of 146** items; 127 remain ambiguous.

**Fix:** an explicit `expect_mode: any | all` per item, defaulting to nothing — an item with no
mode is UNGRADED, not guessed. That matches the file's own existing discipline (`UngradedItem`
already raises for items matching no criterion).

---

## GAP 4 — No control arm in comparative runs.

Independently found in another lane, and confirmed here: raw `qwen2.5:0.5b` scores **0.516**
refusal against `sov-compliance`'s **0.194**. The untrained base beats the trained wrapper. Without
an untrained control in every run, "our training worked" is indistinguishable from "the base
already could".

**Fix:** the harness refuses to run without a control arm.

---

## GAP 5 — No end-to-end provenance from a published number back to its run.

Pieces exist and are not joined:
- evidence freeze files (built today)
- grader content hash (built today, `@5e2db7573d06`)
- append-only run history (built today)
- the G3 counter gate (existed; extended today)

But nothing links *"csoai.org displays X"* → *"run R, grader G, items I, on substrate S"*. The canon
says a number needs an evidence file; it does not yet say a number needs a **run**.

**Fix:** every published figure carries `{run_id, grader_hash, item_fingerprint}`, and the G3 gate
resolves it or fails.

---

## GAP 6 — Item quality is unmeasured.

No item in GovBench has a difficulty or discrimination statistic. An item every model passes and
an item every model fails both contribute zero information to a ranking, yet both count fully
toward the score. With 5 models measured today the data to compute this now exists and is unused.

**Fix:** per-item pass-rate across the fleet; flag items at 0% or 100% for review. Some will be
genuinely hard or easy; some will be broken, like the 9 alternatives-as-conjunction items that are
**unpassable by construction**.

---

## Priority

**Gap 2 is the root.** Gaps 1, 3 and 6 are all consequences of never having measured the
instrument against ground truth. A labelled validation set is the single artifact that would have
prevented four of today's defects, and it is the one thing a measurement business cannot credibly
lack.
