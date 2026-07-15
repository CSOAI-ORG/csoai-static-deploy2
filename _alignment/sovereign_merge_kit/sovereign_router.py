#!/usr/bin/env python3
"""sovereign_router.py — the MASTER-COORDINATOR gateway: dispatch each unit of work to the best AVAILABLE
worker model, so heavy compute runs on the PROVIDERS' GPUs, not the 16GB Mac. Keys come from env vars YOU set
(never handled/logged here). Every call returns WHICH backend answered, so the SIGIL ledger can sign provenance.

Backends (all OpenAI-compatible chat endpoints), tried in the requested tier order:
  groq        GROQ_API_KEY        https://api.groq.com/openai/v1            (fast, free tier)
  nvidia      NVIDIA_API_KEY      https://integrate.api.nvidia.com/v1        (free hosted 70B-405B)
  glm         GLM_API_KEY         https://open.bigmodel.cn/api/paas/v4       (Zhipu GLM, your pro sub)
  minimax     MINIMAX_API_KEY     https://api.minimax.chat/v1                (your pro sub)
  ollama      (local, no key)     http://localhost:11434/v1                  (M4 fallback, small)
"""
import os, json, urllib.request

BACKENDS = {
    "groq":    dict(key="GROQ_API_KEY",    base="https://api.groq.com/openai/v1",           model=os.environ.get("GROQ_MODEL","llama-3.3-70b-versatile")),
    "nvidia":  dict(key="NVIDIA_API_KEY",  base="https://integrate.api.nvidia.com/v1",       model=os.environ.get("NVIDIA_MODEL","meta/llama-3.1-405b-instruct")),   # most-powerful FREE hosted tier
    "glm":     dict(key="GLM_API_KEY",     base="https://open.bigmodel.cn/api/paas/v4",       model=os.environ.get("GLM_MODEL","glm-4-flash")),
    "minimax": dict(key="MINIMAX_API_KEY", base="https://api.minimax.chat/v1",                model=os.environ.get("MINIMAX_MODEL","abab6.5s-chat")),
    "ollama":  dict(key=None,              base="http://localhost:11434/v1",                  model=os.environ.get("OLLAMA_MODEL","sovereign")),
    # --- large open MoE models as optional backends. STATUS: PAID + NOT-YET-FUNCTIONAL (do not count as capability) ---
    # Live-tested by the Claude Code lane 2026-07-14: these are PAID APIs and the accounts are UNFUNDED —
    # Kimi/Moonshot returned "account suspended — insufficient balance"; DeepSeek untested but same paid model.
    # PARAM/LICENSE specs below are UNVERIFIED web-search leads (bodies not retained) — confirm on model card.
    # => Wired for when funded, but NOT working today. Do NOT present as available T-scale capability.
    "deepseek":dict(key="DEEPSEEK_API_KEY", base="https://api.deepseek.com/v1",               model=os.environ.get("DEEPSEEK_MODEL","deepseek-chat"),  note="PAID/UNFUNDED. DeepSeek V4 [UNVERIFIED ~1.6T total — confirm model card; needs funded account]"),
    "kimi":    dict(key="KIMI_API_KEY",     base="https://api.moonshot.ai/v1",                model=os.environ.get("KIMI_MODEL","kimi-k2"),           note="PAID/UNFUNDED (live-tested: account suspended, insufficient balance). Kimi K2 [UNVERIFIED ~1T total]"),
}
# default preference: cheap/fast first, big hosted next, local last. 'trillion' tier = genuine >=1T-total models only.
TIERS = {"fast":["groq","ollama"], "smart":["nvidia","glm","minimax","groq","ollama"],
         "trillion":["deepseek","kimi","glm"], "any":["deepseek","kimi","nvidia","glm","minimax","groq","ollama"]}

def available():
    out=[]
    for n,b in BACKENDS.items():
        if b["key"] is None: out.append(n)                 # ollama = local, assume present
        elif os.environ.get(b["key"]): out.append(n)
    return out

def _call(name, prompt, system, max_tokens, temperature, model=None):
    b=BACKENDS[name]; key=os.environ.get(b["key"]) if b["key"] else None
    if b["key"] and not key: return None
    key=(key or "").strip().strip('"').strip("'")   # tolerate stray paste chars
    msgs=([{"role":"system","content":system}] if system else [])+[{"role":"user","content":prompt}]
    use_model = model or b["model"]                  # per-call model override (confirmed-live model id)
    body=json.dumps({"model":use_model,"messages":msgs,"temperature":temperature,"max_tokens":max_tokens,"stream":False}).encode()
    hdr={"Content-Type":"application/json","User-Agent":"Mozilla/5.0 sovereign-router"}  # UA: Groq/CF need it
    if key: hdr["Authorization"]=f"Bearer {key}"
    req=urllib.request.Request(f"{b['base']}/chat/completions",data=body,headers=hdr)
    try:
        r=json.loads(urllib.request.urlopen(req,timeout=90).read())
        return r["choices"][0]["message"]["content"].strip()
    except Exception:
        return None

def dispatch(prompt, system=None, tier="smart", max_tokens=400, temperature=0.2, model=None, backend=None):
    """Try backends in tier order; return (answer, backend_name). None answer only if ALL fail.
    model=  -> override the model id for the chosen backend (e.g. a confirmed-live NVIDIA model).
    backend= -> pin a single backend (e.g. 'nvidia') instead of trying the whole tier."""
    order = [backend] if backend else TIERS.get(tier, TIERS["any"])
    for name in order:
        if name not in available(): continue
        a=_call(name, prompt, system, max_tokens, temperature, model=model)
        if a: return a, (f"{name}:{model}" if model else name)
    return None, None

if __name__=="__main__":
    av=available()
    print("Available worker backends (by env keys):", av)
    missing=[n for n in BACKENDS if n not in av]
    if missing: print("Not configured (set the env key to enable):", {n:BACKENDS[n]["key"] for n in missing})
    ans,who=dispatch("In one sentence, what is a signed sovereign AI decision?", tier="smart", max_tokens=60)
    print(f"\ndispatch -> backend={who}\n{ans}")
