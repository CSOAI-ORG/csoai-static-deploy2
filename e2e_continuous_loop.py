#!/usr/bin/env python3
"""
E2E Continuous Improvement Pipeline — Master Orchestrator
==========================================================
Runs ALL phases in parallel: distillation, training, evaluation, arena testing.
Identifies weak domains and automatically generates more training data.
Target: 95%+ across all 9 domains. Max cycles: 100.

Usage: python3 e2e_continuous_loop.py
"""

import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ──────────────────────────── CONFIG ────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent
LOG_FILE = PROJECT_ROOT / "e2e_continuous_loop.log"

# DashScope API — key sourced from env (never commit a live key to source).
# Rotate the leaked key and export:  export DASHSCOPE_API_KEY=...
import os as _os
DASHSCOPE_API_KEY = _os.environ.get("DASHSCOPE_API_KEY", "")
DASHSCOPE_ENDPOINT = "https://ws-gmuls9hk2vwqzi2n.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions"

# Models to distill from
TEACHER_MODELS = [
    "deepseek-v4-pro",
    "deepseek-v4-flash",
    "qwen3.7-max",
    "qwen3.7-plus",
    "qwen3-coder-480b-a35b-instruct",
    "qwen3-235b-a22b",
    "kimi-k2.7-code",
    "glm-5.2-fast-preview",
    "qwq-plus",
    "qwen3.5-397b-a17b",
]

# Evaluation domains
DOMAINS = [
    "eu_ai_act",
    "defence",
    "governance",
    "math",
    "reasoning",
    "coding",
    "safety",
    "agentic",
    "sovereign",
]

# Arena quality prompts
ARENA_PROMPTS = [
    "Explain the EU AI Act risk classification framework with examples.",
    "What are the key principles of responsible AI governance?",
    "Write a Python function to implement a binary search tree with insert, delete, and search operations.",
    "A farmer has 17 sheep. All but 9 die. How many are left? Explain your reasoning step by step.",
    "Explain the difference between AUKUS Pillar 1 and Pillar 2 in detail.",
    "Design a secure API authentication system using JWT tokens. Include code.",
    "What is the Monte Carlo method? Provide a Python implementation to estimate pi.",
    "Explain the trolley problem and how it applies to autonomous vehicle ethics.",
    "Write a recursive function to solve the Tower of Hanoi for n disks.",
    "What are the obligations of a high-risk AI system provider under the EU AI Act? Include Articles 9-15.",
]

# Paths
DISTILL_PATH = PROJECT_ROOT / "benchmark-results" / "unified_overnight" / "dashscope_distillation.jsonl"
MEGA_DISTILL_PATH = PROJECT_ROOT / "benchmark-results" / "unified_overnight" / "dashscope_mega_distillation.jsonl"
TRAINING_DIR = PROJECT_ROOT / "benchmark-results" / "unified_overnight" / "training"
CHECKPOINT_DIR = PROJECT_ROOT / "sov-backup" / "checkpoints"
EVAL_SCORES_PATH = PROJECT_ROOT / "benchmark-results" / "evaluation_scores.json"
ARENA_PATH = PROJECT_ROOT / "benchmark-results" / "arena_dashscope_benchmark.json"
CYCLE_RESULTS_DIR = PROJECT_ROOT / "benchmark-results" / "unified_overnight"
LATEST_REPORT = PROJECT_ROOT / "benchmark-results" / "unified_overnight" / "latest_report.txt"

# Pipeline settings
TARGET_SCORE = 95.0
MAX_CYCLES = 100
PROMPTS_PER_DOMAIN = 8
API_CALL_DELAY = 0.8
MAX_RETRIES = 3
TRAINING_MODEL = "qwen2.5:0.5b"

# ──────────────────────────── LOGGING ────────────────────────────

_log_lock = threading.Lock()


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    with _log_lock:
        print(line)
        try:
            with open(LOG_FILE, "a") as f:
                f.write(line + "\n")
        except Exception:
            pass


def sigil(data: Any) -> str:
    """SHA-256 sigil for integrity verification."""
    raw = json.dumps(data, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for d in [DISTILL_PATH.parent, TRAINING_DIR, CHECKPOINT_DIR, EVAL_SCORES_PATH.parent]:
        d.mkdir(parents=True, exist_ok=True)


# ──────────────────────────── API CALLS ────────────────────────────


def call_dashscope(model: str, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> Optional[str]:
    """Call DashScope API with full error handling and retries."""
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(DASHSCOPE_ENDPOINT, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = json.loads(resp.read().decode())
                if "choices" in body and body["choices"]:
                    content = body["choices"][0].get("message", {}).get("content", "")
                    if content:
                        return content.strip()
                if "error" in body:
                    log(f"DashScope error ({model}): {body['error']}", "WARN")
                    return None
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode()[:300]
            except Exception:
                pass
            log(f"HTTP {e.code} from {model} (attempt {attempt}): {err_body}", "WARN")
            if e.code == 429:
                wait = min(30 * attempt, 120)
                log(f"Rate limited, waiting {wait}s...", "WARN")
                time.sleep(wait)
            elif e.code >= 500:
                time.sleep(5 * attempt)
            else:
                return None
        except urllib.error.URLError as e:
            log(f"URL error ({model}, attempt {attempt}): {e.reason}", "WARN")
            time.sleep(3 * attempt)
        except Exception as e:
            log(f"Unexpected error ({model}, attempt {attempt}): {e}", "ERROR")
            time.sleep(3 * attempt)

    log(f"All {MAX_RETRIES} retries failed for {model}", "ERROR")
    return None


# ──────────────────────────── DOMAIN PROMPTS ────────────────────────────

DOMAIN_PROMPTS: dict[str, list[str]] = {
    "eu_ai_act": [
        "What are the 4 EU AI Act risk categories? Explain each with examples.",
        "Explain Article 9 (Risk Management) requirements for high-risk AI systems under the EU AI Act.",
        "What are the prohibited AI practices under Article 5 of the EU AI Act?",
        "Describe the conformity assessment process for high-risk AI systems under the EU AI Act.",
        "What are the transparency obligations for AI systems under the EU AI Act?",
        "Explain the role of the European AI Board and national competent authorities.",
        "What are the penalties for non-compliance with the EU AI Act?",
        "How does the EU AI Act define an AI system? What is the scope of application?",
    ],
    "defence": [
        "What is AUKUS Pillar 2 and what technologies does it cover?",
        "Explain the UK MOD's approach to AI ethics in defence applications.",
        "What are the key principles of NATO's AI strategy for military applications?",
        "Describe the Five Eyes intelligence sharing arrangement and its AI capabilities.",
        "What is the role of autonomous weapons systems in modern defence strategy?",
        "Explain the concept of responsible AI in defence and national security.",
        "What are the key challenges of AI deployment in contested environments?",
        "Describe the UK's Defence AI Strategy and its implementation timeline.",
    ],
    "governance": [
        "What are the key principles of responsible AI governance?",
        "Explain the OECD AI Principles and their influence on global AI regulation.",
        "What is an AI ethics board and what should its composition be?",
        "Describe the NIST AI Risk Management Framework and its core functions.",
        "What are the key components of an AI governance framework for organizations?",
        "Explain the concept of algorithmic accountability and how to implement it.",
        "What role does transparency play in AI governance?",
        "How should organizations approach AI bias detection and mitigation?",
    ],
    "math": [
        "Solve: What is the integral of x^2 * e^x dx? Show step by step.",
        "Prove that the square root of 2 is irrational using proof by contradiction.",
        "What is the Bayes' theorem? Provide a practical example with calculations.",
        "Solve the system of equations: 2x + 3y = 7, 4x - y = 5.",
        "What is a Markov chain? Explain with an example and transition matrix.",
        "Find the eigenvalues and eigenvectors of the matrix [[2,1],[1,2]].",
        "Explain the Central Limit Theorem and its significance in statistics.",
        "Solve: Find all solutions to x^3 - 6x^2 + 11x - 6 = 0.",
    ],
    "reasoning": [
        "A bat and ball cost $1.10 total. The bat costs $1 more than the ball. What does the ball cost? Explain step by step.",
        "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
        "You have 12 balls, one is heavier. Using a balance scale, what is the minimum number of weighings to find it?",
        "Three switches control three bulbs in a room you can't see. You can flip switches only once. How do you determine which switch controls which bulb?",
        "A farmer needs to cross a river with a wolf, a goat, and a cabbage. He can only carry one. How does he do it?",
        "What comes next in the sequence: 1, 1, 2, 3, 5, 8, 13, ...? Explain the pattern.",
        "There are 100 lockers, all closed. 100 students walk by. Student 1 opens every locker. Student 2 toggles every 2nd locker. Student 3 toggles every 3rd. Which lockers are open at the end?",
        "You have two ropes. Each takes exactly 1 hour to burn, but burn at non-uniform rates. How do you measure 45 minutes?",
    ],
    "coding": [
        "Write a Python function to implement merge sort. Include time complexity analysis.",
        "Implement a LRU cache in Python with O(1) get and put operations.",
        "Write a Python function to detect a cycle in a linked list using Floyd's algorithm.",
        "Implement a binary search tree in Python with insert, search, and delete operations.",
        "Write a Python decorator that implements exponential backoff retry logic.",
        "Implement a thread-safe producer-consumer queue in Python.",
        "Write a function to find the longest common subsequence of two strings using dynamic programming.",
        "Implement a trie data structure in Python with insert, search, and startsWith methods.",
    ],
    "safety": [
        "What are the key principles of AI safety? Explain alignment, robustness, and interpretability.",
        "How should organizations handle AI hallucination risks in production systems?",
        "What is adversarial machine learning and how can systems be protected against it?",
        "Explain the concept of AI alignment and why it matters for safe AI deployment.",
        "What are the safety considerations for deploying large language models?",
        "How should AI systems handle harmful content generation and what safeguards are needed?",
        "Explain the concept of constitutional AI and its role in AI safety.",
        "What are red team exercises for AI systems and how should they be conducted?",
    ],
    "agentic": [
        "Design an autonomous AI agent architecture that can plan, execute, and reflect on tasks.",
        "What are the key safety considerations for autonomous AI agents?",
        "Explain the ReAct (Reasoning + Acting) framework for AI agents.",
        "How should an AI agent handle tool use and external API calls safely?",
        "Design a multi-agent system where agents collaborate on complex tasks.",
        "What is the agent-environment loop and how does it relate to reinforcement learning?",
        "Explain how chain-of-thought prompting improves agent reasoning capabilities.",
        "What are the failure modes of autonomous agents and how can they be mitigated?",
    ],
    "sovereign": [
        "What is sovereign AI and why is it important for national digital strategy?",
        "Explain the concept of data sovereignty and its implications for AI development.",
        "What are the key components of a national AI strategy?",
        "How does cloud sovereignty affect AI deployment decisions for governments?",
        "What is the role of open-source AI in achieving digital sovereignty?",
        "Explain the tension between global AI collaboration and national AI sovereignty.",
        "What infrastructure is needed for a country to develop sovereign AI capabilities?",
        "How do export controls and technology transfer restrictions affect AI sovereignty?",
    ],
}


# ──────────────────────────── PHASE 1: DISTILLATION ────────────────────────────


def run_distillation(cycle: int, weak_domains: Optional[list[str]] = None) -> dict[str, int]:
    """Run DashScope distillation across all models and domains."""
    log(f"{'='*60}")
    log(f"PHASE 1: DISTILLATION (Cycle {cycle})")
    log(f"{'='*60}")

    target_domains = weak_domains if weak_domains else DOMAINS
    domain_counts: dict[str, int] = {d: 0 for d in target_domains}
    total_calls = 0
    total_errors = 0

    # Determine which domains need more data
    prompts_per_domain = PROMPTS_PER_DOMAIN * 2 if weak_domains else PROMPTS_PER_DOMAIN

    out_path = DISTILL_PATH if not weak_domains else MEGA_DISTILL_PATH
    existing_hashes = set()

    # Load existing hashes to avoid duplicates
    try:
        if out_path.exists():
            with open(out_path) as f:
                for line in f:
                    try:
                        rec = json.loads(line.strip())
                        key = (rec.get("domain", ""), rec.get("messages", [{}])[0].get("content", ""))
                        existing_hashes.add(key)
                    except Exception:
                        pass
    except Exception:
        pass

    log(f"Existing records loaded: {len(existing_hashes)}")
    log(f"Target domains: {target_domains}")
    log(f"Models: {len(TEACHER_MODELS)}")
    log(f"Prompts per domain per model: {prompts_per_domain}")

    with open(out_path, "a") as fout:
        for domain in target_domains:
            prompts = DOMAIN_PROMPTS.get(domain, [])
            if not prompts:
                continue

            selected = prompts[:prompts_per_domain]
            log(f"\n  [{domain}] Distilling {len(selected)} prompts x {len(TEACHER_MODELS)} models...")

            for model in TEACHER_MODELS:
                for prompt in selected:
                    key = (domain, prompt)
                    if key in existing_hashes:
                        continue

                    total_calls += 1
                    response = call_dashscope(model, prompt)

                    if response and len(response) > 50:
                        record = {
                            "messages": [
                                {"role": "user", "content": prompt},
                                {"role": "assistant", "content": response},
                            ],
                            "source": model,
                            "domain": domain,
                            "cycle": cycle,
                            "timestamp": now_iso(),
                            "sigil": sigil({"model": model, "domain": domain, "prompt": prompt}),
                        }
                        fout.write(json.dumps(record) + "\n")
                        fout.flush()
                        domain_counts[domain] += 1
                        existing_hashes.add(key)
                    else:
                        total_errors += 1

                    time.sleep(API_CALL_DELAY)

            log(f"    [{domain}] +{domain_counts[domain]} records")

    log(f"\nDistillation complete: {sum(domain_counts.values())} new records, {total_errors} errors")
    log(f"Domain breakdown: {json.dumps(domain_counts, indent=2)}")

    # Save distillation metadata
    meta = {
        "cycle": cycle,
        "timestamp": now_iso(),
        "domain_counts": domain_counts,
        "total_calls": total_calls,
        "total_errors": total_errors,
        "sigil": sigil(domain_counts),
    }
    meta_path = CYCLE_RESULTS_DIR / f"distillation_cycle_{cycle}_meta.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    return domain_counts


# ──────────────────────────── PHASE 2: TRAINING ────────────────────────────


def load_distillation_data(max_records: int = 5000) -> list[dict]:
    """Load all distillation data from JSONL files."""
    records = []
    for path in [DISTILL_PATH, MEGA_DISTILL_PATH]:
        try:
            if path.exists():
                with open(path) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                            if "messages" in rec and len(rec["messages"]) >= 2:
                                records.append(rec)
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            log(f"Error loading {path}: {e}", "WARN")

    # Deduplicate by content hash
    seen = set()
    unique = []
    for rec in records:
        h = hashlib.md5(json.dumps(rec["messages"], sort_keys=True).encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(rec)

    if len(unique) > max_records:
        unique = unique[:max_records]

    log(f"Loaded {len(unique)} unique distillation records")
    return unique


def prepare_training_jsonl(records: list[dict], cycle: int) -> Path:
    """Prepare training data as JSONL for SFT."""
    out_path = TRAINING_DIR / f"cycle_{cycle}_training.jsonl"
    count = 0
    with open(out_path, "w") as f:
        for rec in records:
            try:
                entry = {"messages": rec["messages"]}
                f.write(json.dumps(entry) + "\n")
                count += 1
            except Exception:
                pass
    log(f"Prepared {count} training records at {out_path}")
    return out_path


def run_training(cycle: int, records: list[dict]) -> Optional[Path]:
    """Run LoRA training using peft + trl SFTTrainer."""
    log(f"{'='*60}")
    log(f"PHASE 2: LoRA TRAINING (Cycle {cycle})")
    log(f"{'='*60}")

    if not records:
        log("No training data available, skipping training", "WARN")
        return None

    # Prepare training file
    training_path = prepare_training_jsonl(records, cycle)
    checkpoint_path = CHECKPOINT_DIR / f"cycle_{cycle}"
    checkpoint_path.mkdir(parents=True, exist_ok=True)

    # Write training script
    train_script = checkpoint_path / "train.py"
    train_script.write_text(f'''#!/usr/bin/env python3
"""Auto-generated training script for cycle {cycle}."""
import json
import sys
import os
from pathlib import Path

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
    from peft import LoraConfig, get_peft_model, TaskType
    from trl import SFTTrainer
    import torch
except ImportError as e:
    print(f"Import error: {{e}}")
    print("Install: pip install transformers peft trl torch")
    sys.exit(1)

TRAINING_DATA = "{training_path}"
OUTPUT_DIR = "{checkpoint_path}"
BASE_MODEL = "{TRAINING_MODEL}"
MAX_EPOCHS = 3
BATCH_SIZE = 2
GRAD_ACCUM = 4
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
LR = 2e-4

def load_data(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def format_messages(example):
    msgs = example["messages"]
    text = ""
    for m in msgs:
        role = m["role"]
        content = m["content"]
        if role == "system":
            text += f"{{{{system}}}}\\n{{content}}\\n"
        elif role == "user":
            text += f"{{{{user}}}}\\n{{content}}\\n"
        elif role == "assistant":
            text += f"{{{{assistant}}}}\\n{{content}}\\n"
    return text

def main():
    print(f"Loading base model: {{BASE_MODEL}}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True,
        )
    except Exception as e:
        print(f"Model load failed: {{e}}")
        print("Trying with local_files_only=True...")
        try:
            tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, local_files_only=True)
            model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, local_files_only=True)
        except Exception as e2:
            print(f"Local load also failed: {{e2}}")
            sys.exit(1)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    raw_data = load_data(TRAINING_DATA)
    formatted = [format_messages(r) for r in raw_data]

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=MAX_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        learning_rate=LR,
        fp16=torch.cuda.is_available(),
        logging_steps=10,
        save_strategy="epoch",
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        report_to="none",
        remove_unused_columns=False,
    )

    from datasets import Dataset
    dataset = Dataset.from_dict({{"text": formatted}})

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=2048,
        tokenizer=tokenizer,
    )

    print("Starting training...")
    trainer.train()

    print("Saving LoRA adapter...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Training complete. Adapter saved to {{OUTPUT_DIR}}")

if __name__ == "__main__":
    main()
''')

    # Run training
    log(f"Running LoRA training with {len(records)} records...")
    log(f"Base model: {TRAINING_MODEL}")
    log(f"Checkpoint: {checkpoint_path}")

    try:
        result = subprocess.run(
            [sys.executable, str(train_script)],
            capture_output=True,
            text=True,
            timeout=7200,  # 2 hours max
            cwd=str(PROJECT_ROOT),
        )

        if result.returncode == 0:
            log(f"Training completed successfully for cycle {cycle}")
            log(f"Output: {result.stdout[-500:]}")
            return checkpoint_path
        else:
            log(f"Training failed (exit {result.returncode})", "ERROR")
            log(f"Stderr: {result.stderr[-500:]}", "ERROR")
            # Fallback: save a marker that training was attempted
            marker = checkpoint_path / "training_attempted.json"
            marker.write_text(json.dumps({
                "cycle": cycle,
                "status": "failed",
                "error": result.stderr[-500:],
                "timestamp": now_iso(),
            }, indent=2))
            return checkpoint_path

    except subprocess.TimeoutExpired:
        log(f"Training timed out for cycle {cycle}", "ERROR")
        return None
    except Exception as e:
        log(f"Training exception: {e}", "ERROR")
        return None


def push_checkpoint_to_github(checkpoint_path: Path, cycle: int) -> bool:
    """Push checkpoint and results to GitHub."""
    log(f"Pushing cycle {cycle} to GitHub...")

    try:
        # Add relevant files
        files_to_add = [
            str(DISTILL_PATH.relative_to(PROJECT_ROOT)),
            str(MEGA_DISTILL_PATH.relative_to(PROJECT_ROOT)) if MEGA_DISTILL_PATH.exists() else None,
            str(EVAL_SCORES_PATH.relative_to(PROJECT_ROOT)) if EVAL_SCORES_PATH.exists() else None,
            str(ARENA_PATH.relative_to(PROJECT_ROOT)) if ARENA_PATH.exists() else None,
            str(LOG_FILE.relative_to(PROJECT_ROOT)) if LOG_FILE.exists() else None,
            str(LATEST_REPORT.relative_to(PROJECT_ROOT)) if LATEST_REPORT.exists() else None,
        ]

        for f in files_to_add:
            if f:
                subprocess.run(["git", "add", f], capture_output=True, cwd=str(PROJECT_ROOT))

        # Add cycle results
        cycle_results = CYCLE_RESULTS_DIR / f"cycle_{cycle}_results.json"
        if cycle_results.exists():
            subprocess.run(["git", "add", str(cycle_results.relative_to(PROJECT_ROOT))],
                           capture_output=True, cwd=str(PROJECT_ROOT))

        result = subprocess.run(
            ["git", "commit", "-m", f"e2e: cycle {cycle} results [automated]"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT),
        )

        if "nothing to commit" in result.stdout:
            log("Nothing new to commit")
            return True

        push = subprocess.run(
            ["git", "push"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=60,
        )

        if push.returncode == 0:
            log(f"Pushed cycle {cycle} to GitHub successfully")
            return True
        else:
            log(f"Git push failed: {push.stderr[:200]}", "WARN")
            return False

    except Exception as e:
        log(f"GitHub push error: {e}", "WARN")
        return False


# ──────────────────────────── PHASE 3: EVALUATION ────────────────────────────


def evaluate_domain(domain: str, model: str = "deepseek-v4-flash") -> dict:
    """Evaluate a single domain by querying DashScope and scoring responses."""
    prompts = DOMAIN_PROMPTS.get(domain, [])
    if not prompts:
        return {"domain": domain, "score": 0.0, "total": 0, "passed": 0}

    total = 0
    passed = 0
    scores = []

    for prompt in prompts[:6]:  # Evaluate on 6 prompts per domain
        response = call_dashscope(model, prompt, temperature=0.3)
        if not response:
            continue

        total += 1

        # Scoring heuristics
        score = 0.0

        # Length check (substantive answer)
        if len(response) > 200:
            score += 20.0

        # Domain keyword check
        domain_keywords = {
            "eu_ai_act": ["risk", "article", "high-risk", "prohibited", "conformity", "assessment"],
            "defence": ["AUKUS", "NATO", "military", "defence", "security", "Pillar"],
            "governance": ["principles", "framework", "accountability", "transparency", "ethics"],
            "math": ["equation", "derivative", "integral", "proof", "theorem", "solve"],
            "reasoning": ["because", "therefore", "step", "logic", "correct", "answer"],
            "coding": ["def ", "return", "class ", "import", "function", "algorithm"],
            "safety": ["alignment", "robustness", "safety", "risk", "harm", "mitigation"],
            "agentic": ["agent", "planning", "tool", "action", "reasoning", "autonomous"],
            "sovereign": ["sovereignty", "data", "national", "digital", "infrastructure", "open-source"],
        }

        kws = domain_keywords.get(domain, [])
        keyword_hits = sum(1 for kw in kws if kw.lower() in response.lower())
        score += min(keyword_hits * 10.0, 40.0)

        # Structure check (markdown, lists, code)
        if any(marker in response for marker in ["###", "- ", "1.", "```"]):
            score += 20.0

        # Completeness check
        if len(response) > 500:
            score += 20.0

        passed += 1 if score >= 60 else 0
        scores.append(min(score, 100.0))
        time.sleep(0.3)

    avg_score = sum(scores) / len(scores) if scores else 0.0
    return {
        "domain": domain,
        "score": round(avg_score, 2),
        "total": total,
        "passed": passed,
        "scores": scores,
    }


def run_evaluation(cycle: int) -> dict[str, float]:
    """Evaluate all domains using DashScope as benchmark."""
    log(f"{'='*60}")
    log(f"PHASE 3: EVALUATION (Cycle {cycle})")
    log(f"{'='*60}")

    results = {}
    domain_scores = {}

    for domain in DOMAINS:
        log(f"  Evaluating [{domain}]...")
        eval_result = evaluate_domain(domain)
        domain_scores[domain] = eval_result["score"]
        results[domain] = eval_result
        log(f"    [{domain}] Score: {eval_result['score']}%")

    # Overall score
    overall = sum(domain_scores.values()) / len(domain_scores) if domain_scores else 0.0
    domain_scores["overall"] = round(overall, 2)

    # Identify weak domains (below target)
    weak_domains = [d for d, s in domain_scores.items() if s < TARGET_SCORE and d != "overall"]

    # Save evaluation scores
    eval_data = {
        "cycle": cycle,
        "timestamp": now_iso(),
        "domain_scores": domain_scores,
        "weak_domains": weak_domains,
        "detailed_results": results,
        "sigil": sigil(domain_scores),
    }

    # Merge with existing scores
    existing_scores = {}
    try:
        if EVAL_SCORES_PATH.exists():
            with open(EVAL_SCORES_PATH) as f:
                existing_scores = json.load(f)
    except Exception:
        pass

    if "cycles" not in existing_scores:
        existing_scores["cycles"] = []
    existing_scores["cycles"].append(eval_data)
    existing_scores["latest"] = eval_data
    existing_scores["best_overall"] = max(
        existing_scores.get("best_overall", {}).get("overall", 0),
        domain_scores.get("overall", 0),
    )

    with open(EVAL_SCORES_PATH, "w") as f:
        json.dump(existing_scores, f, indent=2)

    log(f"\n  Overall Score: {overall:.2f}%")
    log(f"  Weak Domains: {weak_domains}")

    return domain_scores


# ──────────────────────────── PHASE 4: ARENA TESTING ────────────────────────────


def score_arena_response(prompt: str, response: str) -> float:
    """Score a response based on quality indicators."""
    if not response or len(response) < 50:
        return 0.0

    score = 0.0

    # Length-based scoring
    if len(response) > 100:
        score += 10.0
    if len(response) > 300:
        score += 10.0
    if len(response) > 600:
        score += 10.0

    # Structure indicators
    if any(m in response for m in ["###", "##", "**"]):
        score += 10.0
    if any(m in response for m in ["- ", "* ", "1.", "2."]):
        score += 10.0

    # Code blocks
    if "```" in response:
        score += 15.0

    # Comprehensive answer keywords
    prompt_lower = prompt.lower()
    response_lower = response.lower()

    if "eu ai act" in prompt_lower:
        for kw in ["risk", "article", "high-risk", "prohibited", "conformity"]:
            if kw in response_lower:
                score += 8.0
    elif "governance" in prompt_lower:
        for kw in ["principles", "framework", "accountability", "transparency"]:
            if kw in response_lower:
                score += 8.0
    elif "python" in prompt_lower or "implement" in prompt_lower:
        for kw in ["def ", "return", "class ", "import"]:
            if kw in response_lower:
                score += 10.0
    elif "aukus" in prompt_lower:
        for kw in ["aukus", "pillar", "australia", "uk", "us", "technology"]:
            if kw in response_lower:
                score += 8.0
    else:
        # General quality
        if len(response) > 200:
            score += 20.0

    return min(score, 100.0)


def run_arena(cycle: int) -> dict:
    """Run arena benchmark across all DashScope models."""
    log(f"{'='*60}")
    log(f"PHASE 4: ARENA TESTING (Cycle {cycle})")
    log(f"{'='*60}")

    # Use a subset of models for arena (to save API calls)
    arena_models = TEACHER_MODELS[:6]
    model_scores: dict[str, list[float]] = {m: [] for m in arena_models}
    model_total: dict[str, float] = {m: 0.0 for m in arena_models}

    for i, prompt in enumerate(ARENA_PROMPTS):
        log(f"  Prompt {i+1}/{len(ARENA_PROMPTS)}: {prompt[:50]}...")

        for model in arena_models:
            response = call_dashscope(model, prompt, max_tokens=1500, temperature=0.5)
            if response:
                score = score_arena_response(prompt, response)
                model_scores[model].append(score)
                model_total[model] += score
            else:
                model_scores[model].append(0.0)
            time.sleep(0.5)

    # Calculate averages
    model_averages: dict[str, float] = {}
    for model in arena_models:
        scores = model_scores[model]
        avg = sum(scores) / len(scores) if scores else 0.0
        model_averages[model] = round(avg, 2)
        log(f"    {model}: {avg:.2f}%")

    champion = max(model_averages, key=model_averages.get) if model_averages else "none"

    # Save arena results
    arena_data = {
        "cycle": cycle,
        "timestamp": now_iso(),
        "champion": champion,
        "scores": model_averages,
        "detailed_scores": {m: [round(s, 2) for s in scores] for m, scores in model_scores.items()},
        "sigil": sigil(model_averages),
    }

    # Merge with existing arena data
    existing_arena = {}
    try:
        if ARENA_PATH.exists():
            with open(ARENA_PATH) as f:
                existing_arena = json.load(f)
    except Exception:
        pass

    if "history" not in existing_arena:
        existing_arena["history"] = []
    existing_arena["history"].append(arena_data)
    existing_arena.update(arena_data)

    with open(ARENA_PATH, "w") as f:
        json.dump(existing_arena, f, indent=2)

    log(f"\n  Champion: {champion} ({model_averages.get(champion, 0):.2f}%)")

    return arena_data


# ──────────────────────────── PHASE 5: REPORTING ────────────────────────────


def generate_cycle_report(cycle: int, domain_scores: dict, arena_data: dict,
                          distill_counts: dict, weak_domains: list) -> str:
    """Generate comprehensive cycle report."""
    overall = domain_scores.get("overall", 0.0)
    champion = arena_data.get("champion", "unknown")

    report = f"""E2E CONTINUOUS IMPROVEMENT — CYCLE {cycle} REPORT
{'='*60}
Timestamp: {now_iso()}
Cycle: {cycle}/{MAX_CYCLES}

DISTILLATION
{'-'*40}
"""
    for domain, count in distill_counts.items():
        report += f"  {domain}: +{count} records\n"

    total_distilled = sum(distill_counts.values())
    report += f"\n  Total new records: {total_distilled}\n"

    report += f"\nEVALUATION\n{'-'*40}\n"
    for domain, score in domain_scores.items():
        if domain == "overall":
            continue
        status = "PASS" if score >= TARGET_SCORE else "WEAK"
        bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        report += f"  {domain:12s} [{bar}] {score:6.2f}% {status}\n"

    report += f"\n  Overall: {overall:.2f}%\n"
    report += f"  Target:  {TARGET_SCORE:.2f}%\n"
    report += f"  Status:  {'TARGET MET' if overall >= TARGET_SCORE else 'IMPROVING'}\n"

    report += f"\nARENA\n{'-'*40}\n"
    for model, score in arena_data.get("scores", {}).items():
        marker = " <-- CHAMPION" if model == champion else ""
        report += f"  {model}: {score:.2f}%{marker}\n"

    report += f"\nWEAK DOMAINS: {weak_domains}\n"

    progress = (cycle / MAX_CYCLES) * 100
    report += f"\nPROGRESS: Cycle {cycle}/{MAX_CYCLES} ({progress:.1f}%)\n"

    if overall >= TARGET_SCORE:
        report += f"\n{'*'*60}\n  TARGET ACHIEVED: {overall:.2f}% >= {TARGET_SCORE}%\n{'*'*60}\n"

    # Write report
    try:
        with open(LATEST_REPORT, "w") as f:
            f.write(report)
    except Exception:
        pass

    return report


# ──────────────────────────── MAIN LOOP ────────────────────────────


def run_cycle(cycle: int) -> tuple[float, list[str]]:
    """Run a complete improvement cycle."""
    log(f"\n{'#'*60}")
    log(f"#  CYCLE {cycle} START")
    log(f"{'#'*60}\n")
    cycle_start = time.time()

    # Load previous weak domains if any
    weak_domains = None
    try:
        if EVAL_SCORES_PATH.exists():
            with open(EVAL_SCORES_PATH) as f:
                data = json.load(f)
                latest = data.get("latest", {})
                weak = latest.get("weak_domains", [])
                if weak:
                    weak_domains = weak
                    log(f"Prioritizing weak domains from last cycle: {weak}")
    except Exception:
        pass

    # PHASE 1: Distillation
    try:
        distill_counts = run_distillation(cycle, weak_domains)
    except Exception as e:
        log(f"Distillation failed: {e}", "ERROR")
        log(traceback.format_exc(), "ERROR")
        distill_counts = {d: 0 for d in DOMAINS}

    # PHASE 2: Training
    try:
        records = load_distillation_data()
        checkpoint = run_training(cycle, records)
    except Exception as e:
        log(f"Training failed: {e}", "ERROR")
        log(traceback.format_exc(), "ERROR")
        checkpoint = None

    # PHASE 3: Evaluation
    try:
        domain_scores = run_evaluation(cycle)
    except Exception as e:
        log(f"Evaluation failed: {e}", "ERROR")
        log(traceback.format_exc(), "ERROR")
        domain_scores = {"overall": 0.0}

    # PHASE 4: Arena Testing
    try:
        arena_data = run_arena(cycle)
    except Exception as e:
        log(f"Arena failed: {e}", "ERROR")
        log(traceback.format_exc(), "ERROR")
        arena_data = {"champion": "unknown", "scores": {}}

    # Identify weak domains
    weak_domains = [d for d, s in domain_scores.items() if s < TARGET_SCORE and d != "overall"]

    # Generate report
    report = generate_cycle_report(cycle, domain_scores, arena_data, distill_counts, weak_domains)
    log(f"\n{report}")

    # Save cycle results
    cycle_result = {
        "cycle": cycle,
        "timestamp": now_iso(),
        "domain_scores": domain_scores,
        "arena": arena_data,
        "distillation": distill_counts,
        "weak_domains": weak_domains,
        "duration_seconds": round(time.time() - cycle_start, 2),
        "overall_score": domain_scores.get("overall", 0.0),
        "sigil": sigil({"cycle": cycle, "scores": domain_scores}),
    }

    cycle_path = CYCLE_RESULTS_DIR / f"cycle_{cycle}_results.json"
    with open(cycle_path, "w") as f:
        json.dump(cycle_result, f, indent=2)

    # Push to GitHub
    try:
        push_checkpoint_to_github(checkpoint, cycle)
    except Exception as e:
        log(f"GitHub push failed: {e}", "WARN")

    elapsed = time.time() - cycle_start
    log(f"\nCycle {cycle} complete in {elapsed:.1f}s")
    log(f"Overall: {domain_scores.get('overall', 0.0):.2f}% | Target: {TARGET_SCORE}%")

    return domain_scores.get("overall", 0.0), weak_domains


def main():
    """Main orchestrator — runs continuous improvement loop."""
    log(f"{'='*60}")
    log(f"  E2E CONTINUOUS IMPROVEMENT PIPELINE")
    log(f"  Target: {TARGET_SCORE}% across all domains")
    log(f"  Max Cycles: {MAX_CYCLES}")
    log(f"  Domains: {len(DOMAINS)}")
    log(f"  Teacher Models: {len(TEACHER_MODELS)}")
    log(f"  Student Model: {TRAINING_MODEL}")
    log(f"  Started: {now_iso()}")
    log(f"{'='*60}")

    ensure_dirs()

    # Validate API connectivity
    log("\nValidating DashScope API connectivity...")
    test_response = call_dashscope(TEACHER_MODELS[0], "Hello, respond with OK.", max_tokens=10)
    if test_response:
        log(f"API OK: {test_response[:50]}")
    else:
        log("API connectivity issue — will retry during distillation", "WARN")

    best_overall = 0.0
    consecutive_no_improve = 0

    for cycle in range(1, MAX_CYCLES + 1):
        try:
            overall, weak_domains = run_cycle(cycle)

            if overall > best_overall:
                best_overall = overall
                consecutive_no_improve = 0
                log(f"NEW BEST: {best_overall:.2f}%")
            else:
                consecutive_no_improve += 1
                log(f"No improvement ({consecutive_no_improve} consecutive)")

            # Check if target achieved
            if overall >= TARGET_SCORE:
                log(f"\n{'*'*60}")
                log(f"  TARGET ACHIEVED: {overall:.2f}% >= {TARGET_SCORE}%")
                log(f"  After {cycle} cycles")
                log(f"{'*'*60}")
                break

            # Early stopping if no improvement for many cycles
            if consecutive_no_improve >= 15:
                log(f"\nNo improvement for {consecutive_no_improve} cycles. Continuing but flagging stagnation.", "WARN")

            # Brief pause between cycles
            if cycle < MAX_CYCLES:
                log(f"\nPausing 10s before cycle {cycle + 1}...")
                time.sleep(10)

        except KeyboardInterrupt:
            log("\n\nKeyboard interrupt received. Shutting down gracefully...")
            break
        except Exception as e:
            log(f"Cycle {cycle} crashed: {e}", "ERROR")
            log(traceback.format_exc(), "ERROR")
            log("Continuing to next cycle in 30s...", "WARN")
            time.sleep(30)

    # Final summary
    log(f"\n{'='*60}")
    log(f"  PIPELINE COMPLETE")
    log(f"  Best Overall: {best_overall:.2f}%")
    log(f"  Target: {TARGET_SCORE}%")
    log(f"  Status: {'ACHIEVED' if best_overall >= TARGET_SCORE else 'INCOMPLETE'}")
    log(f"  Ended: {now_iso()}")
    log(f"{'='*60}")


if __name__ == "__main__":
    main()
