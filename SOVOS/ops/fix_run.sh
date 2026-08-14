#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:$PATH
cd /workspace
pkill -f sim_burst 2>/dev/null; pkill -f sovos_city 2>/dev/null
python3 -u fix_loop.py --base Qwen/Qwen2.5-1.5B-Instruct --iters 25 --lr 5e-5
echo "=== fix_loop done $(date -u) ==="
