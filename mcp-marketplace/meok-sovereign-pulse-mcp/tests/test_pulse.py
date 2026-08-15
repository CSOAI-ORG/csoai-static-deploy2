import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import meok_sovereign_pulse_mcp as m
from meok_sovereign_pulse_mcp import (
    pulse_beat, pulse_summary, pulse_drift, pulse_bft_health,
    pulse_dashboard, _BASELINE,
)

def setup():
    m._PULSE_LOG.clear()

def test_beat_basic():
    setup()
    r = pulse_beat(kind="heartbeat", latency_ms=42.0, voter="voter_1")
    assert r["emitted"]["kind"] == "heartbeat"
    assert r["emitted"]["latency_ms"] == 42.0
    assert "kid" in r and r["kid"].startswith("pulse-")
    assert r["log_size"] >= 1

def test_summary_with_beats():
    setup()
    for _ in range(10):
        pulse_beat(kind="heartbeat", latency_ms=50.0)
    s = pulse_summary(window_s=60)
    assert s["n"] >= 10
    assert s["bpm"] > 0
    assert s["kind_counts"]["heartbeat"] >= 10
    assert s["p50_latency_ms"] == 50.0

def test_summary_p95():
    setup()
    for i in range(20):
        pulse_beat(kind="model_call", latency_ms=float(i * 10))
    s = pulse_summary(window_s=60)
    assert s["p95_latency_ms"] >= 175.0

def test_drift_steady():
    setup()
    # Inject realistic traffic matching baseline bpm/p50/p95/sigil
    # 12 sigils + 48 heartbeats spread over 60s window
    # latencies: mix of p50 and p95 to match baseline
    for _ in range(12):
        pulse_beat(kind="sigil", latency_ms=_BASELINE["p50_latency_ms"])
    # latencies for heartbeats: 80% near p50, 20% near p95
    for i in range(48):
        if i % 5 == 0:
            pulse_beat(kind="heartbeat", latency_ms=_BASELINE["p95_latency_ms"])
        else:
            pulse_beat(kind="heartbeat", latency_ms=_BASELINE["p50_latency_ms"])
    d = pulse_drift(window_s=60)
    assert d["verdict"] == "STEADY", f"drifts: {d['drifts']}"

def test_drift_when_high():
    setup()
    for _ in range(60):
        pulse_beat(kind="model_call", latency_ms=_BASELINE["p50_latency_ms"] * 5)
    d = pulse_drift(window_s=60)
    assert d["verdict"] == "DRIFT"
    assert any(x["drift"] for x in d["drifts"])

def test_bft_health_ok():
    h = pulse_bft_health(agreement_ratio=0.8)
    assert h["voters"] == 4
    assert h["verdict"] == "QUORUM_OK"

def test_bft_health_below():
    h = pulse_bft_health(agreement_ratio=0.4)
    assert h["verdict"] == "BELOW_QUORUM"

def test_dashboard():
    setup()
    pulse_beat(kind="sigil")
    d = pulse_dashboard(window_s=60)
    assert "summary" in d and "drift" in d and "bft" in d
    assert d["log_size"] >= 1

def test_log_cap():
    setup()
    for _ in range(10_005):
        pulse_beat(kind="heartbeat")
    assert len(m._PULSE_LOG) <= 10_000
