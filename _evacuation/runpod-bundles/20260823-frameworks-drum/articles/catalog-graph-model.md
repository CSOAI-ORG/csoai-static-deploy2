# Catalog graph + NN/GNN model-layer (kind .642 / binding .908 / GNN .725 / feature layer)

- **Kind:** article | **Issuer:** CSOAI LTD | **Region:** CSOAI
- **Binding:** no | **Status:** measured 2026-08-22
- **Effective:** 2026-08-22

The drum's catalog as a learnable graph (596 nodes, 11,035 issuer/region edges) + NN/GNN trained on it with the promote-gate protocol: kind-classification 0.283 baseline -> 0.642 MLP -> 0.725 GNN-lite (pure-torch message passing); binding-prediction 0.850 -> 0.908 MLP; region NOT-PROMOTED (degenerate baseline).  Kind one-hot and binding features dropped as label leaks (ledger #17). Models are the FEATURE LAYER for a SOV SIGNAL-style gauge, not the gauge itself. Pod path complete (ship_to_pod + ingest_sovos).

## Sources
- master-harness/knowledge/frameworks-drum/train/ (build_graph.py, corpus_model.py, graph_model.py)
