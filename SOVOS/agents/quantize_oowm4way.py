"""quantize_oowm4way.py — quantize oowm-4way to Q4_K_M via llama-cpp-python.

Bypasses ollama's broken safetensors→GGUF conversion by using
llama.cpp's C quantizer directly. The input is the materialised
merged safetensors; the output is a Q4_K_M GGUF.
"""
from __future__ import annotations

import os
import sys
import shutil
from pathlib import Path

REPO = Path("/workspace/csoai-static-deploy2")
SRC = Path("/root/merge/oowm-4way")        # 943M safetensors
OUT_GGUF = Path("/root/merge/oowm-4way-q4km.gguf")

# Use llama-cpp-python's quantize function
sys.path.insert(0, "/usr/local/lib/python3.11/dist-packages")
import llama_cpp
# llama-cpp-python loads GGUF, not safetensors. We need to first
# convert safetensors → GGUF (FP16) then quantize.
# Easier: use llama-cpp-python's quantize_internal function on the
# existing model in memory after a one-shot load.
# But oowm-4way's safetensors won't load as a GGUF — it IS safetensors.

# So we use gguf-py's GGUFWriter to make an FP16 GGUF, then quantize.
sys.path.insert(0, "/usr/local/lib/python3.11/dist-packages")
import llama_cpp

print(f"Step 1: convert safetensors → FP16 GGUF via gguf-py")
import torch
from safetensors import safe_open
from gguf import GGUFWriter, GGMLQuantizationType

print(f"loading from {SRC}...")
tensors = {}
with safe_open(str(SRC / "model.safetensors"), framework="pt") as f:
    for k in f.keys():
        tensors[k] = f.get_tensor(k)
print(f"  loaded {len(tensors)} tensors")

# Get arch metadata from first tensor's shapes
emb_shape = tensors.get("model.embed_tokens.weight")
if emb_shape is None:
    raise RuntimeError("no embed_tokens.weight found")

# Write FP16 GGUF
writer = GGUFWriter(str(OUT_GGUF), arch="qwen2")
writer.add_context_length(2048)
writer.add_embedding_length(emb_shape.shape[1])
writer.add_block_count(24)
writer.add_feed_forward_length(4864)
writer.add_head_count(14)
writer.add_head_count_kv(2)
writer.add_layer_norm_rms_eps(1e-6)
writer.add_vocab_size(emb_shape.shape[0])

# Tokenizer metadata
import json
BASE_TOK = Path("/root/base_models/Qwen2.5-0.5B-Instruct")
for f in ["tokenizer.json", "tokenizer_config.json"]:
    src = BASE_TOK / f
    if src.exists():
        writer.add_string(f"tokenizer.ggml.{f.replace('.json', '')}", src.read_text())
# vocab.json — qwen2 uses BPE
vocab_path = BASE_TOK / "vocab.json"
if vocab_path.exists():
    vocab = json.loads(vocab_path.read_text())
    tokens = list(vocab.keys())
    scores = [0.0] * len(tokens)
    writer.add_token_list(tokens)
    writer.add_token_scores(scores)
merges_path = BASE_TOK / "merges.txt"
if merges_path.exists():
    writer.add_token_merges(merges_path.read_text().splitlines())
# tokenizer model name
writer.add_string("tokenizer.ggml.model", "gpt2")

# tensors
for name, t in tensors.items():
    gguf_name = name.replace("model.", "").replace(".weight", ".weight")
    t_fp16 = t.to(torch.float16).numpy()
    writer.add_tensor(gguf_name, t_fp16)

writer.write_header_to_file()
writer.write_kv_data_to_file()
writer.write_tensors_to_file()
writer.close()
print(f"  wrote FP16 GGUF: {OUT_GGUF}  ({OUT_GGUF.stat().st_size / 1024 / 1024:.1f} MB)")

# Step 2: quantize via llama-cpp-python's C quantizer
print()
print("Step 2: quantize to Q4_K_M")
# Use llama-cpp-python's quantize function
# llama_model_quantize_default is internal; use the higher-level API if available
# Try: llama_model_quantize(model_path, out_path, params)
try:
    params = llama_cpp.llama_model_quantize_params()
    params.ftype = 15  # LLAMA_FTYPE_MOSTLY_Q4_K_M
    params.nthread = 4
    rc = llama_cpp.llama_model_quantize(
        str(OUT_GGUF).encode(),
        str(OUT_GGUF).replace(".gguf", ".q4km.gguf").encode(),
        params,
    )
    print(f"  quantized: rc={rc}")
except Exception as e:
    print(f"  quantize failed: {e}")