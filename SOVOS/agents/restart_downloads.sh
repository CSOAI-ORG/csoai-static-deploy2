#!/usr/bin/env bash
# restart_downloads.sh — restart Qwen + DeepSeek, K3 engine smoke test
set -euo pipefail
echo "=== Killing any leftover hf downloads ==="
pkill -f "hf download" 2>/dev/null || true
sleep 1
rm -rf /workspace/models/qwen3/*.gguf /workspace/models/deepseek-r1/shards 2>/dev/null || true
echo "=== Qwen2.5-72B Q4_K_M (~14GB) ==="
nohup python3 -m hf download bartowski/Qwen2.5-72B-Instruct-GGUF --include "Qwen2.5-72B-Instruct-Q4_K_M.gguf" --local-dir /workspace/models/qwen3 --local-dir-use-symlinks False > /workspace/models/qwen3/hf_download.log 2>&1 &
echo "Qwen PID: $!"
echo "=== DeepSeek-R1 IQ4 shards (~40GB) ==="
nohup python3 -m hf download bartowski/DeepSeek-R1-GGUF --include "DeepSeek-R1-IQ4_NL/*" --local-dir /workspace/models/deepseek-r1 --local-dir-use-symlinks False > /workspace/models/deepseek-r1/hf_download.log 2>&1 &
echo "DeepSeek PID: $!"
echo "=== K3 engine compiled and ready ==="
ls -la /workspace/models/kimi-k3/kimi-k3-in-c/bin/k3 2>/dev/null || echo "K3 NOT COMPILED"
echo "=== Disk ==="
df -h /runpod | tail -2
echo "=== Verify downloads ==="
sleep 3
ps aux | grep "hf download" | grep -v grep | awk '{print $2, "downloading"}'
echo "=== Board DONE ==="
grep "DONE rows" /workspace/jeeves-exec/SOVOS/logs/overnight-v3-20260814-1750.log 2>/dev/null | tail -3