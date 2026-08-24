#!/usr/bin/env python3
"""Run ALL model tasks in one shot + emit the SOV SIGNAL feature layer (P22-19 + P21-5).

1. run_all: build_graph -> kind + binding + region tasks + GNN-lite -> combined report.
2. emit_features: loads the trained GNN, exports node embeddings (the learned feature layer)
   the SOV SIGNAL gauge consumes — the drum -> feature -> gauge bridge, made real.

Run: ~/mlx-venv/bin/python train/run_all.py   (then --emit for the feature layer)
"""
import json
import os
import subprocess
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(PACK, "feeds", "catalog_graph.json")
FEATURES = os.path.join(PACK, "feeds", "gauge_features.json")


def run_all():
    subprocess.run([sys.executable, "train/build_graph.py"], cwd=PACK, check=True)
    results = {}
    for task in ("kind", "binding", "region", "status"):
        r = subprocess.run([sys.executable, "train/corpus_model.py", "--task", task],
                           cwd=PACK, capture_output=True, text=True)
        rep = os.path.join(PACK, "feeds", "corpus_model_report.json")
        if os.path.exists(rep):
            results[task] = json.load(open(rep))
    subprocess.run([sys.executable, "train/graph_model.py"], cwd=PACK, check=True)
    g = json.load(open(os.path.join(PACK, "feeds", "graph_model_report.json")))
    results["gnn"] = g
    combined = os.path.join(PACK, "feeds", "model_benchmarks.json")
    with open(combined, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    print("model benchmarks ->", combined)
    for k, v in results.items():
        print(f"  {k}: {v.get('mlp_test') or v.get('gnn_test')}")


def emit_features():
    """Export the trained-GNN node embeddings as the SOV SIGNAL feature layer."""
    g = json.load(open(GRAPH))
    nodes = g["nodes"]
    F = [n["features"][5:] for n in nodes]  # drop kind one-hot (leak)
    N = len(nodes)
    KINDS = g["kind_index"]
    Y = [KINDS.index(n["kind"]) for n in nodes]
    ei = g["edge_index"]
    try:
        import torch
        import torch.nn as nn
        torch.manual_seed(42)
        X = torch.tensor(F, dtype=torch.float32)
        y = torch.tensor(Y, dtype=torch.long)
        d, C = X.shape[1], len(KINDS)
        adj = torch.zeros(N, N, dtype=torch.bool)
        for s, t in zip(ei[0], ei[1]):
            adj[s, t] = True; adj[t, s] = True

        class GraphConv(nn.Module):
            def __init__(self, din, dout):
                super().__init__(); self.W = nn.Linear(2 * din, dout)
            def forward(self, x, adj):
                deg = adj.float().sum(1).clamp(min=1).unsqueeze(1)
                nb = torch.mm(adj.float(), x) / deg
                return torch.relu(self.W(torch.cat([x, nb], 1)))

        class GNN(nn.Module):
            def __init__(self):
                super().__init__()
                self.c1 = GraphConv(d, 32); self.c2 = GraphConv(32, 32); self.head = nn.Linear(32, C)
            def forward(self, x, adj):
                h1 = self.c1(x, adj)
                h = self.c2(h1, adj)
                return self.head(h), h1  # h1 = 32-dim first-layer embedding (the feature layer)

        model = GNN()
        opt = torch.optim.Adam(model.parameters(), lr=1e-3); lossf = nn.CrossEntropyLoss()
        all_idx = list(range(N))
        for _ in range(300):
            opt.zero_grad()
            logits, _ = model(X, adj)
            # train on a 80% subset (labels train-only; transductive message passing)
            import random as _r
            _r.seed(42); sub = _r.sample(all_idx, int(N * 0.8))
            loss = lossf(logits[sub], y[sub]); loss.backward(); opt.step()
        with torch.no_grad():
            _, emb = model(X, adj)
            layers = emb.numpy().tolist()
        features_out = [{"id": n["id"], "kind": n["kind"], "embedding": [round(v, 5) for v in e]} for n, e in zip(nodes, layers)]
        with open(FEATURES, "w", encoding="utf-8") as fh:
            json.dump({"note": "SOV SIGNAL feature layer — trained-GNN node embeddings (32-dim) from the catalog graph; the gauge's learned input", "feature_dim": 32, "nodes": features_out}, fh, indent=1)
        print(f"feature layer -> {FEATURES} ({len(features_out)} nodes, 32-dim embeddings)")
        return 0
    except Exception as exc:
        print(f"emit_features: torch unavailable ({exc}) — feature layer not emitted")
        return 1


if __name__ == "__main__":
    if "--emit" in sys.argv:
        sys.exit(emit_features())
    run_all()
