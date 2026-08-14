#!/usr/bin/env bash
# nightly_gated_loop.sh — CSOAI honest measure → gated-evolve loop. Runs on the A100.
#
# SAFE for unsupervised nightly use BY DESIGN:
#   1) MEASURE the whole fleet on the GSPC axes — read-only inference, only ever
#      produces honest numbers (Wilson-CI, control-anchored, UNMEASURED-honest).
#   2) EVOLVE (gated): train ONE candidate from fuel, then RE-MEASURE it. It does
#      NOT auto-promote — it prints the ADOPT/KEEP verdict and leaves the swap to a
#      human. Gates: honey_barrier (won't train on a contaminated ruler) +
#      ouroboros verdict (a candidate that can't beat base is flagged KEEP).
#   Worst case of a bad training run: a rejected candidate + an honest "KEEP base".
#      Nothing in the live fleet changes without a human reading the verdict.
#
# Results land on the 2.3 PB /workspace network volume (survives pod restart).
# A second-machine copy (Mac pull / HF) is the durability completion — see README.
set -uo pipefail
cd /workspace
export OLLAMA_HOST=127.0.0.1:11434
export PYTHONPATH="/workspace/SOVOS/packages/sovos-city/src:${PYTHONPATH:-}"
TS=$(date -u +%Y%m%dT%H%M%SZ)
D=/workspace/nightly/$TS; mkdir -p "$D"
exec > >(tee -a "$D/loop.log") 2>&1
echo "=== CSOAI nightly gated loop $TS ==="

# ensure ollama is serving
curl -sf 127.0.0.1:11434/api/tags >/dev/null 2>&1 || {
  setsid bash -c "env OLLAMA_HOST=0.0.0.0 OLLAMA_MODELS=/workspace/ollama ollama serve >/workspace/ollama.log 2>&1" </dev/null &
  sleep 6
}

# ── 1) MEASURE the fleet (always on; cannot harm anything) ──────────────────
CONTROL="${CONTROL:-qwen2.5:0.5b-instruct}"
MODELS=$(ollama list | tail -n+2 | awk '{print $1}' | grep -v "^$CONTROL$" | grep -v "^$" | tr '\n' ' ')
echo "--- MEASURE: $(echo $MODELS | wc -w) models × GSPC axes (control=$CONTROL) ---"
if python3 -u gspc_flywheel.py --models $MODELS --control "$CONTROL" > "$D/fleet_measure.log" 2>&1; then
  echo "  measure: OK"; tail -3 "$D/fleet_measure.log"
else
  echo "  measure: FAILED (see $D/fleet_measure.log)"
fi

# ── 2) GATED EVOLVE (trains a candidate + re-measures; NEVER auto-promotes) ──
# Default ON — safe because it can't change the live fleet. Set NIGHTLY_EVOLVE=0
# to run measure-only. Requires close_train_hop.py + the trainer stack on the pod.
GPU_BUSY=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
if [ "${NIGHTLY_EVOLVE:-1}" = "1" ] && [ "${GPU_BUSY:-100}" -lt 40 ] && [ -f close_train_hop.py ]; then
  echo "--- EVOLVE (gated): honey_barrier + ouroboros verdict, no auto-promote ---"
  if python3 -u close_train_hop.py \
        --base "${EVOLVE_BASE:-qwen2.5:1.5b}" \
        --hf-base "${EVOLVE_HF_BASE:-Qwen/Qwen2.5-1.5B-Instruct}" \
        --steps "${EVOLVE_STEPS:-100}" > "$D/evolve.log" 2>&1; then
    echo "  evolve: candidate trained + re-measured (read the verdict — promotion is yours)"
    tail -4 "$D/evolve.log"
  else
    echo "  evolve: skipped/failed (gate tripped or trainer deps missing) — see $D/evolve.log"
  fi
else
  echo "--- EVOLVE: skipped — NIGHTLY_EVOLVE=0, close_train_hop absent, or GPU busy=${GPU_BUSY}% (yielding to priority A100 I-runs per queue discipline) ---"
fi

# ── 3) CITY SIM — governed multi-agent arena across the fleet (agentic) ──────
# Runs each fleet model as a citizen through the governed city arena (stratified
# so the bank can discriminate). Needs the sovos_city package on the pod; skips
# cleanly otherwise. Read-only w.r.t. the live fleet.
if [ "${NIGHTLY_CITY:-1}" = "1" ] && python3 -c "import sovos_city" 2>/dev/null; then
  echo "--- CITY SIM: fleet through the governed arena (stratified) ---"
  python3 -m sovos_city --models "$(echo $MODELS | tr ' ' ',')" --stratified \
      --epochs "${CITY_EPOCHS:-2}" --out "$D/city" --host 127.0.0.1:11434 > "$D/city.log" 2>&1 \
      && { echo "  city: OK"; tail -2 "$D/city.log"; } || echo "  city: skipped/failed — see $D/city.log"
else
  echo "--- CITY SIM: disabled (NIGHTLY_CITY=0 or sovos_city not on pod) ---"
fi

# ── 4) JAIL BOARD — expanded trap bank (61 items / 36 traps) across the fleet ─
# Axis-14 containment ranking. The bigger bank (was 37) is what lets n>=30
# separate models — the exact gap the axis-14 board flagged. Deterministic.
JAIL_BANK="SOVOS/banks/gspc-jail/items.jsonl"
if [ "${NIGHTLY_JAIL:-1}" = "1" ] && [ -f "$JAIL_BANK" ] && [ -f jailboard.py ]; then
  echo "--- JAIL BOARD: $(wc -l < "$JAIL_BANK") trap items × $(echo $MODELS | wc -w) models ---"
  for m in $MODELS; do
    python3 jailboard.py --backend ollama --model "$m" --bank "$JAIL_BANK" \
        --out "$D/jail_${m//[:\/]/_}.jsonl" >> "$D/jail.log" 2>&1 || echo "  jail: $m failed"
  done
  echo "  jail: done → $D/jail.log"
else
  echo "--- JAIL BOARD: disabled or bank/harness absent ---"
fi

# ── 5) UNSIGNED REPORT — produce side of the signed-card leg ────────────────
# The signing key never leaves the owner keystone, so pods produce UNSIGNED
# nightly summaries; the Mac-side signer (SOVOS/agents/card_issuer.py) turns
# them into Ed25519-signed 3KB cards and lands them in signed-cards/.
# An unsigned report is a claim; a signed card is a receipt. Never confuse them.
REPORT="$D/nightly_report.json"
python3 - "$D" "$TS" "$CONTROL" <<'PYEOF'
import hashlib, json, sys
from pathlib import Path
d, ts, control = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
loop_log = d / "loop.log"
rep = {
  "at": ts,
  "kind": "nightly-gated-loop",
  "control": control,
  "artifacts": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(d.glob("*.log"))},
  "loop_log_sha256": hashlib.sha256(loop_log.read_bytes()).hexdigest()
      if loop_log.exists() else None,
}
(d / "nightly_report.json").write_text(json.dumps(rep, indent=1) + "\n")
PYEOF
MINIO_DIR=/runpod/sovos-master/evidence/nightly
[ -d /runpod/sovos-master ] && { mkdir -p "$MINIO_DIR"; cp "$REPORT" "$MINIO_DIR/$TS.json"; }
echo "  unsigned report → $REPORT (sign Mac-side: card_issuer.py issue --report ... --kind nightly)"

echo "=== done $TS → $D (persistent volume) ==="
echo "$TS done" >> /workspace/nightly/history.log
