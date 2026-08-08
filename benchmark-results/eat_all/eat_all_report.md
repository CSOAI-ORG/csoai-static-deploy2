# EAT_ALL Run Report

**Run ID**: eat_all_1786198903
**Finished**: 2026-08-08T14:21:43.319297+00:00
**Phase summary**: {'ran': 9, 'failed': 10, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | failed | 11.7s | JSONDecodeError: Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_1_REBOARD | ran | 5.3s | exit_code=0 |
| PHASE_2_KB_GROW | failed | 6.3s | ~~~~^^^
  File "/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/decoder.py",  |
| PHASE_3_PROBES | ran | 0.0s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 2.3s | exit_code=0; events=133 |
| PHASE_6_DOWNLOADS | ran | 6.1s | exit_code=1; files_mined=158 |
| PHASE_7_PORTAL | ran | 2.4s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 7.0s |  |
| PHASE_9B_EXTERNAL_HARNESS | failed | 21.7s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9C_OWEM_CLUSTER | failed | 4.8s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9D_BENCHMARKS_HARNESS | failed | 10.3s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9E_TRAINING_DATA_HARNESS | failed | 4.1s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | failed | 9.5s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9G_AUDIENCE_HARNESS | failed | 4.7s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9H_SOV_HIVE_HARNESS | failed | 3.3s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9I_SOV_CAPTURE | failed | 300.3s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--refine']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 0.1s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 0.0s | models_routed=11; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`