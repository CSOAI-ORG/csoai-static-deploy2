#!/usr/bin/env python3
import json, time, hashlib, sys, subprocess, os
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent.parent
BENCH = BASE / "benchmark-results"
SOVSPACE_TRACKER = BENCH / "sov4_sovspace_tracker.py"
BENCH_RUNNER = BENCH / "run_ollama_benchmark.py"
TRAIN_SCRIPT = BENCH / "train_sovereign_adapter.py"
CRON_NIGHTLY = BENCH / "cron-nightly.sh"
LOG = BENCH / "fluid-heartbeat.log"
HEARTBEAT_DIR = BASE / "heartbeats"
SOVEREIGN_DIR = Path.home() / ".sovereign"
MEMORY_PATH = SOVEREIGN_DIR / "sovereign_memory.jsonl"

SOVSPACE_CONCEPTS = [
    "care_floor", "care_score_current", "sigil_position",
    "sigil_prev_hash", "bft_quorum", "bft_approvals",
    "article_0", "invariants", "owem_route", "backend_chain",
    "anti_pattern_check", "fluid_phase", "lineage_rho",
    "j_space_activity", "last_heartbeat", "heartbeat_count",
]

def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def run_py(script, *args, timeout=120):
    cmd = [sys.executable, str(script)] + list(args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"ok": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr[:500]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": f"TIMEOUT ({timeout}s)"}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}

def run_sh(cmd, timeout=120):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"ok": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr[:500]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": f"TIMEOUT ({timeout}s)"}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}

def read_docstore():
    memory = {"memory_exists": False, "memory_count": 0, "entries": []}
    if MEMORY_PATH.exists():
        lines = [l for l in MEMORY_PATH.read_text().strip().split("\n") if l.strip()]
        memory["memory_exists"] = True
        memory["memory_count"] = len(lines)
        memory["entries"] = lines[-10:] if lines else []
    governance_csv = BASE / "_alignment/sov3_governance_episodes.csv"
    governance_count = 0
    if governance_csv.exists():
        governance_count = len(governance_csv.read_text().strip().split("\n")) - 1
    sov_town_dir = SOVEREIGN_DIR / "sov_town"
    sov_town_simulations = 0
    sov_town_last = None
    if sov_town_dir.exists():
        sims = list(sov_town_dir.glob("simulation_*.json"))
        sov_town_simulations = len(sims)
        if sims:
            latest = max(sims, key=lambda p: p.stat().st_mtime)
            try:
                sov_town_last = json.loads(latest.read_text()).get("timestamp", str(datetime.fromtimestamp(latest.stat().st_mtime)))
            except:
                sov_town_last = str(datetime.fromtimestamp(latest.stat().st_mtime))
    return {
        "memory": memory,
        "governance_count": governance_count,
        "sov_town": {"simulations": sov_town_simulations, "last_run": sov_town_last},
    }

def check_sovspace():
    r = run_py(SOVSPACE_TRACKER, "status")
    if r["ok"]:
        try:
            return json.loads(r["stdout"])
        except: pass
    return {"error": "sovspace not available"}

def compute_delta(state):
    if not state or "error" in state:
        return {"needs_training": False, "reason": "no state available"}
    count = state.get("heartbeat_count", 0)
    care = state.get("care_score_current", 0)
    invariants_ok = all(state.get(f"invariant_{i}", False) for i in range(1, 7))
    sigil_pos = state.get("sigil_position", 0)
    now = time.time()
    last_hb = state.get("last_heartbeat")
    hours_since = 999
    if last_hb:
        try:
            hours_since = (now - datetime.fromisoformat(last_hb).timestamp()) / 3600
        except: pass
    needs_training = False
    reasons = []
    if not invariants_ok:
        reasons.append("invariants failing")
    if hours_since > 12:
        reasons.append(f"{hours_since:.1f}h since last heartbeat")
    if len(reasons) >= 2:
        needs_training = True
    return {
        "needs_training": needs_training,
        "reason": "; ".join(reasons) if reasons else "stable",
        "heartbeat_count": count,
        "hours_since_last": round(hours_since, 1),
        "sigil_position": sigil_pos,
        "care_score": care,
        "invariants_ok": invariants_ok,
    }

def train_if_needed(delta):
    if not delta.get("needs_training"):
        return {"trained": False, "reason": "no delta trigger"}
    log(f"Delta trigger: {delta['reason']}. Running adapter training...")
    r = run_py(TRAIN_SCRIPT, "--specs", "master", "general_ability", timeout=300)
    if r["ok"]:
        log("Training OK")
        return {"trained": True, "models": ["sov33-master-v2", "sov4-general-ability"]}
    else:
        log(f"Training FAILED: {r['stderr'][:200]}")
        return {"trained": False, "error": r["stderr"][:200]}

def run_benchmarks(force=False):
    if not force:
        last_bench = None
        for f in sorted(BENCH.glob("benchmark_registry_*.json")):
            last_bench = f
        if last_bench:
            age = time.time() - last_bench.stat().st_mtime
            if age < 3600:
                log(f"Skipping bench (last run {age/60:.0f}m ago)")
                return {"skipped": True, "age_m": age/60}
    log("Running benchmarks...")
    r = run_py(BENCH_RUNNER, timeout=600)
    if r["ok"]:
        log("Benchmarks OK")
        latest = None
        for f in sorted(BENCH.glob("benchmark_registry_*.json")):
            latest = f
        if latest:
            data = json.loads(latest.read_text())
            return {"benchmarked": True, "path": str(latest), "results": data.get("models", {})}
        return {"benchmarked": True}
    else:
        log(f"Benchmarks FAILED: {r['stderr'][:200]}")
        return {"benchmarked": False, "error": r["stderr"][:200]}

def sigil_sign(heartbeat_data):
    payload = json.dumps(heartbeat_data, sort_keys=True).encode()
    digest = hashlib.sha256(payload).hexdigest()
    HEARTBEAT_DIR.mkdir(parents=True, exist_ok=True)
    hb_num = heartbeat_data.get("heartbeat_count", 0)
    path = HEARTBEAT_DIR / f"hb_{hb_num:04d}.json"
    record = {
        "type": "fluid_heartbeat",
        "heartbeat": hb_num,
        "timestamp": heartbeat_data.get("timestamp"),
        "sha256": digest,
        "data": heartbeat_data,
    }
    path.write_text(json.dumps(record, indent=2) + "\n")
    return {"path": str(path), "sha256": digest}

def deploy():
    log("Deploying to Vercel...")
    r = run_sh("vercel deploy --prod --yes", timeout=120)
    if r["ok"]:
        log("Deploy OK")
        return {"deployed": True}
    log(f"Deploy FAILED: {r['stderr'][:200]}")
    return {"deployed": False, "error": r["stderr"][:200]}

def main():
    log("=== SOV4 FLUID HEARTBEAT ===")
    ts = datetime.now(timezone.utc).isoformat()
    tracker_result = run_py(SOVSPACE_TRACKER, "heartbeat")
    if tracker_result["ok"]:
        try:
            heartbeat_state = json.loads(tracker_result["stdout"])
        except:
            heartbeat_state = {"heartbeat": 0, "error": "parse failed"}
    else:
        heartbeat_state = {"heartbeat": 0, "error": tracker_result.get("stderr", "")[:100]}

    step_log = lambda n, ok, msg: log(f"  {n}: {'OK' if ok else 'FAIL'} {msg}")

    log("Step 1: Read docstore...")
    docstore = read_docstore()
    step_log(1, docstore["memory"]["memory_exists"],
             f"{docstore['memory']['memory_count']} memory entries, {docstore['governance_count']} governance rows")

    log("Step 2: Check sov-space...")
    sov = check_sovspace()
    if sov and "error" not in sov:
        inv = all(sov.get(f"invariant_{i}", False) for i in range(1, 7))
        step_log(2, inv, f"invariants={'OK' if inv else 'FAIL'}, care={sov.get('care_score_current')}")
    else:
        step_log(2, False, sov.get("error", "no state"))

    log("Step 3: Compute delta...")
    delta = compute_delta(sov)
    step_log(3, True, delta["reason"])

    log("Step 4: Train if needed...")
    train_r = train_if_needed(delta)
    step_log(4, train_r.get("trained", train_r.get("skipped", True)),
             train_r.get("reason", train_r.get("error", "trained")))

    log("Step 5: Run benchmarks...")
    bench_r = run_benchmarks(force=train_r.get("trained", False))
    step_log(5, bench_r.get("benchmarked", bench_r.get("skipped", True)),
             f"{'new results' if bench_r.get('benchmarked') else 'skipped'}")

    log("Step 6: SIGIL-sign heartbeat...")
    hb_num = heartbeat_state.get("heartbeat", 0)
    hb_data = {
        "heartbeat_count": hb_num,
        "timestamp": ts,
        "docstore": {k: v if not isinstance(v, dict) else {"memory_count": v.get("memory_count", 0)}
                     for k, v in docstore.items()},
        "delta": delta,
        "training": train_r,
        "benchmarks": {k: v for k, v in bench_r.items() if k != "results"},
        "sovspace": {k: v for k, v in heartbeat_state.items() if k != "data"},
    }
    sigil = sigil_sign(hb_data)
    step_log(6, True, f"hb_{hb_num:04d}.json ({sigil['sha256'][:16]}...)")

    log("Step 7: Deploy...")
    if train_r.get("trained") or bench_r.get("benchmarked"):
        deploy_r = deploy()
        step_log(7, deploy_r.get("deployed", False), "vercel")
    else:
        step_log(7, True, "skipped (no changes)")

    all_ok = all([
        inv if sov and "error" not in sov else False,
        True,
        True,
    ])
    log(f"{'ALL OK' if all_ok else 'ISSUES FOUND'} — heartbeat #{hb_num} complete")
    return 0 if all_ok else 1

if __name__ == "__main__":
    if "--cron" in sys.argv:
        while True:
            try:
                rc = main()
                if rc != 0:
                    log("Heartbeat FAILED, retrying in 60s...")
                    time.sleep(60)
                    continue
            except Exception as e:
                log(f"HEARTBEAT CRASH: {e}")
            log(f"Sleeping 30 min...")
            time.sleep(1800)
    else:
        sys.exit(main())
