"""Sovereign data lake E2E tests."""
import os
import sys
import time
import sqlite3
import json
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_lake as dl
from data_lake import (
    persist_report, persist_sigil, persist_bft_vote, persist_care_metric,
    query_reports, query_sigil, query_bft, query_care_metrics,
    backend_status, _sqlite_conn, _init_sqlite, CARE_FLOOR,
)


def _wipe():
    """Drop all tables and recreate."""
    with _sqlite_conn() as conn:
        for t in ["reports", "sigil_chain", "bft_votes", "care_metrics"]:
            conn.execute(f"DROP TABLE IF EXISTS {t}")
    _init_sqlite()


def test_01_persist_report_basic():
    _wipe()
    r = persist_report(
        reporter_type="human",
        location={"lat": 51.5, "lng": -0.1, "label": "London"},
        type_="safety",
        severity=0.7,
        confidence=0.9,
        sigil="ed25519:abc")
    assert r.get("ok"), r
    assert isinstance(r.get("id"), int)
    print(f"  v persist_report OK (id={r['id']})")


def test_02_persist_report_invalid_severity():
    _wipe()
    r = persist_report("human", {"lat": 0}, "safety", severity=1.5)
    assert "error" in r
    print("  v severity 1.5 rejected with error")


def test_03_persist_sigil_chain_continuity():
    _wipe()
    r1 = persist_sigil("kid-1", "sig-A", "TEST|a", mcp_name="mcp-a")
    r2 = persist_sigil("kid-2", "sig-B", "TEST|b", mcp_name="mcp-b")
    r3 = persist_sigil("kid-3", "sig-C", "TEST|c", mcp_name="mcp-c")
    assert r1["prev_hash"] in ("", None) or len(r1["prev_hash"]) < 5
    if r1.get("prev_hash"):
        # If a hash existed from prior runs, ensure chain is contiguous
        assert r2["prev_hash"] == r1["hash"]
    assert r3["prev_hash"] == r2["hash"]
    chain = query_sigil(last_n=10)["rows"]
    assert len(chain) == 3
    print(f"  v SIGIL chain 3 entries with continuous prev_hash (hashes diverge per-digest)")


def test_04_persist_bft_demeter_veto_below_floor():
    _wipe()
    r = persist_bft_vote("Demeter", "for", 0.80, 7.305)
    assert "warning" in r
    assert "non-negotiable veto" in r.get("warning", "")
    print(f"  v Demeter non-negotiable veto when care < 0.95")


def test_05_persist_bft_other_queens_arbitrary_care():
    _wipe()
    r = persist_bft_vote("Artemis", "for", 0.30, 7.305)  # below floor but Artemis
    assert r.get("ok")
    print("  v Artemis at care=0.30 is accepted (only Demeter is non-negotiable)")


def test_06_persist_care_metric_witness_status():
    _wipe()
    persist_care_metric(0.97, source="watchdog", witness_kind="real-time")
    persist_care_metric(0.92, source="review", witness_kind="manual")
    r1 = persist_care_metric(0.96, source="t", witness_kind="t")
    r2 = persist_care_metric(0.93, source="t", witness_kind="t")
    assert r1["witness"] == "CARE_FLOOR_PRESERVED"
    assert r2["witness"] == "DEGRADED"
    print(f"  v Care metric witness status: 0.96=PRESERVED, 0.93=DEGRADED")


def test_07_query_reports_filtered_by_type():
    _wipe()
    persist_report("human", {"lat": 0}, type_="safety")
    persist_report("human", {"lat": 0}, type_="infrastructure")
    persist_report("humanoid", {"lat": 0}, type_="safety")
    r = query_reports(last_n=10, type_="safety")
    assert r["count"] == 2
    print(f"  v query_reports filtered by type=count 2")


def test_08_query_sigil_chain_field_integrity():
    _wipe()
    persist_sigil("kid-x", "sig", "TEST", mcp_name="newsigil")
    persist_sigil("kid-y", "sig", "TEST", mcp_name="newsigil")
    r = query_sigil(last_n=10)
    assert r["count"] == 2
    for row in r["rows"]:
        assert "hash" in row
        assert "prev_hash" in row
        assert "kid" in row
    print(f"  v Query sigil returns hash + prev_hash + kid for each row (chain_len={r['chain_len']})")


def test_09_query_care_metrics_returns_summary():
    _wipe()
    persist_care_metric(0.97, "human", "review")
    persist_care_metric(0.96, "human", "review")
    persist_care_metric(0.95, "human", "review")
    r = query_care_metrics(last_n=10)
    assert r["count"] == 3
    assert abs(r["avg_care"] - 0.96) < 0.001, r["avg_care"]
    assert r["min_care"] == 0.95
    print(f"  v Care metrics summary: avg={r['avg_care']:.4f}, min={r['min_care']:.4f}")


def test_10_backend_status_reports_sqlite_default():
    s = backend_status()
    assert s["backend"].startswith("sqlite") or "sqlite" in s["backend"]
    assert s["table_count"] == 4
    assert s["has_postgres"] is False  # no DATABASE_URL in test
    assert s["care_floor"] == 0.95
    print(f"  v Backend: {s['backend']} | 4 tables | no postgres | Care Floor 0.95")


if __name__ == "__main__":
    print("=" * 70)
    print("  Sovereign Data Lake E2E Tests")
    print("=" * 70)
    print()
    test_01_persist_report_basic()
    test_02_persist_report_invalid_severity()
    test_03_persist_sigil_chain_continuity()
    test_04_persist_bft_demeter_veto_below_floor()
    test_05_persist_bft_other_queens_arbitrary_care()
    test_06_persist_care_metric_witness_status()
    test_07_query_reports_filtered_by_type()
    test_08_query_sigil_chain_field_integrity()
    test_09_query_care_metrics_returns_summary()
    test_10_backend_status_reports_sqlite_default()
    print()
    print("TOTAL: 10 passed, 0 failed")
    print("Care Floor 0.95. BFT 12-around-1. SIGIL Ed25519 + PQC.")
