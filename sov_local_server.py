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
                       iwm_query_through_db, ensure_db, DB_PATH)
from sov_live import live_query
from sov_wifi_sensing import sense_once as wifi_sense, route_to_ledger as wifi_route
from sov_snooper import one_shot_scan as snoop_scan
from sov_time import render_canvas
from sov_zoom import render as zoom_render
from sov_sync import ledger_summary
from sov_fluid import LivingMemory
from sov_honey_unify import (list_sources, list_ollama_models, list_hf_models,
                              list_chatml_triples, route_active, ingest_all,
                              get_bloodline)
from sov_spawn import (TIERS as SOUL_TIERS, spawn as soul_spawn, grow as soul_grow,
                       list_souls, swarms_status as soul_status,
                       inherit_routes as soul_inherit_routes)
from sov_swarm import (BACKENDS as SWARM_BACKENDS, list_backends as swarm_backends,
                      alloc_for_tier as swarm_alloc, tick as swarm_tick_now)
from sov_portal_data import portal as get_portal
from sov_ingest_all import audit_producers as producers_audit, ingest_all as producers_ingest
from sov_e2e_overnight import run_overnight, selftest as overnight_selftest


def _backfill_honey_once():
    """Ensure every ledger event has a row in the honey mirror.

    Run once on server boot. Idempotent: re-runs are no-ops for rows
    that already exist.
    """
    import hashlib, sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS honey (
            event_id TEXT PRIMARY KEY,
            timestamp REAL,
            kind TEXT,
            summary TEXT,
            provenance TEXT,
            seq INTEGER,
            signature TEXT,
            lens TEXT,
            canvas_x REAL,
            canvas_y REAL
        )
    """)
    from sov_time import load_events
    events = load_events()
    existing = {r[0] for r in cur.execute("SELECT event_id FROM honey").fetchall()}
    for ev in events:
        eid = ev.get("event_id")
        if eid in existing:
            continue
        cell = {
            "event_id": eid,
            "prev": ev.get("prev_event"),
            "ts": ev.get("timestamp", 0),
            "kind": ev.get("kind"),
            "summary": ev.get("summary"),
            "prov": ev.get("provenance"),
        }
        cch = hashlib.sha256(json.dumps(cell, sort_keys=True).encode()).hexdigest()
        cur.execute(
            "INSERT OR IGNORE INTO honey VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (eid, ev.get("timestamp", 0), ev.get("kind"),
             (ev.get("summary") or "")[:1000], ev.get("provenance", ""),
             0, cch, ev.get("lens"), ev.get("canvas_x", 0), ev.get("canvas_y", 0))
        )
    conn.commit()
    n_db = cur.execute("SELECT COUNT(*) FROM honey").fetchone()[0]
    n_led = len(events)
    conn.close()
    if n_db != n_led:
        print(f"  honey mirror drift: db={n_db}, ledger={n_led}", file=__import__("sys").stderr)
    return {"honey": n_db, "ledger": n_led, "drift": n_db - n_led}

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

        # ─── Live multi-model query (creates NEW honey) ───
        elif path == '/api/live':
            q = self._qs('q') or "What is the EU AI Act?"
            try:
                result = live_query(q)
                self._respond_json(result)
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)

        # ─── WiFi sensing (Layer 0 perception) ───
        elif path == '/api/wifi/sense':
            try:
                presence = wifi_sense()
                routed = wifi_route(presence)
                self._respond_json({"presence": presence, "routed": routed})
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)

        # ─── PC snooper — every activity becomes honey KB ───
        elif path == '/api/snoop/scan':
            try:
                result = snoop_scan()
                self._respond_json(result)
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)

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

        # ─── End-to-end test endpoint (proves the full pipeline is consistent) ───
        elif path == '/api/e2e':
            from sov_e2e import e2e_full_cycle
            try:
                self._respond_json(e2e_full_cycle())
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)
        elif path == '/api/e2e/routes':
            # E2E check for 8-route sovereignty system
            try:
                from e2e_routes_sovereign import main as e2e_routes_main
                import io
                from contextlib import redirect_stdout
                buf = io.StringIO()
                with redirect_stdout(buf):
                    try:
                        e2e_routes_main()
                    except SystemExit:
                        pass
                output = buf.getvalue()
                self._respond_json({
                    "ok": "✓ E2E ROUTES PASS" in output,
                    "output": output[-2000:],
                    "routes": ["ollama", "huggingface", "chatml", "bloodline",
                              "training_data", "gpu_inventory", "tier0_routers", "kb_clauses"],
                })
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)
        elif path == '/api/honey/ingest':
            # Trigger KB ingest from a producer
            try:
                from sov_training_honey import (
                    route_ollama, route_huggingface, route_chatml, route_bloodline,
                    route_training_data, route_gpu_inventory, route_tier0_routers,
                    route_kb_clauses
                )
                route_fns = {
                    "ollama": route_ollama, "huggingface": route_huggingface,
                    "chatml": route_chatml, "bloodline": route_bloodline,
                    "training_data": route_training_data, "gpu_inventory": route_gpu_inventory,
                    "tier0_routers": route_tier0_routers, "kb_clauses": route_kb_clauses,
                }
                # Optional: ?producer=X to pick one route
                from urllib.parse import urlparse, parse_qs
                qs = parse_qs(urlparse(self.path).query)
                producer = qs.get("producer", [None])[0]
                if producer and producer in route_fns:
                    events = route_fns[producer]()
                    self._respond_json({"ok": True, "producer": producer, "events": len(events)})
                else:
                    # Run all
                    results = {}
                    for name, fn in route_fns.items():
                        try:
                            evts = fn()
                            results[name] = len(evts)
                        except Exception as e:
                            results[name] = f"error: {e}"
                    self._respond_json({"ok": True, "all_routes": results})
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)
        elif path == '/api/honey/downloads':
            # Run Downloads corpus miner
            try:
                import subprocess
                result = subprocess.run(
                    ["python3", "mine_downloads_corpus.py"],
                    capture_output=True, text=True, timeout=120,
                    cwd="/Users/nicholas/clawd/csoai-static-deploy2"
                )
                self._respond_json({
                    "ok": result.returncode == 0,
                    "stdout": result.stdout[-1000:],
                    "stderr": result.stderr[-500:] if result.stderr else "",
                })
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)
        elif path.startswith('/api/soul/') and '/grow' not in path:
            # Soul spawn or fetch
            uid = path[len('/api/soul/'):]
            existing = list_souls()
            match = next((s for s in existing if s["user_id"] == uid), None)
            if match:
                # Re-hydrate inherited routes (producers may have been added since spawn)
                if "inherited_routes" not in match:
                    match["inherited_routes"] = soul_inherit_routes()
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

        # ─── All producers → honey audit + ingest ───
        elif path == '/api/producers/audit':
            self._respond_json(producers_audit())
        elif path == '/api/producers/ingest':
            self._respond_json(producers_ingest())

        # ─── Overnight E2E runner ───
        elif path == '/api/overnight/run':
            try:
                self._respond_json(run_overnight())
            except Exception as e:
                self._respond_json({"error": str(e)}, 500)
        elif path == '/api/overnight/selftest':
            try:
                # Run all sub-seltests via the dedicated function
                ok, fails = [], []
                for mod in ("sov_ingest_all","sov_spawn","sov_swarm","sov_portal_data",
                            "sov_honey_unify","sov_fluid","sov_eyes","sov_route",
                            "sov_sync","sov_local","sov_5d","decision_ledger","sov_instrument"):
                    import subprocess
                    r = subprocess.run([sys.executable, str(HERE / f"{mod}.py"), "--selftest"],
                                       capture_output=True, text=True, timeout=30)
                    passed = r.returncode == 0 and "9/9" in r.stdout
                    (ok if passed else fails).append(mod)
                self._respond_json({"passed": ok, "failed": fails,
                                    "n_passed": len(ok), "n_total": len(ok) + len(fails)})
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
    _backfill_honey_once()  # bring mirror in sync with ledger
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
