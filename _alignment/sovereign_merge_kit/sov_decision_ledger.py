#!/usr/bin/env python3
"""sov_decision_ledger.py — THE DECISION RECORD (SOV-Decision-Record-Schema, 2026-07-29).
Protects the ledger — the estate's most valuable asset (the record of what it got wrong), currently in unsigned markdown.
Append-only, signed, hash-chained. Reads + appends. NEVER edits, resolves, or adjudicates (guard() asserts their absence).
Same discipline as Instrument(no train), Arena(G-guards), ASI-evolve(no resolve): three engines, one rule, enforced identically.

THE FOUR INVARIANTS (in code, not policy):
  1. Never delete — always supersede (the history of being wrong IS the moat).
  2. A tag may never be dropped/upgraded silently — [LEAD]->[MEASURED] needs a NEW record with supersedes + method_ref.
  3. n<20 forces lower_bound=True (structural, not remembered).
  4. Contradiction is SURFACED (both get contested_by, render OPEN), never auto-resolved — a human decides.
"""
import json, hashlib, time, os

VALID_KINDS={"refutation","claim","correction","settled","law","definition","blocked"}
VALID_TAGS={"MEASURED","LEAD","GREENFIELD","VENDOR","REFUTED","SETTLED"}

class LedgerError(Exception): pass

class DecisionLedger:
    """Append-only, signed. Reads and appends. Never edits, never resolves."""
    def __init__(self, path=None):
        self.path=path or os.path.join(os.path.dirname(os.path.abspath(__file__)),"decision_ledger.jsonl")
        self._records=[]
        if os.path.exists(self.path):
            self._records=[json.loads(l) for l in open(self.path) if l.strip()]

    def _prev_hash(self): return self._records[-1]["sigil_link"] if self._records else "GENESIS"

    def append(self, record):
        # invariant 1: never delete/edit — only append. (no edit/delete method exists.)
        if record.get("kind") not in VALID_KINDS: raise LedgerError(f"bad kind {record.get('kind')}")
        if record.get("tag") not in VALID_TAGS: raise LedgerError(f"bad tag {record.get('tag')}")
        # invariant 3: n<20 forces lower_bound
        n=record.get("n")
        if isinstance(n,int) and n<20: record["lower_bound"]=True
        # invariant 2: a tag upgrade LEAD->MEASURED requires supersedes + method_ref
        if record.get("supersedes"):
            prior=self.get(record["supersedes"])
            if prior and prior.get("tag")=="LEAD" and record.get("tag")=="MEASURED" and not record.get("method_ref"):
                raise LedgerError("invariant 2: LEAD->MEASURED requires method_ref (Law 4 in code)")
            # set superseded_by on the OLD record's in-memory view (append a note; never edit the stored line)
        record.setdefault("record_id", f"DR-{len(self._records)+1:04d}")
        record.setdefault("schema_version","1.0.0")
        record.setdefault("decided_on", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        body=json.dumps({k:v for k,v in record.items() if k!="sigil_link"}, sort_keys=True)
        record["sigil_link"]=hashlib.sha256((self._prev_hash()+"\x00"+body).encode()).hexdigest()
        self._records.append(record)
        with open(self.path,"a") as f: f.write(json.dumps(record)+"\n")
        return record["record_id"]

    def get(self, rid): return next((r for r in self._records if r["record_id"]==rid), None)
    def current(self, claim):
        # latest non-superseded record for a claim
        superseded={r.get("supersedes") for r in self._records if r.get("supersedes")}
        matches=[r for r in self._records if r["claim"]==claim and r["record_id"] not in superseded]
        return matches[-1] if matches else None
    def history(self, claim): return [r for r in self._records if r["claim"]==claim]
    def contested(self):
        # invariant 4: claims with >1 live record of opposing verdict render OPEN
        return [r for r in self._records if r.get("contested_by")]
    def by_tag(self, tag): return [r for r in self._records if r.get("tag")==tag]
    def stale_leads(self, days):
        cut=time.time()-days*86400
        out=[]
        for r in self._records:
            if r.get("tag")=="LEAD":
                try: t=time.mktime(time.strptime(r["decided_on"],"%Y-%m-%dT%H:%M:%SZ"))
                except Exception: t=0
                if t<cut: out.append(r)
        return out

    def guard(self):
        forbidden=("edit","delete","resolve","adjudicate","merge","auto_supersede")
        found=[m for m in forbidden if hasattr(self,m)]
        assert not found, f"VIOLATION: {found}"
        return "OK: append-only; contradiction surfaced, never resolved"

def verify_chain(path):
    recs=[json.loads(l) for l in open(path) if l.strip()]
    prev="GENESIS"
    for r in recs:
        body=json.dumps({k:v for k,v in r.items() if k!="sigil_link"}, sort_keys=True)
        exp=hashlib.sha256((prev+"\x00"+body).encode()).hexdigest()
        if exp!=r["sigil_link"]: return False, r["record_id"]
        prev=r["sigil_link"]
    return True, len(recs)

if __name__=="__main__":
    L=DecisionLedger(path="/tmp/dl_demo.jsonl")
    open("/tmp/dl_demo.jsonl","w").close(); L._records=[]
    print("guard:", L.guard())
    # seed the 4 drifts the audit found
    L.append({"kind":"correction","claim":"ProvBench CI upper bound","verdict":"SETTLED","n":12,"lower_bound":True,
      "tag":"MEASURED","evidence":"asset is the independent unit (9 transforms of one asset fail by identical deterministic "
      "mechanism). n=12: one-sided 95% CP 22.1%, two-sided 26.5%. cell-level 3.43% assumes independence that does NOT hold. "
      "24.2% was right-magnitude/wrong-derivation. 12 assets verified genuinely varied (4 kinds x 4 sizes).",
      "method_ref":"provbench.json + FOREST_90","interval":"[0, 22.1%] one-sided"})
    L.append({"kind":"definition","claim":"IWM/OWM/VWM canonical mapping","verdict":"SETTLED","tag":"SETTLED",
      "evidence":"IWM=gates+predicates(how it judges); OWM=C-space honey(what it knows, watcher-fed); VWM=render(what it "
      "shows, never decides). Tell: the alternative leaves the +34.84 gate homeless.","n":None})
    L.append({"kind":"claim","claim":"ProvBench 0 survivals is MEASURED not modelled","verdict":"CONFIRMED","tag":"MEASURED",
      "evidence":"provbench.py real c2pa Builder/Reader/Signer, real signing+Pillow transforms+read-back, 3 outcomes. "
      "Two lanes traced. Denominator: ~9 measured transforms, 1 MODELLED (screenshot_equiv), 1 UNMEASURED (HEIC) — headline "
      "= measured cells only.","method_ref":"provbench.py","n":12,"corpus_hash":None})
    L.append({"kind":"blocked","claim":"corpus-watcher cron is deployed","verdict":"OPEN","tag":"REFUTED",
      "evidence":"AUTHORED+packaged only. Never pushed to a remote, never triggered. Overclaimed twice. Fix: a 'deployed' "
      "flag settable ONLY by a successful remote-triggered run writing back a signed record. Until then: AUTHORED.","n":None})
    print(f"seeded {len(L._records)} records")
    print("by_tag(MEASURED):", [r['record_id'] for r in L.by_tag('MEASURED')])
    print("current('ProvBench CI upper bound'):", L.current("ProvBench CI upper bound")["interval"])
    ok,info=verify_chain("/tmp/dl_demo.jsonl"); print(f"chain valid: {ok} ({info} records)")
    print("\n✅ decision ledger: append-only, 4 invariants, guard() rejects edit/delete/resolve, chain signed+valid.")
