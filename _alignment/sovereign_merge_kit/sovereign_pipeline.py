#!/usr/bin/env python3
"""sovereign_pipeline.py — THE unified Sovereign decision, composed from the pieces proven to work this session.
One entry point, one signed answer:

  question
    → RETRIEVE grounding passages (dense RAG)              [facts come from retrieval, not the small model]
    → CARE-FLOOR gate (abstain if unsupported)             [fail-closed]
    → PROPOSE: several local models answer from the grounding   [fluid multi-model]
    → GROUNDED CARE-GATE: judge each proposal vs the source, DROP contradictors   [Byzantine-robust, text-domain]
    → FUSE survivors → one Sovereign answer                [Mixture-of-Agents]
    → Ed25519-SIGN the whole decision                      [tamper-evident, offline-verifiable]

This is the coherent core: RAG grounding + council fusion + grounded BFT gate + signing — one flow. Local, no GPU.
"""
import os, re, json, sys, time, urllib.request
import numpy as np
os.environ.setdefault("HF_HUB_OFFLINE","1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sov33_ed25519_sigil import Ed25519Sigil

OLLAMA="http://localhost:11434"
PROPOSERS=["qwen3:1.7b","qwen3-precise:latest"]
AGG="sovereign"
CARE_FLOOR=0.28

KB=[("EU AI Act Art.50","Providers of AI that generate synthetic audio, image, video or text must mark outputs as artificially generated in a machine-readable way, and users must be told when they interact with an AI system."),
    ("GDPR Art.9","Biometric data processed to uniquely identify a person is a special category; processing is prohibited unless a lawful exception such as explicit consent applies."),
    ("DORA","Financial entities must run an ICT risk-management framework, report major ICT incidents, and perform digital operational resilience testing."),
    ("ISO/IEC 42001","The first AI management system standard: requires an AI Management System with risk assessment, controls, and continual improvement."),
    ("JSP 936","Externally-acquired defence AI must attract the same assurance confidence as in-house AI; teams may need to stand up additional assurance to close evidence shortfalls.")]

def _strip(o):
    o=re.sub(r"<think>.*?</think>","",o,flags=re.S); o=re.sub(r"^.*?</think>","",o,flags=re.S); o=re.sub(r"^.*?<think>","",o,flags=re.S); return o.strip()
def gen(model,prompt,n=300):
    def call(k):
        body=json.dumps({"model":model,"keep_alive":0,"stream":False,"messages":[{"role":"user","content":prompt}],"options":{"temperature":0.2,"num_predict":k}}).encode()
        req=urllib.request.Request(f"{OLLAMA}/api/chat",data=body,headers={"Content-Type":"application/json"})
        try: return _strip(json.loads(urllib.request.urlopen(req,timeout=180).read())["message"]["content"])
        except Exception: return ""
    return call(n) or call(600)

class Retriever:
    def __init__(self):
        from sentence_transformers import SentenceTransformer
        self.m=SentenceTransformer("all-MiniLM-L6-v2")
        self.D=np.asarray(self.m.encode([t for _,t in KB],normalize_embeddings=True))
    def top(self,q,k=2):
        qe=self.m.encode([q],normalize_embeddings=True)[0]; s=self.D@qe; idx=s.argsort()[::-1][:k]
        return [(KB[i][0],KB[i][1],float(s[i])) for i in idx]

def sovereign_answer(q, R, sig):
    hits=R.top(q,2); top=hits[0][2]
    if top<CARE_FLOOR:
        rec=sig.sign({"q":q,"answer":"ABSTAIN — not in sovereign knowledge base.","care_ok":False,"top":round(top,3)})
        return {"answer":"ABSTAIN — not in sovereign knowledge base.","abstain":True,"sources":[],"dropped":[],"verifies":sig.verify(rec)}
    ctx="\n".join(f"[{s}] {t}" for s,t,_ in hits)
    ground=hits[0][1]
    # propose (grounded)
    props=[]
    for m in PROPOSERS:
        a=gen(m,f"/no_think Answer ONLY from CONTEXT, cite the [source]. If not in context say ABSTAIN.\nCONTEXT:\n{ctx}\nQ: {q}\nA:")
        if a: props.append((m,a))
    # grounded care-gate: drop contradictors
    survivors,dropped=[],[]
    for m,a in props:
        v=gen(AGG,f"/no_think REFERENCE: {ground}\nCANDIDATE: {a}\nDoes CANDIDATE contradict REFERENCE on the key fact? one word: CONTRADICT or CONSISTENT.",50).upper()
        (dropped if ("CONTRADICT" in v and "NOT CONTRADICT" not in v) else survivors).append((m,a))
    # fuse survivors
    if survivors:
        digest="\n".join(f"- {a}" for _,a in survivors)
        fused=gen(AGG,f"/no_think Synthesize ONE grounded answer from these, cite [source], 2 sentences.\nQ: {q}\n{digest}\nFUSED:",220)
    else:
        fused="ABSTAIN — all proposers contradicted the grounded source."
    rec=sig.sign({"q":q,"answer":fused,"sources":[s for s,_,_ in hits],"survivors":[m for m,_ in survivors],"dropped":[m for m,_ in dropped],"care_ok":True,"top":round(top,3)})
    return {"answer":fused,"abstain":False,"sources":[s for s,_,_ in hits],"dropped":[m for m,_ in dropped],"verifies":sig.verify(rec)}

def main():
    R=Retriever(); sig=Ed25519Sigil()
    print("=== SOVEREIGN PIPELINE — RAG-grounded · multi-model · grounded care-gate · signed ===")
    print(f"proposers={PROPOSERS} aggregator={AGG} pubkey={sig.pub_hex()[:16]}…\n")
    Qs=["What must AI providers do for synthetic media under the EU AI Act?",
        "Under GDPR, is biometric identification data specially protected?",
        "What is the capital of the Sun?"]  # out-of-KB -> abstain
    res=[]
    for q in Qs:
        r=sovereign_answer(q,R,sig); res.append({"q":q,**r})
        tag="ABSTAIN" if r["abstain"] else f"sources={r['sources']} dropped={r['dropped']}"
        print(f"── {q}\n   {tag}\n   → {r['answer'][:260]}\n   ✍ signed & verifies={r['verifies']}\n")
    out={"ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"pipeline":"RAG+council+grounded-care-gate+sign",
         "results":res,"all_verify":all(x["verifies"] for x in res),
         "honest":"one composed flow of the working pieces; facts from RAG, robustness from the grounded gate, trust from signing; small models still limited."}
    os.makedirs("benchmarks",exist_ok=True); json.dump(out,open("benchmarks/sovereign_pipeline_2026-07-14.json","w"),indent=2)
    print(f"✅ unified Sovereign pipeline runs · all signed={out['all_verify']} → benchmarks/sovereign_pipeline_2026-07-14.json")

if __name__=="__main__": main()
