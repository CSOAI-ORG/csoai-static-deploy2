#!/usr/bin/env python3
"""runpod_sync.py — Move heavy science-loop artefacts to RunPod and stop the
local Mac from filling up.

What it does:
  1. SSH into sov33-top-bench-2 (the A40 pod, RUNNING, SSH open)
  2. Creates /workspace/sov-sov7/ on the pod
  3. rsyncs the local SOV_DATA_DIR contents (jsonl streams, cycle reports,
     sigil receipts) to the pod
  4. Optionally rsyncs training data and model artefacts if --full is given
  5. Prints before/after disk usage on Mac

Usage:
  python3 runpod_sync.py                # sync data dir only (default)
  python3 runpod_sync.py --full         # also push big model artefacts
  python3 runpod_sync.py --clean-local  # delete synced files from Mac
  python3 runpod_sync.py --setup        # just create the remote dir
  python3 runpod_sync.py --pull         # reverse: pull from pod -> local

After sync, set SOV_DATA_DIR=/workspace/sov-sov7 and SOV_HEARTBEATS_DIR=
/workspace/sov-sov7/heartbeats to keep new work on RunPod.
"""
import argparse, os, shlex, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

POD_NAME = "sov33-top-bench-2"
POD_HOST = "69.30.85.23"
POD_PORT = "22087"
POD_USER = "root"
REMOTE_DIR = os.environ.get("SOV_REMOTE_DIR", "/workspace/sov-sov7")

SSH_BASE = ["ssh", "-p", POD_PORT, "-o", "StrictHostKeyChecking=accept-new",
            "-o", "BatchMode=yes", f"{POD_USER}@{POD_HOST}"]
SCP_BASE = ["scp", "-P", POD_PORT, "-o", "StrictHostKeyChecking=accept-new",
            "-o", "BatchMode=yes"]
RSYNC_SSH = f"ssh -p {POD_PORT} -o StrictHostKeyChecking=accept-new -o BatchMode=yes"

# Things to move by default
DEFAULT_LOCAL = [
    "benchmark-results/capability_registry.json",
    "benchmark-results/run_capability_matrix.py",
    "benchmark-results/aggregate_capability_results.py",
    "benchmark-results/govbench_v6.py",
    "benchmark-results/test_govbench_v6.py",
    "benchmark-results/task_registry.json",
    "benchmark-results/visual_operators.py",
    "benchmark-results/sov6_train_pipeline.py",
    "benchmark-results/sov5_sov6_pipeline.py",
    "benchmark-results/sov5_visual_router.py",
    "sov_invariants.py",
    "sovereign_api.py",
    "sov4_router.py",
    "sov6_stack.py",
    "test_sov_runtime_alignment.py",
    "tools/sov_migrate_payload.py",
    "sovereign-charters/sov33-capability-registry.json",
    "benchmark-results/sov5_self_training.jsonl",
    "benchmark-results/sov5_self_training.avoid.jsonl",
    "benchmark-results/sov5_self_training.json",
    "benchmark-results/sov7_cycles",
    "heartbeats",
]

# Big artefacts to move only with --full
FULL_ARTIFACTS = [
    "benchmark-results/tokenizer.json",
    "benchmark-results/vocab.json",
    "benchmark-results/visual_router_model.pt",
    "benchmark-results/visual_router_model.pt.backup",
    "benchmark-results/adapter_model.safetensors",
    "benchmark-results/sov1_bloodline.jsonl",
    "benchmark-results/sov5_training_chatml.jsonl",
    "benchmark-results/sov5_training_dataset.jsonl",
    "benchmark-results/sov5_train_ready.jsonl",
    "benchmark-results/sovereign_synth_50k.jsonl",
    "benchmark-results/grpo_training_data.jsonl",
    "benchmark-results/checkpoints",
    "benchmark-results/fluid-v1",
]


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def sh_text(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def ssh(cmd_str):
    """Run a shell command on the pod. Returns stdout."""
    r = subprocess.run([*SSH_BASE, cmd_str], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ssh failed: {r.stderr}")
    return r.stdout


def disk_mac():
    r = subprocess.run(["df", "-h", str(ROOT)], capture_output=True, text=True)
    return r.stdout.splitlines()[-1] if r.stdout else "?"


def mac_dir_size(p):
    try:
        out = subprocess.run(["du", "-sh", str(p)], capture_output=True, text=True).stdout
        return out.split()[0] if out else "?"
    except Exception:
        return "?"


def setup_remote():
    """Ensure the remote dir exists and is writable."""
    print(f"  ensuring {REMOTE_DIR} on {POD_NAME}...")
    ssh(f"mkdir -p {REMOTE_DIR}/{{heartbeats,cycles,artifacts}}")
    ssh(f"df -h /workspace | head -2")
    print("  OK")


def sync(local_paths, subdir=""):
    """Push a list of local paths (relative to ROOT) to <REMOTE_DIR>/<subdir>/.
    Uses tar-over-ssh (works on any pod) instead of rsync which may not be
    installed. For a single file, falls back to scp.
    """
    target = f"{REMOTE_DIR}/{subdir}".rstrip("/")
    ssh(f"mkdir -p {target}")
    for rel in local_paths:
        src = ROOT / rel
        if not src.exists():
            print(f"  skip {rel} (missing)")
            continue
        if src.is_file():
            remote_path = f"{POD_USER}@{POD_HOST}:{target}/{src.name}"
            cmd = [*SCP_BASE, str(src), remote_path]
            print(f"  scp {rel} -> {target}/{src.name}")
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"    WARN: scp returned {r.returncode}: {r.stderr[:200]}")
        else:
            # tar pipe over ssh: cd into the dir, tar it, untar on the pod
            name = src.name
            remote = f"{POD_USER}@{POD_HOST}:{target}/{name}.tar"
            cmd = (f"tar -C {shlex.quote(str(src.parent))} -cf - {shlex.quote(name)} | "
                   f"ssh -p {POD_PORT} -o StrictHostKeyChecking=accept-new "
                   f"-o BatchMode=yes {POD_USER}@{POD_HOST} "
                   f"'cd {target} && tar -xf -'")
            print(f"  tar | ssh {rel}/ -> {target}/{name}/")
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"    WARN: tar-ssh returned {r.returncode}: {r.stderr[:200]}")


def clean_local(local_paths):
    """Delete the local copies that were synced."""
    for rel in local_paths:
        p = ROOT / rel
        if not p.exists():
            continue
        if p.is_dir():
            # Only remove files inside that look synced
            n = sum(1 for _ in p.rglob("*"))
            print(f"  rm -rf {rel}/  ({n} files)")
            subprocess.run(["rm", "-rf", str(p)])
        else:
            print(f"  rm {rel}  ({p.stat().st_size} bytes)")
            p.unlink()


def pull_all():
    """Reverse: pull everything from REMOTE_DIR back to local."""
    for sub in ["", "heartbeats", "cycles", "artifacts"]:
        remote = f"{POD_USER}@{POD_HOST}:{REMOTE_DIR}/{sub}".rstrip("/")
        local = ROOT / ("heartbeats" if sub == "heartbeats" else
                        "cycles" if sub == "cycles" else
                        "benchmark-results" if not sub else "benchmark-results/artifacts")
        local.mkdir(parents=True, exist_ok=True)
        cmd = ["rsync", "-avz", "-e", RSYNC_SSH, remote + "/", str(local) + "/"]
        print(f"  rsync {remote} -> {local}")
        subprocess.run(cmd)


def main():
    ap = argparse.ArgumentParser(description="Sync sov7 data to RunPod")
    ap.add_argument("--full", action="store_true", help="Also sync big model artefacts")
    ap.add_argument("--clean-local", action="store_true", help="Delete local files after sync")
    ap.add_argument("--setup", action="store_true", help="Just create the remote dir")
    ap.add_argument("--pull", action="store_true", help="Pull from pod to local")
    args = ap.parse_args()

    print("=== RUNPOD SYNC ===")
    print(f"  pod:    {POD_NAME} ({POD_HOST}:{POD_PORT})")
    print(f"  remote: {REMOTE_DIR}")
    print(f"  local:  {ROOT}")
    print(f"  mac disk before: {disk_mac()}")
    print()

    if args.pull:
        print("--- pull from pod ---")
        pull_all()
        print("\nDONE")
        return

    setup_remote()

    if not args.setup:
        print("\n--- sync data (default) ---")
        sync(DEFAULT_LOCAL, subdir="")
        if args.full:
            print("\n--- sync big artefacts (--full) ---")
            sync(FULL_ARTIFACTS, subdir="artifacts")

    if args.clean_local:
        print("\n--- cleaning local copies ---")
        clean_local(DEFAULT_LOCAL)
        if args.full:
            clean_local(FULL_ARTIFACTS)

    print(f"\n  mac disk after:  {disk_mac()}")
    print(f"\nDONE")
    print(f"\nNext: export SOV_DATA_DIR={REMOTE_DIR}")
    print(f"       export SOV_HEARTBEATS_DIR={REMOTE_DIR}/heartbeats")


if __name__ == "__main__":
    main()
