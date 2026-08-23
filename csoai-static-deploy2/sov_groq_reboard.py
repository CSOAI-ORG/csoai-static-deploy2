#!/usr/bin/env python3
"""sov_groq_reboard.py — the STANDING free-compute reboard tool.
Scores any GovBench item set on any Groq-served model with expect_contains grading. Groq = the live free API lane
(HF serverless is 502-deprecated, Modal spend-capped, Kaggle browser-run). This is how numbers get MEASURED, not assumed.

Usage: GROQ_KEY=... python3 sov_groq_reboard.py <items.json> [model]
  model default: llama-3.1-8b-instant. Also try llama-3.3-70b-versatile.
Emits per-dimension scores + n. Feed the same items to multiple models for a cross-model board.
The lesson that made this exist (FOREST_50): arithmetic-only "divides YES" was REFUTED once real scores were in.
Never trust an item-set's contribution without running it. This is the runner that runs it.
"""
import os, json, sys, time, statistics, urllib.request
from collections import defaultdict
GROQ=os.environ.get("GROQ_KEY") or os.environ.get("GROQ")
def groq_chat(model, content, mt=120):
    if not GROQ: raise SystemExit("set GROQ_KEY")
    body=json.dumps({"model":model,"messages":[{"role":"user","content":content}],"max_tokens":mt,"temperature":0.1}).encode()
    req=urllib.request.Request("https://api.groq.com/openai/v1/chat/completions",data=body,
        headers={"Authorization":f"Bearer {GROQ}","Content-Type":"application/json","User-Agent":"sov-reboard/1.0"})
    for _ in range(4):
        try: return json.loads(urllib.request.urlopen(req,timeout=45).read())["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(6); continue
            return None
        except Exception: return None
    return None
def grade(resp, expect):
    if not resp: return None
    low=resp.lower(); return 1.0 if any(e.lower() in low for e in expect) else 0.0
def reboard(items, model, sleep=0.6):
    by_dim=defaultdict(list)
    for it in items:
        s=grade(groq_chat(model, it["q"]), it["expect_contains"])
        if s is not None: by_dim[it["dimension"]].append(s)
        time.sleep(sleep)
    return {d:round(statistics.mean(v)*100,1) for d,v in by_dim.items()}, {d:len(v) for d,v in by_dim.items()}
if __name__=="__main__":
    items=json.load(open(sys.argv[1]))
    model=sys.argv[2] if len(sys.argv)>2 else "llama-3.1-8b-instant"
    sc,n=reboard(items, model)
    print(json.dumps({"model":model,"scores":sc,"n":n}, indent=1))
