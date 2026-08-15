#!/usr/bin/env python3
"""SOV33 Overnight Auto-Runner — Runs all benchmarks and improvements."""
import json, subprocess, time, hashlib, os
from pathlib import Path
from datetime import datetime, timezone

LOG_FILE = Path("overnight_run.log")
RESULTS = {}

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run_cmd(cmd, timeout=300):
    log(f"Running: {cmd[:80]}...")
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout + r.stderr
    except:
        return False, "timeout"

def main():
    log("="*70)
    log("  SOV33 OVERNIGHT AUTO-RUNNER")
    log("="*70)
    
    # 1. E2E Tests
    log("\n[1/5] Running E2E tests...")
    ok, out = run_cmd("python3 .e2e_tests.py", timeout=300)
    RESULTS["e2e"] = {"passed": ok, "output": out[-500:]}
    log(f"  E2E: {'PASS' if ok else 'FAIL'}")
    
    # 2. Batch Verifier
    log("\n[2/5] Running batch verifier...")
    ok, out = run_cmd("python3 tools/verify_e2e_batch.py", timeout=300)
    RESULTS["batch_verifier"] = {"passed": ok, "output": out[-500:]}
    log(f"  Batch: {'PASS' if ok else 'FAIL'}")
    
    # 3. Generate more training data
    log("\n[3/5] Generating training data...")
    ok, out = run_cmd("python3 benchmark-results/generate_ultimate_training.py", timeout=60)
    RESULTS["training_data"] = {"passed": ok}
    log(f"  Training data: {'OK' if ok else 'FAIL'}")
    
    # 4. Run local benchmarks
    log("\n[4/5] Running local benchmarks...")
    if os.path.exists("benchmark-results/run_ollama_benchmark.py"):
        ok, out = run_cmd("python3 benchmark-results/run_ollama_benchmark.py --model qwen2.5:0.5b --suite sovereign_compliance --limit 10", timeout=600)
        RESULTS["benchmark"] = {"passed": ok, "output": out[-500:]}
        log(f"  Benchmark: {'PASS' if ok else 'FAIL'}")
    
    # 5. Run on RunPod if available
    log("\n[5/5] Checking RunPod...")
    ok, out = run_cmd("python3 benchmark-results/batch_runpod.py status", timeout=30)
    if ok:
        RESULTS["runpod"] = {"status": "available", "output": out[-200:]}
        log("  RunPod: Available")
    else:
        RESULTS["runpod"] = {"status": "unavailable"}
        log("  RunPod: Unavailable")
    
    # Save results
    RESULTS["timestamp"] = datetime.now(timezone.utc).isoformat()
    RESULTS["sigil"] = hashlib.sha256(json.dumps(RESULTS, sort_keys=True).encode()).hexdigest()
    
    with open("overnight_results.json", "w") as f:
        json.dump(RESULTS, f, indent=2)
    
    log(f"\n{'='*70}")
    log(f"  OVERNIGHT RUN COMPLETE")
    log(f"{'='*70}")
    log(f"  Results: overnight_results.json")
    log(f"  SIGIL: {RESULTS['sigil']}")

if __name__ == "__main__":
    main()
