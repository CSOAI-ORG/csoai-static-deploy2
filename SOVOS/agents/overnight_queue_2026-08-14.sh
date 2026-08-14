#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# overnight_queue_2026-08-14.sh — v3 (fixed CLI args + long board timeout)
# ═══════════════════════════════════════════════════════════════════════
# KEY FIX v3: STEP 1 (board) is the priority job and streams durably to
# MinIO every 200 rows — it gets a FULL-NIGHT timeout, NOT the 30min
# kill-chain. Steps 2-4 use the real CLI interfaces (verified).
set -euo pipefail
cd /workspace/jeeves-exec/SOVOS
mkdir -p logs boards-v2-2026-08-14 cross-lab-runs/2026-08-14
LOG="/workspace/jeeves-exec/SOVOS/logs/overnight-v3-$(date +%Y%m%d-%H%M).log"
log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

log "═══ OVERNIGHT QUEUE v3 START ═══"
nvidia-smi --query-gpu=utilization.gpu,memory.free,temperature.gpu --format=csv,noheader | tee -a "$LOG"

# STEP 1: Fleet-wide board — THE priority job (streams to MinIO, durable).
# Full-night timeout (10h). Do NOT kill before 04:00.
log "STEP 1: Fleet-wide board (13 axes × 19 models) — FULL NIGHT, no early kill"
timeout 36000 python3 -u agents/board_v2.py \
  --outdir /workspace/jeeves-exec/SOVOS/boards-v2-2026-08-14 \
  --models "nemotron-3-nano:30b sov6-preservation-v3-light:latest sov6-temporality-v3-light:latest sov6-logic-v3-light:latest sov6-relationality-v3-light:latest sov6-synthesis-v3-light:latest sov6-ethics-v3-light:latest sov6-abstraction-v3-light:latest sov6-creation-v3-light:latest sov6-identity-v3-light:latest sov6-aesthetics-v3-light:latest sov6-agency-v3-light:latest sov6-destruction-v3-light:latest sov6-embodiment-v3-light:latest qwen2.5:3b mistral:7b gemma3:12b llama3.2:3b deepseek-r1:8b" \
  --control "qwen2.5:0.5b-instruct" 2>&1 | tee -a "$LOG"
log "STEP 1 finished (exit ${PIPESTATUS[0]:-$?})"

# STEP 2: Cross-lab quotable city (real CLI: --scenario-bank for Art5 items)
log "STEP 2: Cross-lab quotable city (+ scenario bank)"
timeout 5400 python3 -u agents/cross_lab_city.py \
  --budget 5 --epochs 3 --citizens 40 --scenario-bank \
  --out /workspace/jeeves-exec/SOVOS/cross-lab-runs/2026-08-14/ 2>&1 | tee -a "$LOG"
log "STEP 2 finished"

# STEP 3: City MCP bank analysis (real module path)
log "STEP 3: City protocol bank analysis"
PYTHONPATH="/workspace/jeeves-exec/SOVOS/packages/sovos-city/src" timeout 1200 \
  python3 -c "
from sovos_city import CityBank
bank = CityBank()
try:
    protocols = bank.protocol_bank
    print(f'protocol_bank attr: {type(protocols)}')
except Exception as e:
    print(f'no protocol_bank attr: {e}')
buckets = bank.bucket_names if hasattr(bank, 'bucket_names') else 'n/a'
print(f'CityBank buckets: {buckets}')
" 2>&1 | tee -a "$LOG"
log "STEP 3 finished"

# STEP 4: Daily City Report (longitudinal card)
log "STEP 4: Daily report"
timeout 600 python3 -c "
import json, datetime, pathlib
out = pathlib.Path('cross-lab-runs/2026-08-14/daily_report.json')
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({
    'date': str(datetime.date.today()),
    'source': 'overnight_queue_v3',
    'board_streamed': True,
    'status': 'overnight run',
}, indent=2))
print('Daily report written')
" 2>&1 | tee -a "$LOG"
log "STEP 4 finished"

# STEP 5: G4 claim-linter from repo ROOT
log "STEP 5: G4 claim-linter"
cd /workspace/jeeves-exec
timeout 600 python3 jeeves-exec/SOVOS/agents/claim_linter.py \
  /workspace/jeeves-exec --ignore-patterns "node_modules,.git,__pycache__,logs" 2>&1 | tee -a "$LOG" || log "STEP 5 exit $?"
log "STEP 5 finished"

log "═══ OVERNIGHT QUEUE v3 COMPLETE (or board wall-clock reached) ═══"
nvidia-smi --query-gpu=utilization.gpu,memory.free --format=csv,noheader | tee -a "$LOG"
echo "Overnight end: $(date)" >> "$LOG"