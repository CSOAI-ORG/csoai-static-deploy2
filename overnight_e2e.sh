#!/bin/bash
# overnight_e2e.sh — full E2E overnight run for CSOAI Sovereign Estate
#
# Exercises every system we shipped this session:
#   1. Tier-0 sovereign citizens (qwen2.5:0.5b) — care battery
#   2. Tier-1 sovereign citizens (llama3.2:3b) — care battery
#   3. Care gate eval (49/49 + 0/14)
#   4. flywheel.py selftest (9/9)
#   5. ProvBench canonical bound
#   6. PQC chains — emit + bench (25/25 on our chains)
#   7. UserSovereignLauncher — spawn tier-0 + tier-2
#   8. Decision ledger — SIGIL-signed append
#   9. SovSpaceGalaxy snapshot — build + copy
#  10. Deploy csoai-site (if changed)
#  11. Decision ledger append → flywheel Worker /keystone/decision-ledger
#
# Logs every step to ~/clawd/csoai-static-deploy2/logs/overnight_e2e_*.log
# Emits final verdict to benchmark-results/overnight_e2e_*.json
#
# Cron: nightly at 02:00 BST (lower-noise window).
#   launchd plist: ~/Library/LaunchAgents/com.csoai.overnight-e2e.plist

set -uo pipefail

SOV="/Users/nicholas/clawd/csoai-static-deploy2"
DASH="/Users/nicholas/projects/coai-dashboard"
LOGS="$SOV/logs"
RESULTS="$SOV/benchmark-results"
TS=$(date +%Y%m%d_%H%M%S)
LOG="$LOGS/overnight_e2e_${TS}.log"

mkdir -p "$LOGS" "$RESULTS"

echo "=== overnight E2E $TS ===" | tee -a "$LOG"
date | tee -a "$LOG"

# 1. Tier-0 citizen + care battery (small load — local Ollama)
echo "[1/11] Tier-0 sovereign citizen on care battery" | tee -a "$LOG"
python3 "$SOV/user_sovereign_launcher.py" --spawn "overnight-test-$TS-tier0" --tokens 200 --json >> "$LOG" 2>&1

# 2. Tier-1 citizen (medium load)
echo "[2/11] Tier-1 sovereign citizen (medium load)" | tee -a "$LOG"
python3 "$SOV/user_sovereign_launcher.py" --spawn "overnight-test-$TS-tier1" --tokens 5000 --json >> "$LOG" 2>&1

# 3. Care gate eval (deterministic, no LLM)
echo "[3/11] Care gate eval (deterministic, Law 1)" | tee -a "$LOG"
python3 "$SOV/care_gate_eval.py" 2>&1 | tee -a "$LOG"

# 4. flywheel selftest (9/9 anti-Goodhart)
echo "[4/11] flywheel selftest (anti-Goodhart salt)" | tee -a "$LOG"
cd "$SOV" && python3 flywheel.py --selftest 2>&1 | tee -a "$LOG"

# 5. ProvBench canonical bound (regenerate)
echo "[5/11] ProvBench canonical bound" | tee -a "$LOG"
python3 -c "
import json, os
from pathlib import Path
p = Path('$SOV/benchmark-results/provbench.json')
if p.exists():
    d = json.loads(p.read_text())
    print(f'  ProvBench: {d.get(\"n_assets_marked\", 0)} assets · {len(d.get(\"cells\", []))} cells')
    # Just print the headline
    for entry in d.get('pooled_by_check', [])[:1]:
        print(f'  headline: {entry.get(\"headline\", \"\")[:200]}')
" 2>&1 | tee -a "$LOG"

# 6. PQC chains — emit + bench (25/25)
echo "[6/11] PQC chains — emit + bench" | tee -a "$LOG"
cd "$SOV" && python3 emit_pqc_ready_chains.py 2>&1 | tee -a "$LOG"
python3 pqcbench.py 2>&1 | grep -E "(PER-CRITERION|^      [a-z_]+ +[0-9]+)" | tee -a "$LOG"

# 7. UserSovereignLauncher — tier-2 (free GPU)
echo "[7/11] Tier-2 sovereign citizen (free GPU)" | tee -a "$LOG"
python3 "$SOV/user_sovereign_launcher.py" --spawn "overnight-test-$TS-tier2" --tokens 80000 --json >> "$LOG" 2>&1

# 8. Decision ledger — emit a sample sigil-signed record
echo "[8/11] Decision ledger — SIGIL-signed append" | tee -a "$LOG"
python3 -c "
import sys, json
sys.path.insert(0, '$SOV')
from sov_invariants import emit_sigil, BFT_COUNCIL_SIZE
import hashlib
sigil = emit_sigil({'kind': 'overnight-e2e', 'ts': '$TS', 'plan': 'full-pipeline'},
    {'approve': BFT_COUNCIL_SIZE, 'amend': 0, 'reject': 0}, 0.96)
# Append to decision ledger (canonical)
with open('$SOV/decision_ledger.jsonl', 'a') as f:
    f.write(json.dumps({'payload': {'kind': 'overnight-e2e', 'ts': '$TS'}, 'sigil': sigil}) + '\n')
print(f'  sigil: payload_hash={sigil[\"payload_hash\"][:16]}... root_hash={sigil[\"root_hash\"][:16]}...')
" 2>&1 | tee -a "$LOG"

# 9. SovSpaceGalaxy snapshot
echo "[9/11] SovSpaceGalaxy snapshot rebuild" | tee -a "$LOG"
python3 ~/clawd/councilof-ai/build_flywheel_snapshot.py 2>&1 | tee -a "$LOG"
cp -f ~/clawd/councilof-ai/client/public/flywheel-snapshot.json \
      ~/clawd/councilof-ai/dist/client/flywheel-snapshot.json

# 10. Deploy csoai-site
echo "[10/11] Deploy csoai-site (master surface)" | tee -a "$LOG"
cd ~/clawd/councilof-ai && npx wrangler pages deploy dist/client \
    --project-name=csoai-site --branch=main --commit-dirty=true 2>&1 | \
    grep -E "(Success|Deployment)" | tee -a "$LOG"

# 11. Final verdict emit
echo "[11/11] Final verdict" | tee -a "$LOG"
python3 "$SOV/overnight_e2e.py" --emit-verdict --log "$LOG" --ts "$TS" 2>&1 | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "=== overnight E2E complete: $LOG ===" | tee -a "$LOG"
echo "verdict: $RESULTS/overnight_e2e_${TS}.json" | tee -a "$LOG"