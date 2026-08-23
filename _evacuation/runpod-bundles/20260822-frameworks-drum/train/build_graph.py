#!/usr/bin/env python3
"""Build the catalog-as-GRAPH — the GNN substrate for SOVOS/CSOAI pod training.

Nodes = catalog items (features: kind one-hot, binding, has-issuer, desc length, region token
counts, effective year). Edges = (a) issuer-shared, (b) region-shared, (c) explicit
crosswalk overlap via shared tokens. Emits feeds/catalog_graph.json in COO-friendly format:
  {nodes: [{id, kind, features: [...]}], edge_index: [[src...],[dst...]], edge_type: [...]}

Run: python3 train/build_graph.py   (needs only stdlib; graph is the GNN's input substrate)
"""
import json
import os
import re
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(PACK, "catalog.json")
OUT = os.path.join(PACK, "feeds", "catalog_graph.json")

KINDS = ["framework", "charter", "regulation", "article", "sector"]


def region_tokens(region):
    toks = set()
    if not region:
        return toks
    for part in region.replace("/", " ").split():
        p = re.sub(r"[^a-z]", "", part.lower())
        if len(p) >= 3:
            toks.add(p)
    return toks


def features(item):
    f = [0.0] * len(KINDS)
    if item.get("kind") in KINDS:
        f[KINDS.index(item["kind"])] = 1.0
    f.append(1.0 if item.get("binding") is True else 0.0)
    f.append(1.0 if item.get("issuer") else 0.0)
    f.append(min(1.0, len(item.get("description") or "") / 500.0))
    year = 0
    eff = str(item.get("effective") or "")
    m = re.search(r"(19|20)\d{2}", eff)
    if m:
        year = int(m.group(0))
    f.append(min(1.0, max(0.0, (year - 2015) / 15.0)))
    rt = region_tokens(item.get("region"))
    f.append(min(1.0, len(rt) / 4.0))
    return f


def main():
    cat = json.load(open(CATALOG))
    items = [i for i in cat["items"] if not i.get("internal")]
    idx = {i["id"]: n for n, i in enumerate(items)}
    nodes = [{"id": i["id"], "kind": i["kind"], "binding": i.get("binding") is True, "status": i.get("status") or "", "features": features(i)} for i in items]

    edges = []
    etype = []
    for a in range(len(items)):
        for b in range(a + 1, len(items)):
            ia, ib = items[a], items[b]
            # issuer shared
            if ia.get("issuer") and ib.get("issuer") and ia["issuer"] == ib["issuer"]:
                edges.append((a, b)); etype.append(0)
            # region shared
            ra, rb = region_tokens(ia.get("region")), region_tokens(ib.get("region"))
            if ra & rb:
                edges.append((a, b)); etype.append(1)
    edge_index = [[e[0] for e in edges], [e[1] for e in edges]]

    g = {"nodes": nodes, "node_count": len(nodes), "edge_count": len(edges),
         "feature_dim": len(features(items[0])), "edge_index": edge_index, "edge_type": etype,
         "kind_index": KINDS, "note": "GNN substrate: kind/binding/issuer/region/effective features; issuer+region edges. Train on pods (torch_geometric) or locally via train/corpus_model.py (MLP baseline)."}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(g, fh)
    print(f"graph: {len(nodes)} nodes, {len(edges)} edges, {len(features(items[0]))} features -> {OUT}")


if __name__ == "__main__":
    main()
