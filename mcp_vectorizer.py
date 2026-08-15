#!/usr/bin/env python3
"""
mcp_vectorizer.py — Phase 3 Lane 2, Worker 3: Text vectorization pipeline.

Reads the canonical MCP registry, generates TF-IDF embeddings for each
entry (name + description + category), and writes a portable embeddings
file that future ML pipelines can load.

Why TF-IDF and not transformers?
- Deterministic (Law 1: no LLM-as-judge)
- Portable (numpy, no model weights bundled)
- Fast (sub-second for 300 entries)
- Verifiable (every dimension is a named term)

Output: ~/clawd/csoai-static-deploy2/mcp_embeddings.json
        ~/clawd/csoai-static-deploy2/mcp_vocabulary.json
"""
import json
import math
import re
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.home() / "clawd"
SOURCE = ROOT / "csoai-org-v2" / "mcp_registry.json"
FALLBACK = ROOT / "councilof-ai" / "client" / "data" / "mcpRegistry.json"
OUTPUT = ROOT / "csoai-static-deploy2" / "mcp_embeddings.json"
VOCAB = ROOT / "csoai-static-deploy2" / "mcp_vocabulary.json"

STOP_WORDS = set(
    "the a an and or but if for to of in on at by from with about as is are was were be been being have has had do does did this that these those it its their there then than so not no can could should would will shall may might must say said says also just only very very too more most some any each".split()
)


def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r"[a-z][a-z0-9_-]{1,}", text)
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 2]


def load_entries() -> list[dict]:
    for path in (SOURCE, FALLBACK):
        if path.exists():
            try:
                data = json.loads(path.read_text())
            except json.JSONDecodeError:
                continue
            entries: list[dict] = []
            for key in ("sites", "servers", "mcps", "packs"):
                items = data.get(key)
                if isinstance(items, list):
                    for e in items:
                        if isinstance(e, dict):
                            entries.append({
                                "id": e.get("slug", e.get("domain", e.get("id", e.get("name", "unknown")))),
                                "name": e.get("name", e.get("domain", "")),
                                "description": e.get("description", e.get("purpose", "")),
                                "category": e.get("category", e.get("layer", "")),
                            })
            if entries:
                return entries
    return []


def build_vocabulary(entries: list[dict]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for e in entries:
        tokens = tokenize(" ".join([e["name"], e["description"], e["category"]]))
        counter.update(tokens)
    terms = sorted(counter.keys())
    return {term: i for i, term in enumerate(terms)}


def compute_tfidf(entries: list[dict], vocab: dict[str, int]) -> list[dict]:
    n_docs = len(entries)
    doc_freq: Counter[int] = Counter()
    raw = []
    for e in entries:
        tokens = tokenize(" ".join([e["name"], e["description"], e["category"]]))
        counts = Counter(vocab[t] for t in tokens if t in vocab)
        doc_freq.update(counts.keys())
        raw.append({"id": e["id"], "counts": dict(counts)})

    idf = {i: math.log(1 + n_docs / (1 + df_i)) for i, df_i in doc_freq.items()}
    out = []
    for r in raw:
        total = sum(r["counts"].values()) or 1
        vec = {i: (c / total) * idf.get(i, 0.0) for i, c in r["counts"].items()}
        out.append({
            "id": r["id"],
            "vector": vec,
            "norm": math.sqrt(sum(v * v for v in vec.values())),
        })
    return out


def main() -> None:
    print("=== mcp_vectorizer.py: Phase 3 Lane 2 Worker 3 ===")
    entries = load_entries()
    print(f"  Loaded {len(entries)} entries")
    if not entries:
        print("  ! No entries to vectorize")
        return

    vocab = build_vocabulary(entries)
    print(f"  Vocabulary: {len(vocab)} terms")

    vectors = compute_tfidf(entries, vocab)
    print(f"  Computed {len(vectors)} TF-IDF vectors")

    average_norm = sum(v["norm"] for v in vectors) / max(1, len(vectors))
    nonzero_count = sum(1 for v in vectors if v["vector"])
    print(f"  Avg L2 norm: {average_norm:.4f}")
    print(f"  Non-zero vectors: {nonzero_count}/{len(vectors)}")

    payload = {
        "schema": "mcp-tfidf-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "tfidf",
        "n_documents": len(entries),
        "vocab_size": len(vocab),
        "average_norm": round(average_norm, 4),
        "vectors": vectors,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2))
    print(f"  Wrote: {OUTPUT}")

    vocab_payload = {
        "schema": "mcp-vocab-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "size": len(vocab),
        "term_to_index": vocab,
        "sample_terms": list(vocab.keys())[:20],
    }
    VOCAB.write_text(json.dumps(vocab_payload, indent=2))
    print(f"  Wrote: {VOCAB}")


if __name__ == "__main__":
    main()
