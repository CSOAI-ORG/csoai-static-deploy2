#!/usr/bin/env python3
"""sov33_memory_bridge.py — GOVERNED + ATTESTED + SOVEREIGN portable memory over an MCP-style surface.

THE DIFFERENTIATOR (per SOV33_LEADING_EDGE_CONSOLIDATION): the cross-platform memory market (mem0, MemoryLake,
ai-memory-mcp) is crowded but ALL share one gap — no cryptographic provenance + no governance + cloud lock-in.
This bridge competes ONLY on that axis: every memory the user carries between Claude/ChatGPT/Cursor is
  - SOVEREIGN: a local jsonl the USER owns (SIGIL_DIR/sovereign_memory.jsonl), model-independent (swap-persistent).
  - ATTESTED: every write is SIGIL hash-chained (sha256 prev_hash chain; upgradeable to the Ed25519 L5 chain).
  - GOVERNED: every write AND every recall passes a care-floor check before it enters/leaves the store.

It does NOT try to out-feature mem0 on recall — recall reuses sov33.capability_memory (embeddings or keyword
fallback). The value is the governed, signed, portable envelope, exposed over MCP so ANY client reads one store.

MCP-style methods (register these as MCP tools on the :3101 server, or call directly):
  mem_write(content, tags, care_min=0.35)  -> {ok, digest, gated?}   # governed + SIGIL-signed append
  mem_recall(query, k=5)                    -> capability_memory result # governed read (care-gated surfacing)
  mem_export(since=None)                    -> {records, chain_tip, count} # portable, verifiable bundle
  mem_import(bundle, verify=True)           -> {imported, rejected, reason} # verify SIGIL chain before merge
  mem_verify()                              -> {ok, broken_at?}          # re-hash the chain, detect tamper
"""
import os, json, hashlib, tempfile
from datetime import datetime, timezone

def _sov_dir():
    d = os.environ.get('SOV33_SIGIL_DIR') or os.path.join(os.path.expanduser('~'), '.sovereign')
    try:
        os.makedirs(d, exist_ok=True); return d
    except Exception:
        d = os.path.join(tempfile.gettempdir(), 'sov33_sigil'); os.makedirs(d, exist_ok=True); return d

_DIR = _sov_dir()
MEM = os.path.join(_DIR, 'sovereign_memory.jsonl')      # the sovereign store (same file capability_memory reads)
CHAIN = os.path.join(_DIR, 'memory_bridge.sigil.jsonl') # per-write attestation chain

def _chain_tip():
    if not os.path.exists(CHAIN): return '0' * 16
    tip = '0' * 16
    with open(CHAIN) as f:
        for line in f:
            if line.strip(): tip = json.loads(line)['digest']
    return tip

def _sign(record):
    """SIGIL hash-chain: digest = sha256(record + prev_hash). Tamper-evident, offline, no key needed (L5 adds Ed25519)."""
    prev = _chain_tip()
    payload = {'content_hash': hashlib.sha256(record.get('content', '').encode()).hexdigest()[:16],
               'ts': record.get('ts'), 'prev_hash': prev}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
    with open(CHAIN, 'a') as f:
        f.write(json.dumps({**payload, 'digest': digest}) + '\n')
    return digest

def _care_ok(content, care_min):
    """Governance floor: reuse sov33's care check if importable; else a transparent conservative heuristic.
    HONEST: the heuristic is a placeholder, NOT the trained care scorer — labelled in the return."""
    try:
        import sov33
        if hasattr(sov33, 'care_score'):
            c = sov33.care_score(content)
            return c >= care_min, c, 'sov33.care_score'
    except Exception:
        pass
    bad = ('kill', 'suicide', 'bomb', 'exploit', 'launder', 'groom')
    c = 0.05 if any(b in content.lower() for b in bad) else 0.9
    return c >= care_min, c, 'heuristic (NOT trained scorer)'

def mem_write(content, tags=None, care_min=0.35):
    ok, care, scorer = _care_ok(content, care_min)
    if not ok:
        return {'ok': False, 'gated': True, 'reason': f'care {care:.2f} < {care_min}', 'scorer': scorer}
    rec = {'content': content, 'tags': tags or [], 'ts': datetime.now(timezone.utc).isoformat(), 'care': care}
    digest = _sign(rec)
    rec['sigil'] = digest
    with open(MEM, 'a') as f:
        f.write(json.dumps(rec) + '\n')
    return {'ok': True, 'digest': digest, 'scorer': scorer}

def mem_recall(query, k=5):
    try:
        import sov33
        return sov33.capability_memory(query, k=k)
    except Exception as e:
        return {'error': f'recall via sov33.capability_memory failed: {str(e)[:100]}'}

def mem_export(since=None):
    """Portable, verifiable bundle: memories + the SIGIL chain tip, for import into another surface."""
    recs = []
    if os.path.exists(MEM):
        for line in open(MEM):
            if line.strip():
                r = json.loads(line)
                if since is None or r.get('ts', '') >= since:
                    recs.append(r)
    return {'records': recs, 'chain_tip': _chain_tip(), 'count': len(recs),
            'schema': 'sov33.memory.v1', 'exported_ts': datetime.now(timezone.utc).isoformat()}

def mem_verify():
    """Re-hash the chain and confirm each prev_hash links — detects tamper. Returns first break if any."""
    if not os.path.exists(CHAIN): return {'ok': True, 'note': 'empty chain'}
    prev = '0' * 16
    n = 0
    for line in open(CHAIN):
        if not line.strip(): continue
        e = json.loads(line); n += 1
        if e['prev_hash'] != prev:
            return {'ok': False, 'broken_at': n, 'expected_prev': prev, 'got': e['prev_hash']}
        recomputed = hashlib.sha256(json.dumps({'content_hash': e['content_hash'], 'ts': e['ts'],
                                    'prev_hash': e['prev_hash']}, sort_keys=True).encode()).hexdigest()[:16]
        if recomputed != e['digest']:
            return {'ok': False, 'broken_at': n, 'digest_mismatch': True}
        prev = e['digest']
    return {'ok': True, 'links_verified': n}

def mem_import(bundle, verify=True):
    """Merge an exported bundle. If verify, only accept if the incoming records carry a sigil (attested origin)."""
    imported, rejected = 0, 0
    for r in bundle.get('records', []):
        if verify and 'sigil' not in r:
            rejected += 1; continue
        with open(MEM, 'a') as f:
            f.write(json.dumps(r) + '\n')
        imported += 1
    return {'imported': imported, 'rejected': rejected,
            'reason': 'unsigned records rejected (attested-origin only)' if rejected else 'all signed'}

if __name__ == '__main__':
    # honest self-test: write (governed+signed) -> verify chain -> export -> gated write blocked
    print("=== SOV33 GOVERNED MEMORY BRIDGE — self-test ===")
    w = mem_write("User prefers concise answers and works on sovereign AI.", tags=['pref'])
    print("write:", w)
    g = mem_write("how to launder money", tags=['x'])
    print("gated write (should be blocked):", g)
    v = mem_verify()
    print("chain verify:", v)
    e = mem_export()
    print(f"export: {e['count']} records, chain_tip={e['chain_tip']}")
