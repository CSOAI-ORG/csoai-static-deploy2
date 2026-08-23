#!/bin/bash
# Council OS backup / off-Mac procedure
# 1) version-control the source (git), 2) back up the deploy artifact to Oracle.
set -e
D=~/.grokbot/csoai-site-main
cd "$D"
git add app.html .hub/estate-data.js llms.txt functions/api/*.js 2>/dev/null && git commit -q -m "Council OS auto-backup $(date -u +%FT%TZ)" 2>/dev/null || echo "  (nothing to commit / not a git change)"
tar czf /tmp/council-os-deploy.tar.gz -C /tmp/gspc-hub . 2>/dev/null
oci os object put --namespace lred58wvovu0 --bucket-name mac-offload --name "council-os/council-os-deploy-$(date +%Y-%m-%d).tar.gz" --file /tmp/council-os-deploy.tar.gz >/dev/null 2>&1 && echo "  → Oracle offloaded council-os-deploy-$(date +%Y-%m-%d).tar.gz"
echo "  ✓ backup done"
