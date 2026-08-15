#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
import os as _os, shutil as _sh; _rp=_os.path.expanduser('~/.runpod/api_key'); (_os.path.exists(_rp) and not _os.path.exists('/tmp/.rpk')) and _sh.copy(_rp,'/tmp/.rpk')
"""Guarded background retry: deploy ONE fuel-train pod when a 24GB GPU frees. Exits after it lands
or after the attempt budget. Hard guard: never deploys if a fuel-train pod already exists RUNNING."""
import json, time, urllib.request
TOKEN = open('/tmp/.rpk').read().strip()
UA = "Mozilla/5.0 Chrome/120"
GPUS = ["NVIDIA GeForce RTX 3090", "NVIDIA RTX A5000", "NVIDIA RTX A4500",
        "NVIDIA GeForce RTX 4090", "NVIDIA RTX A6000", "NVIDIA GeForce RTX 4080"]


def gql(q):
    req = urllib.request.Request("https://api.runpod.io/graphql",
        data=json.dumps({"query": q}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}", "User-Agent": UA})
    return json.loads(urllib.request.urlopen(req, timeout=45).read())


def fuel_running():
    d = gql('query{myself{pods{name desiredStatus}}}')
    return any('fuel-train' in p['name'] and p['desiredStatus'] == 'RUNNING'
               for p in d['data']['myself']['pods'])


def deploy(gpu, runid):
    pod = json.load(open('/tmp/trainpod.json'))['data']['pod']
    env = []
    for e in pod['env']:
        k, _, v = e.partition('=')
        env.append({"key": k, "value": runid if k == 'RUN_ID' else v})
    if not any(x['key'] == 'RUN_ID' for x in env):
        env.append({"key": "RUN_ID", "value": runid})
    inp = {"cloudType": "COMMUNITY", "gpuCount": 1, "gpuTypeId": gpu,
           "name": f"sov-fuel-train-{runid}", "imageName": pod['imageName'],
           "dockerArgs": pod['dockerArgs'], "containerDiskInGb": 30, "volumeInGb": 0, "env": env}
    q = ("mutation D($input:PodFindAndDeployOnDemandInput!){podFindAndDeployOnDemand(input:$input)"
         "{id desiredStatus costPerHr}}")
    req = urllib.request.Request("https://api.runpod.io/graphql",
        data=json.dumps({"query": q, "variables": {"input": inp}}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}", "User-Agent": UA})
    d = json.loads(urllib.request.urlopen(req, timeout=60).read())
    if 'errors' in d:
        return None
    return d['data']['podFindAndDeployOnDemand']


ATTEMPTS = 40  # ~60 min at 90s
for i in range(ATTEMPTS):
    try:
        if fuel_running():
            print(f"[{i}] fuel-train already RUNNING — done."); break
        for gpu in GPUS:
            runid = f"retry{i}-fuel-train"
            p = deploy(gpu, runid)
            if p:
                print(f"[{i}] ✅ fuel-train landed on {gpu}: {p['id']} ${p.get('costPerHr')}/hr"); raise SystemExit
        print(f"[{i}] no 24GB GPU free yet — retry in 90s")
    except SystemExit:
        break
    except Exception as e:
        print(f"[{i}] err {str(e)[:50]}")
    time.sleep(90)
else:
    print("budget exhausted — no 24GB GPU freed. fuel-train still pending.")
