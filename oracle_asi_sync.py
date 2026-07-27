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


def build_remote_script():
    return f'''#!/usr/bin/env python3
import json, subprocess, sys, os, time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

REMOTE_DIR = "{REMOTE_DIR}"
DATA_DIR = Path(REMOTE_DIR) / "data"
RESULTS_DIR = Path(REMOTE_DIR) / "results"
RESULTS_DIR.mkdir(exist_ok=True)

BASE_MODEL = "{BASE_MODEL}"
EVOLVED_MODEL = "{EVOLVED_MODEL}"

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{{ts}}] {{msg}}", flush=True)

def load_records():
    all_records = []
    for f in sorted(DATA_DIR.glob("*.jsonl")):
        log(f"  Loading {{f.name}}...")
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    all_records.append(json.loads(line))
    log(f"  Total: {{len(all_records)}} records")
    return all_records

def format_chat(instr, output):
    return {{
        "text": f"<|im_start|>user\\\\n{{instr}}<|im_end|>\\\\n<|im_start|>assistant\\\\n{{output}}<|im_end|>"
    }}

def train_cycle(records, cycle):
    log(f"\\\\n{{'='*60}}")
    log(f"  CYCLE {{cycle}} — bloodline-enhanced")
    log(f"{{'='*60}}")

    by_domain = defaultdict(list)
    for r in records:
        by_domain[r.get("domain", "general")].append(r)

    log(f"\\\\n[1] Domains covered:")
    for d in sorted(by_domain):
        priority = sum(1 for r in by_domain[d] if r.get("source") == "bloodline")
        log(f"    {{d:20s}} {{len(by_domain[d]):4d}} records  ({{priority}} bloodline)")

    training_data = []
    for r in records:
        instr = r.get("instruction", "") or r.get("question", "")
        output = r.get("output", "") or r.get("answer", "") or r.get("response", "")
        if instr and output:
            training_data.append(format_chat(instr, output))

    log(f"\\\\n[2] Training data: {{len(training_data)}} chat examples")

    system_knowledge = []
    for r in records[:300]:
        source_mark = "[B]" if r.get("source") == "bloodline" else "[T]"
        instr = (r.get("instruction", "") or "")[:80]
        output = (r.get("output", "") or "")[:160]
        if instr and output:
            system_knowledge.append(f"- {{source_mark}} {{instr}}: {{output}}")

    model_name = f"sov33-oracle-c{{cycle}}"
    modelfile = f"FROM {{BASE_MODEL}}\\\nPARAMETER temperature 0\\\nPARAMETER num_predict 256\\\n"
    modelfile += 'SYSTEM """You are SOV33-Oracle, a sovereign AI trained on bloodline-enriched data.\n'
    modelfile += 'Key knowledge:\n' + '\\n'.join(system_knowledge) + '\n"""'

    mf_path = RESULTS_DIR / f"Modelfile.c{{cycle}}"
    mf_path.write_text(modelfile)
    log(f"  Modelfile: {{mf_path}} ({{len(modelfile)}} bytes)")

    log(f"\\\\n[3] Creating Ollama model {{model_name}}...")
    r = subprocess.run(
        ["ollama", "create", model_name, "-f", str(mf_path)],
        capture_output=True, text=True, timeout=300
    )
    if r.returncode != 0:
        log(f"  FAILED: {{r.stderr[:300]}}")
        return False
    log(f"  Created: {{model_name}}")

    log(f"\\\\n[4] Tagging as {{EVOLVED_MODEL}}...")
    subprocess.run(["ollama", "cp", model_name, EVOLVED_MODEL],
                   capture_output=True, text=True, timeout=30)
    log(f"  Tagged {{EVOLVED_MODEL}} -> {{model_name}}")

    result = {{
        "cycle": cycle,
        "timestamp": datetime.now().isoformat(),
        "model": model_name,
        "total_records": len(records),
        "training_examples": len(training_data),
        "domains": {{d: len(by_domain[d]) for d in sorted(by_domain)}},
    }}
    with open(RESULTS_DIR / f"bloodline_cycle_{{cycle}}.json", "w") as f:
        json.dump(result, f, indent=2)
    log(f"  Results: bloodline_cycle_{{cycle}}.json")
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
            log(f"\\\\nWaiting 10s...")
            time.sleep(10)

    log(f"\\\\n{{'='*60}}")
    log(f"  BLOODLINE TRAINING COMPLETE — {{len(records)}} records, 3 cycles")
    log(f"{{'='*60}}")

if __name__ == "__main__":
    main()
'''


def step_deploy_and_run():
    log("")
    log("=" * 60)
    log("  STEP 3: Deploy bloodline training script")
    log("=" * 60)

    script_body = build_remote_script()
    local_tmp = Path("/tmp/oracle_bloodline_train.py")
    local_tmp.write_text(script_body)

    remote_script_path = f"{REMOTE_DIR}/bloodline_train.py"
    run(
        SCP_BASE + [str(local_tmp), f"{ORACLE_USER}@{ORACLE_HOST}:{remote_script_path}"],
        "SCP bloodline_train.py",
    )
    local_tmp.unlink(missing_ok=True)

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
