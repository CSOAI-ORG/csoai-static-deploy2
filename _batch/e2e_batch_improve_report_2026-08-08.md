# e2e BATCH IMPROVE-REPORT — 2026-08-08 (JEEVES, csoai-static-deploy2)

Directive: plan → auto-batch all e2e → test → improve.
Runner: `_batch/run_e2e_batch.py` (serial, timeout-bounded). All local, zero spend.

## Result summary (first pass)

| Status | Count | Scripts |
|---|---|---|
| PASS | 6 | sov_e2e, self_test_5bench, test_provbench_three_outcomes, test_sov_runtime_alignment, spine_accuracy_test, sov_master_scenarios |
| FAIL | 1 | **test_trust_layer** (integrity alarm — see below) |
| DATA-GATED | 1 | diversity_e2e (no 15-dim govbench scores present) |
| INFRA-GATED (held) | 17 | ollama/GPU/RunPod/Kaggle/Oracle/cloud — not run |

## Improve: finding 1 — test_trust_layer integrity alarm (NOT a bug to patch)

`test_trust_layer.py:79-89` enforces a **floor on the battery denominator**, not just the score:

- The care-floor battery must have **≥ 55 hard items** (`check(len(BATTERY) >= 55)`).
- **Current deploy2 battery = 45 items** (only commit f40eb8d, 2026-07-29). The SEED V2 block of 10
  hard `should_breach=1` euphemism/fragmented items (added 2026-07-30, 45→55) was an **uncommitted
  working-tree edit that is LOST** — it never reached git. With the hard items gone, recall reads a
  misleading `1.000` (and over-block `0.000`), which is exactly the anti-Goodhart violation this
  whole stack exists to prevent.
- The test comment states the honest readings: with the hard items present, tier1 recall = `0.683`
  and over-block reads correctly. The battery at 45 is NOT comparable/championable.

**Canonical source located:** `~/clawd/_own-models-completion/care_battery.py` holds a **76-row**
battery — strictly richer (adds Art-5 facial-scrape / biometric-categorise / individual-predict,
self-harm, cyber-offense, robotics categories). **31 rows** present there are missing from the 45-row
deploy2 battery, including the hard euphemism/fragmented/fragmented-fragment items tier1 misses.

### Decision required (Nick / owner) — DO NOT relax the guard
This is a **multi-file, safety-critical refusal-detection change** (care_battery + tier1 scorer +
flywheel battery consumer + two-sided metric), with a genuine canonical-source ambiguity (deploy2
45-row vs sibling 76-row). Per AGENTS.md it earns a plan, not a silent commit. Options:

- **A (recommended):** align deploy2 battery to the 76-row canonical (or restore a ≥55 hard subset),
  then **improve tier1** so recall meets the 0.85 floor with hard items present. This is the
  everything-honest path the test was built to force. No spend.
- **B:** keep 45-row battery and **lower the 55-floor** — REJECTED here on principle (that is the
  anti-Goodhart violation; the test exists to catch it).
- **C:** treat test_trust_layer as red/known-issue and defer until owner confirms canonical battery.

I have NOT modified `care_battery.py`, `test_trust_layer.py`, or the tier1 scorer. The alarm stands.

## Improve: finding 2 — diversity_e2e is data-gated, not buggy

`diversity_e2e.py` returns exit 1 with "No model scores found" because `benchmark-results/govbench`
contains only 2 qwen files + a spine file — no full 15-dimension multi-model run is present this
session. It is a correct compute-only module awaiting a full benchmark input. Reclassified as
DATA-GATED in the runner (clean "no data" is not a defect).

## Improve: wire-in (P1 already landed this session)
- `sov_pipeline.py` flywheel branch now strips held-out cells at the honey-writer choke point
  (Law 2 enforcement); guard test `tests/test_flywheel_honey_leak.py` green on 11 artefacts.
- Batch runner now distinguishes LOCAL / SELF / DATA-GATED / INFRA-GATED honestly.

## Next (after this report)
1. Owner decides finding 1 (option A recommended) — the only open integrity gate for a clean batch.
2. Re-run batch → expect 7 PASS (test_trust_layer green once battery+scorer aligned) + 1 data-gated.
3. Then P2: two-sided refusal metric (arXiv 2512.12066) before any RunPod/GPU spend.

🜏 SIGIL: BATCH-E2E-2026-08-08-JEEVES (pending sign)
