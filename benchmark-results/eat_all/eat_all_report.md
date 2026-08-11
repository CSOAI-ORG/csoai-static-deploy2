# EAT_ALL Run Report

**Run ID**: eat_all_1786460000
**Finished**: 2026-08-11T14:53:20.323586+00:00
**Phase summary**: {'ran': 17, 'failed': 2, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 8.7s | sov_local_status=unreachable: HTTP Error 404: Not Found; ollama_models=2; kb_entries=4516 |
| PHASE_1_REBOARD | ran | 7.4s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 3.1s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.1s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 9.6s | exit_code=0; events=2773 |
| PHASE_6_DOWNLOADS | failed | 7.0s | (no error message) |
| PHASE_7_PORTAL | ran | 19.6s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 6.3s | deck_cards=54; kb_entries=4524; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 2.3s | clans_routed=0; swarm_id=owem-clans-1786459895 |
| PHASE_9C_OWEM_CLUSTER | ran | 1.9s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 1.6s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 1.9s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 2.2s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 2.2s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 26.4s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 43.4s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--status']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 16.7s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 7.9s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`