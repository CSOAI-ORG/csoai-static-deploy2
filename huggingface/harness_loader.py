#!/usr/bin/env python3
"""
harness_loader.py — Shared model wrapper for benchmark harnesses.

Provides:
  - ModelCall      : HuggingFace transformers wrapper with caching + device map
  - VLLMCall       : vLLM-based fast inference (for HF Spaces / Kaggle T4)
  - APICall        : OpenAI-compatible API call (for hosted eval)
  - OllamaCall     : local Ollama HTTP caller (restored — referenced by sov33_staged/self_train)

Lazy-loads transformers/vllm; never imports them at module top level.
"""
from __future__ import annotations
import os, time, hashlib, json, re
from dataclasses import dataclass
from typing import Optional

# Force HF cache paths before any HF import
os.environ.setdefault("HF_HOME", os.path.expanduser("~/.cache/huggingface"))
os.environ.setdefault("TRANSFORMERS_CACHE", os.path.expanduser("~/.cache/huggingface"))
os.environ.setdefault("HF_DATASETS_CACHE", os.path.expanduser("~/.cache/huggingface/datasets"))

@dataclass
class ModelCall:
    """Generic HF transformers wrapper."""
    model_id: str
    device: str = "auto"
    default_max_new_tokens: Optional[int] = None
    torch_dtype: str = "auto"  # "auto", "float16", "bfloat16"
    quantize_4bit: bool = False
    _tok = None
    _mdl = None
    _device_resolved: str = "cpu"

    def __post_init__(self):
        # Lazy load on first call
        pass

    def _ensure_loaded(self):
        if self._mdl is not None: return
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM

        dtype = {"float16": torch.float16, "bfloat16": torch.bfloat16}.get(
            self.torch_dtype, torch.float16 if self.torch_dtype == "auto" else torch.float16)
        kwargs = dict(torch_dtype=dtype, trust_remote_code=True, device_map=self.device)
        if self.quantize_4bit:
            from transformers import BitsAndBytesConfig
            kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
            kwargs.pop("torch_dtype", None)

        print(f"[loader] {self.model_id} → {self.device} dtype={dtype} 4bit={self.quantize_4bit}")
        t0 = time.time()
        self._tok = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
        self._mdl = AutoModelForCausalLM.from_pretrained(self.model_id, **kwargs)
        if hasattr(self._mdl, "device"):
            self._device_resolved = str(self._mdl.device)
        print(f"[loader] loaded in {time.time()-t0:.1f}s on {self._device_resolved}")

    def __call__(self, prompt: str, max_new_tokens: Optional[int] = None) -> str:
        self._ensure_loaded()
        import torch
        mnt = max_new_tokens or self.default_max_new_tokens or 256
        inputs = self._tok(prompt, return_tensors="pt", truncation=True, max_length=4096).to(
            self._mdl.device)
        with torch.no_grad():
            out = self._mdl.generate(
                **inputs, max_new_tokens=mnt, do_sample=False,
                temperature=None, top_p=None, top_k=None,
                pad_token_id=self._tok.eos_token_id)
        text = self._tok.decode(out[0][inputs["input_ids"].shape[1]:],
                                skip_special_tokens=True)
        return text.strip()


@dataclass
class VLLMCall:
    """vLLM-based fast batch inference (used on Kaggle T4 with cuda 12.x)."""
    model_id: str
    max_model_len: int = 4096
    gpu_memory_utilization: float = 0.85
    _llm = None

    def _ensure_loaded(self):
        if self._llm is not None: return
        from vllm import LLM
        print(f"[vllm] loading {self.model_id}")
        self._llm = LLM(model=self.model_id, max_model_len=self.max_model_len,
                        gpu_memory_utilization=self.gpu_memory_utilization,
                        trust_remote_code=True)
        print(f"[vllm] ready")

    def __call__(self, prompt: str, max_new_tokens: int = 256) -> str:
        self._ensure_loaded()
        from vllm import SamplingParams
        sp = SamplingParams(temperature=0, max_tokens=max_new_tokens)
        out = self._llm.generate([prompt], sp)
        return out[0].outputs[0].text.strip()


@dataclass
class APICall:
    """OpenAI-compatible HTTP call (for HF Inference Endpoints, OpenRouter, etc)."""
    model_id: str
    base_url: str = "https://api.openai.com/v1"
    api_key: Optional[str] = None
    timeout: int = 60

    def __post_init__(self):
        if self.api_key is None:
            self.api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("HF_TOKEN")

    def __call__(self, prompt: str, max_new_tokens: int = 256) -> str:
        import urllib.request
        url = f"{self.base_url}/chat/completions"
        body = json.dumps({
            "model": self.model_id,
            "messages": [{"role":"user","content":prompt}],
            "max_tokens": max_new_tokens,
            "temperature": 0,
        }).encode()
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            resp = json.loads(r.read())
        return resp["choices"][0]["message"]["content"].strip()


@dataclass
class OllamaCall:
    """Local Ollama HTTP caller (Ollama server, default :11434)."""
    model_id: str
    use_chat: bool = True
    timeout: int = 60
    base_url: str = "http://localhost:11434"

    def __call__(self, prompt: str, max_new_tokens: int = 256) -> str:
        import urllib.request
        if self.use_chat:
            url = f"{self.base_url}/api/chat"
            body = json.dumps({
                "model": self.model_id,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"num_predict": max_new_tokens},
            }).encode()
        else:
            url = f"{self.base_url}/api/generate"
            body = json.dumps({
                "model": self.model_id,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": max_new_tokens},
            }).encode()
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Content-Type": "application/json",
        })
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            resp = json.loads(r.read())
        if self.use_chat:
            return resp["message"]["content"].strip()
        return resp["response"].strip()