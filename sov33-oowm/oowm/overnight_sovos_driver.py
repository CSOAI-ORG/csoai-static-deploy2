#!/usr/bin/env python3
"""overnight_sovos_driver.py — autonomous overnight run on the 3090 pod (2026-08-17 JEEVES).

Runs the SOVOS/OOWM work stack continuously from launch until 04:00 UTC,
entirely on the pod volume (/workspace). Mac is NOT required after deploy.

Cycles (each loop tick, ~5 min):
  1. Estate-mine → OOWM knowledge graph re-ingest (fresh from /workspace volume mirror)
  2. Grok referee round (measure-only vs x-ai/grok-4.6 via OpenRouter) — via keeper
  3. Arena round (existing arena_loop_keeper) — verify alive, restart if dead
  4. A100 wire probe (a100_oowm_wire.sh) — verify armed, re-arm if exhausted
  5. Snapshot state to /workspace/arena-24x7/overnight_state.json (volume-persistent)

At 04:00 UTC: write overnight_summary.md + final snapshot, then exit 0.
All artifacts land on /workspace (the pod's persistent volume) — nothing on Mac.

Run:  nohup setsid python3 /workspace/sov33-oowm/oowm/overnight_sovos_driver.py \
          > /workspace/arena-24x7/overnight_driver.log 2>&1 < /dev/null &
"""
import json, os, subprocess, sys, time, traceback
from datetime import datetime, timezone
from pathlib import Path

VOL = Path("/workspace")
ARENA = VOL / "arena-24x7"
SOVOS = VOL / "sov33-oowm" / "oowm"
STATE = ARENA / "overnight_state.json"
SUMMARY = ARENA / "overnight_summary.md"
TARGET_HOUR = 4   # stop at 04:00 UTC
TICK_S = 300      # 5 min per tick

PY = "python3"
INGEST = [PY, "-m", "oowm.estate_mine_ingest", "--cap", "8000"]
REFEREE_KEEPER = [PY, "/workspace/sov33-oowm/oowm/grok_referee_keeper.py"]
ARENA_KEEPER = [PY, "/workspace/arena-24x7/arena_loop_keeper.py"]
A100_WIRE = ["bash", "/workspace/a100_oowm_wire.sh"]


def now():
    return datetime.now(timezone.utc)


def log(msg):
    ts = now().strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with (ARENA / "overnight_driver.log").open("a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def proc_alive(pattern):
    try:
        out = subprocess.run(["pgrep", "-f", pattern], capture_output=True, text=True, timeout=10)
        return out.returncode == 0 and out.stdout.strip()
    except Exception:
        return False


def ensure_running(cmd, pattern, logpath):
    if proc_alive(pattern):
        return "already-running"
    try:
        with (logpath).open("a") as lf:
            subprocess.Popen(cmd, stdout=lf, stderr=lf, start_new_session=True)
        time.sleep(2)
        return "started" if proc_alive(pattern) else "start-failed"
    except Exception:
        return "error"


def run_ingest():
    try:
        r = subprocess.run(INGEST, cwd=str(SOVOS.parent), capture_output=True, text=True, timeout=300)
        tail = [ln for ln in r.stdout.strip().splitlines() if ln.strip().startswith(('"', "'"))]
        stats = r.stdout.strip().splitlines()
        return {"rc": r.returncode, "added": [s for s in stats if '"added"' in s][0].strip() if any('"added"' in s for s in stats) else "?", "tail": stats[-1] if stats else ""}
    except Exception as e:
        return {"rc": -1, "error": str(e)}


def main():
    ARENA.mkdir(parents=True, exist_ok=True)
    # Stop at the NEXT 04:00 UTC (tomorrow morning if we're past 04:00 now)
    start = now()
    target = start.replace(hour=TARGET_HOUR, minute=0, second=0, microsecond=0)
    if start >= target:
        # past 04:00 today → roll to tomorrow
        from datetime import timedelta
        target = target + timedelta(days=1)
    log("=== OVERNIGHT SOVOS DRIVER START ===")
    log(f"target stop: {target.isoformat()} | tick: {TICK_S}s | volume: {VOL}")

    tick = 0
    while True:
        tick += 1
        t = now()
        if t >= target:
            log(f"target reached ({target.isoformat()}) — finishing")
            break

        log(f"--- TICK {tick} @ {t.strftime('%H:%M:%S')}Z ---")

        # 1. estate mine re-ingest (fresh from volume)
        ing = run_ingest()
        log(f"ingest: rc={ing.get('rc')} {ing.get('added','')}")

        # 2. grok referee keeper
        st = ensure_running(REFEREE_KEEPER, "grok_referee_keeper.py",
                            ARENA / "grok_referee_keeper.log")
        log(f"grok referee keeper: {st}")

        # 3. arena keeper
        st = ensure_running(ARENA_KEEPER, "arena_loop_keeper.py",
                            ARENA / "keeper.log")
        log(f"arena keeper: {st}")

        # 4. A100 wire (re-arm if exhausted/absent)
        st = ensure_running(A100_WIRE, "a100_oowm_wire.sh",
                            ARENA / "a100_oowm_wire.log")
        log(f"A100 wire: {st}")

        # 5. state snapshot (volume)
        snap = {
            "tick": tick, "ts": now().isoformat(), "target": target.isoformat(),
            "ingest": ing, "grok_referee": st, "arena": st, "a100_wire": st,
            "volume": str(VOL),
        }
        try:
            rounds_f = ARENA / "grok_referee_rounds.jsonl"
            snap["grok_referee_rounds"] = sum(1 for _ in rounds_f.open()) if rounds_f.exists() else 0
            arena_r = ARENA / "reborn_rounds.jsonl"
            snap["arena_rounds"] = sum(1 for _ in arena_r.open()) if arena_r.exists() else 0
        except Exception:
            pass
        STATE.write_text(json.dumps(snap, indent=2))
        log(f"state snapshot -> {STATE}")

        time.sleep(TICK_S)

    # final summary
    summary = []
    summary.append("# OVERNIGHT SOVOS RUN — SUMMARY")
    summary.append(f"**Finished:** {now().isoformat()} (target {target.isoformat()})")
    summary.append(f"**Ticks:** {tick}")
    try:
        rf = ARENA / "grok_referee_rounds.jsonl"
        n = sum(1 for _ in rf.open()) if rf.exists() else 0
        summary.append(f"**Grok referee rounds logged:** {n} (volume: {rf})")
        lf = ARENA / "grok_referee_league.json"
        if lf.exists():
            league = json.loads(lf.read_text())
            top = sorted(league.items(), key=lambda x: x[1]["elo"], reverse=True)[:5]
            summary.append("**Top 5 (Grok referee league):**")
            for m, s in top:
                summary.append(f"  - {m}: {s['elo']:.1f} ({s['games']}g)")
    except Exception as e:
        summary.append(f"league read error: {e}")
    summary.append(f"**State snapshot:** {STATE}")
    SUMMARY.write_text("\n".join(summary) + "\n")
    log(f"summary written -> {SUMMARY}")
    log("=== OVERNIGHT SOVOS DRIVER COMPLETE ===")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        log("DRIVER CRASHED — see traceback above")
