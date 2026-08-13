# EAT_ALL Run Report

**Run ID**: eat_all_1786631279
**Finished**: 2026-08-13T14:27:59.928739+00:00
**Phase summary**: {'ran': 18, 'failed': 1, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 19.5s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_status=unreachable: Command '['ollama', 'list']' timed out after 5 seconds; kb_entries=7872 |
| PHASE_1_REBOARD | ran | 2.9s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 1.0s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.0s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 6.5s | exit_code=0; events=4116 |
| PHASE_6_DOWNLOADS | ran | 8.6s | exit_code=0; files_mined=271 |
| PHASE_7_PORTAL | ran | 2.9s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 10.3s | deck_cards=55; kb_entries=7872; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 15.5s | clans_routed=0; swarm_id=owem-clans-1786631171 |
| PHASE_9C_OWEM_CLUSTER | ran | 9.5s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 2.9s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 5.7s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 2.7s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 4.0s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 10.7s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 50.5s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--status']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 15.5s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 0.7s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`