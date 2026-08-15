"""meok-sovereign-pulse-mcp — Sovereign System Heartbeat.

For monitoring the SOVEREIGN substrate in real time:
- BPM: beats per minute (sigil issuance rate per minute)
- Latency: p50/p95 model call latency
- Sigil rate: signed events/sec across the substrate
- Drift: rolling-mean deviation from steady-state

5 tools:
  1. pulse_beat       - emit a single pulse event (heartbeat, sigil, model-call, etc.)
  2. pulse_summary    - rolling summary (BPM, p50/p95, sigil rate)
  3. pulse_drift      - detect drift from baseline (3σ rule)
  4. pulse_bft_health - per-BFT-voter liveness / weight / agreement ratio
  5. pulse_dashboard  - all-in-one dashboard payload
"""
from __future__ import annotations
import json
import hashlib
import time
import math
import statistics
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

PROTOCOL = "sovereign-pulse/1.0"
VERSION = "1.0.0"

_PULSE_LOG = []          # list of pulse events (capped at 10_000)
_BFT_VOTERS = {          # default 33-voter BFT council
    "voter_0":  {"weight": 1.0, "role": "anchor"},
    "voter_1":  {"weight": 1.0, "role": "guardian"},
    "voter_2":  {"weight": 1.0, "role": "care"},
    "voter_3":  {"weight": 1.0, "role": "art5"},
}
_BASELINE = {
    "bpm": 60.0,
    "p50_latency_ms": 80.0,
    "p95_latency_ms": 240.0,
    "sigil_rate_per_min": 12.0,
    "bft_agreement": 0.667,
}
_DRIFT_SIGMA = 3.0


def _sign(payload):
    body = json.dumps(payload, sort_keys=True, default=str)
    payload["kid"] = "pulse-" + hashlib.sha256(body.encode()).hexdigest()[:16]
    payload["sig"] = hashlib.sha256((payload["kid"] + body).encode()).hexdigest()[:16]
    payload["ts"] = datetime.now(timezone.utc).isoformat()
    return payload


# ---- tool 1: pulse_beat ----
def pulse_beat(kind: str = "heartbeat", latency_ms: Optional[float] = None,
               voter: Optional[str] = None, weight: Optional[float] = None,
               meta: Optional[Dict[str, Any]] = None) -> dict:
    """Emit one pulse event. kinds: heartbeat | sigil | model_call | bft_vote | custom."""
    ev = {
        "kind": kind,
        "ts": datetime.now(timezone.utc).isoformat(),
        "epoch": time.time(),
        "latency_ms": latency_ms,
        "voter": voter,
        "weight": weight,
        "meta": meta or {},
    }
    _PULSE_LOG.append(ev)
    if len(_PULSE_LOG) > 10_000:
        del _PULSE_LOG[:len(_PULSE_LOG) - 10_000]
    return _sign({"emitted": ev, "log_size": len(_PULSE_LOG)})


def _percentile(xs, p):
    if not xs:
        return 0.0
    s = sorted(xs)
    k = (len(s) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[f] + (s[c] - s[f]) * (k - f)


def _rolling_window(window_s: int = 60):
    """Return pulse events in the last `window_s` seconds."""
    now = time.time()
    return [e for e in _PULSE_LOG if now - e["epoch"] <= window_s]


# ---- tool 2: pulse_summary ----
def pulse_summary(window_s: int = 60) -> dict:
    """Rolling summary over the last window_s seconds."""
    win = _rolling_window(window_s)
    n = len(win)
    if n == 0:
        return _sign({"window_s": window_s, "n": 0, "bpm": 0.0,
                      "p50_latency_ms": 0.0, "p95_latency_ms": 0.0,
                      "sigil_rate_per_min": 0.0, "kind_counts": {}})
    # BPM = beats per minute. kinds=heartbeat|sigil count.
    beat_kinds = {"heartbeat", "sigil"}
    beats = sum(1 for e in win if e["kind"] in beat_kinds)
    bpm = beats * (60.0 / window_s) if window_s else 0.0
    # latency
    lat = [e["latency_ms"] for e in win if e["latency_ms"] is not None]
    p50 = _percentile(lat, 0.50)
    p95 = _percentile(lat, 0.95)
    # sigil rate
    sigils = sum(1 for e in win if e["kind"] == "sigil")
    sigil_rate = sigils * (60.0 / window_s) if window_s else 0.0
    # kind counts
    kc: Dict[str, int] = {}
    for e in win:
        kc[e["kind"]] = kc.get(e["kind"], 0) + 1
    return _sign({
        "window_s": window_s,
        "n": n,
        "bpm": round(bpm, 2),
        "p50_latency_ms": round(p50, 2),
        "p95_latency_ms": round(p95, 2),
        "sigil_rate_per_min": round(sigil_rate, 2),
        "kind_counts": kc,
    })


# ---- tool 3: pulse_drift ----
def pulse_drift(window_s: int = 60) -> dict:
    """Detect drift from baseline using 3σ rule on the current window."""
    summary = pulse_summary(window_s)
    body = summary.copy()
    drifts = []
    metrics = {
        "bpm": summary["bpm"],
        "p50_latency_ms": summary["p50_latency_ms"],
        "p95_latency_ms": summary["p95_latency_ms"],
        "sigil_rate_per_min": summary["sigil_rate_per_min"],
    }
    # naive σ = 10% of baseline
    for k, v in metrics.items():
        base = _BASELINE.get(k, 0.0)
        sigma = max(abs(base) * 0.1, 1e-6)
        z = (v - base) / sigma if sigma else 0.0
        drifts.append({
            "metric": k,
            "value": v,
            "baseline": base,
            "sigma": round(sigma, 4),
            "z": round(z, 2),
            "drift": abs(z) > _DRIFT_SIGMA,
        })
    body["drifts"] = drifts
    body["baseline"] = _BASELINE
    body["drift_sigma_rule"] = _DRIFT_SIGMA
    body["verdict"] = "DRIFT" if any(d["drift"] for d in drifts) else "STEADY"
    return _sign(body)


# ---- tool 4: pulse_bft_health ----
def pulse_bft_health(agreement_ratio: Optional[float] = None) -> dict:
    """Snapshot BFT voter liveness."""
    if agreement_ratio is not None:
        _BFT_VOTERS["voter_0"]["last_agreement"] = agreement_ratio
    snapshot = {
        "voters": len(_BFT_VOTERS),
        "weights_sum": round(sum(v["weight"] for v in _BFT_VOTERS.values()), 3),
        "agreement_baseline": _BASELINE["bft_agreement"],
        "last_agreement": agreement_ratio,
        "verdict": ("QUORUM_OK"
                    if (agreement_ratio or _BASELINE["bft_agreement"]) >= _BASELINE["bft_agreement"]
                    else "BELOW_QUORUM"),
    }
    return _sign(snapshot)


# ---- tool 5: pulse_dashboard ----
def pulse_dashboard(window_s: int = 60) -> dict:
    """All-in-one dashboard payload."""
    return _sign({
        "summary": pulse_summary(window_s),
        "drift":   pulse_drift(window_s),
        "bft":     pulse_bft_health(),
        "log_size": len(_PULSE_LOG),
    })


def main():
    print(json.dumps({
        "name": "meok-sovereign-pulse-mcp",
        "version": VERSION,
        "protocol": PROTOCOL,
        "tools": [
            {"name": "pulse_beat",        "fn": pulse_beat},
            {"name": "pulse_summary",     "fn": pulse_summary},
            {"name": "pulse_drift",       "fn": pulse_drift},
            {"name": "pulse_bft_health",  "fn": pulse_bft_health},
            {"name": "pulse_dashboard",   "fn": pulse_dashboard},
        ],
    }))


if __name__ == "__main__":
    main()
