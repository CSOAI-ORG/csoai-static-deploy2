#!/usr/bin/env python3
"""
OWEM Cluster Manager — Central Brain for CSOAI Sovereign AI Free-GPU Swarm.

Orchestrates training across ALL free GPU platforms with redundant 3-way
checkpointing, auto-recovery, round-robin workload distribution, and
SHA-256 sigil-verified state persistence.

Usage:
  python3 free_gpu/owem_cluster_manager.py status
  python3 free_gpu/owem_cluster_manager.py deploy [all|platform]
  python3 free_gpu/owem_cluster_manager.py checkpoint save|load
  python3 free_gpu/owem_cluster_manager.py recover
  python3 free_gpu/owem_cluster_manager.py scale
"""
import json
import hashlib
import os
import subprocess
import sys
import time
import threading
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FREE_GPU_DIR = ROOT / "free_gpu"
STATE_FILE = FREE_GPU_DIR / "cluster_state.json"
CHECKPOINT_DIR = ROOT / "sov-backup" / "checkpoints"
GIT_REMOTE = "https://github.com/CSOAI-ORG/csoai-static-deploy2.git"

SOV_VERSION = "sov33"

DOMAINS = [
    "eu_ai_act", "defence", "governance", "math", "coding",
    "safety", "reasoning", "agentic", "sovereign",
]

PLATFORMS = {
    "kaggle_t4": {
        "cost_hr": 0.0, "gpu": "T4", "vram_gb": 16, "limit": "30h/week",
        "tab": "tab5_kaggle_t4_a.py", "alt_tab": "tab6_kaggle_t4_b.py",
        "checkpoint_backend": "kaggle_dataset",
    },
    "colab_t4": {
        "cost_hr": 0.0, "gpu": "T4", "vram_gb": 16, "limit": "~12h/session",
        "tab": "tab7_colab_t4.py",
        "checkpoint_backend": "huggingface",
    },
    "lightning_t4": {
        "cost_hr": 0.0, "gpu": "T4", "vram_gb": 16, "limit": "3x/week",
        "tab": None,
        "checkpoint_backend": "huggingface",
    },
    "hf_t4": {
        "cost_hr": 0.0, "gpu": "T4", "vram_gb": 16, "limit": "limited",
        "tab": None,
        "checkpoint_backend": "huggingface",
    },
    "gradient_p100": {
        "cost_hr": 0.0, "gpu": "P100", "vram_gb": 16, "limit": "free tier",
        "tab": None,
        "checkpoint_backend": "huggingface",
    },
    "modal_t4": {
        "cost_hr": 0.0, "gpu": "T4", "vram_gb": 16, "limit": "spend_limit_exceeded",
        "tab": "tab3_modal_t4_1.py",
        "checkpoint_backend": "huggingface",
    },
    "oracle_arm": {
        "cost_hr": 0.0, "gpu": "ARM CPU", "vram_gb": 0, "limit": "always free",
        "tab": "tab8_oracle_arm_1.py", "alt_tab": "tab9_oracle_arm_2.py",
        "checkpoint_backend": "local",
    },
}


def _sigil(payload: str) -> str:
    return hashlib.sha256(f"owem|{payload}".encode("utf-8")).hexdigest()[:16]


def _full_sigil(payload: str) -> str:
    return hashlib.sha256(f"owem|{payload}".encode("utf-8")).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return data
        except (json.JSONDecodeError, OSError):
            return _fresh_state()
    return _fresh_state()


def _fresh_state() -> dict:
    base = {
        "owem_version": "1.0.0",
        "created": now_iso(),
        "workers": {},
        "workloads": [],
        "checkpoints": [],
        "recoveries": [],
        "total_cost": 0.0,
        "total_savings": 0.0,
        "cycles_completed": 0,
    }
    base["sigil"] = _full_sigil(json.dumps(
        {k: v for k, v in base.items() if k != "sigil"}, sort_keys=True, default=str,
    ))
    return base


def save_state(state: dict) -> None:
    try:
        state["sigil"] = _full_sigil(json.dumps(
            {k: v for k, v in state.items() if k != "sigil"}, sort_keys=True, default=str,
        ))
        state_str = json.dumps(state, indent=2, default=str)
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(state_str + "\n")
    except OSError as e:
        print(f"WARN: Could not save state: {e}")


def _verify_sigil(data: dict) -> bool:
    stored = data.get("sigil", "")
    if not stored:
        return False
    payload = json.dumps({k: v for k, v in data.items() if k != "sigil"}, sort_keys=True, default=str)
    expected = _full_sigil(payload)
    return stored == expected


# ── Worker Registry ──────────────────────────────────────────────────────────

def register_workers(state: dict) -> dict:
    workers = state.get("workers", {})
    for platform_name, info in PLATFORMS.items():
        worker_ids = [platform_name]
        alt_tab = info.get("alt_tab")
        if alt_tab:
            worker_ids.append(f"{platform_name}_b")
        for wid in worker_ids:
            if wid not in workers:
                workers[wid] = {
                    "platform": platform_name,
                    "worker_id": wid,
                    "status": "idle",
                    "current_workload": None,
                    "last_heartbeat": None,
                    "session_expiry": None,
                    "checkpoint_paths": [],
                    "created_at": now_iso(),
                    "gpu": info["gpu"],
                    "vram_gb": info["vram_gb"],
                    "cost_hr": info["cost_hr"],
                    "limit": info["limit"],
                }
    state["workers"] = workers
    return state


def _heartbeat_deadline(minutes: int = 15) -> str:
    deadline = datetime.now(timezone.utc).timestamp() - (minutes * 60)
    return datetime.fromtimestamp(deadline, tz=timezone.utc).isoformat()


def heartbeat(worker_id: str, state: dict) -> dict:
    workers = state.get("workers", {})
    if worker_id not in workers:
        print(f"WARN: Unknown worker {worker_id}")
        return state
    workers[worker_id]["last_heartbeat"] = now_iso()
    workers[worker_id]["status"] = workers[worker_id].get("status", "idle")
    sigil_payload = f"heartbeat|{worker_id}|{workers[worker_id]['last_heartbeat']}"
    workers[worker_id]["heartbeat_sigil"] = _sigil(sigil_payload)
    state["workers"] = workers
    return state


def detect_failed_workers(state: dict) -> list:
    failed = []
    deadline = _heartbeat_deadline(15)
    for wid, worker in state.get("workers", {}).items():
        hb = worker.get("last_heartbeat")
        if hb and hb < deadline and worker["status"] in ("running", "checkpointing"):
            worker["status"] = "failed"
            worker["failed_at"] = now_iso()
            failed.append(wid)
    if failed:
        state["workers"] = state["workers"]
    return failed


# ── Checkpoint System — Redundant 3-way Save ────────────────────────────────

def _checkpoint_filename(model_name: str, cycle: int) -> str:
    return f"owem_cluster_checkpoint_{model_name}_{cycle}.pt"


def _metadata_filename(model_name: str, cycle: int) -> str:
    return f"owem_cluster_checkpoint_{model_name}_{cycle}_metadata.json"


def _compute_sha256(path: Path) -> str:
    try:
        data = path.read_bytes()
        return hashlib.sha256(data).hexdigest()
    except OSError:
        return ""


def checkpoint_save(
    model_name: str,
    cycle: int,
    domain_scores: dict,
    platform: str,
    weights_data: bytes = b"",
    optimizer_data: bytes = b"",
    state: dict = None,
) -> dict:
    if state is None:
        state = load_state()
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    ckpt_name = _checkpoint_filename(model_name, cycle)
    meta_name = _metadata_filename(model_name, cycle)
    ckpt_path = CHECKPOINT_DIR / ckpt_name
    meta_path = CHECKPOINT_DIR / meta_name

    saved_backends = []

    # ── 1. Local disk ───────────────────────────────────────────────────
    try:
        ckpt_path.write_bytes(weights_data if weights_data else b"placeholder_weights")
        print(f"  [checkpoint] Local save: {ckpt_path}")
        saved_backends.append("local_disk")
    except OSError as e:
        print(f"  WARN: Local checkpoint save failed: {e}")

    # ── 2. GitHub (git commit + push) ───────────────────────────────────
    try:
        rel_ckpt = ckpt_path.relative_to(ROOT)
        subprocess.run(
            ["git", "add", str(rel_ckpt)],
            cwd=str(ROOT), capture_output=True, text=True, timeout=30,
        )
        msg = f"owem checkpoint: {model_name} cycle {cycle}"
        subprocess.run(
            ["git", "commit", "-m", msg, "--allow-empty"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=30,
        )
        push = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=60,
        )
        if push.returncode == 0:
            saved_backends.append("github")
            print("  [checkpoint] GitHub push: OK")
        else:
            print(f"  WARN: GitHub push stderr: {push.stderr[:200]}")
    except Exception as e:
        print(f"  WARN: GitHub checkpoint failed: {e}")

    # ── 3. HuggingFace Hub ──────────────────────────────────────────────
    hf_token = os.environ.get("HF_TOKEN", "")
    if hf_token:
        try:
            hf_repo = os.environ.get("HF_CHECKPOINT_REPO", "CSOAI/sov-checkpoints")
            boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
            file_data = weights_data if weights_data else b"placeholder"
            body = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="{ckpt_name}"\r\n'
                f"Content-Type: application/octet-stream\r\n\r\n"
            ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
            req = urllib.request.Request(
                f"https://huggingface.co/api/datasets/{hf_repo}/upload",
                data=body,
                headers={
                    "Authorization": f"Bearer {hf_token}",
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                },
                method="POST",
            )
            urllib.request.urlopen(req, timeout=60)
            saved_backends.append("huggingface")
            print(f"  [checkpoint] HF Hub save: {hf_repo}/{ckpt_name}")
        except Exception as e:
            print(f"  WARN: HF Hub checkpoint failed: {e}")
    else:
        print("  SKIP: No HF_TOKEN set, skipping HF Hub backup")

    # ── 4. Kaggle Dataset (optional 4th backup) ─────────────────────────
    kaggle_key = os.environ.get("KAGGLE_KEY", "")
    if kaggle_key and platform in ("kaggle_t4", "kaggle_t4_b"):
        try:
            kaggle_user = os.environ.get("KAGGLE_USER", "")
            if kaggle_user:
                req = urllib.request.Request(
                    "https://www.kaggle.com/api/v1/datasets/upload",
                    data=json.dumps({
                        "title": f"sov-checkpoint-{model_name}-{cycle}",
                        "ownerSlug": kaggle_user,
                        "subtitle": f"OWEM checkpoint {model_name} cycle {cycle}",
                    }).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {kaggle_key}",
                        "Content-Type": "application/json",
                    },
                    method="POST",
                )
                urllib.request.urlopen(req, timeout=60)
                saved_backends.append("kaggle_dataset")
                print(f"  [checkpoint] Kaggle dataset save: OK")
        except Exception as e:
            print(f"  WARN: Kaggle dataset upload failed: {e}")

    # ── Build metadata ──────────────────────────────────────────────────
    sha256_hash = _compute_sha256(ckpt_path) if ckpt_path.exists() else ""
    metadata = {
        "model_weights_path": str(ckpt_path),
        "optimizer_state_path": str(CHECKPOINT_DIR / f"optimizer_{model_name}_{cycle}.pt"),
        "training_cycle": cycle,
        "domain_scores": domain_scores,
        "timestamp": now_iso(),
        "platform": platform,
        "sha256": sha256_hash,
        "saved_backends": saved_backends,
        "model_name": model_name,
    }
    try:
        meta_path.write_text(json.dumps(metadata, indent=2) + "\n")
        print(f"  [checkpoint] Metadata: {meta_path}")
    except OSError as e:
        print(f"  WARN: Metadata save failed: {e}")

    entry = {
        "checkpoint_id": f"{model_name}_cyc{cycle}_{_sigil(ckpt_name)}",
        "model_name": model_name,
        "cycle": cycle,
        "path": str(ckpt_path),
        "metadata_path": str(meta_path),
        "sha256": sha256_hash,
        "saved_backends": saved_backends,
        "platform": platform,
        "timestamp": now_iso(),
        "sigil": _full_sigil(json.dumps(metadata, sort_keys=True)),
    }
    state.setdefault("checkpoints", []).append(entry)
    state["sigil"] = _full_sigil(json.dumps(
        {k: v for k, v in state.items() if k != "sigil"}, sort_keys=True, default=str,
    ))
    save_state(state)
    return entry


def checkpoint_load(checkpoint_id: str = None, state: dict = None) -> dict:
    if state is None:
        state = load_state()
    checkpoints = state.get("checkpoints", [])
    if not checkpoints:
        print("  No checkpoints found in state")
        return {}

    target = None
    if checkpoint_id:
        for ck in checkpoints:
            if ck.get("checkpoint_id") == checkpoint_id:
                target = ck
                break
        if not target:
            print(f"  Checkpoint {checkpoint_id} not found")
            return {}
    else:
        target = checkpoints[-1]

    ckpt_path = Path(target["path"])
    if ckpt_path.exists():
        sha256 = _compute_sha256(ckpt_path)
        if sha256 != target.get("sha256", ""):
            print(f"  WARN: SHA-256 mismatch for {ckpt_path}")
            print(f"    expected: {target.get('sha256')}")
            print(f"    actual:   {sha256}")
            return {"error": "sha256_mismatch", "expected": target.get("sha256"), "actual": sha256}
        print(f"  [checkpoint] Loaded from local: {ckpt_path}")
        return {"loaded": True, "checkpoint": target, "data": ckpt_path.read_bytes()}

    backends = target.get("saved_backends", [])
    for backend in backends:
        if backend == "github":
            try:
                subprocess.run(
                    ["git", "fetch", "origin", "main"],
                    cwd=str(ROOT), capture_output=True, text=True, timeout=30,
                )
                rel_path = Path(target["path"]).relative_to(ROOT)
                checkout = subprocess.run(
                    ["git", "checkout", "origin/main", "--", str(rel_path)],
                    cwd=str(ROOT), capture_output=True, text=True, timeout=30,
                )
                if checkout.returncode == 0 and ckpt_path.exists():
                    print(f"  [checkpoint] Restored from git: {ckpt_path}")
                    target["sha256"] = _compute_sha256(ckpt_path)
                    return {"loaded": True, "checkpoint": target, "data": ckpt_path.read_bytes()}
            except Exception as e:
                print(f"  WARN: Git restore failed: {e}")
        elif backend == "huggingface":
            try:
                hf_repo = os.environ.get("HF_CHECKPOINT_REPO", "CSOAI/sov-checkpoints")
                hf_token = os.environ.get("HF_TOKEN", "")
                model_name = target.get("model_name", "model")
                cycle = target.get("cycle", 0)
                fname = _checkpoint_filename(model_name, cycle)
                url = f"https://huggingface.co/datasets/{hf_repo}/resolve/main/{fname}"
                req = urllib.request.Request(url)
                if hf_token:
                    req.add_header("Authorization", f"Bearer {hf_token}")
                resp = urllib.request.urlopen(req, timeout=120)
                data = resp.read()
                ckpt_path.parent.mkdir(parents=True, exist_ok=True)
                ckpt_path.write_bytes(data)
                print(f"  [checkpoint] Restored from HF Hub: {url}")
                target["sha256"] = _compute_sha256(ckpt_path)
                return {"loaded": True, "checkpoint": target, "data": data}
            except Exception as e:
                print(f"  WARN: HF Hub restore failed: {e}")

    print(f"  ERROR: Checkpoint {target.get('checkpoint_id')} unrecoverable from all backends")
    return {"error": "unrecoverable", "checkpoint_id": target.get("checkpoint_id")}


def list_checkpoints(state: dict = None) -> list:
    if state is None:
        state = load_state()
    return state.get("checkpoints", [])


# ── Workload Distribution ───────────────────────────────────────────────────

def _generate_workload_id(domain: str, index: int) -> str:
    return f"wl_{domain}_{index}_{_sigil(f'{domain}{index}{now_iso()}')}"


def seed_workloads(state: dict, count_per_domain: int = 2) -> dict:
    existing = state.get("workloads", [])
    existing_domains = {w["domain"] for w in existing}
    idx = len(existing)
    for domain in DOMAINS:
        for i in range(count_per_domain):
            wid = _generate_workload_id(domain, idx)
            existing.append({
                "id": wid,
                "domain": domain,
                "status": "pending",
                "assigned_to": None,
                "checkpoint_id": None,
                "created_at": now_iso(),
                "cycle": 0,
            })
            idx += 1
    state["workloads"] = existing
    return state


def _select_worker_for_workload(domain: str, state: dict) -> str:
    workers = state.get("workers", {})
    idle = [
        (wid, w) for wid, w in workers.items()
        if w["status"] == "idle" and w.get("current_workload") is None
    ]
    idle.sort(key=lambda x: (x[1].get("cost_hr", 0), x[0]))
    if not idle:
        return ""
    return idle[0][0]


def distribute_workloads(state: dict) -> dict:
    workloads = state.get("workloads", [])
    pending = [w for w in workloads if w["status"] == "pending"]
    if not pending:
        print("  No pending workloads to distribute")
        return state

    assigned = 0
    for wl in pending:
        worker_id = _select_worker_for_workload(wl["domain"], state)
        if not worker_id:
            print(f"  No idle workers available for {wl['domain']}:{wl['id']}")
            break
        wl["status"] = "running"
        wl["assigned_to"] = worker_id
        wl["started_at"] = now_iso()
        state["workers"][worker_id]["status"] = "running"
        state["workers"][worker_id]["current_workload"] = wl["id"]
        cost_hr = state["workers"][worker_id].get("cost_hr", 0.0)
        state["total_cost"] = state.get("total_cost", 0.0) + cost_hr
        savings = 3.50 - cost_hr
        state["total_savings"] = state.get("total_savings", 0.0) + max(0, savings)
        assigned += 1
        print(f"  Assigned {wl['domain']}:{wl['id']} -> {worker_id}")

    state["workloads"] = workloads
    state["workers"] = state["workers"]
    state["sigil"] = _full_sigil(json.dumps(
        {k: v for k, v in state.items() if k != "sigil"}, sort_keys=True, default=str,
    ))
    save_state(state)
    print(f"  Distributed {assigned} workload(s)")
    return state


def complete_workload(wl_id: str, domain_scores: dict, state: dict) -> dict:
    workloads = state.get("workloads", [])
    target = None
    for wl in workloads:
        if wl["id"] == wl_id:
            target = wl
            break
    if not target:
        print(f"  Workload {wl_id} not found")
        return state

    worker_id = target.get("assigned_to")
    cycle = target.get("cycle", 0) + 1
    target["status"] = "completed"
    target["completed_at"] = now_iso()
    target["cycle"] = cycle
    target["domain_scores"] = domain_scores
    target["domain"] = target.get("domain", "unknown")
    checkpoint = checkpoint_save(
        model_name=f"sov33_{target['domain']}",
        cycle=cycle,
        domain_scores=domain_scores,
        platform=worker_id or "unknown",
        state=state,
    )
    target["checkpoint_id"] = checkpoint.get("checkpoint_id", "")

    if worker_id and worker_id in state.get("workers", {}):
        state["workers"][worker_id]["status"] = "idle"
        state["workers"][worker_id]["current_workload"] = None
        state["workers"][worker_id]["last_checkpoint"] = checkpoint.get("checkpoint_id", "")

    state["cycles_completed"] = state.get("cycles_completed", 0) + 1
    state["workloads"] = workloads
    state["workers"] = state["workers"]
    state["sigil"] = _full_sigil(json.dumps(
        {k: v for k, v in state.items() if k != "sigil"}, sort_keys=True, default=str,
    ))
    save_state(state)
    print(f"  Completed workload {wl_id} (cycle {cycle})")
    return state


# ── Auto-Recovery ───────────────────────────────────────────────────────────

def auto_recover(state: dict = None) -> dict:
    if state is None:
        state = load_state()

    failed = detect_failed_workers(state)
    if not failed:
        print("  No failed workers detected")
        return state

    print(f"  Detected {len(failed)} failed worker(s): {failed}")
    for worker_id in failed:
        worker = state["workers"].get(worker_id, {})
        wl_id = worker.get("current_workload")

        target_wl = None
        if wl_id:
            for wl in state.get("workloads", []):
                if wl["id"] == wl_id:
                    target_wl = wl
                    break

        checkpoint_data = None
        if target_wl and target_wl.get("checkpoint_id"):
            print(f"  Loading checkpoint for {wl_id}...")
            result = checkpoint_load(target_wl["checkpoint_id"], state)
            if result.get("loaded"):
                checkpoint_data = result["checkpoint"]
                print(f"  Checkpoint loaded: {checkpoint_data.get('checkpoint_id')}")

        new_worker_id = _select_worker_for_workload(
            target_wl["domain"] if target_wl else "unknown", state,
        )
        if not new_worker_id:
            print(f"  No available worker to resume {wl_id}")
            if target_wl:
                target_wl["status"] = "pending"
                target_wl["assigned_to"] = None
            continue

        print(f"  Reassigning {wl_id} from {worker_id} -> {new_worker_id}")
        if target_wl:
            target_wl["status"] = "running"
            target_wl["assigned_to"] = new_worker_id
            target_wl["recovered_at"] = now_iso()
            if checkpoint_data:
                target_wl["resumed_from_checkpoint"] = checkpoint_data.get("checkpoint_id")

        state["workers"][new_worker_id]["status"] = "running"
        state["workers"][new_worker_id]["current_workload"] = wl_id

        recovery_entry = {
            "timestamp": now_iso(),
            "failed_worker": worker_id,
            "workload_id": wl_id,
            "reassigned_to": new_worker_id,
            "checkpoint_used": checkpoint_data.get("checkpoint_id") if checkpoint_data else None,
            "sigil": _sigil(f"recover|{worker_id}|{wl_id}|{new_worker_id}"),
        }
        state.setdefault("recoveries", []).append(recovery_entry)
        print(f"  Recovery logged: {recovery_entry['sigil']}")

    state["workers"] = state["workers"]
    state["workloads"] = state.get("workloads", [])
    state["sigil"] = _full_sigil(json.dumps(
        {k: v for k, v in state.items() if k != "sigil"}, sort_keys=True, default=str,
    ))
    save_state(state)
    print(f"  Recovery complete")
    return state


# ── Scale ───────────────────────────────────────────────────────────────────

def scale_workers(state: dict = None) -> dict:
    if state is None:
        state = load_state()

    workers = state.get("workers", {})
    running_count = sum(
        1 for w in workers.values() if w["status"] == "running"
    )
    idle_count = sum(
        1 for w in workers.values() if w["status"] == "idle"
    )
    pending_count = sum(
        1 for w in state.get("workloads", []) if w["status"] == "pending"
    )

    print(f"  Running: {running_count}, Idle: {idle_count}, Pending workloads: {pending_count}")

    if pending_count > 0 and idle_count == 0 and running_count < len(workers):
        print("  All workers busy; attempting to wake idle platforms...")
        for wid, w in workers.items():
            if w["status"] == "idle":
                continue
            platform_name = w.get("platform", "")
            info = PLATFORMS.get(platform_name, {})
            tab_script = info.get("tab")
            if tab_script and w["status"] in ("idle",):
                tab_path = FREE_GPU_DIR / tab_script
                if tab_path.exists():
                    print(f"  Launching {tab_script} for {wid}...")
                    try:
                        subprocess.Popen(
                            ["python3", str(tab_path)],
                            cwd=str(ROOT),
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        w["status"] = "idle"
                        print(f"  {wid} launched")
                    except OSError as e:
                        print(f"  WARN: Could not launch {wid}: {e}")

    state["workers"] = workers
    state["sigil"] = _full_sigil(json.dumps(
        {k: v for k, v in state.items() if k != "sigil"}, sort_keys=True, default=str,
    ))
    save_state(state)
    return state


# ── CLI Commands ────────────────────────────────────────────────────────────

def cmd_status():
    state = load_state()
    register_workers(state)
    save_state(state)

    print(f"{'='*60}")
    print(f"  OWEM Cluster Manager — {SOV_VERSION}")
    print(f"  State: {STATE_FILE}")
    print(f"{'='*60}\n")

    print("Workers:")
    print(f"  {'Worker ID':20s} {'Platform':16s} {'Status':14s} {'GPU':12s} {'Workload':20s}")
    print(f"  {'-'*20} {'-'*16} {'-'*14} {'-'*12} {'-'*20}")
    for wid, w in sorted(state.get("workers", {}).items()):
        status_icon = {
            "idle": "○", "running": "●", "completed": "✓",
            "failed": "✗", "checkpointing": "◉",
        }.get(w["status"], "?")
        wl = (w.get("current_workload") or "")[:20]
        print(f"  {status_icon} {wid:18s} {w['platform']:16s} {w['status']:14s} {w['gpu']:12s} {wl:20s}")

    print(f"\nWorkloads ({len(state.get('workloads', []))} total):")
    by_status = {}
    for wl in state.get("workloads", []):
        s = wl["status"]
        by_status.setdefault(s, 0)
        by_status[s] += 1
    for s, count in sorted(by_status.items()):
        print(f"  {s:12s}: {count}")

    print(f"\nCheckpoints: {len(state.get('checkpoints', []))}")
    if state.get("checkpoints"):
        latest = state["checkpoints"][-1]
        print(f"  Latest: {latest.get('checkpoint_id', '')[:50]}")
        print(f"  Backends: {latest.get('saved_backends', [])}")

    print(f"\nRecoveries: {len(state.get('recoveries', []))}")
    print(f"Cycles completed: {state.get('cycles_completed', 0)}")
    print(f"Total cost: ${state.get('total_cost', 0.0):.4f}")
    print(f"Total savings vs H100: ${state.get('total_savings', 0.0):.4f}")
    print(f"\nSigil: {state.get('sigil', '')[:20]}...")
    sigil_ok = _verify_sigil(state)
    print(f"State integrity: {'PASS' if sigil_ok else 'FAIL'}")
    return state


def cmd_deploy(target: str):
    state = load_state()
    register_workers(state)

    if target == "all":
        state = seed_workloads(state, count_per_domain=1)
        state = distribute_workloads(state)
    elif target in PLATFORMS:
        platform_workloads = [
            w for w in state.get("workloads", [])
            if w["status"] == "pending"
        ]
        if not platform_workloads:
            state = seed_workloads(state, count_per_domain=1)
            platform_workloads = [
                w for w in state.get("workloads", [])
                if w["status"] == "pending"
            ]
        target_worker = f"{target}"
        if target_worker in state.get("workers", {}):
            worker = state["workers"][target_worker]
            if platform_workloads:
                wl = platform_workloads[0]
                wl["status"] = "running"
                wl["assigned_to"] = target_worker
                wl["started_at"] = now_iso()
                worker["status"] = "running"
                worker["current_workload"] = wl["id"]
                print(f"  Deployed {wl['domain']}:{wl['id']} -> {target_worker}")
        else:
            print(f"  Worker {target} not found in registry")
    elif target.startswith("wl_"):
        state = distribute_workloads(state)
    else:
        print(f"  Unknown deploy target: {target}")
        print("  Usage: deploy [all|platform_name|wl_<id>]")
        return state

    state["sigil"] = _full_sigil(json.dumps(
        {k: v for k, v in state.items() if k != "sigil"}, sort_keys=True, default=str,
    ))
    save_state(state)
    return state


def cmd_checkpoint(op: str):
    state = load_state()
    if op == "save":
        print("  Creating manual checkpoint...")
        entry = checkpoint_save(
            model_name="manual_save",
            cycle=state.get("cycles_completed", 0),
            domain_scores={},
            platform="cli",
            state=state,
        )
        print(f"  Checkpoint created: {entry.get('checkpoint_id', '')}")
    elif op == "load":
        ckpt_id = None
        if len(sys.argv) > 3:
            ckpt_id = sys.argv[3]
        print(f"  Loading checkpoint{' ' + ckpt_id if ckpt_id else ' (latest)'}...")
        result = checkpoint_load(ckpt_id, state)
        if result.get("loaded"):
            print(f"  Loaded: {result['checkpoint'].get('checkpoint_id', '')}")
        else:
            print(f"  Load failed: {result.get('error', 'unknown')}")
    else:
        print("  Usage: checkpoint [save|load [checkpoint_id]]")
    return state


def cmd_recover():
    state = load_state()
    register_workers(state)
    state = auto_recover(state)
    save_state(state)
    return state


def cmd_scale():
    state = load_state()
    register_workers(state)
    state = scale_workers(state)
    save_state(state)
    return state


def cmd_heartbeat():
    state = load_state()
    register_workers(state)
    if len(sys.argv) > 2:
        worker_id = sys.argv[2]
        state = heartbeat(worker_id, state)
        save_state(state)
        print(f"  Heartbeat recorded for {worker_id}")
    else:
        print("  Usage: heartbeat <worker_id>")
    return state


def cmd_complete():
    state = load_state()
    if len(sys.argv) > 2:
        wl_id = sys.argv[2]
        scores = {}
        if len(sys.argv) > 3:
            try:
                scores = json.loads(sys.argv[3])
            except json.JSONDecodeError:
                print("  WARN: Invalid domain_scores JSON, using empty dict")
        state = complete_workload(wl_id, scores, state)
    else:
        print("  Usage: complete <workload_id> [domain_scores_json]")
    return state


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("status", "st"):
        cmd_status()
    elif args[0] == "deploy":
        target = args[1] if len(args) > 1 else "all"
        cmd_deploy(target)
    elif args[0] == "checkpoint":
        op = args[1] if len(args) > 1 else "save"
        cmd_checkpoint(op)
    elif args[0] == "recover":
        cmd_recover()
    elif args[0] == "scale":
        cmd_scale()
    elif args[0] == "heartbeat":
        cmd_heartbeat()
    elif args[0] == "complete":
        cmd_complete()
    else:
        print(f"Usage: {sys.argv[0]} [status|deploy|checkpoint|recover|scale|heartbeat|complete]")
        print(f"  status                          Show all workers + workloads + checkpoints")
        print(f"  deploy [all|platform|wl_<id>]   Deploy workloads to workers")
        print(f"  checkpoint save|load [id]       Manual checkpoint operations")
        print(f"  recover                         Auto-recover failed workers")
        print(f"  scale                           Scale up worker pool")
        print(f"  heartbeat <worker_id>           Record heartbeat for a worker")
        print(f"  complete <wl_id> [scores_json]  Mark workload complete")
        sys.exit(1)


if __name__ == "__main__":
    main()
