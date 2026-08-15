#!/usr/bin/env bash
# install.sh — bootstrap a fresh RunPod A100 PCIe pod into a working SOVOS
# substrate. Tested 2026-08-11 on pod 1dldzposn7ssuu (sov-brain-a100-fresh2).
#
# Use:
#   1) On RunPod, create a fresh pod: NVIDIA A100 80GB PCIe, image
#      `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`,
#      container 100G, volume 100G, ports "8888/http,22/tcp", startSSH on,
#      env SOV33_PIPELINE=true. ~$1.19/hr.
#   2) `ssh-add ~/.runpod/ssh/runpodctl-ssh-key` so the SSH endpoint accepts.
#   3) Run `bash install.sh` from this directory to:
#        - apt-get zstd (required by ollama installer)
#        - pip numpy scipy geomstats (versioned for SOV chain tests)
#        - ollama install + start + pull qwen2.5:0.5b-instruct
#        - clone the CSOAI monorepo from jv-wave8-production into /workspace
#
# The pod is intended to be the heavy-lift substrate: SOV SIGNAL measurement,
# chain training, GPU eval — NOT Ollama serving for users (we use the other
# pods for that).
set -e
POD_HOME=/workspace
mkdir -p "$POD_HOME"
cd "$POD_HOME"

echo "=== A100 SOVOS pod bootstrap ==="
echo "home: $POD_HOME"
echo "whoami: $(whoami)"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>&1 | head -1 || echo 'no nvidia-smi')"
echo

echo "--- 1. apt deps (zstd required by ollama installer) ---"
if ! which zstd >/dev/null 2>&1; then
  apt-get update
  apt-get install -y zstd
fi
echo "zstd: $(zstd --version 2>&1 | head -1)"
echo

echo "--- 2. python deps (numpy 1.x for geomstats compatibility) ---"
python3 -m pip install --quiet --no-input 'numpy<2' scipy geomstats fakeredis requests
python3 -c "import numpy, scipy, geomstats; print('numpy',numpy.__version__,'scipy',scipy.__version__,'geomstats',geomstats.__version__)"
echo

echo "--- 3. ollama ---"
if ! which ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh -o /tmp/install-ollama.sh
  sh /tmp/install-ollama.sh
fi
echo "ollama: $(ollama --version 2>&1 | head -1)"
if ! ss -tlnp | grep -q 11434; then
  nohup ollama serve > /var/log/ollama.log 2>&1 &
  sleep 6
fi
ss -tlnp | grep 11434 | head -1
echo

echo "--- 4. ollama pull qwen2.5:0.5b-instruct (only if not present) ---"
if ! ollama list 2>/dev/null | grep -q qwen2.5:0.5b-instruct; then
  ollama pull qwen2.5:0.5b-instruct
fi
echo

echo "--- 5. monorepo clone (jv-wave8-production branch = SOVOS/) ---"
if [ ! -d "$POD_HOME/csoai-static-deploy2/.git" ]; then
  cd "$POD_HOME"
  git clone --depth 1 --branch jv-wave8-production https://github.com/CSOAI-ORG/csoai-static-deploy2.git
fi
echo "monorepo: $(du -sh $POD_HOME/csoai-static-deploy2 2>&1)"
echo "packages: $(ls $POD_HOME/csoai-static-deploy2/SOVOS/packages | wc -l)"
echo

echo "=== A100 SOVOS pod READY ==="
echo "next: bash spec6-e2e.sh  →  SOV SIGNAL d, OSCAL v1.1.0 attestation"
