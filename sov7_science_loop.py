#!/usr/bin/env python3
"""sov7_science_loop.py — orchestrator that closes the SOV1 spine.

Cycle (single iteration):
  1. load task registry, pick suites
  2. instantiate Sov4Router (auto-loads avoid-list)
  3. run learn loop (route → worker → critic → record)
  4. refresh avoid-list in router
  5. emit a master SIGIL receipt
  6. write cycle report

Run repeatedly and the system gets sharper: avoided (suite, model) pairs
get swapped to the fallback model, kept examples grow the self-training
stream, and the master SIGIL chain records every cycle for auditability.

Usage:
  python3 sov7_science_loop.py cycle [--n 3] [--cycles 1] [--provider groq] [--sigil]
  python3 sov7_science_loop.py status
  python3 sov7_science_loop.py report
"""
import json, os, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from sov4_router import Sov4Router, emit_sigil, AVOID_FILE, DATA_DIR, HEARTBEATS_DIR, CYCLE_DIR

# CYCLE_DIR comes from sov4_router so it tracks SOV_DATA_DIR
CYCLE_DIR = Path(CYCLE_DIR)
CYCLE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SUITES = [
    "sovereign_compliance", "sovereign_defence", "sovereign_governance",
    "sovereign_redline", "sovereign_procurement",
    "mmlu_pro", "arc_challenge", "truthfulqa",
]

REGISTRY_PATH = Path(DATA_DIR) / "task_registry.json"
if not REGISTRY_PATH.exists():
    # Fall back to local benchmark-results
    REGISTRY_PATH = ROOT / "benchmark-results" / "task_registry.json"


def load_registry_suites(suite_names=None, max_per_suite=10):
    if not REGISTRY_PATH.exists():
        return {}
    reg = json.load(open(REGISTRY_PATH))
    suites = reg.get("suites", {})
    if not suite_names:
        return {k: {"tasks": v.get("tasks", [])[:max_per_suite]}
                for k, v in suites.items() if k in DEFAULT_SUITES}
    out = {}
    for s in suite_names:
        if s in suites:
            out[s] = {"tasks": suites[s].get("tasks", [])[:max_per_suite]}
    return out


def run_cycle(router, suite_names=None, max_tasks=3, max_workers=3,
              provider="groq", mock=False, do_sigil=True, refresh=True,
              pillar_aware=False):
    """Run one science cycle. Returns the cycle report dict."""
    suites = load_registry_suites(suite_names=suite_names, max_per_suite=max_tasks)
    if not suites:
        return {"ok": False, "error": "no suites to run"}

    ts = int(time.time() * 1000)
    started = time.time()
    avoid_before = {f"{s}|{m}": c for (s, m), c in router.avoid.items()}

    result = router.learn_from(
        suites, max_tasks_per_suite=max_tasks, max_workers=max_workers,
        provider=provider, mock=mock, do_sigil=do_sigil, refresh_avoid_after=refresh,
        min_overall=0.5, pillar_aware=pillar_aware,
    )

    elapsed = round(time.time() - started, 1)
    avoid_after = {f"{s}|{m}": c for (s, m), c in router.avoid.items()}

    new_avoids = {k: avoid_after[k] for k in avoid_after if k not in avoid_before}
    grown_avoids = {k: avoid_after[k] for k in avoid_after
                    if k in avoid_before and avoid_after[k] > avoid_before[k]}

    cycle = {
        "ts": ts,
        "iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "suites": list(suites.keys()),
        "max_tasks_per_suite": max_tasks,
        "provider": provider,
        "mock": mock,
        "elapsed_s": elapsed,
        "result": result,
        "router_stats": router.stats,
        "avoid_before": avoid_before,
        "avoid_after": avoid_after,
        "new_avoids": new_avoids,
        "grown_avoids": grown_avoids,
    }

    if do_sigil:
        path = emit_sigil("sov7.cycle", cycle, care_score=_cycle_care(result))
        cycle["sigil"] = path

    out_path = CYCLE_DIR / f"cycle_{ts}.json"
    with open(out_path, "w") as f:
        json.dump(cycle, f, indent=2)
    cycle["report"] = str(out_path)

    # Auto-sync to RunPod if SOV_SYNC_TO_RUNPOD=1
    if os.environ.get("SOV_SYNC_TO_RUNPOD") == "1":
        try:
            import subprocess
            from pathlib import Path as _P
            # Tar the new data + sync to pod
            root = _P(__file__).resolve().parent
            for rel in ["sov5_self_training.jsonl", "sov5_self_training.avoid.jsonl"]:
                src = _P(DATA_DIR) / rel
                if src.exists():
                    subprocess.run([
                        "scp", "-P", "22087",
                        "-o", "StrictHostKeyChecking=accept-new", "-o", "BatchMode=yes",
                        str(src), f"root@69.30.85.23:/workspace/sov-sov7/{rel}"
                    ], check=False, capture_output=True)
            subprocess.run([
                "scp", "-P", "22087",
                "-o", "StrictHostKeyChecking=accept-new", "-o", "BatchMode=yes",
                str(out_path), f"root@69.30.85.23:/workspace/sov-sov7/cycles/{out_path.name}"
            ], check=False, capture_output=True)
            print(f"  [sync] pushed to sov33-top-bench-2:/workspace/sov-sov7/")
        except Exception as e:
            print(f"  [sync] failed: {e}")

    return cycle


def _cycle_care(result):
    """Compute a single care score for the cycle (mean overall where available)."""
    suites = result.get("suites", {}) or {}
    scores = []
    for s, v in suites.items():
        if isinstance(v, dict) and v.get("kept", 0) > 0:
            scores.append(0.7)  # we don't have per-task overalls in the summary
    if not scores:
        return 0.5
    return round(sum(scores) / len(scores), 3)


def run_cycles(n_cycles=1, do_sigil=True, pillar_aware=False, **kwargs):
    """Run N cycles. Each cycle uses a fresh router so the avoid-list
    is re-read from disk (true accumulation)."""
    cycles = []
    for i in range(n_cycles):
        router = Sov4Router()  # reloads avoid-file
        c = run_cycle(router, do_sigil=do_sigil, pillar_aware=pillar_aware, **kwargs)
        cycles.append(c)
        if c.get("ok") is False:
            print(f"  cycle {i+1}/{n_cycles}: ERROR {c.get('error')}")
        else:
            pa = "PA" if pillar_aware else "  "
            print(f"  cycle {i+1}/{n_cycles}: {pa} "
                  f"kept={c['result']['kept']} avoided={c['result']['avoided']} "
                  f"err={c['result']['errors']} swaps={c['result'].get('swaps', 0)} "
                  f"elapsed={c['elapsed_s']}s")
    return cycles


def report_status():
    """Snapshot of current state: avoid-list, kept stream, sigil count."""
    kept = Path(DATA_DIR) / "sov5_self_training.jsonl"
    avoid = Path(DATA_DIR) / "sov5_self_training.avoid.jsonl"
    sigils = list(Path(HEARTBEATS_DIR).glob("*.sigil.json"))
    cycles = sorted(CYCLE_DIR.glob("cycle_*.json"))
    print("=== SOV7 SCIENCE LOOP STATUS ===")
    print(f"  kept stream:    {kept} ({kept.stat().st_size if kept.exists() else 0} bytes)")
    if kept.exists():
        n_kept = sum(1 for _ in open(kept))
        print(f"    -> {n_kept} examples")
    print(f"  avoid stream:   {avoid} ({avoid.stat().st_size if avoid.exists() else 0} bytes)")
    if avoid.exists():
        n_avoid = sum(1 for _ in open(avoid))
        print(f"    -> {n_avoid} down-weight entries")
    print(f"  sigil receipts: {len(sigils)} in heartbeats/")
    print(f"  cycle reports:  {len(cycles)} in {CYCLE_DIR}")
    if cycles:
        latest = cycles[-1]
        d = json.load(open(latest))
        print(f"  latest cycle:   {d.get('iso')} "
              f"(kept={d['result']['kept']} avoided={d['result']['avoided']})")
    # Show top avoid keys
    if avoid.exists():
        from collections import Counter
        keys = []
        for line in open(avoid):
            try:
                d = json.loads(line)
                keys.append((d.get("suite", ""), d.get("model", "")))
            except Exception:
                pass
        c = Counter(keys).most_common(8)
        if c:
            print("  top avoid (suite, model) -> count:")
            for (s, m), n in c:
                over = " [SWAPPED]" if n >= 3 else ""
                print(f"    {s:25s} {m:22s} -> {n}{over}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "cycle":
        n_cycles = 1
        max_tasks = 3
        mock = "--mock" in sys.argv
        provider = "groq"
        do_sigil = "--no-sigil" not in sys.argv
        pillar_aware = "--pillar-aware" in sys.argv
        if "--cycles" in sys.argv:
            i = sys.argv.index("--cycles")
            n_cycles = int(sys.argv[i + 1])
        if "--n" in sys.argv:
            i = sys.argv.index("--n")
            max_tasks = int(sys.argv[i + 1])
        if "--provider" in sys.argv:
            i = sys.argv.index("--provider")
            provider = sys.argv[i + 1]
        print(f"=== SOV7 SCIENCE LOOP: {n_cycles} cycle(s), "
              f"max_tasks={max_tasks}, provider={provider}, mock={mock}, "
              f"sigil={do_sigil}, pillar_aware={pillar_aware} ===")
        run_cycles(n_cycles=n_cycles, max_tasks=max_tasks, max_workers=3,
                   provider=provider, mock=mock, do_sigil=do_sigil,
                   pillar_aware=pillar_aware)
    elif cmd == "status":
        report_status()
    elif cmd == "report":
        cycles = sorted(CYCLE_DIR.glob("cycle_*.json"))
        if not cycles:
            print("  no cycles yet — run: python3 sov7_science_loop.py cycle")
            return
        for p in cycles[-5:]:
            d = json.load(open(p))
            print(f"  {d['iso']}  kept={d['result']['kept']:>2} "
                  f"av={d['result']['avoided']:>2} err={d['result']['errors']:>2} "
                  f"swaps={d['result'].get('swaps', 0):>2} "
                  f"avoid+={len(d.get('new_avoids', {}))} "
                  f"elapsed={d['elapsed_s']}s")
    else:
        print(f"unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
