#!/bin/bash
# Launch (or restart) the CSOAI automated axis engine on a pod, fully detached.
# The engine trains/measures continuously against the catalog graph + axes (kind/binding/status).
# Usage:  bash ops/axis_engine_launch.sh [host]
set -u
HOST="${1:-sovos-light-a100}"
DIR="/workspace/frameworks-drum"
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$HOST" "cd $DIR && pkill -f axis_engine 2>/dev/null; (setsid python3 -u train/axis_engine.py </dev/null >feeds/axis_engine.log 2>&1 &) ; sleep 1; echo launched" 2>&1 | tail -2
