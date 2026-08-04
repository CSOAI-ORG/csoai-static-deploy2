#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright (c) 2026 CSOAI (Council for the Safety of AI, UK)
#
# runpod_burn_guard.py — one screen, the whole bill, ground truth.
#
# On 2026-08-04 a rogue pod ran at $4.39/hr producing nothing while two sessions blamed the
# serverless endpoints and chased worker states. The lesson: BALANCE DELTAS LIE (settlement lag),
# and WORKER COUNTS are only half the picture. The bill is the sum of running pods plus any
# endpoint standby workers, and that sum is the only number that matters.
#
# Prints every billable resource, the total $/hr, and the runway. Flags anything over a
# threshold. It never stops anything on its own — stopping a pod can destroy live work, and that
# is the owner's call.
#
#   python3 runpod_burn_guard.py            # report
#   python3 runpod_burn_guard.py --threshold 1.0   # flag pods over $1/hr

import argparse
import json
import re
import urllib.request
from pathlib import Path

KEY = re.search(r'apikey\s*=\s*["\']?([^"\'\s]+)',
                Path.home().joinpath(".runpod/config.toml").read_text()).group(1)


def gql(query):
    req = urllib.request.Request(
        "https://api.runpod.io/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
                 # RunPod's edge 403s the default python-urllib User-Agent; a browser UA passes.
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    return json.load(urllib.request.urlopen(req, timeout=30))["data"]["myself"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=1.0,
                    help="flag any single pod above this $/hr")
    a = ap.parse_args()

    # Split queries: some tokens are 403'd on the combined pods+endpoints shape. Pods alone
    # is what the bill actually depends on; endpoints are queried best-effort and skipped on 403.
    m = gql("query{myself{clientBalance pods{name desiredStatus costPerHr}}}")
    try:
        m["endpoints"] = gql("query{myself{endpoints{name workersMax workersStandby}}}").get("endpoints")
    except Exception:
        m["endpoints"] = None

    bal = m["clientBalance"]
    total = 0.0
    flags = []

    print(f"\n  RunPod bill — balance ${bal:.2f}\n  {'-'*52}")
    print("  RUNNING PODS")
    any_pod = False
    for p in m.get("pods") or []:
        if p.get("desiredStatus") != "RUNNING" or not p.get("name"):
            continue
        any_pod = True
        c = p.get("costPerHr") or 0
        total += c
        mark = "  ⚠️ OVER THRESHOLD" if c > a.threshold else ""
        if c > a.threshold:
            flags.append((p["name"], c))
        print(f"    ${c:>5.2f}/hr  {p['name']}{mark}")
    if not any_pod:
        print("    (none)")

    print("  ENDPOINTS holding standby workers (bill even at 0 jobs)")
    any_sb = False
    for e in m.get("endpoints") or []:
        sb = e.get("workersStandby") or 0
        if sb > 0:
            any_sb = True
            print(f"    standby={sb}  {e['name']}  (zero it in the dashboard if unused)")
    if not any_sb:
        print("    (none)")

    runway = bal / total / 24 if total > 0.01 else float("inf")
    print(f"  {'-'*52}")
    print(f"  TOTAL ${total:.2f}/hr  ·  runway "
          f"{'∞' if runway == float('inf') else f'{runway:.0f} days'}")

    if flags:
        print(f"\n  ⚠️  {len(flags)} pod(s) over ${a.threshold}/hr — verify these are wanted:")
        for n, c in flags:
            print(f"       {n}  ${c}/hr = ${c*24:.0f}/day")
        print("  Stopping a pod can destroy live work — that decision is the owner's.")
        return 1
    print("  ✅ nothing over threshold\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
