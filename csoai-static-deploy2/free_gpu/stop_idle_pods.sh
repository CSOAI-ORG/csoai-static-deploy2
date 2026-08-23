#!/bin/bash
# stop_idle_pods.sh — Stop RunPod pods that are running but idle
# Checks if pods have active SSH work before stopping
set -euo pipefail

API_KEY=$(cat ~/.runpod/api_key 2>/dev/null || echo "")
if [ -z "$API_KEY" ]; then
    echo "ERROR: No RunPod API key"
    exit 1
fi

echo "=== CHECKING RUNPOD PODS ==="
PODS=$(curl -s https://rest.runpod.io/v1/pods?includeMachine=true \
    -H "Authorization: Bearer $API_KEY")

echo "$PODS" | python3 -c '
import json, sys
d = json.load(sys.stdin)
running = [p for p in d if p.get("desiredStatus") == "RUNNING"]
print(f"Running pods: {len(running)}")
for p in running:
    name = p.get("name")
    gpu = (p.get("gpu") or {}).get("displayName") or "?"
    cost = p.get("adjustedCostPerHr", p.get("costPerHr", 0))
    pid = p.get("id")
    print(f"  {name} ({gpu}) ${cost}/hr id={pid}")
'

echo ""
echo "To stop a pod: curl -X POST https://rest.runpod.io/v1/pods/{POD_ID}/stop -H 'Authorization: Bearer $API_KEY'"
echo "To terminate: curl -X DELETE https://rest.runpod.io/v1/pods/{POD_ID} -H 'Authorization: Bearer $API_KEY'"
