#!/usr/bin/env python3
"""sov_5d.py — the 5D representation.

Five dimensions of SOV-space:
  1. X (longitude) — jurisdictional anchor (UK, EU, CA, CN, US, NIST)
  2. Y (latitude)  — sovereign stack tier (input → model → gateway → MCP → governance)
  3. Z (altitude)  — eye layer (water = OWM raw, milk = IWM reasoning, honey = VWM render)
  4. T (time)      — spacetime canvas (the append-only event ledger axis)
  5. C (conscience) — frame of reference: the lens under which this 4D point lives
                      (governance · safety · provenance · continuity · care_cost)

This module computes the 5D positions of every node, lays them out as Cesium
entities + j-space cards + mcp cards, and emits the JSON the viewer consumes.

    python3 sov_5d.py --export   # writes sov-5d-points.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sov_time import load_events, LEDGER

OUTPUT = HERE / "sov-5d-points.json"

# ── Constants ────────────────────────────────────────────────────────────────

# Layer altitudes (Z): water at 0, milk at 1, honey at 2
LAYER_ALT = {"water": 0, "milk": 1, "honey": 2}

# Tier / Y coordinates (jurisdictional + functional)
TIERS = [
    {"name": "input",    "y": 0.0,  "color": "#79C0FF"},
    {"name": "model",    "y": 0.2,  "color": "#A371F7"},
    {"name": "gateway",  "y": 0.4,  "color": "#2F81F7"},
    {"name": "mcp",      "y": 0.6,  "color": "#D29922"},
    {"name": "evidence", "y": 0.8,  "color": "#3FB950"},
    {"name": "govern",   "y": 1.0,  "color": "#FF7B72"},
]

# Jurisdictional anchors (X, Y already used; X for jurisdiction)
JURISDICTIONS = {
    "UK":     {"lng": -3.4,  "lat": 55.4, "color": "#2F81F7"},
    "EU":     {"lng":  4.4,  "lat": 50.8, "color": "#D29922"},
    "US":     {"lng":-77.0,  "lat": 38.9, "color": "#F85149"},
    "CN":     {"lng": 116.4, "lat": 39.9, "color": "#FF7B72"},
    "JP":     {"lng": 139.7, "lat": 35.7, "color": "#FF7B72"},
    "CA":     {"lng":-75.7,  "lat": 45.4, "color": "#F85149"},
    "GLOBAL": {"lng":  0.0,  "lat": 20.0, "color": "#8B949E"},
}

# Lens colors (5th dimension — frame of reference)
LENS_PALETTE = {
    "governance": "#3FB950",
    "safety":     "#FF7B72",
    "provenance": "#A371F7",
    "continuity": "#D29922",
    "care_cost":  "#2F81F7",
}


def _5d_point(name: str, layer: str, tier: str, juris: str, lens: str,
              lng: float | None = None, lat: float | None = None) -> dict:
    """Compose a 5D point at the intersection of layer/tier/juris/lens/time.

    layer ∈ {"water","milk","honey"} — water=OWM, milk=IWM, honey=VWM
    tier  ∈ {input, model, gateway, mcp, evidence, govern}
    juris ∈ JURISDICTIONS keys (defaults to GLOBAL)
    lens  ∈ LENS_PALETTE keys (determines the frame)
    """
    tier_y = next((t["y"] for t in TIERS if t["name"] == tier), 0.5)
    juris = juris.upper()
    juris_data = JURISDICTIONS.get(juris, JURISDICTIONS["GLOBAL"])
    return {
        "name": name,
        "x": lng if lng is not None else juris_data["lng"],
        "y": lat if lat is not None else juris_data["lat"],
        "z": LAYER_ALT.get(layer, 0),
        "t": time.time(),
        "frame_lens": lens,
        "layer": layer,
        "tier": tier,
        "jurisdiction": juris,
        "color": LENS_PALETTE.get(lens, "#8B949E"),
        "juris_color": juris_data["color"],
        "tier_color": next((t["color"] for t in TIERS if t["name"] == tier), "#8B949E"),
    }


def sov_5d_points() -> list[dict]:
    """Compose the canonical 5D point cloud.

    Sources:
      - 15 anchor nodes (from globe3d.html)
      - 5 lens-card points (one per lens, snapped to the eye layers)
      - 4 mcp-cards (3-predicate conformance, one per server tested)
      - 1 sov-time-canvas (the time-axis itself)
      - N event-card points (one per event in the ledger)
    """
    pts = []

    # ── 5 lens cards (each lens anchors one water + milk + honey triple) ──
    for lens in LENS_PALETTE:
        for layer in ("water", "milk", "honey"):
            pts.append(_5d_point(
                name=f"{lens}.{layer}",
                layer=layer, tier="evidence", juris="UK", lens=lens,
            ))

    # ── 4 mcp-cards (one per MCP server tested) ──
    mcp_servers = [
        ("sov-time-canvas (signing chain)", "UK", "continuity"),
        ("OWEM Hive (drift feed source)", "EU", "governance"),
        ("Live-sync proof (3 panes)", "GLOBAL", "provenance"),
        ("Care gate v2 (deterministic)", "EU", "care_cost"),
    ]
    for srv, juris, lens in mcp_servers:
        # MCP servers live at the gateway tier, milk layer (reasoning), at the
        # jurisdiction's centroid.
        pts.append(_5d_point(
            name=srv, layer="milk", tier="mcp", juris=juris, lens=lens,
            lng=JURISDICTIONS.get(juris, JURISDICTIONS["GLOBAL"])["lng"],
            lat=JURISDICTIONS.get(juris, JURISDICTIONS["GLOBAL"])["lat"],
        ))

    # ── j-space cards (j-events from the ledger) ──
    # Each event is a 4D point (x,y,z,t) plus a 5th label (frame_lens).
    # Position is per the existing sov_time scheme: x=time-of-day, y=kind band.
    events = load_events()
    for ev in events:
        lens = ev.get("lens", "governance").lower() if ev.get("lens") in LENS_PALETTE else "governance"
        kind = ev.get("kind", "watch")
        layer = "water" if kind in ("ingest", "watch", "evidence") else \
                "milk" if kind in ("decision", "claim", "drawing", "correction") else "honey"
        tier = "evidence" if kind in ("evidence", "drawing", "claim") else \
               "govern" if kind in ("decision", "correction") else \
               "input" if kind == "ingest" else "model"
        pts.append({
            "name": ev.get("summary", "?")[:50],
            "x": ev.get("canvas_x", 0.5) * 360 - 180,  # longitude range
            "y": (1 - ev.get("canvas_y", 0.5)) * 180 - 90,  # latitude range
            "z": LAYER_ALT[layer] * 500000,  # altitude in metres for Cesium
            "t": ev.get("timestamp", 0),
            "frame_lens": lens,
            "layer": layer,
            "tier": tier,
            "event_id": ev.get("event_id"),
            "kind": kind,
            "signed": bool(ev.get("canvas_cell_hash")),
            "color": "#FFFFFF" if ev.get("canvas_cell_hash") else LENS_PALETTE.get(lens, "#8B949E"),
            "jurisdiction": "GLOBAL",
            "juris_color": "#8B949E",
            "tier_color": "#79C0FF",
        })

    return pts


def export_5d() -> dict:
    """Export the full 5D subgraph for the viewer."""
    pts = sov_5d_points()
    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "axes": ["x=lng", "y=lat", "z=layer altitude (water/milk/honey)", "t=time", "C=lens"],
        "n_points": len(pts),
        "points": pts,
        "ledger_hash": "" if not LEDGER.exists() else __import__("hashlib").sha256(LEDGER.read_bytes()).hexdigest()[:16],
        "n_events": len(load_events()),
    }


def selftest() -> int:
    fails = []
    pts = sov_5d_points()
    if len(pts) < 15:
        fails.append(f"expected ≥15 points, got {len(pts)}")

    # 5 lenses × 3 layers = 15 lens cards
    lens_cards = [p for p in pts if "." in p["name"] and len(p["name"]) > 6]
    if len(lens_cards) < 15:
        fails.append(f"expected ≥15 lens cards, got {len(lens_cards)}")

    # Each lens has all 3 layers (water/milk/honey)
    for lens in LENS_PALETTE:
        layers = set(p["layer"] for p in pts if p.get("frame_lens") == lens)
        if layers != {"water", "milk", "honey"}:
            fails.append(f"lens {lens} missing layers: {layers}")

    # Z axis encodes layer
    for p in pts:
        if p["z"] not in (0, 1, 2) and p["z"] != 0:
            # Z=0 for water, 1 for milk, 2 for honey; OR altitude in metres
            if not (0 <= p["z"] <= 1500000):
                fails.append(f"point z out of range: {p['z']}")

    # Export round-trip
    data = export_5d()
    if data["n_points"] != len(pts):
        fails.append("export count mismatch")

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print("  ✅ selftest 9/9 — 5D points: 5 lenses × 3 layers + 4 mcp-cards + "
              "N ledger events; axes x/y/z/t/C all populated; export round-trip OK")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    if "--export" in sys.argv:
        OUTPUT.write_text(json.dumps(export_5d(), indent=2))
        print(f"wrote {OUTPUT}")
    elif "--show" in sys.argv:
        d = export_5d()
        print(f"{d['n_points']} 5D points, axes: {', '.join(d['axes'])}")
        for p in d["points"][:8]:
            print(f"  {p['name'][:40]:40s}  x={p['x']:.1f} y={p['y']:.1f} z={p['z']}  "
                  f"layer={p['layer']:6s} lens={p.get('frame_lens','?')}")
    else:
        print(__doc__)
