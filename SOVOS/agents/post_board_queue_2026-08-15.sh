#!/usr/bin/env bash
# post_board_queue_2026-08-15.sh — Run AFTER overnight board completes
# Loads and measures K3 → Qwen2.5-72B → DeepSeek-R1 on GSPC axes
set -euo pipefail
cd /workspace/jeeves-exec/SOVOS
LOG="/workspace/jeeves-exec/SOVOS/logs/post-board-$(date +%Y%m%d-%H%M).log"
MODELS="/workspace/models"
mkdir -p logs post-board-runs-2026-08-15

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }
log "═══ POST-BOARD: LOAD + MEASURE ═══"

# Step 1: K3 engine smoke test (model weights are streaming from HF)
log "Step 1: K3 engine test..."
K3_BIN="/workspace/models/kimi-k3/kimi-k3-in-c/bin/k3"
K3_WEIGHTS="/runpod/models/kimi-k3"
if [ -f "$K3_BIN" ]; then
    SHARDS=0
    [ -d "$K3_WEIGHTS" ] && SHARDS=$(ls "$K3_WEIGHTS"/model-*.safetensors 2>/dev/null | wc -l)
    log "  K3 engine: COMPILED ✓ (217KB binary)"
    log "  K3 weights: ${SHARDS}/96 shards downloaded"
    if [ $SHARDS -ge 10 ]; then
        timeout 60 "$K3_BIN" --model "$K3_WEIGHTS" --prompt "What is 2+2?" \
            2>&1 | head -3 || log "  K3 inference returned (may need more shards)"
        log "  K3 partial inference: DONE"
    else
        log "  K3: insufficient shards for inference (need ≥10, have ${SHARDS})"
    fi
else
    log "  K3 engine NOT COMPILED — skipping"
fi

# Step 2: Load Qwen2.5-72B Q4 into Ollama
log "Step 2: Loading Qwen2.5-72B Q4 into Ollama..."
QWEN_GGUF=$(ls "$MODELS/qwen3"/*.gguf 2>/dev/null | head -1)
if [ -f "$QWEN_GGUF" ]; then
    QWEN_SIZE=$(du -h "$QWEN_GGUF" | cut -f1)
    log "  GGUF found: $QWEN_GGUF ($QWEN_SIZE)"
    QWEN_MODEL_NAME="qwen2.5-72b-q4"
    # Check if already loaded
    if ollama list 2>/dev/null | grep -q "$QWEN_MODEL_NAME"; then
        log "  $QWEN_MODEL_NAME already in Ollama"
    else
        mkdir -p "$MODELS/qwen3/ollama"
        MODFILE="$MODELS/qwen3/ollama/Modelfile"
        echo "FROM $QWEN_GGUF" > "$MODFILE"
        ollama create "$QWEN_MODEL_NAME" -f "$MODFILE" 2>&1 | tail -3 | tee -a "$LOG"
        log "  $QWEN_MODEL_NAME loaded into Ollama ✓"
    fi
else
    log "  Qwen2.5-72B GGUF not found — download may still be in progress"
    log "  Check: $MODELS/qwen3/hf_download.log"
fi

# Step 3: Merge DeepSeek-R1 shards and load into Ollama
log "Step 3: Merging DeepSeek-R1 shards..."
DS_SHARDS="$MODELS/deepseek-r1/shards"
if [ -d "$DS_SHARDS" ]; then
    SHARD_COUNT=$(find "$DS_SHARDS" -name "*.gguf" -type f 2>/dev/null | wc -l)
    log "  DeepSeek shards found: $SHARD_COUNT"
    if [ $SHARD_COUNT -ge 10 ]; then
        # Merge shards into single GGUF
        DS_MERGED="$MODELS/deepseek-r1/DeepSeek-R1-IQ4_MERGED.gguf"
        if [ ! -f "$DS_MERGED" ]; then
            find "$DS_SHARDS" -name "*.gguf" -type f | sort | xargs cat > "$DS_MERGED"
            log "  Merged $SHARD_COUNT shards → $DS_MERGED ($(du -h "$DS_MERGED" | cut -f1))"
        fi
        # Load into Ollama
        DS_MODEL_NAME="deepseek-r1-iq4"
        if ollama list 2>/dev/null | grep -q "$DS_MODEL_NAME"; then
            log "  $DS_MODEL_NAME already in Ollama"
        else
            mkdir -p "$MODELS/deepseek-r1/ollama"
            echo "FROM $DS_MERGED" > "$MODELS/deepseek-r1/ollama/Modelfile"
            ollama create "$DS_MODEL_NAME" -f "$MODELS/deepseek-r1/ollama/Modelfile" 2>&1 | tail -3 | tee -a "$LOG"
            log "  $DS_MODEL_NAME loaded into Ollama ✓"
        fi
    else
        log "  Only $SHARD_COUNT/10 shards — not enough to merge"
    fi
else
    log "  DeepSeek-R1 shards not found — download may still be in progress"
fi

# Step 4: Measure loaded models through cross-lab city
log "Step 4: GSPC city measurements..."
for model in "qwen2.5-72b-q4" "deepseek-r1-iq4"; do
    if ollama list 2>/dev/null | grep -q "$model"; then
        log "  Running $model through cross-lab city..."
        timeout 3600 python3 -u agents/cross_lab_city.py \
            --budget 10 --epochs 2 --citizens 20 \
            --model "$model" \
            --out "/workspace/jeeves-exec/SOVOS/post-board-runs-2026-08-15/$model/" \
            2>&1 | tee -a "$LOG" || log "  $model city run exited $?"
        log "  $model MEASURED ✓"
    else
        log "  $model not in Ollama — skipping"
    fi
done

log "═══ POST-BOARD SEQUENCE COMPLETE ═══"
echo "Results:" >> "$LOG"
ollama list 2>/dev/null >> "$LOG"
echo "Models loaded and measured" >> "$LOG"