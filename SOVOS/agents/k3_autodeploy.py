#!/usr/bin/env python3
"""k3_autodeploy.py — Retry K3 A100 pod deployment until stock returns.
Runs via Hermes cron. Creates pod on 2TB volume i4atujketp when A100 frees.
Refuses to re-deploy if already done (idempotent).
"""
import json, os, subprocess, sys, time

KEY_PATH = os.path.expanduser("~/.runpod/api_key")
API = "https://api.runpod.io/graphql"
IMG = "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"
VOL_ID = "i4atujketp"
MARKER = "/tmp/k3_pod_created.json"

def gql(query):
    key = open(KEY_PATH).read().strip()
    r = subprocess.run(["curl", "-s", "-X", "POST", API,
                        "-H", "Content-Type: application/json",
                        "-H", f"Authorization: Bearer {key}",
                        "-d", json.dumps({"query": query})],
                       capture_output=True, text=True, timeout=90)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"errors": [{"message": "bad json"}]}

def already_done():
    return os.path.exists(MARKER)

def deploy():
    q = (f'mutation {{ podFindAndDeployOnDemand(input: {{name: "k3-a100-2tb", '
         f'gpuTypeId: "NVIDIA A100 80GB PCIe", gpuCount: 1, containerDiskInGb: 50, '
         f'networkVolumeId: "{VOL_ID}", cloudType: COMMUNITY, '
         f'imageName: "{IMG}", startSsh: true}}) '
         f'{{ id name desiredStatus runtime {{ uptimeInSeconds }} }} }}')
    d = gql(q)
    p = d.get("data", {}).get("podFindAndDeployOnDemand")
    if p:
        json.dump(p, open(MARKER, "w"))
        print(f"✅ DEPLOYED K3 pod: {p}")
        return True
    err = d.get("errors", [{}])[0].get("message", "unknown")[:90]
    print(f"⏳ no stock: {err}")
    return False

if __name__ == "__main__":
    if already_done():
        print("K3 pod already deployed — skipping (idempotent)")
        sys.exit(0)
    deploy()