# NEXT 100 STEPS — OpenRouter + LM Arena + improve OURS (CSOAI sov model family)
Grounded 2026-08-23. Estate state: 422 OpenRouter models (API live, OPENROUTER_API_KEY present),
14 local pod models, 469 measured boards, 23 GSPC axes, 177-probe genome, EAT loop autonomous.

## GOAL (3 threads, compounding)
1. **OpenRouter** — route/benchmark/eval across 422 models; use the catalog as a measured substrate.
2. **LM Arena** — understand + leverage the arena Elo ranking; publish our measurement for ranked models.
3. **Improve OURS** — the sov/* model family; measure → route → improve on the GSPC axes; push to OpenRouter/Arena.

---
## BLOCK 1 — OPENROUTER AS MEASURED SUBSTRATE (steps 1-30)
The estate already has an OpenRouter catalog adapter (baseURL https://openrouter.ai/api/v1). Turn it into a *measured* substrate.
1. Pull full OpenRouter model catalog (42 models x metadata: id, context, pricing, provider).
2. Build an index: model -> {provider, context_window, price_in/out, modality}.
3. Query our OpenRouter key's budget/usage (auth'd /api/v1/models + usage endpoint).
4. Map the top 50 OpenRouter models to our GSPC axis taxonomy (which axes each is relevant to).
5. Wire OpenRouter as a *measurement* model source in measure_chain (route GSPC probes through OpenRouter chat completions).
6. Add an OpenRouter benchmarking run: run our 177-probe genome through 20 flagship OpenRouter models.
7. Score each OpenRouter model on the GSPC axes (our honest grader, not their leaderboard).
8. Produce a cross-model GSPC leaderboard (our models vs OpenRouter frontier).
9. Build cost/latency per model measured (so routing is cost-aware, not just accurate).
10. Wire OpenRouter into the AEAI auto-router logic (route by cost/latency/accuracy from our measurements).

### OpenRouter routing + evals (11-20)
11. Test OpenRouter auto-router vs our cost-aware routing on a held-out probe set.
12. Add provider-preference routing (route to a cheaper provider for the same model).
13. Measure per-provider variance (same model, different provider may differ in quality).
14. Use OpenRouter Fusion-style cheap-model ensembling — measure if cheap-ensemble beats a frontier model.
15. Compare a cheap-model ensemble vs single frontier model on the GSPC axes (honest delta).
16. Add fallback routing: if a provider 5xx/errors, fall back to next-best provider (EAT resilience).
17. Build a routing scorecard: accuracy + cost + latency per route, published.
18. Push the measured routing into the DSH settings.yaml (so the harness routes by our measurements).
19. Re-run the flight (step 6) monthly to catch model drift (frontier models change).
20. Sign + chain the OpenRouter benchmark results into the estate (so they're EAT-auditable).

### OpenRouter as product/measurement surface (21-30)
21. Expose the OpenRouter-derived GSPC leaderboard at /api/gspc (add OpenRouter models as rows).
22. Add an /api/model-router endpoint (agents ask "which model for axis X" -> our measured answer).
23. Publish the OpenRouter benchmark as a signed measurement board (measurement, not certification).
24. Wire the router into the AG-UI catalog (agents see the measured best model per task).
25. Add a cost/accuracy Pareto frontier visual (the honest routing tradeoff).
26. Benchmark our sov/* models vs the top OpenRouter models honestly (no cherry-picking).
27. Publish honest negative results (where OpenRouter frontier beats us) — measurement body integrity.
28. Add OpenAI-compatible tool-calling routing test (do our models/tools work via OpenRouter).
29. Automate a weekly OpenRouter model-drift probe (cheap, 1 sample per model).
30. Chain the drift-probe results into the estate (EAT anchor).

---
## BLOCK 2 — LM ARENA (steps 31-55)
LMArena is HTML-only (no public leaderboard API) but hydrates from an internal endpoint; arena Elo is the industry's preference ranking.
31. Probe the LMArena internal endpoint (the React app hydrates from it — find the JSON feed).
32. Scrape/parse the current arena Elo leaderboard (top models + Elo + votes).
33. Normalize arena Elo to our GSPC axis mapping (which arena-ranked models map to which axes).
34. Correlate arena Elo vs our GSPC measured scores (do they agree? honest analysis).
35. Identify the discrepancy: models that rank high in arena but score low on our deterministic axes (and vice-versa) — publish.
36. Use arena Elo as a *preference* signal alongside our *deterministic* score (never replace).
37. Determine how to submit/register our sov/* models to LMArena (peer-reviewed arena bots).
38. Prepare a sov model variant for arena submission (a clean instruct-tuned checkpoint).
39. Run the arena-facing eval (are our models competitive in a blind pair-wise arena?).
40. If competitive, submit a sov model to LMArena for public Elo.
41. Track our arena Elo over time (weekly) — measure if our models improve.
42. Use arena human-preference data as a reward signal to fine-tune our sov models (DPO/RLHF).
43. Correlate human-preference (arena) with our deterministic safety measurements (both matter).
44. Build an arena-vs-deterministic dashboard (the honest two-signal measurement).
45. Publish the arena correlation study (measurement body: how preferences relate to safety).

### Arena-informed improvement (46-55)
46. Feed arena-preference as a secondary reward in a sov fine-tune (pairwise preference loss).
47. Re-measure the fine-tuned sov model on GSPC — did it improve without hurting safety? (ouroboros).
48. Keep the fine-tune only if GSPC improves AND safety holds (honest gate).
49. Add arena-style pair-wise eval to our own pipeline (internal A/B of sov variants).
50. Build an internal arena (our models pair-wise, human/scorer judged) to iterate variants fast.
51. Use the internal arena to select the best sov variant before any public submission.
52. Measure per-axis Elo (arena Elo split by task) — where are we strong/weak.
53. Route to our strongest sov variant per axis (internal auto-router).
54. Publish honest arena-vs-GSPC findings in a measurement report (not marketing).
55. Chain the arena/Elo data as a measured input (never a certification).

---
## BLOCK 3 — IMPROVE OURS (the sov/* family, steps 56-85)
The estate's own models (sov33, sov-*, clan-*) served on the pod (14 models).
56. Inventory the sov/* family: base + variants + the weights we own.
57. Measure each sov variant on all 23 GSPC axes (honest baseline).
58. Identify per-axis strengths/weaknesses (which sov variant wins which axis).
59. Build a per-axis sov router (route to our best variant per axis — this is the moat).
60. Pick the weakest axis for the first improvement iteration (ouroboros, fix-what's-wrong).
61. Collect error vectors: capture the failed GSPC probes for the weak axis (exact failures).
62. Build a QLoRA fine-tune on those exact failures (real weights, not prompt-engineering).
63. Re-measure base+sov variant on the same axis — honest delta (did it actually improve?).
64. Keep the variant only if the mean genuinely went up (ouroboros gate).
65. Repeat for the next weakest axis (iterate the self-improvement loop).
66. Add retrieval-grounding: statute-retrieval-augmented inference on the weak axes (a retrieval win).
67. Measure if retrieval-grounding beats weight-tuning on the weak axes (honest comparison).
68. Try a "majority-confidence" route (2-model ensemble on the weak axis) — measure.
69. Keep only what provably improves (no reward-hacking; DRUM-anchor discipline).
70. Publish honest negative results (where our sov family is beat by OpenRouter frontier).

### Widen the mine (71-80)
71. Distil a frontier capability into a sov variant (e.g. distil a strong OpenRouter model onto ours).
72. Measure the distilled variant on GSPC (did distillation transfer or hurt?).
73. Build a sov variant specifically for EU AI Act / Article 50 (the compliance moat).
74. Measure the compliance variant on the art5/Art50 axes (dedicated evaluation).
75. Add a "safety-first" sov variant that optimizes refusal correctness (when to refuse vs engage).
76. Measure the guardrail-rejection rate honestly (refusal precision/recall — don't over-block).
77. Build a "documentation" sov variant for llms.txt/agent-facing surfaces.
78. Cross-benchmark against the estate's existing sov variants (GOVBENCH 0.931, etc.).
79. Publish the sov family to MCP/PyPI as measured products.
80. Wire the improved sov variants into the live route (councilof.ai /api/model-router).

### Productionize (81-85)
81. Push the best-per-axis sov variants to the OpenRouter catalog (if we can host/serve them).
82. Register the measured sov variants in the MCP registry (meokLabs:false, CSOAI).
83. Sign + chain every improved model card (EAT measure->sign->chain).
84. Mirror the improved sov weights to the pod RAG volume + Oracle (backup).
85. Auto-re-measure daily; auto-promote the best variant per axis (continuous improve).

---
## BLOCK 4 — TEST + EAT LOOP + OWNER (steps 86-100)
86. Full E2E: route a probe through the improved sov model -> GSPC score -> sign -> chain -> board.
87. Verify the front-end /api/model-router + /api/gspc show the improved results.
88. Run the Claims-E2E + pre-deploy smoke tests (all user types).
89. Auto batch run (mine->measure->improve->test->audit->re-batch) — the continuous loop.
90. Verify the EAT 7-box: measured, CI, signed, chained, anchored, boarded, mirrored.
91. Set up a nightly improve-batch (cron/timer) so the loop compounds.
92. Monitor inference stability (the wedging model issue) — harden the serving layer.
93. Build a drift-guard on the OpenRouter catalog (models change monthly).
94. Audit: cost of improvement vs value (is the fine-tune worth it?).
95. Publish the honest improvement report (what worked, what didn't).
96. Owner-gated: OpenRouter credit budget, LMArena submission approval, GPU fine-tune budget.
97. Owner: SOV3 billing reactivation (the estate's big model host).
98. Owner: GitHub org public access (to publish models/cards).
99. Re-run all front-end E2E across user types (agents/lm-arena-submitters/verifiers).
100. Final: 100/100 A++++ scorecard — every surface signed, measured, tested, and au-published.

## VERIFICATION DOCTRINE
- Measurement, not certification. Never claim "gold standard" or "attestation" for a model score.
- Honest negatives published (where frontier beats us). Probe every claim against signed artifacts.
- Every improvement gated by "did the GSPC score genuinely go up" (ouroboros) — no reward-hacking.
- Keep the EAT loop autonomous: measure->sign->chain->anchor->board->mirror, on the pod.
