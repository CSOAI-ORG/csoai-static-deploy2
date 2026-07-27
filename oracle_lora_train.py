#!/usr/bin/env python3
"""
Oracle ARM LoRA Training Script for Qwen2.5-0.5B-Instruct
==========================================================
Runs on Oracle Cloud Free Tier ARM (CPU-only, 956MB RAM, 34GB disk).
Fine-tunes with LoRA using DashScope distillation data.

Usage:
    python oracle_lora_train.py
"""

import os
import sys
import json
import gc
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_FILE = Path(__file__).parent / "oracle_lora_train.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("oracle_lora")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
DATA_PATH = ROOT / "benchmark-results" / "unified_overnight" / "dashscope_mega_distillation.jsonl"
CHECKPOINT_DIR = ROOT / "sov-backup" / "checkpoints"
ADAPTER_DIR = CHECKPOINT_DIR / "qwen05b-lora-adapter"
RESULTS_FILE = ROOT / "oracle_lora_results.json"

# ---------------------------------------------------------------------------
# Hyperparameters (conservative for 956MB RAM)
# ---------------------------------------------------------------------------
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
TARGET_MODULES = ["q_proj", "k_proj", "v_proj", "o_proj"]
NUM_EPOCHS = 3
BATCH_SIZE = 1
GRADIENT_ACCUMULATION = 8  # effective batch = 8
LEARNING_RATE = 2e-4
MAX_SEQ_LENGTH = 256
SAVE_STEPS = 50
LOGGING_STEPS = 10
WARMUP_RATIO = 0.05
WEIGHT_DECAY = 0.01
FP16 = False  # ARM CPU — no fp16
BF16 = False  # ARM CPU — no bf16

# ---------------------------------------------------------------------------
# 9 evaluation domains
# ---------------------------------------------------------------------------
EVAL_DOMAINS = [
    "math_reasoning",
    "code_generation",
    "instruction_following",
    "creative_writing",
    "factual_qa",
    "summarization",
    "classification",
    "conversation",
    "translation",
]


def banner(msg: str):
    log.info("=" * 70)
    log.info(msg)
    log.info("=" * 70)


def check_system():
    """Verify environment and available resources."""
    banner("SYSTEM CHECK")
    import platform
    log.info("Platform: %s %s", platform.system(), platform.machine())
    log.info("Python: %s", sys.version)

    # Memory
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    log.info("RAM: %s", line.strip())
                    break
    except FileNotFoundError:
        log.info("RAM: (non-linux, skipping meminfo)")

    # Disk
    try:
        st = os.statvfs(str(ROOT))
        free_gb = (st.f_bavail * st.f_frsize) / (1024 ** 3)
        log.info("Disk free: %.1f GB", free_gb)
        if free_gb < 5:
            log.warning("Low disk! Only %.1f GB free — may fail.", free_gb)
    except Exception:
        pass


def install_deps():
    """Install required packages if missing."""
    banner("DEPENDENCY CHECK")
    pkgs = [
        "torch",
        "transformers",
        "peft",
        "trl",
        "datasets",
        "accelerate",
        "bitsandbytes",
    ]
    for pkg in pkgs:
        try:
            __import__(pkg)
            log.info("✓ %s", pkg)
        except ImportError:
            log.info("Installing %s ...", pkg)
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--quiet", pkg
            ])


def load_data() -> list[dict]:
    """Load distillation JSONL data."""
    banner("LOADING DATA")
    if not DATA_PATH.exists():
        log.error("Data file not found: %s", DATA_PATH)
        sys.exit(1)

    records = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                log.warning("Skipping malformed line %d", i)

    log.info("Loaded %d records from %s", len(records), DATA_PATH)
    return records


def format_for_sft(records: list[dict]) -> list[dict]:
    """
    Convert raw records into chat-format dicts for SFTTrainer.
    Expected format: {"messages": [{"role": ..., "content": ...}, ...]}
    """
    formatted = []
    for rec in records:
        messages = []

        # Handle various data formats
        if "messages" in rec:
            messages = rec["messages"]
        elif "instruction" in rec and "output" in rec:
            messages = [
                {"role": "user", "content": rec["instruction"]},
                {"role": "assistant", "content": rec["output"]},
            ]
        elif "prompt" in rec and "response" in rec:
            messages = [
                {"role": "user", "content": rec["prompt"]},
                {"role": "assistant", "content": rec["response"]},
            ]
        elif "question" in rec and "answer" in rec:
            messages = [
                {"role": "user", "content": rec["question"]},
                {"role": "assistant", "content": rec["answer"]},
            ]
        elif "input" in rec and "output" in rec:
            user_content = rec["input"]
            if "instruction" in rec:
                user_content = rec["instruction"] + "\n" + user_content
            messages = [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": rec["output"]},
            ]

        if messages:
            formatted.append({"messages": messages})

    log.info("Formatted %d / %d records for SFT", len(formatted), len(records))
    return formatted


def load_model_and_tokenizer():
    """Load Qwen2.5-0.5B-Instruct and tokenizer with memory optimizations."""
    banner("LOADING MODEL")
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    log.info("Loading tokenizer: %s", MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
        padding_side="right",
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    log.info("Loading model: %s (this may take a few minutes on ARM)", MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,  # ARM CPU needs fp32
        device_map="cpu",
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    model.config.use_cache = False  # needed for gradient checkpointing

    param_count = sum(p.numel() for p in model.parameters())
    log.info("Model loaded — %d parameters (%.1fM)", param_count, param_count / 1e6)

    gc.collect()
    return model, tokenizer


def apply_lora(model):
    """Wrap model with LoRA adapter."""
    banner("APPLYING LoRA")
    from peft import LoraConfig, get_peft_model, TaskType

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        target_modules=TARGET_MODULES,
        bias="none",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    return model


def train(model, tokenizer, dataset):
    """Run SFT training."""
    banner("STARTING TRAINING")
    from trl import SFTTrainer, SFTConfig

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)

    training_args = SFTConfig(
        output_dir=str(CHECKPOINT_DIR),
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION,
        learning_rate=LEARNING_RATE,
        lr_scheduler_type="cosine",
        warmup_ratio=WARMUP_RATIO,
        weight_decay=WEIGHT_DECAY,
        max_seq_length=MAX_SEQ_LENGTH,
        logging_steps=LOGGING_STEPS,
        save_steps=SAVE_STEPS,
        save_total_limit=3,
        fp16=FP16,
        bf16=BF16,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        report_to="none",
        optim="adamw_torch",
        dataloader_pin_memory=False,
        remove_unused_columns=True,
        seed=42,
        max_grad_norm=1.0,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )

    log.info("Trainer initialized. Training on %d samples.", len(dataset))
    log.info("Effective batch size: %d × %d = %d",
             BATCH_SIZE, GRADIENT_ACCUMULATION,
             BATCH_SIZE * GRADIENT_ACCUMULATION)

    gc.collect()

    try:
        result = trainer.train()
        log.info("Training complete! Train loss: %.4f", result.training_loss)
    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            log.error("OOM during training! Try reducing batch size or seq length.")
            gc.collect()
            raise
        raise

    # Save adapter
    log.info("Saving LoRA adapter to %s", ADAPTER_DIR)
    model.save_pretrained(str(ADAPTER_DIR))
    tokenizer.save_pretrained(str(ADAPTER_DIR))
    log.info("Adapter saved successfully.")

    return result


def evaluate_domains(records: list[dict]) -> dict:
    """Evaluate the fine-tuned model on each of the 9 domains."""
    banner("EVALUATING ON 9 DOMAINS")
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

    # Group records by domain
    domain_data: dict[str, list[dict]] = {d: [] for d in EVAL_DOMAINS}
    for rec in records:
        domain = rec.get("domain", rec.get("category", ""))
        if domain in domain_data:
            domain_data[domain].append(rec)

    # If no domain field, distribute evenly
    if all(len(v) == 0 for v in domain_data.values()):
        log.warning("No 'domain' field found — distributing evenly across domains")
        chunk = max(1, len(records) // len(EVAL_DOMAINS))
        for i, d in enumerate(EVAL_DOMAINS):
            domain_data[d] = records[i * chunk: (i + 1) * chunk]

    # Load base model for comparison
    log.info("Loading base model for comparison...")
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        device_map="cpu",
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    base_model.eval()

    # Load fine-tuned model
    log.info("Loading fine-tuned model with adapter...")
    ft_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        device_map="cpu",
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    ft_model = PeftModel.from_pretrained(ft_model, str(ADAPTER_DIR))
    ft_model.eval()

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME, trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    gen_config = GenerationConfig(
        max_new_tokens=128,
        do_sample=False,
        temperature=1.0,
        pad_token_id=tokenizer.pad_token_id,
    )

    results = {}

    for domain in EVAL_DOMAINS:
        samples = domain_data.get(domain, [])
        if not samples:
            log.info("  %s: no samples — skipping", domain)
            results[domain] = {"count": 0, "base_scores": [], "ft_scores": []}
            continue

        # Take up to 5 samples per domain for eval
        eval_samples = samples[:5]
        base_scores = []
        ft_scores = []

        log.info("  Evaluating %s (%d samples)...", domain, len(eval_samples))

        for sample in eval_samples:
            # Extract user prompt
            user_msg = ""
            expected = ""
            if "messages" in sample:
                for m in sample["messages"]:
                    if m.get("role") == "user":
                        user_msg = m["content"]
                    elif m.get("role") == "assistant":
                        expected = m["content"]
            elif "instruction" in sample:
                user_msg = sample["instruction"]
                expected = sample.get("output", "")
            elif "prompt" in sample:
                user_msg = sample["prompt"]
                expected = sample.get("response", "")
            elif "question" in sample:
                user_msg = sample["question"]
                expected = sample.get("answer", "")

            if not user_msg:
                continue

            messages = [{"role": "user", "content": user_msg}]
            prompt_text = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = tokenizer(prompt_text, return_tensors="pt", truncation=True,
                               max_length=MAX_SEQ_LENGTH)

            # Base model generation
            with torch.no_grad():
                base_out = base_model.generate(**inputs, generation_config=gen_config)
                base_text = tokenizer.decode(
                    base_out[0][inputs["input_ids"].shape[-1]:],
                    skip_special_tokens=True,
                )

            # Fine-tuned model generation
            with torch.no_grad():
                ft_out = ft_model.generate(**inputs, generation_config=gen_config)
                ft_text = tokenizer.decode(
                    ft_out[0][inputs["input_ids"].shape[-1]:],
                    skip_special_tokens=True,
                )

            # Simple scoring: response length ratio to expected
            def score(response: str, reference: str) -> float:
                if not reference:
                    return 1.0 if len(response) > 10 else 0.0
                # Character overlap ratio (simple heuristic)
                ref_chars = set(reference.lower().split())
                resp_chars = set(response.lower().split())
                if not ref_chars:
                    return 0.5
                overlap = len(ref_chars & resp_chars) / len(ref_chars)
                return min(1.0, overlap)

            base_scores.append(score(base_text, expected))
            ft_scores.append(score(ft_text, expected))

            gc.collect()

        avg_base = sum(base_scores) / len(base_scores) if base_scores else 0
        avg_ft = sum(ft_scores) / len(ft_scores) if ft_scores else 0
        delta = avg_ft - avg_base

        log.info("    %s — base: %.3f  ft: %.3f  Δ: %+.3f",
                 domain, avg_base, avg_ft, delta)

        results[domain] = {
            "count": len(eval_samples),
            "base_avg": round(avg_base, 4),
            "ft_avg": round(avg_ft, 4),
            "delta": round(delta, 4),
            "base_scores": [round(s, 4) for s in base_scores],
            "ft_scores": [round(s, 4) for s in ft_scores],
        }

        # Free memory between domains
        gc.collect()

    # Cleanup eval models
    del base_model, ft_model
    gc.collect()

    return results


def push_to_github():
    """Commit and push results to GitHub."""
    banner("PUSHING TO GITHUB")
    try:
        os.chdir(ROOT)
        subprocess.run(["git", "add", "."], check=False)
        msg = f"oracle-lora: train + eval @ {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        subprocess.run(["git", "commit", "-m", msg], check=False)
        result = subprocess.run(
            ["git", "push"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            log.info("Pushed to GitHub successfully.")
        else:
            log.warning("git push returned %d: %s", result.returncode, result.stderr)
    except Exception as e:
        log.warning("GitHub push failed: %s", e)


def main():
    start = time.time()
    banner(f"ORACLE LORA TRAINING — {datetime.now().isoformat()}")

    check_system()
    install_deps()

    # 1. Load and format data
    records = load_data()
    formatted = format_for_sft(records)
    if not formatted:
        log.error("No valid training samples. Exiting.")
        sys.exit(1)

    # 2. Load model + tokenizer
    model, tokenizer = load_model_and_tokenizer()

    # 3. Apply LoRA
    model = apply_lora(model)

    # 4. Train
    from datasets import Dataset
    dataset = Dataset.from_list(formatted)
    train_result = train(model, tokenizer, dataset)

    # 5. Evaluate
    eval_results = evaluate_domains(records)

    # 6. Save overall results
    overall = {
        "timestamp": datetime.now().isoformat(),
        "model": MODEL_NAME,
        "lora_r": LORA_R,
        "lora_alpha": LORA_ALPHA,
        "epochs": NUM_EPOCHS,
        "batch_size": BATCH_SIZE,
        "effective_batch": BATCH_SIZE * GRADIENT_ACCUMULATION,
        "learning_rate": LEARNING_RATE,
        "max_seq_length": MAX_SEQ_LENGTH,
        "training_loss": float(train_result.training_loss) if hasattr(train_result, "training_loss") else None,
        "train_runtime_seconds": round(time.time() - start, 1),
        "domains": eval_results,
    }

    # Compute overall delta
    all_base = []
    all_ft = []
    for d in eval_results.values():
        all_base.extend(d.get("base_scores", []))
        all_ft.extend(d.get("ft_scores", []))

    if all_base and all_ft:
        overall["overall_base_avg"] = round(sum(all_base) / len(all_base), 4)
        overall["overall_ft_avg"] = round(sum(all_ft) / len(all_ft), 4)
        overall["overall_delta"] = round(overall["overall_ft_avg"] - overall["overall_base_avg"], 4)

    with open(RESULTS_FILE, "w") as f:
        json.dump(overall, f, indent=2)
    log.info("Results saved to %s", RESULTS_FILE)

    # 7. Push to GitHub
    push_to_github()

    elapsed = time.time() - start
    banner(f"DONE in {elapsed / 60:.1f} minutes")
    log.info("Adapter: %s", ADAPTER_DIR)
    log.info("Results: %s", RESULTS_FILE)
    log.info("Log: %s", LOG_FILE)


if __name__ == "__main__":
    main()
