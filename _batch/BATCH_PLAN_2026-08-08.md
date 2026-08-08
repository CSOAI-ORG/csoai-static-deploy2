# BATCH PLAN — next 100 moves (JEEVES, csoai-static-deploy2)

Directive: *plan the next 100 moves, auto-batch all e2e, test, then improve.*
Session: 2026-08-08. Zero-spend default; RunPod cap ~$5 only if audit-justified and later approved.

## Phase 0 — Integrity precondition (DONE this session)
- [x] P1 honey-leak fix: `sov_pipeline.py` flywheel branch strips held-out cells before any
      honey write. Guard test `tests/test_flywheel_honey_leak.py` green (11 real artefacts).
- [x] flywheel.py self-test 9/9.

## Move 1–10 — Assemble the batch
1. Classify every `*e2e*.py` / `*_test*.py` / selftest into: LOCAL (runnable now, no infra) ·
   INFRA-GATED (needs RunPod/GCP/Oracle/Kaggle/billing) · SELF (unit/deterministic).
2. Write `_batch/run_e2e_batch.py` — discovers scripts, runs LOCAL ones serially with timeout,
   reports PASS/FAIL/SKIP + wall-time, writes JSONL + MD report.
3. Dry-run discovery: inventory count of each class.
4. Run the LOCAL batch (auto, serialized, timeout-bounded). Capture per-script result.
5. Aggregate results → `_batch/e2e_batch_report_2026-08-08.md`.
6. Parse failures → tag each with root-cause (import error / env / logic / infra).
7. Fix import/logic failures (free, local).
8. Re-run the affected scripts to confirm green.
9. Update the batch report with before→after.
10. Promote report to `_alignment/` as BATCH_E2E_2026-08-08.md.

## Move 11–40 — Test hardening (science-driven, free)
11. Add two-sided refusal metric (TPR + false-refusal) per arXiv 2512.12066 — seed/temperature aggregation.
12. Verify tokens_per_correct surfaced as the novel metric in scorecard narrative (Q5).
13. Assert salt immutability posture in docs (resolve IP_NOTICE rotatability claim → immutable v1).
14. Re-run self_test_5bench.py; confirm the updated "ONLY writer" claim is now structurally true.
15. Wire the honey-leak guard into self_test_5bench.py battery (so CI runs it).
16–20. Contamination detectors (arXiv 2510.09259): add output-distribution leak probe to flywheel.
21–30. Extend honey KB GNN/NN training to consume the practice-only cells (now that leak is closed).
31–40. Expand care battery cover (benign-near coverage) for the two-sided metric.

## Move 41–70 — e2e + parity + greenfield (infra-aware)
41–50. Run parity_e2e, sov_e2e, sovspace_e2e, gspc_six_axis_e2e where infra permits; record gated ones.
51–60. greenfield_e2e + unified_free_pipeline (free-lane only).
61–70. coverage_status re-run; cross-check against anchored 96-model spread (ALIGNMENT_2026-08-02 §1.5).

## Move 71–90 — Improve / document / promote
71–80. Record learnings in notes.md; promote durable findings to MEMORY.md.
81–90. Draft P2 two-sided-metric change + RunPod bounded SFT re-measure as an owner-gated proposal.

## Move 91–100 — Report + gate
91–95. Final batch summary with metrics (scripts run / pass / fail / gated / time).
96–100. Present to Nick: what shipped, what's gated (RunPod/billing), next decision (P2 + spot spend).

## Legal + spend guardrails
- All measurement is of PUBLIC data / own infra / published benchmarks (per goal doc §legal).
- No unauthorized probing, no kinetic/surveillance patterns. Zero-spend unless owner approves spot.
- Do not touch `sov-brain-2` HF cache (sibling-lane risk); never `git add -A` (mega-repo guard).
