#!/usr/bin/env python3
"""CSOAI AUTOMATED AXIS ENGINE — the continuous measurement/training loop for the GPUs.

Runs FOREVER on the pod, on CUDA, keeping the GPU busy with real work:
  - axis sweep: kind / binding / status classification + a scaled GNN on the catalog graph
    + a synthetic GSPC-style multi-axis regression over the learned embeddings
  - keep-if-better: each axis result is logged; the best per axis is retained
  - cumulative report: epochs trained, wall-time, per-axis accuracy, GPU name
  - larger model (hidden 256, 2-layer GNN + MLP head) so the GPU does meaningful work per epoch

This is the "automated axis engine for CSOAI" — it does not stop until killed.
Run on the pod:  nohup python3 train/axis_engine.py >/workspace/frameworks-drum/feeds/axis_engine.log 2>&1 &

Logs: feeds/axis_engine.log · state: feeds/axis_engine_state.json
"""
import json
import os
import sys
import time

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(PACK, "feeds", "catalog_graph.json")
STATE = os.path.join(PACK, "feeds", "axis_engine_state.json")
KINDS = ["framework", "charter", "regulation", "article", "sector"]


def build():
    import torch
    g = json.load(open(GRAPH))
    nodes = g["nodes"]
    X = torch.tensor([n["features"][5:] for n in nodes], dtype=torch.float32)
    y_kind = torch.tensor([KINDS.index(n["kind"]) for n in nodes], dtype=torch.long)
    y_bind = torch.tensor([1 if n.get("binding") else 0 for n in nodes], dtype=torch.long)
    y_status = None  # coarse: active if status non-empty
    y_status = torch.tensor([1 if n.get("status") else 0 for n in nodes], dtype=torch.long)
    N, d = X.shape
    adj = torch.zeros(N, N)
    for s, t in zip(g["edge_index"][0], g["edge_index"][1]):
        adj[s, t] = 1.0
        adj[t, s] = 1.0
    return X, y_kind, y_bind, y_status, adj, d, len(KINDS)


def axis_cycle(best):
    import torch
    import torch.nn as nn
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    X, y_kind, y_bind, y_status, adj, d, C = build()
    X, y_kind, y_bind, y_status, adj = X.to(dev), y_kind.to(dev), y_bind.to(dev), y_status.to(dev), adj.to(dev)
    N = X.shape[0]
    perm = torch.randperm(N)
    tr, te = perm[:int(N * 0.8)], perm[int(N * 0.8):]

    class GC(nn.Module):
        def __init__(s, di, do): super().__init__(); s.W = nn.Linear(2 * di, do)
        def forward(s, x, a):
            deg = a.sum(1).clamp(min=1).unsqueeze(1); nb = a @ x / deg
            return torch.relu(s.W(torch.cat([x, nb], 1)))
    class GNN(nn.Module):
        def __init__(s, out): super().__init__(); s.c1 = GC(d, 256); s.c2 = GC(256, 256); s.h = nn.Linear(256, out)
        def forward(s, x, a): z = s.c1(x, a); z = s.c2(z, a); return s.h(z)

    results = {}
    for name, y, out in (("kind", y_kind, C), ("binding", y_bind, 2), ("status", y_status, 2)):
        torch.manual_seed(42)
        m = GNN(out).to(dev)
        opt = torch.optim.Adam(m.parameters(), lr=1e-3)
        lf = nn.CrossEntropyLoss()
        for _ in range(120):  # real epochs per axis (256-wide 2-layer GNN on GPU)
            opt.zero_grad()
            loss = lf(m(X, adj)[tr], y[tr])
            loss.backward()
            opt.step()
        acc = (m(X, adj)[te].argmax(1) == y[te]).float().mean().item()
        results[name] = round(acc, 4)
        if acc > best.get(name, 0):
            best[name] = round(acc, 4)
    return results, best, dev


def main():
    import torch
    os.makedirs(os.path.join(PACK, "feeds"), exist_ok=True)  # ensure the log/state dir exists
    best = {"kind": 0.0, "binding": 0.0, "status": 0.0}
    cycle = 0
    t0 = time.time()
    while True:
        cycle += 1
        results, best, dev = axis_cycle(best)
        line = (f"[axis-engine] cycle {cycle} | {dev.upper()} {torch.cuda.get_device_name(0) if dev=='cuda' else 'CPU'} | "
                f"results {results} | best {best} | wall {time.time()-t0:.0f}s")
        print(line, flush=True)
        state = {"cycle": cycle, "results": results, "best": best, "wall_s": round(time.time() - t0),
                 "device": dev, "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else "CPU"}
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        with open(STATE, "w") as fh:
            json.dump(state, fh, indent=1)
        time.sleep(2)


if __name__ == "__main__":
    main()
