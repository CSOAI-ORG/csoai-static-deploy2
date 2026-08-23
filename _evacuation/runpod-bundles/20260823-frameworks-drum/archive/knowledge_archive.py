#!/usr/bin/env python3
"""Knowledge archive — append-only, content-addressed, lineage-tracked (Stage 1, moves 31-40).

The MAPE-K stage-5 residue store ("copy-and-improve"): every candidate, its provenance,
evaluation result, and lineage go here. Append-only: entries supersede, never delete.
Entries are sha256 content-addressed; signatures are recorded honestly (signed:false until
the estate Ed25519 rail is wired — no fake signing).

Append is IDEMPOTENT: identical (kind, name, payload) maps to the same content_id, and a
re-append is a no-op (returns the existing id). This closes the regrowth class where test
harnesses (selftest / property-test) pollute the production store with duplicate entries
(ledger #21). Tests isolate themselves by pointing KNOWLEDGE_ARCHIVE_INDEX at a temp file.

Stdlib-only. Run: python3 archive/knowledge_archive.py --selftest
"""
import hashlib
import json
import os
import sys

ARCHIVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store")
INDEX = os.path.join(ARCHIVE_DIR, "index.jsonl")

# Isolation override: tests set this to a temp file so they never touch production.
_ENV_INDEX = "KNOWLEDGE_ARCHIVE_INDEX"


def get_index():
    return os.environ.get(_ENV_INDEX) or INDEX


def content_id(entry):
    """sha256 over the canonical-minimal payload (content_id recomputable by anyone)."""
    payload = {k: entry[k] for k in ("kind", "name", "payload") if k in entry}
    canon = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _existing_ids(index_path):
    ids = set()
    if os.path.exists(index_path):
        for line in open(index_path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                ids.add(json.loads(line).get("content_id"))
            except Exception:
                continue
    return ids


def _last_chain_hash(index_path):
    """Return the chain_hash of the last entry (or None if none yet)."""
    last = None
    if os.path.exists(index_path):
        for line in open(index_path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                last = json.loads(line).get("chain_hash")
            except Exception:
                continue
    return last


def _chain_hash(cid, prev_hash):
    """sha256 over (content_id || prev_chain_hash) — a tamper-evident hash-chain link."""
    canon = json.dumps([cid, prev_hash], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def append(kind, name, payload, parent=None, outcome=None, signed=False, sig=None):
    index_path = get_index()
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    entry = {
        "kind": kind,
        "name": name,
        "payload": payload,
        "parent": parent,
        "outcome": outcome,
        "signed": signed,
        "signature": sig,
        "ts": __import__("datetime").date.today().isoformat(),
    }
    cid = content_id(entry)
    entry["content_id"] = cid
    # hash-chain: each entry commits to the previous entry's chain_hash (tamper-evident;
    # ledger #29 — the local 'chained' foundation; the signed sigil chain stays a [GATE]).
    prev_hash = _last_chain_hash(index_path)
    entry["prev_hash"] = prev_hash
    entry["chain_hash"] = _chain_hash(cid, prev_hash)
    # idempotent: content-addressed append is a no-op when the id already exists.
    if cid in _existing_ids(index_path):
        return cid
    with open(index_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return cid


def lineage(content_id_val):
    """Walk parent chain from an entry id. Returns list of entries (oldest -> newest)."""
    entries = {}
    index_path = get_index()
    if os.path.exists(index_path):
        for line in open(index_path, encoding="utf-8"):
            e = json.loads(line)
            entries[e["content_id"]] = e
    out = []
    cur = entries.get(content_id_val)
    while cur:
        out.insert(0, cur)
        cur = entries.get(cur.get("parent"))
    return out


def count():
    index_path = get_index()
    if not os.path.exists(index_path):
        return 0
    return sum(1 for _ in open(index_path, encoding="utf-8"))


def selftest():
    # Isolate the store: the archive's own selftest must never pollute production.
    import tempfile
    os.environ[_ENV_INDEX] = os.path.join(tempfile.mkdtemp(), "index.jsonl")
    a = append("finding", "candidate-A", {"axis": "gov", "score": 0.81})
    b = append("finding", "candidate-B", {"axis": "gov", "score": 0.83}, parent=a, outcome="promoted")
    assert count() == 2, count()
    # idempotency: re-appending identical content must not grow the store
    append("finding", "candidate-A", {"axis": "gov", "score": 0.81})
    assert count() == 2, f"append not idempotent: {count()}"
    lin = lineage(b)
    assert [e["name"] for e in lin] == ["candidate-A", "candidate-B"], lin
    # hash-chain integrity: each entry's chain_hash commits to the previous; tampering breaks it.
    entries = [json.loads(l) for l in open(get_index(), encoding="utf-8") if l.strip()]
    prev = None
    for e in entries:
        assert e["prev_hash"] == prev, f"chain link broken at {e['name']}"
        assert e["chain_hash"] == _chain_hash(e["content_id"], prev), f"chain mismatch at {e['name']}"
        prev = e["chain_hash"]
    # append-only: nothing deleted
    assert count() >= 2
    # honest signing: signed flag must be False when no key is wired
    assert all(not e["signed"] for e in lin), "no fake signing"
    n = count()
    # clean up the isolation override so later callers in the same process see production
    os.environ.pop(_ENV_INDEX, None)
    print(f"selftest: knowledge archive PASS ({n} entries, lineage {len(lin)}, hash-chain verified)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
