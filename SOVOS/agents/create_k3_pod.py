#!/usr/bin/env python3
"""create_k3_pod.py — Create a pod on the 2TB K3 volume (EU-RO-1 pinned)."""
import json, os, subprocess, sys, time

KEY = os.path.expanduser("~/.runpod/api_key").strip()
API = "https://api.runpod.io/graphql"
VOL_ID = "i4atujketp"
HEADERS = ["-H", "Content-Type: application/json", "-H", f"Authorization: Bearer {open(KEY).read().strip()}"]

def gql(query):
    r = subprocess.run(["curl", "-s", "-X", "POST", API] + HEADERS +
                       ["-d", json.dumps({"query": query})],
                       capture_output=True, text=True, timeout=90)
    return json.loads(r.stdout)

def try_deploy(name, gpu, dc=None):
    dc_field = f', dataCenterId: "{dc}"' if dc else ""
    q = f'''mutation {{ podFindAndDeployOnDemand(input: {{name: "{name}", gpuTypeId: "{gpu}", gpuCount: 1, containerDiskInGb: 30, networkVolumeId: "{VOL_ID}", cloudType: COMMUNITY{dc_field}, imageName: "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04", startSsh: true}}) {{ id name desiredStatus runtime {{ uptimeInSeconds }} }} }}'''
    d = gql(q)
    pod = d.get("data", {}).get("podFindAndDeployOnDemand")
    if pod:
        return pod
    msg = d.get("errors", [{}])[0].get("message", "unknown")[:90]
    return {"error": msg}

def main():
    # Try common GPUs in EU-RO-1 (volume is pinned there)
    gpus = [
        "NVIDIA L40S 48GB",
        "NVIDIA RTX A6000 48GB",
        "NVIDIA GeForce RTX 3090 Ti",
        "NVIDIA GeForce RTX 4090",
        "NVIDIA GeForce RTX 3090",
    ]
    for gpu in gpus:
        print(f"Trying {gpu} in EU-RO-1...", flush=True)
        for attempt in range(3):
            r = try_deploy("k3-2tb-"+gpu.lower().replace(" ","").replace("nvidia","")[:20], gpu)
            if "id" in r:
                print(f"  ✅ DEPLOYED: {r['id']} ({r['name']}) status={r['desiredStatus']}")
                print(json.dumps({"pod_id": r["id"], "name": r["name"], "gpu": gpu,
                                  "volume_id": VOL_ID}, indent=2))
                return
            if "no longer any instances" in r.get("error",""):
                break  # out of stock, move on
            print(f"  retry {attempt}: {r.get('error')}")
            time.sleep(2)
        print(f"  ✗ {gpu} unavailable")

    print("All EU-RO-1 GPUs tried. Volume i4atujketp created but needs an available GPU.")
    print("Run this again when stock returns (the 2TB volume persists).")

if __name__ == "__main__":
    main()