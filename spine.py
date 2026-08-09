#!/usr/bin/env python3
"""spine.py — the SPINE: the J-Space card graph. Retrieval now; GNN reasoning staged for GPU.

    python3 spine.py                 # build the graph from the Phlabet deck, print structure
    python3 spine.py --query "..."   # surface the J-cards relevant to a task
    python3 spine.py --json          # machine-readable graph

WHERE THIS SITS (SOVOS GOAL, top→bottom)
  J-Space cards (Phlabet) ──▶ spine.py builds the GRAPH ──▶ the mind reasons over it
The SPINE in the doc is "GNN Core Reasoning". A GNN needs a graph and needs training. This file builds
the graph and makes it QUERYABLE today — given a task, it surfaces the relevant compressed lessons.
That is the honest half you can run with no GPU. The learned half (a GNN that reasons over the graph
to route and predict) is staged: the data structure is here, the training is GPU-gated and must be
pre-registered and measured before any capability is claimed. A graph you can query is real; a GNN you
have not trained is not, so this file will not pretend to reason — it retrieves.

An empty deck is FATAL, never a silent pass.
"""
import argparse, json, os, sys, re, hashlib, itertools

DECK = os.path.expanduser("~/clawd/_alignment/PHLABET_DECK.json")
GRAPH = os.path.expanduser("~/clawd/_alignment/SPINE_GRAPH.json")


def toks(s):
    return set(re.findall(r"[a-z0-9]+", (s or "").lower()))


def build(cards):
    """Nodes = J-cards. Edge (i,j) when they share axis, anchor-token, or drift target — the theme-level
    links a GNN would later weight. Retrieval today walks these edges; training would learn them."""
    nodes = [{"id": i, "glyph": c["glyph"], "archetype": c["archetype"], "axis": c["axis"],
              "correct": c["correct"], "drift": c.get("drift"), "n_honey": c.get("n_honey", 0)}
             for i, c in enumerate(cards)]
    edges = []
    for a, b in itertools.combinations(range(len(cards)), 2):
        ca, cb = cards[a], cards[b]
        reasons = []
        if ca["axis"] == cb["axis"]: reasons.append("axis")
        if ca.get("drift") and ca.get("drift") == cb.get("drift"): reasons.append("drift")
        if ca.get("correct") and ca.get("correct") == cb.get("correct"): reasons.append("gold")
        if reasons:
            edges.append({"a": a, "b": b, "on": reasons, "w": len(reasons)})
    return nodes, edges


def query(cards, nodes, q):
    """Surface the cards a task should consult. Token overlap over archetype+anchor+trigger — the
    deterministic stand-in for the GNN's learned relevance. Returns ranked, with the score shown."""
    qt = toks(q)
    scored = []
    for i, c in enumerate(cards):
        ct = toks(c["archetype"]) | toks(" ".join(c.get("example_anchors", []))) | toks(c.get("trigger", ""))
        overlap = len(qt & ct)
        if overlap:
            scored.append((overlap, i, c))
    scored.sort(reverse=True, key=lambda x: (x[0], x[2].get("n_honey", 0)))
    return scored


def load_deck():
    if not os.path.exists(DECK):
        sys.exit("NO DECK: run phlabet.py first — a spine with no cards is not an empty spine, it is no spine.")
    deck = json.load(open(DECK))
    cards = deck.get("cards", [])
    if not cards:
        sys.exit("DECK EMPTY: 0 J-cards. Either no honey yet, or the run is incomplete. Not a spine.")
    return deck, cards


def main():
    ap = argparse.ArgumentParser(description="SPINE — the J-Space card graph")
    ap.add_argument("--query")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    deck, cards = load_deck()
    nodes, edges = build(cards)

    if a.query:
        hits = query(cards, nodes, a.query)
        if not hits:
            print(f"no J-card matches '{a.query}' — the mind has no measured lesson here yet.")
            return
        print(f"SPINE · cards relevant to: {a.query!r}\n")
        for score, i, c in hits[:8]:
            print(f"  {c['glyph']}  [{score}] {c['archetype']:<26} → {c['correct']}  ({c['trigger']})")
        return

    graph = {"spine": "J-Space", "n_nodes": len(nodes), "n_edges": len(edges),
             "deck_sha256": deck.get("sha256"), "nodes": nodes, "edges": edges,
             "gnn": "NOT_TRAINED — retrieval only; learned reasoning is GPU-gated and must be measured first"}
    graph["sha256"] = hashlib.sha256(json.dumps({"n": len(nodes), "e": len(edges),
                                                 "d": deck.get("sha256")}, sort_keys=True).encode()).hexdigest()[:16]
    json.dump(graph, open(GRAPH, "w"), indent=2)
    if a.json:
        print(json.dumps(graph, indent=2)); return
    print(f"SPINE · {len(nodes)} J-cards · {len(edges)} edges (theme links) · deck {deck.get('sha256')}\n")
    deg = {}
    for e in edges:
        deg[e["a"]] = deg.get(e["a"], 0) + 1; deg[e["b"]] = deg.get(e["b"], 0) + 1
    for i, c in enumerate(nodes):
        print(f"  {c['glyph']}  {c['archetype']:<26} axis={c['axis']:<6} deg={deg.get(i,0):<3} n_honey={c['n_honey']}")
    print(f"\n  graph signed sha256:{graph['sha256']} → {GRAPH}")
    print("  GNN reasoning: NOT trained — retrieval works today; the learned spine is GPU-gated.")


if __name__ == "__main__":
    main()
