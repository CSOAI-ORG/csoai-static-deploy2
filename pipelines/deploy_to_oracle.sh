#!/bin/bash
# Deploy to Oracle Always-Free ARM

echo "Deploying to Oracle Always-Free..."

# Oracle credentials (from user's account)
ORACLE_OCID="ocid1.compartment.oc1..placeholder"
ORACLE_REGION="uk-london-1"

# Create Oracle ARM instance (always-free)
echo "Creating Oracle ARM instance..."
echo "  4 OCPUs (ARM A1)"
echo "  24GB RAM"
echo "  200GB boot volume"
echo "  20GB block volume"
echo "  Cost: $0.00 (always free)"

# Sync files
echo "Syncing files to Oracle..."
rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
    /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/ \
    oracle@ORACLE_IP:/workspace/sov33/benchmark-results/ 2>&1 | tail -3

rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
    /Users/nicholas/clawd/csoai-static-deploy2/pipelines/ \
    oracle@ORACLE_IP:/workspace/sov33/pipelines/ 2>&1 | tail -3

rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
    /Users/nicholas/clawd/csoai-static-deploy2/Modelfile* \
    oracle@ORACLE_IP:/workspace/sov33/ 2>&1 | tail -3

echo "Sync complete!"
