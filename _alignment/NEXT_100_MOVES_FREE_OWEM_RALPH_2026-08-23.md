# NEXT 100 MOVES — free OWEM routing + online/offline backend + improve OURS (2026-08-23, ralph)
Foundation verified: free cross-eval (sovereign 0.75 > free frontier 0.0, £0), free sov-router (build),
offline-index sync wired, online pod :11434 + bench :11435, KB 5,726 signed, 732 boards, EAT loop durable
(supervisor/measure/keeper/referee/ops_daemons all PPID=1, auto-run overnight).

## BLOCK 1 — COMPLETE THE FREE OWEM ROUTER (moves 1-12)
1. Finish the sov-router per-axis measurement (all 23 axes, not just 6).
2. Persist free_sov_router.json (per-axis best sov model + scores).
3. Wire it into /api/model-router (agents ask "best sov model for axis X").
4. Add latency + £0 cost per route (measured, honest).
5. Retry-on-drop per probe (no 0.000-from-timeout; the flaky inference).
6. Default fallback route (sov33-unified if measurement missing).
7. Publish /api/model-router to Council OS + add as /api/tools discovery entry.
8. Re-measure the router weekly (models drift) — timer.
9. Audit: does routed measurement beat un-routed? (ouroboros gate).
10. Keep routing only if > baseline.
11. Sign + chain the route decisions (EAT anchor).
12. Add degrade-detection (re-route if accuracy drifts).

## BLOCK 2 — WIRE FREE ROUTING INTO THE ENGINE (moves 13-30)
13. Route measure_chain jobs by the sov-router (best sov model per axis).
14. Route the improve-loop mutation + measure through the sov-router.
15. Add "route" as an EAT step (measure->route->sign->chain->board).
16. Score routed vs un-routed (honest delta).
17. Fallback routing: next-best sov model if one is down (never drop).
18. Monitor per-route latency + accuracy (degrade).
19. Build a sov-router audit trail (which route won each axis).
20. Measure the route win-rate per axis (does routing help?).
21. Wire router priority: ovx sov champion per axis.
22. Add a route fallback to base model (safe default).
23. Chain route decisions into the board.
24. Add route-aware measure (measure each axis with its champion).
25. Improve-loop uses the champion per axis (mutation + measure).
26. Re-measure after route-improvement (did scores lift? honest).
27. Keep route+improve only if the axis score rose (ouroboros).
28. Persist the per-axis champion map.
29. Add a routing-scorecard endpoint.
30. Publish route-win-rate to the board.

## BLOCK 3 — ONLINE/OFFLINE RESILIENCE (moves 31-48)
31. Verify offline-index sync fires each batch cycle (KB/genome/board -> RAG).
32. Add restore-from-offline path (drill: simulate online loss -> offline bring-up).
33. Add checksum to offline index (corruption detect).
34. Add change-detection (only sync on KB change).
35. Add a 2nd offline target (Oracle /evac-bulk when up).
36. Ensure remote backup host (213.173.105.83) receives daily EAT tar.
37. Bootstrap-from-offline script (estate comes up from RAG alone).
38. Test the offline bootstrap drill.
39. Add /api/index-health (reports online+offline state).
40. Add a daily offline-index verify (checksum + count).
41. Mirror the CBX sov weights to the RAG volume (offline model copy).
42. Add model-weight offline backup (sov variants).
43. Add a restore drill for model weights.
44. Verify the backup/offline cycle (tar -> RAG -> restore).
45. Add hot standby: second pod/endpoint for the index.
46. Cross-host replicate KB to the 2nd host.
47. Simulate an online outage (drop pod) -> offline serve test.
48. Confirm the estate serves from offline during an outage.

## BLOCK 4 — KAGGLE FREE-GPU + DATA MINING (moves 49-70)
49. Copy Kaggle token (Mac) to the pod.
50. Auth Kaggle (competitions/datasets list).
51. Mine a Kaggle public dataset -> honey/KB entries (free fuel).
52. Convert Kaggle entries into KB (dedup sha256).
53. Build a Kaggle GPU runner (submit benchmark to free T4/P100).
54. Split the cross-eval across Kaggle + pod (parallel).
55. Harvest Kaggle model-eval outputs as frontier reference.
56. Download a frontier eval -> compare vs our sov (honest).
57. Add Kaggle as an offline-compute source.
58. Chain the Kaggle-mined records into the KB.
59. Measure + sign the Kaggle-mined KB.
60. Offload slow improve-loop cycles to Kaggle free-GPU.
61. Store Kaggle outputs on the RAG volume (offline).
62. Add a Kaggle quota guard (stay free).
63. Keep a monthly Kaggle dataset-drift scan (new datasets).
64. Mine Kaggle benchmark metadata as an eval-reference bank.
65. Synthesize benchmark-vs-benchmark across Kaggle + our sov.
66. Build the Frontier Reference Archive (Kaggle + free-OR evals, honest).
67. Add the reference bank to llms.txt (agents discover it).
68. Measure how free-OR/Kaggle frontier performs vs our sov (gap map).
69. Wire the gap map into the improvement priority.
70. Monitor Kaggle free-tier quota (stop at limit).

## BLOCK 5 — SYNTHESIZE BENCHMARK-vs-BENCHMARK (moves 71-88)
71. Build the honest sov-vs-frontier leaderboard (same grader, real scores).
72. Compare per-axis across the sov family + free frontier.
73. Identify gap axes (frontier beats us) — the improvement targets.
74. Identify moat axes (we beat frontier) — the brand.
75. Publish the gap map (honest).
76. Prioritize the worst gap axis (fix what's wrong).
77. Collect error vectors on the gap axis (exact GSPC failures).
78. QLoRA fine-tune a sov variant on those failures.
79. Re-measure base vs variant (ouroboros).
80. Keep only if it improved.
81. Iterate the next gapless axis.
82. Add law-RAG + DORADO gate to the champion (compliance moat).
83. Distil a frontier capability into a sov variant.
84. Measure distillation transfer (help or hurt?).
85. Build a safety-first sov variant (refusal precision).
86. Publish the sov family as measured MCP/PyPI products.
87. Route the live board through the per-axis champion.
88. Re-measure the board after improvement (honest delta).

## BLOCK 6 — E2E + AUTONOMOUS OVERNIGHT (moves 89-100)
89. Full E2E: free-route probe -> GSPC score -> sign -> chain -> board -> /api.
90. Verify /api/model-router + /api/gspc show the free-routed results.
91. Run Claims-E2E + pre-deploy smoke (all user types).
92. Confirm the overnight auto-batch (mine->route->measure->test->audit->re-batch) sustains.
93. Verify EAT 7-box: measured, CI, signed, chained, anchored, boarded, mirrored.
94. Monitor the loop over an overnight window (boards/KB grow).
95. Harden inference (dedicated runners for the flaky llama-server).
96. Drift-guard the model catalog.
97. Audit cost-of-improvement vs value.
98. Publish the honest improvement report.
99. Owner-gated: Kaggle quota, Oracle OWEM creds, OpenRouter credits (optional).
100. Final 100/100 scorecard — every surface free-routed, measured, tested.

## DOCTRINE (unchanged)
- Measurement not certification; honest negatives published.
- Ouroboros: keep only if GSPC genuinely improves (no reward-hacking).
- Free-first: our sov/OWEM family is the substrate; OpenRouter credits optional never required.
- Online/offline: every index has a durable offline copy; never lose state.
- Ralph loop: fresh-agent iteration, workspace-as-memory, work from the pod.
