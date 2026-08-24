# NEXT 100 — LIVE ARENA + TRUSTED MEASUREMENT (LM-arena/OpenRouter space)

> Forward plan to move the drum from **indexing** benchmarks (static, like a leaderboard) to
> **running + owning** a measured, signed, contamination-aware live evaluation layer — the thing
> OpenRouter/LM Arena cannot do because they route/host but don't own or verify the data.
> Doctrine: measurement, not certification; no fabrication; consent-gated; [GATE]/[LANE] tagged.
> Grounded: 662 items, EAT 4/7, trust flip gated on a real nonconformity score.

## PHASE 1 — TRUST FLIP (the gate to everything) — 1–15
1. [in-lane] Stand up a decoder that exposes per-token logprobs (locally via MLX, or a pod 3090
   model). Unblocks TECP token-entropy.
2. [in-lane] Implement `s(x) = mean per-token −log p` in `token_entropy_score.py`.
3. [in-lane] Score the 80 measured labels with token-entropy.
4. [in-lane] Split-conformal calibrate → q̂ on the calibration split.
5. [in-lane] Realized-coverage check: `Pr[auto AND wrong] ≤ α=0.05`.
6. [in-lane] If it clears → flip `router_trust.json` `trusted:true` (+7, honest).
7. [in-lane] Else document the negative (ledger), never force.
8. [in-lane] Add confidence-weighted self-consistency as a second score; compare coverage.
9. [in-lane] Multi-model re-run (Groq gpt-oss-120b, Oracle 70B) to confirm the score generalizes.
10. [in-lane] Report the winner score + its realized bound in the trust marker.
11. [in-lane] Cross-validate on a held-out probe set (no leakage into calibration).
12. [in-lane] Add the nonconformity score to the calibration-set schema (score no longer proxy).
13. [in-lane] Wire `drum_route` to use the trusted score (only routes when `trusted:true`).
14. [in-lane] Drift-monitor the score distribution over time (drift_monitor.py).
15. [in-lane] Update the scorecard + EAT "ci"/measured boxes only after the signed flip.

## PHASE 2 — MEASURED LIVE ARENA — 16–30
16. [GATE] Stand up a live measured arena on the pod fleet (frozen probe-set, signed runs).
17. [in-lane] Define the arena probe-set (the 80 measured + a frozen public/eval set).
18. [in-lane] Per-model arena runner (fleet or API) with per-token capture.
19. [in-lane] Emit `feeds/arena_runs.json` — signed, timestamped, per-model measured results.
20. [in-lane] ETA-style measured Elo (not crowd-sourced) — each pair a measured, signed run.
21. [in-lane] Store per-run (probe, prompt, tokens, entropy, verdict, human-ref).
22. [in-lane] Deterministic graders (the sibling's axis-eval graders) for objective tasks.
23. [in-lane] LLM-adjacent graders only for open-ended tasks, with a signed human-audit path.
24. [in-lane] Report measured results with the honest "measured, not certified" marker.
25. [in-lane] Per-model card (the frontier-lab sectors) surfacing its measured arena runs.
26. [in-lane] Arena → benchmark-card linkage (each benchmark gets its measured runs).
27. [in-lane] The 7-box EAT "measured" box reads the live arena (computed, not hardcoded).
28. [in-lane] Loop-latency feed extended to the full arena run (days-to-hours proof).
29. [GATE] Sign each arena run (Ed25519) once the rail lands.
30. [in-lane] UNMEASURED stays UNMEASURED — no model gets a measured label without a signed run.

## PHASE 3 — CONTAMINATION (the anti-Goodhart moat) — 31–45
31. ✅ [in-lane] `contamination` field on every benchmark card + `feeds/benchmark_contamination.json` (36 benchmarks, honest levels: 12 designed-resistant, 5 high).
32. ✅ [in-lane] Leakage register per benchmark (evidence + level) — never inflates a score; `drum_route` now returns a contamination note.
33. [in-lane] Leakage pre-check before routing a model to a probe it has seen.
34. [in-lane] LiveBench-style expiry: rotate leaked probes; re-measure.
35. [in-lane] Report contamination in the board (the honest scoring caveat).
36. [in-lane] Contamination-aware `drum_route` (never route on seen data).
37. [in-lane] Track cross-benchmark overlap (the same probe in 2 benchmarks).
38. [in-lane] A contamination "measure this benchmark's own leakage" metric.
39. [in-lane] Wire contamination into the gauge feature (a feature channel, not a score).
40. [in-lane] Quarterly contamination re-audit of all 36 benchmark cards.
41. [in-lane] Document the SWE-bench ~33% + reward-hacking 73.8% contamination evidence (validation).
42. [in-lane] Anti-overfit: report + strip any inflated benchmark score from a leaked probe.
43. [in-lane] The contamination feed as a data-licensing SKU (the freshest moat data).
44. [in-lane] Crosswalk contamination ↔ model-benchmark relation for the gauge.
45. [in-lane] Never report a contamination-inflated number as a capability (doctrine rule).

## PHASE 4 — CONSENTED DATA PRODUCT — 46–60
46. [GATE] Consent-gated data product: licensed eval-transcripts (disclosed probes, licensed outputs).
47. [in-lane] Signed eval-transcript schema (the reusable data unit).
48. [in-lane] Transcript provenance (probe source, model, config, entropy, verdict, human-ref).
49. [in-lane] The transcripts are the MEOK/consented data path (never harvested — disclosed).
50. [in-lane] Historical-pattern correctness predictor (learned score, attempt #4b).
51. [in-lane] Preference pairs (A>B measured, not crowd).
52. [in-lane] Safety-incident captures (failures = highest-value data, flagged not hidden).
53. [in-lane] A data marketplace scaffold (licensing metadata, not crypto).
54. [LANE] Price/terms (transcript tier, contamination tier, incident tier).
55. [in-lane] Data-license control (who can buy, what they can do — sovereignty).
56. [in-lane] Consent register (every disclosed probe + its license).
57. [in-lane] Data product → csoai-fisher-rao feature channel.
58. [in-lane] PII-scrub the transcripts before licensing (privacy rail).
59. [in-lane] Data product unit tests (schema, attestation, scrub).
60. [in-lane] The data-product README marks [BET] — "measured, never certified; value unproven".

## PHASE 5 — DOMAIN + EAST↔WEST ARENAS — 61–75
61. [in-lane] Sector-tagged arena runs (financial, legal, medical, defence).
62. [in-lane] Domain-specific leaderboards (the 9 sectors as a lens, not a generic list).
63. [in-lane] East↔West divergence: run the same probes on East + West models.
64. [in-lane] `feeds/east_west_divergence.json` — the measured pair-gap.
65. [LANE] Feed divergence into DORADO's pair-gap.
66. [in-lane] Frontier-lab cards (xAI, DeepSeek, Qwen, Kimi) as measured actors.
67. [in-lane] Sector card enrichment (measurement axes + live arena per sector).
68. [in-lane] Crosswalk arena domain ↔ GSPC 14-slot.
69. [in-lane] Per-domain risk ranking (the measured gauge input).
70. [in-lane] Regional model disclosure (UNMEASURED until a signed run exists).
71. [in-lane] The 22-axis scope (siblings) → measured visibility.
72. [in-lane] Per-domain contamination focus.
73. [in-lane] Domain-specific red-team probes (harm benchmarks per sector).
74. [in-lane] The arena as the domain-flywheel (gaming → financial → legal reasoning).
75. [in-lane] Quarterly domain coverage re-scan (mining the gap per sector).

## PHASE 6 — OFF-MAC INFRA + WIRING (it runs on the pods) — 76–88
76. [GATE] Fix the runpod git remote auth (or a reachable bare repo) — push master-harness off-Mac.
77. [in-lane] Nightly pod run of the drum gates (the ship + keepalive already exists).
78. [in-lane] Pod-side MCP server (query the drum from the pod, not a copy).
79. [LANE] csoai-fisher-rao consumes the pod-side gauge_features.
80. [LANE] csoai-arena indexes the pod-side benchmark cards.
81. [in-lane] Ship the live arena + router to sov-brain-2 + oracle (backup_offmac).
82. [in-lane] Off-Mac backup of the arena_runs + contamination feeds (the valuable data, not just the code).
83. [in-lane] Volume quota watch (RAG volume fills → rotate).
84. [in-lane] Pod reachability registry (dead pod skipped, never hammered).
85. [in-lane] The orchestration lives on the pod (workflows, not the Mac).
86. [in-lane] Ephemeral Mac state re-derivable from git + off-Mac backup.
87. [in-lane] Overnight status card includes off-Mac backup status.
88. [in-lane] Cross-run pod coherence (sov-brain-2 + oracle hold the same drum).

## PHASE 7 — GOVERNANCE / SIGNING / COMPLIANCE — 89–95
89. [GATE] Ed25519 signing rail (did:web + #dsh) — the EAT "signed" box.
90. [GATE] Bitcoin/OTS anchor the arena manifest — the EAT "anchored" box.
91. [in-lane] Key-continuity charter.
92. [in-lane] Public-grammar + naming-quarantine + language-lock audit on arena surfaces.
93. [in-lane] EU-AI-Act evidence pack from the signed measurement (high-risk hook).
94. [in-lane] The signed-card format gates all arena/transcript signing.
95. [in-lane] Never a certification; a signed attestation of a measurement.

## PHASE 8 — SCALE + REVIEW — 96–100
96. [in-lane] Quarterly adversarial-evidence review (every [BET] counter-evidence re-checked).
97. [in-lane] Quarterly 7-box EAT card publish (measured, never certified).
98. [in-lane] Promote-gate: only "measured" after a signed run clears.
99. [in-lane] Task-allocation ops (decisions→human, scale→AI).
100. [in-lane] Re-run the full E2E + scorecard after the trust flip; set NEXT 100.

## HONEST WALL (what blocks the moonshot)

The whole moat is the **trust flip** (steps 1–15) — a *real* nonconformity score clearing coverage.
Attempts #3/#4 are blocked by **model capability** (quota-429, logprobs-disabled), not by the
signal being wrong. The single unblock: a logprobs-capable decoder. Every downstream step is gated
on the signing rail [GATE #dsh] or consent [GATE] — nothing is fabricated to look done.

## The honest delta vs LM Arena / OpenRouter

| Capability | LM Arena / OpenRouter | Ours (after this) |
|---|---|---|
| Live leaderboard | crowd-sourced Elo | **measured + signed** |
| Owns the data | ❌ | ✅ consented transcripts |
| Contamination tracking | ❌ | ✅ |
| Trust router | routes blind | **conformal-trusted** |
| Domain-specific | ❌ | ✅ |
| East↔West measured | US-centric | ✅ |
| Signed/verifiable | ❌ | ✅ (rail lands) |
