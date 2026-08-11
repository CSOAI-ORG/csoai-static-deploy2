#!/usr/bin/env bash
# Runs the final specialist (care) training on the GPU pod.
# Designed to be called in nohup on the pod:
#   nohup bash run_care_specialist_train.sh > care.log 2>&1 & disown
#
# Idempotent — aborts if adapter already exists. Re-mergeable.
set -e
set -u

SPEC="/root/specialists_v1"
LOG="/workspace/care_specialist_train.log"
PY="/workspace/sov-governance-venv/bin/python"

# Already trained? Skip.
if [ -f "$SPEC/care/adapter/adapter_config.json" ]; then
  echo "[$(date -Iseconds)] care adapter already exists at $SPEC/care/adapter — skipping." | tee -a "$LOG"
  exit 0
fi

# Preconditions
mkdir -p "$SPEC/care"
[ -f "$SPEC/normalized/care.jsonl" ] || { echo "FATAL: $SPEC/normalized/care.jsonl not found" | tee -a "$LOG"; exit 1; }

cd "$SPEC"
echo "[$(date -Iseconds)] starting care specialist training (LoRA, rank 8, Qwen2.5-0.5B base)" | tee -a "$LOG"

# Match the trainer's actual CLI (verified via --help)
"$PY" /workspace/train_refusal_lora.py \
  --data "$SPEC/normalized/care.jsonl" \
  --out "$SPEC/care" \
  --name "sov-care-v1" \
  --rank 8 \
  --epochs 3 \
  --lr 2e-4 \
  >> "$LOG" 2>&1

# Sanity: did the adapter get written?
if [ ! -f "$SPEC/care/adapter/adapter_config.json" ]; then
  echo "[$(date -Iseconds)] TRAINING DID NOT PRODUCE ADAPTER — see $LOG" | tee -a "$LOG"
  exit 2
fi

echo "[$(date -Iseconds)] care adapter trained and saved" | tee -a "$LOG"
echo "  size: $(du -sh $SPEC/care/adapter | cut -f1)" | tee -a "$LOG"

# 3KB provenance card for care (best-effort, optional)
if [ -f /workspace/sov_3kb_converter.py ]; then
  echo "[$(date -Iseconds)] generating 3KB provenance card" | tee -a "$LOG"
  "$PY" /workspace/sov_3kb_converter.py "$SPEC/care" > "$SPEC/care.3kb" 2>>"$LOG" || true
  if [ -s "$SPEC/care.3kb" ]; then
    echo "  card: $(wc -c < $SPEC/care.3kb) bytes" | tee -a "$LOG"
  fi
fi

echo "[$(date -Iseconds)] DONE — care specialist ready for TIES merge" | tee -a "$LOG"
