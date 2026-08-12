#!/usr/bin/env bash
# merge_adapters_v2.sh — merge PEFT adapters via mergekit's LoRA path
# with the CORRECT YAML schema:
#   - model: base_model_path
#     lora: lora_path
# plus a --lora-cache-dir flag (or env var).
set -e
SPEC="/root/specialists_v1"
BASE="/root/base_models/Qwen2.5-0.5B-Instruct"
OUT="/root/merge/sweep/oowm_adapters_v2"
LORA_CACHE="/root/merge/sweep/_lora_cache"
mkdir -p "$OUT" "$LORA_CACHE"

cat > /workspace/.mergekit_v2.yml << YAML
merge_method: ties
base_model: $BASE
parameters:
  density: 0.5
  weight: 0.5
  lambda: 0.5
  normalize_weights: true
dtype: float16
out_path: $OUT
models:
  - model: $BASE
    lora: $SPEC/governance/adapter
    weight: 0.40
  - model: $BASE
    lora: $SPEC/safety/adapter
    weight: 0.20
  - model: $BASE
    lora: $SPEC/privacy/adapter
    weight: 0.30
  - model: $BASE
    lora: $SPEC/care/adapter
    weight: 0.30
YAML

echo "=== running mergekit-yaml with proper lora: schema ==="
mergekit-yaml --lora-merge-cache "$LORA_CACHE" /workspace/.mergekit_v2.yml "$OUT" 2>&1 | tail -10
echo ""
echo "=== result ==="
ls -la "$OUT"/ 2>&1 | head -10