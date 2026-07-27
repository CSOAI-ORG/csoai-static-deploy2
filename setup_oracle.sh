#!/bin/bash
# setup_oracle.sh — Set up Oracle as primary SOV33 workspace
# Run once to install all dependencies

set -e
REMOTE="oracle-micro"
DIR="/home/ubuntu/sov33_shared"

ssh_cmd() {
    ssh -o StrictHostKeyChecking=no -o BatchMode=yes $REMOTE "$@"
}

echo "=== Setting up Oracle SOV33 Workspace ==="

# 1. Install Python dependencies
echo "1. Installing Python dependencies..."
ssh_cmd "pip3 install --quiet requests huggingface_hub datasets" 2>&1 | tail -3
echo "  ✓ Python deps installed"

# 2. Install Ollama
echo "2. Installing Ollama..."
ssh_cmd "curl -fsSL https://ollama.com/install.sh | sh" 2>&1 | tail -3
echo "  ✓ Ollama installed"

# 3. Pull small model
echo "3. Pulling qwen2.5:0.5b..."
ssh_cmd "ollama pull qwen2.5:0.5b" 2>&1 | tail -3
echo "  ✓ Model pulled"

# 4. Create benchmark results directory
echo "4. Creating directories..."
ssh_cmd "mkdir -p $DIR/benchmark-results/training $DIR/benchmark-results/pyrit $DIR/benchmark-results/corpus"
echo "  ✓ Directories created"

# 5. Set up API keys (from local env, never hardcode)
echo "5. Setting up API keys..."
GROQ_KEY=${GROQ_API_KEY:?"Set GROQ_API_KEY env var before running"}
OR_KEY=${OPENROUTER_API_KEY:?"Set OPENROUTER_API_KEY env var before running"}
NVIDIA_KEY=${NVIDIA_API_KEY:?"Set NVIDIA_API_KEY env var before running"}
ssh_cmd "cat > /home/ubuntu/.env << 'EOF'
GROQ_API_KEY=${GROQ_KEY}
OPENROUTER_API_KEY=${OR_KEY}
NVIDIA_API_KEY=${NVIDIA_KEY}
EOF
chmod 600 /home/ubuntu/.env"
echo "  ✓ API keys set"

# 6. Verify setup
echo "6. Verifying setup..."
ssh_cmd "echo '=== Disk ==='; df -h / $DIR 2>&1 | head -3; echo '=== Ollama ==='; ollama list 2>&1 | head -5; echo '=== Python ==='; python3 --version; echo '=== Files ==='; ls $DIR/*.py 2>/dev/null | head -5"
echo "  ✓ Setup verified"

echo ""
echo "=== SETUP COMPLETE ==="
echo "Oracle is ready as primary SOV33 workspace."
echo "Run: bash work_remote.sh oracle status"