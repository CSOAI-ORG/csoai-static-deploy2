#!/usr/bin/env python3
"""surface_probe.py — content-asserted end-user test board for the estate's public surfaces."""
import json, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

SURFACES = [
    ("csoai.org-apex",        "https://csoai.org/",                    "Council of AI", "GREEN"),
    ("www.csoai.org",         "https://www.csoai.org/",                "Council of AI", "GREEN"),
    ("csoai.org/llms.txt",    "https://csoai.org/llms.txt",            "Council",       "CHECK"),
    ("csoai.org/SOV33_BFT33", "https://csoai.org/SOV33_BFT33_COUNCIL.html", "BFT", "CHECK"),
    ("gspc-scoreboard",       "https://csoai.org/gspc-scoreboard/",    "signed",        "GREEN"),
    ("gspc-index",            "https://csoai.org/gspc-index/",         "57",            "GREEN"),
    ("councilof.ai-apex",     "https://councilof.ai/",                 "Council",       "GREEN"),
    ("j-space",               "https://councilof.ai/j-space/",         "signed",        "GREEN"),
    ("sov-space",             "https://councilof.ai/sov-space/",       "axes",          "CHECK"),
    ("meok.ai",               "https://meok.ai/",                      "MEOK",          "AMBER"),
    ("proofof.ai",            "https://proofof.ai/",                   "proof",         "AMBER"),
    ("mcp-install",           "https://csoai.org/mcp-install.html",    "install",       "CHECK"),
    ("sovereign-os",          "https://csoai.org/sovereign-os.html",   "sovereign",     "CHECK"),
    ("csoai-site.pages.dev",  "https://csoai-site.pages.dev/",         "Council",       "AMBER"),
]
# Lock-words to flag on the two breach files (naming canon: SOV33/sovereign/BFT-33/sov6 must NOT be public)
LOCK = ["SOV33", "sovereign", "BFT-33", "sov6", "SOVOS", "SOV-", "omnipotent"]

def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "council-surface-probe/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", errors="replace")
            return r.status, len(body), body
    except Exception as e:
        return None, 0, str(e)

def lock_hits(body):
    hits = []
    for w in LOCK:
        if w.lower() in body.lower():
            hits.append(w)
    return hits

def probe(item):
    name, url, assert_str, _ = item
    code, size, body = fetch(url)
    if code is None:
        return f"  {name:<30} ERR     {size:<22} — {body[:60]}"
    assert_ok = assert_str.lower() in body.lower()
    lock = lock_hits(body)
    lock_txt = f" LOCK:{','.join(lock)}" if lock else ""
    verdict = "ASSERT-OK" if assert_ok else "NO-ASSERT"
    status = "PASS" if (assert_ok and not lock) else ("BREACH" if lock else "FAIL")
    return f"  {name:30} {code} {size:>7,}B {verdict:10} {status}{lock_txt}"

if __name__ == "__main__":
    print("=== END-USER SURFACE TEST BOARD ===")
    for item in SURFACES:
        print(probe(item))