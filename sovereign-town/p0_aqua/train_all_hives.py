#!/usr/bin/env python3
"""
P1 moat→models — train a per-hive sovereign threat model from each hive's own governed-behaviour data.

This is the data moat made concrete: one distinct dataset + one trained model PER HIVE. At scale this
is the GPU-consuming layer (free credits / RunPod / Vast) — here it runs on CPU to prove the loop.
Saves models/<hive>_threat_nn.pkl + moat_models.json. python3.11 train_all_hives.py
"""
import json, os, io, warnings
warnings.filterwarnings("ignore")
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import joblib, sim

OUT = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(OUT, "models"); os.makedirs(MODELS, exist_ok=True)
NAMES = ["hunger","energy","social","wallet","scarcity","lawlessness","commons","broke&hungry","caring"]
SEEDS = [47, 48, 49]

def feats(r):
    n = r["perception"]["needs"]; w = r["perception"]["wallet"]; t = r["town"]
    caring = 1.0 if r["agent"]["care_style"] in ("gentle","supporter") else 0.0
    return [n["hunger"]/100, n["energy"]/100, n["social"]/100, min(w,12)/12,
            1.0 if r["scarcity"] else 0.0, t["lawlessness"], t["commons"],
            1.0 if (n["hunger"]<30 and w<3) else 0.0, caring]

def profile_for(district):                       # distinct economic season per hive (mirror batch.py)
    idx = list(sim.DISTRICTS.keys()).index(district)
    return {"scarcity": range(3 + idx % 9, 3 + idx % 9 + 4 + idx % 5), "off": (idx + 1) * 1000}

def gen(district):
    buf = io.StringIO()
    p = profile_for(district); sim.SCARCITY_DAYS = set(p["scarcity"])
    for s in SEEDS:
        s += p["off"]
        sim.run_arm("A_governed",   buf, {"sig": ""}, None, sign=False, district=district, seed=s)
        sim.run_arm("B_ungoverned", buf, {"sig": ""}, None, sign=False, district=district, seed=s)
    X, Y = [], []
    for line in buf.getvalue().splitlines():
        r = json.loads(line); X.append(feats(r)); Y.append(1 if r["governance"]["would_block"] else 0)
    return np.array(X), np.array(Y)

moat = {}
print(f"\n  P1 MOAT → MODELS — one sovereign threat model per hive")
print("  " + "-" * 62)
print(f"  {'hive':<16}{'episodes':>9}{'test acc':>9}{'F1':>7}{'model':>20}")
print("  " + "-" * 62)
for d, meta in sim.DISTRICTS.items():
    X, Y = gen(d)
    Xtr, Xte, Ytr, Yte = train_test_split(X, Y, test_size=0.3, random_state=47, stratify=Y)
    clf = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=300, random_state=47).fit(Xtr, Ytr)
    pred = clf.predict(Xte); acc = accuracy_score(Yte, pred)
    _, _, f1, _ = precision_recall_fscore_support(Yte, pred, average="binary", zero_division=0)
    path = os.path.join(MODELS, f"{d}_threat_nn.pkl")
    joblib.dump({"model": clf, "features": NAMES, "hive": meta["hive"]}, path)
    moat[d] = {"hive": meta["hive"], "episodes": len(X), "test_acc": round(acc, 3),
               "f1": round(f1, 3), "model": os.path.basename(path)}
    print(f"  {meta['hive']:<16}{len(X):>9,}{acc:>9.3f}{f1:>7.2f}{os.path.basename(path):>20}")
print("  " + "-" * 62)
json.dump({"hives": len(moat), "models": moat}, open(os.path.join(OUT, "moat_models.json"), "w"), indent=2)
print(f"  {len(moat)} per-hive models saved → models/   ·  moat_models.json")
print(f"  THE MOAT: {len(moat)} distinct governed-behaviour datasets → {len(moat)} sovereign models nobody else has.\n")
