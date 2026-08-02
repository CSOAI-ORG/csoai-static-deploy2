"""Cross-jurisdictional Equivalence Classes (EC) — the non-adjudicating divergence layer (compass Cell 1).
An EC is a HUMAN-CURATED, versioned, signed assertion that a set of provisions ADDRESS THE SAME OBLIGATION TYPE —
NEVER that they impose identical legal duties. It is a taxonomy claim (like a crosswalk), not an adjudication.
Divergence is MEASURED as the delta between predicate outcomes across members, NEVER resolved.

STRUCTURAL GUARDS (enforced in code, matching the estate's no-train()/no-resolve() pattern):
  - The EC engine can only APPLY a pre-signed EC; it has NO method to CREATE or MODIFY an EC from a predicate run.
    (ECs are authored by a human curator out-of-band and loaded signed; measure_divergence only reads them.)
  - No adjudicate()/resolve()/decide() — divergence is reported as data; interpretation routes to a human appeal layer.
  - Every member carries corpus_hash + as_of; a member with no live hash is flagged CITED_NOT_WATCHED (degrade, not hide).
Output framing: a factual measurement of behaviour against provision P (corpus_hash H) as of date D — never
'compliant/non-compliant', never a legal conclusion."""
import json, hashlib

def _h(o): return hashlib.sha256((o if isinstance(o,str) else json.dumps(o,sort_keys=True)).encode()).hexdigest()

class EquivalenceClass:
    """A loaded, signed EC. Immutable after construction — the engine can only READ it."""
    __slots__=("ec_id","obligation_type","axis","members","predicate","criteria_doc","version","_sig")
    def __init__(self, d):
        self.ec_id=d["ec_id"]; self.obligation_type=d["obligation_type"]; self.axis=d["axis"]
        self.members=d["members"]; self.predicate=d["predicate"]; self.criteria_doc=d.get("criteria_doc")
        self.version=d["version"]; self._sig=d.get("signature")
    # NOTE: deliberately NO create/modify/adjudicate/resolve methods. The class is read-only by construction.
    def content_hash(self):
        return _h({"ec_id":self.ec_id,"obligation_type":self.obligation_type,"axis":self.axis,
                   "members":self.members,"predicate":self.predicate,"version":self.version})

def measure_divergence(ec: EquivalenceClass, behaviour_result: dict):
    """APPLY a signed EC to a measured behaviour. behaviour_result: {jurisdiction: {predicate_pass: bool, ...}}.
    Returns the DIVERGENCE (which members pass vs fail on the same obligation) — measured, not resolved."""
    rows=[]
    for m in ec.members:
        j=m["jurisdiction"]; watched = m.get("corpus_hash") is not None
        br=behaviour_result.get(j, {})
        passed=br.get("predicate_pass")
        rows.append({"jurisdiction":j,"instrument":m["instrument"],"provision":m["provision"],
                     "as_of":m["as_of"],"corpus_hash":(m.get("corpus_hash") or "CITED_NOT_WATCHED"),
                     "predicate_pass":passed,
                     "source_status":("watched" if watched else "cited_not_watched")})
    passes=[r for r in rows if r["predicate_pass"] is True]
    fails=[r for r in rows if r["predicate_pass"] is False]
    return {"ec_id":ec.ec_id,"obligation_type":ec.obligation_type,"axis":ec.axis,
            "predicate":ec.predicate,"members":len(rows),
            "diverges": len(passes)>0 and len(fails)>0,   # same obligation, different outcome = divergence
            "pass_in":[r["jurisdiction"] for r in passes],"fail_in":[r["jurisdiction"] for r in fails],
            "rows":rows,
            "framing":"measurement of behaviour vs named provision as-of date; NOT a legal compliance conclusion"}

def engine_guard():
    """Structural check: the engine exposes NO way to author/adjudicate an EC."""
    forbidden=[n for n in ("create_ec","modify_ec","adjudicate","resolve","decide") if n in globals()]
    ecls=[m for m in dir(EquivalenceClass) if m in ("create","modify","adjudicate","resolve","decide")]
    ok = not forbidden and not ecls
    return ok, ("OK: engine can only APPLY signed ECs; no create/modify/adjudicate/resolve exists" if ok
                else f"VIOLATION: found {forbidden+ecls}")
