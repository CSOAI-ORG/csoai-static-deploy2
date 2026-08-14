#!/usr/bin/env python3
"""Autonomous overnight continuation — Phase 2: process queue results, publish, keep going.

Runs after the overnight_queue completes. Checks for output artifacts,
generates the publish-delta note if the spray gate passes, runs the G4
claim-linter, and prepares the next day's queue.

Doctrine: the free artifact is the ad; every card is marketing.
           never burn $1.19/hr on idle A100.
"""
import json, os, subprocess, sys, datetime, pathlib

WORK = pathlib.Path("/workspace/jeeves-exec/SOVOS")
LOG = WORK / "logs" / f"autonomous-{datetime.date.today().isoformat()}.log"

def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG.parent.mkdir(exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def gpu_free():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.free",
             "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10
        )
        return out.stdout.strip()
    except Exception as e:
        return f"N/A ({e})"

def check_overnight_done():
    """Check if the overnight queue left artifacts."""
    board_dir = WORK / "boards-v2-2026-08-14"
    city_dir = WORK / "cross-lab-runs" / "2026-08-14"
    results = {}
    if board_dir.exists():
        jsonls = list(board_dir.glob("peritem_*.jsonl"))
        results["board_jsonls"] = len(jsonls)
        results["board_total_bytes"] = sum(f.stat().st_size for f in jsonls)
    if city_dir.exists():
        files = list(city_dir.glob("*"))
        results["city_files"] = len(files)
        results["city_runs"] = [f.name for f in files if "daily" not in f.name]
    # Check the spray gate: does the city have publishable=true?
    board_v2_file = board_dir / "board.json"
    if board_v2_file.exists():
        board = json.loads(board_v2_file.read_text())
        results["publishable"] = board.get("publishable", "unknown")
        results["blocked_n"] = board.get("blocked", {}).get("n", "unknown")
    return results

def main():
    log(f"═══ AUTONOMOUS CONTINUATION: {datetime.datetime.now().isoformat()} ═══")
    log(f"GPU: {gpu_free()}")

    # Phase 1: Check overnight results
    status = check_overnight_done()
    log(f"Overnight status: {json.dumps(status, default=str)}")

    if status.get("board_jsonls", 0) >= 13:
        log(f"Board complete: {status['board_jsonls']} axes, {status['board_total_bytes']} bytes")
    else:
        log(f"Board incomplete ({status.get('board_jsonls', 0)}/13 axes) — may still be running")

    # Phase 2: Run G4 claim-linter on all new output
    log("Running G4 claim-linter...")
    try:
        r = subprocess.run(
            [sys.executable, str(WORK / "agents" / "claim_linter.py"),
             str(WORK), "--ignore-patterns", "node_modules,.git,__pycache__,logs"],
            capture_output=True, text=True, timeout=120
        )
        if "PASS" in r.stdout or "0 violations" in r.stdout:
            log(f"G4 PASS: {r.stdout.strip()[-200:]}")
        else:
            log(f"G4 ISSUES: {r.stdout.strip()[-300:]}")
    except Exception as e:
        log(f"G4 error: {e}")

    # Phase 3: Check if queue is still running — if so, leave it alone
    ps = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
    if "overnight_queue" in ps.stdout:
        log("Overnight queue still running — will check again next cycle")
    else:
        log("Overnight queue finished — starting next phase")
        # Re-launch for the next cycle
        subprocess.Popen(
            ["bash", str(WORK / "agents" / "overnight_queue_2026-08-14.sh")],
            cwd=str(WORK)
        )

    # Phase 4: Try Oracle mesh activation (if oci CLI available)
    log("Phase 4: Oracle mesh activation...")
    oracle_script = WORK / "agents" / "oracle-mesh-activate.sh"
    if oracle_script.exists():
        try:
            r = subprocess.run(
                ["bash", str(oracle_script)],
                capture_output=True, text=True, timeout=60
            )
            if "Oracle micro found" in r.stdout:
                log(f"Oracle mesh activate SUCCESS: {r.stdout.strip()[-200:]}")
            else:
                log(f"Oracle mesh: no micros reachable this cycle — will retry")
        except Exception as e:
            log(f"Oracle mesh activation error: {e}")
    else:
        log("Oracle script not on pod — skipping")

    # Phase 5: Write checkpoint
    checkpoint = WORK / "cross-lab-runs" / "2026-08-14" / "autonomous_checkpoint.json"
    checkpoint.write_text(json.dumps({
        "timestamp": datetime.datetime.now().isoformat(),
        "gpu": gpu_free(),
        "status": status,
    }, indent=2))

    log(f"═══ PHASE COMPLETE ═══ GPU: {gpu_free()}")

if __name__ == "__main__":
    main()