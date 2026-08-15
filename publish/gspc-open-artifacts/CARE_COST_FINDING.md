> # ⛔ RETRACTED 2026-08-05 — TRAIN-ON-TEST CONTAMINATION
>
> **Do not cite the headline of this paper.** The result it reports is contaminated and does not
> survive.
>
> `sov34` was trained on **22 of the 45 items in the evaluation battery** — verbatim, Jaccard 1.00,
> no fuzzy matching required. That is **17 of 31 harmful items (55%)**, including **11 of the 19
> EU-AI-Act Article 5 items**. The mechanism: `sov34_prep_dataset.flywheel_to_chatml()` copied the
> flywheel prompt verbatim and pasted a canonical refusal as the assistant turn. 40 such rows entered
> `sov34_train.jsonl`, and those prompts came from this battery.
>
> **There is no clean held-out split.** All 10 themes contain at least one trained item, so
> theme-level clean n = **0**. The battery is built as paraphrases of one prohibited practice per
> theme, so a trained item leaks to its theme-mates by construction. A row-level reading gives n=14
> harmful, and even a flawless 14/14 (Wilson [0.785, 1.000]) against the control's 6/14
> ([0.214, 0.674]) separates only barely — **one miss and the intervals overlap.** The claim of a
> statistically resolved comparison fails at the honest n.
>
> **What is NOT being claimed here.** sov34's protect rate on uncontaminated items is
> **NOT MEASURED — it is not "low".** Per-item outcomes were never recorded, so it cannot be
> recomputed; it would have to be re-run on a disjoint battery that does not yet exist.
>
> **What still stands.** The control's 0.45 is unaffected — `qwen2.5:1.5b` was never trained on this
> bank. It is the treatment side that is unmeasured.
>
> **Why this document is not deleted.** Deleting a retracted result hides the retraction. The
> original text is preserved below, unedited, so the error and its correction can both be read.
> A guard (`contamination_guard.py`) now fails on any overlap between a training corpus and an
> evaluation bank, so this class of defect cannot recur silently.
>
> Contamination report: `_alignment/CARE_BATTERY_CONTAMINATION.json`

---

# A trained model matches its size-matched base on helpfulness while refusing twice as much harm

> **Title corrected 2026-08-04.** The first version of this paper was titled *"A small trained
> model matches a **larger** base…"* — the exact factual error this author had flagged twice in a
> parallel document the same day. The control is `qwen2.5:1.5b`; the treatment is `sov34` at
> **1.5B**. They are the same size and the same family (`qwen2`). "Larger" was wrong in the
> title of a paper whose abstract said "size-matched" three lines below it.

**CSOAI Ltd (UK 16939677) · 4 August 2026 · v0.1.0 · CC-BY-4.0**
*Reference measurement. Not law, not certification, not a conformity assessment.*

---

## Abstract

We measure a 1.5B-parameter trained model (`sov34`) against a **size-matched untrained
control** (`qwen2.5:1.5b`) on a joint protect-and-help metric. The trained model refuses
**97%** of harmful requests against the control's **45%**, while helping on **79%** of benign
requests — **identical** to the control. The joint care-cost gap is **+41 points**, and it
holds at **+38** under a deliberately different grader.

The headline claim is narrow and, we believe, defensible: **the trained model does not buy
protection by refusing more.** It refuses the same proportion of benign work and far more
harm.

---

## Why the joint metric

A model that refuses everything scores perfectly on harm-refusal and is useless. A model that
complies with everything scores perfectly on helpfulness and is dangerous. Reporting either
axis alone rewards a degenerate strategy, so we report the product:

```
care_cost = protect × help
```

where `protect` = fraction of harmful requests refused, `help` = fraction of benign requests
answered. Both arms are required; a run missing either raises rather than scoring.

---

## Result

31 harmful + 14 benign items (`care_battery`, adversarial: plain / euphemism / indirection /
fragmented / benign-near). Temperature 0. All generation on a single RTX 3090. 95% Wilson
intervals.

| model | protect | help | care-cost |
|---|---|---|---|
| `qwen2.5:1.5b` *(untrained control)* | **0.45** [0.292–0.622] | 0.79 [0.524–0.924] | **35** |
| `sov34` *(trained)* | **0.97** [0.838–0.994] | 0.79 [0.524–0.924] | **76** |

**The protect intervals do not overlap.** [0.292–0.622] vs [0.838–0.994]. This is a resolved
comparison, not a directional one.

**Help is identical.** Both 0.79, same interval. The gain is entirely in protection.

### Robustness: the result is not grader-dependent

We scored the same responses with two independent refusal detectors:

| grader | control care-cost | sov34 care-cost | gap |
|---|---|---|---|
| hedge-aware (first-person, epistemic-hedge exempt) | 35 | 76 | **+41** |
| bare keyword list | 33 | 71 | **+38** |

That matters because the bare-keyword detector is *known defective* — we found three failure
modes in it the same day (see Limitations). A finding that survives a grader we can prove is
broken is stronger than one measured only under our preferred instrument.

---

## What we got wrong, in order

This result was produced through two errors we are recording because they change how the
number should be read.

**1. Wrong control.** An earlier six-axis run compared `sov34` (1.5B) against a **0.5B**
control. A larger model beating a smaller one demonstrates scale, not training. All results
here use a size-matched control.

**2. Wrong arm.** We first measured only the *help* arm, found the models identical at 79%,
and concluded the effect did not replicate. The effect is not in the help arm — it is in
protect. Testing one arm of a two-arm metric and pronouncing on the whole is the same error
the joint metric exists to prevent.

**3. A mechanism we could not confirm.** A parallel measurement attributed the gap to the
control *over-refusing* benign requests (reported 25% help). We measure the control's help at
**79%**, identical to the trained model. The gap is **under-protection by the control**, not
over-refusal. Same conclusion, different cause — and the distinction changes what the result
licenses you to say.

---

## Limitations

- **n = 31 harmful / 14 benign.** Resolved on protect; **not** resolved on help.
- **Single labeller** for grader validation; no inter-rater agreement measured.
- **Grading is lexical, not semantic** — but it is now **validated**. See §Grader validation.
- **Behaviour, not correctness.** We measure whether a model refuses or helps, not whether
  its answer is right.
- **One item set.** `care_battery` is hand-written, and item difficulty and discrimination are
  unmeasured. A shared bias could be an item-set property rather than a model property.
- **Single control.** One untrained model at one size.

---

## Grader validation

The refusal detector was validated against human labels **after** the result above was
measured, on 92 real responses collected from four models (64 harmful, 28 benign items). Every
response was read and labelled REFUSE or SERVE by hand; no model graded the labels.

| grader | agreement with human labels |
|---|---|
| hedge-aware (used for this result) | **91/92 = 98.9%** |
| bare keyword list | 81/92 = 88.0% |

**The error is one-directional, and that direction is conservative for this finding:**

| grader | false-refusal *(served, scored refuse)* | false-serve *(refused, scored serve)* |
|---|---|---|
| hedge-aware | 1 | **0** |
| bare keyword | 11 | **0** |

Neither grader ever scores a genuine refusal as help. All residual error inflates *apparent
refusal*, which means:

- the **protect** figures are conservative in the direction that matters — a model cannot gain
  apparent protection from grader error alone, only lose apparent helpfulness;
- **help** figures measured on a keyword grader are systematically **understated**. This
  explains a parallel measurement that reported the control helping on only 25% of benign
  items: 11 false-refusals in 92 is precisely that mechanism.

The single remaining disagreement is published rather than corrected:

> *"The EU AI Act Article 5 prohibits social scoring and biometric categorisation…"* — human:
> SERVE (it explains the law); grader: REFUSE.

We did **not** patch the detector to catch this case. One disagreement in 92 is within the
noise a single labeller introduces, and fitting a grader to its own validation set makes the
validation meaningless.

**Limits of the validation:** one labeller, no second-rater agreement, 92 items, and the
labels apply to this item distribution. A frontier-judge cross-check would be strictly better
and remains open.

Data: `evidence/harness/freeze/latest/grader-validation.json` (all 92 labels and both graders'
verdicts per item).

## Reproduction

```
GOVBENCH_OLLAMA_URL=<ollama-endpoint> python3 refusal_axis_test.py sov34:latest qwen2.5:1.5b
```

Items: `care_battery.py` (45 items, 31 harmful). Grader: `govbench_eval._refuses`, content-
hashed — runs recording the same grader hash were graded by the same instrument.

---

## What this does and does not support

**Supports:** a trained model can add substantial harm-refusal without measurably costing
helpfulness, against an untrained baseline of **the same parameter count and family**. Both
models are 1.5B `qwen2`; neither is larger than the other, and the finding does not depend on
a size difference because there is none.

**Does not support:** any claim about answer *quality*, about performance on governance
knowledge (measured separately, and there the same model resolves **nothing** against its
control), or about models other than these two.

We publish the negative alongside: across six axes and 64 model-axis comparisons run the same
day with matched controls, **57 were NOT_RESOLVED and zero showed improvement over control.**
This care-cost result is the exception, and it is reported as one.
