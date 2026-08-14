# CSOAI Canonical Bank-Count Registry

Generated: 2026-08-14T03:24:16.974630+00:00 · live pull from Hugging Face API, sha256-pinned per file

**Doctrine: the file is the truth, not the card.** rows = all parsed lines · real = rows minus canary (any truthy `_canary`/`canary` value, bool or GUID string) · labels = first present of gold/label/verdict/expected/class · n30 = the n≥30 quotable floor

| dataset | file | rows | real | canary | dupes | n≥30 | labels (top) |
|---|---|---|---|---|---|---|---|
| agisafe-bench | items.jsonl | 14 | 14 | 0 | — | ⚠️ | expected=REFUSE:7, expected=COMPLY:7 |
| ai-act-flywheel-master-corpus | honey_master_pairs_2026-08-03.jsonl | 6991 | 6991 | 0 | 6946 | ✅ |  |
| aiact-frozen-split-harness | scenarios.jsonl | 339 | 339 | 0 | — | ✅ |  |
| arc-easy-family-sweep-2026-08-03 | — | — | — | — | — | — | no .jsonl |
| arena-matrices | — | — | — | — | — | — | no .jsonl |
| asisec-bench | — | — | — | — | — | — | no .jsonl |
| coai-bench | sov_signal.jsonl | 24 | 24 | 0 | — | ⚠️ |  |
| compbench | — | — | — | — | — | — | no .jsonl |
| csoai-benchmarks | — | — | — | — | — | — | no .jsonl |
| gspc-affect | items.jsonl | 42 | 41 | 1 | — | ✅ | expected=PROHIBITED:18, expected=PERMITTED:12, expected=DISCLOSE:11 |
| gspc-agi | items.jsonl | 37 | 36 | 1 | — | ✅ | expected=COMPLY:19, expected=REFUSE:17 |
| gspc-airbench-eu-mandatory-run | airbench_full_checkpoint.jsonl | 1181 | 1181 | 0 | — | ✅ | verdict=REFUSED:585, verdict=COMPLIED:542, verdict=UNMEASURED:54 |
| gspc-airbench-eu-mandatory-run | eu_mandatory.jsonl | 3402 | 3402 | 0 | 2 | ✅ |  |
| gspc-arena-results | — | — | — | — | — | — | no .jsonl |
| gspc-art5 | items.jsonl | 37 | 36 | 1 | — | ✅ | expected=PERMITTED:19, expected=PROHIBITED:17 |
| gspc-asi | items.jsonl | 34 | 33 | 1 | — | ✅ | expected=QUANTUM_SAFE:13, expected=NOT_APPLICABLE:11, expected=QUANTUM_VULNERABLE:9 |
| gspc-boards | peritem_affect.jsonl | 0 | 0 | 0 | — | ⚠️ |  |
| gspc-boards | peritem_agi.jsonl | 144 | 144 | 0 | — | ✅ | expected=COMPLY:76, expected=REFUSE:68 |
| gspc-boards | peritem_art5.jsonl | 144 | 144 | 0 | — | ✅ | expected=PERMITTED:76, expected=PROHIBITED:68 |
| gspc-boards | peritem_asi.jsonl | 132 | 132 | 0 | — | ✅ | expected=QUANTUM_SAFE:52, expected=NOT_APPLICABLE:44, expected=QUANTUM_VULNERABLE:36 |
| gspc-boards | peritem_care.jsonl | 800 | 800 | 0 | — | ✅ | expected=1:400, expected=0:400 |
| gspc-boards | peritem_det.jsonl | 132 | 132 | 0 | — | ✅ | expected=INTEROPERABLE:104, expected=DIVERGENT:28 |
| gspc-boards | peritem_gov.jsonl | 1185 | 1185 | 0 | — | ✅ | expected=MINIMAL_RISK:345, expected=HIGH_RISK:295, expected=LIMITED_RISK:295, expected=PROHIBITED:250 |
| gspc-boards | peritem_jail.jsonl | 2592 | 2592 | 0 | — | ✅ | verdict=PASS:2589, verdict=FAIL:3 |
| gspc-boards | peritem_mach.jsonl | 132 | 132 | 0 | — | ✅ | expected=PART_A:48, expected=OUT_OF_SCOPE:48, expected=NOT_SAFETY_FUNCTION:36 |
| gspc-boards | peritem_mcp.jsonl | 140 | 140 | 0 | — | ✅ | expected=CONFORMS:72, expected=VIOLATES:68 |
| gspc-boards | peritem_oss.jsonl | 128 | 128 | 0 | — | ✅ | expected=PERMITTED:64, expected=RESTRICTED:64 |
| gspc-boards | peritem_prv.jsonl | 128 | 128 | 0 | — | ✅ | expected=SURVIVES:68, expected=DESTROYED:60 |
| gspc-boards | peritem_swarm.jsonl | 164 | 164 | 0 | — | ✅ | expected=CONSENSUS_CORRECT:156, expected=CONSENSUS_WRONG:4, expected=CANARY:4 |
| gspc-boards | peritem_xr.jsonl | 128 | 128 | 0 | — | ✅ | expected=CONFIRM:52, expected=REFUSE:44, expected=PROCEED:32 |
| gspc-boards | v2/peritem_affect.jsonl | 779 | 779 | 0 | — | ✅ | expected=PROHIBITED:342, expected=PERMITTED:228, expected=DISCLOSE:209 |
| gspc-boards | v2/peritem_agi.jsonl | 684 | 684 | 0 | — | ✅ | expected=COMPLY:361, expected=REFUSE:323 |
| gspc-boards | v2/peritem_art5.jsonl | 684 | 684 | 0 | — | ✅ | expected=PERMITTED:361, expected=PROHIBITED:323 |
| gspc-boards | v2/peritem_asi.jsonl | 627 | 627 | 0 | — | ✅ | expected=QUANTUM_SAFE:247, expected=NOT_APPLICABLE:209, expected=QUANTUM_VULNERABLE:171 |
| gspc-boards | v2/peritem_care.jsonl | 3800 | 3800 | 0 | — | ✅ | expected=1:1900, expected=0:1900 |
| gspc-boards | v2/peritem_det.jsonl | 627 | 627 | 0 | — | ✅ | expected=INTEROPERABLE:494, expected=DIVERGENT:133 |
| gspc-boards | v2/peritem_gov.jsonl | 4503 | 4503 | 0 | — | ✅ | expected=MINIMAL_RISK:1311, expected=HIGH_RISK:1121, expected=LIMITED_RISK:1121, expected=PROHIBITED:950 |
| gspc-boards | v2/peritem_mach.jsonl | 627 | 627 | 0 | — | ✅ | expected=PART_A:228, expected=OUT_OF_SCOPE:228, expected=NOT_SAFETY_FUNCTION:171 |
| gspc-boards | v2/peritem_mcp.jsonl | 665 | 665 | 0 | — | ✅ | expected=CONFORMS:342, expected=VIOLATES:323 |
| gspc-boards | v2/peritem_oss.jsonl | 608 | 608 | 0 | — | ✅ | expected=PERMITTED:304, expected=RESTRICTED:304 |
| gspc-boards | v2/peritem_prv.jsonl | 608 | 608 | 0 | — | ✅ | expected=SURVIVES:323, expected=DESTROYED:285 |
| gspc-boards | v2/peritem_swarm.jsonl | 760 | 760 | 0 | — | ✅ | expected=CONSENSUS_CORRECT:741, expected=CONSENSUS_WRONG:19 |
| gspc-boards | v2/peritem_xr.jsonl | 608 | 608 | 0 | — | ✅ | expected=CONFIRM:247, expected=REFUSE:209, expected=PROCEED:152 |
| gspc-care | items.jsonl | 201 | 200 | 1 | 1 | ✅ | expected=1:100, expected=0:100 |
| gspc-det | items.jsonl | 34 | 33 | 1 | — | ✅ | expected=INTEROPERABLE:26, expected=DIVERGENT:7 |
| gspc-det | protocol.jsonl | 6 | 6 | 0 | — | ⚠️ |  |
| gspc-gov | items.jsonl | 238 | 237 | 1 | — | ✅ | expected=MINIMAL_RISK:69, expected=HIGH_RISK:59, expected=LIMITED_RISK:59, expected=PROHIBITED:50 |
| gspc-jail | items.jsonl | 37 | 36 | 1 | — | ✅ | expected=CONFINED:36 |
| gspc-mach | items.jsonl | 34 | 33 | 1 | — | ✅ | expected=PART_A:12, expected=OUT_OF_SCOPE:12, expected=NOT_SAFETY_FUNCTION:9 |
| gspc-mcp | items.jsonl | 36 | 35 | 1 | — | ✅ | expected=CONFORMS:18, expected=VIOLATES:17 |
| gspc-normalized | — | — | — | — | — | — | no .jsonl |
| gspc-oss | items.jsonl | 33 | 32 | 1 | — | ✅ | expected=PERMITTED:16, expected=RESTRICTED:16 |
| gspc-papers | — | — | — | — | — | — | no .jsonl |
| gspc-prv | items.jsonl | 33 | 32 | 1 | — | ✅ | expected=SURVIVES:17, expected=DESTROYED:15 |
| gspc-swarm | items.jsonl | 41 | 40 | 1 | — | ✅ | expected=CONSENSUS_CORRECT:39, expected=CONSENSUS_WRONG:1 |
| gspc-swarm | protocol.jsonl | 6 | 6 | 0 | — | ⚠️ |  |
| gspc-xr | checks.jsonl | 8 | 8 | 0 | — | ⚠️ |  |
| gspc-xr | items.jsonl | 33 | 32 | 1 | — | ✅ | expected=CONFIRM:13, expected=REFUSE:11, expected=PROCEED:8 |
| hellaswag-pod-top-down-2026-08-03 | — | — | — | — | — | — | no .jsonl |
| lmeval-official-format | — | — | — | — | — | — | no .jsonl |
| mcp-scoreboard | items.jsonl | 11 | 11 | 0 | — | ⚠️ | expected=VIOLATES:6, expected=CONFORMS:5 |
| omai-bench | items.jsonl | 13 | 13 | 0 | — | ⚠️ | expected=PERMITTED:7, expected=RESTRICTED:6 |
| oowm-ground-truth-v2 | signed/train.signed.jsonl | 16 | 16 | 0 | — | ⚠️ |  |
| oowm-ground-truth-v2 | train.jsonl | 16 | 16 | 0 | — | ⚠️ |  |
| oowm-ground-truth-v3 | train.jsonl | 32 | 32 | 0 | — | ✅ |  |
| oowm-ground-truth-v3 | train.signed.jsonl | 32 | 32 | 0 | — | ✅ |  |
| oowm-ground-truth-v7 | sov_signal_v7.jsonl | 778 | 778 | 0 | 0 | ✅ |  |
| oowm-ground-truth-v7 | train.dualsigned.jsonl | 12 | 12 | 0 | — | ⚠️ |  |
| oowm-ground-truth-v7 | train.jsonl | 12 | 12 | 0 | — | ⚠️ |  |
| oowm-ground-truth-v7 | train.signed.jsonl | 12 | 12 | 0 | — | ⚠️ |  |
| oowm-ground-truth-v9 | balanced_v31/data.jsonl | 68448 | 68448 | 0 | 0 | ✅ |  |
| oowm-ground-truth-v9 | sov_signal.dualsigned.jsonl | 778 | 778 | 0 | 0 | ✅ |  |
| oowm-ground-truth-v9 | sov_signal/data.jsonl | 778 | 778 | 0 | 0 | ✅ |  |
| oowm-ground-truth-v9 | train/data.jsonl | 12 | 12 | 0 | — | ⚠️ |  |
| oowm-runtime | — | — | — | — | — | — | no .jsonl |
| oowm-sov-signal-v8 | data.jsonl | 778 | 778 | 0 | 0 | ✅ |  |
| oowm-sov-signal-v8 | sov_signal.dualsigned.jsonl | 778 | 778 | 0 | 0 | ✅ |  |
| oowm-substrate-v4 | — | — | — | — | — | — | no .jsonl |
| oowm-substrate-v5 | — | — | — | — | — | — | no .jsonl |
| poai-bench | — | — | — | — | — | — | no .jsonl |
| provbench-headline-2026-08-03 | — | — | — | — | — | — | no .jsonl |
| provbench-manifest-survival | — | — | — | — | — | — | no .jsonl |
| sov-signal-ground-truth-v10 | train.signed.jsonl | 1972 | 1972 | 0 | — | ✅ |  |
| sov-signal-ground-truth-v8 | train.jsonl | 1972 | 1972 | 0 | — | ✅ |  |
| sov-signal-ground-truth-v8 | train.signed.jsonl | 1972 | 1972 | 0 | — | ✅ |  |
| sov-signal-leaderboard-v1 | — | — | — | — | — | — | no .jsonl |
| sov33-pod-top-down-2026-08-03 | — | — | — | — | — | — | no .jsonl |
| sov33-v12-results | — | — | — | — | — | — | no .jsonl |
| sov34-1p5b-vs-baseline | — | — | — | — | — | — | no .jsonl |
| sov34-training-corpus | — | — | — | — | — | — | no .jsonl |

## Delta v0.3 — 2026-08-14 (~04:30 UTC)

Seven sub-floor banks topped up with law-anchored gold items in their existing schemas and re-verified by live pull: agisafe-bench 14→30, coai-bench 24→30, gspc-det/protocol 6→30, gspc-swarm/protocol 6→30, gspc-xr/checks 8→30, mcp-scoreboard 11→30, omai-bench 13→30. **Zero sub-floor measurement banks remain** (oowm-ground-truth train corpora and gspc-boards/peritem_affect.jsonl are excluded — training data and per-item result files are not gold banks; the affect per-item file fills when a board runs it). coai-bench additions carry measurement fields as UNMEASURED — no fabricated model results.
