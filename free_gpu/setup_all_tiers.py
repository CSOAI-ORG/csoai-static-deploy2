#!/usr/bin/env python3
"""
setup_all_tiers.py — Master Setup Orchestrator

Runs all free GPU tier setup scripts and generates a comprehensive
deployment status report.

This script:
  1. Runs setup_colab.py      → Colab T4 notebook
  2. Runs setup_lightning.py  → Lightning AI Studio files
  3. Runs setup_hf_spaces.py  → HuggingFace Space files
  4. Runs setup_gradient.py   → Gradient/PaperSpace notebook
  5. Reads existing tiers from orchestrator.py
  6. Generates all_tiers_status.json with full deployment report
  7. Prints a table of all 7+ free GPU tiers

Usage:
  python3 free_gpu/setup_all_tiers.py [--skip-generate] [--output-dir PATH]

Options:
  --skip-generate  Skip running sub-generators (just produce status report)
  --output-dir     Output directory (default: free_gpu/)
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
FREE_GPU_DIR = ROOT_DIR / "free_gpu"
STATE_FILE = FREE_GPU_DIR / "swarm_state.json"
STATUS_OUTPUT = FREE_GPU_DIR / "all_tiers_status.json"

TIERS: dict[str, dict[str, Any]] = {
    "local_m4": {
        "gpu": "Apple M4 (CPU inference)",
        "vram_gb": 0,
        "cost_hr": 0.0,
        "limit": "Always",
        "provider": "Local",
        "status": "available",
        "setup_script": None,
    },
    "m2_lan": {
        "gpu": "Apple M2 (CPU inference)",
        "vram_gb": 0,
        "cost_hr": 0.0,
        "limit": "Always",
        "provider": "Local LAN",
        "status": "available",
        "setup_script": None,
    },
    "oracle_arm": {
        "gpu": "Oracle ARM (CPU, 4 OCPU)",
        "vram_gb": 0,
        "cost_hr": 0.0,
        "limit": "Always-free",
        "provider": "Oracle Cloud",
        "status": "available",
        "setup_script": None,
    },
    "kaggle_t4": {
        "gpu": "NVIDIA T4 16GB",
        "vram_gb": 16,
        "cost_hr": 0.0,
        "limit": "30h/week",
        "provider": "Kaggle",
        "status": "available",
        "setup_script": "setup_colab.py",
    },
    "colab_t4": {
        "gpu": "NVIDIA T4 16GB",
        "vram_gb": 16,
        "cost_hr": 0.0,
        "limit": "12h/session",
        "provider": "Google Colab",
        "status": "available",
        "setup_script": "setup_colab.py",
    },
    "lightning_t4": {
        "gpu": "NVIDIA T4 16GB",
        "vram_gb": 16,
        "cost_hr": 0.0,
        "limit": "22h/month",
        "provider": "Lightning AI",
        "status": "setup_available",
        "setup_script": "setup_lightning.py",
    },
    "hf_spaces_t4": {
        "gpu": "NVIDIA T4 16GB",
        "vram_gb": 16,
        "cost_hr": 0.0,
        "limit": "2 concurrent, ~24h",
        "provider": "HuggingFace Spaces",
        "status": "setup_available",
        "setup_script": "setup_hf_spaces.py",
    },
    "gradient_p100": {
        "gpu": "NVIDIA P100 16GB",
        "vram_gb": 16,
        "cost_hr": 0.0,
        "limit": "6h/session",
        "provider": "Gradient/PaperSpace",
        "status": "setup_available",
        "setup_script": "setup_gradient.py",
    },
    "modal_t4": {
        "gpu": "NVIDIA T4 16GB",
        "vram_gb": 16,
        "cost_hr": 0.0,
        "limit": "~30h/month",
        "provider": "Modal Labs",
        "status": "spend_limit_exceeded",
        "setup_script": None,
    },
    "runpod_3090": {
        "gpu": "NVIDIA RTX 3090 24GB",
        "vram_gb": 24,
        "cost_hr": 0.22,
        "limit": "On-demand",
        "provider": "RunPod",
        "status": "available",
        "setup_script": None,
    },
    "runpod_a40": {
        "gpu": "NVIDIA A40 48GB",
        "vram_gb": 48,
        "cost_hr": 0.44,
        "limit": "On-demand",
        "provider": "RunPod",
        "status": "available",
        "setup_script": None,
    },
    "runpod_h100": {
        "gpu": "NVIDIA H100 80GB",
        "vram_gb": 80,
        "cost_hr": 3.50,
        "limit": "On-demand",
        "provider": "RunPod",
        "status": "available",
        "setup_script": None,
    },
}


def log(msg: str) -> None:
    print(msg, flush=True)


def compute_sigil(data: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, default=str).encode()
    ).hexdigest()


def file_exists(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def check_generated_artifacts() -> dict[str, dict[str, Any]]:
    """Check which setup artifacts exist and return their status."""
    artifacts: dict[str, dict[str, Any]] = {}

    checks: list[tuple[str, str, Path]] = [
        ("kaggle_t4", "Notebook (via setup_colab)", FREE_GPU_DIR / "sov33_colab_training.ipynb"),
        ("colab_t4", "Notebook (via setup_colab)", FREE_GPU_DIR / "sov33_colab_training.ipynb"),
        ("lightning_t4", "Studio YAML", FREE_GPU_DIR / "lightning_studio.yaml"),
        ("lightning_t4_train", "Training script", FREE_GPU_DIR / "lightning_train.py"),
        ("hf_spaces_t4", "README", FREE_GPU_DIR / "hf_space" / "README.md"),
        ("hf_spaces_t4_app", "Gradio app", FREE_GPU_DIR / "hf_space" / "app.py"),
        ("hf_spaces_t4_reqs", "Requirements", FREE_GPU_DIR / "hf_space" / "requirements.txt"),
        ("gradient_p100", "Notebook", FREE_GPU_DIR / "gradient_sov33.ipynb"),
    ]

    for key, label, fpath in checks:
        exists = file_exists(fpath)
        size_kb = round(fpath.stat().st_size / 1024, 1) if exists else 0
        sigil = ""
        if exists:
            sigil = compute_sigil({"path": str(fpath), "size": fpath.stat().st_size})
        artifacts[key] = {
            "label": label,
            "path": str(fpath),
            "exists": exists,
            "size_kb": size_kb,
            "sigil": sigil[:16] if sigil else "",
        }

    return artifacts


def run_setup_scripts() -> dict[str, dict[str, Any]]:
    """Run each setup script and return results."""
    results: dict[str, dict[str, Any]] = {}

    scripts: list[tuple[str, str, list[str]]] = [
        ("setup_colab", "Colab T4 Notebook", [
            sys.executable, str(FREE_GPU_DIR / "setup_colab.py"),
        ]),
        ("setup_lightning", "Lightning AI Studio", [
            sys.executable, str(FREE_GPU_DIR / "setup_lightning.py"),
        ]),
        ("setup_hf_spaces", "HuggingFace Space", [
            sys.executable, str(FREE_GPU_DIR / "setup_hf_spaces.py"),
        ]),
        ("setup_gradient", "Gradient/PaperSpace Notebook", [
            sys.executable, str(FREE_GPU_DIR / "setup_gradient.py"),
        ]),
    ]

    for key, name, cmd in scripts:
        log(f"  [{key}] Running {name}...")
        t0 = datetime.now(timezone.utc)
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120,
            )
            elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
            results[key] = {
                "name": name,
                "returncode": proc.returncode,
                "elapsed_s": round(elapsed, 2),
                "stdout_preview": proc.stdout.strip()[:300],
                "stderr_preview": proc.stderr.strip()[:300],
                "success": proc.returncode == 0,
            }
            if proc.returncode == 0:
                log(f"    ✓ Completed in {elapsed:.1f}s")
            else:
                log(f"    ✗ Failed (rc={proc.returncode}): {proc.stderr.strip()[:100]}")
        except subprocess.TimeoutExpired:
            results[key] = {
                "name": name,
                "returncode": -1,
                "elapsed_s": 120,
                "stdout_preview": "",
                "stderr_preview": "Timed out after 120s",
                "success": False,
            }
            log(f"    ✗ Timed out")
        except FileNotFoundError:
            results[key] = {
                "name": name,
                "returncode": -2,
                "elapsed_s": 0,
                "stdout_preview": "",
                "stderr_preview": f"Script not found: {cmd[1]}",
                "success": False,
            }
            log(f"    ✗ Script not found")
        except Exception as e:
            results[key] = {
                "name": name,
                "returncode": -3,
                "elapsed_s": 0,
                "stdout_preview": "",
                "stderr_preview": str(e),
                "success": False,
            }
            log(f"    ✗ Error: {e}")

    return results


def load_swarm_state() -> dict[str, Any]:
    """Load existing swarm state for cumulative metrics."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def build_status_report(
    setup_results: dict[str, dict[str, Any]] | None,
    artifacts: dict[str, dict[str, Any]],
    run_setups: bool,
) -> dict[str, Any]:
    """Build the complete status report."""
    swarm = load_swarm_state()

    tier_statuses: dict[str, dict[str, Any]] = {}
    for name, info in TIERS.items():
        status = dict(info)
        tier_statuses[name] = status

    report: dict[str, Any] = {
        "report_metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generated_by": "setup_all_tiers.py",
            "project_root": str(ROOT_DIR),
            "free_gpu_dir": str(FREE_GPU_DIR),
        },
        "tier_count": len(TIERS),
        "free_tier_count": sum(1 for t in TIERS.values() if t["cost_hr"] == 0.0),
        "tiers": tier_statuses,
        "artifacts": artifacts,
        "swarm_state_summary": {
            "total_runs": len(swarm.get("runs", [])),
            "total_cost": swarm.get("total_cost", 0.0),
            "total_savings": swarm.get("total_savings", 0.0),
            "state_file": str(STATE_FILE),
        },
    }

    if setup_results is not None:
        report["setup_scripts_run"] = setup_results
        report["all_setups_succeeded"] = all(
            r["success"] for r in setup_results.values()
        )

    report["sigil"] = compute_sigil(report)

    return report


def print_table(report: dict[str, Any]) -> None:
    """Print a formatted table of all GPU tiers."""
    tiers = report["tiers"]
    artifacts = report["artifacts"]

    log("")
    log("=" * 90)
    log("  SOV33 — FREE GPU TIER STATUS REPORT")
    log(f"  Generated: {report['report_metadata']['generated_at'][:19]} UTC")
    log("=" * 90)
    log("")
    log(
        f"  {'#':>2s}  {'Tier':<20s}  {'Provider':<20s}  {'GPU':<24s}  "
        f"{'VRAM':>5s}  {'Cost':>6s}  {'Limit':<16s}  {'Status':<12s}"
    )
    log("  " + "-" * 110)

    free_only = sorted(
        [(n, t) for n, t in tiers.items()],
        key=lambda x: (x[1]["cost_hr"], x[1]["provider"]),
    )

    for idx, (name, info) in enumerate(free_only, 1):
        artifacts_exist = any(
            a.get("exists", False)
            for a_key, a in artifacts.items()
            if a_key.startswith(name.rstrip("_train"))
        )

        status = info.get("status", "unknown")
        if status == "available":
            status_display = "✓ Available"
        elif status == "setup_available":
            if artifacts_exist:
                status_display = "✓ Generated"
            else:
                status_display = "○ Setup ready"
        elif status == "spend_limit_exceeded":
            status_display = "✗ Spend limit"
        else:
            status_display = f"? {status}"

        vram = str(info.get("vram_gb", "")) + "GB" if info.get("vram_gb") else "CPU"
        cost = f"${info['cost_hr']}/hr" if info["cost_hr"] > 0 else "Free"

        log(
            f"  {idx:>2d}  {name:<20s}  {info['provider']:<20s}  {info['gpu']:<24s}  "
            f"{vram:>5s}  {cost:>6s}  {info['limit']:<16s}  {status_display:<12s}"
        )

    log("  " + "-" * 110)
    total_free = sum(1 for t in tiers.values() if t["cost_hr"] == 0.0)
    total_paid = sum(1 for t in tiers.values() if t["cost_hr"] > 0.0)
    log(f"  Total tiers: {len(tiers)}  (Free: {total_free}  Paid: {total_paid})")
    log("")

    # ── Artifacts ─────────────────────────────────────────────────────
    log("  Generated Artifacts:")
    log(f"  {'Path':<50s}  {'Exists':>8s}  {'Size':>8s}  {'SHA-256 Sigil':<18s}")
    log("  " + "-" * 86)
    for a_key, a_info in artifacts.items():
        exists = "✓" if a_info["exists"] else "✗"
        size = f"{a_info['size_kb']}KB" if a_info["size_kb"] else "-"
        sigil = a_info["sigil"] if a_info["sigil"] else "-"
        log(f"  {a_info['path']:<50s}  {exists:>8s}  {size:>8s}  {sigil:<18s}")
    log("  " + "-" * 86)
    log("")

    # ── Setup Scripts ─────────────────────────────────────────────────
    if "setup_scripts_run" in report:
        log("  Setup Script Results:")
        log(f"  {'Script':<25s}  {'Status':>8s}  {'Time':>8s}")
        log("  " + "-" * 43)
        for s_key, s_info in report["setup_scripts_run"].items():
            status = "✓" if s_info["success"] else "✗"
            elapsed = f"{s_info['elapsed_s']}s"
            log(f"  {s_key:<25s}  {status:>8s}  {elapsed:>8s}")
        log("  " + "-" * 43)
        if report.get("all_setups_succeeded"):
            log("  All setup scripts completed successfully.")
        else:
            log("  Some setup scripts failed — check output above.")
        log("")

    # ── Swarm State ───────────────────────────────────────────────────
    swarm = report.get("swarm_state_summary", {})
    log("  Cumulative Swarm Metrics:")
    log(f"    Total runs:     {swarm.get('total_runs', 0)}")
    log(f"    Total cost:     ${swarm.get('total_cost', 0.0):.2f}")
    log(f"    Total savings:  ${swarm.get('total_savings', 0.0):.2f}")
    log("")

    # ── Cost Comparison ──────────────────────────────────────────────
    log("  Cost Comparison (60h/month):")
    log(f"  {'Tier':<25s}  {'Monthly Cost':>14s}  {'vs H100 Savings':>18s}")
    log("  " + "-" * 60)
    h100_rate = 3.50
    h100_monthly = h100_rate * 60
    for name, info in sorted(tiers.items(), key=lambda x: x[1]["cost_hr"]):
        monthly = info["cost_hr"] * 60
        savings = h100_monthly - monthly
        log(f"  {name:<25s}  ${monthly:>8.2f}/mo  ${savings:>12.2f}/mo")
    log("  " + "-" * 60)
    log(f"  {'H100 Baseline':<25s}  ${h100_monthly:>8.2f}/mo")
    log("")

    log(f"  Report saved: {STATUS_OUTPUT}")
    log(f"  Sigil:        {report['sigil']}")
    log("=" * 90)
    log("")


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="Master orchestrator for all free GPU tier setup scripts"
    )
    parser.add_argument("--skip-generate", action="store_true",
                        help="Skip running sub-generators, just produce status report")
    parser.add_argument("--output-dir", type=str, default=str(FREE_GPU_DIR),
                        help=f"Output directory (default: {FREE_GPU_DIR})")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    artifacts = check_generated_artifacts()

    setup_results = None
    if not args.skip_generate:
        log("Running tier setup scripts...")
        log("")
        setup_results = run_setup_scripts()
        log("")

        # Re-check artifacts after generation
        artifacts = check_generated_artifacts()
    else:
        log("Skipping sub-generator execution (--skip-generate)")
        log("")

    report = build_status_report(setup_results, artifacts, not args.skip_generate)

    # Write status report
    status_path = output_dir / "all_tiers_status.json"
    status_path.write_text(json.dumps(report, indent=2))
    print(f"Status report written to {status_path}")

    print_table(report)

    if setup_results and not report.get("all_setups_succeeded"):
        log("WARNING: Some setup scripts failed. Check errors above.")
        log("You can re-run individual scripts:")
        log("  python3 free_gpu/setup_colab.py")
        log("  python3 free_gpu/setup_lightning.py")
        log("  python3 free_gpu/setup_hf_spaces.py")
        log("  python3 free_gpu/setup_gradient.py")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
