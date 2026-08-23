#!/bin/bash
# A100 auto-start chain: board → board2fly → frontier day-0 pull → auto-audit
# Self-healing on pod restart. All steps safe/idempotent.

# Step 1: Start/restart the board (detached, survives SSH drops)
sleep 15
if ! pgrep -f "board_v2.py" >/dev/null 2>&1; then
  cd /workspace/csoai-static-deploy2/SOVOS/agents
  setsid nohup /workspace/venv-test/bin/python -u board_v2.py >> /workspace/board_autostart.log 2>&1 < /dev/null &
fi

# Step 2: Convert any completed boards into the flywheel input dir (idempotent)
sleep 30
cd /workspace/csoai-static-deploy2
setsid nohup /workspace/venv-test/bin/python -u board2fly.py --boards SOVOS/boards-v2-2026-08-12 >> /workspace/board2fly.log 2>&1 < /dev/null &

# Step 3: Pull the day-0 frontier model for auto-audit (qwen3.8-27b, ~16GB)
# Only pulls if the model isn't already present. Runs after board to avoid contention.
sleep 120
if ! ollama list 2>/dev/null | grep -q "qwen3.8-27b"; then
  cd /workspace/csoai-static-deploy2
  setsid nohup timeout 600 ollama pull qwen3.8-27b:latest >> /workspace/frontier_pull.log 2>&1 < /dev/null &
fi

# Step 4: Run day0_audit (detects any newly available frontier models, no-ops if none)
sleep 180
cd /workspace/csoai-static-deploy2
setsid nohup /workspace/venv-test/bin/python -u day0_audit.py >> /workspace/day0_audit.log 2>&1 < /dev/null &

exit 0