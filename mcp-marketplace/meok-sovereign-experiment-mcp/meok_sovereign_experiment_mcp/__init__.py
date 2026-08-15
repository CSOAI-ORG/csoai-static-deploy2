"""meok-sovereign-experiment-mcp — A/B Testing Harness for Sovereign AI.

For comparing sovereign fine-tunes against base models on measured axes.
Wilson 95% CI + McNemar exact test on discordant pairs.

5 tools:
  1. exp_register   - register a new experiment (control + variant + axis + items)
  2. exp_record     - record a comparison result (which item won, who was control)
  3. exp_analyze    - Wilson 95% CI for both + McNemar p on discordants
  4. exp_list       - list all experiments with current state
  5. exp_conclude   - emit a signed conclusion if sample size is sufficient
"""
from __future__ import annotations
import json
import hashlib
import math
from datetime import datetime, timezone
from typing import Optional, List

PROTOCOL = "sovereign-experiment/1.0"
VERSION = "1.0.0"

EXPERIMENTS = {}   # eid -> {control, variant, axis, items[], results[]}
USABLE_N = 30      # below this -> UNMEASURED label, never quote


def _sign(payload):
    body = json.dumps(payload, sort_keys=True, default=str)
    payload["kid"] = "exp-" + hashlib.sha256(body.encode()).hexdigest()[:16]
    payload["sig"] = hashlib.sha256((payload["kid"] + body).encode()).hexdigest()[:16]
    payload["ts"] = datetime.now(timezone.utc).isoformat()
    return payload


def _wilson(k, n, z=1.96):
    """Wilson 95% CI for a binomial proportion. k=wins, n=trials."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    denom = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denom
    half = (z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half), p)


def _mcnemar(b, c):
    """McNemar exact test (two-sided) on discordant pairs (b,c)."""
    if b + c == 0:
        return 1.0
    # binomial p=0.5, two-sided via min(1, 2*binom.cdf(min(b,c), b+c, 0.5))
    n = b + c
    k = min(b, c)
    # binomial pmf cumulative from 0..k
    from math import comb
    p_le_k = sum(comb(n, i) * (0.5 ** n) for i in range(k + 1))
    p_val = min(1.0, 2 * p_le_k)
    return round(p_val, 6)


# ---- tool 1: exp_register ----
def exp_register(control: str, variant: str, axis: str, items: List[str],
                 hypothesis: str = "", eid: Optional[str] = None) -> dict:
    """Register a new A/B experiment."""
    eid = eid or "e-" + hashlib.sha256(
        (control + variant + axis + datetime.now().isoformat()).encode()
    ).hexdigest()[:12]
    payload = {
        "eid": eid,
        "control": control,         # baseline model name
        "variant": variant,         # sovereign model name
        "axis": axis,               # governance / art5 / prv / care ...
        "items": items,             # list of item ids
        "hypothesis": hypothesis,
        "results": [],              # [{item_id, winner: control|variant, agree: bool}]
        "status": "registered",
    }
    EXPERIMENTS[eid] = payload
    return _sign({"eid": eid, **payload})


# ---- tool 2: exp_record ----
def exp_record(eid: str, item_id: str, winner: str, control_correct: bool,
               variant_correct: bool) -> dict:
    """Record one comparison result. discordants feed McNemar; both-correct count as ties."""
    if eid not in EXPERIMENTS:
        return _sign({"error": f"experiment {eid} not found"})
    exp = EXPERIMENTS[eid]
    rec = {
        "item_id": item_id,
        "winner": winner,
        "control_correct": control_correct,
        "variant_correct": variant_correct,
        "agree": control_correct == variant_correct,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    exp["results"].append(rec)
    exp["status"] = "running"
    return _sign({"eid": eid, "recorded": rec, "n": len(exp["results"])})


# ---- tool 3: exp_analyze ----
def exp_analyze(eid: str) -> dict:
    """Wilson 95% CI for control & variant win-rate + McNemar exact p on discordants."""
    if eid not in EXPERIMENTS:
        return _sign({"error": f"experiment {eid} not found"})
    exp = EXPERIMENTS[eid]
    r = exp["results"]
    n = len(r)
    ctrl_wins = sum(1 for x in r if x["winner"] == "control")
    var_wins = sum(1 for x in r if x["winner"] == "variant")
    ties = sum(1 for x in r if x["winner"] in ("tie", "neither"))
    # discordants: control correct but variant wrong (b), and the opposite (c)
    b = sum(1 for x in r if x["control_correct"] and not x["variant_correct"])
    c = sum(1 for x in r if not x["control_correct"] and x["variant_correct"])
    ctrl_lo, ctrl_hi, ctrl_p = _wilson(ctrl_wins, n)
    var_lo, var_hi, var_p = _wilson(var_wins, n)
    mcnemar_p = _mcnemar(b, c)
    usable = n >= USABLE_N
    label = "MEASURED" if usable else "UNMEASURED"
    # winner label
    if not usable:
        verdict = "INSUFFICIENT_SAMPLES"
    elif mcnemar_p < 0.05:
        if var_p > ctrl_p:
            verdict = "VARIANT_WINS"
        elif ctrl_p > var_p:
            verdict = "CONTROL_WINS"
        else:
            verdict = "TIE"
    else:
        verdict = "NO_SIGNIFICANT_DIFFERENCE"
    analysis = {
        "eid": eid,
        "n": n,
        "usable_n": USABLE_N,
        "label": label,
        "control": {
            "model": exp["control"],
            "wins": ctrl_wins,
            "win_rate": round(ctrl_p, 4),
            "ci95": [round(ctrl_lo, 4), round(ctrl_hi, 4)],
        },
        "variant": {
            "model": exp["variant"],
            "wins": var_wins,
            "win_rate": round(var_p, 4),
            "ci95": [round(var_lo, 4), round(var_hi, 4)],
        },
        "ties": ties,
        "discordants": {"b_control_only": b, "c_variant_only": c},
        "mcnemar_p": mcnemar_p,
        "verdict": verdict,
        "axis": exp["axis"],
    }
    return _sign(analysis)


# ---- tool 4: exp_list ----
def exp_list() -> dict:
    """List all experiments with current state."""
    out = []
    for eid, exp in EXPERIMENTS.items():
        n = len(exp["results"])
        out.append({
            "eid": eid,
            "control": exp["control"],
            "variant": exp["variant"],
            "axis": exp["axis"],
            "n": n,
            "label": "MEASURED" if n >= USABLE_N else "UNMEASURED",
            "status": exp["status"],
        })
    return _sign({"count": len(out), "experiments": out})


# ---- tool 5: exp_conclude ----
def exp_conclude(eid: str, signer: str = "sovereign-council") -> dict:
    """Emit a signed conclusion. Only valid if MEASURED (n >= USABLE_N)."""
    if eid not in EXPERIMENTS:
        return _sign({"error": f"experiment {eid} not found"})
    exp = EXPERIMENTS[eid]
    if len(exp["results"]) < USABLE_N:
        return _sign({"error": f"n={len(exp['results'])} < USABLE_N={USABLE_N}; cannot conclude"})
    analysis = exp_analyze(eid)
    body = json.dumps(analysis, sort_keys=True, default=str)
    conclusion = {
        "eid": eid,
        "verdict": analysis["verdict"],
        "axis": exp["axis"],
        "signer": signer,
        "analysis": analysis,
        "conclusion_kid": "conc-" + hashlib.sha256(body.encode()).hexdigest()[:16],
    }
    conclusion["conclusion_sig"] = hashlib.sha256(
        (conclusion["conclusion_kid"] + body).encode()
    ).hexdigest()[:32]
    return _sign(conclusion)


# ---- MCP server entrypoint ----
def main():
    import sys
    print(json.dumps({
        "name": "meok-sovereign-experiment-mcp",
        "version": VERSION,
        "protocol": PROTOCOL,
        "tools": [
            {"name": "exp_register",  "fn": exp_register},
            {"name": "exp_record",    "fn": exp_record},
            {"name": "exp_analyze",   "fn": exp_analyze},
            {"name": "exp_list",      "fn": exp_list},
            {"name": "exp_conclude",  "fn": exp_conclude},
        ],
    }))


if __name__ == "__main__":
    main()
