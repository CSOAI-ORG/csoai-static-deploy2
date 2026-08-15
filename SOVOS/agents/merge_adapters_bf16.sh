#!/usr/bin/env bash
# merge_adapters_v3.sh — merge PEFT adapters via mergekit's LoRA path,
# preserving the base model's bfloat16 dtype (downcast to fp16 was the
# garbage-output bug — too much precision loss for a 0.5B model).
set -e
SPEC="/root/specialists_v1"
BASE="/root/base_models/Qwen2.5-0.5B-Instruct"
OUT="/root/merge/sweep/oowm_bf16"
LORA_CACHE="/root/merge/sweep/_lora_cache_bf16"
mkdir -p "$OUT" "$LORA_CACHE"

cat > /workspace/.mergekit_bf16.yml << YAML
merge_method: ties
base_model: $BASE
parameters:
  density: 0.5
  weight: 0.5
  lambda: 0.5
dtype: bfloat16
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

echo "=== running mergekit-yaml with bfloat16 dtype (preserves base precision) ==="
mergekit-yaml --lora-merge-cache "$LORA_CACHE" /workspace/.mergekit_bf16.yml "$OUT" 2>&1 | tail -10
echo ""
echo "=== result ==="
ls -la "$OUT"/ 2>&1 | head -10
echo ""
echo "=== test inference ==="
mkdir -p /root/ollama-models/oowm_bf16
cat > /root/ollama-models/oowm_bf16/Modelfile << EOF
FROM $OUT
TEMPLATE """<|im_start|>system
You are a sovereign AI on Qwen2.5-0.5B.<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""
PARAMETER temperature 0.1
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|im_start|>"
EOF
ollama create oowm-bf16 -f /root/ollama-models/oowm_bf16/Modelfile 2>&1 | tail -2
echo ""
curl -s http://localhost:11434/api/generate -d "{\"model\":\"oowm-bf16:latest\",\"prompt\":\"What is 2+2?\",\"stream\":false,\"options\":{\"num_predict\":30,\"temperature\":0.1}}" 2>&1 | /usr/bin/python3 -c "
import sys, json
d = json.loads(sys.stdin.read())
print(\"oowm-bf16 (bfloat16 merge) on 2+2:\", repr(d.get(\"response\",\"\")))
"