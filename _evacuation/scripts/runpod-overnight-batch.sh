#!/bin/bash
# overnight_batch.sh — runs ON the 3090 pod (EU-CZ-1) through the 04:00 window.
# All heavy compute lives here; the Mac only dispatches + collects + commits.
# Idempotent: every leg checks for an existing process/lock before starting.
# Log: /workspace/overnight/batch.log
set -uo pipefail
mkdir -p /workspace/overnight /workspace/SOVOS/living
LOG=/workspace/overnight/batch.log
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }
echo "===== overnight batch start $(TS) =====" >> "$LOG"

# ── Leg 0: arena keeper alive? (the 24x7 ELO loop) ────────────────
if ! pgrep -f arena_loop_keeper.py >/dev/null; then
  echo "$(TS) arena keeper DEAD — restarting" >> "$LOG"
  cd /workspace/arena-24x7 && nohup setsid python3 arena_loop_keeper.py >> keeper.log 2>&1 < /dev/null & disown
  sleep 2
  pgrep -f arena_loop_keeper.py >/dev/null && echo "$(TS) arena keeper restarted" >> "$LOG"
else
  echo "$(TS) arena keeper alive ($(wc -l < /workspace/arena-24x7/reborn_rounds.jsonl) rounds)" >> "$LOG"
fi

# ── Leg 1: grok referee alive? ────────────────────────────────────
if ! pgrep -f grok_referee_keeper.py >/dev/null; then
  echo "$(TS) grok referee DEAD — restarting" >> "$LOG"
  cd /workspace && nohup setsid python3 /workspace/sov33-oowm/oowm/grok_referee_keeper.py >> /workspace/arena-24x7/grok_referee_keeper.log 2>&1 < /dev/null & disown
else
  echo "$(TS) grok referee alive" >> "$LOG"
fi

# ── Leg 2: F2 data-gen (synth pair flywheel, v2 with 101-prompt bank) ───
# Priority rule: never run f2 while the specialist ring is using ollama
# (ring = the 12-around-1 council architecture in execution; it owns the queue).
if pgrep -f specialist_ring >/dev/null; then
  echo "$(TS) specialist_ring RUNNING — f2 deferred (ollama priority rule)" >> "$LOG"
elif pgrep -f f2_gen >/dev/null; then
  echo "$(TS) f2_gen RUNNING ($(wc -l < /workspace/f2/sovereign_synth.jsonl 2>/dev/null || echo 0) pairs)" >> "$LOG"
else
  if [ -f /workspace/f2_gen_v2.py ]; then
    echo "$(TS) f2 v2 idle — relaunching 300 (101-prompt bank)" >> "$LOG"
    cd /workspace && nohup python3 f2_gen_v2.py 300 > f2_v2.log 2>&1 & disown
  elif [ -f /workspace/f2_gen.py ]; then
    echo "$(TS) f2 v1 idle — relaunching 400 (legacy bank)" >> "$LOG"
    cd /workspace && nohup python3 f2_gen.py 400 > f2_run.log 2>&1 & disown
  else
    echo "$(TS) f2_gen missing on pod — skip" >> "$LOG"
  fi
fi

# ── Leg 3: gold bank re-verify (only if gold_results missing) ─────
if [ -f /workspace/gold_results.json ]; then
  echo "$(TS) gold results present (kept from earlier run)" >> "$LOG"
fi

# ── Leg 4: 3KB units regen (unit_decompose on pod if present) ─────
if [ -f /workspace/unit_decompose.py ]; then
  if [ ! -f /workspace/SOVOS/living/units/units.jsonl ]; then
    echo "$(TS) generating 3KB units" >> "$LOG"
    cd /workspace && python3 unit_decompose.py >> "$LOG" 2>&1 || echo "$(TS) units gen failed" >> "$LOG"
  else
    echo "$(TS) units.jsonl present ($(wc -l < /workspace/SOVOS/living/units/units.jsonl) units)" >> "$LOG"
  fi
fi

# ── Leg 5: GSPC genetic living harness (self-improving probe genome) ──
# Runs in the quiet window (after the ring, before f2) — qwen3:4b mutation.
# Evolution: mutate gap-axis probes → measure vs frozen anchors → keep discriminators.
if pgrep -f specialist_ring >/dev/null; then
  echo "$(TS) specialist_ring RUNNING — genetic harness deferred (ollama priority rule)" >> "$LOG"
elif pgrep -f gspc_genetic >/dev/null; then
  echo "$(TS) gspc_genetic RUNNING — skip (already evolving)" >> "$LOG"
else
  if [ -f /workspace/gspc_genetic.py ]; then
    echo "$(TS) genetic harness idle — running 3 cycles" >> "$LOG"
    cd /workspace && nohup python3 gspc_genetic.py --cycles 3 > genetic.log 2>&1 & disown
  else
    echo "$(TS) gspc_genetic.py missing on pod — skip" >> "$LOG"
  fi
fi

# ── Leg 5b: axis-17 Leg A — refresh published human-baseline cells (Mac-side, no DPIA) ──
# (Runs on the Mac via the driver's final pass — the harness pins public baselines)
echo "$(TS) Leg A cells present on Mac: $(ls "$HOME/clawd/csoai-static-deploy2/SOVOS/living/human_baseline_cells.jsonl" 2>/dev/null | wc -l | tr -d ' ')" >> "$LOG"

# ── Leg 6: collect live DB bundle for the Mac pull ────────────────
mkdir -p /workspace/overnight/out
cp /workspace/gold_results.json /workspace/overnight/out/ 2>/dev/null
cp /workspace/goldbank_jail.json /workspace/overnight/out/ 2>/dev/null
cp /workspace/arena-24x7/reborn_rounds.jsonl /workspace/overnight/out/ 2>/dev/null
cp /workspace/arena-24x7/reborn_league.json /workspace/overnight/out/ 2>/dev/null
cp /workspace/f2/sovereign_synth.jsonl /workspace/overnight/out/ 2>/dev/null
cp /workspace/f2/items/slot15.jsonl /workspace/overnight/out/ 2>/dev/null
cp /workspace/f2/items/human-vs-ai.jsonl /workspace/overnight/out/ 2>/dev/null
cp /workspace/SOVOS/living/probe_genome.jsonl /workspace/overnight/out/ 2>/dev/null
cp /workspace/overnight/out/axis_verdicts.json /workspace/overnight/out/ 2>/dev/null
ls /workspace/overnight/out/ > /workspace/overnight/out/manifest.txt 2>&1
echo "$(TS) out bundle: $(cat /workspace/overnight/out/manifest.txt | tr '\n' ' ')" >> "$LOG"
echo "===== overnight batch pass done $(TS) =====" >> "$LOG"
