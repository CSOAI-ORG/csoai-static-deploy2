#!/bin/bash
# pod_gateway_watchdog.sh — retry SSH until the RunPod gateway recovers,
# then run the harvest sequence (route+store, pull results, index refresh).
# Meant to run from the Mac as a nohup watchdog.
# Usage: nohup bash pod_gateway_watchdog.sh > /tmp/pod-watchdog.log 2>&1 &

P1="root@104.255.9.187 -p 11703"
P2="root@104.255.9.187 -p 11628"
MAX=40   # ~2.5h of retries

echo "=== pod gateway watchdog start $(date -u +%FT%TZ) ==="

for i in $(seq 1 $MAX); do
  if ssh ${P1} 'echo ok' > /dev/null 2>&1; then
    echo "POD1 SSH UP after ${i} tries at $(date -u +%FT%TZ)"
    echo "--- running harvest sequence ---"
    # 1. route+store every artifact into sov-space/mind registers
    ssh ${P1} 'cd /workspace/jeeves-exec && /workspace/venv-test/bin/python SOVOS/agents/route_and_store.py --artifacts /workspace --out /workspace/route-manifest.jsonl' 2>&1 | tail -3
    # 2. snapshot the burst outputs
    ssh ${P1} 'ls -la /workspace/top10-burst-2026-08-15/ 2>/dev/null; ls -la /workspace/overnight-bench-2026-08-16/ 2>/dev/null; tail -12 /tmp/top10-burst.log 2>/dev/null; tail -12 /tmp/overnight-bench.log 2>/dev/null' > /tmp/burst-snapshot.txt 2>&1
    echo "burst snapshot -> /tmp/burst-snapshot.txt"
    echo "=== harvest done $(date -u +%FT%TZ) ==="
    exit 0
  fi
  echo "[$i] pod1 ssh down $(date -u +%H:%M:%S)"
  sleep 240
done
echo "=== watchdog gave up after ${MAX} tries — check RunPod console ==="
exit 1