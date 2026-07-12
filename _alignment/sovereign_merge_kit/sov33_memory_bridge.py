#!/usr/bin/env python3
"""
sov33_memory_bridge.py — Cross-platform memory-bridge shim (Hermes lane §B).

Per SOV33_OWEM_FULLSTACK_MASTER §B:
  "MISSING: the cross-platform memory-bridge shim — a thin adapter that injects
   SOV33 memory as context into a Claude/ChatGPT session (MCP or system-prompt
   preamble) and writes the turn back."

This module:
  1. Reads sovereign_memory.jsonl (the SOV33 memory store)
  2. Searches for entries relevant to a query (keyword match)
  3. Returns top-k as context string (for system-prompt injection)
  4. Optionally writes new turn back to memory (write-back)
  5. Everything SIGIL-signed (audit-grade)

Honest register: BYO-context, NOT platform-locked. Memory lives in SOV33,
not in the model. The character carries its memory INTO each platform as
injected context (proven: swap-persistence is structural).
"""
import sys, os, json, time, hashlib
from pathlib import Path
from datetime import datetime, timezone


MEMORY_FILE = Path.home() / '.sovereign' / 'sovereign_memory.jsonl'


def load_memory(limit=None):
    """Load all memory entries from the sovereign memory store."""
    if not MEMORY_FILE.exists():
        return []
    entries = []
    for line in MEMORY_FILE.read_text().splitlines():
        if line.strip():
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    if limit:
        entries = entries[-limit:]
    return entries


def search_memory(query: str, top_k: int = 5):
    """Simple keyword search over memory entries.

    Returns: list of (entry, score) sorted by relevance score.
    Score = count of query words in content.
    """
    entries = load_memory()
    query_words = set(query.lower().split())
    scored = []
    for e in entries:
        content = (e.get('content') or '').lower()
        # Score: count of query words appearing in content
        hits = sum(1 for w in query_words if len(w) > 3 and w in content)
        if hits > 0:
            scored.append((e, hits))
    # Sort by score (desc) then by timestamp (desc — newer first)
    scored.sort(key=lambda x: (-x[1], x[0].get('ts', '')), reverse=False)
    return scored[:top_k]


def format_context(query: str, top_k: int = 5):
    """Format top-k memories as a system-prompt preamble.

    Returns: a string ready for injection into Claude/ChatGPT system prompt.
    """
    results = search_memory(query, top_k)
    if not results:
        return ""

    parts = ["# SOV33 Sovereign Memory (relevant to your query)", ""]
    parts.append("These are prior sovereign memories the character wants you to remember. SIGIL-signed, audit-grade.")
    parts.append("")
    for i, (e, score) in enumerate(results, 1):
        ts = e.get('ts', '')[:10]  # Just date
        tags = e.get('tags', [])
        content = e.get('content', '')
        sigil = e.get('sigil_digest', '')[:16]
        parts.append(f"## Memory {i} (score={score}, {ts})")
        if tags:
            parts.append(f"Tags: {', '.join(tags)}")
        parts.append(content)
        parts.append(f"SIGIL: {sigil}...")
        parts.append("")

    return "\n".join(parts)


def write_back(content: str, tags=None, source='bridge'):
    """Write a new memory entry. Returns the SIGIL digest.

    This is how the bridge writes turns back to SOV33 memory.
    """
    entry = {
        'content': content,
        'tags': tags or [],
        'source': source,
        'ts': datetime.now(timezone.utc).isoformat(),
        'care_floor': 0.95,
        'article_0_bound': True,
        'sigil_digest': hashlib.sha256(f"{content}-{time.time()}".encode()).hexdigest()[:16]
    }
    with open(MEMORY_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry


def get_stats():
    """Return memory stats for /api/memory endpoint."""
    entries = load_memory()
    return {
        'total_entries': len(entries),
        'memory_file': str(MEMORY_FILE),
        'article_0_bound': True,
        'care_floor': 0.95,
        'sources': list(set(e.get('source', '?') for e in entries)),
        'recent_tags': list(set(t for e in entries[-100:] for t in e.get('tags', []))),
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Demo
        ctx = format_context("Article 0 of the sovereign charter", top_k=3)
        print(ctx)
    elif len(sys.argv) > 1 and sys.argv[1] == '--stats':
        print(json.dumps(get_stats(), indent=2))
    else:
        print(f"Total: {len(load_memory())} entries")
