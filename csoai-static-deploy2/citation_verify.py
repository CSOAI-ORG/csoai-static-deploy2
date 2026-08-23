#!/usr/bin/env python3
"""citation_verify.py — the missing success signal: does the cited law actually exist?

═══════════════════════════════════════════════════════════════════════════════
WHY THIS IS THE KEYSTONE
═══════════════════════════════════════════════════════════════════════════════
Two separate things were blocked on the same missing piece:

  1. **Stigmergy** needs a per-query success signal. Without one, reinforcing a trail because
     it was TAKEN produces rich-get-richer on an accident — worse than the max-router.
  2. **The spine** cannot be scored, because GovBench dimensions are test modalities not topics,
     so benchmark accuracy measures the wrong thing.

Governance is unusually lucky here: **its ground truth is checkable.** "Article 5 of the EU AI
Act prohibits social scoring" is either right or it is not. A model that answers fluently while
citing Article 47 for something Article 5 covers is producing exactly the failure a compliance
buyer cares about most — and it is detectable without a human.

That makes citation accuracy a real, automatic, per-response signal. It is the one this estate
can actually build, and it feeds both blocked systems.

═══════════════════════════════════════════════════════════════════════════════
WHAT IT CAN AND CANNOT DO — read before trusting the number
═══════════════════════════════════════════════════════════════════════════════
  ✅ CATCHES: citations to articles/annexes that DO NOT EXIST (out of range), and citations
     that exist but are attributed the WRONG SUBJECT (Article 5 claimed to cover documentation).
  ❌ MISSES: a real citation used in a subtly wrong context, and any instrument not in the
     registry below. Absence of a flag is NOT proof of correctness.

The registry is deliberately small and hand-checked. A large auto-scraped registry would be
worse: wrong ground truth turns a verifier into a confident liar, and this file's whole purpose
is to be the thing you can trust when models cannot be.

    python3 citation_verify.py --text "Article 5 prohibits social scoring"
    python3 citation_verify.py --score-model sov33-evolved:latest
"""
from __future__ import annotations

import argparse, json, os, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OLLAMA = os.environ.get("OLLAMA_CHAT", "http://localhost:11434/api/chat")

# Hand-checked. Each entry: valid range + the subject each key article actually governs.
REGISTRY = {
    "EU AI Act": {
        "max_article": 113,
        "max_annex_roman": 13,
        "articles": {
            5:  ["prohibited", "social scoring", "biometric", "manipulat", "exploit",
                 "predictive polic", "emotion recognition", "facial recognition", "scraping"],
            6:  ["high-risk", "classification", "annex iii"],
            9:  ["risk management"],
            10: ["data", "governance", "training data"],
            11: ["technical documentation", "annex iv"],
            12: ["record", "logging", "logs"],
            13: ["transparency", "instructions for use"],
            14: ["human oversight"],
            15: ["accuracy", "robustness", "cybersecurity"],
            50: ["transparency obligation", "disclos", "deepfake", "ai-generated", "chatbot"],
            99: ["penalt", "fine", "35 million", "7%"],
        },
        "annexes": {"III": ["high-risk", "use case"], "IV": ["technical documentation"]},
    },
    "GDPR": {
        "max_article": 99,
        "articles": {
            9:  ["special categor", "sensitive", "biometric", "health"],
            17: ["erasure", "right to be forgotten"],
            22: ["automated decision", "profiling"],
            35: ["impact assessment", "dpia"],
            83: ["fine", "penalt", "20 million", "4%"],
        },
    },
    "Solvency II": {
        "max_article": 311,
        "articles": {
            45:  ["orsa", "own risk"],
            100: ["scr", "solvency capital"],
            101: ["scr", "calibrat", "99.5"],
            112: ["internal model", "approval"],
            128: ["mcr", "minimum capital"],
            129: ["mcr", "floor"],
            51:  ["sfcr", "public disclosure"],
        },
    },
}

# Known non-article instruments (top-level facts, REAL-cited from corrections #51-56).
# These are RECOGNIZED (exists: true) but not article-subject-checked (subject_match: None)
# because their article-level text is not yet in the registry. No fabricated mappings.
KNOWN = {
    "Illinois SB 315": {"signed": "2026-07-06", "effective": "2027-01-01",
                        "audits": "2028-01-01", "scope": ">$500M or >10^26 FLOPs"},
    "Vietnam Decree 142": {"basis": "Law 33/2026", "systems": 46, "sectors": 6,
                           "deadlines": "2027-03-01 / 2027-09-01"},
    "Germany KI-MIG": {"operator": "BNetzA", "since": "2026-07-29", "cab_assessor": "DAkkS"},
    "SCITT RFC 9943": {"status": "Standards Track", "date": "2026-06"},
    "COSE Receipts RFC 9942": {"status": "Standards Track", "date": "2026-06"},
}

CITE_RX = re.compile(
    r"\b(?:(EU AI Act|AI Act|GDPR|Solvency II)\s+)?"
    r"(?:Article|Art\.?)\s*(\d{1,3})"
    r"|(?:Annex)\s+([IVXL]+)", re.I)


def _instrument(text: str, near: str) -> str:
    t = (near + " " + text).lower()
    if "gdpr" in t or "data protection regulation" in t: return "GDPR"
    if "solvency" in t: return "Solvency II"
    return "EU AI Act"


def verify_text(text: str) -> dict:
    """Extract citations and check each against the registry."""
    findings = []
    for name, facts in KNOWN.items():
        if name.lower() in text.lower():
            findings.append({"cite": name, "exists": True, "subject_match": None, "facts": facts})
    for m in CITE_RX.finditer(text):
        named, art, annex = m.group(1), m.group(2), m.group(3)
        ctx = text[max(0, m.start() - 90): m.end() + 140].lower()
        inst = named if named else _instrument(text, ctx)
        inst = {"AI Act": "EU AI Act"}.get(inst, inst)
        reg = REGISTRY.get(inst)
        if not reg:
            continue
        if annex:
            ok = annex.upper() in reg.get("annexes", {})
            subj = reg.get("annexes", {}).get(annex.upper(), [])
            hit = any(s in ctx for s in subj) if subj else None
            findings.append({"cite": f"{inst} Annex {annex.upper()}", "exists": ok,
                             "subject_match": hit})
            continue
        n = int(art)
        exists = n <= reg["max_article"]
        subj = reg["articles"].get(n)
        # subject_match is None when we hold no subject list — "unknown", never "wrong".
        hit = (any(s in ctx for s in subj) if subj else None)
        findings.append({"cite": f"{inst} Article {n}", "exists": exists,
                         "subject_match": hit,
                         "expected_subjects": subj[:4] if subj else None})

    fabricated = [f for f in findings if not f["exists"]]
    misattributed = [f for f in findings if f["exists"] and f["subject_match"] is False]
    checked = [f for f in findings if f["subject_match"] is not None]
    return {
        "citations": len(findings),
        "fabricated": len(fabricated),
        "misattributed": len(misattributed),
        "checkable": len(checked),
        "accuracy": (round(sum(1 for f in checked if f["subject_match"]) / len(checked), 3)
                     if checked else None),
        "findings": findings,
    }


PROBES = [
    "Which article of the EU AI Act prohibits social scoring, and what else does it cover?",
    "What does Article 50 of the EU AI Act require?",
    "Under GDPR, which article covers the right to erasure?",
    "Which Solvency II article governs the Solvency Capital Requirement?",
    "What does Annex III of the EU AI Act list?",
    "Which GDPR article sets the maximum administrative fine?",
    "Which EU AI Act article requires human oversight of high-risk systems?",
    "Which Solvency II article requires prior approval of an internal model?",
]


def score_model(model: str) -> dict:
    print(f"  CITATION ACCURACY — {model}, {len(PROBES)} probes\n")
    tot = fab = mis = 0
    checked = correct = 0
    for p in PROBES:
        body = json.dumps({"model": model, "stream": False,
                           "options": {"temperature": 0, "num_predict": 220},
                           "messages": [{"role": "user", "content": p}]}).encode()
        req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                resp = json.loads(r.read())["message"]["content"]
        except Exception as e:
            print(f"    ⏭️  unreachable: {str(e)[:50]}")
            return {"unreachable": True}
        v = verify_text(resp)
        tot += v["citations"]; fab += v["fabricated"]; mis += v["misattributed"]
        checked += v["checkable"]
        correct += sum(1 for f in v["findings"] if f["subject_match"])
        flag = "🔴" if v["fabricated"] else ("🟠" if v["misattributed"] else "🟢")
        print(f"    {flag} cites={v['citations']} fabricated={v['fabricated']} "
              f"misattributed={v['misattributed']}  {p[:46]}")
    acc = round(correct / checked, 3) if checked else None
    print(f"\n    total citations : {tot}")
    print(f"    FABRICATED      : {fab}   (article does not exist)")
    print(f"    misattributed   : {mis}   (exists, wrong subject)")
    print(f"    subject accuracy: {acc if acc is not None else 'n/a'}  ({correct}/{checked} checkable)")
    out = {"timestamp": datetime.now(timezone.utc).isoformat(), "model": model,
           "citations": tot, "fabricated": fab, "misattributed": mis,
           "subject_accuracy": acc}
    p = HERE / "benchmark-results" / "citation_accuracy.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    hist = json.loads(p.read_text()) if p.exists() else []
    hist.append(out); p.write_text(json.dumps(hist, indent=2))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--score-model")
    a = ap.parse_args()
    if a.text:
        print(json.dumps(verify_text(a.text), indent=2))
    elif a.score_model:
        score_model(a.score_model)
    else:
        ap.print_help()
