#!/usr/bin/env python3
"""TRACK D: L3 anchor-routing quorum. 3 routers pick anchor; agree->route, split->escalate."""
import oci, json
from collections import Counter
cfg=oci.config.from_file("~/.oci/config","DEFAULT"); COMP=cfg["tenancy"]
EP="https://inference.generativeai.uk-london-1.oci.oraclecloud.com"
cl=oci.generative_ai_inference.GenerativeAiInferenceClient(cfg, service_endpoint=EP)
M=oci.generative_ai_inference.models
S="cohere.command-r-08-2024"; ANCHORS=["COMPLIANCE","DEFENSE","INTUITION","VOICE"]
def route(task,seed):
    msg=f"Route to ONE anchor {ANCHORS} (view {seed}). Reply ONLY the anchor word.\nTASK: {task}"
    cr=M.CohereChatRequest(api_format="COHERE",message=msg,max_tokens=6,temperature=0.3)
    t=cl.chat(M.ChatDetails(compartment_id=COMP,serving_mode=M.OnDemandServingMode(model_id=S),chat_request=cr)).data.chat_response.text.upper()
    return next((a for a in ANCHORS if a in t),"UNKNOWN")
def quorum(task):
    v=[route(task,i) for i in range(3)]; top,n=Counter(v).most_common(1)[0]
    return {"votes":v,"chosen":top if n>=2 else None,"escalate":n<2}
TASKS=["Draft an EU AI Act Annex IV file.","Detect a prompt-injection attack.",
       "Write a grief-support message.","Assess if this action harms a vulnerable person."]
print("TRACK D: L3 anchor-quorum (3 routers, escalate on split)")
rows=[]
for t in TASKS:
    r=quorum(t); rows.append({"task":t[:36],**r})
    print(f"  {r['votes']} -> {'ESCALATE' if r['escalate'] else r['chosen']:12} | {t[:36]}")
json.dump(rows,open("l3_anchor_results.json","w"),indent=2)
print(f"  -> {sum(1 for r in rows if r['escalate'])}/{len(TASKS)} escalated on disagreement")
