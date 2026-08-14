#!/usr/bin/env bash
# sim_burst.sh — overnight sim burst on the SMALL pod (3090). Runs the city +
# jail sims across the local model set in a loop until morning, signing results
# to /workspace/sims. This offloads the sims from the A100 (the priority signing
# node) so JEEVES's day-one I-runs keep the big GPU.
#
# "Earning the 3KB" honestly: these sims produce the signed raw material
# (city rows, jail containment records) that FEED the flywheel toward the 3KB
# IWM/J-Space card. The distillation INTO the 3KB card is the honey/phlabet step
# (run where the honey pipeline lives) — this burst earns the inputs, not the card.
set -uo pipefail
cd /workspace
export PATH="/usr/local/bin:/usr/bin:$PATH"
export OLLAMA_HOST=127.0.0.1:11434
export PYTHONPATH="/workspace/SOVOS/packages/sovos-city/src:${PYTHONPATH:-}"

# ensure ollama serving
curl -sf 127.0.0.1:11434/api/tags >/dev/null 2>&1 || {
  setsid bash -c "env OLLAMA_HOST=0.0.0.0 OLLAMA_MODELS=/workspace/ollama ollama serve >/workspace/ollama.log 2>&1" </dev/null &
  sleep 6
}

MODELS=$(ollama list | tail -n+2 | awk '{print $1}' | grep -v '^$' | tr '\n' ',' | sed 's/,$//')
[ -z "$MODELS" ] && { echo "no models on this pod — refusing to run an empty sim"; exit 2; }
HOURS="${BURST_HOURS:-8}"
END=$(( $(date +%s) + HOURS*3600 ))
round=0
echo "=== sim burst start · models=[$MODELS] · ${HOURS}h ==="

while [ "$(date +%s)" -lt "$END" ]; do
  round=$((round+1)); TS=$(date -u +%Y%m%dT%H%M%SZ); D="/workspace/sims/$TS"; mkdir -p "$D"
  echo "--- round $round $TS ---"
  # CITY: governed multi-agent arena (stratified → discriminating)
  python3 -m sovos_city --models "$MODELS" --stratified --epochs "${CITY_EPOCHS:-3}" \
      --out "$D/city" --host http://127.0.0.1:11434 > "$D/city.log" 2>&1 && echo "  city: OK" || echo "  city: fail (see city.log)"
  # JAIL: expanded trap bank × each model (containment ranking)
  if [ -f jailboard.py ] && [ -f SOVOS/banks/gspc-jail/items.jsonl ]; then
    for m in $(echo "$MODELS" | tr ',' ' '); do
      python3 jailboard.py --backend ollama --model "$m" --bank SOVOS/banks/gspc-jail/items.jsonl \
          --out "$D/jail_${m//[:\/]/_}.jsonl" >> "$D/jail.log" 2>&1 || echo "  jail: $m fail"
    done
    echo "  jail: done"
  fi
  echo "$TS round $round done" >> /workspace/sims/history.log
done
echo "=== sim burst complete · $round rounds · results in /workspace/sims ==="
