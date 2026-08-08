# EAT_ALL Run Report

**Run ID**: eat_all_1786199118
**Finished**: 2026-08-08T14:25:18.806939+00:00
**Phase summary**: {'ran': 13, 'failed': 6, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | failed | 2.3s | JSONDecodeError: Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_1_REBOARD | ran | 0.1s | exit_code=0 |
| PHASE_2_KB_GROW | failed | 1.4s | ~~~~^^^
  File "/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/decoder.py",  |
| PHASE_3_PROBES | ran | 0.0s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 0.2s | exit_code=0; events=133 |
| PHASE_6_DOWNLOADS | ran | 5.9s | exit_code=1; files_mined=158 |
| PHASE_7_PORTAL | ran | 0.1s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 1.0s |  |
| PHASE_9B_EXTERNAL_HARNESS | failed | 1.8s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9C_OWEM_CLUSTER | failed | 2.4s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9D_BENCHMARKS_HARNESS | failed | 1.5s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 0.0s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 0.0s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 0.0s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 0.2s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 300.5s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--refine']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 0.1s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 0.0s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`