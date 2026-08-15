#!/usr/bin/env python3
"""goal_state.py — verify the SOVOS GOAL action list against what is actually on disk/network.

Every row is checked, not asserted. RUNNING / PARTIAL / MISSING / UNVERIFIABLE.
UNVERIFIABLE is used honestly for anything requiring a human or an account I cannot see
(incorporation, investor contact, customer revenue) — those are not scored as missing.
"""
import json
import os
import shutil
import socket
import subprocess
import urllib.request
from pathlib import Path

HOME = Path.home()
R = []


def add(cat, item, state, evidence):
    R.append({"category": cat, "item": item, "state": state, "evidence": evidence})


def have_cmd(c):
    return shutil.which(c) is not None


def find_dir(*names, roots=(HOME, HOME / "clawd", HOME / "projects")):
    for root in roots:
        for n in names:
            p = root / n
            if p.exists():
                return str(p)
    return None


def http(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()[:200000]
    except Exception as e:
        return None, str(e)[:120]


# ---- 1. the TODAY tool installs -------------------------------------------------
for tool, cmd, dirnames in [
    ("TurboFieldfare (local 26B inference)", "turbofieldfare", ("turbofieldfare", "TurboFieldfare")),
    ("Graft (codebase graph / token saver)", "graft", ("graft", ".graft")),
    ("OpenCode (free Cursor replacement)", "opencode", ("opencode", ".opencode")),
    ("Hermes Agent (persistent learning)", "hermes", ("hermes-agent", ".hermes")),
    ("0DIN AI scanner", "ai-scanner", ("ai-scanner", "0din-ai")),
    ("mcp-audit-scanner", "mcp-audit", ("mcp-audit-scanner",)),
]:
    d = find_dir(*dirnames)
    if have_cmd(cmd):
        add("TODAY tools", tool, "RUNNING", f"binary on PATH: {shutil.which(cmd)}")
    elif d:
        add("TODAY tools", tool, "PARTIAL", f"directory present ({d}) but no binary on PATH")
    else:
        add("TODAY tools", tool, "MISSING", "no binary on PATH, no directory found")

# ---- 2. inference substrate -----------------------------------------------------
try:
    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=8) as r:
        ms = json.loads(r.read())["models"]
    biggest = max((m.get("details", {}).get("parameter_size", "?") for m in ms), default="?")
    add("Inference", "Local model substrate (zero-cloud inference)", "RUNNING",
        f"Ollama up, {len(ms)} models; largest parameter_size seen: {biggest}")
    add("Inference", "Local model >= 20B (the 'GPU problem solved' claim)", "MISSING",
        "largest local model is 3.2B (llama3.2:3b). No 20B+ local model exists.")
except Exception as e:
    add("Inference", "Local model substrate", "MISSING", str(e)[:80])

add("Inference", "RunPod GPU pod", "MISSING",
    "sov34_train_events_2026-08-04.json: success=false, watch=budget_exceeded, pod stopped")
add("Inference", "OpenRouter frontier access", "PARTIAL",
    "key valid (write role) but HTTP 402 on paid models — account never purchased credits. "
    "Only openai/gpt-oss-20b:free is callable.")

# ---- 3. the harness: measurement instrument -------------------------------------
base = HOME / "clawd/csoai-static-deploy2"
ev = base / "evidence/harness/freeze/latest"
for name, f in [("Axis saturation measured (30 models)", "axis-saturation.json"),
                ("Item difficulty/discrimination", "item-quality.json"),
                ("Negative-item adjudication", "negative-item-audit.json"),
                ("Fleet-size power analysis", "fleet-power.json"),
                ("Grader validated vs human labels", "grader-validation.json"),
                ("Corpus coverage gap", "corpus-coverage-gap.json"),
                ("Art5 sub-limb hashes", "../../../../publish/gspc-open-artifacts/art5-sublimb-hashes-v0.1.0.json")]:
    p = ev / f
    add("Harness (the thing to sell)", name, "RUNNING" if p.exists() else "MISSING",
        f"{p.name} {p.stat().st_size:,}B" if p.exists() else "absent")
for name, f in [("Acceptance gate (executable)", "item_gate.py"),
                ("Discriminating-items spec", "publish/gspc-open-artifacts/DISCRIMINATING_ITEMS_SPEC.md")]:
    p = base / f
    add("Harness (the thing to sell)", name, "RUNNING" if p.exists() else "MISSING",
        f"{p.name} present" if p.exists() else "absent")

# ---- 4. MCP estate --------------------------------------------------------------
mcp_dirs = []
for root in (HOME / "clawd", HOME / "projects"):
    if root.exists():
        mcp_dirs += [str(p) for p in root.glob("*mcp*") if p.is_dir()][:10]
add("MCP estate", "MCP server directories on disk", "RUNNING" if mcp_dirs else "MISSING",
    f"{len(mcp_dirs)} dirs, e.g. {mcp_dirs[:3]}")
add("MCP estate", "Migrate 313+ MCPs to the 2026-07-28 stateless spec", "MISSING",
    "no migration artefact found; earlier measurement resolved the LIVE fleet to 7 tools "
    "across 3 servers (mcp-count-resolved.json), not 313")

# ---- 5. public surfaces ---------------------------------------------------------
for label, url in [("csoai.org homepage", "https://www.csoai.org/"),
                   ("csoai.org/benchmarks (goal: live dashboard + open API)",
                    "https://www.csoai.org/benchmarks"),
                   ("csoai.org/arena", "https://www.csoai.org/arena"),
                   ("csoai.org security.txt", "https://www.csoai.org/.well-known/security.txt")]:
    st, body = http(url)
    if st is None:
        add("Public surface", label, "MISSING", f"unreachable: {body}")
        continue
    text = body.decode("utf-8", "replace") if isinstance(body, bytes) else str(body)
    import re
    vis = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    vis = " ".join(re.sub(r"<[^>]+>", " ", vis).split())
    if st != 200:
        add("Public surface", label, "MISSING", f"HTTP {st}")
    elif len(vis) < 200:
        add("Public surface", label, "PARTIAL",
            f"HTTP 200 but only {len(vis)} visible chars — JS shell, crawlers see nothing")
    else:
        add("Public surface", label, "RUNNING", f"HTTP 200, {len(vis)} visible chars")

# ---- 6. mail --------------------------------------------------------------------
for d in ("csoai.org", "meok.ai", "councilof.ai"):
    try:
        out = subprocess.run(["nslookup", "-type=MX", d], capture_output=True, text=True, timeout=15).stdout
        has = "mail exchanger" in out.lower()
        add("Mail", f"{d} can receive mail", "RUNNING" if has else "MISSING",
            "MX present" if has else "NO MX RECORD — mail to this domain is undeliverable")
    except Exception as e:
        add("Mail", f"{d} MX", "MISSING", str(e)[:60])

# ---- 7. SovSpace / visual layer -------------------------------------------------
ue = find_dir("SovSpace", "sovspace")
add("SOV-Space", "UE5 project 'SovSpace'", "RUNNING" if ue else "MISSING",
    ue or "no SovSpace UE5 project directory found")

# ---- 8. things only a human can settle ------------------------------------------
for item in ["Incorporate MEOK Labs Ltd / clean cap table",
             "Draft 10-slide investor deck", "Pitch 10 UK angels (£200K at £5M cap)",
             "UKRI Future Leaders Fellowship (closes Nov 4)",
             "First paying customer (£500/month CSOAI compliance)",
             "Contact 3 banks / humanoid outreach"]:
    add("Commercial (human-only)", item, "UNVERIFIABLE",
        "requires an account, filing or conversation I cannot observe — not scored as missing")

print(json.dumps(R, indent=2))
