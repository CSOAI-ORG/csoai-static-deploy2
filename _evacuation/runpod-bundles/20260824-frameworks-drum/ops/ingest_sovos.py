#!/usr/bin/env python3
"""Ingest the drum into the SOVOS/MEOK OOWM knowledge index (council-oowm substrate).

Makes the drum's surfaces answerable by the OOWM index on any pod that has the
sov33-oowm tree (or this script + a local OOWMIndex). Mapping TESTED 2026-08-21
(5 surfaces ingested, 5/6 queries resolved). Run on the pod after ship_to_pod.sh.

Usage: python3 ops/ingest_sovos.py [--oowm-root /path/to/sov33-oowm] [--out PATH]
"""
import glob
import json
import os
import sys

DRUM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def surface_docs():
    docs = {}
    cat = json.load(open(os.path.join(DRUM, "catalog.json")))
    docs["catalog-digest"] = (f"Catalog has {len(cat['items'])} items across 5 kinds. "
                              f"Counts: {json.dumps(cat['counts'])}. Reg events: "
                              f"{json.load(open(os.path.join(DRUM, 'feeds', 'reg_events.json')))['count']} "
                              f"regulation events east/west/global tagged. Sectors include space family, xAI/Grok, Tesla/AV.")
    for f in ("docs/MASTER_FRAMEWORK.md", "docs/RESEARCH_VALIDATION.md",
              "docs/PHYSICAL_COMPUTATION_MAP.md", "docs/NEXT_100_MOVES.md"):
        p = os.path.join(DRUM, f)
        if os.path.exists(p):
            docs[f.replace("docs/", "doc-").replace(".md", "")] = open(p, encoding="utf-8").read()[:6000]
    return docs


def main():
    oowm_root = None
    if "--oowm-root" in sys.argv:
        oowm_root = sys.argv[sys.argv.index("--oowm-root") + 1]
    candidates = ["/Users/nicholas/clawd/sov33-oowm", "/workspace/sov33-oowm", "/workspace/.stash/mac-backup/clawd/sov33-oowm"]
    for c in candidates:
        if os.path.exists(os.path.join(c, "oowm", "knowledge.py")):
            oowm_root = c
            break
    if not oowm_root:
        print("OOWM knowledge module not found — install sov33-oowm on this host first.")
        return 2
    sys.path.insert(0, oowm_root)
    from oowm.knowledge import OOWMIndex  # noqa: E402

    idx = OOWMIndex()
    docs = surface_docs()
    for name, text in docs.items():
        idx.add_doc(f"frameworks-drum/{name}", name, text)
    idx.build_tfidf()
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    if out:
        idx.save(out)
        print(f"saved index -> {out}")
    print(f"ingested {len(docs)} drum surfaces into OOWM index: {idx.stats()}")
    # probe queries
    for q in ("conformal router", "catalog items", "space sector"):
        top = idx.query(q, k=1)
        print(f"  probe {q!r:22} -> {top[0]['source'] if top else 'NO MATCH'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
