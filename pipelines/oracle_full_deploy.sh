#!/bin/bash
# Oracle Always-Free Full Deployment

echo "=== ORACLE ALWAYS-FREE DEPLOYMENT ==="
echo "4 OCPUs ARM, 24GB RAM, 200GB storage, $0.00 forever"

# Step 1: Create Oracle instance
echo "1. Creating Oracle ARM instance..."
echo "  Go to: https://cloud.oracle.com"
echo "  Create → Compute → ARM A1.Flex"
echo "  Config: 4 OCPU, 24GB RAM, 200GB boot"
echo "  Region: uk-london-1"
echo "  Cost: $0.00 (always free)"

# Step 2: SSH into instance
echo "2. SSH into instance..."
echo "  ssh -i ~/.ssh/id_rsa opc@YOUR_ORACLE_IP"

# Step 3: Install Ollama
echo "3. Installing Ollama..."
ssh opc@YOUR_ORACLE_IP "curl -fsSL https://ollama.com/install.sh | sh"

# Step 4: Start Ollama
echo "4. Starting Ollama..."
ssh opc@YOUR_ORACLE_IP "nohup ollama serve &"

# Step 5: Pull models
echo "5. Pulling models..."
ssh opc@YOUR_ORACLE_IP "ollama pull qwen2.5:3b"
ssh opc@YOUR_ORACLE_IP "ollama pull qwen2.5:0.5b"

# Step 6: Sync files
echo "6. Syncing files..."
rsync -avz /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/ opc@YOUR_ORACLE_IP:/workspace/sov33/benchmark-results/
rsync -avz /Users/nicholas/clawd/csoai-static-deploy2/pipelines/ opc@YOUR_ORACLE_IP:/workspace/sov33/pipelines/
rsync -avz /Users/nicholas/clawd/csoai-static-deploy2/Modelfile* opc@YOUR_ORACLE_IP:/workspace/sov33/

echo "Deploy complete!"
