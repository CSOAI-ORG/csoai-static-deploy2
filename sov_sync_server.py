#!/usr/bin/env python3
"""sov_sync_server.py — minimal HTTP server for live sync demo.

Serves sov-sync-proof.html and exposes two endpoints:
  GET /                  → sov-sync-proof.html
  GET /sov-time-canvas.svg → rendered SVG
  GET /sov-sync-summary.json → ledger summary
  GET /append-event      → append a random event to the ledger
"""
from __future__ import annotations

import http.server
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sov_time import record_event, render_canvas, LEDGER
from sov_sync import ledger_summary, ledger_hash

PORT = 8765


class SyncHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Strip query string
        path = self.path.split('?')[0]

        if path == '/' or path == '/sov-sync-proof.html':
            self._serve_file(HERE / 'sov-sync-proof.html', 'text/html')
        elif path == '/sov-space-vwm.html':
            self._serve_file(HERE / 'sov-space-vwm.html', 'text/html')
        elif path == '/sov-time-canvas.svg':
            body = render_canvas(window_seconds=86400).encode()
            self._respond(200, 'image/svg+xml', body)
        elif path == '/sov-sync-summary.json':
            body = json.dumps(ledger_summary()).encode()
            self._respond(200, 'application/json', body)
        elif path == '/append-event':
            kind = 'claim'
            if '?' in self.path and 'kind=' in self.path:
                qs = self.path.split('?', 1)[1]
                for kv in qs.split('&'):
                    if kv.startswith('kind='):
                        kind = kv.split('=', 1)[1]
            ev = record_event({
                'timestamp': time.time(),
                'kind': kind,
                'summary': f'live-sync demo: {kind} appended at {time.strftime("%H:%M:%S")} from {self.client_address[0]}',
                'provenance': 'sov_sync_server.py',
            })
            body = json.dumps(ev, indent=2).encode()
            self._respond(200, 'application/json', body)
        else:
            self._respond(404, 'text/plain', b'404')

    def _serve_file(self, path, content_type):
        try:
            body = path.read_bytes()
            self._respond(200, content_type, body)
        except FileNotFoundError:
            self._respond(404, 'text/plain', b'file not found')

    def _respond(self, status, content_type, body):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        # CORS for fetch from any origin
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Quiet — don't pollute terminal
        pass


if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', PORT), SyncHandler)
    print(f'╔══════════════════════════════════════════════════════════════╗')
    print(f'║ SOV-Space Live Sync Demo                                      ║')
    print(f'║ http://localhost:{PORT}/                                            ║')
    print(f'╚══════════════════════════════════════════════════════════════╝')
    print(f'Ledger: {LEDGER} ({LEDGER.stat().st_size if LEDGER.exists() else 0} bytes)')
    print(f'Hash:   {ledger_hash()[:16]}...')
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nshutting down')
        server.shutdown()
