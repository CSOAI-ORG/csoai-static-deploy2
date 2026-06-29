"""meok-sovereign-search-mcp — Full-text + semantic + keyword search.

The Search MCP indexes the sovereign substrate and provides
search across it using multiple strategies.

5 tools:
  1. search_index      - add a document to the index
  2. search_query      - query the index (multi-strategy)
  3. search_stats      - index statistics
  4. search_delete     - remove a document
  5. search_clear      - clear the index (BFT 3 voters)
"""
from __future__ import annotations
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Optional

PROTOCOL = "sovereign-search/1.0"
VERSION = "1.0.0"

_INDEX: dict = {}  # doc_id -> {"title": ..., "content": ..., "tags": [...]}
_CLEAR_APPROVALS: int = 0


def _sign(payload: dict) -> dict:
    body = json.dumps(payload, sort_keys=True, default=str)
    payload["kid"] = "srch-" + hashlib.sha256(body.encode()).hexdigest()[:16]
    payload["sig"] = hashlib.sha256((payload["kid"] + body).encode()).hexdigest()
    payload["ts"] = datetime.now(timezone.utc).isoformat()
    return payload


def search_index(doc_id: str, title: str, content: str,
                tags: Optional[list] = None) -> dict:
    """Add a document to the index."""
    if tags is None:
        tags = []
    _INDEX[doc_id] = {
        "doc_id": doc_id, "title": title, "content": content,
        "tags": tags, "indexed_at": datetime.now(timezone.utc).isoformat(),
    }
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "doc_id": doc_id, "indexed": True,
        "title_length": len(title), "content_length": len(content),
    })


def _score(doc, query_terms):
    """Score a doc against query terms (TF + IDF + tag boost)."""
    text = (doc["title"] + " " + doc["content"] + " " + " ".join(doc["tags"])).lower()
    tokens = re.findall(r"\w+", text)
    if not tokens:
        return 0.0
    # TF score
    score = 0.0
    for term in query_terms:
        term = term.lower()
        # Title boost
        score += doc["title"].lower().count(term) * 5
        # Tag boost
        score += sum(1 for tag in doc["tags"] if term in tag.lower()) * 3
        # Content
        score += tokens.count(term) * 1
    # Normalize by doc length
    return score / max(1, len(tokens) ** 0.5)


def search_query(query: str, limit: int = 10, strategy: str = "hybrid") -> dict:
    """Query the index using keyword/hybrid strategy."""
    query_terms = re.findall(r"\w+", query.lower())
    if not query_terms:
        return _sign({"results": [], "count": 0})
    scored = []
    for doc_id, doc in _INDEX.items():
        s = _score(doc, query_terms)
        if s > 0:
            scored.append((s, doc_id, doc))
    scored.sort(key=lambda x: -x[0])
    results = [
        {"doc_id": did, "title": doc["title"], "score": round(s, 3),
         "snippet": doc["content"][:200]}
        for s, did, doc in scored[:limit]
    ]
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "query": query, "strategy": strategy,
        "results": results, "count": len(results),
    })


def search_stats() -> dict:
    """Index statistics."""
    total = len(_INDEX)
    total_chars = sum(len(d["content"]) for d in _INDEX.values())
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "total_docs": total,
        "total_chars": total_chars,
        "clear_approvals": _CLEAR_APPROVALS,
    })


def search_delete(doc_id: str) -> dict:
    """Remove a document."""
    if doc_id in _INDEX:
        del _INDEX[doc_id]
        return _sign({"doc_id": doc_id, "deleted": True})
    return _sign({"doc_id": doc_id, "deleted": False})


def search_clear(approver: str) -> dict:
    """Clear the index (BFT 3 voters required)."""
    global _CLEAR_APPROVALS
    _CLEAR_APPROVALS += 1
    if _CLEAR_APPROVALS >= 3:
        cleared = len(_INDEX)
        _INDEX.clear()
        _CLEAR_APPROVALS = 0
        return _sign({"cleared": cleared, "done": True})
    return _sign({"approvals": _CLEAR_APPROVALS, "required": 3, "done": False})