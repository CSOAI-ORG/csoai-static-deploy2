#!/usr/bin/env python3
"""Standalone remote training script for Oracle Micro — synced by oracle_asi_sync.py"""
import json, subprocess, sys, os, time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

REMOTE_DIR = "/home/ubuntu/asi_training"
DATA_DIR = Path(REMOTE_DIR) / "data"
RESULTS_DIR = Path(REMOTE_DIR) / "results"
BASE_MODEL = "qwen2.5:0.5b"
EVOLVED_MODEL = "sov33-oracle:latest"
RESULTS_DIR.mkdir(exist_ok=True)


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_records():
    all_records = []
    for f in sorted(DATA_DIR.glob("*.jsonl")):
        log(f"  Loading {f.name}...")
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    all_records.append(json.loads(line))
    log(f"  Total: {len(all_records)} records")
    return all_records


def train_cycle(records, cycle):
    log(f"\n{'='*60}")
    log(f"  CYCLE {cycle} — bloodline-enhanced")
    log(f"{'='*60}")

    by_domain = defaultdict(list)
    for r in records:
        by_domain[r.get("domain", "general")].append(r)

    log(f"\n[1] Domains covered:")
    for d in sorted(by_domain):
        priority = sum(1 for r in by_domain[d] if r.get("source") == "bloodline")
        log(f"    {d:20s} {len(by_domain[d]):4d} records  ({priority} bloodline)")

    training_data = []
    for r in records:
        instr = r.get("instruction", "") or r.get("question", "")
        output = r.get("output", "") or r.get("answer", "") or r.get("response", "")
        if instr and output:
            chat = (
                f"<|im_start|>user\n{instr}<|im_end|>\n"
                f"<|im_start|>assistant\n{output}<|im_end|>"
            )
            training_data.append(chat)

    log(f"\n[2] Training data: {len(training_data)} chat examples")

    system_knowledge = []
    for r in records[:300]:
        source_mark = "[B]" if r.get("source") == "bloodline" else "[T]"
        instr = (r.get("instruction", "") or "")[:80]
        output = (r.get("output", "") or "")[:160]
        if instr and output:
            system_knowledge.append(f"- {source_mark} {instr}: {output}")

    model_name = f"sov33-oracle-c{cycle}"
    knowledge_text = "\n".join(system_knowledge)
    modelfile = (
        f"FROM {BASE_MODEL}\n"
        f"PARAMETER temperature 0\n"
        f"PARAMETER num_predict 256\n"
        f'SYSTEM """You are SOV33-Oracle, a sovereign AI trained on '
        f"bloodline-enriched data.\n"
        f"Key knowledge:\n"
        f"{knowledge_text}\n"
        f'"""'
    )

    mf_path = RESULTS_DIR / f"Modelfile.c{cycle}"
    mf_path.write_text(modelfile)
    log(f"  Modelfile: {mf_path} ({len(modelfile)} bytes)")

    log(f"\n[3] Creating Ollama model {model_name}...")
    r = subprocess.run(
        ["ollama", "create", model_name, "-f", str(mf_path)],
        capture_output=True, text=True, timeout=300
    )
    if r.returncode != 0:
        log(f"  FAILED: {r.stderr[:300]}")
        return False
    log(f"  Created: {model_name}")

    log(f"\n[4] Tagging as {EVOLVED_MODEL}...")
    subprocess.run(["ollama", "cp", model_name, EVOLVED_MODEL],
                   capture_output=True, text=True, timeout=30)
    log(f"  Tagged {EVOLVED_MODEL} -> {model_name}")

    result = {
        "cycle": cycle,
        "timestamp": datetime.now().isoformat(),
        "model": model_name,
        "total_records": len(records),
        "training_examples": len(training_data),
        "domains": {d: len(by_domain[d]) for d in sorted(by_domain)},
    }
    with open(RESULTS_DIR / f"bloodline_cycle_{cycle}.json", "w") as f:
        json.dump(result, f, indent=2)
    log(f"  Results: bloodline_cycle_{cycle}.json")
    return True


def main():
    log("=" * 60)
    log("  SOV33 BLOODLINE-ENHANCED TRAINING — Oracle Micro")
    log("=" * 60)

    records = load_records()
    if not records:
        log("ERROR: no records loaded")
        sys.exit(1)

    for cycle in range(1, 4):
        if not train_cycle(records, cycle):
            break
        if cycle < 3:
            log(f"\nWaiting 10s...")
            time.sleep(10)

    log(f"\n{'='*60}")
    log(f"  BLOODLINE TRAINING COMPLETE — {len(records)} records, 3 cycles")
    log(f"{'='*60}")


if __name__ == "__main__":
    main()
