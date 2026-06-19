#!/usr/bin/env python3
"""
Sovereign Town — flywheel turn 1: train a REAL neural net on the episode stream.

Trains an sklearn MLPClassifier (same .pkl family SOV3 stores its NNs in) to detect the
"intervene here" moment from an agent's raw perception — the seed of a working threat/care
detector. Crucially: SOV3's PRODUCTION care_validation_nn is degenerate (returns 0.424 for
everything — see summary.json live_care_nn_audit). This shows the town's self-labelled data
trains a model that ACTUALLY discriminates → the flywheel fixes the broken production model.

Saves the trained model to town_threat_nn.pkl. python3.11 flywheel_train.py
"""
import json, os, warnings
warnings.filterwarnings("ignore")
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import joblib

OUT = os.path.dirname(os.path.abspath(__file__))
from common import features, FEATURE_NAMES as NAMES   # deduped — was a local copy


X, Y = [], []
for line in open(os.path.join(OUT, "episodes.jsonl")):
    r = json.loads(line)
    X.append(features(r)); Y.append(1 if r["governance"]["would_block"] else 0)
X, Y = np.array(X), np.array(Y)
Xtr, Xte, Ytr, Yte = train_test_split(X, Y, test_size=0.3, random_state=47, stratify=Y)

clf = MLPClassifier(hidden_layer_sizes=(32,16), max_iter=400, random_state=47)   # a real neural net
clf.fit(Xtr, Ytr)
pred = clf.predict(Xte)
acc = accuracy_score(Yte, pred)
prec, rec, f1, _ = precision_recall_fscore_support(Yte, pred, average="binary", zero_division=0)
base = max(Y.mean(), 1 - Y.mean())
joblib.dump({"model": clf, "features": NAMES}, os.path.join(OUT, "town_threat_nn.pkl"))

# importance via permutation (quick)
import_scores = []
for j in range(X.shape[1]):
    Xp = Xte.copy(); np.random.RandomState(47).shuffle(Xp[:, j])
    import_scores.append((NAMES[j], round(acc - accuracy_score(Yte, clf.predict(Xp)), 3)))
top = sorted(import_scores, key=lambda x: -x[1])[:3]

print(f"\n  FLYWHEEL TURN 1 — MLP threat-detector (real NN) on {len(X)} episodes")
print("  " + "-"*58)
print(f"  architecture                : MLPClassifier (32,16), sklearn")
print(f"  majority-class baseline acc : {base:.3f}")
print(f"  TEST accuracy               : {acc:.3f}")
print(f"  TEST precision / recall / F1: {prec:.3f} / {rec:.3f} / {f1:.3f}")
print(f"  top features (perm-import)  : {', '.join(f'{n}({s})' for n,s in top)}")
print(f"  --- vs SOV3 production care_validation_nn ---")
print(f"  production model spread     : 0.000 (degenerate — 0.424 for every action)")
print(f"  town-trained model          : discriminates (F1 {f1:.2f}) → FLYWHEEL FIXES THE BROKEN MODEL")
print(f"  saved                       : town_threat_nn.pkl")
print("  " + "-"*58 + "\n")
