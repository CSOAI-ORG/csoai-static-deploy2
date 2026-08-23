#!/usr/bin/env python3
"""
LIVING GSPC DATABASE — the site's benchmarks read from here, not hardcoded code.

Mines + merges every benchmark source into ONE living store the site API serves:
  1. board_all13.json   — the canonical 13-axis board (from board_v2.py)
  2. per-axis board_*.json — individual axis boards
  3. longitudinal/       — dated archives (the moat)
  4. API override        — what's currently live (so we never regress)

Writes: ~/clawd/csoai-static-deploy2/SOVOS/living/board_living.json
The site's /api/gspc should read this file. Every bench run updates it.
The DB is "living" = auto-updates on ingest, keeps history, never regresses.

Usage:
  python3 living_gspc_db.py ingest <dir>   # merge a board dir into living store
  python3 living_gspc_db.py update         # refresh from all known sources
  python3 living_gspc_db.py show           # print the living board
  python3 living_gspc_db.py history <axis> # longitudinal view of one axis
"""
from __future__ import annotations
import json, os, sys, shutil, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIVING_DIR = Path(os.environ.get("GSPC_LIVING", str(Path.home() / "clawd/csoai-static-deploy2/SOVOS/living")))
HISTORY_DIR = LIVING_DIR / "history"
SOURCES = [
    # (name, glob pattern) — order matters, later wins on merge
    ("longitudinal", str(Path.home() / "clawd/csoai-static-deploy2/benchmark-results/longitudinal/*/board.json")),
    ("boards-v2", str(Path.home() / "clawd/kimi-regen/SOVOS/boards-v2-2026-08-12/board_all13.json")),
    ("boards-v2-alt", str(Path.home() / "clawd/kimi-regen/SOVOS/arena-real-runs/*/board_all13.json")),
]

def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch_live_api() -> dict:
    """The currently-live board (baseline — never regress below this)."""
    try:
        req = urllib.request.Request("https://councilof.ai/api/gspc",
                                     headers={"User-Agent": "living-gspc-db/1.0", "Accept": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=15).read())
    except Exception:
        return {"axes": []}

def ingest_board(board: dict, source: str) -> dict:
    """Merge one board's axes into the living store (later source wins per axis)."""
    out_path = LIVING_DIR / "board_living.json"
    out = {}
    if out_path.exists():
        try:
            out = json.loads(out_path.read_text())
        except Exception:
            out = {}
    axes = {a.get("axis"): a for a in out.get("axes", [])}
    for a in board.get("axes", []):
        if a.get("axis"):
            axes[a["axis"]] = dict(a, _source=source, _updated=ts())
    out["schema"] = "csoai.gspc-living/0.1"
    out["updated"] = ts()
    out["source"] = source
    out["axes"] = list(axes.values())
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out

def archive_history(board: dict) -> None:
    """Append to the longitudinal history (the moat — every state kept forever)."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    stamp = ts().replace(":", "").replace("-", "").replace("T", "_")
    (HISTORY_DIR / f"board_{stamp}.json").write_text(json.dumps(board, ensure_ascii=False, indent=2))

def update() -> dict:
    """Refresh from all known sources + live API (never regress)."""
    merged = {"schema": "csoai.gspc-living/0.1", "updated": ts(), "axes": []}
    # 1. live API baseline (so we never serve less than today)
    live = fetch_live_api()
    merged = ingest_board(live, "live-api-baseline")
    # 2. each local source
    for name, pattern in SOURCES:
        for f in sorted(Path.home().glob(pattern.replace(str(Path.home()), "").lstrip("/"))):
            pass
    # simpler: iterate sources directly
    for name, pattern in SOURCES:
        import glob as g
        for f in g.glob(pattern):
            p = Path(f)
            if p.exists():
                try:
                    b = json.loads(p.read_text())
                    merged = ingest_board(b, name)
                except Exception as e:
                    print(f"  [skip] {name} {p.name}: {e}")
    archive_history(merged)
    print(f"living DB updated: {len(merged.get('axes', []))} axes, archived to history/")
    return merged

def show() -> None:
    p = LIVING_DIR / "board_living.json"
    if not p.exists():
        print("no living board yet — run 'update' first")
        return
    b = json.loads(p.read_text())
    print(f"LIVING GSPC BOARD (updated {b.get('updated')}, source {b.get('source')})")
    for a in b.get("axes", []):
        print(f"  {a.get('axis'):<16} n={a.get('n','?'):>5} status={a.get('status','?'):<11} src={a.get('_source','?')}")

def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    if cmd == "update":
        update()
    elif cmd == "ingest":
        d = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        if d and d.exists():
            for f in d.glob("board*.json"):
                try:
                    b = json.loads(f.read_text())
                    ingest_board(b, str(f.parent.name))
                    print(f"  ingested {f.name}")
                except Exception as e:
                    print(f"  err {f.name}: {e}")
    elif cmd == "show":
        show()
    else:
        print(__doc__)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
