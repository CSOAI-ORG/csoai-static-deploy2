#!/usr/bin/env python3
"""FUSE → measured_compliance.json (next-week plan move #1).

Merges the four estate assets into ONE public evidence surface:
  - catalog.json            (the reference index — what exists)
  - feeds/benchmark_contamination.json (the anti-Goodhart register)
  - ~/sim-world-data/arena-elo.json     (the MEASURED arena Elo, own pillars, not market)
  - ~/sim-world-data/board-live.json    (the LIVE measured gauge — 18 axes, signed cards)

Doctrine: this is MEASUREMENT (a signed attestation when the Ed25519 rail lands), NEVER a
certification. anti-benchmark-gaming / EU-AI-Act-GPAI compliance is the target consumer.

Run: python3 ops/build_measured_compliance.py
"""
import json
import os
import time

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(PACK, "feeds", "measured_compliance.json")


def load(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def main():
    cat = load(os.path.join(PACK, "catalog.json"))
    contam = load(os.path.join(PACK, "feeds", "benchmark_contamination.json"))
    elo = load(os.path.expanduser("~/sim-world-data/arena-elo.json"))
    board = load(os.path.expanduser("~/sim-world-data/board-live.json"))

    idx = {"items": cat.get("counts") if cat else None, "canary": cat.get("canary") if cat else None}
    cont = {"benchmarks": len((contam or {}).get("benchmarks", [])),
            "resistant": sum(1 for b in (contam or {}).get("benchmarks", []) if b.get("designed_resistant")),
            "high": sum(1 for b in (contam or {}).get("benchmarks", []) if b.get("level") == "high")}
    elo_lb = sorted((elo or {}).get("leaderboard", []), key=lambda m: -m.get("elo", 0))[:10]
    axes_out = [{"axis": a.get("axis"), "records": a.get("record_count"),
                 "models": a.get("model_count"), "mean": round(a.get("mean_score", 0), 4)}
                for a in (board or {}).get("axes", [])]

    out = {
        "generated": time.strftime("%Y-%m-%d"),
        "purpose": "measured-compliance evidence surface — reference index + measured gauge + "
                   "measured arena Elo + contamination register, fused. Anti-benchmark-gaming and "
                   "EU AI Act GPAI-compliance evidence. MEASUREMENT, not certification.",
        "index": idx,
        "contamination_register": cont,
        "measured_arena_elo": {"method": (elo or {}).get("method", "—"),
                               "head_to_head": (elo or {}).get("head_to_head", 0),
                               "top": [{"model": m.get("model"), "elo": m.get("elo")} for m in elo_lb],
                               "notes": (elo or {}).get("honest", "—")},
        "measured_gauge": {"live_records": (board or {}).get("live_records", 0),
                           "signed_cards": (board or {}).get("signed_cards", 0),
                           "mean_of_axes": (board or {}).get("mean_of_axes"),
                           "axes": axes_out},
        "status": "MEASURED (not certified) — the signed Ed25519 attestation lands with the #dsh rail",
        "honest_register": "unmeasured axes stay UNMEASURED; no score inflated by contamination; "
                           "anti-Goodhart register is the differentiator",
    }
    os.makedirs(os.path.dirname(FEED), exist_ok=True)
    with open(FEED, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(f"measured_compliance.json written — index {idx.get('items')} · contamination {cont} · "
          f"arena {len(elo_lb)} top · gauge {out['measured_gauge']['live_records']} records "
          f"({len(axes_out)} axes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
