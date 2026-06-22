#!/usr/bin/env python3
"""town_feed.py — emit town_feed.json: REAL attested data for Kimi's Agent-47 town UI.

Replaces the town's Math.random() fakes with the actual King-hive governed-vs-ungoverned
verdicts + the signed Policy-Lab DORA result + the SIGIL/Bitcoin anchors. ONLY attestable
verdicts are surfaced; everything carries honest scope labels. The UI fetch()es this file
(drop it in app/public/town_feed.json). Verify-it-yourself link points at the public repo.

Inputs (paths via env, all optional — missing ones are skipped):
  PL_VERDICTS  king_hive_verdicts.jsonl   (default ./king_hive_verdicts.jsonl)
  PL_POLICY    policy_lab_dora.jsonl      (default ./policy_lab_dora.jsonl)
  PL_ANCHORS   dir of anchor manifests    (default ./anchors)
Output: ./town_feed.json
"""
import os, sys, json, glob, statistics
from datetime import datetime, timezone

VERDICTS = os.environ.get("PL_VERDICTS", "king_hive_verdicts.jsonl")
POLICY = os.environ.get("PL_POLICY", "policy_lab_dora.jsonl")
ANCHORS = os.environ.get("PL_ANCHORS", "anchors")
OUT = os.environ.get("PL_OUT", "town_feed.json")
REPO = "https://github.com/CSOAI-ORG/sigil-proofs"

def load_jsonl(p):
    if not os.path.exists(p): return []
    out = []
    for l in open(p):
        l = l.strip()
        if l:
            try: out.append(json.loads(l))
            except Exception: pass
    return out

def king_hive():
    rows = load_jsonl(VERDICTS)
    att = [r for r in rows if r.get("attestable")]
    wins = {"A": 0, "B": 0, "TIE": 0}
    for r in att: wins[r.get("winner", "TIE")] = wins.get(r.get("winner", "TIE"), 0) + 1
    margins = [r.get("margin", 0) for r in att if isinstance(r.get("margin"), (int, float))]
    recent = []
    for r in att[-20:]:
        recent.append({
            "ts": r.get("ts"), "winner": r.get("winner"), "margin": r.get("margin"),
            "prompt": (r.get("prompt") or "")[:90],
            "king": (r.get("A") or {}).get("persona", "King/Dragon"),
            "queen": (r.get("B") or {}).get("persona", "Queen/Turtle"),
            "signed": bool(r.get("sigil")),
        })
    return {
        "summary": {"total_rounds": len(rows), "attestable": len(att), "wins": wins,
                    "avg_margin": round(statistics.mean(margins), 4) if margins else 0.0},
        "recent_verdicts": recent,
    }

def policy_lab():
    rows = load_jsonl(POLICY)
    results = [r for r in rows if str(r.get("schema", "")).endswith("experiment-result/v1")]
    out = []
    for r in results[-5:]:
        out.append({
            "experiment_id": r.get("experiment_id"), "verdict": r.get("verdict"),
            "agents": r.get("agents"), "attestable": r.get("attestable"),
            "merkle_root": (r.get("merkle_root") or "")[:24] + "…",
            "signed": bool(r.get("sigil")),
            "aggregate": r.get("aggregate"),
            "scope": r.get("_scope"),
        })
    return out

def anchors():
    out = []
    for m in sorted(glob.glob(os.path.join(ANCHORS, "manifest_*.json")) +
                    glob.glob(os.path.join(ANCHORS, "anchor_[0-9]*.json"))):
        try:
            d = json.load(open(m))
        except Exception:
            continue
        out.append({
            "anchor": os.path.basename(m),
            "root": (d.get("attestable_root") or "")[:24] + "…",
            "n_attestable": d.get("n_attestable"),
            "ts_first": d.get("ts_first"), "ts_last": d.get("ts_last"),
            "ots_proof": os.path.exists(m.replace("manifest_", "root_").replace(".json", ".txt.ots"))
                         or os.path.exists(m + ".ots"),
        })
    return out

def main():
    kh = king_hive()
    pl = policy_lab()
    an = anchors()
    feed = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": ("IN-SIMULATION governed-vs-ungoverned data. ONLY cryptographically-attestable "
                  "verdicts are shown. Policy-Lab results may be agents=stub (labeled). Bitcoin "
                  "anchors may be pending confirmation. Verify any of this yourself — no trust required."),
        "summary": {
            "king_hive": kh["summary"],
            "policy_lab": {"experiments": len(pl), "latest": (pl[-1]["verdict"] if pl else None),
                           "agents": (pl[-1]["agents"] if pl else None)},
            "anchors": {"count": len(an), "latest_root": (an[-1]["root"] if an else None),
                        "bitcoin": "pending-or-confirmed (run ots verify)"},
        },
        "recent_verdicts": kh["recent_verdicts"],
        "policy_lab": pl,
        "anchors": an,
        "verify": {"repo": REPO,
                   "how": "git clone " + REPO + " && python3 verify_anchor.py proofs/manifest_0000.json"},
    }
    json.dump(feed, open(OUT, "w"), indent=2, default=str)
    print("wrote", OUT)
    print("  king-hive: %d attestable / %d rounds  wins=%s" % (
        kh["summary"]["attestable"], kh["summary"]["total_rounds"], kh["summary"]["wins"]))
    print("  policy-lab experiments:", len(pl), "| anchors:", len(an))

if __name__ == "__main__":
    main()
