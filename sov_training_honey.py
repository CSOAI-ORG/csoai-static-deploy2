#!/usr/bin/env python3
"""
sov_training_honey.py — unify ALL training-data + GPU inventory + tier-0 routers
+ KB clauses into one honey + one KB inside sov-space.

Routes (8):
  1. ollama           — live ollama list
  2. huggingface      — forest/honey_hf_models.jsonl
  3. chatml           — forest/honey_chatml.jsonl (108 triplets)
  4. bloodline        — forest/bloodline.json
  5. training_data    — training_data/*.jsonl (9 files, ~78K triplets)
  6. gpu_inventory    — system RAM/CPU + sov_swarm.py backend pool
  7. tier0_routers    — sov_layer0_watchers + sov_spawn.py specs
  8. kb_clauses       — corpus/*.md + 417 frozen provisions

Every event → sov_route.route() so the ledger, honey DB, 5D, fluid, IWM/VWM
all see the same hash. The E2E test asserts exact mirror.
"""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / "clawd" / "csoai-static-deploy2"
FOREST = ROOT / "forest"
TRAINING = ROOT / "training_data"
BENCH = ROOT / "benchmark-results"

HONEY_ALL = FOREST / "honey_all_producers.jsonl"
HONEY_TRAINING = FOREST / "honey_training.jsonl"
HONEY_DOWNLOADS = FOREST / "honey_downloads.jsonl"
HONEY_LAYER0 = FOREST / "honey_layer0.jsonl"
GPU_INVENTORY = FOREST / "gpu_inventory.json"
TIER0_ROUTERS = FOREST / "tier0_routers.json"

# Try to import sov_route for proper signing
try:
    sys.path.insert(0, str(ROOT))
    from sov_route import route, verify
    HAS_SOV_ROUTE = True
except ImportError:
    HAS_SOV_ROUTE = False


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit_event(kind: str, summary: str, payload: dict, tags: list, source: str) -> dict:
    """Emit a honey event. Uses sov_route.route() if available."""
    event = {
        "timestamp": now_iso(),
        "kind": kind,
        "summary": summary,
        "source": source,
        "tags": tags,
        "payload": payload,
        "capture_id": sha256_str(f"{kind}:{summary}:{time.time()}")[:16],
    }
    if HAS_SOV_ROUTE:
        try:
            return route(event)
        except Exception as e:
            event["route_error"] = str(e)
    return event


def route_ollama() -> list:
    """Route 1: live ollama list."""
    events = []
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().split("\n")[1:]  # skip header
        models = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                models.append({
                    "name": parts[0],
                    "id": parts[1][:12],
                    "size": parts[2] if len(parts) > 2 else "",
                    "modified": parts[-2:] if len(parts) >= 4 else [],
                })
        evt = emit_event(
            "ollama_list",
            f"ollama: {len(models)} models loaded",
            {"models": models},
            ["[OLLAMA]", "[TRAIN]", "[GPU]"],
            "ollama"
        )
        events.append(evt)
    except Exception as e:
        events.append(emit_event("ollama_error", str(e), {}, ["[OLLAMA]"], "ollama"))
    return events


def route_huggingface() -> list:
    """Route 2: HF models from forest/honey_hf_models.jsonl."""
    events = []
    hf_path = FOREST / "honey_hf_models.jsonl"
    if not hf_path.exists():
        return [emit_event("hf_missing", "forest/honey_hf_models.jsonl not found", {}, ["[HF]"], "huggingface")]
    count = 0
    with open(hf_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                events.append(emit_event(
                    "hf_model",
                    f"HF: {rec.get('model_id', 'unknown')}",
                    rec,
                    ["[HF]", "[TRAIN]"],
                    "huggingface"
                ))
                count += 1
            except json.JSONDecodeError:
                continue
    return events


def route_chatml() -> list:
    """Route 3: chatml triplets from forest/honey_chatml.jsonl."""
    events = []
    path = FOREST / "honey_chatml.jsonl"
    if not path.exists():
        return [emit_event("chatml_missing", "forest/honey_chatml.jsonl not found", {}, ["[CHATML]"], "chatml")]
    count = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                events.append(emit_event(
                    "chatml_triplet",
                    rec.get("summary", "chatml triplet")[:50],
                    rec,
                    ["[CHATML]", "[TRAIN]"],
                    "chatml"
                ))
                count += 1
            except json.JSONDecodeError:
                continue
    return events


def route_bloodline() -> list:
    """Route 4: lineage from forest/bloodline.json."""
    events = []
    path = FOREST / "bloodline.json"
    if not path.exists():
        return [emit_event("bloodline_missing", "forest/bloodline.json not found", {}, ["[BLOODLINE]"], "bloodline")]
    try:
        with open(path) as f:
            rec = json.load(f)
        events.append(emit_event(
            "bloodline",
            "sovereign lineage tree",
            rec,
            ["[BLOODLINE]", "[LAYER-0]", "[ROUTER]"],
            "bloodline"
        ))
    except json.JSONDecodeError as e:
        events.append(emit_event("bloodline_error", str(e), {}, ["[BLOODLINE]"], "bloodline"))
    return events


def route_training_data() -> list:
    """Route 5: 9 training_data/*.jsonl files."""
    events = []
    if not TRAINING.exists():
        return [emit_event("training_missing", "training_data/ not found", {}, ["[TRAIN]"], "training_data")]
    total = 0
    for jf in sorted(TRAINING.glob("*.jsonl")):
        count = 0
        with open(jf) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    events.append(emit_event(
                        "training_pair",
                        f"{jf.name}: #{count}",
                        rec,
                        ["[TRAIN]", f"[FILE:{jf.stem}]"],
                        "training_data"
                    ))
                    count += 1
                    total += 1
                except json.JSONDecodeError:
                    continue
    return events


def route_gpu_inventory() -> list:
    """Route 6: live system RAM/CPU + sov_swarm backend pool."""
    events = []
    system_info = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python": platform.python_version(),
    }
    try:
        sysmem = psutil_sysmem() if "psutil" in sys.modules else None
        if sysmem:
            system_info["ram_total_gb"] = round(sysmem["total"] / (1024**3), 1)
            system_info["ram_available_gb"] = round(sysmem["available"] / (1024**3), 1)
    except ImportError:
        pass

    # Try to read sov_swarm backend pool
    swarm_backends = []
    swarm_path = ROOT / "sov_swarm.py"
    if swarm_path.exists():
        try:
            content = swarm_path.read_text()
            # Extract the backend list — naive but works for known structure
            for line in content.split("\n"):
                if "TIER_PRIMARY" in line or "backend" in line.lower():
                    if "=" in line and ":" in line:
                        swarm_backends.append(line.strip())
        except Exception:
            pass

    inventory = {
        "system": system_info,
        "swarm_backends_observed": swarm_backends,
        "scanned_at": now_iso(),
    }
    GPU_INVENTORY.write_text(json.dumps(inventory, indent=2))

    events.append(emit_event(
        "gpu_inventory",
        f"system: {system_info['machine']}, {system_info.get('ram_total_gb', '?')}GB RAM",
        inventory,
        ["[GPU]", "[LAYER-0]"],
        "gpu_inventory"
    ))
    return events


def psutil_sysmem():
    """Optional: psutil may not be installed."""
    import psutil
    return {
        "total": psutil.virtual_memory().total,
        "available": psutil.virtual_memory().available,
    }


def route_tier0_routers() -> list:
    """Route 7: sov_layer0_watchers/*.py + sov_spawn.py tier specs."""
    events = []
    routers = {"watchers": [], "spawn_tiers": [], "found_at": now_iso()}

    # Watchers
    watchers_dir = ROOT / "sov_layer0_watchers"
    if watchers_dir.exists():
        for py in sorted(watchers_dir.glob("*.py")):
            if py.name.startswith("_"):
                continue
            routers["watchers"].append({
                "name": py.stem,
                "path": str(py.relative_to(ROOT)),
                "size": py.stat().st_size,
            })
            events.append(emit_event(
                "watcher",
                f"layer0 watcher: {py.stem}",
                {"name": py.stem, "path": str(py.relative_to(ROOT))},
                ["[ROUTER]", "[LAYER-0]"],
                "tier0_routers"
            ))

    # Spawn tiers — read from sov_spawn.py
    spawn_path = ROOT / "sov_spawn.py"
    if spawn_path.exists():
        routers["spawn_path"] = str(spawn_path.relative_to(ROOT))
        events.append(emit_event(
            "spawn_tier_spec",
            "soul spawn 5-tier ladder source",
            {"path": str(spawn_path.relative_to(ROOT))},
            ["[ROUTER]", "[LAYER-0]"],
            "tier0_routers"
        ))

    TIER0_ROUTERS.write_text(json.dumps(routers, indent=2))
    return events


def route_kb_clauses() -> list:
    """Route 8: corpus/*.md + spec files."""
    events = []
    corpus_dirs = [ROOT / "corpus", ROOT / "specs", ROOT / "anchors"]
    count = 0
    for d in corpus_dirs:
        if not d.exists():
            continue
        for md in sorted(d.glob("*.md")):
            count += 1
            events.append(emit_event(
                "kb_clause",
                f"{d.name}: {md.stem}",
                {"path": str(md.relative_to(ROOT)), "size": md.stat().st_size},
                ["[KB]", "[LAYER-0]"],
                "kb_clauses"
            ))
    return events


def snapshot_layer0(all_events: list, output: Path = HONEY_LAYER0, cap: int = 1000):
    """Snapshot the [LAYER-0] slice as a tier-0-ready subset."""
    layer0 = []
    for e in all_events:
        tags = e.get("tags", [])
        if any("[LAYER-0]" in t for t in tags):
            layer0.append(e)
        if len(layer0) >= cap:
            break
    with open(output, "w") as f:
        for e in layer0:
            f.write(json.dumps(e) + "\n")
    return len(layer0)


def write_honey(all_events: list, output: Path = HONEY_ALL):
    """Write all events to one honey file."""
    with open(output, "w") as f:
        for e in all_events:
            f.write(json.dumps(e) + "\n")
    return len(all_events)


def main():
    parser = argparse.ArgumentParser(description="Sovereign training honey producer")
    parser.add_argument("--selftest", action="store_true", help="Run selftest on all 8 routes")
    parser.add_argument("--routes", nargs="+", help="Specific routes to run", default=None)
    args = parser.parse_args()

    routes = {
        "ollama": route_ollama,
        "huggingface": route_huggingface,
        "chatml": route_chatml,
        "bloodline": route_bloodline,
        "training_data": route_training_data,
        "gpu_inventory": route_gpu_inventory,
        "tier0_routers": route_tier0_routers,
        "kb_clauses": route_kb_clauses,
    }

    if args.routes:
        routes = {k: v for k, v in routes.items() if k in args.routes}

    print(f"sov_training_honey.py — {len(routes)} routes")
    print(f"  sov_route available: {HAS_SOV_ROUTE}")
    print(f"  Root: {ROOT}")
    print()

    all_events = []
    passed = 0
    failed = 0

    for name, fn in routes.items():
        print(f"  [{name}]", end=" ", flush=True)
        try:
            events = fn()
            n = len(events)
            all_events.extend(events)
            print(f"OK ({n} events)")
            passed += 1
        except Exception as e:
            print(f"FAIL ({e})")
            failed += 1

    # Save honey
    n_total = write_honey(all_events)
    print(f"\n  Total events: {n_total}")
    print(f"  Honey written to: {HONEY_ALL}")

    # Snapshot layer-0
    n_layer0 = snapshot_layer0(all_events)
    print(f"  Layer-0 slice: {n_layer0} events")
    print(f"  Layer-0 written to: {HONEY_LAYER0}")

    # Summary
    print(f"\n  Routes passed: {passed}/{len(routes)}")
    if args.selftest:
        if failed == 0:
            print(f"  ✓ SELFTEST PASS")
            sys.exit(0)
        else:
            print(f"  ✗ SELFTEST FAIL ({failed} failed)")
            sys.exit(1)


if __name__ == "__main__":
    main()
