#!/usr/bin/env bash
# Create config.json alongside adapter_config.json for each specialist.
# mergekit's AutoConfig.from_pretrained looks for config.json, NOT
# adapter_config.json. So we synthesise a Qwen2-shaped config.json
# so mergekit can resolve the architecture.
set -e
set -u

SPEC="/root/specialists_v1"
LOG="/workspace/fix_adapter_config_full_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date -Iseconds)] patching adapter configs: model_type + config.json" | tee -a "$LOG"

for s in governance safety privacy care; do
  ACFG="$SPEC/$s/adapter/adapter_config.json"
  CFG="$SPEC/$s/adapter/config.json"
  [ -f "$ACFG" ] || { echo "  $s: no adapter_config.json — skipping" | tee -a "$LOG"; continue; }

  if [ -f "$CFG" ] && grep -q '"model_type"' "$CFG" 2>/dev/null; then
    echo "  $s: config.json already exists with model_type — skipping" | tee -a "$LOG"
    continue
  fi

  echo "  $s: writing config.json from qwen2 model shape" | tee -a "$LOG"
  CFG_PATH="$CFG" ACFG_PATH="$ACFG" /usr/bin/python3 -c '
import json, os
cfg_path = os.environ["CFG_PATH"]
acfg_path = os.environ["ACFG_PATH"]
# PEFT adapter_config.json has the LoRA hyperparams; build a parallel
# config.json with the qwen2 base-model shape (Qwen2.5-0.5B-Instruct
# defaults from the transformers source).
config = {
    "architectures": ["Qwen2ForCausalLM"],
    "attention_dropout": 0.0,
    "bos_token_id": 151643,
    "eos_token_id": 151645,
    "hidden_act": "silu",
    "hidden_size": 896,
    "initializer_range": 0.02,
    "intermediate_size": 4864,
    "max_position_embeddings": 32768,
    "max_window_layers": 24,
    "model_type": "qwen2",
    "num_attention_heads": 14,
    "num_hidden_layers": 24,
    "num_key_value_heads": 2,
    "rms_norm_eps": 1e-06,
    "rope_theta": 1000000.0,
    "sliding_window": 32768,
    "tie_word_embeddings": True,
    "torch_dtype": "float16",
    "transformers_version": "4.46.0",
    "use_cache": True,
    "use_sliding_window": False,
    "vocab_size": 151936,
}
# Carry through base-model_name_or_path if present
try:
    a = json.load(open(acfg_path))
    if "base_model_name_or_path" in a:
        config["base_model_name_or_path"] = a["base_model_name_or_path"]
except Exception:
    pass
with open(cfg_path, "w") as f:
    json.dump(config, f, indent=2, sort_keys=True)
    f.write("\n")
print(f"  wrote {cfg_path}")
'
done

echo "[$(date -Iseconds)] done — every adapter now has model_type + config.json" | tee -a "$LOG"
