#!/usr/bin/env python3
"""mlx_distributed_launcher.py — Phase 5: MLX distributed launcher (mlx.launch + hostfile).

Apple MLX Distributed (WWDC 2026, July 30):
- RDMA over Thunderbolt 5 for distributed ML across multiple Macs
- Apple demoed 4× M3 Ultra Macs running 1 trillion parameter Kimi 2.6
- 3× speedup on fine-tuning vs single machine
- Single M3 Ultra: ~180 tok/s training → Cluster: ~600 tok/s

Our hardware:
- M4 MacBook Air (16GB unified memory, ~13GB usable) — this machine
- M2 Mac (8GB unified memory) — offline, will be online when connected

The hostfile lists machines available for distributed training:
- mlx.launch automatically shards the model across machines
- Tensor parallelism by default. Add --pipeline for pipeline parallelism.

Usage:
    python3 mlx_distributed_launcher.py --hostfile hosts.txt --model mlx-community/Qwen3-30B-A3B-4bit
    python3 mlx_distributed_launcher.py --hosts m2.local,m4.local --probe
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

DEPLOY2 = Path("/Users/nicholas/clawd/csoai-static-deploy2")
OUT = DEPLOY2 / "mlx_cluster" / "launcher_status.json"


def detect_local_node():
    """Detect this Mac's network address."""
    try:
        # Get hostname
        hostname = subprocess.run(["hostname"], capture_output=True, text=True, timeout=5).stdout.strip()
        # Get IP
        ip = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True, text=True, timeout=5).stdout.strip()
        return {
            "hostname": hostname,
            "ip": ip,
            "role": "controller",
            "memory_gb": 17.2,
            "usable_gb": 13.2,
        }
    except Exception as e:
        return {"error": str(e)}


def write_hostfile(hosts, path: Path) -> dict:
    """Write the mlx.launch hostfile."""
    path.write_text("\n".join(hosts) + "\n")
    return {
        "path": str(path),
        "hosts": hosts,
        "count": len(hosts),
    }


def probe_host(host: str) -> dict:
    """Probe a remote host (placeholder until SSH configured)."""
    return {
        "host": host,
        "reachable": False,
        "note": "M2 Mac is offline. Will be probed when connected to same network.",
        "expected": {
            "memory_gb": 8,
            "usable_gb": 4,
            "mlx_installed": "(verify when online)",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostfile", type=Path, help="Path to hostfile (overrides --hosts)")
    parser.add_argument("--hosts", help="Comma-separated hosts")
    parser.add_argument("--probe", action="store_true", help="Probe each host")
    parser.add_argument("--model", default="mlx-community/Qwen3-30B-A3B-4bit", help="Model to launch")
    args = parser.parse_args()
    
    print("=== MLX Distributed Launcher (Phase 5) ===\n")
    
    status = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reference": "Apple WWDC 2026 — Explore distributed inference and training with MLX",
        "published": "2026-07-30",
    }
    
    # Local node detection
    local = detect_local_node()
    status["local_node"] = local
    print(f"Local node: {local}")
    print()
    
    # Hosts
    hosts = []
    if args.hostfile:
        hosts = [h.strip() for h in args.hostfile.read_text().splitlines() if h.strip()]
        print(f"Hostfile: {args.hostfile}")
        print(f"Hosts: {hosts}")
    elif args.hosts:
        hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
        hostfile = Path("/Users/nicholas/clawd/csoai-static-deploy2/mlx_cluster/hosts.txt")
        result = write_hostfile(hosts, hostfile)
        status["hostfile"] = result
        print(f"Hosts: {hosts}")
        print(f"Written to: {hostfile}")
    else:
        hosts = [local.get("hostname", "localhost"), "m2-mac.local"]  # default
        hostfile = Path("/Users/nicholas/clawd/csoai-static-deploy2/mlx_cluster/hosts.txt")
        result = write_hostfile(hosts, hostfile)
        status["hostfile"] = result
        print(f"Default hosts (M4 + M2): {hosts}")
        print(f"Written to: {hostfile}")
    print()
    
    # Probe hosts
    if args.probe:
        print("Probing hosts:")
        probes = []
        for h in hosts:
            p = probe_host(h)
            probes.append(p)
            print(f"  {h}: {p['reachable']} — {p.get('note', '')}")
        status["probes"] = probes
        print()
    
    # Launch instructions
    if not args.probe:
        print("Launch command (when both Macs are online):")
        print(f"  mlx.launch --hostfile mlx_cluster/hosts.txt \\")
        print(f"    python -m mlx_lm.server \\")
        print(f"    --model {args.model} \\")
        print(f"    --port 8080")
        print()
        print("Or for fine-tuning:")
        print(f"  mlx.launch --hostfile mlx_cluster/hosts.txt \\")
        print(f"    python -m mlx_lm.lora \\")
        print(f"    --model {args.model} \\")
        print(f"    --train-data sov_training_data.jsonl \\")
        print(f"    --iters 1000 \\")
        print(f"    --batch-size 4 \\")
        print(f"    --lora-ranks 16")
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(status, indent=2))
    print(f"\n-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())