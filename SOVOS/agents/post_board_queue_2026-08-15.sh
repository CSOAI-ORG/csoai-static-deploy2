#!/usr/bin/env bash
# post_board_queue_2026-08-15.sh — Run AFTER the overnight board completes
# Loads and measures K3, Qwen3-235B-A22B, DeepSeek-R1 on GSPC axes
set -euo pipefail
cd /workspace/jeeves-exec/SOVOS
LOG="/workspace/jeeves-exec/SOVOS/logs/post-board-$(date +%Y%m%d-%H%M).log"
MODELS="/workspace/models"
HF_HOME="$MODELS/hf"
mkdir -p logs post-board-runs-2026-08-15

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }
log "═══ POST-BOARD MODEL LOAD + MEASURE ═══"

# Install hf CLI if needed
if ! command -v hf &>/dev/null; then
    pip install -q huggingface_hub 2>/dev/null && log "hf CLI installed (pip)" || log "hf CLI not available"
fi

# Step 1: Start K3 model download (background, multi-day, public repo)
log "Step 1: Starting K3 1.56TB model download (background)..."
K3_DEST="/runpod/models/kimi-k3"
mkdir -p "$K3_DEST"
if [ -f "$MODELS/kimi-k3/kimi-k3-in-c/bin/k3" ]; then
    nohup bash "$MODELS/kimi-k3/kimi-k3-in-c/scripts/download-model.sh" "$K3_DEST" \
        > "$MODELS/kimi-k3/download.log" 2>&1 &
    log "  K3 download PID: $! (1.56TB, ~2-3 days)"
    log "  Engine ready at: $MODELS/kimi-k3/kimi-k3-in-c/bin/k3"
fi

# Step 2: Load Qwen3-235B-A22B via Ollama
log "Step 2: Loading Qwen3-235B-A22B..."
ollama pull hf.co/bartowski/Qwen3-235B-A22B-GGUF:Q4_K_M 2>&1 | tail -3 || \
ollama pull qwen3:235b 2>&1 | tail -3 || \
log "  Trying direct HF GGUF..."
# Alternative: pull via Ollama library if available
if ollama list 2>/dev/null | grep -q "qwen3"; then
    log "  Qwen3 already in Ollama"
else
    # Download GGUF from HF directly
    log "  Downloading Qwen3-235B Q4_KM GGUF..."
    pip install -q huggingface-hub[hf_transfer] 2>/dev/null
    # Try a known GGUF provider
    for repo in "bartowski/Qwen3-235B-A22B-GGUF:Q4_K_M" "mradermacher/Qwen3-235B-A22B-GGUF:Q4_K_M"; do
        log "  Trying $repo..."
        huggingface-cli download "$repo" --local-dir "$MODELS/qwen3" --local-dir-use-symlinks False 2>&1 | tail -3 && break
    done
    # Create Modelfile and load into Ollama
    if ls "$MODELS/qwen3"/*.gguf 2>/dev/null; then
        MODFILE="$MODELS/qwen3/Modelfile"
        echo "FROM $(ls $MODELS/qwen3/*.gguf | head -1)" > "$MODFILE"
        (cd "$MODELS/qwen3" && ollama create qwen3-235b -f Modelfile 2>&1 | tail -3)
        log "  Qwen3-235B loaded into Ollama"
    fi
fi

# Step 3: Load DeepSeek-R1
log "Step 3: Loading DeepSeek-R1..."
ollama pull deepseek-r1:671b 2>&1 | tail -3 || \
ollama pull hf.co/unsloth/DeepSeek-R1-GGUF:Q4_K_M 2>&1 | tail -3 || \
log "  Trying Direct GGUF..."
for repo in "unsloth/DeepSeek-R1-GGUF:Q4_K_M" "bartowski/DeepSeek-R1-GGUF:Q4_K_M"; do
    huggingface-cli download "$repo" --local-dir "$MODELS/deepseek-r1" --local-dir-use-symlinks False 2>&1 | tail -3 && break
done
if ls "$MODELS/deepseek-r1"/*.gguf 2>/dev/null; then
    MODFILE="$MODELS/deepseek-r1/Modelfile"
    echo "FROM $(ls $MODELS/deepseek-r1/*.gguf | head -1)" > "$MODFILE"
    (cd "$MODELS/deepseek-r1" && ollama create deepseek-r1-q4 -f Modelfile 2>&1 | tail -3)
    log "  DeepSeek-R1 loaded into Ollama"
fi

# Step 4: Measure models on GSPC city
log "Step 4: Running GSPC city measurements..."
for model in "qwen3-235b" "deepseek-r1-q4"; do
    if ollama list 2>/dev/null | grep -q "$model"; then
        log "  Running $model through cross-lab city..."
        python3 -u agents/cross_lab_city.py \
            --budget 10 --epochs 2 --citizens 20 \
            --local-models "$model" \
            --out "/workspace/jeeves-exec/SOVOS/post-board-runs-2026-08-15/$model/" \
            2>&1 | tee -a "$LOG" || log "  $model city run failed"
    else
        log "  $model not in Ollama — skipping"
    fi
done

# Step 5: Test K3 partial inference
log "Step 5: Testing K3 partial inference..."
K3_BIN="$MODELS/kimi-k3/kimi-k3-in-c/bin/k3"
K3_WEIGHTS="$K3_DEST"
if [ -f "$K3_BIN" ] && ls "$K3_WEIGHTS"/*.safetensors 2>/dev/null | head -1; then
    SHARDS=$(ls "$K3_WEIGHTS"/*.safetensors 2>/dev/null | wc -l)
    log "  K3: $SHARDS/96 shards downloaded — testing partial inference"
    timeout 120 "$K3_BIN" --model "$K3_WEIGHTS" --prompt "What is the capital of France?" 2>&1 | tee -a "$LOG" | head -5 || log "  K3 partial test done"
else
    log "  K3: $SHARDS/96 shards — not enough for inference this cycle" 
fi

log "═══ POST-BOARD CYCLE COMPLETE ═══"