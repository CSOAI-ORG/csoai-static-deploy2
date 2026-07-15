#!/usr/bin/env python3
"""sov33_modal_train.py — fine-tune SOV's OWN weights on the 113 distilled pairs, on a Modal GPU.

WHAT THIS IS (honest): a real LoRA fine-tune of a SMALL open base (Qwen2.5-0.5B/1.5B) on the
verified 113-pair sovereign distillation corpus. It produces SOV's OWN adapter weights — the
sovereign 'voice' distilled from the 70B teacher, carrying the governance/citation style.

WHAT THIS IS NOT: this does NOT train a 1.6T model. Training a T-scale model from scratch is
infeasible (hundreds of $M compute). The honest T path is SEPARATE: route/serve a real open
1.6T base (DeepSeek V4, funded) as the CORE brain, and wrap it in SOV governance. This script
makes the SMALL sovereign student; the T-core is a serving/routing choice, not a training one.

RUN (owner, ~£ pennies-to-a-few-pounds on Modal):
  pip install modal && modal token new         # owner sets token (once)
  modal run sov33_modal_train.py               # dispatches the GPU job, downloads adapter
"""
import os

try:
    import modal
except ImportError:
    modal = None

STUB = modal.App("sov33-sovereign-train") if modal else None
DATA = os.environ.get("SOV_DATA", "expert_data/merged_corpus.jsonl")   # merged local corpus (1289 rows); override via SOV_DATA
BASE = os.environ.get("SOV_BASE", "Qwen/Qwen2.5-0.5B-Instruct")

if modal:
    image = (modal.Image.debian_slim()
             .pip_install("torch","transformers>=4.44","peft","trl","datasets","accelerate","bitsandbytes"))

    @STUB.function(gpu="T4", image=image, timeout=3600)
    def train(pairs: list):
        import torch, json, tempfile
        from datasets import Dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import LoraConfig, get_peft_model
        from trl import SFTConfig, SFTTrainer
        tok = AutoTokenizer.from_pretrained(BASE); tok.pad_token = tok.pad_token or tok.eos_token
        def fmt(r): return {"text": f"<|user|>\n{r['instruction']}\n<|assistant|>\n{r['response']}"}
        ds = Dataset.from_list([fmt(p) for p in pairs])
        model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float16, device_map="auto")
        model = get_peft_model(model, LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj","k_proj","v_proj","o_proj"], lora_dropout=0.05, task_type="CAUSAL_LM"))
        cfg = SFTConfig(output_dir="/tmp/sov_out", per_device_train_batch_size=2, gradient_accumulation_steps=4,
                        num_train_epochs=3, learning_rate=2e-4, fp16=True, max_seq_length=1024, logging_steps=5, report_to=[])
        tr = SFTTrainer(model=model, train_dataset=ds, args=cfg); tr.train()
        model.save_pretrained("/tmp/sov_out"); 
        import io, base64, tarfile
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as t: t.add("/tmp/sov_out", arcname="sov_adapter")
        return base64.b64encode(buf.getvalue()).decode()

    @STUB.local_entrypoint()
    def main():
        import json, base64
        pairs = [json.loads(l) for l in open(DATA) if l.strip()]
        print(f"[modal] training SOV student on {len(pairs)} pairs, base={BASE}")
        b64 = train.remote(pairs)
        open("sov_adapter.tar.gz","wb").write(base64.b64decode(b64))
        print("[modal] DONE -> sov_adapter.tar.gz (SOV's own weights). Untar + point sovereign at it.")
else:
    if __name__ == "__main__":
        print("Modal not installed. Owner: pip install modal && modal token new && modal run sov33_modal_train.py")
        print(f"Will train on {DATA} (113 pairs), base {BASE}, T4 GPU, ~3 epochs LoRA -> SOV's own adapter.")
