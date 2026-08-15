#!/usr/bin/env bash
# k3-watchdog.sh — Retry K3 A100 pod deployment until stock returns.
# Runs via Hermes cron every 15 min. Creates pod on 2TB volume when A100 frees.
LOG="$HOME/clawd/csoai-static-deploy2/SOVOS/logs/k3-watchdog.log"
mkdir -p "$(dirname "$LOG")"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Check if pod alrename created
POD=$(ls /tmp/k3_pod_created 2>/dev/null || echo "")
if [ -n "$POD" ]; then
    echo "$TS already deployed: $POD" >> "$LOG"
    exit 0
fi

# Try A100 in EU-RO-1 (volume i4atujketp lives there) — with volume attached
runpodctl pod create k3-a100-2tb \
    --gpu-id "NVIDIA A100 80GB PCIe" \
    --gpu-count 1 \
    --cloud-type COMMUNITY \
    --volume-size 0 \
    --network-volume i4atujketp \
    --template "$HOME/clawd/csoai-static-deploy2/SOVOS/agents/k3-pod-template.yaml" \
    --start-ssh \
    --image "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04" \
    > /tmp/k3_pod_created 2>&1

if grep -qE "id:|[a-f0-9]{16}" /tmp/k3_pod_created 2>/dev/null; then
    echo "$TS ✅ DEPLOYED: $(cat /tmp/k3_pod_created | head -3)" >> "$LOG"
    # Signal the A100 to start downloading once pod is up
    echo "K3 pod deployed. Volume i4atujketp + A100. Start download-model.sh to /runpod."
else
    echo "$TS ⏳ no A100 stock: $(head -1 /tmp/k3_pod_created)" >> "$LOG"
fi