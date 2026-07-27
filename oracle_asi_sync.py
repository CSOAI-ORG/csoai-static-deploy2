#!/usr/bin/env python3
"""
oracle_asi_sync.py — Sync enriched training data to oracle-micro and run
a bloodline-enhanced ASI evolution training cycle.

Oracle Micro: 145.241.232.16 (ubuntu, key: ~/.ssh/id_ed25519)
"""

import subprocess, sys, os, json
from pathlib import Path
from datetime import datetime

ORACLE_HOST = "145.241.232.16"
ORACLE_USER = "ubuntu"
SSH_KEY = os.path.expanduser("~/.ssh/id_ed25519")
REMOTE_DIR = "/home/ubuntu/asi_training"
BASE_MODEL = "qwen2.5:0.5b"
EVOLVED_MODEL = "sov33-oracle:latest"

DATA_FILES = [
    "benchmark-results/sovereign_synth_50k.jsonl",
    "benchmark-results/sov5_training_dataset.jsonl",
    "benchmark-results/sovereign_corpus_e2e.jsonl",
]

SSH_BASE = [
    "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10", f"{ORACLE_USER}@{ORACLE_HOST}",
]
SCP_BASE = [
    "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
]


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def run(cmd, desc, timeout=600):
    log(f"> {desc}")
    log(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        for line in result.stderr.strip().split("\n"):
            if line.strip():
                log(f"  STDERR: {line.strip()}")
        raise RuntimeError(f"{desc} failed (exit {result.returncode})")
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            log(f"  {line.strip()}")
    return result.stdout.strip()


def ssh(script_body, desc, timeout=600):
    log(f"> {desc}")
    full_cmd = SSH_BASE + ["bash", "-s"]
    result = subprocess.run(
        full_cmd, input=script_body, capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        for line in result.stderr.strip().split("\n"):
            if line.strip():
                log(f"  STDERR: {line.strip()}")
        raise RuntimeError(f"SSH {desc} failed (exit {result.returncode})")
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            log(f"  {line.strip()}")
    return result.stdout.strip()


def step_verify_and_sync():
    log("=" * 60)
    log("  STEP 1: Verify local data files")
    log("=" * 60)
    for f in DATA_FILES:
        p = Path(f)
        if not p.exists():
            log(f"  MISSING: {f}")
            sys.exit(1)
        log(f"  OK: {f} ({p.stat().st_size / 1024:.0f} KB)")

    log("")
    log("=" * 60)
    log("  STEP 2: Create remote directory and sync data")
    log("=" * 60)

    ssh(f"mkdir -p {REMOTE_DIR}/data {REMOTE_DIR}/results", "create remote dirs")

    for f in DATA_FILES:
        remote = f"{ORACLE_USER}@{ORACLE_HOST}:{REMOTE_DIR}/data/"
        run(SCP_BASE + [f, remote], f"SCP {f}")

    log("  Data sync complete.")


def step_deploy_and_run():
    log("")
    log("=" * 60)
    log("  STEP 3: Deploy bloodline training script")
    log("=" * 60)

    local_script = Path("oracle_bloodline_train.py")
    remote_script_path = f"{REMOTE_DIR}/bloodline_train.py"
    run(
        SCP_BASE + [str(local_script), f"{ORACLE_USER}@{ORACLE_HOST}:{remote_script_path}"],
        "SCP bloodline_train.py",
    )

    log("")
    log("=" * 60)
    log("  STEP 4: Run bloodline-enhanced training on oracle-micro")
    log("  (training on remote — may take several minutes)")
    log("=" * 60)
    ssh(
        f"cd {REMOTE_DIR} && python3 bloodline_train.py",
        "bloodline_train.py",
        timeout=7200,
    )

    log("")
    log("=" * 60)
    log("  STEP 5: Sync results back to ./oracle_results/")
    log("=" * 60)
    local_results = Path("oracle_results")
    local_results.mkdir(exist_ok=True)
    run(
        SCP_BASE + [
            "-r",
            f"{ORACLE_USER}@{ORACLE_HOST}:{REMOTE_DIR}/results/",
            str(local_results) + "/",
        ],
        "SCP results ← oracle-micro",
    )
    log(f"  Results saved to {local_results}/")


def main():
    print(f"""
{"=" * 70}
  ORACLE ASI SYNC — Bloodline-Enhanced Training Pipeline
  Target:   {ORACLE_USER}@{ORACLE_HOST}
  Data:     {', '.join(DATA_FILES)}
  Key:      {SSH_KEY}
{"=" * 70}
""")
    try:
        step_verify_and_sync()
        step_deploy_and_run()
        log("")
        log("=" * 60)
        log("  ALL DONE — Bloodline training cycle complete!")
        log("=" * 60)
    except RuntimeError as e:
        log(f"FATAL: {e}")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log("FATAL: Command timed out")
        sys.exit(1)


if __name__ == "__main__":
    main()
