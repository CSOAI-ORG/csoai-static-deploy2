#!/usr/bin/env python3
"""Live surface probe v2 — the post-deploy estate state (content-asserted)."""
import json, re, urllib.request
from concurrent.futures import ThreadPoolExecutor

SURFACES = [
    ("csoai.org apex",       "https://csoai.org/",                       "Council of AI", "PASS-expect"),
    ("csoai.org llms.txt",   "https://csoai.org/llms.txt",               "measurement",   "PASS-expect"),
    ("gspc-scoreboard",      "https://csoai.org/gspc-scoreboard/",       "signed",        "PASS-expect"),
    ("gspc-index",           "https://csoai.org/gspc-index/",            "57",            "CHECK"),
    ("councilof.ai apex",    "https://councilof.ai/",                    "Council",       "PASS-expect"),
    ("j-space",              "https://councilof.ai/j-space/",            "signed",        "PASS-expect"),
    ("meok.ai",              "https://meok.ai/",                         "MEOK",          "CHECK"),
    ("proofof.ai",           "https://proofof.ai/",                      "proof",         "CHECK"),
    ("mcp-install",          "https://csoai.org/mcp-install.html",       "install",       "CHECK"),
    ("gspc MCP /mcp",        "https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp", "csoai-gspc-mcp", "PASS-expect"),
    ("city-3d MCP /mcp",     "https://csoai-city-3d-mcp.nicholastempleman.workers.dev/mcp", "csoai-city-3d-mcp", "PASS-expect"),
    ("council-5d-engine",    "https://csoai.org/council-5d-engine.html", "5D",            "CHECK" ),
    ("old sov-5d-engine (redirect)", "https://csoai.org/sov-5d-engine.html", "council", "CHECK"),
]

LOCK = ["sov33", "sovereign", "bft-33", "sov6", "sovos", "sov-"]

def fetch(url, timeout=12, post=None):
    try:
        if post:
            req = urllib.request.Request(url, data=post.encode(), headers={"Content-Type": "application/json", "User-Agent": "council-probe"})
        else:
            req = urllib.request.Request(url, headers={"User-Agent": "council-probe"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", errors="replace")
            return r.status, len(body), body
    except Exception as e:
        return None, 0, str(e)

def probe(item):
    name, url, want, _ = item
    if url.endswith("/mcp"):
        body = None
        code, size, body = fetch(url, post='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}')
    else:
        code, size, body = fetch(url)
    if code is None:
        return f"  {name:28} ERR  — {body[:70]}"
    ok = want.lower() in body.lower()
    locks = [w for w in LOCK if w in body.lower()]
    status = "PASS" if (ok and not locks) else ("LOCK:" + ",".join(locks) if locks else "FAIL(no-assert)")
    kind = "MCP-OK" if url.endswith("/mcp") and "serverInfo" in body else ""
    return f"  {name:28} {code} {size:>7,}B {kind:8} {status}"

if __name__ == "__main__":
    print("=== LIVE SURFACE STATE (post-deploy probe) ===")
    with ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(probe, SURFACES):
            print(r)