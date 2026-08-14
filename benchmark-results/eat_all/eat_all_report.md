# EAT_ALL Run Report

**Run ID**: eat_all_1786727874
**Finished**: 2026-08-14T17:17:54.028743+00:00
**Phase summary**: {'ran': 9, 'failed': 10, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | failed | 15.7s | JSONDecodeError: Extra data: line 298535 column 2 (char 12816009) |
| PHASE_1_REBOARD | ran | 22.6s | exit_code=0 |
| PHASE_2_KB_GROW | failed | 21.5s | ts-to-kb.py", line 196, in main
    kb = json.loads(kb_path.read_text())
  File "/Library/Frameworks |
| PHASE_3_PROBES | ran | 1.2s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 51.0s | exit_code=0; events=4716 |
| PHASE_6_DOWNLOADS | ran | 12.4s | exit_code=0; files_mined=296 |
| PHASE_7_PORTAL | ran | 4.6s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 2.5s | deck_cards=0 |
| PHASE_9B_EXTERNAL_HARNESS | failed | 0.8s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9C_OWEM_CLUSTER | failed | 1.0s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9D_BENCHMARKS_HARNESS | failed | 2.0s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9E_TRAINING_DATA_HARNESS | failed | 1.9s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | failed | 1.2s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9G_AUDIENCE_HARNESS | failed | 1.7s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9H_SOV_HIVE_HARNESS | failed | 4.1s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9I_SOV_CAPTURE | ran | 13.9s | events_processed=0; skills_extracted=0 |
| PHASE_9J_IWM_BOOTSTRAP | ran | 2.4s | iwm_records=0; kb_entries_added=0; exit_code=1 |
| PHASE_10B_MODEL_ROUTING | failed | 0.8s | Extra data: line 298535 column 2 (char 12816009) |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`