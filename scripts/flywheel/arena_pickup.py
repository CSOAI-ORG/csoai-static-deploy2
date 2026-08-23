#!/usr/bin/env python3
"""arena_pickup.py — the submit→measure bridge (closes the arena loop).

The Cloudflare submit endpoint (POST /api/arena/submit) returns a queued
receipt. This daemon on the 3090 polls the endpoint's queue surface, drops
job specs into /workspace/measure-queue/ for measure_chain.py to pick up,
run the real harness, and sign.

Queue surface today: the endpoint returns {status:"queued", receipt_id} but
does not persist jobs yet (no datastore bound on the function). This script
accepts jobs two ways:
  1. a local drop dir (/workspace/arena-inbox/*.json) — the overnight driver
     or any lane drops a job spec here, and this moves it to measure-queue.
  2. polling a remote queue URL if one is ever bound (GATE: off by default —
     no fabricated queue).

Honest: the endpoint-side persistence is the real fix (a KV-bound queue);
this script makes the pod-side half real NOW so a job spec CAN flow through
the whole signed chain the moment the endpoint persists.
"""
import json, time, shutil, sys
from pathlib import Path

QUEUE = Path("/workspace/measure-queue")
INBOX = Path("/workspace/arena-inbox")
INBOX.mkdir(exist_ok=True)
LOG = "/workspace/arena_pickup.log"

def log(*a):
    line = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " " + " ".join(str(x) for x in a)
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")

log("=== arena_pickup daemon start ===")
while True:
    # 1. local inbox drop (the working path — the driver or a lane drops job specs)
    for job_path in sorted(INBOX.glob("*.json")):
        try:
            job = json.loads(job_path.read_text())
            bank = job.get("bank")
            models = job.get("models")
            if not bank or not models:
                log("bad inbox job (needs bank + models):", job_path.name)
                job_path.rename(INBOX / ("BAD-" + job_path.name))
                continue
            # move to measure-queue for the chain daemon
            dest = QUEUE / job_path.name
            shutil.move(str(job_path), str(dest))
            log("bridged:", job_path.name, "->", dest.name, "bank:", bank, "models:", models)
        except Exception as e:
            log("inbox err:", job_path.name, str(e)[:80])
            try: job_path.rename(INBOX / ("ERR-" + job_path.name))
            except Exception: pass
    time.sleep(30)
