#!/usr/bin/env bash
# Inject model_type= into each specialist's adapter config so mergekit can
# recognise it as Qwen2 when loading from AutoConfig.
#
# mergekit refuses adapters that lack model_type: "ValueError:
# Unrecognized model in /root/specialists_v1/<S>/adapter. Should have a
# `model_type` key in its config.json." The adapter trainer omits
# model_type when saving PEFT adapters; this script patches the
# adapter_config.json (which is now JSON) to include it, so mergekit
# can resolve them as Qwen2Architecture.
set -e
set -u

SPEC="/root/specialists_v1"
LOG="/workspace/fix_adapter_config_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date -Iseconds)] patching adapter configs → add model_type=qwen2" | tee -a "$LOG"

# Pre-flight: also ensure the SYSTEM mergekit python is on PATH (not the venv).
PYTHON_FOR_MERGE="/usr/bin/python3"
if ! "$PYTHON_FOR_MERGE" -c 'from mergekit.scripts.run_yaml import main' 2>/dev/null; then
  echo "  WARN: system python lacks mergekit — skipping merge verification" | tee -a "$LOG"
fi

for s in governance safety privacy care; do
  CFG="$SPEC/$s/adapter/adapter_config.json"
  [ -f "$CFG" ] || { echo "  $s: no adapter_config.json — skipping" | tee -a "$LOG"; continue; }

  # If already has model_type, skip
  if grep -q '"model_type"' "$CFG"; then
    echo "  $s: already has model_type — skipping" | tee -a "$LOG"
    continue
  fi

  echo "  $s: patching $CFG" | tee -a "$LOG"

  # Inline python via env var (avoids heredoc-quoting issues entirely)
  CFG_PATH="$CFG" "$PYTHON_FOR_MERGE" -c '
import json, os, sys
path = os.environ["CFG_PATH"]
d = json.load(open(path))
d["model_type"] = "qwen2"
d["architectures"] = ["Qwen2ForCausalLM"]
# peft adapter_config.json omits the base-model shape; mergekit needs
# these to resolve AutoConfig via qwen2.AutoConfig.
d.setdefault("hidden_size", 896)
d.setdefault("intermediate_size", 4864)
d.setdefault("num_hidden_layers", 24)
d.setdefault("num_attention_heads", 14)
d.setdefault("vocab_size", 151936)
json.dump(d, open(path, "w"), indent=2, sort_keys=True)
print(f"  patched {path}")
'
done

echo "[$(date -Iseconds)] done — adapter configs are now qwen2" | tee -a "$LOG"
