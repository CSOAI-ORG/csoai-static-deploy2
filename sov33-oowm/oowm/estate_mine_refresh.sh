#!/bin/bash
# Daily estate-mine → OOWM knowledge graph refresh (JEEVES 2026-08-17)
cd /Users/nicholas/clawd/sov33-oowm || exit 1
python3 -m oowm.estate_mine_ingest --cap 1500 >> /tmp/estate_mine_refresh.log 2>&1
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) refresh done" >> /tmp/estate_mine_refresh.log
