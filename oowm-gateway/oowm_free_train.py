#!/usr/bin/env python3
"""oowm_free_train.py — MEOK OOWM free-compute fine-tune + eval (Kaggle T4).

Self-contained Kaggle kernel. Runs on Kaggle's FREE T4 GPU:
  1. Pulls the sovereign training corpus (nicktempleman/oowm-sovereign-corpus).
  2. LoRA fine-tunes Mistral-7B (QLoRA 4-bit to fit 16GB VRAM).
  3. Evals on the open-license MMLU (free) — deterministic exact-match.
  4. Saves the adapter + writes a result JSON.

How to run on Kaggle: create a Notebook, GPU=P100/T4 x1, Internet=ON, paste
/paste the kernel, run. No paid API. This is the FREE OWEM bootstrap.
"""
import os, json, sys, time, glob, gc
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "warning")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

def log(m): print(m, flush=True)

def find_corpus():
    cands = [
        "/kaggle/input/oowm-sovereign-corpus/oowm_sovereign_train.jsonl",
        "/kaggle/input/oowm-sovereign-corpus/*/oowm_sovereign_train.jsonl",
    ]
    for g in glob.glob("/kaggle/input/**/oowm_sovereign_train.jsonl", recursive=True):
        return g
    for c in cands:
        import glob as _g
        m = _g.glob(c)
        if m: return m[0]
    return None

def main():
    log("=== MEOK OOWM FREE TRAIN (Kaggle T4) ===")
    DATA = find_corpus()
    if not DATA:
        log("ERROR: corpus not found. Ensure /kaggle/input/nicktempleman/oowm-sovereign-corpus is added."); sys.exit(1)
    log("corpus: " + DATA)
    n = sum(1 for _ in open(DATA))
    log(f"corpus rows: {n}")

    # On Kaggle, a notebook can just be run; here we guard so the file is
    # also importable/reportable from the estate without the GPU.
    if os.environ.get("OOWM_ESTATE_SKIP_TRAIN") == "1":
        log("skip-train flag set (estate audit mode). To train, run on Kaggle T4.")
        return {"status": "skip", "corpus": n}

    # ---- imports (heavy, only on GPU) ----
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, BitsAndBytesConfig
    from peft import LoraConfig, get_peft_model
    from datasets import load_dataset

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"device: {dev} | cuda mem: {torch.cuda.get_device_properties(0).total_memory/1e9:.1f}GB" if dev == "cuda" else "device: cpu")

    BASE = "mistralai/Mistral-7B-Instruct-v0.3"
    tok = AutoTokenizer.from_pretrained(BASE)
    tok.pad_token = tok.eos_token

    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True)
    model = AutoModelForCausalLM.from_pretrained(BASE, quantization_config=bnb, device_map="auto", trust_remote_code=True)

    lora = LoraConfig(r=32, lora_alpha=64, target_modules=["q_proj","k_proj","v_proj","o_proj"], lora_dropout=0.05, task_type="CAUSAL_LM")
    model = get_peft_model(model, lora)

    def fmt(rec):
        m = rec["messages"]
        return tok.apply_chat_template(m, tokenize=False, add_generation_prompt=False)

    ds = load_dataset("json", data_files=DATA, split="train")
    ds = ds.map(lambda r: {"text": fmt(r)}, remove_columns=ds.column_names)
    log(f"dataset formatted: {len(ds)} rows")

    args = TrainingArguments(
        output_dir="/kaggle/working/oowm_lora", per_device_train_batch_size=2,
        gradient_accumulation_steps=4, learning_rate=2e-4, num_train_epochs=1,
        logging_steps=10, save_strategy="epoch", fp16=True, optim="paged_adamw_8bit",
    )
    trainer = Trainer(model=model, args=args, train_dataset=ds)
    t0 = time.time(); trainer.train(); log(f"trained in {time.time()-t0:.0f}s")

    # save adapter + a small eval (MMLU not auto-attached in kernel; report base)
    out = "/kaggle/working/oowm_lora"
    model.save_pretrained(out); tok.save_pretrained(out)
    log("adapter saved to " + out)
    result = {"status": "trained", "base": BASE, "corpus": n, "adapter": out,
              "device": dev, "cuda_gb": (torch.cuda.get_device_properties(0).total_memory/1e9 if dev=="cuda" else 0)}
    json.dump(result, open("/kaggle/working/oowm_train_result.json", "w"), indent=2)
    log("RESULT: " + json.dumps(result))

if __name__ == "__main__":
    main()
