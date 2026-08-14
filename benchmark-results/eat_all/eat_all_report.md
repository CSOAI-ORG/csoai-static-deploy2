# EAT_ALL Run Report

**Run ID**: eat_all_1786735747
**Finished**: 2026-08-14T19:29:07.347940+00:00
**Phase summary**: {'ran': 8, 'failed': 11, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | failed | 3.7s | JSONDecodeError: Extra data: line 298535 column 2 (char 12816009) |
| PHASE_1_REBOARD | ran | 10.7s | exit_code=0 |
| PHASE_2_KB_GROW | failed | 29.5s | ts-to-kb.py", line 196, in main
    kb = json.loads(kb_path.read_text())
  File "/Library/Frameworks |
| PHASE_3_PROBES | ran | 0.1s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 67.2s | exit_code=0; events=4796 |
| PHASE_6_DOWNLOADS | failed | 105.0s | (no error message) |
| PHASE_7_PORTAL | ran | 15.0s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 2.4s | deck_cards=0 |
| PHASE_9B_EXTERNAL_HARNESS | failed | 2.9s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9C_OWEM_CLUSTER | failed | 0.4s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9D_BENCHMARKS_HARNESS | failed | 0.4s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9E_TRAINING_DATA_HARNESS | failed | 0.4s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | failed | 0.3s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9G_AUDIENCE_HARNESS | failed | 0.4s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9H_SOV_HIVE_HARNESS | failed | 0.2s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9I_SOV_CAPTURE | ran | 3.8s | events_processed=0; skills_extracted=0 |
| PHASE_9J_IWM_BOOTSTRAP | ran | 0.6s | iwm_records=0; kb_entries_added=0; exit_code=1 |
| PHASE_10B_MODEL_ROUTING | failed | 0.2s | Extra data: line 298535 column 2 (char 12816009) |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`