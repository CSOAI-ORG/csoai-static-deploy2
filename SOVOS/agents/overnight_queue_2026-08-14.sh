#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# overnight_queue_2026-08-14.sh — v2 (direct execution, no function scoping)
# ═══════════════════════════════════════════════════════════════════════
set -euo pipefail
cd /workspace/jeeves-exec/SOVOS
mkdir -p logs boards-v2-2026-08-14 cross-lab-runs/2026-08-14
LOG="/workspace/jeeves-exec/SOVOS/logs/overnight-$(date +%Y%m%d-%H%M).log"
TOUT=1800

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }
log "═══ OVERNIGHT QUEUE v2 START ═══"
nvidia-smi --query-gpu=utilization.gpu,memory.free,temperature.gpu --format=csv,noheader | tee -a "$LOG"

# STEP 1: Fleet-wide board re-run
log "STEP 1: Fleet-wide board (13 axes × 19 models)"
timeout $TOUT python3 -u agents/board_v2.py \
  --outdir /workspace/jeeves-exec/SOVOS/boards-v2-2026-08-14 \
  --models "nemotron-3-nano:30b sov6-preservation-v3-light:latest sov6-temporality-v3-light:latest sov6-logic-v3-light:latest sov6-relationality-v3-light:latest sov6-synthesis-v3-light:latest sov6-ethics-v3-light:latest sov6-abstraction-v3-light:latest sov6-creation-v3-light:latest sov6-identity-v3-light:latest sov6-aesthetics-v3-light:latest sov6-agency-v3-light:latest sov6-destruction-v3-light:latest sov6-embodiment-v3-light:latest qwen2.5:3b mistral:7b gemma3:12b llama3.2:3b deepseek-r1:8b" \
  --control "qwen2.5:0.5b-instruct" 2>&1 | tee -a "$LOG" || log "STEP 1 exit $?"
log "STEP 1 finished"

# STEP 2: Cross-lab quotable city (local models)
log "STEP 2: Cross-lab quotable city"
timeout $TOUT python3 -u agents/cross_lab_city.py \
  --epochs 3 --local-only \
  --output /workspace/jeeves-exec/SOVOS/cross-lab-runs/2026-08-14/ \
  2>&1 | tee -a "$LOG" || log "STEP 2 exit $?"
log "STEP 2 finished"

# STEP 3: MCP scoreboard separation
log "STEP 3: MCP scoreboard analysis"
timeout $TOUT python3 -c "
from sovos_city.protocols import ProtocolBank
import json
bank = ProtocolBank()
bank.load_banks()
mcp_items = bank.get_bank('mcp').items
print(f'MCP bank: {len(mcp_items)} items')
for i in mcp_items[:5]:
    print(f'  {i.id}: {i.text[:80]}')
with open('cross-lab-runs/2026-08-14/mcp_bank_snapshot.json', 'w') as f:
    json.dump([{'id': i.id, 'text': i.text} for i in mcp_items], f, indent=2)
" 2>&1 | tee -a "$LOG" || log "STEP 3 exit $?"
log "STEP 3 finished"

# STEP 4: Daily City Report
log "STEP 4: Daily City Report"
timeout 300 python3 -c "
import json, datetime
from sovos_signal_index import SignalIndex
report = {
    'date': str(datetime.date.today()),
    'pods': {'a100': True, 'status': 'overnight_queue'},
    'axes_measured': 13,
    'signed': False,
}
with open('cross-lab-runs/2026-08-14/daily_report.json', 'w') as f:
    json.dump(report, f, indent=2)
print('Daily report written')
" 2>&1 | tee -a "$LOG" || log "STEP 4 exit $?"
log "STEP 4 finished"

# STEP 5: Claim-linter verification (G4 gate check)
log "STEP 5: G4 claim-linter sweep"
timeout 300 python3 agents/claim_linter.py /workspace/jeeves-exec/ \
  --ignore-patterns "node_modules,.git,__pycache__,boards-v2,logs" \
  2>&1 | tee -a "$LOG" || log "STEP 5 exit $?"
log "STEP 5 finished"

log "═══ OVERNIGHT QUEUE COMPLETE ═══"
nvidia-smi --query-gpu=utilization.gpu,memory.free --format=csv,noheader | tee -a "$LOG"
echo "Overnight end: $(date)" >> "$LOG"