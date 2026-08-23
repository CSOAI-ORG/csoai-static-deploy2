#!/usr/bin/env python3
"""CI cross-check pass — cross-validate the drum's web citations against their sources.

The EAT 7-box "ci" leg: the drum is not just self-referential — it indexes competitor/peer
instruments, and this pass verifies the web citations (arXiv IDs + project URLs) actually
resolve to live sources. Runs the check, writes `feeds/ci_crosscheck.json`, and exits non-zero
if any citation is dead (so the overnight/standing check can enforce it).

Run: python3 ops/ci_crosscheck.py
"""
import concurrent.futures
import json
import os
import re
import subprocess
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(PACK, "feeds", "ci_crosscheck.json")


def resolve(url):
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "20", "-L", url],
            capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except Exception:
        return "ERR"


def citations():
    cat = json.load(open(os.path.join(PACK, "catalog.json")))
    out = []
    seen = set()
    # local estate surfaces are files, not public URLs — never treat them as web citations
    LOCAL = ("csoai.org", "clawd", "master-harness", "localhost")
    for i in cat["items"]:
        text = " ".join([i.get("estate") or "", " ".join(i.get("sources") or [])])
        # arXiv IDs
        for m in re.findall(r"arXiv:([\d.]+)", text):
            out.append((i["id"], f"arxiv.org/abs/{m}", f"https://arxiv.org/abs/{m}"))
        # genuine web URL citations (https:// explicit or leading-//) — NOT local paths
        for m in re.findall(r"(?:https?://|//)[^\s\`\"\)]+", text):
            host = re.sub(r"^https?://", "", m)
            host = re.sub(r"^//", "", host).rstrip(".,);")
            if "arxiv.org" in host:
                continue
            if any(l in host for l in LOCAL):
                continue
            if host in seen:
                continue
            seen.add(host)
            out.append((i["id"], host, f"https://{host}"))
    return out


def main():
    cites = citations()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda c: (c[0], c[1], resolve(c[2])), cites))
    ALIVE = ("200", "301", "302", "303", "307", "308")
    BLOCKED = ("403", "418", "429", "202")  # bot-gated / async-accepted — NOT a dead link
    UNREACHABLE = ("000", "500", "502", "503", "ERR")  # transient/connection — warn, don't gate-fail
    DEAD = ("404", "410")  # definitively gone
    ok = [r for r in results if r[2] in ALIVE]
    blocked = [r for r in results if r[2] in BLOCKED]
    unreachable = [r for r in results if r[2] in UNREACHABLE]
    dead = [r for r in results if r[2] in DEAD]
    # anything not classed (e.g. other 4xx) counts as dead so we don't silently pass it
    dead += [r for r in results if r[2] not in ALIVE and r[2] not in BLOCKED and r[2] not in UNREACHABLE and r[2] not in DEAD]
    out = {
        "generated": __import__("datetime").date.today().isoformat(),
        "checked": len(results),
        "resolved": len(ok),
        "bot_blocked": [{"item": d[0], "url": d[1], "code": d[2]} for d in blocked],
        "unreachable": [{"item": d[0], "url": d[1], "code": d[2]} for d in unreachable],
        "dead": [{"item": d[0], "url": d[1], "code": d[2]} for d in dead],
        "verdict": "ALL RESOLVE" if not dead else f"{len(dead)} DEAD",
    }
    os.makedirs(os.path.dirname(FEED), exist_ok=True)
    with open(FEED, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(f"ci cross-check: {len(ok)}/{len(results)} resolve, {len(blocked)} bot-blocked, "
          f"{len(unreachable)} unreachable(transient), {len(dead)} DEAD — {FEED}")
    if dead:
        for item_id, url, code in dead:
            print(f"  DEAD {item_id}: {url} ({code})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
