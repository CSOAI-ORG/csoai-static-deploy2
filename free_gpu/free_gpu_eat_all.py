#!/usr/bin/env python3
"""
FREE GPU EAT ALL — Extraction-Augmented Training across ALL 19 model families.
Uses free-tier APIs (Groq, OpenRouter, NVIDIA) + optional Kaggle T4 GPU.

Usage:
  # API extraction (no GPU needed, uses free API tiers)
  python3 free_gpu/free_gpu_eat_all.py --mode api --families all

  # Kaggle T4 GPU extraction (run inside Kaggle notebook)
  python3 free_gpu/free_gpu_eat_all.py --mode kaggle --families qwen,llama,deepseek

  # Resume interrupted extraction
  python3 free_gpu/free_gpu_eat_all.py --mode api --resume

Output: eat_results/free_gpu_eat_all.json + per-family extract files
"""
import json, os, sys, time, re, hashlib
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
EAT_DIR = ROOT / "eat_results"
FREE_GPU_DIR = ROOT / "free_gpu"
EAT_DIR.mkdir(exist_ok=True)

STRIP_THINK = re.compile(r"<think>.*?</think>|<thinking>.*?</thinking>", re.IGNORECASE | re.DOTALL)

FAMILIES = {
    "qwen": "Qwen architecture, MoE, training data sizes, multilingual support",
    "deepseek": "DeepSeek architecture, V3, R1, reasoning, distillation",
    "llama": "Llama architecture, Meta AI, open-weight, instruction tuning, safety",
    "mistral": "Mistral architecture, MoE, Mixtral, coding, multilingual",
    "gemma": "Gemma architecture, Google, lightweight, responsible AI, Keras",
    "phi": "Phi architecture, Microsoft, small language models, textbook quality data",
    "gpt-oss": "Open-source GPT architectures, transformer, decoder-only, attention",
    "code": "Code-focused models, CodeLlama, DeepSeek Coder, StarCoder, Qwen Coder",
    "vision": "Vision-language models, LLaVA, Qwen-VL, multimodal, image understanding",
    "embedding": "Embedding models, text embeddings, sentence transformers, semantic search",
    "qwen-vision": "Qwen vision-language, Qwen-VL, Qwen2.5-VL, visual QA",
    "MiniMax": "MiniMax architecture, MiniMax-01, linear attention, lightning attention",
    "nemotron": "Nemotron architecture, NVIDIA, MoE, reward modeling, synthetic data",
    "core": "EU AI Act compliance, GDPR, ISO 42001, AUKUS, NATO DASA, NCSC CAF framework",
    "research": "AI research methodology, benchmarks, evaluation, safety research, alignment",
    "arch": "Neural architecture, transformer variants, MoE, SSM, linear attention design",
    "compliance": "Regulatory compliance, AI governance frameworks, audit procedures, risk classification",
    "distribution": "Model distribution, HuggingFace Hub, ONNX, GGUF, quantization deployment",
    "infra": "AI infrastructure, serving, vLLM, Ollama, Kubernetes, GPU orchestration",
}
FAMILY_ORDER = sorted(FAMILIES.keys())

QUESTIONS_PER_FAMILY = {
    f: [
        f"What is {f} and its key architectural innovations?",
        f"Describe the training methodology used in {f} models.",
        f"What are the main strengths and limitations of {f}?",
        f"How does {f} compare to other model families in its class?",
        f"What benchmark performance does {f} achieve on standard tasks?",
        f"Explain the tokenizer and vocabulary design in {f}.",
        f"What context length does {f} support and how was it achieved?",
        f"How does {f} handle multilingual or cross-lingual tasks?",
        f"What safety or alignment techniques were used in {f}?",
        f"Describe the training data composition for {f}.",
        f"What hardware was used to train {f} and what was the cost?",
        f"How does {f} approach instruction following and chat?",
        f"What quantization or compression methods work well with {f}?",
        f"Explain the attention mechanism used in {f}.",
        f"What is the parameter count range for {f} models?",
        f"How does {f} handle long document understanding?",
        f"What evaluation benchmarks are most relevant for {f}?",
        f"Describe the model family tree and variants of {f}.",
        f"What are the commercial or licensing terms for {f}?",
        f"How does {f} approach few-shot and zero-shot learning?",
        f"What inference optimizations are available for {f}?",
        f"How does {f} compare with closed-source alternatives like GPT-4?",
        f"What fine-tuning approaches work best for {f}?",
        f"Describe the tool use and function calling capabilities in {f}.",
        f"What are the known limitations or failure modes of {f}?",
    ]
    for f in FAMILIES
}

PROVIDERS = []


def detect_providers():
    """Detect which free API providers are available."""
    global PROVIDERS
    available = []
    if os.environ.get("GROQ_API_KEY"):
        available.append("groq")
    if os.environ.get("OPENROUTER_API_KEY"):
        available.append("openrouter")
    if os.environ.get("NVIDIA_API_KEY"):
        available.append("nvidia")
    if os.environ.get("GOOGLE_API_KEY"):
        available.append("gemini")
    try:
        import torch
        if torch.cuda.is_available():
            available.append("kaggle_gpu")
    except ImportError:
        pass
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            available.append("ollama")
    except Exception:
        pass
    PROVIDERS = available
    return available


def call_groq(prompt, model="llama-3.3-70b-versatile"):
    import requests
    key = os.environ["GROQ_API_KEY"]
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 512, "temperature": 0.3},
        timeout=60,
    )
    if r.status_code == 200:
        return STRIP_THINK.sub("", r.json()["choices"][0]["message"]["content"]).strip()
    return None


def call_openrouter(prompt, model="google/gemma-4-26b-a4b-it:free"):
    import requests
    key = os.environ["OPENROUTER_API_KEY"]
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 512, "temperature": 0.3},
        timeout=60,
    )
    if r.status_code == 200:
        return STRIP_THINK.sub("", r.json()["choices"][0]["message"]["content"]).strip()
    return None


def call_nvidia(prompt, model="meta/llama-3.1-70b-instruct"):
    import requests
    key = os.environ["NVIDIA_API_KEY"]
    r = requests.post(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 512, "temperature": 0.3},
        timeout=60,
    )
    if r.status_code == 200:
        return STRIP_THINK.sub("", r.json()["choices"][0]["message"]["content"]).strip()
    return None


def call_ollama(prompt, model="qwen2.5:0.5b"):
    import requests
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.3, "num_predict": 512}},
        timeout=120,
    )
    if r.status_code == 200:
        return STRIP_THINK.sub("", r.json().get("response", "")).strip()
    return None


def extract(family, question, providers):
    """Try each provider in order until one succeeds."""
    prompt = f"You are an expert on {FAMILIES[family]}. Answer concisely but thoroughly.\n\nQuestion: {question}"
    for provider in providers:
        try:
            if provider == "groq":
                for m in ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "qwen/qwen3-32b"]:
                    ans = call_groq(prompt, m)
                    if ans and len(ans) > 20:
                        return ans, f"groq/{m}"
            elif provider == "openrouter":
                for m in ["google/gemma-4-26b-a4b-it:free", "nvidia/nemotron-3-ultra-550b-a55b:free", "deepseek/deepseek-v4-pro:free"]:
                    ans = call_openrouter(prompt, m)
                    if ans and len(ans) > 20:
                        return ans, f"openrouter/{m}"
            elif provider == "nvidia":
                ans = call_nvidia(prompt)
                if ans and len(ans) > 20:
                    return ans, "nvidia/llama-3.1-70b"
            elif provider == "ollama":
                ans = call_ollama(prompt)
                if ans and len(ans) > 20:
                    return ans, "ollama/local"
        except Exception as e:
            continue
    return None, None


def run_api_extraction(families, resume=False):
    """Extract using free API providers (no GPU needed)."""
    results_path = EAT_DIR / "free_gpu_eat_all.json"
    existing = []
    if resume and results_path.exists():
        existing = json.loads(results_path.read_text())
        done = {(e["family"], e["q"]) for e in existing}
        print(f"Resuming: {len(existing)} existing entries loaded")
    else:
        done = set()

    providers = detect_providers()
    print(f"Available providers: {providers}")
    if not providers:
        print("ERROR: No API providers available. Set GROQ_API_KEY or OPENROUTER_API_KEY")
        sys.exit(1)

    results = list(existing)
    total = len(families) * QUESTIONS_PER_FAMILY[families[0]]
    count = 0

    for family in families:
        family_dir = EAT_DIR / f"extract_{family}.json"
        family_results = []
        if family_dir.exists():
            family_results = json.loads(family_dir.read_text())

        for q in QUESTIONS_PER_FAMILY[family]:
            count += 1
            if (family, q) in done:
                print(f"  [{count}/{total}] SKIP {family} — already extracted")
                continue

            print(f"  [{count}/{total}] {family} → {q[:60]}...", end=" ", flush=True)
            ans, source = extract(family, q, providers)

            if ans:
                entry = {"q": q, "a": ans, "family": family, "ok": True, "source": source, "ts": datetime.now().isoformat()}
                results.append(entry)
                family_results.append({"q": q, "a": ans, "family": family})
                print(f"✓ ({len(ans)} chars from {source})")
            else:
                entry = {"q": q, "a": "", "family": family, "ok": False, "ts": datetime.now().isoformat()}
                results.append(entry)
                print("✗ (failed)")

            # Save incrementally
            json.dump(results, open(results_path, "w"), indent=2)
            json.dump(family_results, open(family_dir, "w"), indent=2)

            # Rate limit: 2 seconds between calls
            time.sleep(2)

    print(f"\nDone! {len(results)} total entries across {len(families)} families")
    return results


def run_kaggle_extraction(families):
    """Extract using Kaggle T4 GPU (run inside Kaggle notebook)."""
    print("=" * 60)
    print("  KAGGLE T4 GPU EXTRACTION MODE")
    print("=" * 60)
    try:
        import torch
        if not torch.cuda.is_available():
            print("WARNING: No GPU detected. Run this inside a Kaggle notebook with GPU T4x2 enabled.")
            print("Copy this script to Kaggle and enable GPU accelerator.")
            return
        print(f"GPU: {torch.cuda.get_device_name(0)} — {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB VRAM")
    except ImportError:
        print("torch not available — are you in a Kaggle notebook?")
        return

    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    print(f"Loading {model_name} on GPU...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype="auto", device_map="auto"
    )
    results_path = EAT_DIR / "free_gpu_eat_all.json"
    results = []

    for family in families:
        print(f"\n--- {family} ---")
        for q in QUESTIONS_PER_FAMILY[family]:
            prompt = f"You are an expert on {FAMILIES[family]}. Answer concisely.\n\nQuestion: {q}"
            messages = [{"role": "user", "content": prompt}]
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(text, return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.3, do_sample=True)
            ans = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
            entry = {"q": q, "a": ans, "family": family, "ok": bool(ans), "source": f"kaggle/{model_name}"}
            results.append(entry)
            status = "✓" if ans else "✗"
            print(f"  {status} {q[:50]}... -> {len(ans)} chars")

    json.dump(results, open(results_path, "w"), indent=2)
    print(f"\nKaggle extraction complete: {len(results)} entries")


def show_coverage():
    """Show current coverage across all families."""
    results_path = EAT_DIR / "free_gpu_eat_all.json"
    if not results_path.exists():
        print("No free_gpu_eat_all.json found. Run extraction first.")
        return

    results = json.loads(results_path.read_text())
    by_family = {}
    for e in results:
        by_family.setdefault(e["family"], {"total": 0, "ok": 0})
        by_family[e["family"]]["total"] += 1
        if e.get("ok"):
            by_family[e["family"]]["ok"] += 1

    print(f"\n{'='*60}")
    print(f"  FREE GPU EAT ALL — Coverage Report")
    print(f"{'='*60}")
    print(f"  {'Family':20s} {'Extracted':>10s} {'OK':>6s} {'Coverage':>10s}")
    print(f"  {'-'*46}")
    for f in FAMILY_ORDER:
        if f in by_family:
            c = by_family[f]
            pct = 100 * c["ok"] / len(QUESTIONS_PER_FAMILY[f])
        else:
            c = {"total": 0, "ok": 0}
            pct = 0
        bar = "█" * int(pct / 5)
        print(f"  {f:20s} {c['total']:10d} {c['ok']:6d} {pct:8.0f}%  {bar}")

    total_ok = sum(c["ok"] for c in by_family.values())
    total_qs = len(FAMILIES) * len(QUESTIONS_PER_FAMILY[FAMILY_ORDER[0]])
    print(f"  {'-'*46}")
    print(f"  {'TOTAL':20s} {sum(c['total'] for c in by_family.values()):10d} {total_ok:6d} {100*total_ok/total_qs:7.0f}%")
    print(f"\n  Target: {total_qs} Q/A pairs across {len(FAMILIES)} families")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Free GPU EAT ALL")
    parser.add_argument("--mode", choices=["api", "kaggle", "coverage"], default="coverage")
    parser.add_argument("--families", default="all", help="Comma-separated families or 'all'")
    parser.add_argument("--resume", action="store_true", help="Resume interrupted extraction")
    args = parser.parse_args()

    if args.families == "all":
        families = FAMILY_ORDER
    else:
        families = [f.strip() for f in args.families.split(",") if f.strip() in FAMILIES]

    print(f"\n{'='*60}")
    print(f"  FREE GPU EAT ALL")
    print(f"  Mode: {args.mode}")
    print(f"  Families: {len(families)} — {', '.join(families)}")
    print(f"{'='*60}\n")

    if args.mode == "api":
        run_api_extraction(families, resume=args.resume)
    elif args.mode == "kaggle":
        run_kaggle_extraction(families)
    else:
        show_coverage()


if __name__ == "__main__":
    main()
