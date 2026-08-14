#!/usr/bin/env bash
# m4_fluid_keeper.sh — the M4 as an always-on FLUID node (the Zeus/generate half
# of the OWEM sandwich brain). Runs LOCALLY on the M4, cron'd. Free ($0), offline.
#
# Each pass:
#   1. MEASURE local ollama models on GSPC (governance/safety/art5) → signed board
#   2. TRAIN a LoRA adapter with MLX QLoRA on the Art-5 governance set (on-device)
#   3. outputs land in benchmark-results/m4_fluid/ + mlx_adapters/ (EAT syncs them)
#
# The frozen/sign/commit step is NOT here — that belongs on the A100/Oracle
# (the Eunomia/frozen crust). This node only produces fluid evolution material.
set -uo pipefail
cd "$HOME/clawd/csoai-static-deploy2" || exit 1
export OLLAMA=http://localhost:11434
export PYTHONPATH="$PWD/SOVOS/packages/sovos-city/src:${PYTHONPATH:-}"
TS=$(date -u +%Y%m%dT%H%M%SZ); D="benchmark-results/m4_fluid/$TS"; mkdir -p "$D"

# ensure ollama is serving locally
curl -sf http://localhost:11434/api/tags >/dev/null 2>&1 || { (ollama serve >/dev/null 2>&1 &); sleep 4; }

# 1) MEASURE — the fluid judge signal (control-anchored, honest)
MODELS=$(ollama list 2>/dev/null | tail -n+2 | awk '{print $1}' | grep -v '^$' | tr '\n' ' ')
CTRL=$(printf '%s\n' $MODELS | grep -iE '0\.5b' | head -1)
if [ -n "$MODELS" ]; then
  python3 gspc_flywheel.py --models $MODELS ${CTRL:+--control "$CTRL"} \
      --axes governance safety art5 > "$D/measure.log" 2>&1 && echo "  measure: ok" || echo "  measure: fail"
fi

# 2) TRAIN — MLX QLoRA on-device, free (only if a quantized MLX model exists)
Q="mlx_models/qwen1.5b-q4"
if [ -d "$Q" ] && [ -f mlx_data/train.jsonl ]; then
  python3 -m mlx_lm lora --model "$Q" --train --data mlx_data --iters 20 --batch-size 1 \
      --adapter-path "mlx_adapters/$TS" > "$D/train.log" 2>&1 && echo "  train: ok (adapter → mlx_adapters/$TS)" || echo "  train: fail"
else
  echo "  train: skipped (quantized model not ready yet)"
fi

echo "$TS m4 fluid pass done" >> benchmark-results/m4_fluid/history.log
echo "  === M4 fluid pass $TS done → $D ==="
