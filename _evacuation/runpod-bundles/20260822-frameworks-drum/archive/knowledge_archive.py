#!/usr/bin/env python3
"""Knowledge archive — append-only, content-addressed, lineage-tracked (Stage 1, moves 31-40).

The MAPE-K stage-5 residue store ("copy-and-improve"): every candidate, its provenance,
evaluation result, and lineage go here. Append-only: entries supersede, never delete.
Entries are sha256 content-addressed; signatures are recorded honestly (signed:false until
the estate Ed25519 rail is wired — no fake signing).

Stdlib-only. Run: python3 archive/knowledge_archive.py --selftest
"""
import hashlib
import json
import os
import sys

ARCHIVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store")
INDEX = os.path.join(ARCHIVE_DIR, "index.jsonl")


def content_id(entry):
    """sha256 over the canonical-minimal payload (content_id recomputable by anyone)."""
    payload = {k: entry[k] for k in ("kind", "name", "payload") if k in entry}
    canon = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def append(kind, name, payload, parent=None, outcome=None, signed=False, sig=None):
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
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
    entry["content_id"] = content_id(entry)
    with open(INDEX, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry["content_id"]


def lineage(content_id):
    """Walk parent chain from an entry id. Returns list of entries (oldest -> newest)."""
    entries = {}
    if os.path.exists(INDEX):
        for line in open(INDEX, encoding="utf-8"):
            e = json.loads(line)
            entries[e["content_id"]] = e
    out = []
    cur = entries.get(content_id)
    while cur:
        out.insert(0, cur)
        cur = entries.get(cur.get("parent"))
    return out


def count():
    if not os.path.exists(INDEX):
        return 0
    return sum(1 for _ in open(INDEX, encoding="utf-8"))


def selftest():
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    a = append("finding", "candidate-A", {"axis": "gov", "score": 0.81})
    b = append("finding", "candidate-B", {"axis": "gov", "score": 0.83}, parent=a, outcome="promoted")
    assert count() >= 2
    lin = lineage(b)
    assert [e["name"] for e in lin] == ["candidate-A", "candidate-B"], lin
    # append-only: nothing deleted
    assert count() >= 2
    # honest signing: signed flag must be False when no key is wired
    assert all(not e["signed"] for e in lin), "no fake signing"
    print(f"selftest: knowledge archive PASS ({count()} entries, lineage {len(lin)})")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
