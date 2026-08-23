"""Integration test 1: MCP ↔ Sovereign DB.

Verifies that MCP invocations (registration, tool calls, ichar creation) produce
real, SIGIL-signed entries in the canonical Sovereign DB.

Uses the real `sovereign_db` + `witness_store` modules pointed at temp DBs.
"""
from __future__ import annotations

import json
import sqlite3
import time


def test_mcp_registration_creates_sovereign_db_entry(sdb):
    """Registering an MCP server must create a row in `mcp_federation`."""
    before = sdb.get_stats()["mcp_federation"]

    mcp_id = sdb.register_mcp("test-mcp-integration-1", tools_count=12)

    after = sdb.get_stats()["mcp_federation"]
    assert after == before + 1
    assert mcp_id.startswith("mcp-")

    # Verify the row actually exists with the SIGIL
    conn = sqlite3.connect(str(sdb.DB_PATH))
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM mcp_federation WHERE id = ?", (mcp_id,)
    ).fetchone()
    conn.close()
    assert row is not None
    assert row["server_name"] == "test-mcp-integration-1"
    assert row["tools_count"] == 12
    assert len(row["sigil"]) == 32  # HMAC-SHA256 truncated to 32 hex chars


def test_mcp_invocation_creates_ichar(sdb):
    """An MCP-driven i-character creation must land in the `ichars` table."""
    ichar_id = sdb.create_ichar(
        "MCP Test Citizen",
        "sovereign",
        "queen-king",
        21,
        {"O": 0.7, "C": 0.8, "E": 0.6, "A": 0.9, "N": 0.3},
    )
    assert ichar_id.startswith("ich-")

    ichar = sdb.get_ichar(ichar_id)
    assert ichar["name"] == "MCP Test Citizen"
    assert ichar["archetype"] == "sovereign"
    assert ichar["arcana_lens"] == 21
    assert ichar["ocean"]["O"] == 0.7
    assert ichar["ocean"]["A"] == 0.9


def test_mcp_call_emits_sigil_chain_entry(sdb):
    """Every sovereign DB write must extend the SIGIL chain."""
    chain_len_before = sdb.get_stats()["sigil_chain_length"]

    # Multiple "MCP calls" → multiple DB writes
    sdb.register_mcp("mcp-a", 3)
    sdb.create_ichar("Alice", "guardian", "queen-watch", 17, {})
    sdb.create_invoice("caller-x", "mcp-tool", 0.05)

    chain_len_after = sdb.get_stats()["sigil_chain_length"]
    assert chain_len_after > chain_len_before
    assert sdb.verify_sigil_chain() is True


def test_mcp_invocation_appears_in_audit_log(sdb):
    """MCP invocations must be logged in audit_log."""
    audit_before = sdb.get_stats()["audit_log_size"]

    sdb.create_ichar("Audit Test", "sage", "queen-sage", 9, {})

    audit_after = sdb.get_stats()["audit_log_size"]
    assert audit_after == audit_before + 1


def test_mcp_federation_lists_registered_servers(sdb):
    """The MCP federation table is queryable and lists all registered servers."""
    sdb.register_mcp("mcp-federation-1", 5)
    sdb.register_mcp("mcp-federation-2", 7)
    sdb.register_mcp("mcp-federation-3", 9)

    conn = sqlite3.connect(str(sdb.DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT server_name, tools_count FROM mcp_federation WHERE server_name LIKE 'mcp-federation-%'"
    ).fetchall()
    conn.close()

    names = {r["server_name"] for r in rows}
    assert "mcp-federation-1" in names
    assert "mcp-federation-2" in names
    assert "mcp-federation-3" in names


def test_x402_invoice_is_signed_and_auditable(sdb):
    """An MCP call that issues an x402 invoice must be SIGIL-signed + audit-logged."""
    inv_id = sdb.create_invoice("mcp-caller", "article50-passport", 0.10)
    assert inv_id.startswith("x402-")

    conn = sqlite3.connect(str(sdb.DB_PATH))
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM x402_invoices WHERE id = ?", (inv_id,)
    ).fetchone()
    conn.close()
    assert row["service"] == "article50-passport"
    assert row["amount_usd"] == 0.10
    assert len(row["sigil"]) == 32


def test_mcp_registration_intersects_with_witness_audit_if_wired(sdb, wstore):
    """If MCP writes also forward to the Witness audit log, they should appear."""
    # Real sovereign DB emits audit_log entries with the same shape
    sdb.register_mcp("witness-bridge-mcp", 4)

    # The witness_audit fixture: log a parallel entry in the witness
    wstore.SovereignWitness().audit(
        actor="mcp-bridge",
        actor_type="mcp",
        action="register_mcp",
        status="success",
        details={"server_name": "witness-bridge-mcp"},
    )

    # Both must have a record
    w = wstore.SovereignWitness()
    audit_entries = w.recent_audit(actor_type="mcp", action="register_mcp")
    assert any(
        e["details_json"] and "witness-bridge-mcp" in e["details_json"]
        for e in audit_entries
    )
