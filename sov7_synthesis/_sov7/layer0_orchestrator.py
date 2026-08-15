#!/usr/bin/env python3
"""SOV Layer 0 — Free GPU Orchestrator

Master router that sends tasks to the cheapest/fastest free resource.
Routes: simple Q&A → Oracle, reasoning → Groq, inference → Cloudflare,
training → Kaggle/Modal, backup → OpenRouter/NVIDIA.

Zero-cost primary with paid fallback chain.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "layer0_results.json"
STATS_PATH = ROOT / "layer0_stats.json"

# ─── Task Types ──────────────────────────────────────────────────────────────

class TaskType(str, Enum):
    SIMPLE_QA = "simple_qa"
    REASONING = "reasoning"
    INFERENCE = "inference"
    TRAINING = "training"
    BACKUP = "backup"


# ─── Resource Definitions ────────────────────────────────────────────────────

@dataclass
class Resource:
    id: str
    name: str
    kind: str            # cpu | gpu | api
    provider: str
    model: str
    cost: float          # per-call or per-hour in USD
    cost_label: str
    daily_limit: int     # 0 = unlimited
    latency_ms: int      # typical latency
    good_for: List[str]  # task types this resource handles
    endpoint: str
    api_key_env: str     # env var name for API key
    api_key_file: str    # fallback file path
    headers: Dict[str, str] = field(default_factory=dict)
    payload_fn: str = "" # name of payload builder method
    parse_fn: str = ""   # name of response parser method
    status: str = "active"
    priority: int = 0    # lower = preferred


RESOURCES: Dict[str, Resource] = {
    "oracle_arm": Resource(
        id="oracle_arm",
        name="Oracle ARM (sov33-evolved)",
        kind="cpu",
        provider="oracle",
        model="sov33-evolved",
        cost=0.0,
        cost_label="$0",
        daily_limit=0,
        latency_ms=3000,
        good_for=[TaskType.SIMPLE_QA],
        endpoint="",  # local inference, no API
        api_key_env="",
        api_key_file="",
        priority=0,
    ),
    "groq": Resource(
        id="groq",
        name="Groq llama-3.3-70b",
        kind="api",
        provider="groq",
        model="llama-3.3-70b-versatile",
        cost=0.0,
        cost_label="$0 (100K tok/day)",
        daily_limit=100_000,
        latency_ms=800,
        good_for=[TaskType.REASONING, TaskType.SIMPLE_QA],
        endpoint="https://api.groq.com/openai/v1/chat/completions",
        api_key_env="GROQ_API_KEY",
        api_key_file="~/.groq/api_key",
        priority=1,
    ),
    "cloudflare": Resource(
        id="cloudflare",
        name="Cloudflare Workers AI",
        kind="api",
        provider="cloudflare",
        model="@cf/meta/llama-3.3-70b-instruct-fp8",
        cost=0.0,
        cost_label="$0 (10K neurons/day)",
        daily_limit=10_000,
        latency_ms=1200,
        good_for=[TaskType.INFERENCE, TaskType.REASONING],
        endpoint="https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{model}",
        api_key_env="CLOUDFLARE_API_TOKEN",
        api_key_file="~/.cloudflare/api_token",
        headers={"Authorization": "Bearer {api_key}"},
        priority=2,
    ),
    "openrouter": Resource(
        id="openrouter",
        name="OpenRouter (free models)",
        kind="api",
        provider="openrouter",
        model="meta-llama/llama-3.3-70b-instruct:free",
        cost=0.0,
        cost_label="$0 (50 req/day)",
        daily_limit=50,
        latency_ms=2000,
        good_for=[TaskType.BACKUP, TaskType.REASONING, TaskType.SIMPLE_QA],
        endpoint="https://openrouter.ai/api/v1/chat/completions",
        api_key_env="OPENROUTER_API_KEY",
        api_key_file="~/.openrouter/api_key",
        priority=5,
    ),
    "nvidia": Resource(
        id="nvidia",
        name="NVIDIA Build (free tier)",
        kind="api",
        provider="nvidia",
        model="meta/llama-3.1-8b-instruct",
        cost=0.0,
        cost_label="$0 (1000 calls/day)",
        daily_limit=1000,
        latency_ms=1500,
        good_for=[TaskType.BACKUP, TaskType.INFERENCE],
        endpoint="https://integrate.api.nvidia.com/v1/chat/completions",
        api_key_env="NVIDIA_API_KEY",
        api_key_file="~/.nvidia/api_key",
        priority=6,
    ),
    "kaggle_t4": Resource(
        id="kaggle_t4",
        name="Kaggle T4 GPU",
        kind="gpu",
        provider="kaggle",
        model="T4 16GB",
        cost=0.0,
        cost_label="$0 (30h/week)",
        daily_limit=0,
        latency_ms=14400000,  # ~4 hours
        good_for=[TaskType.TRAINING],
        endpoint="",
        api_key_env="KAGGLE_USERNAME",
        api_key_file="~/.kaggle/kaggle.json",
        priority=3,
    ),
    "modal": Resource(
        id="modal",
        name="Modal ($30/mo free credit)",
        kind="gpu",
        provider="modal",
        model="A10G 24GB",
        cost=0.0,
        cost_label="$0 ($30 credit/mo)",
        daily_limit=0,
        latency_ms=3600000,  # ~1 hour
        good_for=[TaskType.TRAINING, TaskType.INFERENCE],
        endpoint="",
        api_key_env="MODAL_TOKEN_ID",
        api_key_file="~/.modal/token.json",
        priority=4,
    ),
}


# ─── Routing Table ───────────────────────────────────────────────────────────

ROUTING_TABLE: Dict[str, List[str]] = {
    TaskType.SIMPLE_QA:  ["oracle_arm", "groq", "openrouter", "nvidia"],
    TaskType.REASONING:  ["groq", "cloudflare", "openrouter", "nvidia"],
    TaskType.INFERENCE:  ["cloudflare", "groq", "openrouter", "nvidia"],
    TaskType.TRAINING:   ["kaggle_t4", "modal"],
    TaskType.BACKUP:     ["openrouter", "nvidia", "groq", "cloudflare"],
}


# ─── Keyword-based Task Classifier ───────────────────────────────────────────

CLASSIFIER_KEYWORDS: Dict[str, List[str]] = {
    TaskType.SIMPLE_QA: [
        "what is", "who is", "define", "explain", "tell me",
        "how many", "when did", "where is", "which",
    ],
    TaskType.REASONING: [
        "reason", "analyze", "compare", "contrast", "evaluate",
        "argue", "debate", "logic", "prove", "infer", "implications",
        "trade-off", "pros and cons", "ethical", "philosophy",
    ],
    TaskType.INFERENCE: [
        "generate", "create", "write", "produce", "compose",
        "summarize", "translate", "classify", "extract", "parse",
        "code", "program", "function", "algorithm",
    ],
    TaskType.TRAINING: [
        "train", "fine-tune", "finetune", "lora", "dataset",
        "benchmark", "evaluate model", "epoch", "gradient",
    ],
}


def classify_task(task: str) -> str:
    """Classify a task string into a TaskType using keyword matching."""
    lower = task.lower()
    scores: Dict[str, int] = defaultdict(int)
    for task_type, keywords in CLASSIFIER_KEYWORDS.items():
        for kw in keywords:
            if kw in lower:
                scores[task_type] += 1
    if not scores:
        return TaskType.SIMPLE_QA
    return max(scores, key=scores.get)


# ─── API Key Resolution ─────────────────────────────────────────────────────

def resolve_api_key(resource: Resource) -> str:
    """Resolve API key from env var or file."""
    key = os.environ.get(resource.api_key_env, "")
    if key:
        return key
    if resource.api_key_file:
        path = Path(os.path.expanduser(resource.api_key_file))
        if path.exists():
            try:
                text = path.read_text().strip()
                if path.suffix == ".json":
                    data = json.loads(text)
                    return data.get("api_key", data.get("key", data.get("token", text)))
                return text
            except Exception:
                pass
    return ""


# ─── Callers (per-resource API call logic) ───────────────────────────────────

def call_oracle_arm(task: str, resource: Resource) -> Tuple[str, bool]:
    """Oracle ARM: local sov33-evolved inference via subprocess."""
    script = ROOT.parent / "sov_space" / "sandwich_brain.py"
    if not script.exists():
        # Fallback: try ollama if available
        try:
            r = subprocess.run(
                ["ollama", "run", "sov33", task],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip(), False
        except FileNotFoundError:
            pass
        return "[ORACLE_ARM] No local model available — deploy sov33-evolved to Oracle", True
    try:
        r = subprocess.run(
            [sys.executable, str(script), "--query", task],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip(), False
        return f"[ORACLE_ARM] Script failed: {r.stderr[:200]}", True
    except Exception as e:
        return f"[ORACLE_ARM] {e}", True


def call_openai_compat(task: str, resource: Resource, api_key: str) -> Tuple[str, bool]:
    """Generic OpenAI-compatible API call via curl."""
    endpoint = resource.endpoint
    if "{account}" in endpoint:
        account = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
        endpoint = endpoint.replace("{account}", account)

    payload = json.dumps({
        "model": resource.model,
        "messages": [{"role": "user", "content": task}],
        "temperature": 0.7,
        "max_tokens": 2048,
    })

    auth_header = f"Authorization: Bearer {api_key}"
    if resource.id == "openrouter":
        auth_header = f"Authorization: Bearer {api_key}"
    elif resource.id == "cloudflare":
        auth_header = f"Authorization: Bearer {api_key}"

    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "120", endpoint,
             "-H", auth_header,
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=125,
        )
        if r.returncode != 0:
            return f"[CURL_ERROR] {r.stderr[:200]}", True
        data = json.loads(r.stdout)
        if "error" in data:
            return json.dumps(data["error"]), True
        # OpenAI format
        if "choices" in data:
            return data["choices"][0]["message"]["content"], False
        # Cloudflare format
        if "result" in data and "response" in data["result"]:
            return data["result"]["response"], False
        return f"[UNEXPECTED] {r.stdout[:300]}", True
    except json.JSONDecodeError:
        return f"[JSON_ERROR] {r.stdout[:200]}", True
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] Request exceeded 120s", True
    except Exception as e:
        return f"[ERROR] {e}", True


def call_training(task: str, resource: Resource) -> Tuple[str, bool]:
    """Training resources: return status/availability info."""
    if resource.id == "kaggle_t4":
        kaggle_json = Path(os.path.expanduser("~/.kaggle/kaggle.json"))
        if not kaggle_json.exists():
            return "[KAGGLE] No ~/.kaggle/kaggle.json found — configure Kaggle API", True
        return (
            "[KAGGLE] Ready for training. Submit notebook via: "
            "kaggle kernels push -p <notebook-dir>\n"
            f"Task queued: {task[:100]}",
            False,
        )
    if resource.id == "modal":
        token = resolve_api_key(resource)
        if not token:
            return "[MODAL] No MODAL_TOKEN_ID found — run: modal token set", True
        return (
            "[MODAL] Ready for training. Deploy via: modal deploy <script>\n"
            f"Task queued: {task[:100]}",
            False,
        )
    return f"[TRAINING] Unknown resource: {resource.id}", True


def call_resource(task: str, resource: Resource) -> Tuple[str, bool]:
    """Dispatch to the correct caller based on resource kind."""
    if resource.id == "oracle_arm":
        return call_oracle_arm(task, resource)
    if resource.kind == "gpu":
        return call_training(task, resource)
    # All other API resources: openai-compatible
    api_key = resolve_api_key(resource)
    if not api_key:
        return f"[{resource.id.upper()}] No API key found (env: {resource.api_key_env})", True
    return call_openai_compat(task, resource, api_key)


# ─── Latency Tracking ───────────────────────────────────────────────────────

@dataclass
class ResourceStats:
    calls: int = 0
    successes: int = 0
    failures: int = 0
    total_latency_ms: float = 0.0
    total_cost: float = 0.0
    last_error: str = ""
    last_used: str = ""

    @property
    def success_rate(self) -> float:
        return self.successes / self.calls if self.calls else 0.0

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.calls if self.calls else 0.0


class StatsTracker:
    """Thread-safe per-resource statistics tracker."""

    def __init__(self):
        self._lock = threading.Lock()
        self._stats: Dict[str, ResourceStats] = defaultdict(ResourceStats)

    def record(self, resource_id: str, success: bool, latency_ms: float, cost: float = 0.0, error: str = ""):
        with self._lock:
            s = self._stats[resource_id]
            s.calls += 1
            if success:
                s.successes += 1
            else:
                s.failures += 1
                s.last_error = error
            s.total_latency_ms += latency_ms
            s.total_cost += cost
            s.last_used = datetime.now(timezone.utc).isoformat()

    def get(self, resource_id: str) -> ResourceStats:
        with self._lock:
            return self._stats[resource_id]

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {rid: asdict(s) for rid, s in self._stats.items()}

    def save(self, path: Path = STATS_PATH):
        path.write_text(json.dumps(self.snapshot(), indent=2))


# ─── Result Dataclass ───────────────────────────────────────────────────────

@dataclass
class TaskResult:
    task: str
    task_type: str
    route_mode: str          # auto | manual
    primary_resource: str
    response: str
    success: bool
    fallbacks_tried: List[str]
    final_resource: str
    latency_ms: float
    cost: float
    timestamp: str
    error: str = ""


# ─── Orchestrator ────────────────────────────────────────────────────────────

class Layer0Orchestrator:
    """Master router: classifies tasks, routes to cheapest resource, falls back on failure."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.stats = StatsTracker()
        self.results: List[TaskResult] = []

    def route(self, task: str, route: str = "auto", resource_override: str = "") -> TaskResult:
        """Route a single task. route='auto' classifies; route='manual' uses resource_override."""
        timestamp = datetime.now(timezone.utc).isoformat()

        if route == "manual" and resource_override:
            task_type = TaskType.SIMPLE_QA  # unknown when manual
            chain = [resource_override]
        else:
            task_type = classify_task(task)
            chain = list(ROUTING_TABLE.get(task_type, ROUTING_TABLE[TaskType.SIMPLE_QA]))

        primary = chain[0]
        fallbacks_tried: List[str] = []
        response = ""
        success = False
        final_resource = ""
        error = ""
        total_latency = 0.0

        for res_id in chain:
            resource = RESOURCES.get(res_id)
            if not resource:
                continue

            print(f"  → Trying {resource.name} ...")
            t0 = time.monotonic()
            resp, is_err = call_resource(task, resource)
            elapsed_ms = (time.monotonic() - t0) * 1000
            total_latency += elapsed_ms

            self.stats.record(res_id, not is_err, elapsed_ms, error=resp if is_err else "")

            if is_err:
                fallbacks_tried.append(res_id)
                print(f"    ✗ {resource.id}: {resp[:120]}")
                error = resp
                continue

            response = resp
            success = True
            final_resource = res_id
            print(f"    ✓ {resource.name} ({elapsed_ms:.0f}ms)")
            break

        if not success:
            final_resource = fallbacks_tried[-1] if fallbacks_tried else primary
            print(f"  ✗ All resources failed for: {task[:60]}")

        result = TaskResult(
            task=task,
            task_type=task_type if route == "auto" else "manual",
            route_mode=route,
            primary_resource=primary,
            response=response,
            success=success,
            fallbacks_tried=fallbacks_tried,
            final_resource=final_resource,
            latency_ms=total_latency,
            cost=0.0,
            timestamp=timestamp,
            error=error,
        )
        self.results.append(result)
        return result

    def route_parallel(self, tasks: List[str], route: str = "auto") -> List[TaskResult]:
        """Route multiple tasks in parallel."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.route, t, route): t for t in tasks}
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    task = futures[future]
                    results.append(TaskResult(
                        task=task, task_type="error", route_mode=route,
                        primary_resource="", response="", success=False,
                        fallbacks_tried=[], final_resource="",
                        latency_ms=0, cost=0,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        error=str(e),
                    ))
        return results

    def save_results(self, path: Path = RESULTS_PATH):
        data = [asdict(r) for r in self.results]
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return path

    def print_summary(self):
        total = len(self.results)
        ok = sum(1 for r in self.results if r.success)
        fail = total - ok
        total_latency = sum(r.latency_ms for r in self.results)

        print()
        print("═" * 60)
        print(f"  LAYER 0 ORCHESTRATOR — SUMMARY")
        print(f"  Tasks: {total}  Success: {ok}  Failed: {fail}")
        print(f"  Total latency: {total_latency:.0f}ms")
        print(f"  Avg latency:   {total_latency / total:.0f}ms" if total else "")
        print("═" * 60)

        if self.results:
            print()
            print("  Resource usage:")
            usage: Dict[str, int] = defaultdict(int)
            for r in self.results:
                usage[r.final_resource] += 1
            for res_id, count in sorted(usage.items(), key=lambda x: -x[1]):
                r = RESOURCES.get(res_id)
                name = r.name if r else res_id
                print(f"    {name:35s} {count} calls")

            print()
            print("  Fallback chains triggered:")
            for r in self.results:
                if r.fallbacks_tried:
                    chain_str = " → ".join(r.fallbacks_tried + [r.final_resource])
                    print(f"    [{r.task_type}] {chain_str}")

        # Stats snapshot
        print()
        print("  Per-resource stats:")
        for rid, snap in self.stats.snapshot().items():
            if snap["calls"] > 0:
                print(f"    {rid:20s}  calls={snap['calls']}  "
                      f"ok={snap['successes']}  "
                      f"rate={snap['success_rate']:.0%}  "
                      f"avg={snap['avg_latency_ms']:.0f}ms")


# ─── CLI ─────────────────────────────────────────────────────────────────────

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║  SOV LAYER 0 — FREE GPU ORCHESTRATOR                       ║
║  Cheapest route first. Fallback chain. Zero-cost primary.   ║
╚══════════════════════════════════════════════════════════════╝
"""


def print_resources():
    """Print available resources table."""
    print("\n  Available resources:")
    print(f"  {'ID':18s} {'Kind':5s} {'Cost':20s} {'Good for':30s}")
    print("  " + "─" * 75)
    for rid, r in RESOURCES.items():
        good_for = ", ".join(r.good_for) if isinstance(r.good_for[0], str) else ", ".join(r.good_for)
        print(f"  {r.id:18s} {r.kind:5s} {r.cost_label:20s} {good_for:30s}")


def print_routing_table():
    """Print the routing table."""
    print("\n  Routing table (priority order):")
    for task_type, chain in ROUTING_TABLE.items():
        names = [RESOURCES[r].name if r in RESOURCES else r for r in chain]
        print(f"    {task_type:12s} → {' → '.join(names)}")


def cmd_route(args):
    """Route a single task."""
    orch = Layer0Orchestrator(max_workers=args.parallel)

    print(BANNER)
    print_resources()
    print_routing_table()

    print(f"\n  Task: {args.task}")
    print(f"  Route mode: {args.route}")

    if args.route == "auto":
        task_type = classify_task(args.task)
        print(f"  Classified as: {task_type}")
    print()

    result = orch.route(args.task, route=args.route, resource_override=args.resource)

    print()
    print("─" * 60)
    print(f"  RESULT")
    print(f"  Success:   {result.success}")
    print(f"  Resource:  {result.final_resource}")
    print(f"  Latency:   {result.latency_ms:.0f}ms")
    if result.fallbacks_tried:
        print(f"  Fallbacks: {' → '.join(result.fallbacks_tried)}")
    print(f"  Response ({len(result.response)} chars):")
    print("─" * 60)
    # Truncate long responses for CLI display
    preview = result.response[:2000]
    if len(result.response) > 2000:
        preview += f"\n... [{len(result.response) - 2000} more chars]"
    print(preview)

    path = orch.save_results()
    orch.stats.save()
    orch.print_summary()
    print(f"\n  Results saved to: {path}")
    print(f"  Stats saved to:   {STATS_PATH}")


def cmd_batch(args):
    """Route multiple tasks from a file (one per line) or stdin."""
    orch = Layer0Orchestrator(max_workers=args.parallel)

    if args.file and args.file != "-":
        tasks = [line.strip() for line in Path(args.file).read_text().splitlines() if line.strip()]
    else:
        print("Enter tasks (one per line, Ctrl-D to finish):")
        tasks = [line.strip() for line in sys.stdin if line.strip()]

    if not tasks:
        print("No tasks provided.")
        sys.exit(1)

    print(BANNER)
    print(f"  Batch: {len(tasks)} tasks, route={args.route}, parallel={args.parallel}")
    print()

    results = orch.route_parallel(tasks, route=args.route)

    for r in results:
        status = "✓" if r.success else "✗"
        print(f"  {status} [{r.task_type:12s}] {r.final_resource:18s} {r.latency_ms:7.0f}ms  {r.task[:60]}")

    path = orch.save_results()
    orch.stats.save()
    orch.print_summary()
    print(f"\n  Results saved to: {path}")


def cmd_stats(args):
    """Show historical stats."""
    if STATS_PATH.exists():
        data = json.loads(STATS_PATH.read_text())
        print("\n  Historical resource stats:")
        for rid, snap in data.items():
            if snap["calls"] > 0:
                print(f"    {rid:20s}  calls={snap['calls']}  "
                      f"rate={snap['success_rate']:.0%}  "
                      f"avg={snap['avg_latency_ms']:.0f}ms  "
                      f"cost=${snap['total_cost']:.4f}")
    else:
        print("  No stats file yet. Run some tasks first.")


def cmd_list(args):
    """List resources and routing table."""
    print(BANNER)
    print_resources()
    print_routing_table()


def main():
    parser = argparse.ArgumentParser(
        description="SOV Layer 0 — Free GPU Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 layer0_orchestrator.py --task "What is EU AI Act?" --route auto
  python3 layer0_orchestrator.py --task "Analyze trade-offs of GDPR vs CCPA" --route auto
  python3 layer0_orchestrator.py --task "Write a sorting algorithm" --resource groq
  python3 layer0_orchestrator.py --batch --file tasks.txt --parallel 4
  python3 layer0_orchestrator.py --list
  python3 layer0_orchestrator.py --stats
""",
    )
    parser.add_argument("--task", "-t", help="Single task to route")
    parser.add_argument("--route", "-r", default="auto", choices=["auto", "manual"],
                        help="Routing mode: auto (classify) or manual (use --resource)")
    parser.add_argument("--resource", help="Force a specific resource ID (for manual mode)")
    parser.add_argument("--batch", "-b", action="store_true", help="Batch mode: read multiple tasks")
    parser.add_argument("--file", "-f", help="File with tasks (one per line), or '-' for stdin")
    parser.add_argument("--parallel", "-p", type=int, default=4, help="Max parallel workers (default: 4)")
    parser.add_argument("--list", "-l", action="store_true", help="List resources and routing table")
    parser.add_argument("--stats", "-s", action="store_true", help="Show historical stats")
    parser.add_argument("--output", "-o", help="Custom output path for results JSON")

    args = parser.parse_args()

    if args.output:
        global RESULTS_PATH, STATS_PATH
        RESULTS_PATH = Path(args.output)
        STATS_PATH = RESULTS_PATH.with_name(RESULTS_PATH.stem + "_stats.json")

    if args.list:
        cmd_list(args)
    elif args.stats:
        cmd_stats(args)
    elif args.batch:
        cmd_batch(args)
    elif args.task:
        cmd_route(args)
    else:
        parser.print_help()
        print("\n  Quick start:")
        print('    python3 layer0_orchestrator.py --task "What is EU AI Act?" --route auto')


if __name__ == "__main__":
    main()
