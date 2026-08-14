# Correlated Refusal Failure: When an Entire Model Fleet Gets the Same Safety Call Wrong

**DRAFT — for review before submission. CSOAI (CSOAI LTD, UK 16939677). Not legal advice.**
*Author to submit; this is the drafted manuscript, not a published record.*

## Abstract

Safety leaderboards report a per-model **mean** — how often each model refuses correctly.
A mean is a linear aggregator: a rare item that every model fails together vanishes into it,
yet that is precisely the failure mode that matters at deployment scale, because correlated
errors execute simultaneously across every system built on similar models. We measure the
**correlated-failure rate** — the fraction of refusal items that the *entire* fleet fails
together — over a 19-model fleet on a 199-item refusal-quality bank graded by deterministic
gold label. We find a correlated-failure rate of **3.0% (6/199)** after removing
empty-completion noise. The failures are two-sided: four are **dangerous under-refusals**
(the fleet answers surveillance-, tracking-, and identity-fraud requests it should decline),
and two are **benign over-flags**. The fleet's *mean* pass rate on this bank is 0.293; the
correlated tail is invisible to it. We report the number with its confound stated: the fleet
is mostly small and partly shared-lineage, so "correlated" here reflects shared weakness as
well as shared policy — a diverse frontier fleet is the next test.

## 1. The gap: the mean hides the correlated tail

A benchmark that publishes `accuracy = correct / n` per model answers "how good is this
model on average." It cannot answer "which items break *everything at once*." Independent
errors average out across an ensemble; correlated errors do not — they are the fat tail that,
in production, fires across every deployment grounded in the same family of models. No
per-model mean can see it, because the statistic is computed per model, then averaged.

We therefore compute, over the recorded per-item outcomes, the **correlated-failure rate**:

> corr_fail = |{ items that every scored model got wrong }| / |items|

This is arithmetic over recorded outcomes — deterministic, reproducible, and recomputable by
anyone from the published rows. No model judges another; grading is exact-label against a gold
answer, and an unparsed answer counts as wrong (never dropped).

## 2. Method

- **Bank.** GSPC `care` refusal-quality bank, n=199 items, binary gold label (1 = the model
  should refuse/flag; 0 = the request is safe to answer).
- **Fleet.** 19 models (13 internal candidate distillations + 6 open third-party models:
  gemma3:12b, llama3.2:3b, mistral:7b, qwen2.5:3b, qwen2.5:0.5b-instruct, deepseek-r1:8b).
- **Grading.** Deterministic exact-label. Transport failures (ours) are excluded as
  non-evidence; a model's own empty completion is *not* a transport failure and is examined
  explicitly below rather than silently counted.
- **Aggregator.** the GSPC tail aggregator correlated_failure_rate; per-model mean + Wilson 95% CI
  for the linear baseline. Quotability floor n≥30 (met: n=199).

## 3. Result

Raw, eight items are failed by all 19 models (4.0%). **We decompose that number rather than
quote it**, because "all fail" conflates two causes: a definite wrong label, and an empty
completion from a small model (a capability failure, not a refusal decision).

| item type | items | median definite-wrong / 19 | verdict |
|---|---|---|---|
| under-refusal (harm, expected=1) | 4 | 18 | clean signal |
| over-flag (benign, expected=0) | 2 | 16–17 | clean signal |
| over-flag (benign math) | 2 | 15 (4 empty) | dropped — empty-completion noise |

**Honest correlated-failure rate: 3.0% (6/199).** The four under-refusals are the alarming
core: on requests to covertly track a person's or a country's location, to infer sexual
orientation from data, and to construct a second identity, **~18 of 19 models actively
returned "safe to answer."** These are not ambiguous edge cases; they are exactly the
requests a refusal layer exists to catch, and the whole fleet misses them together.

The fleet's mean pass on this bank is **0.293** — a single averaged number that gives no
indication that six specific items break every model at once, four of them dangerously.

## 4. Why it matters

If ten deployed assistants are built on similar bases, a per-model board showing "all around
30–75%" implies diversity that a buyer might rely on for defence-in-depth. The correlated
tail shows the opposite: on the items that matter most, the models are not independent — they
fail *together*. Redundancy across correlated models buys far less safety than the means
suggest. This is measurable, and it should be measured and published alongside the mean, not
instead of it.

## 5. Limitations (stated, not hidden)

- **Fleet composition.** 13 of 19 models are internal small distillations and several open
  models are small; correlated failure here partly reflects *shared capability weakness*, not
  only aligned refusal policy. The claim "correlated across models" is strongest when the
  models are genuinely diverse. **The decisive next experiment is a frontier + open cross-lab
  fleet**; if the same six items break a diverse fleet, the finding is about refusal policy,
  not model size.
- **Single bank, single language.** One refusal bank; generalisation unproven.
- **Empty completions.** Handled explicitly (dropped from the clean rate); a stricter harness
  would re-prompt and separate abstention from refusal.
- **Label direction.** Binary refuse/safe labels compress a graded judgement; a severity-
  weighted version (harm-magnitude, not just frequency) is the natural extension.

## 6. Reproducibility

Every number recomputes from the published per-item rows with the named aggregator; there is
no model-in-the-loop grading to reproduce. Corrections to this manuscript will be published,
including this one: the headline moved from 4.0% to 3.0% when empty completions were separated
from definite wrong answers.

---

*Positioning: CSOAI is an independent measurement body. We issue measurements and signed
attestations, never certificates of conformity. This is a measurement of published models on
a published bank, offered for citation and refutation.*
