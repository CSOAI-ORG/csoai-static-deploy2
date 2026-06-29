#!/usr/bin/env python3
"""
PHASE 229: Public connectivity matrix for SOV3 domains
"""
import urllib.request, urllib.error, json
from datetime import datetime
from pathlib import Path

DOMAINS = [
    "meok.ai",
    "csoai.org",
    "sov3.csoai.org",
    "proofof.ai",
    "csoai-os.meok.ai",
    "meok-deploy.vercel.app",
    "huggingface.co",
    "github.com",
    "localhost",
]

LOCAL_ENDPOINTS = [
    ("http://localhost:8000/api/backend/status", "MEOK Backend"),
    ("http://localhost:3101/mcp", "SOV3 MCP"),
]

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
GOLD = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

print(f"\n{BOLD}{GOLD}🜏 SOV3 PUBLIC CONNECTIVITY MATRIX — {datetime.now().isoformat()[:19]} BST{RESET}\n")

# Public domains
print(f"{BOLD}{'Domain':<35} {'Status':<10} {'HTTP':<8} {'Latency':<10}{RESET}")
print("-" * 70)
for d in DOMAINS:
    try:
        url = f"https://{d}" if not d.startswith("localhost") else f"http://{d}:8000/api/backend/status"
        t0 = datetime.now()
        with urllib.request.urlopen(url, timeout=5) as r:
            elapsed = (datetime.now() - t0).total_seconds()
            status = f"{GREEN}✓{RESET}"
            http_code = str(r.status)
        print(f"{d:<35} {status:<10} {http_code:<8} {elapsed*1000:.0f}ms")
    except urllib.error.HTTPError as e:
        elapsed = (datetime.now() - t0).total_seconds()
        print(f"{d:<35} {YELLOW}⚠{RESET}        {e.code:<8} {elapsed*1000:.0f}ms (HTTP error but reachable)")
    except Exception as e:
        elapsed = (datetime.now() - t0).total_seconds() if 't0' in dir() else 0
        print(f"{d:<35} {RED}❌{RESET}        -        {elapsed*1000:.0f}ms ({type(e).__name__})")

# Local SOV3 endpoints
print(f"\n{BOLD}{'Local SOV3 endpoint':<35} {'Status':<10} {'HTTP':<8} {'Latency':<10}{RESET}")
print("-" * 70)
for url, name in LOCAL_ENDPOINTS:
    try:
        t0 = datetime.now()
        if "3101" in url:
            payload = json.dumps({"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}).encode()
            req = urllib.request.Request(url, data=payload,
                                          headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=5) as r:
                elapsed = (datetime.now() - t0).total_seconds()
                status = f"{GREEN}✓{RESET}"
                http_code = str(r.status)
        else:
            with urllib.request.urlopen(url, timeout=5) as r:
                elapsed = (datetime.now() - t0).total_seconds()
                status = f"{GREEN}✓{RESET}"
                http_code = str(r.status)
        print(f"{name:<35} {status:<10} {http_code:<8} {elapsed*1000:.0f}ms")
    except Exception as e:
        elapsed = (datetime.now() - t0).total_seconds() if 't0' in dir() else 0
        print(f"{name:<35} {RED}❌{RESET}        -        {elapsed*1000:.0f}ms ({type(e).__name__})")

print(f"\n{GREEN}✓ Connectivity check complete{RESET}")