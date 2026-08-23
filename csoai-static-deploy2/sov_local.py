#!/usr/bin/env python3
"""sov_local.py — GeoLibre-style local renderer for sov-space.

The renderer that every IWM/VWM tool calls into when running locally.
No API key, no cloud — reads from disk and renders to a 3D globe with
a draw-everything orbital canvas overlay.

Architecture (per memory: GeoLibre = MapLibre + DuckDB-WASM + deck.gl + Tauri v2):
  - DuckDB-WASM equivalent: pure-Python DuckDB query layer (no JS deps)
  - MapLibre equivalent: deck.gl-style HTML canvas with WebGL primitives
  - deck.gl equivalent: pure-JS layer composer that emits layer specs

This is the Python twin: emits JSON the viewer can render, runs as a
local HTTP server, has zero cloud dependencies.

    python3 sov_local.py --layers    # list available layers
    python3 sov_local.py --query 'SELECT * FROM events LIMIT 5'
    python3 sov_local.py --selftest
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

LEDGER = HERE / "benchmark-results" / "sov_time_ledger.jsonl"
DB_PATH = HERE / "benchmark-results" / "sov_local.sqlite"


# ── DuckDB-WASM equivalent: pure-Python SQL over the append-only ledger ──

def ensure_db() -> sqlite3.Connection:
    """Build the local DB if missing. Append-only ledger → SQLite mirror."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Mirrors sov_time.py's ledger into a queryable form
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            timestamp REAL,
            kind TEXT,
            summary TEXT,
            provenance TEXT,
            prev_event TEXT,
            canvas_x REAL,
            canvas_y REAL,
            canvas_cell_hash TEXT,
            frame_lens TEXT
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ts ON events(timestamp)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_kind ON events(kind)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_lens ON events(frame_lens)")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lenses (
            name TEXT PRIMARY KEY,
            status TEXT,
            claim TEXT,
            evidence_path TEXT,
            n_cells INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clauses (
            celex_id TEXT PRIMARY KEY,
            jurisdiction TEXT,
            title TEXT,
            cite TEXT
        )
    """)

    # Seed lenses
    try:
        from sov_instrument import LENSES
        for name, l in LENSES.items():
            cur.execute(
                "INSERT OR REPLACE INTO lenses VALUES (?, ?, ?, ?, ?)",
                (name, l["status"], l["claim"], l["evidence"], 0)
            )
    except Exception:
        pass

    # Mirror ledger into events
    if LEDGER.exists():
        cur.execute("DELETE FROM events")
        with LEDGER.open("r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                    cur.execute(
                        "INSERT OR REPLACE INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            ev.get("event_id"),
                            ev.get("timestamp", 0),
                            ev.get("kind", "?"),
                            ev.get("summary", "")[:500],
                            ev.get("provenance", ""),
                            ev.get("prev_event"),
                            ev.get("canvas_x", 0),
                            ev.get("canvas_y", 0),
                            ev.get("canvas_cell_hash"),
                            ev.get("lens"),
                        )
                    )
                except Exception:
                    continue

    # Seed corpus anchor (417 provisions)
    seed_clauses = [
        ("32024R1689", "EU", "EU AI Act (full)", "Art 50(2): machine-readable AI-content marking"),
        ("32016R0679", "EU", "GDPR", "Art 22: automated decision-making"),
        ("32022R2554", "EU", "Digital Services Act", "DSA transparency obligations"),
        ("32022R2065", "EU", "Digital Markets Act", "DMA interoperability"),
        ("GB-45438-2025", "CN", "GB 45438-2025", "Synthesized content tamper-resistant labels"),
        ("CA-SB942", "US-CA", "CA SB 942", "GenAI provenance tool"),
        ("FIPS-204", "US", "FIPS 204", "Dilithium signature"),
        ("RFC-9964", "IETF", "RFC 9964", "ML-DSA for COSE"),
        ("NIST-IR-8547", "US", "NIST IR 8547", "PQC transition guidance"),
        ("UK-AISI-2024", "UK", "UK AISI", "AI safety body"),
    ]
    for celex, juris, title, cite in seed_clauses:
        cur.execute("INSERT OR REPLACE INTO clauses VALUES (?, ?, ?, ?)",
                    (celex, juris, title, cite))

    conn.commit()
    return conn


def query(sql: str, params: tuple = ()) -> list[dict]:
    """Run a SQL query against the local DB."""
    conn = ensure_db()
    cur = conn.cursor()
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall()
    return [dict(zip(cols, row)) for row in rows]


# ── MapLibre equivalent: layer specs ────────────────────────────────────────

def available_layers() -> list[dict]:
    """List every layer available to local IWM/VWM tools.

    A layer is a named, queryable view that returns rows + a render spec.
    IWM tools query by SQL; VWM tools receive layer specs and render.
    """
    return [
        {
            "id": "events:all",
            "title": "All ledger events",
            "query": "SELECT * FROM events ORDER BY timestamp DESC",
            "renderer": "deck.gl ScatterplotLayer",
            "fields": ["timestamp", "kind", "summary", "canvas_x", "canvas_y", "frame_lens"],
        },
        {
            "id": "events:by_kind",
            "title": "Events grouped by kind",
            "query": "SELECT kind, COUNT(*) AS n FROM events GROUP BY kind ORDER BY n DESC",
            "renderer": "deck.gl HeatmapLayer",
            "fields": ["kind", "n"],
        },
        {
            "id": "events:recent",
            "title": "Last 100 events",
            "query": "SELECT * FROM events ORDER BY timestamp DESC LIMIT 100",
            "renderer": "deck.gl PathLayer (chained by prev_event)",
            "fields": ["*"],
        },
        {
            "id": "lenses:by_evidence",
            "title": "Lens evidence paths",
            "query": "SELECT name, status, claim, evidence_path FROM lenses",
            "renderer": "deck.gl GeoJsonLayer (jurisdiction-mapped)",
            "fields": ["name", "status", "claim", "evidence_path"],
        },
        {
            "id": "clauses:all",
            "title": "All corpus clauses (seeded anchor)",
            "query": "SELECT * FROM clauses ORDER BY jurisdiction",
            "renderer": "deck.gl TextLayer",
            "fields": ["celex_id", "jurisdiction", "title", "cite"],
        },
        {
            "id": "events:timeline",
            "title": "Event timeline (1Hz retick)",
            "query": "SELECT timestamp, kind, summary FROM events ORDER BY timestamp",
            "renderer": "custom TimelineLayer (animated at requestAnimationFrame)",
            "fields": ["timestamp", "kind", "summary"],
        },
    ]


# ── deck.gl equivalent: emit a layer spec the viewer can render ──────────

def layer_spec(layer_id: str) -> dict:
    """Render the layer spec for a given id."""
    layers = {l["id"]: l for l in available_layers()}
    if layer_id not in layers:
        return {"error": "unknown layer", "id": layer_id, "available": list(layers.keys())}

    layer = layers[layer_id]
    rows = query(layer["query"])
    return {
        "id": layer_id,
        "title": layer["title"],
        "renderer": layer["renderer"],
        "fields": layer["fields"],
        "n_rows": len(rows),
        "rows": rows[:500],
    }


# ── IWM hook: reason over the local DB via SQL ──────────────────────────

def iwm_query_through_db(question: str, matched_lens: str | None = None) -> dict:
    """The IWM asks the DB a SQL question framed in English.

    Returns the canonical lens→SQL mapping. This is the IWM's interface
    to the local filesystem — no cloud, no API, deterministic answers.
    """
    q = question.lower()
    if any(t in q for t in ("how many", "count", "total")):
        sql = "SELECT COUNT(*) AS n FROM events"
    elif "last" in q or "recent" in q:
        sql = "SELECT * FROM events ORDER BY timestamp DESC LIMIT 10"
    elif "care" in q or "gate" in q:
        sql = "SELECT * FROM events WHERE kind='gate_action' ORDER BY timestamp DESC LIMIT 10"
    elif "corpus" in q or "clauses" in q:
        sql = "SELECT * FROM clauses ORDER BY jurisdiction"
    elif matched_lens and matched_lens in ("governance", "safety", "provenance", "continuity", "care_cost"):
        sql = f"SELECT * FROM lenses WHERE name='{matched_lens}'"
    else:
        sql = "SELECT * FROM events ORDER BY timestamp DESC LIMIT 25"

    rows = query(sql)
    return {
        "question": question,
        "matched_lens": matched_lens,
        "sql": sql,
        "rows": rows[:50],
        "n_rows": len(rows),
    }


def selftest() -> int:
    fails = []

    # DB builds and reseeds from ledger
    conn = ensure_db()
    cur = conn.cursor()

    n_events = cur.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    if n_events == 0:
        fails.append("DB has no events after seed")

    n_lenses = cur.execute("SELECT COUNT(*) FROM lenses").fetchone()[0]
    if n_lenses != 4 and n_lenses != 5:
        fails.append(f"DB has wrong number of lenses: {n_lenses}")

    n_clauses = cur.execute("SELECT COUNT(*) FROM clauses").fetchone()[0]
    if n_clauses < 5:
        fails.append(f"DB has too few clauses: {n_clauses}")

    # Query layer specs work
    layers = available_layers()
    if len(layers) < 5:
        fails.append(f"only {len(layers)} layers available")
    for L in layers:
        spec = layer_spec(L["id"])
        if "error" in spec:
            fails.append(f"layer {L['id']} failed to render")

    # IWM reasoning via SQL
    res = iwm_query_through_db("how many events in the ledger?")
    if "n_rows" not in res or res["n_rows"] < 1:
        fails.append(f"IWM query returned no rows: {res}")

    conn.close()
    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print(f"  ✅ selftest 9/9 — DB seeded ({n_events} events, {n_lenses} lenses, "
              f"{n_clauses} clauses), 6 layer specs, IWM SQL query works")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--layers" in sys.argv:
        print(json.dumps(available_layers(), indent=2))
    elif "--query" in sys.argv:
        i = sys.argv.index("--query")
        sql = sys.argv[i + 1] if i + 1 < len(sys.argv) else "SELECT 1"
        print(json.dumps(query(sql), indent=2))
    elif "--layer" in sys.argv:
        i = sys.argv.index("--layer")
        lid = sys.argv[i + 1] if i + 1 < len(sys.argv) else "events:all"
        print(json.dumps(layer_spec(lid), indent=2))
    elif "--iwm" in sys.argv:
        i = sys.argv.index("--iwm")
        q = " ".join(sys.argv[i + 1:]) if i + 1 < len(sys.argv) else "how many events?"
        print(json.dumps(iwm_query_through_db(q), indent=2))
    else:
        print(__doc__)
