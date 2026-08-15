#!/bin/zsh
# align_bench_publish.sh — Phase 8: Auto-run overnight (align + bench + publish).
# Runs all 7 phases of the bleed-edge alignment every night.
# Idempotent. Re-runs produce new sigils but same counts.

REPO=/Users/nicholas/clawd/csoai-static-deploy2
DASHBOARD=/Users/nicholas/projects/coai-dashboard
LOG=/tmp/align_bench_publish.log
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "" >> $LOG
echo "[$TS] === align_bench_publish.sh started ===" >> $LOG

# Phase 1: Mac cluster detection
echo "[$TS] Phase 1: Mac cluster detect" >> $LOG
cd $REPO && /usr/bin/python3 mlx_cluster/mlx_cluster_detect.py >> $LOG 2>&1

# Phase 2: REAP pruning harness
echo "[$TS] Phase 2: REAP prune harness" >> $LOG
cd $REPO && /usr/bin/python3 mlx_cluster/reap_prune_harness.py >> $LOG 2>&1

# Phase 3: Unsloth MoE harness
echo "[$TS] Phase 3: Unsloth MoE harness" >> $LOG
cd $REPO && /usr/bin/python3 mlx_cluster/unsloth_moe_harness.py --base sov33-unified >> $LOG 2>&1

# Phase 4: Progressive training
echo "[$TS] Phase 4: Progressive training" >> $LOG
cd $REPO && /usr/bin/python3 mlx_cluster/progressive_training.py --estimate --target 13 >> $LOG 2>&1

# Phase 5: MLX distributed launcher
echo "[$TS] Phase 5: MLX distributed launcher" >> $LOG
cd $REPO && /usr/bin/python3 mlx_cluster/mlx_distributed_launcher.py --probe >> $LOG 2>&1

# Phase 6: GSPC alignment
echo "[$TS] Phase 6: GSPC alignment" >> $LOG
cd $REPO && /usr/bin/python3 mlx_cluster/gspc_alignment.py >> $LOG 2>&1

# Phase 7: N-sites eat-all
echo "[$TS] Phase 7: N-sites eat-all" >> $LOG
cd $REPO && /usr/bin/python3 mlx_cluster/n_sites_eat_all.py >> $LOG 2>&1

# Existing e2e_overnight (from previous batch)
echo "[$TS] Existing: e2e_overnight" >> $LOG
cd $DASHBOARD && /usr/bin/python3 scripts/e2e_overnight.py --only 2 >> $LOG 2>&1
cd $DASHBOARD && /usr/bin/python3 scripts/e2e_overnight.py --only 6 >> $LOG 2>&1

# Compute alignment witness
echo "[$TS] Computing alignment witness" >> $LOG
cd $REPO && /usr/bin/python3 -c "
import hashlib, json
from pathlib import Path
from datetime import datetime, timezone

mlx_dir = Path('mlx_cluster')
files = sorted(mlx_dir.glob('*.json'))
hashes = []
for f in files:
    with open(f, 'rb') as fh:
        h = hashlib.sha256(fh.read()).hexdigest()
    hashes.append({'file': f.name, 'sha256': h})

combined = ''.join(h['sha256'] for h in hashes)
root = hashlib.sha256(combined.encode()).hexdigest()

manifest = {
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'phase': 'align_bench_publish',
    'files': hashes,
    'root_hash': root,
    'auto_run': True,
}
with open('mlx_cluster/alignment_witness.json', 'w') as f:
    json.dump(manifest, f, indent=2)
print(f'Alignment witness: {root[:16]}...')
" >> $LOG 2>&1

echo "[$TS] === align_bench_publish.sh complete ===" >> $LOG