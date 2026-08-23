#!/usr/bin/env python3
"""
Master Batch Runner — Runs ALL work continuously
Cycles: EAT → GovBench → ASI Evolution → Stigmergy → Distributed → Deploy → Report

Usage:
  python3 master_batch.py                  # Run infinite cycles
  python3 master_batch.py --cycles 10      # Run 10 cycles
  python3 master_batch.py --phase eat      # Run only EAT phase
  python3 master_batch.py --parallel       # Run independent phases in parallel
  python3 master_batch.py --dry-run        # Show phases without executing
"""
import json
import subprocess
import sys
import os
import time
import hashlib
import argparse
import threading
import traceback
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent
BATCH_DIR = ROOT / "batch_results"
BATCH_DIR.mkdir(exist_ok=True)
LOG_FILE = ROOT / "master_batch.log"

ALL_PHASES = ["eat", "govbench", "asi_evolution", "stigmergy", "distributed", "deploy", "report"]

# Phase execution groups — phases in the same group can run in parallel
PARALLEL_GROUPS = [
    ["eat", "govbench"],           # Independent benchmarks
    ["asi_evolution"],              # Needs clean model state
    ["stigmergy", "distributed"],  # Independent evolution tracks
    ["deploy"],                     # Must happen after all evolution
    ["report"],                     # Reads all results
]


def log(msg, also_print=True):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    if also_print:
        print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def run_cmd(cmd, timeout=600, cwd=None):
    """Run a shell command, return (success, stdout+stderr, duration_sec)."""
    start = time.monotonic()
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=cwd or str(ROOT)
        )
        elapsed = time.monotonic() - start
        return r.returncode == 0, (r.stdout + r.stderr).strip(), elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        return False, f"TIMEOUT after {timeout}s", elapsed
    except Exception as e:
        elapsed = time.monotonic() - start
        return False, f"ERROR: {e}", elapsed


def sigil(data):
    """Generate a deterministic hash for any result dict."""
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()[:16]


# ─── Phase Runners ───────────────────────────────────────────────────────────

def phase_eat(cycle_num):
    """Phase 1: Run overnight_eat.py benchmarks."""
    log("  [EAT] Running overnight benchmarks...")
    ok, out, dur = run_cmd("python3 benchmark-results/overnight_eat.py --all", timeout=600)
    result = {
        "phase": "eat",
        "success": ok,
        "duration_sec": round(dur, 1),
        "output_tail": out[-2000:] if out else "",
    }
    # Try to parse JSON from output
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                result["benchmarks"] = json.loads(line)
            except json.JSONDecodeError:
                pass
    log(f"  [EAT] {'PASS' if ok else 'FAIL'} ({dur:.1f}s)")
    return result


def phase_govbench(cycle_num):
    """Phase 2: Run govbench_eval.py on all models."""
    log("  [GovBench] Running governance benchmarks...")
    ok, out, dur = run_cmd("python3 govbench_eval.py --all", timeout=900)
    result = {
        "phase": "govbench",
        "success": ok,
        "duration_sec": round(dur, 1),
        "output_tail": out[-2000:] if out else "",
    }
    # Try to parse summary from output
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                result["govbench"] = json.loads(line)
            except json.JSONDecodeError:
                pass
    log(f"  [GovBench] {'PASS' if ok else 'FAIL'} ({dur:.1f}s)")
    return result


def phase_asi_evolution(cycle_num):
    """Phase 3: Run one cycle of asi_evolution.py."""
    log("  [ASI Evolution] Running evolution cycle...")
    ok, out, dur = run_cmd("python3 asi_evolution.py", timeout=1200)
    result = {
        "phase": "asi_evolution",
        "success": ok,
        "duration_sec": round(dur, 1),
        "output_tail": out[-2000:] if out else "",
    }
    # Try to find the JSON result in output
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                result["evolution"] = json.loads(line)
            except json.JSONDecodeError:
                pass
    log(f"  [ASI Evolution] {'PASS' if ok else 'FAIL'} ({dur:.1f}s)")
    return result


def phase_stigmergy(cycle_num):
    """Phase 4: Run stigmergy cycle."""
    log("  [Stigmergy] Running stigmergy cycle...")
    ok, out, dur = run_cmd("python3 stigmergy/stigmergy.py", timeout=120)
    result = {
        "phase": "stigmergy",
        "success": ok,
        "duration_sec": round(dur, 1),
        "output_tail": out[-1000:] if out else "",
    }
    # Load state if available
    state_file = ROOT / "stigmergy" / "stigmergy_state.json"
    if state_file.exists():
        try:
            result["stigmergy_state"] = json.loads(state_file.read_text())
        except Exception:
            pass
    log(f"  [Stigmergy] {'PASS' if ok else 'FAIL'} ({dur:.1f}s)")
    return result


def phase_distributed(cycle_num):
    """Phase 5: Run distributed_evolution.py sync."""
    log("  [Distributed] Syncing distributed evolution...")
    ok, out, dur = run_cmd(
        "python3 free_gpu/distributed_evolution.py sync", timeout=300
    )
    result = {
        "phase": "distributed",
        "success": ok,
        "duration_sec": round(dur, 1),
        "output_tail": out[-2000:] if out else "",
    }
    log(f"  [Distributed] {'PASS' if ok else 'FAIL'} ({dur:.1f}s)")
    return result


def phase_deploy(cycle_num):
    """Phase 6: Deploy to Cloudflare Pages."""
    log("  [Deploy] Deploying to Cloudflare Pages...")
    ok, out, dur = run_cmd("bash deploy-cloudflare.sh", timeout=300)
    result = {
        "phase": "deploy",
        "success": ok,
        "duration_sec": round(dur, 1),
        "output_tail": out[-2000:] if out else "",
    }
    log(f"  [Deploy] {'PASS' if ok else 'FAIL'} ({dur:.1f}s)")
    return result


def phase_report(cycle_num, phase_results):
    """Phase 7: Generate summary report for this cycle."""
    log("  [Report] Generating cycle report...")
    successes = sum(1 for r in phase_results if r.get("success"))
    failures = len(phase_results) - successes
    total_dur = sum(r.get("duration_sec", 0) for r in phase_results)

    report = {
        "cycle": cycle_num,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phases_run": len(phase_results),
        "successes": successes,
        "failures": failures,
        "total_duration_sec": round(total_dur, 1),
        "sigil": sigil(phase_results),
        "phases": phase_results,
    }

    # Check for EAT score improvement
    for r in phase_results:
        if r.get("phase") == "eat" and "benchmarks" in r:
            report["eat_score"] = r["benchmarks"]
        if r.get("phase") == "govbench" and "govbench" in r:
            report["govbench_score"] = r["govbench"]

    log(f"  [Report] {successes}/{len(phase_results)} phases passed ({total_dur:.1f}s total)")
    return report


# ─── Phase Dispatcher ────────────────────────────────────────────────────────

PHASE_MAP = {
    "eat": phase_eat,
    "govbench": phase_govbench,
    "asi_evolution": phase_asi_evolution,
    "stigmergy": phase_stigmergy,
    "distributed": phase_distributed,
    "deploy": phase_deploy,
}


def run_phase(phase_name, cycle_num):
    """Run a single phase and return its result dict."""
    runner = PHASE_MAP.get(phase_name)
    if not runner:
        return {"phase": phase_name, "success": False, "error": "unknown phase"}
    return runner(cycle_num)


def run_cycle_sequential(cycle_num, phases):
    """Run all phases sequentially."""
    log(f"─── CYCLE {cycle_num} (sequential) ───")
    phase_results = []
    for phase_name in phases:
        try:
            result = run_phase(phase_name, cycle_num)
        except Exception as e:
            result = {
                "phase": phase_name,
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
        phase_results.append(result)

    # Report phase always runs last
    report = phase_report(cycle_num, phase_results)
    return report


def run_cycle_parallel(cycle_num, phases):
    """Run phases in parallel groups."""
    log(f"─── CYCLE {cycle_num} (parallel) ───")
    phase_results = []
    phase_set = set(phases)

    for group in PARALLEL_GROUPS:
        group_phases = [p for p in group if p in phase_set]
        if not group_phases:
            continue

        if len(group_phases) == 1:
            # Single phase — run directly
            try:
                result = run_phase(group_phases[0], cycle_num)
            except Exception as e:
                result = {
                    "phase": group_phases[0],
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            phase_results.append(result)
        else:
            # Multiple phases — run in parallel
            log(f"  Parallel group: {', '.join(group_phases)}")
            with ThreadPoolExecutor(max_workers=len(group_phases)) as pool:
                futures = {
                    pool.submit(run_phase, p, cycle_num): p
                    for p in group_phases
                }
                for future in as_completed(futures):
                    phase_name = futures[future]
                    try:
                        result = future.result()
                    except Exception as e:
                        result = {
                            "phase": phase_name,
                            "success": False,
                            "error": str(e),
                            "traceback": traceback.format_exc(),
                        }
                    phase_results.append(result)

    report = phase_report(cycle_num, phase_results)
    return report


# ─── Main Loop ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Master Batch Runner — Runs ALL work continuously"
    )
    parser.add_argument(
        "--cycles", type=int, default=0,
        help="Number of cycles to run (0 = infinite)"
    )
    parser.add_argument(
        "--phase", type=str, default=None,
        choices=ALL_PHASES,
        help="Run only one specific phase"
    )
    parser.add_argument(
        "--parallel", action="store_true",
        help="Run independent phases in parallel"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show phases without executing"
    )
    parser.add_argument(
        "--delay", type=int, default=0,
        help="Seconds to sleep between cycles"
    )
    args = parser.parse_args()

    phases = [args.phase] if args.phase else ALL_PHASES[:-1]  # exclude 'report' — it's auto

    log("=" * 70)
    log("  MASTER BATCH RUNNER — STARTING")
    log("=" * 70)
    log(f"  Cycles:     {'infinite' if args.cycles == 0 else args.cycles}")
    log(f"  Phases:     {', '.join(phases)}")
    log(f"  Mode:       {'parallel' if args.parallel else 'sequential'}")
    log(f"  Delay:      {args.delay}s between cycles")
    log(f"  PID:        {os.getpid()}")
    log("=" * 70)

    if args.dry_run:
        log("\n[DRY RUN] Would execute phases:")
        for i, p in enumerate(phases, 1):
            log(f"  {i}. {p}")
        return

    cycle_num = 0
    all_reports = []

    try:
        while True:
            cycle_num += 1
            if args.cycles > 0 and cycle_num > args.cycles:
                break

            log(f"\n{'=' * 70}")
            log(f"  CYCLE {cycle_num} START")
            log(f"{'=' * 70}")

            cycle_start = time.monotonic()

            if args.parallel:
                report = run_cycle_parallel(cycle_num, phases)
            else:
                report = run_cycle_sequential(cycle_num, phases)

            cycle_elapsed = time.monotonic() - cycle_start
            report["wall_clock_sec"] = round(cycle_elapsed, 1)

            # Save cycle report
            cycle_file = BATCH_DIR / f"cycle_{cycle_num}.json"
            cycle_file.write_text(json.dumps(report, indent=2, default=str))
            log(f"  Saved: {cycle_file}")

            all_reports.append(report)

            # Update rolling summary
            summary = {
                "last_update": datetime.now(timezone.utc).isoformat(),
                "total_cycles": cycle_num,
                "total_successes": sum(r["successes"] for r in all_reports),
                "total_failures": sum(r["failures"] for r in all_reports),
                "total_wall_clock_sec": round(sum(r["wall_clock_sec"] for r in all_reports), 1),
                "cycles": [
                    {
                        "cycle": r["cycle"],
                        "successes": r["successes"],
                        "failures": r["failures"],
                        "duration": r["wall_clock_sec"],
                        "sigil": r["sigil"],
                    }
                    for r in all_reports
                ],
            }
            summary_file = BATCH_DIR / "summary.json"
            summary_file.write_text(json.dumps(summary, indent=2))

            log(f"\n  CYCLE {cycle_num} COMPLETE — "
                f"{report['successes']}/{report['phases_run']} passed "
                f"({cycle_elapsed:.1f}s)")

            if args.delay > 0:
                log(f"  Sleeping {args.delay}s before next cycle...")
                time.sleep(args.delay)

    except KeyboardInterrupt:
        log("\n  INTERRUPTED — saving final state...")
    except Exception as e:
        log(f"\n  FATAL ERROR: {e}")
        log(traceback.format_exc())

    # Final summary
    log(f"\n{'=' * 70}")
    log(f"  MASTER BATCH COMPLETE")
    log(f"{'=' * 70}")
    log(f"  Cycles completed: {len(all_reports)}")
    if all_reports:
        total_ok = sum(r["successes"] for r in all_reports)
        total_fail = sum(r["failures"] for r in all_reports)
        total_phases = total_ok + total_fail
        log(f"  Phases passed:    {total_ok}/{total_phases}")
        log(f"  Total runtime:    {sum(r['wall_clock_sec'] for r in all_reports):.0f}s")
    log(f"  Results dir:      {BATCH_DIR}")
    log(f"  Log file:         {LOG_FILE}")
    log("=" * 70)


if __name__ == "__main__":
    main()
