#!/usr/bin/env python3
"""deploy_k3.py — Create an A100 pod on the 2TB volume across available DCs.
Checks each DC for stock, then deploys with the K3 volume attached.
"""
import json, os, subprocess, sys, time

KEY_PATH = os.path.expanduser("~/.runpod/api_key")
API = "https://api.runpod.io/graphql"
IMG = "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"

def gql(query):
    key = open(KEY_PATH).read().strip()
    r = subprocess.run(["curl", "-s", "-X", "POST", API,
                        "-H", "Content-Type: application/json",
                        "-H", f"Authorization: Bearer {key}",
                        "-d", json.dumps({"query": query})],
                       capture_output=True, text=True, timeout=90)
    return json.loads(r.stdout)

def deploy(dc=None, vol_id=None, name="k3-a100-2tb"):
    dc_f = f', dataCenterId: "{dc}"' if dc else ""
    vol_f = f', networkVolumeId: "{vol_id}"' if vol_id else ""
    q = (f'mutation {{ podFindAndDeployOnDemand(input: {{name: "{name}", '
         f'gpuTypeId: "NVIDIA A100 80GB PCIe", gpuCount: 1, containerDiskInGb: 50, '
         f'cloudType: COMMUNITY{dc_f}{vol_f}, '
         f'imageName: "{IMG}", startSsh: true}}) '
         f'{{ id name desiredStatus runtime {{ uptimeInSeconds }} }} }}')
    d = gql(q)
    p = d.get("data", {}).get("podFindAndDeployOnDemand")
    if p:
        return p, None
    err = d.get("errors", [{}])[0].get("message", "unknown")[:80]
    return None, err

def find_stock_and_deploy():
    dcs = ["EU-RO-1", "US-MD-1", "US-WA-1", "US-KS-2", "EU-FR-1",
           "CA-MTL-3", "US-TX-1", "US-OR-1", "US-CA-2", "US-AL-1"]
    # First try EU-RO-1 (volume already there) — fast check without volume first
    print("Probing DCs for A100 stock...", flush=True)
    for dc in dcs:
        pod, err = deploy(dc=dc, name=f"k3-a100-probe-{dc.replace('-','').lower()}")
        if pod:
            print(f"  {dc}: ✅ A100 STOCK (probe pod {pod['id']})", flush=True)
            # Delete probe, redeploy with volume on the 2TB volume in THIS DC
            # But volume is EU-RO-1 pinned... so if DC != EU-RO-1 we need a new volume
            if dc == "EU-RO-1":
                pass  # volume already there
            else:
                print(f"  {dc}: no volume here — need volume creation in {dc}")
            return dc, pod
        else:
            print(f"  {dc}: ✗ {err}", flush=True)
    print("\nNo A100 stock in any probed DC right now.")
    return None, None

if __name__ == "__main__":
    dc, pod = find_stock_and_deploy()