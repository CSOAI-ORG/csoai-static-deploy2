#!/bin/bash
# sovereign_pipeline.sh — runs ON the A100 80GB pod

set -euo pipefail
cd /workspace

echo "=== SOV33 PIPELINE STARTING ON $(hostname) ==="
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader)"
echo "Time: $(date)"

# Install sovereign deps
pip install --no-cache-dir pyyaml requests rich numpy pandas matplotlib

# Clone the repo
git clone https://github.com/CSOAI-ORG/csoai-sovereign.git csoai || true
cd csoai

# Run govbench
python3 sov33/govbench_takeover.py 2>&1 | tee /tmp/govbench.log
echo "GovBench complete. Sigil chain length: $(wc -l < ~/.sovereign/layerGOVBENCH-V2_chain.jsonl 2>/dev/null)"

# Run master takeover
python3 sov33/master_takeover.py 2>&1 | tee /tmp/master.log

# Run all the modules
for mod in ledgerboard_v2 hybrid_merge ssd_venturi_speedup test_matrix owem_checklist capstone_portal help_other_agents deepseek_tune_owem; do
  echo "--- Running $mod ---"
  python3 sov33/${mod}.py 2>&1 | tail -10
done

# Emit summary
python3 -c "
import json
from pathlib import Path
print('=== FINAL STATE ===')
for f in Path.home().joinpath('.sovereign').glob('layer*_chain.jsonl'):
    print(f'  {f.stem}: {sum(1 for _ in open(f))}')
print(f'TOTAL: {sum(1 for f in Path.home().joinpath(".sovereign").glob("layer*_chain.jsonl") for _ in open(f))}')
"

# Stay alive so we can inspect
echo "Sleeping 1 hour so we can ssh in..."
sleep 3600
