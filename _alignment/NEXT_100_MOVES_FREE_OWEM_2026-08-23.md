# NEXT 100 MOVES — free OWEM routing + online/offline backend (2026-08-23, round 2)
Grounded on: free cross-eval (sovereign 0.75 > free frontier 0.0, zero credits), free sov-router
(built, compute-bound), offline-index sync wired, online pod :11434 + bench :11435, KB 5,726, 732 boards.

## BLOCK 1 — COMPLETE THE FREE OWEM ROUTER (moves 1-20)
1. Finish the free-sov-router measurement run (6 axes x 4 sov models) on the dedicated bench server.
2. Wire the completed route table into /api/model-router (agents ask "best sov model for axis X").
3. Add per-axis scores to free_sov_router.json (honest, from our GSPC measurement).
4. Add auto-retry + per-probe timeout (survive the flaky inference; no 0.000-from-timeout).
5. Measure all 23 GSPC axes (not just the 6 probes) so the router is complete per-axis.
6. Add a cost column (all £0 — our sov models) + latency column (measured).
7. Publish the sov-router at /api/model-router (Council OS surface).
8. Wire sov-router into agent-catalog (/api/tools) as a discovery tool.
9. Hard-code a fallback route (if measurement missing, default to sov33-unified).
10. Re-run the router weekly (models drift) — wire to a timer.

## BLOCK 2 — WIRE THE FREE ROUTING INTO THE ENGINE (moves 11-30)
11. Route measure_chain's jobs by the sov-router (measure each axis with its best sov model).
12. Route the improve-loop's mutation + measure through the sov-router.
13. Add a "route" step to the EAT loop (measure->route->sign->chain->board).
14. Score the routed measurement vs the un-routed baseline (does routing help? honest delta).
15. Keep routing only if it > baseline (ouroboros gate).
16. Build a sov-router audit trail (which route won each axis, signed).
17. Chain the route decisions into the estate (EAT anchor).
18. Add fallback routing: if a sov model is down, fall to the next-best (never drop).
19. Monitor per-route latency + accuracy (degrade detection).
20. Re-route if a model's accuracy drifts (measurement-aware routing).

## BLOCK 3 — ONLINE/OFFLINE RESILIENCE (moves 21-45)
21. Verify the offline-index sync fires each batch cycle (board/KB/genome -> RAG).
22. Add a restore path: if online index is lost, restore from the offline RAG copy (drill).
23. Add a 2nd offline target (Oracle /evac-bulk when it's up — cross-host redundancy).
24. Ensure the remote backup host (213.173.105.83:25804) receives the daily EAT tar.
25. Verify offline index JSON is valid after sync (no partial write).
26. Add a checksum to the offline index (detect corruption).
27. Add change-detection: only sync when the KB changed (avoid redundant copies).
28. Build a bootstrap-from-offline script (the estate can come up from the RAG volume alone).
29. Test the offline bootstrap (simulate online loss -> offline restore works).
30. Add an online/offline health endpoint (/api/index-health) reporting both states.

## BLOCK 4 — KAGGLE FREE-GPU (moves 31-55)
31. Copy the Kaggle token (Mac) to the pod so Kaggle API works.
32. Auth: kaggle competitions/datasets list (confirm the token works).
33. Find a free-GPU Kaggle benchmark dataset (the "scrape their data" for flywheel fuel).
34. Mine a Kaggle dataset -> convert to honey/KB entries (free fuel).
35. Build a Kaggle GPU runner (submit a benchmark notebook/script to run on Kaggle's free T4/P100).
36. Split our GSPC cross-eval across Kaggle free-GPU + pod (parallel benchmark compute).
37. Harvest Kaggle public model-eval outputs as frontier reference (synthesize vs benchmarks).
38. Download a frontier model's  eval results -> compare vs our sov (honest).
39. Add Kaggle as an offline-compute source (when pod GPU is busy).
40. Chain the Kaggle-mined results into the KB (free flywheel fuel).
41. Dedup Kaggle honey into the KB (sha256).
42. Measure the Kaggle-mined KB (signed).
43. Use Kaggle free-GPU to run the slow improve-loop cycles (offload compute).
44. Store Kaggle model outputs on the RAG volume (offline).
45. Add a Kaggle quota guard (stay under free tier).

## BLOCK 5 — SYNTHESIZE BENCHMARK-vs-BENCHMARK (moves 56-75)
46. Build a benchmark-notebook synthesis: our sov scores vs frozen baselines (DORADO gate + law-RAG).
47. Compare sovereign vs frontier on each GSPC axis (honest, same grader).
48. Identify axes where frontier beats us (the gaps to improve).
49. Identify axes where we beat frontier (the moat).
50. Build a "gap map" (per-axis sov-vs-frontier) published honestly.
51. Use the gap map to prioritize which axis's sov model to improve first.
52. For each gap axis: collect failure vectors (exact GSPC errors).
53. QLoRA fine-tune a sov variant on those failures (real weights).
54. Re-measure base vs variant (ouroboros: keep only if GSPC improved).
55. Repeat per gap-axis (iterate the self-improvement).

## BLOCK 6 — IMPROVE OURS (the sov family) (moves 76-90)
56. Inventory + measure all sov variants on all 23 axes (baseline).
57. Build the per-axis sov champion (one variant wins each axis).
58. Add law-RAG + DORADO gate to the champion (0.937 GOVBENCH build) for the compliance axes.
59. Distil a frontier capability into a sov variant (from the free-cross-eval reference).
60. Measure distillation transfer (did it help or hurt? honest).
61. Build a safety-first sov variant (refusal precision, no over-block).
62. Publish the sov family as measured MCP/PyPI products.
63. Route the live board through the improved sov champion per axis.
64. Re-measure the board after the improvement (did scores move? honest).
65. Chain + sign every improved model card.

## BLOCK 7 — E2E + AUTONOMOUS LOOP (moves 91-100)
66. Full E2E: free-sov-route a probe -> GSPC score -> sign -> chain -> board -> /api.
67. Verify /api/model-router + /api/gspc show the free-routed results.
68. Run Claims-E2E + pre-deploy smoke (all user types).
69. Auto-batch run: mine->route->measure->test->audit->re-batch (continuous).
70. Verify the EAT 7-box: measured, CI, signed, chained, anchored, boarded, mirrored.
71. Wire a nightly improve-batch timer (the loop compounds without a human).
72. Harden the inference serving layer (the flaky llama-server -> dedicated runners).
73. Drift-guard the free model catalog (sov + OpenRouter-free change).
74. Audit cost of improvement vs value (is the fine-tune worth it?).
75. Publish the honest improvement report (what worked, what didn't).
76. Owner-gated: Kaggle quota, Oracle OWEM creds, OpenRouter credits (optional upgrade).

## VERIFICATION DOCTRINE (unchanged)
- Measurement, not certification. Honest negatives published.
- Ouroboros gate: keep a variant only if GSPC genuinely improves (no reward-hacking).
- Free-first: our sov/OWEM family is the substrate; OpenRouter credits optional, never required.
- Online/offline: every index has a durable offline copy; the estate never loses state.
- Work from the pod; Mac is a thin terminal. EAT loop autonomous.
