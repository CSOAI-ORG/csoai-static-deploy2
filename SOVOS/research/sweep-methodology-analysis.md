# GSPC Fleet Sweep — Methodology Analysis (130-cell matrix)

**Subject:** CSOAI fleet sweep — 10 local models × 13 governance axes, 3 items/axis, deterministic
predicates (temp=0, exact-label), frozen anchors. 390 item-level binary observations (10 models × 13
axes × 3 items) aggregated into a 130-cell score matrix.

**Status:** Analysis + recommendations. All statistics computed from the provided aggregates.
Anything not confirmable from the given data is flagged **UNVERIFIED**.

---

## TL;DR

1. **3 items/axis is not a measurement — it is a coin flip.** A per-axis 1/3 score has a 95% Wilson
   CI of [0.061, 0.792]; even 3/3 gives [0.438, 1.000]. Per-axis ranking of models is meaningless.
2. **The ranking below position 1 is noise.** Even aggregated over all 39 items/model, mistral (0.487)
   is not separable from qwen3:4b (0.385): z = 0.91. The entire mid-table (5 models within 0.052) is
   unresolvable. Only the extremes (council-oowm 0.000 vs everyone) are statistically real.
3. **The difficulty gradient (care 0.733 → art5 0.133) is statistically real at the axis level**
   (n=30/axis, CIs don't overlap) but its *cause* — genuine construct difficulty vs item-wording /
   predicate-strictness artifacts — is untested. With 3 items/axis you cannot fit axis-difficulty
   parameters separately from model ability; you can only compute fleet pass rates.
4. **The persistent zero is a real statistical outlier (z ≈ 2.4–2.7 vs the next-lowest models) but a
   causally ambiguous one.** 39 failures bounds the true per-item rate below ~10% but cannot say
   *why* — genuine failure vs format/instruction-following failure vs predicate interaction. This
   must be disambiguated at the response level before "0.000" is reported as a governance result.
5. **Three high-leverage changes:** (a) grow banks to ≥15–30 items/axis with frozen-anchor
   continuity; (b) multi-signal predicates + sampled decoding + failure-mode taxonomy; (c) CI /
   reliability / significance reporting with bank versioning in the signed card.

---

## 1. Item quality — minimum item counts for stable axis scores

### The math: 3 items is below any defensible floor

- A binary axis score with n=3 can only take values {0, 0.333, 0.667, 1.0}.
- **95% Wilson intervals (computed):**

  | score | 95% CI (n=3) | half-width |
  |---|---|---|
  | 0/3 | [0.000, 0.562] | ±0.28 |
  | 1/3 | [0.061, 0.792] | ±0.37 |
  | 2/3 | [0.208, 0.939] | ±0.37 |
  | 3/3 | [0.438, 1.000] | ±0.28 |

  A per-axis 1/3 vs 3/3 score cannot even be distinguished from chance. (Wilson 1927; Brown, Cai &
  DasGupta 2001 for the interval's coverage superiority.)

- **IRT (1PL/Rasch) standard error:** per-item Fisher information peaks at 0.25 (item difficulty =
  ability). SE(θ) = 1/√(ΣI):
  - 3 items → **SE ≈ 1.15 logits** (95% CI ±2.26 logits — spans nearly the entire difficulty
    range; on the probability scale near p=0.5 that is SE ≈ 0.29, matching the binomial SE exactly);
  - 10 items → 0.63 logits; 30 items → 0.37 logits (probability-scale ≈ 0.09).
  - So 3 items gives an ability estimate whose CI covers most of the bank — useless for ranking.

- **Classical reliability (Spearman-Brown prophecy):** r_kk = k·r₁/(1+(k−1)r₁). With a typical
  per-item intercorrelation r₁ = 0.1–0.2 (plausible for governance items sharing a construct):

  | items | r₁=0.1 | r₁=0.2 |
  |---|---|---|
  | 3 | 0.25 | 0.43 |
  | 10 | 0.53 | 0.71 |
  | 30 | 0.77 | 0.88 |

  Nunnally & Bernstein (1994) standard: ≥0.70 for research use, ≥0.80 for applied decisions.
  Under realistic inter-item correlation, **you need ~10 items for "acceptable research"
  reliability and ~30 for stable ranking.**

- **Practice precedent:** short forms of 4–8 items are used in PRO measurement *for group-level
  comparisons only*; individual-level precision is handled by computerized adaptive testing
  (CAT) ([CAT vs short forms, pediatric IBD PRO](https://doaj.org/article/5a6c26f5cf944dd18d65e3f145e5fbf2)).
  Item *format* changes measurably shift measurement range ([PMC5359818](https://pmc.ncbi.nlm.nih.gov/articles/PMC5359818/))
  — relevant to §2 below. For ranking models separated by ~0.1, group-level short-form logic does
  not apply; you need the power analysis in §3 (~28 items/axis).

### Cheapest ways to grow the banks (ranked by $/item)

1. **Templated mutation (≈$0).** Each of the 39 frozen anchor items → 5–10 scenario templates
   (swap actor, jurisdiction, entity type, numeric values, format) × 4–8 surface variations.
   130 new items/axis in one local generation pass. **Risks:** construct drift; correlated items
   *inflate alpha artificially* while adding little unique IRT information (redundant items don't
   raise the information ceiling). **Mitigations:** embedding dedupe (cosine ≤0.85 against the
   bank), and an anchor-consistency gate — every new item must reproduce the source item's pass/fail
   on 2–3 fixed anchor models.
2. **LLM paraphrase/synthesis + verification (≈$0 compute, cheap human spot-check).** Automatic
   item generation is a mature discipline (Gierl & Haladyna, *Automatic Item Generation: Theory and
   Practice*, Routledge 2013). Modern LLM pipelines add automated verification gates: multi-agent
   generation with Bloom-specialized item writers + automated answer verification
   ([From Questions to Assessment Tuples, ACL 2026 BEA](https://aclanthology.org/2026.bea-1.22/));
   generate-filter-edit pipelines with human-AI collaboration
   ([Generate-Filter-Edit, ACM](https://dl.acm.org/doi/abs/10.1145/3774398.3811566)). For GSPC the
   gate is cheap and *local*: run the candidate on the anchor fleet, keep only items that
   discriminate (p(strong anchor) − p(weak anchor) ≥ 0.2) and fall in the 0.1–0.9 difficulty band.
3. **Bounties ($$; the right tool for the hard axes).** Jail, art5, mach sit at p ≤ 0.133 across the
   fleet — synthetic generation quality collapses exactly where floor items dominate, because there
   is no anchor signal to verify against. Precedent: BIG-bench's 204 community-contributed tasks
   from 450+ authors (Srivastava et al. 2022, arXiv:2206.04615). Structure the bounty: item +
   predicate + expected-label rationale, dual independent adjudication, pilot discrimination gate,
   pay per accepted item ($5–25 range). Jail/art5 items should be solicited from red-team-flavored
   authors, not generic crowds.

**Calibration-first rule for all growth:** every new item gets piloted on a fixed anchor set
(frozen across sweeps) before entering the scored bank. Only items with demonstrated discrimination
and mid-band difficulty enter; the pilot data (per-item p on anchors) becomes the item's calibration
record, versioned alongside the bank.

---

## 2. Difficulty calibration — genuine spread or wording artifact?

### What the data can and cannot say

The reported gradient (care 0.733 … art5 0.133) is presumably fleet mean pass rate per axis — a
**model-sample-dependent statistic** (UNVERIFIED: computed as mean over the 10 models? Only 8 of 13
axes are named in the gradient — 5 axes' difficulties are not given, UNVERIFIED).

At the **axis level** (n=30 = 10 models × 3 items), the gradient is statistically real:

| axis | p (n=30) | 95% Wilson CI |
|---|---|---|
| care | 0.733 | [0.555, 0.858] |
| open / det | 0.600 | [0.423, 0.754] |
| gov | 0.556 | [0.382, 0.717] |
| jail | 0.333 | [0.192, 0.512] |
| safety | 0.167 | [0.074, 0.336] |
| mach / art5 | 0.133 | [0.053, 0.296] |

care and art5 are clearly separated. **But the *cause* is unidentified.** Four mechanisms are
confounded in a fleet pass rate: (a) genuine construct difficulty; (b) item-wording difficulty
(length, abstraction, number of constraints); (c) **predicate-strictness differences** — exact-label
matching is trivially easier for axes whose expected label is short/unique and harder when the
expected response is a longer clause, so part of the "gradient" may be a *gradient of predicate
strictness*, not of governance difficulty; (d) floor/ceiling effects.

Note the distribution: care at 0.733 is near the fleet's ceiling; art5/mach at 0.133 near the floor.
In IRT, item information → 0 as P → 0 or 1. **Items that nearly everyone passes or nearly everyone
fails contribute almost no ranking information** — a large share of the gradient is the instrument
being poorly targeted at this fleet, not merely "axes differ." The fleet grand mean is 0.281; a bank
centered near 0.5 would maximize information.

### How to test wording vs capability (practical battery)

1. **Separate difficulty from ability (IRT).** Fit a 1PL/Rasch model on a *pooled* bank (needs
   ≥10 items/axis to be identifiable; 3 is insufficient — with 3 items per axis you cannot estimate
   b_i and θ_j separately, only a confounded pass rate). Then axis difficulty = mean b_i, and the
   gradient's wording component can be tested against item features.
2. **Judge norming.** Have 2–3 independent raters predict each item's difficulty from the item text
   alone (before seeing results). Low judge–observed correlation ⇒ wording/format artifacts dominate.
3. **Wording-variant perturbation.** Write 2–3 surface variants per item (same construct, different
   length/format/abstraction). If observed p swings >0.2 across variants, the axis score is
   wording-sensitive.
4. **Predicate-sensitivity test.** Re-score the *same responses* with exact → keyword → semantic
   equivalence predicates. If the axis difficulty ordering flips, the gradient is a predicate
   gradient. (This is the cheapest, most decisive single test.)
5. **Floor/ceiling audit.** Report per-item p and item–total correlation. Replace items with
   p > 0.9 (ceiling, no discrimination) or p < 0.1 (floor) — or route them to a stratified bank
   targeted at weaker/stronger models.
6. **Feature regression.** Fit item pass ~ (prompt length, expected-response length, number of
   constraints, predicate type, named-entity density). Significant coefficients identify the
   wording features driving the gradient.

---

## 3. Model ranking stability — CI on a 3-item vs 30-item score

### Per-axis (n=3): no information
See §1 table. Per-axis scores cannot order models at all.

### Model level (39 items — the full current instrument)

| model | score | 95% Wilson CI |
|---|---|---|
| mistral:7b | 0.487 | [0.339, 0.638] |
| qwen3:4b | 0.385 | [0.249, 0.541] |
| qwen2.5:0.5b | 0.359 | [0.227, 0.516] |
| llama3:8b | 0.354 | [0.222, 0.512] |
| qwen2.5:7b / 1.5b | 0.333 | [0.205, 0.491] |
| deepseek-r1:7b | 0.282 | [0.165, 0.438] |
| council-safe | 0.154 | [0.072, 0.297] |
| qwen3:8b | 0.128 | [0.056, 0.267] |
| council-oowm | 0.000 | [0.000, 0.090] |

- **mistral vs qwen3:4b: z = 0.91 — NOT separable.** The headline "mistral leads" is not
  statistically supported at n=39. The whole block from qwen3:4b (0.385) down to qwen2.5:7b (0.333)
  — five models spanning 0.052 — is one unresolvable band.
- The **minimum gap two CIs can resolve at n=39 is ~0.31** (computed: 2·1.96·√(0.25/39)). Only
  council-oowm's 0.000 is separable from the fleet (vs 0.128: z=2.39; vs 0.154: z=2.66).
- CIs above are **optimistic**: they assume item independence within a model; positive
  intra-axis correlation (guaranteed by shared wording) widens them further.

### Projections (assuming the observed rates hold)

| bank | items/model | mistral CI | qwen3:4b CI | top-2 z | min resolvable gap |
|---|---|---|---|---|---|
| current | 39 | [0.339, 0.638] | [0.249, 0.541] | 0.91 (no) | ~0.31 |
| 10 items/axis | 130 | [0.400, 0.570] | [0.305, 0.470] | 1.67 (no) | ~0.17 |
| 30 items/axis | 390 | [0.438, 0.537] | [0.338, 0.434] | 2.89 (yes) | ~0.10 |

**Power:** ~28 items/axis (~367 items/model) to detect the observed 0.102 top-2 gap at 80% power,
α=0.05 (independent-binomial). **Paired analysis changes the economics:** all models answer the same
items, so McNemar on discordant item pairs is the correct test and is far more powerful than
marginal-CI overlap — with a paired design, ~10–15 items/axis is a plausible path to a defensible
top-2 claim (UNVERIFIED: exact paired power depends on the discordance rate, which the aggregate
data cannot reveal). **Use paired tests as the primary inference; report per-model CIs only as
descriptives.**

**Other stability notes:**
- **Bootstrap ranks:** resample items (axis-stratified) to produce a rank distribution per model;
  report the proportion of resamples in which each pair's ordering holds. With 3 items/axis expect
  near-chance ordering stability in the mid-table.
- **"Deterministic" ≠ deterministic:** temp=0 greedy is not guaranteed run-to-run deterministic
  across backends, batch sizes, and GPU kernels. The evaluation literature now treats
  non-determinism as a first-class measurement issue ([The Good, The Bad, and The Greedy,
  arXiv:2407.10457](https://www.semanticscholar.org/paper/The-Good%2C-The-Bad%2C-and-The-Greedy%3A-Evaluation-of-Song-Wang/1281f7cbab728c2aa89f0a1cac925992f64eb2e3);
  [Instance-level Randomization, EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.182/)).
  Recommend duplicate runs (2×) and reporting a flip rate; if any item flips, its pass status is
  noise and should be flagged. (Ollama-specific behavior: UNVERIFIED.)

---

## 4. The honest-gap pattern — persistent zero: signal or artifact?

### Statistical reading
39 failures (13 axes × 3 items) with (approximately) independent items:

- true p = 0.10 ⇒ P(0/39) = 0.016 → p ≥ 0.10 is ruled out at 95%;
- true p = 0.05 ⇒ P(0/39) = 0.135 → p ≤ ~0.05 remains fully plausible.

So the zero is *consistent with* a genuine floor but cannot distinguish "true rate ~0" from
"true rate ~5%". Because items share axes/format, effective N < 39 and the bound is weaker still.
The zero **is** statistically separable from the rest of the fleet (z ≈ 2.4–2.7 vs the 0.128–0.154
group) — the gap is real; the *cause* is open.

### The causal menu (all produce a literal 0.000 under exact-label + temp=0)
1. Genuine capability floor (the model truly cannot satisfy these predicates).
2. **Instruction-following / format failure** — the model answers but never emits the exact label
   (very plausible for an "open world" model; exact-label scoring is a strict-format construct and
   conflates instruction-following with governance behavior — the IFEval line of work exists
   precisely because verifiable-format scoring measures format compliance first
   ([Zhou et al. 2023, arXiv:2311.07911](https://systems-analysis.ru/eng/IFEval_Benchmark); see also
   the inverse failure mode — models trapped into emitting schema-conformant-but-wrong output,
   [the "schema-compliance trap"](https://github.com/rkstu/schema-compliance-trap)).
3. Refusal suppression (safety-tuned refusal applied to governance probes).
4. Parser/tokenizer mismatch (expected label never present in the emitted string).
5. Prompt-interaction (single phrasing the model misreads; temp=0 hides any output-distribution
   mass that might carry the label).

### Disambiguation protocol (cheap — ~1–2 hours of local runs)
1. **Response-level audit (decisive, do first).** Capture all 39 raw outputs; classify each into:
   empty / refusal / off-format / wrong-label-but-sensible / right-label-wrong-format / correct.
   The distribution usually settles it. **Never report "0.000 = fails all 13 axes" without this
   breakdown** — report "0.000 (n=39; all format-failures — UNMEASURED by this instrument)" if that
   is what the decomposition shows.
2. **Sanity items.** Add trivial format items ("Output exactly: PASS"). If these also fail, the
   model has an instruction-following/format problem, not a governance one.
3. **Predicate A/B on the same responses.** exact → keyword → semantic. If the zero vanishes under
   fuzzy/semantic matching while outputs look sane, it is a predicate interaction.
4. **Prompt-variant A/B.** 5 rewordings of a subset of items; any variant >30% pass ⇒ prompt
   interaction.
5. **Sampled decoding.** 10 samples at temp 0.7 (or best-of-n). If the correct label appears in the
   sample distribution >20% of the time, the deterministic pass rate understates capability —
   "best-of-N can unlock smaller models" ([arXiv:2407.10457](https://app.argminai.com/arxiv-dashboard/papers/2407.10457v1)).
6. **Cross-instrument probe.** Run the model on a standard instruction-following probe (IFEval-style)
   to separate instruction-following from GSPC-specific behavior.

**Recommendation:** treat council-oowm's 0.000 as "unmeasurable by this instrument" until steps 1–3
run. The honest framing for the board is "council-oowm: UNMEASURED (format/instrument failure
suspected)" — not "fails all 13 governance axes."

---

## 5. Three concrete improvements to the next sweep

### A. Item count: grow each axis to ≥15 (target 30) with frozen-anchor continuity
- **Change:** keep the original 3 items/axis *frozen forever* as longitudinal anchors; add 12–27
  items/axis via templated mutation + LLM paraphrase (local, ≈$0), each gated by anchor-fleet
  piloting (discrimination ≥0.2, difficulty in 0.1–0.9); use bounties for the jail/art5/mach floor
  axes where synthesis quality collapses. Report both anchor-only and full-bank scores for one
  transition sweep so historical comparability is preserved.
- **Expected effect:** axis reliability ~0.25–0.43 → ~0.65–0.85 (Spearman-Brown); per-axis CI
  ±0.37 → ±0.17 (n=15) / ±0.13 (n=30); model-level top-2 gap resolves (z 0.91 → 2.89 at 30
  items/axis; ~28 items/axis for 80% power); the difficulty gradient becomes *estimable* as real
  IRT difficulty parameters instead of fleet pass rates.

### B. Predicate robustness: multi-signal scoring + sampled decoding + failure-mode taxonomy
- **Change:** (1) score every response on three signals — exact-label, keyword, semantic
  equivalence — and report the vector, not one number; (2) classify every response into a
  failure-mode bucket (empty/refusal/off-format/wrong-label); (3) decode with 5 repeats (fixed seed,
  low temp) or 2 duplicate greedy runs, and report a flip rate; (4) pre-register predicate rules and
  bank hash in the signed card so the score's meaning is frozen with the data.
- **Expected effect:** the 0.000 class of results becomes decomposable (genuine vs format vs
  predicate artifact) without a re-run — the raw responses already in hand answer it; scores stop
  silently conflating instruction-following with governance behavior; measurement noise becomes
  visible and can be bounded. Cost: ~5× decoding (local, cheap) + a scoring module.

### C. Reporting: CIs + reliability + significance + resolvable-gap on every sweep
- **Change:** ship with each sweep: per-axis and per-model Wilson CIs; per-axis reliability
  (KR-20/alpha or IRT SE) and item-total correlations; a **paired (McNemar) significance matrix**
  between models (which orderings are real); bootstrap rank-stability; and a headline
  "minimum resolvable gap at this n" statistic. Version the item bank (bank hash + item texts +
  per-item anchor calibration) inside the 3KB signed card — the card format already supports
  provenance; make score interpretability part of the payload.
- **Expected effect:** the leaderboard becomes honest — readers immediately see that ranks 2–10
  form a band rather than an ordering; the board can make item-bank investment decisions from the
  resolvable-gap number (e.g., "we need ~28 items/axis to resolve the current top-2"); and the
  signed cards become self-describing measurement artifacts (score + uncertainty + bank version +
  per-item calibration), which strengthens the training-fuel and certification uses.

---

## References

- Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *JASA* 22(158), 209–212. (standard; interval used throughout)
- Brown, L. D., Cai, T. T., & DasGupta, A. (2001). Interval estimation for a binomial proportion. *Statistical Science* 16(2), 101–133. (standard)
- Nunnally, J. C., & Bernstein, I. H. (1994). *Psychometric Theory* (3rd ed.). McGraw-Hill. (reliability thresholds 0.70/0.80; standard)
- Embretson, S. E., & Reise, S. P. (2000). *Item Response Theory for Psychologists*. Erlbaum. (SE/information; standard)
- Gierl, M. J., & Haladyna, T. M. (2013). *Automatic Item Generation: Theory and Practice*. Routledge. ([library record](https://www.abebooks.com/Automatic-Item-Generation-Theory-Practice-Gierl/31243081103/bd))
- Rasch Measurement Transactions — *Sample Size and Item Calibration [or Person Measure] Stability* ([rasch.org](https://www.rasch.org/rmt/rmt74m.htm)) — calibration stability with small samples.
- Zhou, J., et al. (2023). Instruction-Following Evaluation for Large Language Models (IFEval). arXiv:2311.07911. ([summary](https://systems-analysis.ru/eng/IFEval_Benchmark))
- Song, Wang, et al. (2024). The Good, The Bad, and The Greedy: Evaluation of LLMs Should Not Ignore Non-Determinism. arXiv:2407.10457. ([semanticscholar](https://www.semanticscholar.org/paper/The-Good%2C-The-Bad%2C-and-The-Greedy%3A-Evaluation-of-Song-Wang/1281f7cbab728c2aa89f0a1cac925992f64eb2e3); [argmin summary](https://app.argminai.com/arxiv-dashboard/papers/2407.10457v1))
- Instance-level Randomization: Toward More Stable LLM Evaluations. EMNLP 2025 Findings. ([aclanthology](https://aclanthology.org/2025.findings-emnlp.182/))
- Srivastava, A., et al. (2022). Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models (BIG-bench). arXiv:2206.04615. (community-contributed task precedent)
- From Questions to Assessment Tuples: A Multi-Agent Framework with Bloom-Specialized Agents and Automated Verification. ACL 2026 BEA. ([aclanthology](https://aclanthology.org/2026.bea-1.22/))
- Generate-Filter-Edit: A Human-AI Collaborative Pipeline for Middle School Math Questions. ACM. ([dl.acm.org](https://dl.acm.org/doi/abs/10.1145/3774398.3811566))
- CAT vs short forms for pediatric IBD PRO assessment ([DOAJ](https://doaj.org/article/5a6c26f5cf944dd18d65e3f145e5fbf2)); item-format effects on measurement range ([PMC5359818](https://pmc.ncbi.nlm.nih.gov/articles/PMC5359818/))
- The schema-compliance trap — models emitting schema-conformant-but-wrong output ([github](https://github.com/rkstu/schema-compliance-trap))

## UNVERIFIED items
- Per-cell values of the 130-cell matrix (only aggregates were provided) — all model-level statistics above are derived from the stated averages and assume they are simple means.
- The definition of "axis difficulty" (assumed = fleet mean pass rate across the 10 models); only 8 of 13 axes are named in the gradient.
- That the sweep scored *generated text* with exact-label matching (vs multiple-choice labels) — the whole §2/§4 analysis of predicate strictness assumes generation+exact-label.
- Ollama temp=0 run-to-run determinism behavior on this fleet.
- council-oowm's actual raw outputs (why it scored 0.000) — the response-level audit is prescribed, not performed.
- Exact paired-design power for the top-2 comparison (depends on item-level discordance, not recoverable from aggregates).
