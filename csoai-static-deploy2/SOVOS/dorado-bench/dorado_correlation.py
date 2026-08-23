#!/usr/bin/env python3
"""dorado_correlation.py — reg-event → market-gap time-window correlation (longitudinal Dorado).

For each regulation event (East or West), pull the index time series around the event date
and compute the East-vs-West log-return gap over that window. This is the longitudinal
extension: point-in-time pair-gap (dorado_bench) → event-anchored gap.

Register: MEASURED (deterministic historical-data predicates). Context, never fused into
provision-conformance. Fail-closed: no series -> no gap -> UNMEASURED stated.
"""
from __future__ import annotations
import json, time, urllib.request, urllib.error
from dorado_bench import REG_EVENTS, WEST_INDICES, EAST_INDICES

def historical_series(symbol: str, period1: int, period2: int) -> list:
    """Daily closes for symbol between unix times. Deterministic, fail-closed -> []."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(symbol)}"
           f"?period1={period1}&period2={period2}&interval=1d")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read().decode())
        res = d.get("chart", {}).get("result", [{}])
        if not res: return []
        ts = res[0].get("timestamp", [])
        closes = res[0].get("indicators", {}).get("quote", [{}])[0].get("close", [])
        return [{"date": time.strftime("%Y-%m-%d", time.gmtime(t)), "close": c}
                for t, c in zip(ts, closes) if c is not None]
    except Exception:
        return []

def event_window_gap(event: dict, east_sym: str, west_sym: str, days: int = 21) -> dict:
    """Gap = log-return(East) - log-return(West) over the window starting at the event date.
    East event -> expect East to react; West event -> expect West. The gap is context."""
    import datetime
    try:
        ev_date = datetime.datetime.strptime(event["date"], "%Y-%m-%d")
    except Exception:
        return {"ok": False, "error": "bad event date"}
    p1 = int(ev_date.replace(tzinfo=datetime.timezone.utc).timestamp())
    p2 = p1 + days * 86400
    e_ser = historical_series(east_sym, p1, p2)
    w_ser = historical_series(west_sym, p1, p2)
    if len(e_ser) < 2 or len(w_ser) < 2:
        return {"ok": False, "error": "series unavailable (fail-closed)", "event": event["id"],
                "east": east_sym, "west": west_sym, "register": "UNMEASURED"}
    e_ret = __import__("math").log(e_ser[-1]["close"] / e_ser[0]["close"])
    w_ret = __import__("math").log(w_ser[-1]["close"] / w_ser[0]["close"])
    gap = e_ret - w_ret
    return {"ok": True, "event": event["id"], "jurisdiction": event["jurisdiction"],
            "region": event["region"], "date": event["date"], "days": days,
            "east": {"symbol": east_sym, "log_return": round(e_ret, 5)},
            "west": {"symbol": west_sym, "log_return": round(w_ret, 5)},
            "gap": round(gap, 5),
            "interpretation": ("EAST_OVERPERFORMS" if gap > 0 else "WEST_OVERPERFORMS" if gap < 0 else "PARITY"),
            "register": "MEASURED (historical data, deterministic)",
            "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

if __name__ == "__main__":
    out = []
    for ev in REG_EVENTS:
        # East event -> East index reacts; West event -> West index reacts; compare the other side
        east_sym = "^HSI" if ev["region"] == "EAST" else "^N225"
        west_sym = "^GSPC"
        out.append(event_window_gap(ev, east_sym, west_sym))
    print(json.dumps(out, indent=1))
