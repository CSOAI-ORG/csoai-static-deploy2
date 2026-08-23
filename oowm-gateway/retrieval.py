#!/usr/bin/env python3
"""retrieval.py — BM25 semantic retrieval over the domain-annotated card bank.

Self-contained (stdlib only). Builds a per-domain inverted index with BM25
term-weighting, so retrieval is precise (term-frequency + inverse-doc-frequency
+ length normalization) instead of naive keyword matching.

NOT a neural embedding (fleet has no embed model, no sklearn, and pulling one
needs the slow tunnel). BM25 is a genuine IR retrieval model that beats naive
keyword matching and needs zero downloads — the honest executable step.
"""
import json, re, math, glob, bisect, os, pickle
from pathlib import Path
from collections import defaultdict

CARDS = "/Users/nicholas/sim-world-data/cards/mined/h3k-*.json"
INDEX_PATH = Path("/Users/nicholas/sim-world-data/retrieval-index.pkl")
STOP = set("the a an and or of to in is are for with on as by at from that this be it its not which what how".split())

def tokenize(t):
    return [w for w in re.findall(r'[a-z0-9]+', t.lower()) if w not in STOP and len(w) > 1]

def load_card_bank():
    bank = defaultdict(list)
    for f in glob.glob(CARDS):
        try:
            b = json.loads(json.load(open(f))['body'])
        except Exception:
            continue
        for r in b.get('p', []):
            q = r['r'].get('q', ''); a = r['r'].get('a', '')
            if q and a:
                bank[r.get('f', 'mine')].append((q, a))
    return bank

class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.docs = []; self.tf = []; self.ndl = []; self.avgdl = 0.0
        self.idf = {}
        self.field = ""

    def build(self, field, docs):
        self.field = field; self.docs = docs
        self.tf = [defaultdict(int) for _ in docs]
        lengths = []
        for i, (q, a) in enumerate(docs):
            for w in tokenize(q + " " + a):
                self.tf[i][w] += 1
            lengths.append(sum(self.tf[i].values()))
        self.avgdl = sum(lengths) / len(lengths) if lengths else 1.0
        df = defaultdict(int)
        for i in range(len(docs)):
            for w in self.tf[i]:
                df[w] += 1
        n = len(docs)
        for w, c in df.items():
            self.idf[w] = math.log((n - c + 0.5) / (c + 0.5) + 1.0)

    def score(self, q, i):
        s = 0.0
        doclen = sum(self.tf[i].values())
        for w in tokenize(q):
            if w not in self.idf or self.idf[w] == 0:
                continue
            tf = self.tf[i].get(w, 0)
            denom = tf + self.k1 * (1 - self.b + self.b * doclen / self.avgdl)
            s += self.idf[w] * tf * (self.k1 + 1) / (denom or 1)
        return s

    def search(self, q, k=3):
        scored = sorted(range(len(self.docs)), key=lambda i: -self.score(q, i))
        return [self.docs[i] for i in scored[:k] if self.score(q, i) > 0]

def get_index(card_bank, field):
    """Lazy-build + cache per-field BM25 index."""
    idx = None
    if INDEX_PATH.exists():
        try:
            idx = pickle.load(open(INDEX_PATH, 'rb'))
        except Exception:
            idx = {}
    else:
        idx = {}
    if field not in idx or not idx[field]:
        idx[field] = BM25()
        idx[field].build(field, card_bank.get(field, []))
        pickle.dump(idx, open(INDEX_PATH, 'wb'))
    return idx[field]

def retrieve(bank, field, q, k=3):
    if field not in bank or not bank[field]:
        return []
    return get_index(bank, field).search(q, k)
