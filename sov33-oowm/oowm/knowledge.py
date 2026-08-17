"""OOWM knowledge graph — local-only TF-IDF index over all sovereign knowledge.

Estate-mine extension (2026-08-17, JEEVES): the index is now persistent.
`save(path)` writes the mined corpus to JSON so the MCP server boots from the
estate mine, not the 17-doc seed. `load(path)` restores it. Sources use the
mine's verified surface names (honest_mine, estate_mine, sovos_package,
llm_json, sovereign_os) so every query result traces to a mined artifact.
"""
import os, re, json, hashlib, math
from pathlib import Path
from collections import Counter, defaultdict

class OOWMIndex:
    def __init__(self):
        self.docs = []  # (id, path, source, text, length)
        self.df = Counter()  # doc frequency per term
        self.tf = []  # term frequency per doc
        self.built_at = None
    
    def add_doc(self, path, source, text):
        doc_id = hashlib.md5(path.encode()).hexdigest()[:12]
        tokens = self._tokenize(text)
        self.docs.append({"id": doc_id, "path": path, "source": source, "text": text, "tokens": tokens})
        seen = set()
        for t in tokens:
            if t not in seen:
                self.df[t] += 1
                seen.add(t)
        return doc_id
    
    def _tokenize(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s_-]', ' ', text)
        return [t for t in text.split() if len(t) > 2 and len(t) < 25]
    
    def build_tfidf(self):
        N = len(self.docs)
        self.tf = []
        for d in self.docs:
            tf = Counter(d["tokens"])
            vec = {}
            for t, c in tf.items():
                if self.df[t] > 0:
                    vec[t] = (1 + math.log(c)) * math.log(N / self.df[t])
            self.tf.append(vec)
        self.built_at = "2026-07-13"
    
    def query(self, q, brain="auto", k=5):
        q_tokens = self._tokenize(q)
        if not q_tokens: return []
        q_vec = {}
        for t in q_tokens:
            if t in self.df and self.df[t] > 0:
                q_vec[t] = 1 + math.log(q_tokens.count(t))
        scores = []
        for i, doc in enumerate(self.docs):
            s = 0
            for t, qv in q_vec.items():
                if t in self.tf[i]:
                    s += qv * self.tf[i][t]
            if s > 0:
                scores.append((s, i))
        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:k]:
            d = self.docs[idx]
            snippet = d["text"][:300].replace("\n", " ")
            results.append({
                "id": d["id"], "path": d["path"], "source": d["source"],
                "score": round(score, 3), "snippet": snippet
            })
        return results
    
    def stats(self):
        return {
            "docs": len(self.docs),
            "unique_terms": len(self.df),
            "total_tokens": sum(len(d["tokens"]) for d in self.docs),
            "built_at": self.built_at
        }

    # ---- estate-mine persistence (added 2026-08-17) ----
    def to_dict(self):
        """Serialize the index (text only; tokens/tf rebuilt on load)."""
        return {
            "schema": "oowm-knowledge-index/v2",
            "built_at": self.built_at,
            "docs": [{"path": d["path"], "source": d["source"], "text": d["text"]} for d in self.docs],
        }

    def save(self, path):
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path):
        """Restore an index saved with save(); rebuilds TF-IDF from text."""
        data = json.loads(Path(path).read_text())
        ix = cls()
        for d in data.get("docs", []):
            ix.add_doc(d["path"], d.get("source", "mine"), d.get("text", ""))
        ix.build_tfidf()
        ix.built_at = data.get("built_at", ix.built_at)
        return ix

    def add_many(self, items, cap=2000):
        """Bulk-add (path, source, text) triples with a hard cap (memory-safe)."""
        added = 0
        for path, source, text in items:
            if added >= cap:
                break
            self.add_doc(path, source, text)
            added += 1
        return added
