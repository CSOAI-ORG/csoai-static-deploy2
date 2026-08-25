#!/usr/bin/env python3
"""COORDINATION_LEDGER.py — append/update the living coordination ledger (dedup-aware, no secrets).
Usage:
  python3 tools/ledger.py add     '{type, target, status, owner, frames}'
  python3 tools/ledger.py set     '{key, status, note}'
  python3 tools/ledger.py list    [type]
Every entry keys on slug(type:target) — updates existing, never duplicates.
Never store a password/key/secret. Owner gates: status=gated_owner, owner=OWNER_nick.
"""
import json, os, sys, re

LEDGER = os.path.join(os.path.dirname(__file__), '..', 'COORDINATION_LEDGER.json')
def slug(type, target):
    s = re.sub(r'[^a-z0-9]+', '-', (str(type)+':'+str(target)).lower()).strip('-')
    return s

def load():
    with open(LEDGER) as f: return json.load(f)
def save(d):
    with open(LEDGER, 'w') as f: json.dump(d, f, indent=2)
def section(d, t):
    return 'accounts' if t=='account' else 'connections' if t=='connection' else 'outreach' if t=='outreach' else 'moves_done'

def add(obj):
    d = load(); t = obj['type']
    # dedup: if a caller supplies a canonical key, use it; else slug type+target.
    key = obj.get('key') or slug(obj['type'], (obj.get('target') or obj.get('name') or ''))
    sec = section(d, t)
    for e in d.get(sec, []):
        if e['key']==key:
            e.update({k:v for k,v in obj.items() if v is not None}); save(d)
            return f"updated {key} in {sec}"
    obj['key']=key; obj.setdefault('status','planned'); obj.setdefault('owner','JEEVES')
    d.setdefault(sec, []).append(obj); save(d)
    return f"added {key} to {sec}"

def set_status(key, status, note):
    d = load()
    for sec in ('accounts','connections','outreach','moves_done'):
        for e in d.get(sec, []):
            if e['key']==key:
                e['status']=status
                if note: e['note']=note
                save(d); return f"set {key} -> {status}"
    return f"{key} not found (add first)"

def main():
    if len(sys.argv)<3: print(__doc__); return
    cmd=sys.argv[1]; payload=json.loads(sys.argv[2])
    if sys.argv[1]=='add': print(add(payload))
    elif sys.argv[1]=='set': print(set_status(payload['key'], payload.get('status'), payload.get('note')))
    elif sys.argv[1]=='list':
        d=load(); t=sys.argv[2] if len(sys.argv)>2 else None
        for sec in ('accounts','connections','outreach','moves_done'):
            if t and t not in (sec, sec[:-1]): continue
            for e in d.get(sec, []):
                print(f"  [{sec[:-1]}] {e['key']} -> {e.get('status')} ({e.get('owner')})")
main()
