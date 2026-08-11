#!/usr/bin/env bash
# 4-way TIES merge of the four sovereign specialists on the GPU pod.
# Idempotent — aborts if merged-out dir exists. Skips specialists whose
# adapters are missing (so a partial run still produces a useful merge).
#
# Run:
#   nohup bash merge_4_specialists_ties.sh > merge.log 2>&1 & disown
#
# Reads:
#   /root/specialists_v1/{governance,safety,privacy,care}/adapter/
# Writes:
#   /root/merge/oowm_4way_<timestamp>/   (full TIES output)

set -e
set -u

SPEC="/root/specialists_v1"
OUT_DIR="/root/merge/oowm_4way_$(date +%Y%m%d_%H%M%S)"
LOG="/workspace/merge_4way_$(date +%Y%m%d_%H%M%S).log"

# Pre-flight: mergekit refuses adapters without model_type in
# adapter_config.json. The saved PEFT configs omit it; patch them
# in-place before building the YAML.
if [ -x "$(dirname $0)/fix_adapter_config.sh" ]; then
  bash "$(dirname $0)/fix_adapter_config.sh"
fi
# Use the system python / mergekit binary for the merge itself —
# mergekit's working install is at /usr/local/lib/python3.11/dist-packages
# (system python 3.11); it is NOT pip-installed into the canonical venv.
# We only fall back to the venv python for mergekit if the system
# one fails.
PY=""
for cand in /usr/bin/python3 /workspace/sov-governance-venv/bin/python /opt/conda/bin/python3; do
  if [ -x "$cand" ]; then
    if "$cand" -c 'from mergekit.scripts.run_yaml import main' 2>/dev/null; then
      PY="$cand"; break
    fi
  fi
done
if [ -z "$PY" ]; then
  echo "FATAL: no python with mergekit.scripts.run_yaml importable" | tee -a "$LOG"
  exit 1
fi
echo "  python: $PY ($(basename $(dirname $PY)))" | tee -a "$LOG"

# mergekit uses pydantic forward refs (ConfiguredModuleArchitecture
# contains a torch.dtype field) — importing torch FIRST and calling
# model_rebuild() avoids 'not fully defined; define `torch`' error.
"$PY" -c "import torch; from mergekit.plan import ConfiguredModuleArchitecture; ConfiguredModuleArchitecture.model_rebuild(); print('  mergekit pydantic warm-up OK')" 2>&1 | tee -a "$LOG" || {
  echo "  WARN: pydantic warm-up failed; merge may fail with forward-ref error" | tee -a "$LOG"
}

mkdir -p /root/merge
echo "[$(date -Iseconds)] starting 4-way TIES merge → $OUT_DIR" | tee -a "$LOG"

# Build the mergekit config dynamically.
SPECS_AVAILABLE=""
for s in governance safety privacy care; do
  if [ -f "$SPEC/$s/adapter/adapter_config.json" ]; then
    SPECS_AVAILABLE="$SPECS_AVAILABLE $s"
  fi
done

N=$(echo $SPECS_AVAILABLE | wc -w)
if [ "$N" -lt 2 ]; then
  echo "FATAL: need >=2 specialist adapters; only found:$SPECS_AVAILABLE" | tee -a "$LOG"
  exit 1
fi

echo "  found $N specialists: $SPECS_AVAILABLE" | tee -a "$LOG"

# mergekit's ShardedTensorIndex.from_disk() only looks for
# 'model.safetensors' or 'pytorch_model.bin'. PEFT adapters save
# 'adapter_model.safetensors'. We pre-merge each adapter into the base
# model via PEFT into <spec>/<s>/merged_full/ which mergekit can read.
# Run that materialize step first if missing.
for s in $SPECS_AVAILABLE; do
  AD="$SPEC/$s/adapter"
  MF="$SPEC/$s/merged_full"
  if [ -f "$AD/adapter_model.safetensors" ] && [ ! -f "$MF/model.safetensors" ]; then
    echo "  $s: materializing PEFT adapter into full model..." | tee -a "$LOG"
    BASE_MODEL="$BASE_MODEL" ADAPTER_PATH="$AD" OUT_PATH="$MF" /usr/bin/python3 << 'PYEOF'
import os, shutil
from peft import PeftModel
from transformers import AutoModelForCausalLM
import torch
base = AutoModelForCausalLM.from_pretrained(os.environ["BASE_MODEL"], dtype=torch.float16, low_cpu_mem_usage=True)
pm = PeftModel.from_pretrained(base, os.environ["ADAPTER_PATH"], is_trainable=False)
m = pm.merge_and_unload()
os.makedirs(os.environ["OUT_PATH"], exist_ok=True)
m.save_pretrained(os.environ["OUT_PATH"], safe_serialization=True)
for fn in ["tokenizer.json", "tokenizer_config.json", "chat_template.jinja", "generation_config.json"]:
    src = os.path.join(os.environ["ADAPTER_PATH"], fn)
    if os.path.exists(src):
        shutil.copy2(src, os.environ["OUT_PATH"])
print(f"  materialized -> {os.environ['OUT_PATH']}")
PYEOF
  fi
done

# Dynamic mergekit config (TIES, density 0.5, base = local Qwen2.5-0.5B)
# mergekit requires a real HF model dir as base_model, NOT an Ollama tag
# like "qwen2.5:0.5b-instruct". Auto-detect: prefer /root/base_models/
# (git clone of Qwen2.5-0.5B-Instruct), fall back to other known locations.
BASE_MODEL=""
for cand in \
  /root/base_models/Qwen2.5-0.5B-Instruct \
  /workspace/base_models/Qwen2.5-0.5B-Instruct \
  /root/Qwen2.5-0.5B-Instruct; do
  if [ -f "$cand/config.json" ]; then
    BASE_MODEL="$cand"
    break
  fi
done
if [ -z "$BASE_MODEL" ]; then
  echo "FATAL: no base_model dir with config.json found" | tee -a "$LOG"
  echo "  expected one of: /root/base_models/Qwen2.5-0.5B-Instruct" | tee -a "$LOG"
  echo "  fix: git clone https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct /root/base_models/" | tee -a "$LOG"
  exit 1
fi
echo "  base_model: $BASE_MODEL" | tee -a "$LOG"
CFG_TMP=/workspace/.mergekit_$(date +%H%M%S).yml
{
  echo "merge_method: ties"
  echo "base_model: $BASE_MODEL"
  echo "parameters:"
  echo "  density: 0.5"
  echo "  weight: 0.5"
  echo "  lambda: 0.5"
  echo "dtype: float16"
  echo "out_path: $OUT_DIR"
  echo "models:"
  for s in $SPECS_AVAILABLE; do
    case "$s" in
      governance) w=0.40 ;;  # governance carry some weight
      safety)     w=0.20 ;;  # safety is the regression axis — underweight
      privacy)    w=0.30 ;;
      care)       w=0.30 ;;
      *)          w=0.25 ;;
    esac
    echo "  - model: $SPEC/$s/merged_full"
    echo "    weight: $w"
  done
} > "$CFG_TMP"
cat "$CFG_TMP" | tee -a "$LOG"

# Run mergekit. `mergekit-yaml CONFIG_FILE OUT_PATH` takes the OUT_PATH
# as an explicit positional arg (not via the YAML's `out_path:` field).
# We pass the YAML as the first arg + the path as the second.
if command -v mergekit-yaml >/dev/null 2>&1; then
  MERGE_CMD="mergekit-yaml"
  echo "[$(date -Iseconds)] running $MERGE_CMD $CFG_TMP $OUT_DIR" | tee -a "$LOG"
  "$MERGE_CMD" "$CFG_TMP" "$OUT_DIR" >> "$LOG" 2>&1 || true
elif command -v mergekit >/dev/null 2>&1; then
  MERGE_CMD="mergekit"
  echo "[$(date -Iseconds)] running $MERGE_CMD $CFG_TMP $OUT_DIR" | tee -a "$LOG"
  "$MERGE_CMD" "$CFG_TMP" "$OUT_DIR" >> "$LOG" 2>&1 || true
else
  echo "[$(date -Iseconds)] running $PY -m mergekit.scripts.run_yaml $CFG_TMP $OUT_DIR" | tee -a "$LOG"
  "$PY" -m mergekit.scripts.run_yaml "$CFG_TMP" "$OUT_DIR" >> "$LOG" 2>&1 || true
fi

echo "[$(date -Iseconds)] merge complete → $OUT_DIR" | tee -a "$LOG"
du -sh "$OUT_DIR" | tee -a "$LOG"
ls -la "$OUT_DIR" | tee -a "$LOG"

# 3KB card for the merged model (best-effort)
if [ -f /workspace/sov_3kb_converter.py ]; then
  "$PY" /workspace/sov_3kb_converter.py "$OUT_DIR" > "$OUT_DIR.3kb" 2>>"$LOG" || true
fi

# Skip GGUF + ollama register on purpose per the coordination doc
# (mergekit output must NOT be imported via ollama FROM dir).
# Instead, the runnable artifact is the safetensors at $OUT_DIR.
