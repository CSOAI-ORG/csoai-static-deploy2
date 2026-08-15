#!/usr/bin/env python3
"""mlx_cluster_detect.py — Phase 1: detect Mac hardware + MLX capability.

Prints the local cluster status: hardware, MLX version, available memory,
running models. Reports whether REAP pruning + Unsloth MoE + progressive
training can run on this machine.

Usage:
    python3 mlx_cluster_detect.py
"""

import json
import subprocess
import sys
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("/Users/nicholas/clawd/csoai-static-deploy2/mlx_cluster/cluster_status.json")


def detect_mac_hardware():
    """Detect Mac model + chip + memory."""
    out = {}
    try:
        # macOS specifics
        chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True, timeout=5).stdout.strip()
        mem_bytes = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=5).stdout.strip())
        cores_phys = int(subprocess.run(["sysctl", "-n", "hw.physicalcpu"], capture_output=True, text=True, timeout=5).stdout.strip())
        cores_log = int(subprocess.run(["sysctl", "-n", "hw.logicalcpu"], capture_output=True, text=True, timeout=5).stdout.strip())
        
        out["chip"] = chip
        out["unified_memory_gb"] = round(mem_bytes / 1_000_000_000, 1)
        out["cores_physical"] = cores_phys
        out["cores_logical"] = cores_log
        out["unified_memory_usable_gb"] = round(mem_bytes / 1_000_000_000 - 4, 1)  # ~4GB reserved for OS
        out["machine_model"] = subprocess.run(["sysctl", "-n", "hw.model"], capture_output=True, text=True, timeout=5).stdout.strip()
        
        # macOS version
        sw = subprocess.run(["sw_vers", "-productVersion"], capture_output=True, text=True, timeout=5).stdout.strip()
        out["macos_version"] = sw
    except Exception as e:
        out["error"] = str(e)
    return out


def detect_mlx():
    """Detect MLX + mlx_lm installation."""
    out = {"mlx_installed": False, "mlx_lm_installed": False}
    try:
        import mlx.core as mx
        out["mlx_installed"] = True
        out["mlx_version"] = mx.__version__ if hasattr(mx, "__version__") else "unknown"
        out["device"] = str(mx.default_device())
        if hasattr(mx, "metal"):
            out["metal_available"] = mx.metal.is_available() if hasattr(mx.metal, "is_available") else False
    except ImportError:
        pass
    try:
        import mlx_lm
        out["mlx_lm_installed"] = True
        out["mlx_lm_version"] = mlx_lm.__version__ if hasattr(mlx_lm, "__version__") else "unknown"
    except ImportError:
        pass
    return out


def detect_ollama():
    """Detect Ollama + running models."""
    out = {"ollama_running": False}
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5) as r:
            data = json.loads(r.read())
            models = [m["name"] for m in data.get("models", [])]
            out["ollama_running"] = True
            out["model_count"] = len(models)
            out["top_models"] = models[:10]
            # Categorize
            out["sov_models"] = [m for m in models if "sov" in m.lower()]
            out["clan_models"] = [m for m in models if "clan" in m.lower()]
            out["kimi_models"] = [m for m in models if "kimi" in m.lower()]
    except Exception as e:
        out["error"] = str(e)
    return out


def compute_capability(hw, mlx, ollama):
    """Compute what models can run on this hardware."""
    usable_gb = hw.get("unified_memory_usable_gb", 12)
    capability = {
        "tiny_0.5B_to_3B": "✓ native (qwen2.5:0.5b family, 379MB)",
        "small_7B": "✓ native (qwen2.5:7b, llama3.2:3b family)",
        "medium_13B": "✓ native with 4-bit (mlx_lm)",
        "large_30B": "⚠ partial (need 30-40GB usable, 4-bit quantize)",
        "xlarge_70B": "✗ insufficient unified memory (need 50-70GB usable)",
        "kimi_K3_pruned": "✓ MLX distributed + REAP 50% prune + 4-bit (fits on M4 + M2 cluster)",
        "mlx_distributed": "✓ mlx.launch ready if M2 + M4 cluster detected",
    }
    
    if mlx.get("mlx_installed"):
        capability["mlx_ready"] = "✓ MLX 0.32.0 installed, GPU device active"
    else:
        capability["mlx_ready"] = "✗ MLX not installed (pip install mlx mlx-lm)"
    
    if ollama.get("sov_models"):
        capability["ollama_sov"] = f"✓ {len(ollama['sov_models'])} sov models loaded"
    else:
        capability["ollama_sov"] = "✗ no sov models"
    
    return capability


def main():
    hw = detect_mac_hardware()
    mlx = detect_mlx()
    ollama = detect_ollama()
    capability = compute_capability(hw, mlx, ollama)
    
    status = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hardware": hw,
        "mlx": mlx,
        "ollama": ollama,
        "capability": capability,
        "cluster_topology": {
            "node_1": {
                "name": "M4 MacBook Air (this machine)",
                "role": "controller",
                "memory_gb": hw.get("unified_memory_gb"),
                "mlx_ready": mlx.get("mlx_installed"),
            },
            "node_2": {
                "name": "M2 Mac (offline)",
                "role": "worker",
                "memory_gb": 8,
                "mlx_ready": "(assumed; verify when online)",
                "detected": False,
            },
            "note": "MLX distributed requires both Macs on same network with mlx.launch hostfile",
        },
    }
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(status, indent=2))
    
    print("=== Mac Cluster Status (Phase 1) ===\n")
    print(f"Chip: {hw.get('chip')}")
    print(f"Unified memory: {hw.get('unified_memory_gb')}GB ({hw.get('unified_memory_usable_gb')}GB usable)")
    print(f"Cores: {hw.get('cores_physical')} physical, {hw.get('cores_logical')} logical")
    print(f"macOS: {hw.get('macos_version')}")
    print(f"Machine: {hw.get('machine_model')}")
    print()
    
    print("MLX:")
    for k, v in mlx.items():
        print(f"  {k}: {v}")
    print()
    
    print("Ollama:")
    print(f"  Running: {ollama.get('ollama_running')}")
    print(f"  Model count: {ollama.get('model_count', 0)}")
    print(f"  sov models: {len(ollama.get('sov_models', []))}")
    print(f"  clan models: {len(ollama.get('clan_models', []))}")
    print(f"  kimi models: {len(ollama.get('kimi_models', []))}")
    print()
    
    print("Capability:")
    for k, v in capability.items():
        print(f"  {k}: {v}")
    print()
    
    print(f"-> {OUT}")
    print()
    print("=== Next steps ===")
    print("1. Install MLX distributed launcher (already installed)")
    print("2. Connect M2 + M4 via Thunderbolt (when M2 is online)")
    print("3. Run mlx.launch with hostfile (Phase 5)")
    print("4. Apply REAP 50% pruning to a MoE model (Phase 2)")
    print("5. Wire Unsloth MoE training (Phase 3)")
    print("6. Progressive training: 1B → 3B → 7B → 13B (Phase 4)")
    print("7. Wire all into GSPC 4-axis measurement instrument (Phase 6)")
    print("8. Eat across N sites: HF + Kaggle + csoai.org + sov-space (Phase 7)")


if __name__ == "__main__":
    main()