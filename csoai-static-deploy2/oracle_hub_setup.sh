#!/bin/bash
# oracle_hub_setup.sh — Set up Oracle ARM as central hub
set -euo pipefail

ORACLE="ubuntu@145.241.232.16"

echo "=== SETTING UP ORACLE ARM AS CENTRAL HUB ==="
echo ""

# 1. Create directory structure
echo "[1/6] Creating directory structure..."
ssh $ORACLE "mkdir -p ~/csoai-hub/{training,models,results,logs,config,honey,sigil,heartbeat}"
echo "  OK"

# 2. Install required packages
echo "[2/6] Installing packages..."
ssh $ORACLE "sudo apt-get update -qq && sudo apt-get install -y -qq python3-pip python3-venv git curl jq"
echo "  OK"

# 3. Set up Python environment
echo "[3/6] Setting up Python environment..."
ssh $ORACLE "cd ~/csoai-hub && python3 -m venv .venv && source .venv/bin/activate && pip install -q requests tqdm"
echo "  OK"

# 4. Create hub configuration
echo "[4/6] Creating hub configuration..."
ssh $ORACLE "cat > ~/csoai-hub/config/hub.json << 'EOF'
{
  \"hub\": \"oracle-arm\",
  \"ip\": \"145.241.232.16\",
  \"storage\": \"~/csoai-hub\",
  \"gpu_tiers\": {
    \"kaggle\": {\"gpu\": \"T4\", \"hours_per_week\": 30, \"status\": \"available\"},
    \"colab\": {\"gpu\": \"T4\", \"hours_per_session\": 12, \"status\": \"available\"},
    \"lightning\": {\"gpu\": \"T4\", \"hours_per_month\": 22, \"status\": \"available\"},
    \"hf_spaces\": {\"gpu\": \"T4\", \"status\": \"available\"}
  },
  \"model\": \"sov33-ultimate-sovereign\",
  \"arena_composite\": 72.5,
  \"capabilities\": [\"governance\", \"security\", \"defence\", \"agentic\", \"code\", \"math\"]
}
EOF"
echo "  OK"

# 5. Sync training data
echo "[5/6] Syncing training data..."
rsync -avz --progress /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/training/ $ORACLE:~/csoai-hub/training/ 2>&1 | tail -3
echo "  OK"

# 6. Create spine/drum/rhythm configuration
echo "[6/6] Creating spine/drum/rhythm..."
ssh $ORACLE "cat > ~/csoai-hub/config/rhythm.json << 'EOF'
{
  \"spine\": {
    \"heartbeat\": 300,
    \"evolution\": 3600,
    \"backup\": 86400,
    \"sync\": 1800
  },
  \"drum\": {
    \"train\": \"0 * * * *\",
    \"evaluate\": \"0 */4 * * *\",
    \"deploy\": \"0 0 * * *\",
    \"report\": \"0 0 * * 0\"
  },
  \"rhythm\": {
    \"phases\": [\"absorb\", \"transform\", \"integrate\", \"evolve\"],
    \"current_phase\": \"absorb\",
    \"cycle_count\": 0
  }
}
EOF"
echo "  OK"

echo ""
echo "=== ORACLE ARM HUB READY ==="
echo "Hub: ubuntu@145.241.232.16:~/csoai-hub/"
echo "Storage: 38GB available"
echo "Config: ~/csoai-hub/config/"
echo ""
