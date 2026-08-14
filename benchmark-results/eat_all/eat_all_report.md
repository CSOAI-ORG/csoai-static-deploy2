# EAT_ALL Run Report

**Run ID**: eat_all_1786717895
**Finished**: 2026-08-14T14:31:35.725465+00:00
**Phase summary**: {'ran': 13, 'failed': 6, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 39.5s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_status=unreachable: Command '['ollama', 'list']' timed out after 5 seconds; kb_entries=9224 |
| PHASE_1_REBOARD | ran | 9.9s | exit_code=0 |
| PHASE_2_KB_GROW | failed | 8.7s | ~~~~~~~~~~~~~~~~~~~^^^
  File "/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/jso |
| PHASE_3_PROBES | ran | 0.6s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.3s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 40.9s | exit_code=0; events=4676 |
| PHASE_6_DOWNLOADS | failed | 14.8s | (no error message) |
| PHASE_7_PORTAL | ran | 33.8s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 45.8s | deck_cards=55; kb_entries=9225; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 12.7s | clans_routed=0; swarm_id=owem-clans-1786717732 |
| PHASE_9C_OWEM_CLUSTER | ran | 14.9s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 13.8s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 13.6s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 9.0s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | failed | 10.1s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9H_SOV_HIVE_HARNESS | failed | 9.6s | Extra data: line 298535 column 2 (char 12816009) |
| PHASE_9I_SOV_CAPTURE | failed | 53.3s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--status']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 23.8s | iwm_records=0; kb_entries_added=0; exit_code=1 |
| PHASE_10B_MODEL_ROUTING | failed | 11.9s | Extra data: line 298535 column 2 (char 12816009) |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`