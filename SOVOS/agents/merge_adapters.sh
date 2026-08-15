#!/usr/bin/env bash
# merge_adapters.sh — merge PEFT adapters using mergekit's LoRA path directly.
# Bypasses the materialize step.
set -e
SPEC="/root/specialists_v1"
BASE="/root/base_models/Qwen2.5-0.5B-Instruct"
OUT="/root/merge/sweep/oowm_adapters_direct"
mkdir -p "$OUT"

# Use mergekit's lora: syntax (handles PEFT adapters natively)
cat > /workspace/.mergekit_adapters.yml << YAML
merge_method: ties
base_model: $BASE
parameters:
  density: 0.5
  weight: 0.5
  lambda: 0.5
dtype: float16
out_path: $OUT
models:
  - model: $SPEC/governance/adapter
    lora: true
    weight: 0.40
  - model: $SPEC/safety/adapter
    lora: true
    weight: 0.20
  - model: $SPEC/privacy/adapter
    lora: true
    weight: 0.30
  - model: $SPEC/care/adapter
    lora: true
    weight: 0.30
YAML

echo "=== running mergekit-yaml with lora:true syntax ==="
mergekit-yaml /workspace/.mergekit_adapters.yml "$OUT" 2>&1 | tail -10
echo ""
echo "=== result ==="
ls -la "$OUT"/ 2>&1 | head -10