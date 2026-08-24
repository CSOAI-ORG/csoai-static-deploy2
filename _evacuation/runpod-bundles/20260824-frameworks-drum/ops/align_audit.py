#!/usr/bin/env python3
"""TOP-DOWN ALIGNMENT AUDITOR — every surface vs the master (v1.4) + live counts.

Checks: master version vs manifest/agent-card · registry note vs live item count ·
PACK_INDEX/README version mentions · llms.txt/README path resolution · catalog counts vs
cards · reg feed count vs regulation items · scorecard freshness · dual-walk verdict ·
stale hardcoded counts anywhere in public surfaces. Exit 1 on any drift.
"""
import json
import os
import re
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(PACK, "docs", "MASTER_FRAMEWORK.md")
CATALOG = os.path.join(PACK, "catalog.json")
REG = os.path.join(PACK, "feeds", "reg_events.json")
SCORE = os.path.join(PACK, "docs", "SCORECARD.md")
DUAL = os.path.join(PACK, "feeds", "dualwalk_report.json")
STALE_COUNTS = ["150 items", "555-item", "557 items", "559 items", "581 items", "582 items", "v1.1 ", "v1.2 ", "v1.3 "]

failures = []


def check(name, ok, detail=""):
    print(f"  {'ok ' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def main():
    print("TOP-DOWN ALIGNMENT AUDIT")
    master = open(MASTER, encoding="utf-8").read()
    m = re.search(r"OAI Master Framework · (v[\d.]+)", master)
    mv = m.group(1) if m else "?"
    check("master version parsed", mv, mv)
    mvnum = mv.lstrip("v")

    manifest = json.load(open(os.path.join(PACK, "mcp", "manifest.json")))
    agent = json.load(open(os.path.join(PACK, "a2a", "agent-card.json")))
    check("manifest version == master", manifest.get("version", "").startswith(mvnum), manifest.get("version"))
    check("agent-card version == master", agent.get("version", "").startswith(mvnum), agent.get("version"))

    registry = open(os.path.expanduser("~/master-harness/mcp/registry.yaml"), encoding="utf-8").read()
    cat = json.load(open(CATALOG))
    n_items = len(cat["items"])
    check("registry tile mentions live count", str(n_items) in registry, f"{n_items}")

    pack = open(os.path.expanduser("~/master-harness/knowledge/PACK_INDEX.md"), encoding="utf-8").read()
    readme = open(os.path.join(PACK, "README.md"), encoding="utf-8").read()
    check("PACK_INDEX mentions master version", mv in pack)
    check("README mentions master version", mv in readme)

    # stale hardcoded counts
    stale_hits = []
    for f in ("README.md", "llms.txt", "docs/WIRING.md"):
        text = open(os.path.join(PACK, f), encoding="utf-8").read()
        for s in STALE_COUNTS:
            if s in text:
                stale_hits.append(f"{f}: {s!r}")
    check("no stale hardcoded counts", not stale_hits, "; ".join(stale_hits[:3]))

    # llms.txt path resolution
    missing = []
    for line in open(os.path.join(PACK, "llms.txt"), encoding="utf-8"):
        for p in re.findall(r"docs/[A-Za-z0-9_./-]+|ops/[A-Za-z0-9_./-]+|feeds/[A-Za-z0-9_./-]+|mcp/[A-Za-z0-9_./-]+|a2a/[A-Za-z0-9_./-]+", line):
            if not os.path.exists(os.path.join(PACK, p)):
                missing.append(p)
    check("llms.txt refs resolve", not missing, "; ".join(missing[:3]))

    # README path resolution
    rmissing = []
    for line in open(os.path.join(PACK, "README.md"), encoding="utf-8"):
        for p in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|py|json|sh))`", line):
            if not os.path.exists(os.path.join(PACK, p)):
                rmissing.append(p)
    check("README refs resolve", not rmissing, "; ".join(rmissing[:3]))

    # catalog counts vs cards
    dirs = {"framework": "frameworks", "charter": "charters", "regulation": "regulations",
            "article": "articles", "sector": "sectors", "benchmark": "benchmarks"}
    expected = {f"{dirs[i['kind']]}/{i['id']}.md" for i in cat["items"]}
    actual = set()
    for d in set(dirs.values()):
        actual |= {f"{d}/{f}" for f in os.listdir(os.path.join(PACK, d)) if f.endswith(".md")}
    check("cards == items", expected == actual, f"{len(expected - actual)} missing, {len(actual - expected)} stale")

    # reg feed count vs regulation items (public only)
    reg = json.load(open(REG))
    reg_items = sum(1 for i in cat["items"] if i["kind"] == "regulation" and not i.get("internal"))
    check("reg feed count == regulation items", reg["count"] == reg_items, f"{reg['count']} vs {reg_items}")

    # scorecard freshness (grace: today or yesterday — the midnight boundary must not
    # false-alarm before the next scorecard.py regen; ledger #23)
    if os.path.exists(SCORE):
        import datetime
        sc = open(SCORE, encoding="utf-8").read()
        today = datetime.date.today().isoformat()
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        check("scorecard fresh (today or yesterday)", today in sc or yesterday in sc)
    else:
        check("scorecard exists", False)

    # dual-walk verdict
    if os.path.exists(DUAL):
        d = json.load(open(DUAL))
        check("dual-walk verdict REAL", "REAL" in d.get("verdict", ""), d.get("verdict"))
    else:
        check("dualwalk report exists", False)

    print()
    if failures:
        print(f"ALIGNMENT AUDIT: {len(failures)} FAILURES — {failures}")
        sys.exit(1)
    print("ALIGNMENT AUDIT: ALL ALIGNED")
    sys.exit(0)


if __name__ == "__main__":
    main()
