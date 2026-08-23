# D2026-08-09 — sov33-v12 champion locked + HF leaderboard V2 closed (JEEVES lane, evidence-cited)

## Headline
- **Champion sov33-v12 (Qwen2.5-1.5B + LoRA) locked at SOV-SIGNAL 69.07%** (472/473 graded, fully-graded via hardened M89 extractor; aggregate 66.33% over 1972 rows). +5.22 pts over prior champion v9 (63.85%); +26.71 pts over baseline sov33-unified (42.36%).

## HF Leaderboard V2 (lm_eval 0.4.12, bf16) — full 6-task table published
- Dataset: https://huggingface.co/datasets/csoai/sov33-v12-results (README + results.json + gpqa_results.json live)
| task | metric | score |
|---|---|---|
| BBH (27 subtasks) | acc_norm | 0.4088 |
| MMLU-Pro | acc | 0.2809 |
| MuSR | acc_norm | 0.4101 |
| IFEval | inst loose/strict | 0.4365 / 0.3825 |
| Math-Hard | exact_match | 0.0793 |
| GPQA (n=1192) | acc_norm | 0.3096 +/- 0.0134 |

Honest framing: 1.5B governance-specialist — reasoning scores low (expected); leadership is governance. SOV-SIGNAL per-axis Wilson95: conformance 1.0 / art5-safeguard 1.0 / provenance 0.938 / openness 0.906 / safety 0.829 / continuity 0.636 / governance 0.549 / cross-reality 0.500.

## Companion dataset
- `csoai/sov-signal-ground-truth-v10` — 1972 Ed25519-signed gold rows, contamination=0, per-row attestation.

## Infra
- RunPod pod fpowppss5ngtkw (RTX 3090, 30GB vol) drove all measurement + retrain.
- Migration Mac->pod paused (sibling-lane rsyncs active on /workspace volume); MIGRATION_LEDGER.md written.
- Token rotation advised (HF_TOKEN appeared in pod launchers earlier; all launchers now deleted).

## Open next
- M3 (Downloads move) blocked on pod disk (100% full).
- 100-move plan doc: `~/sov-space/docs/NEXT_100_MOVES_2026-08-08.md`; this batch executed M1-M8 + D31 + D32 + E40.
- v13 (3B) + v16 (ensemble) are the next concrete acc lifts per M90 consensus basis.
