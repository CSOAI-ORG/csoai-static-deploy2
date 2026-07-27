"""SOV master agent runner with full parallel swarm against the live H100 model forest."""
import argparse
import base64
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from sov_master import SOVMaster
from sov_master_scenarios import (
    J_SPACE_QUERIES,
    SOV_SPACE_QUERIES,
    GAME_PROMPTS,
    MASTER_TASKS,
)


def fixture_b64(name):
    if not name:
        return None
    path = ROOT / "benchmark-results" / "capability-results" / "fixtures" / f"{name}.png"
    if not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode()


def build_capability_registry():
    with (ROOT / "benchmark-results" / "capability_registry.json").open() as handle:
        return json.load(handle)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ollama-url", default=os.environ.get("SOV_OLLAMA_URL", "http://127.0.0.1:11434"))
    parser.add_argument("--output", type=Path, default=ROOT / "benchmark-results" / "sov-master-honey.json")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args()
    master = SOVMaster(base_url=args.ollama_url)
    registry = build_capability_registry()
    capability_registry = {
        "capabilities": {
            **registry["capabilities"],
            **{capability: {"modality": "text", "tasks": tasks} for capability, tasks in MASTER_TASKS.items()},
        }
    }
    started = time.monotonic()
    summary = master.run_honey_stage(capability_registry, J_SPACE_QUERIES, SOV_SPACE_QUERIES, GAME_PROMPTS)
    summary["master_description"] = master.describe()
    summary["elapsed_s"] = round(time.monotonic() - started, 2)
    master.bake_honey(summary)
    if args.print:
        print(json.dumps(summary, indent=2, ensure_ascii=False)[:5000])
    return summary


if __name__ == "__main__":
    main()
