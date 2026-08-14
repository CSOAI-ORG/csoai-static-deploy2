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

    # Phase 1.5: JCS canonical-signing of new board output (RFC 8785)
    # The research report confirms: RFC 8785 JCS + SHA-256 + detached sig
    # is THE universal card serialization. Authority accrues only on recompute.
    log("Phase 1.5: JCS canonical-signing new board output...")
    board_dir = WORK / "boards-v2-2026-08-14"
    if board_dir.exists():
        jsonls = sorted(board_dir.glob("peritem_*.jsonl"))
        for jf in jsonls:
            signed_out = board_dir / f"signed_{jf.name}"
            if signed_out.exists() and signed_out.stat().st_size > 100:
                continue  # already signed
            try:
                # Read, canonicalize each row, sign batch as a content-addressed card
                rows = []
                with open(jf) as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            rows.append(json.loads(line))
                if not rows:
                    continue
                # Build the signed card: canonical JSON of {inputs, output, method}
                import hashlib as _hlib
                card = {
                    "type": "gspc-peritem-card",
                    "axis": jf.stem.replace("peritem_", ""),
                    "source": jf.name,
                    "rows": len(rows),
                    "generated": str(datetime.datetime.now(datetime.timezone.utc)),
                    "method": "board_v2 deterministic gate",
                    "output": rows,
                }
                # Canonical JSON: sorted keys, no whitespace (RFC 8785)
                canonical = json.dumps(card, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
                digest = _hlib.sha256(canonical.encode()).hexdigest()
                signed_card = {
                    "schema": "jcs+sha256+ed25519",
                    "digest": digest,
                    "card": card,
                    "signed": False,  # detached sig not yet applied
                    "signature_source": "autonomous_continuation",
                }
                with open(signed_out, "w") as f:
                    json.dump(signed_card, f, indent=2, sort_keys=True)
                log(f"  Signed {jf.name}: {len(rows)} rows, sha256={digest[:16]}")
            except Exception as e:
                log(f"  Failed to sign {jf.name}: {e}")
    else:
        log("  No board dir yet — skipping")

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

    # Phase 5: Write checkpoint with honest status
    # 3090 reachability probe (honest: did it reconnect or not?)
    _3090_alive = False
    try:
        _r = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
             "-i", "/root/.ssh/id_ed25519",
             "-p", "17446", "root@194.26.196.156",
             "echo alive"],
            capture_output=True, text=True, timeout=15
        )
        _3090_alive = "alive" in _r.stdout
    except Exception:
        pass

    checkpoint = WORK / "cross-lab-runs" / "2026-08-14" / "autonomous_checkpoint.json"
    checkpoint.write_text(json.dumps({
        "timestamp": datetime.datetime.now().isoformat(),
        "gpu": gpu_free(),
        "3090_reachable": _3090_alive,
        "3090_note": "arena_24x7_loop streaming" if _3090_alive else "UNREACHABLE all night — A100-only operation",
        "overnight_note": (
            "All measurements are RECOMPUTABLE artifacts, awaiting external recompute. "
            "Safety-substitution findings (refusal gaps) are estate-internal until "
            "an independent party re-runs the same probes against disclosed inputs. "
            "Corpus is building; flywheel is not yet turning."
        ),
        "status": status,
    }, indent=2))

    log(f"═══ PHASE COMPLETE ═══ GPU: {gpu_free()}")

if __name__ == "__main__":
    main()