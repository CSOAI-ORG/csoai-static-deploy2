#!/bin/bash
# Sync volume across all sites

echo "Syncing SOV33 volume across sites..."

# Source: RunPod fresh-a40
SOURCE="root@194.68.245.24:/workspace/sovereign"
SSH_OPTS="-p 22087 -o StrictHostKeyChecking=no"

# Targets
TARGETS=(
    "root@62.169.159.96:/workspace/sovereign"  # H100
    "root@localhost:/tmp/sov-backup"            # Local (placeholder)
)

for target in "${TARGETS[@]}"; do
    echo "Syncing to $target..."
    rsync -avz --progress -e "ssh -p 22087 -o StrictHostKeyChecking=no" \
        "$SOURCE/" "$target/sov33/" \
        --exclude='*.pyc' --exclude='__pycache__' 2>&1 | tail -3
done

echo "Sync complete!"
