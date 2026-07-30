#!/usr/bin/env python3
"""sov_local_server.py — the GeoLibre-style local server for the inner visualisation.

Mirrors GeoLibre's local-first stack in Python:
  DuckDB-WASM   → sqlite3 (in-memory + queryable, NO cloud)
  MapLibre      → HTML5 canvas + WebGL primitives via deck.gl CDN
  deck.gl       → layer specs emitted as JSON, rendered client-side
  Tauri v2      → replaced with: this Python server, stdlib only

Endpoint:
  GET /                       → sov-local-viewer.html (this screen)
  GET /sov-local-viewer.html  → same viewer
  GET /api/layers             → list available layers
  GET /api/layer/<id>         → render layer spec
  GET /api/query?sql=...      → run SQL
  GET /api/iwm?q=...          → IWM reasoning endpoint (returns matched lens + rows)
  GET /sov-time-canvas.svg    → render the spacetime canvas
  GET /sov-zoom/<level>.svg   → render a fractal zoom level
  GET /sov-sync-summary.json  → ledger hash + event count

Runs at http://localhost:8765 for the local inner-visualisation.
No API key, no cloud. Reads from disk only.
"""
from __future__ import annotations

import http.server
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sov_5d import export_5d
from sov_local import (available_layers, layer_spec, query,
                       iwm_query_through_db, ensure_db)
from sov_time import render_canvas
from sov_zoom import render as zoom_render
from sov_sync import ledger_summary
from sov_fluid import LivingMemory
from sov_honey_unify import (list_sources, list_ollama_models, list_hf_models,
                              list_chatml_triples, route_active, ingest_all,
                              get_bloodline)
from sov_spawn import (TIERS as SOUL_TIERS, spawn as soul_spawn, grow as soul_grow,
                       list_souls, swarms_status as soul_status)
from sov_swarm import (BACKENDS as SWARM_BACKENDS, list_backends as swarm_backends,
                      alloc_for_tier as swarm_alloc, tick as swarm_tick_now)
from sov_portal_data import portal as get_portal

PORT = 8766  # different port from sov_sync_server.py (8765)

# Reused across requests so we get a coherent swarm — but tick advances each poll
_FLUID = LivingMemory()
_FLUID_TICKED = 0


class LocalHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Most POSTs are mutations on soul/spawn — treat them like GETs here
        self.do_GET()

    def do_GET(self):
        path = self.path.split('?')[0]

        if path == '/' or path == '/sov-local-viewer.html':
            self._serve_file(HERE / 'sov-local-viewer.html', 'text/html')
        elif path == '/sov-fluid-viewer.html':
            self._serve_file(HERE / 'sov-fluid-viewer.html', 'text/html')
        elif path == '/sov-space-vwm.html':
            self._serve_file(HERE / 'sov-space-vwm.html', 'text/html')
        elif path == '/sov-three-eyes.html':
            self._serve_file(HERE / 'sov-three-eyes.html', 'text/html')
        elif path == '/sov-5d-engine.html':
            self._serve_file(HERE / 'sov-5d-engine.html', 'text/html')

        elif path == '/api/eyes':
            self._respond_json(self._three_eyes_snapshot())
        elif path == '/api/substrate':
            self._respond_json(self._substrate())

        elif path == '/api/layers':
            self._respond_json({"layers": available_layers()})
        elif path.startswith('/api/layer/'):
            lid = path[len('/api/layer/'):]
            self._respond_json(layer_spec(lid))
        elif path == '/api/query':
            sql = self._qs('sql') or "SELECT 1"
            try:
                self._respond_json({"sql": sql, "rows": query(sql)[:200]})
            except Exception as e:
                self._respond_json({"sql": sql, "error": str(e)}, 500)
        elif path == '/api/iwm':
            q = self._qs('q') or "how many events?"
            self._respond_json(iwm_query_through_db(q))

        elif path == '/api/fluid':
            # Living-memory snapshot — caller may request 'tick' to advance
            advance = int(self._qs('tick') or '1')
            for _ in range(advance):
                _FLUID.tick()
                _FLUID_TICKED += 1
            self._respond_json(_FLUID.snapshot())
        elif path == '/api/fluid/zoom':
            nid = self._qs('id')
            if not nid:
                self._respond_json({"error": "missing id"}, 400)
                return
            self._respond_json(_FLUID.zoomed_inner(nid))
        elif path == '/api/inner':
            path_arg = self._qs('path')
            if not path_arg:
                self._respond_json({"error": "missing path"}, 400)
                return
            inner = self._load_inner_docstore(path_arg)
            self._respond_json(inner)
        elif path == '/api/tick':
            _FLUID.tick()
            _FLUID_TICKED += 1
            self._respond_json({"tick": _FLUID_TICKED, "snapshot": _FLUID.snapshot()})

        # ── Honey unification endpoints ──
        elif path == '/api/honey/sources':
            self._respond_json({"sources": list_sources()})
        elif path == '/api/honey/models':
            self._respond_json({
                "ollama": list_ollama_models()[:15],
                "huggingface": list_hf_models()[:10],
            })
        elif path == '/api/honey/route':
            self._respond_json(route_active())
        elif path == '/api/honey/ingest':
            self._respond_json(ingest_all())
        elif path == '/api/honey/bloodline':
            self._respond_json(get_bloodline())
        elif path == '/api/honey/chatml':
            n = int(self._qs('n') or '20')
            self._respond_json({"triples": list_chatml_triples(n=n)})

        # ─── End-user soul + swarm + portal endpoints ───
        elif path.startswith('/api/soul/') and path.endswith('/grow/' + (path.split('/grow/')[-1] if '/grow/' in path else '')):
            # Soul grow
            parts = path.split('/')
            uid = parts[3]
            tgt = int(parts[5]) if len(parts) > 5 and parts[5].isdigit() else 1
            self._respond_json(soul_grow(uid, tgt))
        elif path.startswith('/api/soul/') and '/grow' not in path:
            # Soul spawn or fetch
            uid = path[len('/api/soul/'):]
            existing = list_souls()
            match = next((s for s in existing if s["user_id"] == uid), None)
            if match:
                self._respond_json({"soul": match, "spawned": False})
            else:
                try:
                    self._respond_json(soul_spawn(uid))
                except Exception as e:
                    self._respond_json({"error": str(e)}, 500)
        elif path == '/api/souls/list':
            self._respond_json({"souls": list_souls()})
        elif path == '/api/souls/summary':
            self._respond_json(soul_status())
        elif path == '/api/swarm/backends':
            self._respond_json(swarm_backends())
        elif path == '/api/swarm/tick':
            self._respond_json(swarm_tick_now())
        elif path.startswith('/api/swarm/alloc/'):
            tier = int(path[len('/api/swarm/alloc/'):]) if path[len('/api/swarm/alloc/'):].isdigit() else 2
            self._respond_json(swarm_alloc(tier))
        elif path.startswith('/api/portal/'):
            uid = path[len('/api/portal/'):]
            try:
                self._respond_json(get_portal(uid))
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)

        elif path == '/sov-time-canvas.svg':
            self._respond(200, 'image/svg+xml', render_canvas(window_seconds=86400).encode())
        elif path.startswith('/sov-zoom-') and path.endswith('.svg'):
            # sov-zoom-microsecond.svg?window=86400
            level = path[len('/sov-zoom-'):-len('.svg')]
            window = int(self._qs('window') or '86400')
            self._respond(200, 'image/svg+xml', zoom_render(zoom=level, window=window).encode())

        elif path == '/sov-sync-summary.json':
            self._respond_json(ledger_summary())
        elif path == '/sov-5d-points.json':
            self._respond_json(export_5d())
        elif path == '/drift-feed.json':
            # Re-emit drift via the public reader
            self._serve_file(HERE / 'drift-feed.json', 'application/json')

        else:
            self._respond(404, 'text/plain', b'404')

    def _qs(self, key: str) -> str | None:
        if '?' not in self.path:
            return None
        qs = self.path.split('?', 1)[1]
        for kv in qs.split('&'):
            if kv.startswith(f'{key}='):
                return kv[len(key) + 1:]
        return None

    def _three_eyes_snapshot(self) -> dict:
        # DB hits local sqlite for OWM facts
        conn = ensure_db()
        n_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        n_clauses = conn.execute("SELECT COUNT(*) FROM clauses").fetchone()[0]
        n_lenses = conn.execute("SELECT COUNT(*) FROM lenses").fetchone()[0]
        conn.close()

        return {
            "owm": {
                "role": "KNOWS — local sqlite + ledger + forest",
                "events": n_events,
                "clauses": n_clauses,
                "lenses": n_lenses,
            },
            "iwm": {
                "role": "DECIDES — 4 lenses on 1 engine, no train()",
                "lenses": {
                    "governance": "composed pipeline +6.63 [+1.05, +12.21], n=193",
                    "safety":     "1 of 4 axes resolved WITH the deterministic gate",
                    "provenance": "0/108 survive any transform, CI [0.0%, 24.2%]",
                    "continuity": "1 of 25 criteria pass — failing subject is US",
                    "care_cost":  "100% recall, 0% over-block on 55-item battery",
                },
            },
            "vwm": {
                "role": "RENDERS — local renderer, no cloud",
                "renderer": "GeoLibre-style (MapLibre + DuckDB-WASM + deck.gl)",
                "zoom_levels": ["microsecond", "second", "hour", "day", "year"],
            },
        }

    def _substrate(self) -> dict:
        s = ledger_summary()
        return {
            "ledger": s,
            "layers": [L["id"] for L in available_layers()],
            "ts": time.time(),
        }

    def _respond_json(self, data, status=200):
        self._respond(status, 'application/json', json.dumps(data, indent=2).encode())

    def _respond(self, status, content_type, body):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path: Path, content_type: str):
        try:
            body = path.read_bytes()
            self._respond(200, content_type, body)
        except FileNotFoundError:
            self._respond(404, 'text/plain', b'file not found')

    def _load_inner_docstore(self, path: str) -> dict:
        """Load inner content from a node's inner_ref path."""
        try:
            p = Path(path)
            if not p.exists():
                return {"error": f"path not found: {path}"}
            if p.suffix == ".py":
                lines = p.read_text().splitlines()
                return {
                    "type": "python_source",
                    "path": str(p),
                    "lines": len(lines),
                    "size": p.stat().st_size,
                    "preview": "\n".join(lines[:80]),
                }
            elif p.suffix == ".json":
                data = json.loads(p.read_text())
                return {
                    "type": "json_blob",
                    "path": str(p),
                    "size": p.stat().st_size,
                    "preview": json.dumps(data, indent=2)[:3000],
                }
            elif p.suffix == ".pyi" or p.suffix == ".txt":
                return {
                    "type": "text",
                    "path": str(p),
                    "size": p.stat().st_size,
                    "preview": p.read_text()[:3000],
                }
            else:
                return {
                    "type": "binary" if p.stat().st_size > 10_000 else "small",
                    "path": str(p),
                    "size": p.stat().st_size,
                }
        except Exception as e:
            return {"error": str(e)}

    def log_message(self, fmt, *args):
        # Quiet
        pass


if __name__ == '__main__':
    server = http.server.HTTPServer(('127.0.0.1', PORT), LocalHandler)
    ensure_db()  # pre-build
    print('╔══════════════════════════════════════════════════════════════╗')
    print('║ GeoLibre-style local server for SOV-space inner-visualisation ║')
    print(f'║ http://localhost:{PORT}/                                          ║')
    print('║ No cloud, no API key, no deps — pure stdlib + sqlite3       ║')
    print('╚══════════════════════════════════════════════════════════════╝')
    print(f'Layers: {len(available_layers())} | Engine: sqlite3 + HTML5 canvas')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nshutting down')
        server.shutdown()
