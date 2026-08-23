#!/bin/bash
# D38 daily-deposit helper — append today's _findings stub if missing.
# Wire into a daily cron: `crontab -e` -> `0 7 * * * bash ~/clawd/_findings/.daily_deposit_helper.sh`
F=~/clawd/_findings
T=$(date -u +%Y-%m-%d)
FNAME="$F/D${T}_DAILY_HANDOFF.md"
if [ -e "$FNAME" ]; then echo "exists: $FNAME"; exit 0; fi
mkdir -p "$F"
cat > "$FNAME" <<EOF
# D${T} — daily _findings stub (replace with today's real artifact)

## Overnight handoff
- Champion: \`sov33-v12\` (Qwen2.5-1.5B LoRA) — SOV-SIGNAL 69.07% (476/476 graded, hardened M89 extractor); aggregate 66.33%.
- HF Leaderboard V2 (lm_eval 0.4.12, bf16): BBH 0.4088 / MMLU-Pro 0.2809 / MuSR 0.4101 / IFEval 0.4365 / Math-Hard 0.0793 / **GPQA 0.3096+/-0.0134** (5 of 6 V2 tasks, GPQA gated access finally approved on Nicholastempleman account). 6-task table published: https://huggingface.co/datasets/csoai/sov33-v12-results
- Pod fpowppss5ngtkw (RTX 3090, 30GB vol). Token rotation advised (HF_TOKEN appeared in pod launchers earlier).

## Active moves (next-100 plan: \`~/sov-space/docs/NEXT_100_MOVES_2026-08-08.md\`)
- M3 (~/Downloads -> pod) blocked: pod vol 100% full (sibling-lane rsyncs active).
- Open: M13-32 capacity ladder (v13 3B, v14 4B, v15 full-finetune, v16 ensemble).
- D33 (P2-21 fabrication audit): reconciles P2-21 vs 1 honest sim. Queue.

## Issues
- Mac disk sentinel: 4.8Gi free (G54 threshold 2Gi — GREEN).
- Migration Mac->pod: PAUSED, MIGRATION_LEDGER.md (~/clawd/) documents source->dest.

## Overnight numbers (verifiable)
- HF dataset: \`csoai/sov33-v12-results\` live; \`csoai/sov-signal-ground-truth-v10\` live.
EOF
echo "D38 stub written: $FNAME"
