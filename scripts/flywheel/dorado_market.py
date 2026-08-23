#!/usr/bin/env python3
"""dorado_market.py — pull live East/West index data for the Dorado Bench market rail.

Writes a timestamped JSON snapshot that functions/api/dorado.ts can serve, or the
Mac-side cron can refresh every 15 min. yfinance, no key needed.

Output: /tmp/dorado_market.json (and optionally SOVOS/living/dorado_market.json)
"""
import json, sys, os
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    print("yfinance not installed", file=sys.stderr)
    sys.exit(1)

# East-vs-West AI-THEME pair (2026-08-20 research: country indices dilute the AI
# story with banks/energy). West = AI-specific ETFs; East = China AI/tech proxies.
# NOTE: KCAI is NOT an AI-companies ETF (AI-managed CSI-300 picker) — never use it.
PAIRS = [
    ("AIQ", "west", "Global X AI & Tech (AIQ)"),
    ("CHAT", "west", "Roundhill Generative AI (CHAT)"),
    ("BOTZ", "west", "Global X Robotics & AI (BOTZ)"),
    ("KWEB", "east", "KraneShares China Internet (KWEB)"),
    ("512930.SS", "east", "CSI AI Theme 930713 via 512930 ETF"),
]

def pull():
    rows = []
    for sym, side, label in PAIRS:
        try:
            h = yf.Ticker(sym).history(period="1mo")
            # NaN handling: some feeds (e.g. 512930.SS) have a one-day gap —
            # drop NaN closes and use the last valid value, noting the gap
            # honestly instead of emitting NaN into the rail.
            hc = h["Close"].dropna()
            if len(hc) > 1:
                last = float(hc.iloc[-1])
                prev = float(hc.iloc[-2])
                first = float(hc.iloc[0])
                n_gap = len(h) - len(hc)
                rows.append({
                    "index": label, "symbol": sym, "side": side,
                    "last": round(last, 2),
                    "chg_1d": round((last / prev - 1) * 100, 2),
                    "chg_30d": round((last / first - 1) * 100, 2),
                    "high_30d": round(float(h["High"].max()), 2),
                    "low_30d": round(float(h["Low"].min()), 2),
                    **({"note": f"{n_gap} day(s) NaN dropped (feed gap)"} if n_gap else {}),
                })
            else:
                rows.append({"index": label, "symbol": sym, "side": side, "last": None, "note": "insufficient data"})
        except Exception as e:
            rows.append({"index": label, "symbol": sym, "side": side, "last": None, "note": str(e)[:40]})
    return {
        "schema": "csoai.dorado-market/0.1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "source": "yfinance live pull (Yahoo Finance), free no-key",
        "discipline": "timestamped live snapshot — REPORTED market state, never blended into MEASURED cells",
        "rows": rows,
    }

if __name__ == "__main__":
    snap = pull()
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/dorado_market.json"
    with open(out, "w") as f:
        json.dump(snap, f, indent=1)
    print(f"dorado market snapshot -> {out} ({len(snap['rows'])} rows)")
    for r in snap["rows"]:
        if r.get("last"):
            print(f"  {r['side']:4s} {r['index']:14s} {r['last']:>10,.0f}  1d {r['chg_1d']:+.2f}%  30d {r['chg_30d']:+.2f}%")
