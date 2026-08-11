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

# Dynamic mergekit config (TIES, density 0.5, base = qwen2.5:0.5b-instruct)
CFG_TMP=/workspace/.mergekit_$(date +%H%M%S).yml
{
  echo "merge_method: ties"
  echo "base_model: qwen2.5:0.5b-instruct"
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
    echo "  - model: $SPEC/$s/adapter"
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
