# EAT_ALL Run Report

**Run ID**: eat_all_1786633023
**Finished**: 2026-08-13T14:57:03.442594+00:00
**Phase summary**: {'ran': 18, 'failed': 1, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | failed | 121.3s | PHASE TIMEOUT after 120s (daemon worker left to die with process) |
| PHASE_1_REBOARD | ran | 13.1s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 4.7s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.0s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 3.3s | exit_code=0; events=4136 |
| PHASE_6_DOWNLOADS | ran | 1.7s | exit_code=0; files_mined=271 |
| PHASE_7_PORTAL | ran | 3.2s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 4.6s | deck_cards=55; kb_entries=7896; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 1.8s | clans_routed=0; swarm_id=owem-clans-1786632953 |
| PHASE_9C_OWEM_CLUSTER | ran | 1.5s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 1.7s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 2.0s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 3.1s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 4.9s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 16.7s | kb_entries_added=14; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | ran | 20.1s | events_processed=0; skills_extracted=0; refine_output=KB Refinery — processing today's capture events...
  terminal: 10 events (refine window 500)
  browser: 0 events
  files: 0 events
  chat: 0 events
  KB: 7897 → 7897 entries (+0 new, dedup by normalized question)
  Saved to: /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/sov_kb.json
; extract_output=GNN Spine — extracting patterns from capture events...
  Extracted 0 unique skills
  Skills file: /Users/nicholas/.sov/iwm/skills_20260813.jsonl
  KB updated: 7897 entries total
 |
| PHASE_9J_IWM_BOOTSTRAP | ran | 9.1s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 10.9s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`