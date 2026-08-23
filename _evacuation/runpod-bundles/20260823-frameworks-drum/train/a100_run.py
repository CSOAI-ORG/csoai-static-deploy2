#!/usr/bin/env python3
"""A100 CUDA trainer — the drum's GNN+NN on the estate's idle A100 (put the GPU to work).

Runs the GraphSAGE-style GNN (and the kind/binding tasks) on CUDA when available, reports the
device + throughput + accuracy. The A100 is the estate's training GPU; the Mac and the 3090 are
fallbacks. This file IS the pod-side training entrypoint.

Run (on the A100): python3 train/a100_run.py
"""
import json
import os
import sys
import time

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(PACK, "feeds", "catalog_graph.json")


def gnn(epochs=500):
    import torch
    import torch.nn as nn
    torch.manual_seed(42)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    g = json.load(open(GRAPH))
    KINDS = g["kind_index"]
    X = torch.tensor([n["features"][5:] for n in g["nodes"]], dtype=torch.float32, device=dev)
    y = torch.tensor([KINDS.index(n["kind"]) for n in g["nodes"]], dtype=torch.long, device=dev)
    N, d = X.shape
    C = len(KINDS)
    adj = torch.zeros(N, N, device=dev)
    for s, t in zip(g["edge_index"][0], g["edge_index"][1]):
        adj[s, t] = 1.0
        adj[t, s] = 1.0

    class GC(nn.Module):
        def __init__(self, di, do):
            super().__init__()
            self.W = nn.Linear(2 * di, do)
        def forward(self, x, a):
            deg = a.sum(1).clamp(min=1).unsqueeze(1)
            nb = a @ x / deg
            return torch.relu(self.W(torch.cat([x, nb], 1)))

    class GNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.c1, self.c2, self.h = GC(d, 32), GC(32, 32), nn.Linear(32, C)
        def forward(self, x, a):
            z = self.c1(x, a)
            z = self.c2(z, a)
            return self.h(z)

    m = GNN().to(dev)
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    lf = nn.CrossEntropyLoss()
    perm = torch.randperm(N)
    tr, te = perm[:int(N * 0.8)], perm[int(N * 0.8):]
    t0 = time.time()
    for _ in range(epochs):
        opt.zero_grad()
        loss = lf(m(X, adj)[tr], y[tr])
        loss.backward()
        opt.step()
    dt = time.time() - t0
    acc = (m(X, adj)[te].argmax(1) == y[te]).float().mean().item()
    print(f"{dev.upper()} GNN: {N} nodes, {epochs} epochs in {dt:.2f}s ({dt/epochs*1000:.1f} ms/epoch) | test acc {acc:.3f} | device {torch.cuda.get_device_name(0) if dev=='cuda' else 'CPU'}")
    return acc


if __name__ == "__main__":
    sys.exit(0 if gnn() is not None else 1)
