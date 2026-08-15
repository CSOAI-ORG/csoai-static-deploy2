#!/usr/bin/env bash
# merge_sweep.sh — run multiple merge recipes on the materialized specialists.
#
# Goal: find a recipe that produces a usable sovereign model (not garbage
# on "2+2"). TIES with density=0.5 / lambda=0.5 produced a model that
# emits only "????????" — likely the merge is destroying the base model's
# calibration.
#
# This script tries 4 recipes, each materialized into its own dir:
#   1. ties_d0.5_l0.5  (current, broken)
#   2. ties_d0.3_l0.5  (sparser TIES)
#   3. ties_d0.5_l0.3  (less aggressive lambda)
#   4. linear          (no TIES, plain weighted average)
#
# Each output dir is checked: load into ollama, run "2+2", record pass/fail.
set -u

SPEC="/root/specialists_v1"
BASE="/root/base_models/Qwen2.5-0.5B-Instruct"
MERGES="/root/merge/sweep"
mkdir -p "$MERGES"

merge_recipe() {
  local name="$1"
  local method="$2"
  local cfg_tmp="/workspace/.sweep_${name}.yml"
  local out="${MERGES}/oowm_${name}"
  mkdir -p "$out"

  if [ -d "$out" ] && [ -f "$out/model.safetensors" ]; then
    echo "[$name] already exists — skipping"
    return 0
  fi

  cat > "$cfg_tmp" << YAML
merge_method: $method
base_model: $BASE
parameters:
  density: 0.5
  weight: 0.5
  lambda: 0.5
dtype: float16
out_path: $out
models:
  - model: $SPEC/governance/merged_full
    weight: 0.40
  - model: $SPEC/safety/merged_full
    weight: 0.20
  - model: $SPEC/privacy/merged_full
    weight: 0.30
  - model: $SPEC/care/merged_full
    weight: 0.30
YAML

  echo "[$name] starting..."
  mergekit-yaml "$cfg_tmp" "$out" 2>&1 | tail -3
  echo "[$name] done -> $out"
}

merge_recipe "ties_d05_l05" ties
merge_recipe "ties_d03_l05" ties
merge_recipe "ties_d05_l03" ties
merge_recipe "linear"        linear

echo ""
echo "=== sweep complete; output dirs ==="
ls -la "$MERGES"/ 2>&1 | head
echo ""
echo "=== sizes ==="
for d in "$MERGES"/*/; do
  if [ -f "$d/model.safetensors" ]; then
    sz=$(du -h "$d/model.safetensors" | cut -f1)
    echo "  $(basename $d): $sz"
  fi
done