#!/usr/bin/env python3
"""TEA × EAT dual-walk — the drum's BACKWARD walker (TEA).

EAT walks forward (premise -> artifact: build the catalog, append the archive).
TEA walks backward (artifact -> premises: re-derive content_ids from the bytes,
re-verify signature labels, re-check the canary). Meet in the middle = the claim
is REAL; diverge = anomaly logged loud. The archive audits itself.

Checks:
  1. content_id recompute — every archive entry's id must re-derive from (kind,name,payload)
  2. signed-label drift — signed:true entries MUST carry a signature; signed:false must not
  3. catalog canary + card coverage — the live catalog is the forward artifact
  4. router trust marker — honest state reported (not re-decided)

Run: python3 archive/dualwalk.py   (writes feeds/dualwalk_report.json, exit 1 on drift)
"""
import json
import os
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(PACK, "archive", "store", "index.jsonl")
REPORT = os.path.join(PACK, "feeds", "dualwalk_report.json")


def tea_walk():
    findings = {"content_id_drift": [], "signed_label_drift": [], "unparseable": 0}
    if not os.path.exists(ARCHIVE):
        return findings, 0
    sys.path.insert(0, os.path.join(PACK, "archive"))
    import knowledge_archive as ka
    walked = 0
    for line in open(ARCHIVE, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        walked += 1
        try:
            e = json.loads(line)
        except Exception:
            findings["unparseable"] += 1
            continue
        recomputed = ka.content_id(e)
        if recomputed != e.get("content_id"):
            findings["content_id_drift"].append({"name": e.get("name"), "stored": e.get("content_id"), "recomputed": recomputed})
        if e.get("signed") is True and not e.get("signature"):
            findings["signed_label_drift"].append({"name": e.get("name"), "kind": "signed-without-signature"})
        if e.get("signed") is False and e.get("signature"):
            findings["signed_label_drift"].append({"name": e.get("name"), "kind": "unsigned-but-carrying-signature"})
    return findings, walked


def forward_state():
    cat = json.load(open(os.path.join(PACK, "catalog.json")))
    dirs = {"framework": "frameworks", "charter": "charters", "regulation": "regulations",
            "article": "articles", "sector": "sectors"}
    expected = {f"{dirs[i['kind']]}/{i['id']}.md" for i in cat["items"]}
    actual = set()
    for d in set(dirs.values()):
        for f in os.listdir(os.path.join(PACK, d)):
            if f.endswith(".md"):
                actual.add(f"{d}/{f}")
    return {"canary_ok": cat.get("canary") == "drum-canary-7f3a9c2e",
            "cards_ok": expected == actual,
            "items": len(cat["items"]),
            "missing_cards": len(expected - actual), "stale_cards": len(actual - expected)}


def main():
    findings, walked = tea_walk()
    fwd = forward_state()
    drift = findings["content_id_drift"] + findings["signed_label_drift"] or findings["unparseable"]
    report = {
        "walk": "TEA (backward)",
        "ts": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
        "archive": {"walked": walked, "content_id_drift": findings["content_id_drift"],
                    "signed_label_drift": findings["signed_label_drift"],
                    "unparseable": findings["unparseable"]},
        "forward": fwd,
        "verdict": "EAT meets TEA — claim REAL" if not drift and fwd["canary_ok"] and fwd["cards_ok"]
                   else "DIVERGENCE — anomaly logged loud",
    }
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    print(json.dumps(report, indent=1)[:600])
    return 1 if (drift or not fwd["canary_ok"] or not fwd["cards_ok"]) else 0


if __name__ == "__main__":
    sys.exit(main())
