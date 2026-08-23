#!/bin/bash
# SHIP TO POD — make the drum available to SOVOS/CSOAI in the fleet (pods / Oracle / RunPod).
# Bundles the doctrine-clean pack (catalog, graph, feeds, router, archive, train, docs) with
# a sha256 manifest into ~/clawd/_evacuation/runpod-bundles/ — the estate's fleet bundle dir.
# The pod side runs: ops/ingest_sovos.py (OOWM index) + train/corpus_model.py (NN baseline);
# GNNs (torch_geometric) run on the pod against feeds/catalog_graph.json.
set -eu
DRUM="$HOME/master-harness/knowledge/frameworks-drum"
DATE=$(date +%Y%m%d)
BUNDLE="$HOME/clawd/_evacuation/runpod-bundles/${DATE}-frameworks-drum"
mkdir -p "$BUNDLE"

# doctrine-clean surfaces only — never _mining/, never the git dir, never keys, never caches
# full doctrine-clean pack (build_catalog + tests + mcp + a2a + site) so the pod can run the gates
rsync -a --exclude="_mining" --exclude=".git" --exclude="ops/backups" --exclude="__pycache__" \
  --exclude="archive/store" --exclude="router/calibration_set.jsonl" \
  "$DRUM"/ "$BUNDLE/" 2>/dev/null

# checksum manifest (the TEA walker's proof the bundle is intact)
(cd "$BUNDLE" && find . -type f | sort | xargs shasum -a 256 > MANIFEST.sha256)
echo "bundle: $BUNDLE ($(du -sh "$BUNDLE" | cut -f1))"
echo "files: $(find "$BUNDLE" -type f | wc -l | tr -d ' ')"
cat "$BUNDLE/MANIFEST.sha256" | head -3
# push to the canonical RAG volume (sov-brain-2, 68G free on /workspace)
POD="sov-brain-2"
POD_DIR="/workspace/frameworks-drum"
SSH="ssh -o ConnectTimeout=8 -o BatchMode=yes -o StrictHostKeyChecking=no"
if $SSH "$POD" 'exit 0' 2>/dev/null; then
  $SSH "$POD" "mkdir -p $POD_DIR" 2>/dev/null
  scp -q -o ConnectTimeout=8 -o StrictHostKeyChecking=no -r "$BUNDLE"/. "$POD:$POD_DIR/" 2>/dev/null && echo "pushed to $POD:$POD_DIR (RAG volume)"
  $SSH "$POD" "cd $POD_DIR && python3 ops/ingest_sovos.py --oowm-root /workspace/sov33-oowm >/dev/null 2>&1 && echo 'OOWM index refreshed on pod'" 2>/dev/null
else
  echo "POD $POD unreachable (fail-fast) — bundle staged on Mac; overnight continues"
fi
