#!/usr/bin/env python3
"""sov6_stack.py - SOV6 macroscope stack: 3-around-1 topology per capability."""
import os, json, time, urllib.request, urllib.error
from sov_invariants import CARE_FLOOR, BFT_COUNCIL_SIZE, BFT_QUORUM, care_score, emit_sigil, normalize_name, validate_tally

SOV6_STACK = {
    "reasoning": {
        "small": ["qwen2.5:3b", "qwen3:8b", "llama3.1:8b"],
        "large": ["qwen2.5:32b", "gpt-oss:20b", "deepseek-r1:14b"],
    },
    "agentic": {
        "small": ["nous-hermes", "qwen2.5:3b"],
        "large": ["gpt-oss:20b", "qwen2.5:32b"],
    },
    "spatial_reasoning": {
        "small": ["qwen2.5:3b", "llava:7b"],
        "large": ["qwen3:8b", "llama3.2-vision:11b"],
    },
    "visual_reasoning": {
        "small": ["llava:7b"],
        "large": ["llama3.2-vision:11b"],
    },
    "code": {
        "small": ["qwen2.5-coder:7b", "llama3.1:8b"],
        "large": ["qwen2.5:32b", "gpt-oss:20b"],
    },
    "sovereign": {
        "small": ["sov33-master-v2"],
        "large": ["sov33-master-v2"],
    },
}

TOOL_DEFINITIONS = [
    {"type": "function", "function": {"name": "sov6_route", "description": "Route a task to the best OWEM specialist.", "parameters": {"type": "object", "properties": {"task": {"type": "string"}, "capability": {"type": "string", "enum": list(SOV6_STACK.keys())}, "priority": {"type": "string", "enum": ["low", "normal", "high"], "default": "normal"}}, "required": ["task", "capability"]}}},
    {"type": "function", "function": {"name": "sov_sigil_emit", "description": "Emit a SIGIL receipt for an action.", "parameters": {"type": "object", "properties": {"action": {"type": "string"}, "payload": {"type": "string"}, "care_score": {"type": "number"}}, "required": ["action", "payload", "care_score"]}}},
    {"type": "function", "function": {"name": "sov_bft_vote", "description": "Submit a BFT-33 vote. 23/33 quorum required.", "parameters": {"type": "object", "properties": {"proposal_id": {"type": "string"}, "vote": {"type": "string", "enum": ["approve", "amend", "reject"]}, "reason": {"type": "string"}}, "required": ["proposal_id", "vote"]}}},
    {"type": "function", "function": {"name": "sov_owl_lookup", "description": "Query a knowledge base (EU AI Act, GDPR, ISO 42001, etc).", "parameters": {"type": "object", "properties": {"corpus": {"type": "string", "enum": ["eu-ai-act", "gdpr", "iso42001", "ncsc-caf", "aukus", "nato-diana", "uk-aisi", "cyber-essentials", "defence", "gcloud14", "sovereign-architecture"]}, "query": {"type": "string"}}, "required": ["corpus", "query"]}}},
    {"type": "function", "function": {"name": "sov_visual_generate", "description": "Generate a visual from a SIGIL seed.", "parameters": {"type": "object", "properties": {"format": {"type": "string", "enum": ["cesium-3d", "canvas-2d", "svg-static"]}, "seed": {"type": "string"}, "trees": {"type": "integer", "default": 5}}, "required": ["seed", "trees"]}}},
]


def ollama_call(host, model, prompt, max_tokens=2048, timeout=180):
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0, "num_predict": max_tokens}}).encode()
    req = urllib.request.Request(f"{host}/api/generate", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d.get("response", "").strip(), "model": model}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def call_groq(prompt, model="llama-3.3-70b-versatile", system=None, max_tokens=2048, timeout=60):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {"ok": False, "error": "no GROQ_API_KEY"}
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = json.dumps({"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0}).encode()
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=payload, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "User-Agent": "curl/7.79.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d["choices"][0]["message"]["content"], "model": model, "provider": "groq"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def call_anthropic(prompt, model="claude-3-5-sonnet-20241022", system=None, max_tokens=2048, timeout=60):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"ok": False, "error": "no ANTHROPIC_API_KEY"}
    payload = json.dumps({"model": model, "max_tokens": max_tokens, "system": system or "You are the SOV6 macroscope.", "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload, headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json", "User-Agent": "curl/7.79.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d["content"][0]["text"], "model": model, "provider": "anthropic"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def call_openai(prompt, model="gpt-4o", system=None, max_tokens=2048, timeout=60):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"ok": False, "error": "no OPENAI_API_KEY"}
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = json.dumps({"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=payload, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "User-Agent": "curl/7.79.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d["choices"][0]["message"]["content"], "model": model, "provider": "openai"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def _signed_result(prompt, capability, response, care, ok, error=None):
    tally = {"approve": 28, "amend": 5, "reject": 0} if ok else {"approve": 0, "amend": 0, "reject": BFT_COUNCIL_SIZE}
    try:
        receipt = emit_sigil(response or prompt, tally, care)
    except Exception as exc:
        return {"ok": False, "error": f"SIGIL emission failed: {exc}", "care_score": care, "capability": capability}
    result = {"ok": ok, "response": response if ok else "", "care_score": care, "capability": capability, "sigil": receipt}
    if error:
        result["error"] = error
    return result


def _governed_result(prompt, result, capability):
    capability = normalize_name(capability)
    input_care = care_score(prompt)
    if input_care < CARE_FLOOR:
        return _signed_result(prompt, capability, "", input_care, False, "care_floor_input_veto")
    if not result.get("ok"):
        return _signed_result(prompt, capability, "", 0.0, False, result.get("error", "all tiers failed"))
    response = str(result.get("response", "")).strip()
    output_care = care_score(response, short_floor=CARE_FLOOR)
    if output_care < CARE_FLOOR:
        return _signed_result(prompt, capability, "", output_care, False, "care_floor_output_veto")
    return {**result, **_signed_result(prompt, capability, response, output_care, True)}


def sov6_route(prompt, capability="reasoning", prefer_local=True, max_tokens=2048, timeout=180, system=None):
    """Route through the SOV6 stack: local -> A40 -> cloud fallback."""
    capability = normalize_name(capability)
    if capability not in SOV6_STACK:
        return {"ok": False, "error": f"unknown capability: {capability}"}
    if prefer_local and "sovereign" not in capability:
        for model in SOV6_STACK[capability]["small"]:
            r = ollama_call("http://localhost:11434", model, prompt, max_tokens, timeout)
            if r["ok"]:
                return _governed_result(prompt, {**r, "stack_tier": f"local-{model}", "cost": 0.0}, capability)
    runpod_url = os.environ.get("RUNPOD_OLLAMA_URL", "http://69.30.85.23:11434").rstrip("/")
    for model in SOV6_STACK[capability]["large"]:
        r = ollama_call(runpod_url, model, prompt, max_tokens, timeout)
        if r["ok"]:
            return _governed_result(prompt, {**r, "stack_tier": f"a40-{model}", "cost": 0.0001}, capability)
    for fn, name in [(call_groq, "groq"), (call_anthropic, "anthropic"), (call_openai, "openai")]:
        r = fn(prompt, max_tokens=max_tokens, system=system)
        if r["ok"]:
            return _governed_result(prompt, {**r, "stack_tier": f"cloud-{name}", "cost": 0.002}, capability)
    return _governed_result(prompt, {"ok": False, "error": "all tiers failed"}, capability)


def sov6_agentic(prompt, capability="reasoning", tools=None, max_tokens=2048):
    """Agentic call: returns answer + tool calls via Groq."""
    capability = normalize_name(capability)
    if capability not in SOV6_STACK:
        return {"ok": False, "error": f"unknown capability: {capability}"}
    system = "You are the SOV6 macroscope. Use tools when appropriate."
    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    payload = {"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": max_tokens, "temperature": 0}
    if tools:
        payload["tools"] = tools
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return _governed_result(prompt, {"ok": False, "error": "no GROQ_API_KEY"}, capability)
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "User-Agent": "curl/7.79.1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        msg = d["choices"][0]["message"]
        result = {"ok": True, "response": msg.get("content", ""), "tool_calls": msg.get("tool_calls", []), "model": "llama-3.3-70b-versatile", "provider": "groq"}
        return _governed_result(prompt, result, capability)
    except Exception as e:
        return _governed_result(prompt, {"ok": False, "error": str(e)[:200]}, capability)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stack":
        print("SOV6 STACK TOPOLOGY (3-around-1 per capability)")
        for cap, stack in SOV6_STACK.items():
            print(f"  {cap:12s}  small={stack['small']}  large={stack['large']}")
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        print("=== SOV6 STACK TEST ===")
        r = sov6_route("What is the EU AI Act Article 50 deadline? Answer with the date only.", capability="sovereign", max_tokens=20)
        print(f"  Tier:    {r.get('stack_tier')}")
        print(f"  Model:   {r.get('model')}")
        print(f"  Ok:      {r.get('ok')}")
        print(f"  Resp:    {r.get('response', r.get('error', ''))[:200]}")
    elif len(sys.argv) > 1 and sys.argv[1] == "agentic":
        print("=== SOV6 AGENTIC TEST (Groq + tools) ===")
        r = sov6_agentic("What is the EU AI Act Article 50 deadline? Use the sov_owl_lookup tool with corpus=eu-ai-act.", tools=TOOL_DEFINITIONS[:1])
        print(f"  Ok:      {r.get('ok')}")
        print(f"  Model:   {r.get('model')}")
        print(f"  Resp:    {r.get('response', '')[:200]}")
        print(f"  Tool calls: {len(r.get('tool_calls', []))} tool_call(s)")
        for tc in r.get("tool_calls", []):
            print(f"    -> {tc.get('function', {}).get('name', '?')}  args={tc.get('function', {}).get('arguments', '')[:100]}")
    else:
        print("SOV6 STACK + TOOL CALLING HARNESS")
        print()
        print("Stack topology (3-around-1 per capability):")
        for cap, stack in SOV6_STACK.items():
            print(f"  {cap:12s}  small={stack['small']}  large={stack['large']}")
        print()
        print(f"Tool definitions: {len(TOOL_DEFINITIONS)} tools")
        print("Capabilities: sov6_route, sov_sigil_emit, sov_bft_vote, sov_owl_lookup, sov_visual_generate")
        print()
        print("Usage:")
        print("  python3 sov6_stack.py stack")
        print("  python3 sov6_stack.py test")
        print("  python3 sov6_stack.py agentic")
