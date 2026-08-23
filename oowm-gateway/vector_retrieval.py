#!/usr/bin/env python3
"""vector_retrieval.py — TF-IDF + cosine vector retrieval (stdlib-only).

Numeric vector space retrieval, self-contained (no numpy/sklearn/fleet model).
Builds a TF-IDF vector per card document, encodes a query the same way, and
ranks by cosine similarity. Complements BM25 (BM25 is term-frequency;
TF-IDF-cosine weights by document rarity).

NOTE: true neural embeddings (nomic-embed-text) are present on the pod but
this Ollama build does not serve /api/embed (verified live) — so this is the
honest, working vector retrieval available right now.
"""
import re, math, glob, pickle
from pathlib import Path
from collections import defaultdict

CARDS = "/Users/nicholas/sim-world-data/cards/mined/h3k-*.json"
INDEX_PATH = Path("/Users/nicholas/sim-world-data/vector-index.pkl")
STOP = set("the a an and or of to in is are for with on as by at from that this be it its not which what how".split())

def tokenize(t):
    return [w for w in re.findall(r'[a-z0-9]+', t.lower()) if w not in STOP and len(w) > 1]

def build(field, docs):
    """Build TF-IDF vectors for a field's docs. Returns (vocab, vectors, idf)."""
    vocab = set()
    tfs = []
    for q, a in docs:
        tf = defaultdict(int)
        for w in tokenize(q + " " + a):
            tf[w] += 1
        tfs.append(tf)
        vocab |= set(tf)
    vocab = sorted(vocab)
    N = len(docs)
    idf = {w: math.log((N + 1) / (sum(1 for t in tfs if w in t) + 1)) + 1 for w in vocab}
    def norm(vec):
        n = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / n for x in vec]
    cache = {}
    def vec(tf):
        key = id(tf)
        if key not in cache:
            cache[key] = norm([tf.get(w, 0) * idf[w] for w in vocab])
        return cache[key]
    return vocab, [vec(t) for t in tfs], idf

class VectorIndex:
    def __init__(self, field, docs, max_docs=40000):
        self.field = field
        self.docs = docs[:max_docs]
        self.vocab, self.vecs, self.idf = build(field, self.docs)

    def search(self, q, k=3):
        qtf = defaultdict(int)
        for w in tokenize(q):
            qtf[w] += 1
        n = math.sqrt(sum(v * v for v in qtf.values())) or 1.0
        qv = [qtf.get(w, 0) * self.idf.get(w, 0) / n for w in self.vocab]
        scored = [(i, sum(a * b for a, b in zip(qv, self.vecs[i]))) for i in range(len(self.docs))]
        scored.sort(key=lambda x: -x[1])
        return [self.docs[i] for i, s in scored[:k] if s > 0]

def get_index(bank, field):
    idx = {}
    if INDEX_PATH.exists():
        try:
            idx = pickle.load(open(INDEX_PATH, 'rb'))
        except Exception:
            idx = {}
    if field not in idx or not idx[field]:
        idx[field] = VectorIndex(field, bank.get(field, []))
        try:
            pickle.dump(idx, open(INDEX_PATH, 'wb'))
        except Exception:
            pass
    return idx[field]

def retrieve(bank, field, q, k=3):
    if field not in bank or not bank[field]:
        return []
    return get_index(bank, field).search(q, k)
