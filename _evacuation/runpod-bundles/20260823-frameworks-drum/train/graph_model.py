#!/usr/bin/env python3
"""Graph-model (GNN-lite) on the catalog graph — does GRAPH STRUCTURE help beyond the MLP?

Pure-torch message passing (GraphSAGE-style mean-pool, no torch_geometric required), same
task + protocol as train/corpus_model.py: frozen 80/20 split, baseline = majority class,
promote-if-better. The honest comparison: MLP (0.592) vs GNN-lite (this). Kind one-hot
features are DROPPED (ledger #17 — label leak). Transductive note: message passing uses the
full graph (standard node-classification practice); labels only from the train split.

Run: ~/mlx-venv/bin/python train/graph_model.py
"""
import json
import os
import random
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(PACK, "feeds", "catalog_graph.json")
REPORT = os.path.join(PACK, "feeds", "graph_model_report.json")
KINDS = ["framework", "charter", "regulation", "article", "sector", "benchmark"]


def main():
    g = json.load(open(GRAPH))
    nodes = g["nodes"]
    F = [n["features"][len(KINDS):] for n in nodes]  # drop kind one-hot (leak, ledger #17)
    Y = [KINDS.index(n["kind"]) for n in nodes]
    N = len(nodes)
    ei = g["edge_index"]

    random.seed(42)
    order = list(range(N)); random.shuffle(order)
    cut = int(N * 0.8)
    tr, te = set(order[:cut]), order[cut:]

    import torch
    import torch.nn as nn
    torch.manual_seed(42)
    X = torch.tensor(F, dtype=torch.float32)
    y = torch.tensor(Y, dtype=torch.long)
    d = X.shape[1]
    C = len(KINDS)

    # adjacency (COO -> dense bool)
    adj = torch.zeros(N, N, dtype=torch.bool)
    for s, t in zip(ei[0], ei[1]):
        adj[s, t] = True
        adj[t, s] = True

    class GraphConv(nn.Module):
        def __init__(self, din, dout):
            super().__init__()
            self.W = nn.Linear(2 * din, dout)  # concat(x, neighbor-mean) -> 2*din

        def forward(self, x, adj):
            deg = adj.float().sum(1).clamp(min=1).unsqueeze(1)
            # mean-pool neighbor features, normalized
            nb = torch.mm(adj.float(), x) / deg
            return torch.relu(self.W(torch.cat([x, nb], 1)))  # GraphSAGE concat

    class GNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.c1 = GraphConv(d, 32)
            self.c2 = GraphConv(32, 32)
            self.head = nn.Linear(32, C)

        def forward(self, x, adj):
            h = self.c1(x, adj)
            h = self.c2(h, adj)
            return self.head(h)

    model = GNN()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    lossf = nn.CrossEntropyLoss()
    tr_list = sorted(tr)
    for epoch in range(400):
        opt.zero_grad()
        h = model(X, adj)  # transductive: full-graph message passing; labels train-only
        loss = lossf(h[tr_list], y[tr_list])
        loss.backward()
        opt.step()
    with torch.no_grad():
        pred = model(X, adj).argmax(1).numpy()
    acc = sum(1 for i in te if pred[i] == y[i].item()) / len(te)
    majority = max((y[i].item() for i in tr_list), key=lambda v: sum(1 for j in tr_list if y[j].item() == v))
    base = sum(1 for i in te if y[i].item() == majority) / len(te)
    print(f"baseline (majority): {base:.3f}")
    print(f"GNN-lite test acc:    {acc:.3f}   (MLP reference: 0.592)")
    promoted = acc > 0.592 + 0.02
    print(f"vs MLP: {'PROMOTED (graph structure helps)' if promoted else 'NOT PROMOTED (honest — MLP stands)'}")
    report = {"task": "kind-classification", "baseline": round(base, 3), "mlp_reference": 0.592,
              "gnn_test": round(acc, 3), "promoted_vs_mlp": bool(promoted),
              "transductive_note": "full-graph message passing, labels train-only (standard node-classification practice)"}
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
