#!/usr/bin/env python3
"""MINE GAPS — reusable estate gap-miner (P15-43).

Scans estate corpora for framework-like instruments (ISO/NIST/BSI/ITU/ECSS codes, named
Acts/Directives/Standards) and monorepo packages NOT yet in the drum catalog. Run it after
any big estate change; add the genuine finds to build_catalog.py SEED.

Run:  python3 ops/mine_gaps.py [--codes] [--packages] [--verbose]
"""
import glob
import json
import os
import re
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORPORA = [
    "/Users/nicholas/clawd/csoai-static-deploy2/SOVOS/*.md",
    "/Users/nicholas/clawd/_alignment/*.md",
    "/Users/nicholas/clawd/sovereign-substrate/*.md",
    "/Users/nicholas/clawd/meok-compliance-gateway/docs/**/*.md",
    "/Users/nicholas/clawd/csoai-platform/docs/**/*.md",
    "/Users/nicholas/clawd/csoai-dashboard-master/content/**/*.md",
    "/Users/nicholas/clawd/kimi-regen/SOVOS/*.md",
    "/Users/nicholas/clawd/master-harness/knowledge/*.md",
    "/Users/nicholas/clawd/_findings/**/*.md",
    "/Users/nicholas/clawd/kimi-regen/**/*.md",
    "/Users/nicholas/clawd/sovereign-charters/**/*.md",
    "/Users/nicholas/clawd/openpatent-hive/**/*.md",
    "/Users/nicholas/clawd/meok-universe/**/*.md",
    "/Users/nicholas/clawd/csoai-org/**/*.md",
    "/Users/nicholas/clawd/_TABS/_inventory/**/*.md",
    "/Users/nicholas/clawd/_TABS/**/*.md",
    "/Users/nicholas/clawd/proofof-site/**/*.md",
    "/Users/nicholas/clawd/sim-world-data/**/*.md",
    "/Users/nicholas/clawd/_findings/**/*.md",
]

CODE_RE = re.compile(
    r"\b(ISO/IEC\s?\d{4,5}(?::\d{4})?|ISO\s?\d{4,5}|NIST\s?(?:SP\s?\d{3}-?\d*|AI\s?\d{3}-?\d*|IR\s?\d{3,4})"
    r"|BSI\s?(?:PAS|EN)\s?\d{3,5}|ITU-T?\s?[A-Z0-9.\-]{2,10}|ECSS-[A-Z]{2,4}-[0-9A-Z\-]+)\b")


def load_have():
    cat = json.load(open(os.path.join(PACK, "catalog.json")))
    have = set()
    for i in cat["items"]:
        have.add(re.sub(r"[^a-z0-9]+", "", i["name"].lower()))
        d = i.get("description") or ""
        have.add(re.sub(r"[^a-z0-9]+", "", d.lower())[:40])
        # also add any instrument CODES present in the item (normalized), so already-indexed
        # standards like 'ISO/IEC 27001' don't report as missing
        for m in CODE_RE.findall(i["name"] + " " + d):
            code = re.sub(r"[^a-z0-9]+", "", m.lower())
            have.add(code)
            # a "ISO/IEC 27001" entry also satisfies a corpus "ISO 27001" reference (and vice
            # versa) — add the plain variant so already-indexed standards stop reporting missing
            for j, c in enumerate(code):
                pass
            m2 = re.match(r"(isoiec|iso|nist|bsi|itut|ecss)(.+)$", code)
            if m2:
                have.add(m2.group(1) + m2.group(2))
                have.add(m2.group(2) + m2.group(1))
            elif code.startswith("iso"):
                have.add("iso" + code[3:])
                have.add("isoicec" + code[3:])
    return have


def mine_codes(have, verbose=False):
    miss = set()
    for c in CORPORA:
        for f in glob.glob(c, recursive=True):
            if not os.path.isfile(f):
                continue
            try:
                t = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for m in CODE_RE.findall(t):
                m = m.strip()
                k = re.sub(r"[^a-z0-9]+", "", m.lower())
                bare = re.sub(r"^(isoiec|iso|iec|nistsp|nistai|nistir|bsi|itut|ecss)", "", k)
                if len(bare) > 3 and bare not in have and k not in have:
                    miss.add(m)
    return sorted(miss)


def mine_packages(have, verbose=False):
    miss = []
    for p in sorted(glob.glob("/Users/nicholas/clawd/councilof-ai-monorepo/packages/*")):
        name = os.path.basename(p)
        k = re.sub(r"[^a-z0-9]+", "", name.lower())
        if k not in have:
            miss.append(name)
    return miss


if __name__ == "__main__":
    have = load_have()
    verbose = "--verbose" in sys.argv
    if "--codes" in sys.argv or "--packages" not in sys.argv:
        codes = mine_codes(have)
        print(f"instrument codes MISSING: {len(codes)}")
        for m in codes:
            print("  -", m)
    if "--packages" in sys.argv:
        pkgs = mine_packages(have)
        print(f"monorepo packages MISSING: {len(pkgs)}")
        for m in pkgs:
            print("  -", m)
