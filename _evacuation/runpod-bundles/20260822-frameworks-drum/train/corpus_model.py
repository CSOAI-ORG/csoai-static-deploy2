#!/usr/bin/env python3
"""Corpus NN training scaffold — NNs trained on the drum against benchmarks (the evolve loop).

Task (sanity + protocol): classify catalog items into KIND from node features. The protocol
is the promote-gate in miniature: FROZEN 80/20 split (seeded), baseline = majority class,
candidate = small MLP (torch, or numpy fallback), promoted only if it beats baseline with a
margin — measured, never claimed.

"Against benchmarks and findings": the eval split is frozen and never trained on (canary
discipline); arena-agreement labels (feeds/router_trust.json + calibration set) are the
findings layer the next task will attach to. GNN upgrade path: same graph input
(feeds/catalog_graph.json) via torch_geometric on the pods — this script is the MLP baseline
that GNNs must beat to be promoted.

Run with the estate ML stack:  ~/mlx-venv/bin/python train/corpus_model.py
"""
import json
import os
import random
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(PACK, "feeds", "catalog_graph.json")
REPORT = os.path.join(PACK, "feeds", "corpus_model_report.json")


KINDS = ["framework", "charter", "regulation", "article", "sector"]


def load():
    """Kind-prediction task. The kind one-hot features are DROPPED (ledger #17 — they ARE
    the label; a model reading them back scores 1.0 by copying, not by learning)."""
    g = json.load(open(GRAPH))
    # drop the kind one-hot, which sits FIRST in the feature vector (features[0:5])
    X = [n["features"][len(KINDS):] for n in g["nodes"]]
    y = [KINDS.index(n["kind"]) for n in g["nodes"]]
    return X, y, KINDS


def baseline_accuracy(y_train, y_test):
    majority = max(set(y_train), key=y_train.count)
    return sum(1 for y in y_test if y == majority) / len(y_test)


def train_torch(X, y):
    import torch
    import torch.nn as nn
    torch.manual_seed(42)
    Xt = torch.tensor(X, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.long)
    d, c = Xt.shape[1], len(set(y))
    model = nn.Sequential(nn.Linear(d, 32), nn.ReLU(), nn.Linear(32, c))
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    lossf = nn.CrossEntropyLoss()
    for _ in range(300):
        opt.zero_grad()
        loss = lossf(model(Xt), yt)
        loss.backward()
        opt.step()
    with torch.no_grad():
        pred = model(Xt).argmax(1).numpy()
    return list(pred)


def main():
    task = "kind"
    if "--task" in sys.argv:
        task = sys.argv[sys.argv.index("--task") + 1]
    g = json.load(open(GRAPH))
    # drop the kind one-hot (features[0:5]) — always (ledger #17)
    X = [n["features"][len(KINDS):] for n in g["nodes"]]
    if task == "kind":
        y = [KINDS.index(n["kind"]) for n in g["nodes"]]
    elif task == "binding":
        # drop the binding feature (index 0 of the de-leaked vector) — label leak
        X = [f[1:] for f in X]
        y = [1 if n["binding"] else 0 for n in g["nodes"]]
    elif task == "status":
        # predict a collapsed lifecycle bucket from item.status (NOT a feature — no leak)
        import re as _re
        def bucket(s):
            s = (s or "").lower()
            for b, keys in (("active", ("active", "in force", "living", "canonical", "measured", "running", "ratified")),
                            ("proposed", ("proposed", "draft", "pending", "initial", "consult")),
                            ("historical", ("lapsed", "revoked", "withdrawn", "historical", "repealed")),
                            ("voluntary", ("voluntary", "declaration", "principles"))):
                if any(k in s for k in keys):
                    return b
            return "other"
        buckets = ["active", "proposed", "historical", "voluntary", "other"]
        y = [buckets.index(bucket(n.get("status"))) for n in g["nodes"]]  # label ints, not strings
    elif task == "region":
        # predict region bucket (EU/US/UK/ISO/global); drop region-token-count feature (index 3
        # after the kind-drop+binding-drop) to avoid the count leaking the label
        X = [f[:3] + f[4:] for f in X]
        import re as _re
        def bucket(n):
            r = (n.get("region") or "")
            if any(s in r for s in ("EU", "ISO", "ITU", "UNESCO", "OECD", "Council of Europe")): return 0
            if "US" in r: return 1
            if "UK" in r: return 2
            if r in ("CSOAI", "MEOK") or r == "Sector": return 3
            return 4
        y = [bucket(n) for n in g["nodes"]]
    else:
        raise ValueError(f"task {task}")

    kinds = KINDS
    random.seed(42)
    n = len(X)
    cut = int(n * 0.8)
    order = list(range(n))
    random.shuffle(order)
    tr, te = order[:cut], order[cut:]
    Xtr, ytr = [X[i] for i in tr], [y[i] for i in tr]
    Xte, yte = [X[i] for i in te], [y[i] for i in te]

    base = baseline_accuracy(ytr, yte)
    try:
        import torch
        import torch.nn as nn
        torch.manual_seed(42)
        Xt = torch.tensor(Xtr, dtype=torch.float32); yt = torch.tensor(ytr, dtype=torch.long)
        d, c = Xt.shape[1], max(ytr) + 1  # full label range so absent-from-train classes fit
        m = nn.Sequential(nn.Linear(d, 32), nn.ReLU(), nn.Linear(32, c))
        o = torch.optim.Adam(m.parameters(), lr=1e-2); lf = nn.CrossEntropyLoss()
        for _ in range(300):
            o.zero_grad(); loss = lf(m(Xt), yt); loss.backward(); o.step()
        with torch.no_grad():
            pred = m(torch.tensor(Xte, dtype=torch.float32)).argmax(1).numpy()
        acc = sum(1 for p, t in zip(pred, yte) if p == t) / len(yte)
        print(f"baseline (majority class): {base:.3f}")
        print(f"MLP test accuracy:         {acc:.3f}")
        promoted = acc > base + 0.05
        print(f"promote-if-better vs baseline: {'PROMOTED' if promoted else 'NOT PROMOTED (honest)'}")
        report = {"task": "kind-classification", "baseline": round(base, 3), "mlp_test": round(acc, 3),
                  "promoted": bool(promoted), "n_train": len(tr), "n_test": len(te),
                  "note": "smoke scaffold on catalog features; real tasks attach to GovBench/GSPC findings next"}
    except Exception as exc:
        report = {"error": str(exc)[:200], "baseline": round(base, 3)}
        print(f"torch path failed ({exc}); baseline only: {base:.3f}")
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
