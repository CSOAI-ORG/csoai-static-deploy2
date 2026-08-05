#!/usr/bin/env python3
"""Watch for SECURE-cloud capacity in the DCs where our network volumes live, and deploy
sov-brain-3 with the 300GB volume attached the moment stock appears. Bounded + cost-safe."""
import json,urllib.request,os,time,sys
tok=open(os.path.expanduser("~/.runpod/api_key")).read().strip()
def gql(q,v=None):
    b={"query":q}
    if v: b["variables"]=v
    r=urllib.request.Request("https://api.runpod.io/graphql",data=json.dumps(b).encode(),
      headers={"Content-Type":"application/json","Authorization":f"Bearer {tok}","User-Agent":"Mozilla/5.0 Chrome/120"})
    return json.loads(urllib.request.urlopen(r,timeout=90).read())
Q="mutation D($input:PodFindAndDeployOnDemandInput!){podFindAndDeployOnDemand(input:$input){id name}}"
TARGETS=[("b0h5gma2fy","CA-MTL-3"),("ahqvo6d4f3","CA-MTL-4")]
# preference order: value first, then power. All >= 2x the current 3090's 24GB.
GPUS=["NVIDIA A40","NVIDIA L40S","NVIDIA L40","NVIDIA RTX 6000 Ada Generation","NVIDIA RTX A6000",
      "NVIDIA A100 80GB PCIe","NVIDIA A100-SXM4-80GB","NVIDIA H100 PCIe"]
MAX_HOURS=float(sys.argv[1]) if len(sys.argv)>1 else 6.0
deadline=time.time()+MAX_HOURS*3600
attempt=0
while time.time()<deadline:
    attempt+=1
    bal=gql('query{myself{clientBalance}}')['data']['myself']['clientBalance']
    if bal<40: print(f"⛔ balance ${bal:.2f} < $40 — stopping, not deploying"); break
    for vol,dc in TARGETS:
        for gpu in GPUS:
            inp={"cloudType":"SECURE","gpuCount":1,"gpuTypeId":gpu,"name":"sov-brain-3",
                 "imageName":"runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04",
                 "containerDiskInGb":60,"volumeInGb":0,"networkVolumeId":vol,
                 "volumeMountPath":"/workspace","dataCenterId":dc,
                 "ports":"22/tcp,11434/http","startSsh":True,
                 "env":[{"key":"OLLAMA_MODELS","value":"/workspace/ollama"}]}
            try:
                d=gql(Q,{"input":inp})
                if "errors" in d: continue
                p=d['data']['podFindAndDeployOnDemand']
                print(f"✅ DEPLOYED {p['name']} id={p['id']} · {gpu} · SECURE · {dc} · vol {vol} → /workspace")
                sys.exit(0)
            except Exception: continue
    print(f"  attempt {attempt}: no secure capacity yet (balance ${bal:.2f}) — retrying in 5m")
    time.sleep(300)
print("no capacity within the window; re-run when convenient")
