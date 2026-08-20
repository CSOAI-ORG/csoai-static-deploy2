# SWEEP METHODOLOGY IMPROVEMENTS — FROM THE STATISTICAL AUDIT (2026-08-20)
**JEEVES · the 130-cell matrix was audited with real statistics (Wilson CIs, power, IRT, Spearman-Brown) · here's what we fix**

---

## THE AUDIT'S VERDICT (live-computed, not vibes)
1. **3 items/axis is a coin flip** — a 1/3 score has a 95% Wilson CI spanning [0.06, 0.79]. IRT SE ±2.26 logits. Spearman-Brown reliability 0.25–0.43 vs 0.77–0.88 at 30 items.
2. **The difficulty gradient is statistically real** at axis level (care [0.56, 0.86] vs art5 [0.05, 0.30] — no overlap), but its cause (genuine difficulty vs wording vs predicate strictness) is untested.
3. **mistral's "lead" is NOT statistically supported** — 0.487 vs 0.385 at n=39 gives z=0.91; mid-table ranks 2-6 are one unresolvable band. ~28 items/axis needed for 80% power; 30 items resolves it (z=2.89).
4. **council-oowm's persistent 0.000 is statistically separable (z≈2.4-2.7) but causally ambiguous** — it's likely a format/instruction-following artifact (exact-label scoring measures format compliance first, per IFEval). Never report "0.000 = fails all 13 axes" without a failure-mode audit.

## THE THREE IMPROVEMENTS (applied next sweep)
| # | Change | Why | Expected effect |
|---|---|---|---|
| 1 | **≥15-30 items/axis** (frozen-anchor continuity) | 3 items = coin flip; 30 = z=2.89 | trustworthy axis scores + rankings |
| 2 | **Triple-signal predicates** (exact + keyword + semantic) + sampled decoding + failure-mode taxonomy | disambiguates genuine failure vs format | the 0.000 story becomes a measured finding, not an artifact |
| 3 | **CI/reliability/significance reporting in the signed card** | Wilson CI per cell, bank version, McNemar for model comparison | every number self-verifying |

## IMMEDIATE ACTIONS
- [ ] Patch `local_fleet_sweep.py` → failure-mode taxonomy (empty/refusal/off-format/wrong-label) in the next run
- [ ] Re-score council-oowm's cells with triple predicates → is 0.000 format or genuine?
- [ ] Bank growth: templated mutation (≈$0) → LLM paraphrase with anchor-verification → bounties for jail/art5/mach
- [ ] The signed card gains: Wilson CI per cell + bank version + McNemar vs fleet

## WHY THIS MATTERS (the moat)
**The audit IS the moat**: no competitor publishes CIs, power analysis, or failure-mode audits on their leaderboards (Vals has SEM bars only; nobody has the full package). We're not just signing — we're signing *statistically honest* numbers. That's the difference between a scoreboard and a measurement instrument.

## SIGIL
`sweep-methodology-improvements-2026-08-20-jeeves`

## THE 0.000 DECODED (verified live after rebuild)
- **council-oowm's 0.000 across 13 axes = OFF-FORMAT artifact, NOT genuine failure.**
- The rebuilt model responds `??????????` to all classification prompts — a tokenizer/merge artifact from the OOWM worldview merge (the model generates but in a broken token sequence).
- **This is the audit's prediction confirmed**: exact-label scoring measures format compliance first (IFEval's premise). The "our fine-tune scores zero" story was a measurement artifact, not a capability finding.
- **The honest report**: "council-oowm 0.000 (n=39, format-failures — UNMEASURED by this instrument)" — the failure-mode taxonomy made it decomposable.
- **Next**: decide the merge fix (the `?` artifact) or report council-oowm as format-broken, honestly.
