#!/bin/bash
# oracle_synth_deploy.sh — Deploy data synthesis to Oracle ARM (always-free)
# Uses OCI CLI to run CPU-only synthesis on the always-free ARM instance
set -euo pipefail

echo "=== ORACLE ARM DEPLOYMENT ==="
echo "Target: Oracle Cloud ARM (always-free)"
echo "Use: Data synthesis, corpus building, E2E checks"
echo ""

# Check OCI config
if [ ! -f ~/.oci/config ]; then
    echo "ERROR: No OCI config at ~/.oci/config"
    exit 1
fi

echo "OCI config found. Instance details:"
oci compute instance list --compartment-id $(oci iam compartment list --query 'data[0].id' --raw-output 2>/dev/null || echo "tenancy") --query 'data[?state==`RUNNING`].{id:id,name:displayName,shape:shape}' --output table 2>/dev/null || echo "  (check OCI console for instance details)"

echo ""
echo "To deploy synthesis:"
echo "  1. SSH into Oracle ARM instance"
echo "  2. Pull latest code from volume"
echo "  3. Run synthesis: python3 benchmark-results/synthesize_training_data.py"
echo "  4. Results auto-sync to network volume"
