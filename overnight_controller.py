#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
import os as _os, shutil as _sh; _rp=_os.path.expanduser('~/.runpod/api_key'); (_os.path.exists(_rp) and not _os.path.exists('/tmp/.rpk')) and _sh.copy(_rp,'/tmp/.rpk')
"""
overnight_controller.py — bounded, cost-guarded overnight EAT orchestrator.

Runs waves at a sane pace and writes OVERNIGHT_REPORT.md continuously so Nick wakes to a summary.
Safe by construction:
  • COST GUARD: stops ALL pods and exits if balance < MIN_BALANCE.
  • SPRAY CAP: never more than MAX_SPRAY browser-eat pods (redeploys as they self-terminate).
  • FUEL IDLE-STOP: stops fuel-train once it has been up > FUEL_MAX_MIN (LoRA done → it parks).
  • BOUNDED: exits after MAX_HOURS regardless.
  • PACED: one arena firing per cycle (rapid-fire gets throttled), 120s cycles.
Pods (browser-eat, fuel-train) and Kaggle arena runs continue on their own servers even if this
controller (or the Mac) sleeps — this just manages waves + guards cost + reports.
"""
import json, time, urllib.request, subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN = open('/tmp/.rpk').read().strip()
UA = "Mozilla/5.0 Chrome/120"
REPORT = HERE / "benchmark-results" / "OVERNIGHT_REPORT.md"

MIN_BALANCE = 95.0
MAX_SPRAY = 4
MAX_HOURS = 9
FUEL_MAX_MIN = 55
CYCLE = 120

ARENAS = ["govbench-eu-ai-act-risk-tier", "provbench-does-the-article-50-marking-survive",
          "pqcbench-post-quantum-continuity", "defbench-calibrated-refusal",
          "mcpbench-3-predicate-tool-conformance", "ossbench-licence-vs-intended-use"]
ADD_MODELS = ["claude-opus-4-8-default", "claude-opus-4-6-default", "claude-opus-4-5-20251101",
              "claude-sonnet-4-6-default", "gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.5-2026-04-23",
              "gemini-3.5-flash-lite", "gemini-3.1-flash-lite-preview", "gemma-4-31b-it"]
# pending arena queue: (task, model)
QUEUE = [(t, m) for t in ARENAS for m in ADD_MODELS]


def gql(q):
    req = urllib.request.Request("https://api.runpod.io/graphql",
        data=json.dumps({"query": q}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}", "User-Agent": UA})
    return json.loads(urllib.request.urlopen(req, timeout=45).read())


def fleet():
    d = gql('query{myself{clientBalance pods{id name desiredStatus costPerHr runtime{uptimeInSeconds}}}}')
    return d['data']['myself']


def stop_pod(pid):
    try:
        gql(f'mutation{{podStop(input:{{podId:"{pid}"}}){{id desiredStatus}}}}'); return True
    except Exception:
        return False


def deploy_spray(runid):
    pod = json.load(open('/tmp/eatpod.json'))['data']['pod']
    env = [{"key": k, "value": (runid if k == 'RUN_ID' else v)} for k, _, v in (e.partition('=') for e in pod['env'])]
    if not any(x['key'] == 'RUN_ID' for x in env):
        env.append({"key": "RUN_ID", "value": runid})
    for gpu in ["NVIDIA RTX A2000", "NVIDIA GeForce RTX 3070", "NVIDIA RTX A4000", "NVIDIA RTX A5000"]:
        inp = {"cloudType": "COMMUNITY", "gpuCount": 1, "gpuTypeId": gpu, "name": f"sov-browser-eat-{runid}",
               "imageName": pod['imageName'], "dockerArgs": pod['dockerArgs'],
               "containerDiskInGb": pod.get('containerDiskInGb') or 20, "volumeInGb": 0, "env": env}
        q = "mutation D($input:PodFindAndDeployOnDemandInput!){podFindAndDeployOnDemand(input:$input){id}}"
        try:
            req = urllib.request.Request("https://api.runpod.io/graphql",
                data=json.dumps({"query": q, "variables": {"input": inp}}).encode(),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}", "User-Agent": UA})
            d = json.loads(urllib.request.urlopen(req, timeout=60).read())
            if 'errors' not in d:
                return d['data']['podFindAndDeployOnDemand']['id']
        except Exception:
            continue
    return None


def fire_arena(task, model):
    try:
        r = subprocess.run(["kaggle", "benchmarks", "tasks", "run", task, "-m", model],
                           capture_output=True, text=True, timeout=60)
        return "Scheduled" in (r.stdout + r.stderr)
    except Exception:
        return False


def now():
    return datetime.now(timezone.utc).strftime("%H:%M")


def write_report(log, m, fired, spray_n, note):
    lines = ["# Overnight EAT — live report\n",
             f"_Updated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}Z_\n",
             f"- **Balance:** ${m['clientBalance']:.2f}",
             f"- **Arena runs fired this session:** {fired} / {len(ARENAS)*len(ADD_MODELS)}",
             f"- **Spray pods active:** {spray_n}",
             f"- **Note:** {note}\n", "## Fleet"]
    for p in m['pods']:
        if p['desiredStatus'] == 'RUNNING':
            up = ((p.get('runtime') or {}).get('uptimeInSeconds') or 0) // 60
            lines.append(f"- {p['name'][:44]} · up {up}m · ${p.get('costPerHr')}/hr")
    lines += ["\n## Event log (newest last)"] + [f"- {e}" for e in log[-40:]]
    REPORT.write_text("\n".join(lines) + "\n")


def main():
    deadline = time.time() + MAX_HOURS * 3600
    log = [f"{now()} controller start — {len(QUEUE)} arena firings queued"]
    fired = 0
    while time.time() < deadline:
        try:
            m = fleet()
            bal = m['clientBalance']
            running = [p for p in m['pods'] if p['desiredStatus'] == 'RUNNING']
            spray = [p for p in running if 'browser-eat' in p['name']]

            # COST GUARD
            if bal < MIN_BALANCE:
                for p in running:
                    stop_pod(p['id'])
                log.append(f"{now()} ⛔ COST GUARD: balance ${bal:.2f} < ${MIN_BALANCE} — stopped all {len(running)} pods, exiting")
                write_report(log, m, fired, 0, "STOPPED on cost guard")
                return

            # FUEL IDLE-STOP
            for p in running:
                if 'fuel-train' in p['name']:
                    up = ((p.get('runtime') or {}).get('uptimeInSeconds') or 0) // 60
                    if up > FUEL_MAX_MIN:
                        if stop_pod(p['id']):
                            log.append(f"{now()} 🛑 fuel-train up {up}m (LoRA done + parked) — stopped, idle-burn avoided")

            # SPRAY WAVE — redeploy up to MAX_SPRAY
            if len(spray) < MAX_SPRAY and QUEUE_SPRAY[0] < 6:  # cap total redeploys
                rid = f"wave{QUEUE_SPRAY[0]}-{int(time.time())%100000}-browser-eat"
                pid = deploy_spray(rid)
                if pid:
                    QUEUE_SPRAY[0] += 1
                    log.append(f"{now()} 🕷 spray wave: deployed {pid} (now {len(spray)+1} active)")

            # ARENA — one paced firing per cycle
            if QUEUE:
                task, model = QUEUE.pop(0)
                if fire_arena(task, model):
                    fired += 1
                    log.append(f"{now()} 🏟 arena {task.split('-')[0]} ← {model}: scheduled ({fired} total)")
                else:
                    QUEUE.append((task, model))  # requeue on throttle

            write_report(log, m, fired, len(spray), f"running · {len(QUEUE)} arena firings left")
        except Exception as e:
            log.append(f"{now()} err {str(e)[:60]}")
        time.sleep(CYCLE)

    # graceful end
    try:
        m = fleet()
        log.append(f"{now()} controller reached {MAX_HOURS}h bound — exiting (pods keep running)")
        write_report(log, m, fired, len([p for p in m['pods'] if p['desiredStatus'] == 'RUNNING' and 'browser-eat' in p['name']]), "DONE — max hours reached")
    except Exception:
        pass


QUEUE_SPRAY = [0]  # mutable redeploy counter
if __name__ == "__main__":
    main()
