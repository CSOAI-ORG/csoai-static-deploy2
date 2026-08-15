#!/usr/bin/env python3
"""
SOV Inference Server — Simple, reliable, no Ollama dependency.
Uses transformers + FastAPI for production inference.

Usage:
  python3 sov_server.py --model Qwen/Qwen2.5-3B-Instruct
  python3 sov_server.py --model Qwen/Qwen2.5-7B-Instruct --port 8080
"""
import json, time, argparse
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Will be loaded on startup
model = None
tokenizer = None

app = FastAPI(title="SOV Inference Server")

class ChatRequest(BaseModel):
    model: str = "default"
    messages: list
    temperature: float = 0
    max_tokens: int = 512

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: list
    usage: dict

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """OpenAI-compatible chat completions endpoint."""
    import torch
    
    prompt = request.messages[-1]["content"] if request.messages else ""
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    start = time.time()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            do_sample=request.temperature > 0
        )
    latency = (time.time() - start) * 1000
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return ChatResponse(
        id=f"sov-{int(time.time())}",
        choices=[{
            "index": 0,
            "message": {"role": "assistant", "content": response},
            "finish_reason": "stop"
        }],
        usage={
            "prompt_tokens": inputs["input_ids"].shape[1],
            "completion_tokens": outputs.shape[1] - inputs["input_ids"].shape[1],
            "total_tokens": outputs.shape[1]
        }
    )

@app.get("/v1/models")
async def list_models():
    """List available models."""
    return {
        "object": "list",
        "data": [{"id": "sov", "object": "model", "owned_by": "CSOAI"}]
    }

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok", "model": model.config._name_or_path if model else "none"}

def load_model(model_name: str):
    """Load model on startup."""
    global model, tokenizer
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    print(f"Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    print(f"Model loaded: {model_name}")
    print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    
    load_model(args.model)
    uvicorn.run(app, host="0.0.0.0", port=args.port)
