# NEXT 100 STEPS — EXECUTION PLAN (2026-08-22)

Unblocked by: GCP retired → RunPod 3090 (11439) + Oracle (11436/11437) are the inference backends.
Status markers: ✅ done · 🔄 running · ⏸️ gated (owner/lane/external) · ⬜ queued.

## PHASE A — EAT LEADERBOARD (steps 1–18)
1. ✅ qwen2.5:7b measured (28.6→66.7)
2. ✅ mistral:7b measured (32.6→66.1)
3. ✅ llama3:8b measured (sovereignty +52.3 RAG)
4. 🔄 qwen3:8b measuring
5. ⬜ deepseek-r1:7b measure
6. ⬜ qwen2.5:1.5b measure
7. ⬜ qwen2.5:0.5b measure
8. ⬜ qwen2.5:0.5b-instruct measure
9. ⬜ compile full leaderboard → EAT-GOVBENCH-RESULTS
10. ⬜ citation_verify --score-model (real citation accuracy on 3090)
11. ⬜ jail-probe against local models (Mvt 5 security)
12. ⬜ flag council-oowm corruption → rebuild ticket
13. ⬜ flag muse-glimmer (verify or flag)
14. ⬜ Oracle micro smoke (qwen2.5-0.5b-mined)
15. ⬜ record baseline-vs-RAG gap as signed-able finding
16. ⬜ honey_harvest.py from EAT answers (RAG lift → retrieval pool)
17. ⬜ bench_to_honey_kb.py from new benchmarks
18. ⬜ sov_honey_unify --ingest (grow mine)

## PHASE B — MINE EXPANSION (19–30)
19. ⬜ verify honey row count grows (was 94,181)
20. ⬜ verify arena rounds grow (was 2,739)
21. ⬜ mine: sov_ingest_all.py
22. ⬜ mine: ingest_annexes.py
23. ⬜ mine: mine_downloads_corpus.py (if reachable)
24. ⬜ honey health: sov_honey_unify --selftest (watch 11→N ollama)
25. ⬜ mine OOWM query smoke
26. ⬜ mine bloodline reconciliation
27. ⬜ mine chatml triplet count
28. ⬜ record mine growth → alignment doc
29. ⬜ honey provenance (append-only ledger intact)
30. ⬜ mine disk hygiene (reclaim, no purge)

## PHASE C — SIM WORLD MEASUREMENT (31–48)
31. ⬜ sim_benchmark per-axis (16 axes, more count)
32. ⬜ sim_spawn agents (12 hives)
33. ⬜ sim_emit_card (signed h3k over fresh records)
34. ⬜ sim_game rps (signed replay)
35. ⬜ sim_game connectx (signed replay, more seeds)
36. ⬜ record replay receipts (Mvt 4 substrate)
37. ⬜ sim_scene audit (alive/defeated drift)
38. ⬜ sim_control reset if drift (only if needed)
39. ⬜ sim_benchmark targeted axes (jail/slot15/human-vs-ai)
40. ⬜ emit card per axis-cluster
41. ⬜ verify card signatures offline
42. ⬜ map replay+cards → Mvt 4 envelope schema
43. ⬜ record sim round count
44. ⬜ sim sovSpace flag audit
45. ⬜ sim scoreboard snapshot
46. ⬜ sim card gzip/bytes audit
47. ⬜ sim → h3k card count
48. ⬜ write sim measurement ledger row

## PHASE D — REGISTRY EXECUTION (49–68)
49. ⬜ write IE registry rows (SB 315)
50. ⬜ write IE registry rows (Vietnam 33/2026 + Decree 142)
51. ⬜ write IE registry rows (Germany KI-MIG)
52. ⬜ write IE registry rows (transparency-code signatories)
53. ⬜ write IE registry rows (CA SB 243, NY Art 47, S9051B)
54. ⬜ write IE registry rows (Italy 612-quater)
55. ⬜ write IE registry rows (UK OSA Novi/Joi)
56. ⬜ write IE registry rows (Colorado dormant)
57. ⬜ write IE registry rows (Korea contrast)
58. ⬜ ProvisionRecord schema bump (signatory+audit-deadline+absentee)
59. ⬜ hash-anchor each row
60. ⬜ registry quality gate (sourced+dated)
61. ⬜ registry RSS/API stub
62. ⬜ registry changelog
63. ⬜ staleness rule (>14d flag)
64. ⬜ SB 315 row ↔ positioning paper link
65. ⬜ absentee watch (xAI/Amazon)
66. ⬜ NANDO/EN 18286 watch armed
67. ⬜ first-enforcement watch armed
68. ⬜ Anthropic detector watch armed

## PHASE E — DRAFT REMAINING (69–88)
69. ⬜ Mvt 5: DeepJack mitigation matrix (158)
70. ⬜ Mvt 5: signed-recipe gate spec (151)
71. ⬜ Mvt 5: marketplace-spoofing counter (167)
72. ⬜ Mvt 6: 18+ gate spec (181)
73. ⬜ Mvt 6: local-first BYOK spec (190)
74. ⬜ Mvt 6: approval-gate UX spec (191)
75. ⬜ Mvt 6: signed approval logs (192)
76. ⬜ Mvt 6: spend-cap wallet (196)
77. ⬜ Mvt 8: OSF preregistration text (241)
78. ⬜ Mvt 8: ICLR abstract (253)
79. ⬜ Mvt 8: in-toto predicate schema (254)
80. ⬜ Mvt 9: capacity plan (292)
81. ⬜ Mvt 9: transparency report commitment (296)
82. ⬜ Mvt 3: funding-transparency page (104)
83. ⬜ Mvt 3: grants ceiling (103)
84. ⬜ Mvt 2: insurer deck (077)
85. ⬜ Mvt 2: GPAI CoP tracker (081)
86. ⬜ Mvt 7: crosswalk feed AIUC-1 (072+101)
87. ⬜ Mvt 4: arena fairness methodology (136)
88. ⬜ Mvt 4: verify page spec (140)

## PHASE F — VERIFY / AUDIT / ALIGN / MANIFEST (89–100)
89. ⬜ hash-anchor all new files
90. ⬜ update MACHINE-TRUTH-MANIFEST (add session 2 artifacts)
91. ⬜ grammar self-audit (banned strings = 0)
92. ⬜ required-grammar present check
93. ⬜ correction ledger supersession chain intact
94. ⬜ cross-file consistency (dates/REAL tags)
95. ⬜ INDEX.md refresh (new files)
96. ⬜ TOP_DOWN_ALIGNMENT refresh (EAT results)
97. ⬜ PHASES.md refresh (phase status)
98. ⬜ kill-switch/restore drill note
99. ⬜ final honest-gates report
100. ⬜ SIGIL / commit-by-name note (never git add -A)
