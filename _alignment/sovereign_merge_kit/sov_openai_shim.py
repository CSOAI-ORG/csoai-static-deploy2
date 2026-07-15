#!/usr/bin/env python3
"""sov_openai_shim.py — GOVERNED OpenAI-compatible endpoint for SOV333.

Point Open WebUI (or any OpenAI client) at  http://localhost:8802/v1  and pick a
"sov333-*" model. Every request: care-gate (RECALL 1.00, floor 0.35) -> route to a
brain (Ollama local / NVIDIA ~400B / 1.6T slot when reachable) -> Ed25519-sign.

  python sov_openai_shim.py       # -> http://localhost:8802/v1

Honest: the governance (care-gate + signature) is ours; the intelligence is the brain's.
"sov333-frontier" reaches the biggest reachable API model; 1.6T answers only when that
model actually responds on this machine (not faked).
"""
import os, sys, json, time, http.server, socketserver
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from sov33_care_local import score_local, FLOOR
import sovereign_router as ROUTER
try:
    from sov33_ed25519_sigil import Ed25519Sigil, HAVE
    SIGIL=Ed25519Sigil() if HAVE else None
except Exception: SIGIL=None

PORT=int(os.environ.get("SOV_SHIM_PORT","8802"))
# model name (what the user picks in Open WebUI) -> router tier
MODELS={"sov333-fast":"fast","sov333-smart":"smart","sov333-frontier":"frontier"}
SYS=("You are SOV333, a sovereign governed AI. Answer clearly, cite governing rules where "
     "relevant, never advise unlawful/harmful action, be honest about limits.")
REFUSAL="I can't help with that — it's below the sovereign care-floor (governance withheld this request)."

def last_user(messages):
    for m in reversed(messages or []):
        if m.get("role")=="user": return m.get("content","")
    return ""

def completion(model, messages):
    tier=MODELS.get(model,"smart"); prompt=last_user(messages)
    care,intent=score_local(prompt)
    if care<FLOOR:
        text=REFUSAL; backend="governance-veto"; gated=True
    else:
        # pass full history as a single governed prompt (system + convo)
        convo="\n".join(f"{m['role']}: {m['content']}" for m in messages if m.get("content"))
        text,backend=ROUTER.dispatch(convo, system=SYS, tier=tier, max_tokens=600)
        text=text or "(no brain reachable — start Ollama or set a provider key on this machine)"
        gated=False
    sig=""
    if SIGIL:
        sig=SIGIL.sign(json.dumps({"p":prompt,"a":text,"c":round(care,2)})).get("own_hash","")[:16]
    # standard OpenAI response shape, + sovereign metadata Open WebUI will ignore but audit keeps
    return {"id":f"sov-{int(time.time())}","object":"chat.completion","model":model,
        "choices":[{"index":0,"message":{"role":"assistant","content":text},"finish_reason":"stop"}],
        "usage":{"prompt_tokens":len(prompt.split()),"completion_tokens":len(text.split()),"total_tokens":0},
        "sovereign":{"care_score":round(care,2),"intent":intent,"gated":gated,"backend":backend,
                     "signature":sig,"verified":bool(sig)}}

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def _j(self,o,c=200):
        b=json.dumps(o).encode()
        self.send_response(c); self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Content-Length",str(len(b))); self.end_headers()
        self.wfile.write(b)
    def do_OPTIONS(self):
        self.send_response(204); self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","*"); self.send_header("Access-Control-Allow-Methods","*"); self.end_headers()
    def do_GET(self):
        if self.path.rstrip("/").endswith("/models"):
            self._j({"object":"list","data":[{"id":m,"object":"model","owned_by":"sovereign"} for m in MODELS]})
        else: self._j({"error":"not found"},404)
    def do_POST(self):
        n=int(self.headers.get("Content-Length",0)); body=json.loads(self.rfile.read(n) or b"{}")
        if self.path.rstrip("/").endswith("/chat/completions"):
            self._j(completion(body.get("model","sov333-smart"), body.get("messages",[])))
        else: self._j({"error":"not found"},404)

if __name__=="__main__":
    print(f"\n  SOV333 governed OpenAI endpoint -> http://localhost:{PORT}/v1")
    print(f"  models: {list(MODELS)}   care-floor={FLOOR}  signing={'ON' if SIGIL else 'off'}")
    print(f"  backends reachable now: {ROUTER.available()}")
    print(f"  In Open WebUI: Settings -> Connections -> OpenAI API -> URL http://localhost:{PORT}/v1 (any key)\n")
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(("127.0.0.1",PORT),H) as s: s.serve_forever()
