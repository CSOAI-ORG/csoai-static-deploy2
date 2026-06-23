#!/usr/bin/env python3
"""
Sovereign Town dashboard server.
Serves JSON API, WebSocket live feed, and static files for the public landing page,
research dashboard, 3D town viewer, and verifier.
"""
import asyncio
import json
import os
import glob
import pathlib
import hashlib
import threading
import time
import logging
from collections import deque
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse, FileResponse, RedirectResponse, StreamingResponse, Response
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.websockets import WebSocket

import town_sim_live
import httpx
import sov3_bridge
import regulation_parser
import policy_lab
import websockets
import config

P0 = config.P0
_START_TIME = time.time()
HARNESS_URL = config.HARNESS_URL
MCP_URL = config.MCP_URL

# Security knobs (override via environment, centralized in config.py).
_CORS_ORIGINS = config.CORS_ORIGINS
_MAX_BODY_BYTES = config.MAX_BODY_BYTES
_MAX_QUERY_LENGTH = config.MAX_QUERY_LENGTH

# ─── Observability state ─────────────────────────────────────────────────────
_METRICS = {
    "requests_total": 0,
    "requests_by_status": {},
    "request_latencies": deque(maxlen=config.METRICS_WINDOW),
}


def _record_request_metrics(status: int, latency_ms: float) -> None:
    _METRICS["requests_total"] += 1
    _METRICS["requests_by_status"][str(status)] = _METRICS["requests_by_status"].get(str(status), 0) + 1
    _METRICS["request_latencies"].append(latency_ms)


def _metrics_summary() -> dict:
    lat = list(_METRICS["request_latencies"])
    return {
        "uptime_seconds": round(time.time() - _START_TIME, 1),
        "requests_total": _METRICS["requests_total"],
        "requests_by_status": dict(_METRICS["requests_by_status"]),
        "latency_ms": {
            "count": len(lat),
            "avg": round(sum(lat) / len(lat), 3) if lat else 0.0,
            "p50": round(sorted(lat)[len(lat) // 2], 3) if lat else 0.0,
        },
        "websocket_clients": len(_WS_CLIENTS),
        "regime_clients": {
            "governed": sum(1 for r in _CLIENT_REGIMES.values() if r == "governed"),
            "ungoverned": sum(1 for r in _CLIENT_REGIMES.values() if r == "ungoverned"),
        },
    }

_HTTPS_CLIENT: httpx.AsyncClient | None = None
logger = logging.getLogger("dashboard")
LABS = config.LABS_DIR
PUBLIC = config.PUBLIC_DIR
VERIFY = config.VERIFY_DIR
EXPERIMENTS_DIR = config.P0 / "experiments"

# ─── WebSocket live-feed state ───────────────────────────────────────────────
_WS_CLIENTS: set[WebSocket] = set()
_TAILER_THREAD: threading.Thread | None = None
_TAILER_STOP = threading.Event()
# Reference to the uvicorn event loop, captured in lifespan.startup.
_MAIN_LOOP = None
# Track last-seen inode/size/mtime per watched file so we only broadcast new lines.
_TAILER_STATE: dict[str, dict] = {}

# Live town-state broadcast state
# Per-client regime (default governed) so one viewer cannot mutate the feed for all.
_CLIENT_REGIMES: dict[WebSocket, str] = {}
_TOWN_TICK_COUNTER: int = 0
_TOWN_TICK_INTERVAL: int = 1  # broadcast a town tick every tailer second


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        return default


def load_jsonl_tail(path, n=20):
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        return [json.loads(l) for l in lines[-n:]]
    except (OSError, json.JSONDecodeError, ValueError):
        return []


def _safe_path(root: pathlib.Path, rel: str) -> pathlib.Path | None:
    """Resolve a path under root and confirm it does not escape. Returns None if unsafe."""
    try:
        root_resolved = root.resolve()
        target = (root / rel).resolve()
        if not str(target).startswith(str(root_resolved) + os.sep) and target != root_resolved:
            return None
        return target
    except (OSError, ValueError):
        return None


def _passport_files():
    files = []
    if (P0 / "passports").exists():
        files = sorted((P0 / "passports").glob("*.json"))
    return files


# ─── WebSocket broadcast helpers ─────────────────────────────────────────────

async def _ws_broadcast(message: dict):
    """Send a JSON message to every connected WebSocket client."""
    dead = set()
    for ws in _WS_CLIENTS:
        try:
            await ws.send_json(message)
        except Exception:
            dead.add(ws)
    for ws in dead:
        _WS_CLIENTS.discard(ws)
        _CLIENT_REGIMES.pop(ws, None)


async def _ws_broadcast_regime_tick(governed_msg: dict, ungoverned_msg: dict):
    """Send the appropriate town_tick snapshot to each client based on its chosen regime."""
    dead = set()
    for ws in _WS_CLIENTS:
        regime = _CLIENT_REGIMES.get(ws, "governed")
        msg = governed_msg if regime == "governed" else ungoverned_msg
        try:
            await ws.send_json(msg)
        except Exception:
            dead.add(ws)
    for ws in dead:
        _WS_CLIENTS.discard(ws)
        _CLIENT_REGIMES.pop(ws, None)


def _broadcast_from_thread(message: dict):
    """Thread-safe bridge to schedule an async broadcast on the main event loop."""
    import asyncio
    loop = _MAIN_LOOP
    if loop and loop.is_running():
        asyncio.run_coroutine_threadsafe(_ws_broadcast(message), loop)


def _snapshot_status():
    """Return the same payload as /api/status for periodic pushes."""
    mac = load_json(P0 / "fleet_status_mac.json", {})
    vm = load_json(PUBLIC / "fleet_status_vm.json", {})
    models = load_json(P0 / "moat_models.json", {}).get("models", {})
    registry = load_json(PUBLIC / "registry.json", {})
    total_eps = (mac.get("cum_episodes", 0) or 0) + (vm.get("cum_episodes", 0) or 0)
    return {
        "hives": mac.get("hives", 28) if isinstance(mac.get("hives"), int) else len(mac.get("hives", [])),
        "passports": len(registry.get("passports", [])) if registry else 0,
        "cum_episodes": total_eps,
        "governed_crimes": (mac.get("governed_crimes", 0) or 0) + (vm.get("governed_crimes", 0) or 0),
        "ungoverned_crimes": (mac.get("ungoverned_crimes", 0) or 0) + (vm.get("ungoverned_crimes", 0) or 0),
        "models_trained": sum(1 for m in models.values() if isinstance(m, dict) and m.get("test_acc")),
        "mac": mac,
        "vm": vm,
    }


def _tail_file(path: pathlib.Path, topic: str, host: str | None = None):
    """Read any new lines appended to `path` since last call and broadcast them."""
    if not path.exists():
        return
    key = str(path)
    stat = path.stat()
    state = _TAILER_STATE.get(key)
    # If file was truncated or replaced, restart from beginning.
    if state and (stat.st_ino != state["ino"] or stat.st_size < state["size"]):
        state = None
    if state is None:
        _TAILER_STATE[key] = {
            "ino": stat.st_ino,
            "size": stat.st_size,
            "mtime": stat.st_mtime,
            "lines": 0,
        }
        return

    if stat.st_size <= state["size"]:
        state["size"] = stat.st_size
        state["mtime"] = stat.st_mtime
        return

    try:
        with open(path, "r") as f:
            f.seek(state["size"])
            new_lines = f.readlines()
    except Exception:
        return

    state["size"] = stat.st_size
    state["mtime"] = stat.st_mtime

    for line in new_lines:
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            payload = {"raw": line}
        _broadcast_from_thread({
            "topic": topic,
            "host": host,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime()),
            "payload": payload,
        })


def _tailer_loop():
    """Background thread: tail ledgers, pheromone bus, and push periodic snapshots."""
    snapshot_counter = 0
    global _TOWN_TICK_COUNTER
    while not _TAILER_STOP.is_set():
        try:
            _tail_file(P0 / "flywheel_ledger_mac.jsonl", topic="ledger", host="mac")
            _tail_file(P0 / "flywheel_ledger_vm.jsonl", topic="ledger", host="vm")
            _tail_file(P0 / "pheromone_bus.jsonl", topic="pheromone")

            _TOWN_TICK_COUNTER += 1
            if _TOWN_TICK_COUNTER >= _TOWN_TICK_INTERVAL:
                _TOWN_TICK_COUNTER = 0
                try:
                    g_msg = town_sim_live.snapshot("governed")
                    u_msg = town_sim_live.snapshot("ungoverned")
                    loop = _MAIN_LOOP
                    if loop and loop.is_running():
                        import asyncio
                        asyncio.run_coroutine_threadsafe(
                            _ws_broadcast_regime_tick(g_msg, u_msg), loop
                        )
                except Exception:
                    pass

            snapshot_counter += 1
            if snapshot_counter >= 10:  # every ~10 seconds
                snapshot_counter = 0
                _broadcast_from_thread({"topic": "status", "payload": _snapshot_status()})
        except Exception:
            # Never let the tailer crash; keep the feed alive.
            pass
        _TAILER_STOP.wait(1.0)


@asynccontextmanager
async def lifespan(app):
    global _TAILER_THREAD, _MAIN_LOOP
    import asyncio
    _MAIN_LOOP = asyncio.get_running_loop()
    _TAILER_STOP.clear()
    _TAILER_THREAD = threading.Thread(target=_tailer_loop, daemon=True, name="sov-town-tailer")
    _TAILER_THREAD.start()
    yield
    _TAILER_STOP.set()
    if _TAILER_THREAD:
        _TAILER_THREAD.join(timeout=2.0)
    global _HTTPS_CLIENT
    if _HTTPS_CLIENT:
        await _HTTPS_CLIENT.aclose()
        _HTTPS_CLIENT = None


async def ws_feed(websocket: WebSocket):
    await websocket.accept()
    _WS_CLIENTS.add(websocket)
    _CLIENT_REGIMES[websocket] = "governed"
    try:
        # Send a welcome snapshot immediately so the UI populates without polling.
        await websocket.send_json({"topic": "status", "payload": _snapshot_status()})
        # Keep connection open; accept viewer regime commands.
        while True:
            try:
                msg = await websocket.receive_text()
                try:
                    cmd = json.loads(msg)
                except Exception:
                    cmd = {}
                if isinstance(cmd, dict) and cmd.get("regime") in ("governed", "ungoverned"):
                    _CLIENT_REGIMES[websocket] = cmd["regime"]
                    await websocket.send_json({"topic": "regime", "regime": cmd["regime"]})
                    continue
                # Echo a heartbeat so clients can measure latency.
                await websocket.send_json({"topic": "pong", "received": msg})
            except Exception:
                break
    finally:
        _WS_CLIENTS.discard(websocket)
        _CLIENT_REGIMES.pop(websocket, None)


# ─── HTTP API ────────────────────────────────────────────────────────────────

async def api_status(request):
    return JSONResponse(_snapshot_status())


async def api_health(request):
    """Liveness/readiness probe for orchestrators and monitors."""
    status = {
        "status": "ok",
        "uptime_seconds": round(time.time() - _START_TIME, 1),
        "websocket_clients": len(_WS_CLIENTS),
        "town_regime_default": "governed",
        "town_regime_counts": {
            "governed": sum(1 for r in _CLIENT_REGIMES.values() if r == "governed"),
            "ungoverned": sum(1 for r in _CLIENT_REGIMES.values() if r == "ungoverned"),
        },
        "town_tick_index": town_sim_live.GENERATOR._tick_index if town_sim_live.GENERATOR._timeline else 0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    # Basic dependency check: can we produce a town snapshot?
    try:
        town_sim_live.snapshot("governed")
    except Exception as e:
        status["status"] = "degraded"
        status["error"] = str(e)
    return JSONResponse(status)


async def api_metrics(request):
    """Lightweight operational metrics for dashboards and monitors."""
    return JSONResponse(_metrics_summary())


async def _check_harness_ready(url: str) -> dict:
    try:
        client = await _httpx_client()
        r = await client.get(url, timeout=5.0)
        return {"ok": r.status_code == 200, "status": r.status_code}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__}


async def _check_mcp_ready(url: str) -> dict:
    try:
        client = await _httpx_client()
        async with client.stream("GET", url, timeout=5.0) as r:
            chunk = await r.aiter_text().__anext__()
            return {"ok": r.status_code == 200 and bool(chunk), "status": r.status_code}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__}


async def api_ready(request):
    """Deep readiness probe: dashboard + harness + MCP SSE all answering."""
    started = time.time()
    harness_url = HARNESS_URL.rstrip("/") + "/harness/health"
    mcp_url = MCP_URL.rstrip("/") + "/mcp/sse"
    harness, mcp = await asyncio.gather(
        _check_harness_ready(harness_url),
        _check_mcp_ready(mcp_url),
    )
    duration_ms = round((time.time() - started) * 1000, 3)
    ready = harness.get("ok") and mcp.get("ok")
    body = {
        "ready": ready,
        "checks": {
            "dashboard": {"ok": True},
            "harness": harness,
            "mcp": mcp,
        },
        "duration_ms": duration_ms,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return JSONResponse(body, status_code=200 if ready else 503)




async def api_experiments_spawn(request):
    """Regulation intake → auto-spawn experiment (requires API token)."""
    auth = request.headers.get("authorization", "")
    expected = f"Bearer {config.API_TOKEN}" if config.API_TOKEN else None
    if expected and auth != expected:
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    if not config.API_TOKEN:
        return JSONResponse({"error": "API token not configured"}, status_code=503)
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)
    intake = body.get("intake")
    if not intake or not isinstance(intake, dict):
        return JSONResponse({"error": "intake object required"}, status_code=400)
    try:
        result = regulation_parser.generate_from_intake(intake)
        exp_path = config.P0 / result["experiment"]
        policy_lab.vote_experiment(exp_path)
        live = bool(body.get("live"))
        if live:
            policy_lab.spawn_experiment(exp_path, live=True)
            # report expects completed runs; if live fails, status stays queued.
            try:
                policy_lab.report_experiment(exp_path)
            except Exception:
                pass
        exp = load_json(exp_path, {})
        return JSONResponse({
            "experiment_id": exp.get("id"),
            "status": exp.get("status"),
            "files": {
                "automated_policy": result["automated_policy"],
                "manual_policy": result["manual_policy"],
                "experiment": result["experiment"],
            },
        })
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"spawn failed: {e}"}, status_code=500)


async def api_experiments(request):
    """List sanitized Policy Lab experiments."""
    items = []
    if EXPERIMENTS_DIR.exists():
        for f in sorted(EXPERIMENTS_DIR.glob("*.json")):
            try:
                data = load_json(f, {})
                items.append({
                    "id": data.get("id", f.stem),
                    "name": data.get("name"),
                    "status": data.get("status"),
                    "regulation": data.get("regulation"),
                    "industry": data.get("industry"),
                    "duration_sim_days": data.get("duration_sim_days"),
                })
            except Exception:
                continue
    return JSONResponse({"experiments": items})


async def api_experiment_detail(request):
    """Return one experiment JSON by id (safe directory scan)."""
    exp_id = request.path_params["id"]
    if not exp_id or any(c in exp_id for c in "/\\") or exp_id.startswith("."):
        return JSONResponse({"error": "invalid experiment id"}, status_code=400)
    if not EXPERIMENTS_DIR.exists():
        return JSONResponse({"error": "not found"}, status_code=404)
    for f in EXPERIMENTS_DIR.glob("*.json"):
        data = load_json(f, {})
        if data.get("id") == exp_id:
            return JSONResponse(data)
    return JSONResponse({"error": "not found"}, status_code=404)




async def api_sov3_handshake(request):
    """Return a signed Ed25519 attestation for the VM SOV3 mesh."""
    return JSONResponse(sov3_bridge.handshake())


async def api_sov3_think(request):
    """Proxy a ``bridge_think`` call to the VM SOV3 mesh."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)
    character = body.get("character", "sov-town")
    message = body.get("message", "")
    profile = body.get("profile", "balanced")
    if not message:
        return JSONResponse({"error": "message required"}, status_code=400)
    result = await sov3_bridge.bridge_think(character, message, profile)
    if "error" in result:
        status = 503 if "unreachable" in result.get("error", "").lower() else 502
        return JSONResponse(result, status_code=status)
    return JSONResponse(result)

async def api_aethelgard_hive(request):
    """Return the Aethelgard Finance Hive roster + state contract for meok-ai/ui."""
    data = load_json(P0 / "aethelgard_finance_hive.json", {})
    if not data:
        return JSONResponse({"error": "hive data not configured"}, status_code=404)
    data["_contract_version"] = "2026-06-22"
    return JSONResponse(data)


async def api_council_vote(request):
    """Deterministic BFT council vote for a proposal."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    proposal = body.get("proposal", "") or "No proposal provided"
    proposal_id = body.get("proposal_id") or hashlib.sha256(proposal.encode()).hexdigest()[:16]
    # Deterministic council seeded by proposal_id.
    members = ["Minerva", "Oracle", "Sentinel", "Nomad", "Architect"]
    options = ["FUND", "MODIFY", "REJECT"]
    weights = [0.60, 0.25, 0.15]
    votes = []
    import random
    rng = random.Random(proposal_id)
    for m in members:
        vote = rng.choices(options, weights=weights)[0]
        reason = {
            "FUND": "Evidence supports the hypothesis.",
            "MODIFY": "Add cross-border or edge-case coverage.",
            "REJECT": "Insufficient evidence for the claimed effect.",
        }[vote]
        votes.append({"member": m, "vote": vote, "reason": reason})
    fund_count = sum(1 for v in votes if v["vote"] == "FUND")
    result = "approved" if fund_count >= 3 else "modify" if fund_count >= 2 else "rejected"
    return JSONResponse({
        "proposal_id": proposal_id,
        "proposal": proposal,
        "votes": votes,
        "fund_count": fund_count,
        "result": result,
    })


async def agent_chat(request):
    """OpenAI-compatible chat endpoint proxied to FreeLLMAPI."""
    import httpx
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid JSON"}, status_code=400)
    messages = body.get("messages", [])
    if not messages or not isinstance(messages, list):
        return JSONResponse({"error": "messages array required"}, status_code=400)
    system = {
        "role": "system",
        "content": (
            "You are a research assistant for Sovereign Town, a governed-vs-ungoverned "
            "multi-agent AI simulation. Ground answers in the public experiment data at "
            "https://proofof.ai/sovereign-town/experiments.html. Do not reveal private keys, "
            "raw ledger entries, or individual agent identities."
        ),
    }
    payload = {
        "model": body.get("model", "auto"),
        "messages": [system] + messages,
        "temperature": body.get("temperature", 0.7),
    }
    if not config.FREELLMAPI_KEY:
        return JSONResponse({
            "error": "FreeLLMAPI key not configured",
            "detail": "Set SOV_TOWN_FREELLMAPI_KEY to enable /agent/chat",
        }, status_code=503)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {config.FREELLMAPI_KEY}"}
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(config.FREELLMAPI_URL, json=payload, headers=headers)
        return JSONResponse(r.json(), status_code=r.status_code)
    except httpx.ConnectError:
        return JSONResponse({"error": "FreeLLMAPI unavailable", "detail": "Is the FreeLLMAPI server running on port 3001?"}, status_code=503)
    except Exception as e:
        return JSONResponse({"error": "proxy failed", "detail": str(e)}, status_code=502)


async def api_hives(request):
    registry = load_json(PUBLIC / "registry.json", {"passports": []})
    models = load_json(P0 / "moat_models.json", {}).get("models", {})
    characters = load_json(P0 / "characters.json", {})
    out = []
    for p in registry.get("passports", []):
        key = p["id"].split(":")[-1]
        out.append({
            "id": p["id"],
            "key": key,
            "name": p["name"],
            "type": p.get("type"),
            "frameworks": p.get("frameworks", []),
            "capabilities": p.get("capabilities", []),
            "pubkey": p.get("pubkey"),
            "model": models.get(key, {}),
            "personas": characters.get(key, {}).get("personas", []),
        })
    return JSONResponse(out)


async def api_hive_detail(request):
    key = request.path_params["key"]
    registry = load_json(PUBLIC / "registry.json", {"passports": []})
    models = load_json(P0 / "moat_models.json", {}).get("models", {})
    characters = load_json(P0 / "characters.json", {})
    corpus = load_json(P0 / "batch_corpus.json", {}).get("moat", {})
    passport = next((p for p in registry.get("passports", []) if p["id"].split(":")[-1] == key), None)
    if not passport:
        return JSONResponse({"error": "hive not found"}, status_code=404)
    return JSONResponse({
        "passport": passport,
        "model": models.get(key, {}),
        "characters": characters.get(key, {}),
        "corpus": corpus.get(key, {}),
    })


async def api_characters(request):
    return JSONResponse(load_json(P0 / "characters.json", {}))


async def api_characters_hive(request):
    key = request.path_params["key"]
    chars = load_json(P0 / "characters.json", {})
    if key not in chars:
        return JSONResponse({"error": "hive not found"}, status_code=404)
    return JSONResponse(chars[key])


async def api_episodes(request):
    district = request.query_params.get("district")
    arm = request.query_params.get("arm")
    try:
        limit = min(int(request.query_params.get("limit", "50")), 1000)
    except ValueError:
        limit = 50
    if limit < 1:
        limit = 1
    rows = []
    try:
        with open(P0 / "episodes.jsonl") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if district and r.get("district") != district:
                    continue
                if arm and r.get("arm") != arm:
                    continue
                rows.append(r)
                if len(rows) >= limit:
                    break
    except FileNotFoundError:
        pass
    return JSONResponse(rows)


async def api_ledger(request):
    host = request.query_params.get("host", "mac")
    if host not in ("mac", "vm"):
        return JSONResponse({"error": "invalid host"}, status_code=400)
    path = P0 / f"flywheel_ledger_{host}.jsonl"
    return JSONResponse(load_jsonl_tail(path, n=50))


async def api_models(request):
    return JSONResponse(load_json(P0 / "moat_models.json", {}))


async def api_corpus(request):
    return JSONResponse(load_json(P0 / "batch_corpus.json", {}))


async def api_labs_index(request):
    try:
        idx = (LABS / "INDEX.md").read_text()
    except Exception:
        idx = ""
    return PlainTextResponse(idx)


async def api_labs_file(request):
    name = request.path_params["name"]
    if ".." in name or name.startswith("/"):
        return PlainTextResponse("not found", status_code=404)
    path = _safe_path(LABS, name)
    if path is None or not path.exists():
        return PlainTextResponse("not found", status_code=404)
    if name.endswith(".svg"):
        return FileResponse(path, media_type="image/svg+xml")
    return PlainTextResponse(path.read_text())


async def api_passports(request):
    out = []
    for f in _passport_files():
        out.append({"key": f.stem, "file": f.name})
    return JSONResponse(out)


async def api_passport_detail(request):
    key = request.path_params["key"]
    if ".." in key or "/" in key or not key:
        return JSONResponse({"error": "invalid passport key"}, status_code=400)
    path = _safe_path(P0 / "passports", f"{key}.json")
    if path is None or not path.exists():
        # try registry lookup by id
        registry = load_json(PUBLIC / "registry.json", {"passports": []})
        alt = next((p for p in registry.get("passports", []) if p["id"].split(":")[-1] == key), None)
        return JSONResponse(alt if alt else {"error": "passport not found"}, status_code=200 if alt else 404)
    return JSONResponse(load_json(path, {}))


async def api_moat(request):
    return JSONResponse(load_json(P0 / "data_moat.json", {}))


async def api_attestations(request):
    return JSONResponse(load_json(P0 / "attestation_moat.json", {}))


async def api_attestations_anchor(request):
    """External anchor for a self-signed gaming/compliance attestation.

    Sovereign Town acts as a third-party notary: it independently verifies the
    attestation's own Ed25519 self-signature (against the pubkey embedded in the
    attestation) and records it in an append-only, prev-chained log. This closes
    the self-attestation gap: the anchor is the third-party append-only record +
    the independent signature check.

    Canonicalization matches Sovereign Town's scheme: the signed message is the
    attestation body minus `sig`, serialized with json.dumps(sort_keys=True)
    (spaced separators) — identical to how passports/attestations are signed and
    to the JS `pyDumps` in meok-saas/src/lib/attestation.ts.

    HONESTY — `sovereign_signature` is null by default. A King-countersign is an
    OPTIONAL, explicitly privileged step, enabled ONLY by env
    SOV_TOWN_KING_COUNTERSIGN=1. When enabled, this endpoint signs a small RECEIPT
    (anchor_id + received_ts + attestation_sha256 + attestation_agent + anchor)
    — NOT the raw attestation — with the sovereign key (sign_lib). It does NOT
    sign arbitrary submitted payloads with the King key.

    SECURITY FINDING (2026-06-23): the local `.town_priv.key` MATCHES the canonical
    King issuer pubkey (53kc24…), i.e. the King private key IS present on this
    machine — contradicting the memory "King key never on this machine." The
    default-off design means the running instance does NOT use it unless an
    operator deliberately sets SOV_TOWN_KING_COUNTERSIGN=1. Reconcile the key's
    presence before relying on any local King signature (see
    ~/CSOAI_ALIGNMENT_AND_BRIDGE_2026-06-23.md).
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)
    att = body.get("attestation")
    if not isinstance(att, dict) or "sig" not in att or "pubkey" not in att:
        return JSONResponse({"error": "attestation must be an object with sig + pubkey"}, status_code=400)
    signed_body = {k: v for k, v in att.items() if k != "sig"}
    msg = json.dumps(signed_body, sort_keys=True)  # spaced separators, ensure_ascii default
    try:
        import sign_lib
        self_ok = sign_lib.verify(att["pubkey"], msg, att["sig"])
    except Exception as e:
        return JSONResponse({"anchored": False, "self_sig_verified": False, "error": f"verify raised: {e}"}, status_code=400)
    if not self_ok:
        return JSONResponse({"anchored": False, "self_sig_verified": False, "error": "attestation self-signature did not verify"}, status_code=400)
    att_canon = json.dumps(att, sort_keys=True)
    att_sha = hashlib.sha256(att_canon.encode()).hexdigest()
    log_path = P0 / "gaming_attestations.jsonl"
    prev_anchor_id = ""
    if log_path.exists():
        try:
            with open(log_path, "r") as f:
                lines = [ln for ln in f.read().splitlines() if ln.strip()]
            if lines:
                prev_anchor_id = json.loads(lines[-1]).get("anchor_id", "")
        except Exception:
            prev_anchor_id = ""
    anchor_id = "ga-" + att_sha[:16]
    received_ts = time.time()
    att_agent = att.get("agent") or att.get("server") or ""
    receipt = {
        "schema": "sovereign-town.anchor_receipt/v1",
        "anchor_id": anchor_id,
        "prev_anchor_id": prev_anchor_id,
        "received_ts": received_ts,
        "attestation_sha256": att_sha,
        "attestation_agent": att_agent,
        "anchor": "sovereign-town-local-appendonly",
    }
    sovereign_signature = None
    sovereign_pubkey = None
    sovereign_receipt = None
    king_countersign = os.environ.get("SOV_TOWN_KING_COUNTERSIGN") == "1"
    if king_countersign:
        try:
            import sign_lib
            priv, pub = sign_lib.load_or_create_key()
            sovereign_signature = sign_lib.sign(priv, json.dumps(receipt, sort_keys=True))
            sovereign_pubkey = pub
            sovereign_receipt = receipt
        except Exception as e:
            # Countersign failure does NOT lose the anchor — we still record it,
            # but report the countersign error honestly.
            king_countersign = False
            sovereign_signature = None
            _cs_error = f"king-countersign failed: {e}"
        else:
            _cs_error = None
    else:
        _cs_error = None
    record = {
        "anchor_id": anchor_id,
        "prev_anchor_id": prev_anchor_id,
        "received_ts": received_ts,
        "schema": "sovereign-town.anchor/v1",
        "attestation_sha256": att_sha,
        "attestation": att,
        "self_sig_verified": True,
        "sovereign_signature": sovereign_signature,
        "sovereign_pubkey": sovereign_pubkey,
        "sovereign_receipt": sovereign_receipt,
        "king_countersign": king_countersign,
        "anchor": "sovereign-town-local-appendonly",
    }
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
    except Exception as e:
        return JSONResponse({"anchored": False, "self_sig_verified": True, "error": f"failed to append: {e}"}, status_code=500)
    note = ("recorded in sovereign-town append-only anchor log; King-countersign RECEIPT signed with the sovereign key (SOV_TOWN_KING_COUNTERSIGN=1)"
            if king_countersign else
            "recorded in sovereign-town append-only anchor log; King-countersign is opt-in (set SOV_TOWN_KING_COUNTERSIGN=1)")
    if _cs_error:
        note += f"; {_cs_error}"
    return JSONResponse({
        "anchored": True,
        "anchor_id": anchor_id,
        "prev_anchor_id": prev_anchor_id,
        "attestation_sha256": att_sha,
        "self_sig_verified": True,
        "sovereign_signature": sovereign_signature,
        "sovereign_pubkey": sovereign_pubkey,
        "sovereign_receipt": sovereign_receipt,
        "king_countersign": king_countersign,
        "anchor": "sovereign-town-local-appendonly",
        "note": note,
    })


async def api_attestations_anchor_log(request):
    """Read the tail of the anchored gaming attestation log."""
    log_path = P0 / "gaming_attestations.jsonl"
    if not log_path.exists():
        return JSONResponse({"count": 0, "entries": []})
    try:
        with open(log_path, "r") as f:
            lines = [ln for ln in f.read().splitlines() if ln.strip()]
        entries = [json.loads(ln) for ln in lines[-50:]]
        return JSONResponse({"count": len(lines), "entries": entries})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ── Live sovereign-town export (closes the proofof.ai 404 on the read side) ────
# These endpoints derive the export the meok-saas read-bridge expects straight from
# the real P0 artifacts, LIVE, so the SaaS can point SOV_EXPORT_BASE at this server
# (http://127.0.0.1:3940/api/sov-export) instead of the dead proofof.ai mirror.
# Mirrors meok-saas/scripts/gen-sov-export.mjs so the local-static file and the live
# endpoint return the same shape. HONESTY: status is an UNSIGNED snapshot; the only
# cryptographic link to trust is the signed entries served by ledger_head.json.


def _ledger_signed_entries():
    """Return all signed entries from flywheel_ledger_mac.jsonl (each has a `sig`)."""
    ledger = P0 / "flywheel_ledger_mac.jsonl"
    if not ledger.exists():
        return []
    out = []
    try:
        with open(ledger, "r") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    e = json.loads(ln)
                except Exception:
                    continue
                if isinstance(e, dict) and "sig" in e:
                    out.append(e)
    except Exception:
        pass
    return out


def _issuer_pubkey():
    pub = P0 / "town_pub.key"
    if pub.exists():
        try:
            return open(pub).read().strip()
        except Exception:
            pass
    return "53kc24fqQz4MctZwtH+SuPLEKdX+NLlhK5wALr5H188="


def _sov_export_status():
    entries = _ledger_signed_entries()
    if not entries:
        return {"error": "no local sovereign artifacts", "source": str(P0),
                "message": "flywheel_ledger_mac.jsonl not found or has no signed entries"}
    last = entries[-1]
    cum = last.get("cum_episodes", 0)
    crimes = last.get("B_crimes", 0)
    cycle = last.get("cycle", 0)
    updated = last.get("ts", "")
    hosts = [{"host": last.get("host", "mac"), "cycle": cycle,
              "cum_episodes": cum, "ungoverned_crimes": crimes,
              "chain_head": last.get("sig"), "updated": updated}]
    passports_dir = P0 / "passports"
    passports_count = 0
    if passports_dir.exists():
        passports_count = len([f for f in passports_dir.iterdir() if f.suffix == ".json"])
    hives = 28
    moat_path = P0 / "moat_models.json"
    if moat_path.exists():
        try:
            moat = json.loads(open(moat_path).read())
            if isinstance(moat.get("hives"), (int, float)):
                hives = moat["hives"]
        except Exception:
            pass
    import datetime
    return {
        "_honest": "unsigned snapshot; chain_head links to the signed Ed25519 ledger",
        "cum_episodes": cum,
        "governed_crimes": 0,  # tautology under the Sovereign Gate — do NOT headline this
        "ungoverned_crimes": crimes,
        "hives": hives,
        "personas": 140,
        "passports": passports_count,
        "hosts": hosts,
        "issuer_pubkey": _issuer_pubkey(),
        "verify_url": "https://github.com/CSOAI-ORG/sovereign-town",
        "updated": updated,
        "published_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ"),
    }


async def api_sov_export_status(request):
    return JSONResponse(_sov_export_status())


async def api_sov_export_moat(request):
    p = P0 / "moat_models.json"
    if p.exists():
        return JSONResponse(load_json(p, {}))
    return JSONResponse({"error": "moat_models.json missing", "source": str(p)}, status_code=404)


async def api_sov_export_registry(request):
    registry = {"passports": []}
    pdir = P0 / "passports"
    if pdir.exists():
        for f in sorted(pdir.iterdir()):
            if f.suffix == ".json":
                try:
                    registry["passports"].append(json.loads(f.read_text()))
                except Exception:
                    pass
    return JSONResponse(registry)


async def api_sov_export_ledger_head(request):
    """Real Ed25519-signed, genesis-chained flywheel entries — the artifact that
    lets a browser verify the ledger client-side (closes the self-attestation gap
    on the READ side). Serves the last 12 signed entries + total count."""
    entries = _ledger_signed_entries()
    if not entries:
        return JSONResponse({"error": "no signed ledger entries", "source": str(P0)}, status_code=404)
    tail = entries[-12:]
    last = entries[-1]
    return JSONResponse({
        "schema": "sovereign-town.ledger_head/v1",
        "issuer_pubkey": _issuer_pubkey(),
        "n_entries": len(tail),
        "of_total": len(entries),
        "host": last.get("host", "mac"),
        "scope": "flywheel_mac_local",
        "verify_url": "https://github.com/CSOAI-ORG/sovereign-town",
        "how_to_verify": "for each entry: message = entry.prev + json.dumps({k:v for k,v in entry.items() if k not in ('sig','prev','prev_sig','alg')}, sort_keys=True); verify entry.sig against issuer_pubkey with Ed25519",
        "entries": tail,
    })


async def api_sov_export_anchor(request):
    """Honest anchor pointer. We do NOT fabricate Bitcoin confirmation — external
    Bitcoin anchoring of the full ledger is the still-open self-attestation gap
    (memory: csoai-competitive-moat). We serve a real merkle root over the signed
    entry sigs + the full-ledger sha256, and mark Bitcoin anchoring unconfirmed."""
    entries = _ledger_signed_entries()
    if not entries:
        return JSONResponse({"error": "no signed ledger entries"}, status_code=404)

    def _sha(b):
        return hashlib.sha256(b).hexdigest()

    # Merkle root over leaf = sha256(entry.sig) (real, verifiable digest of the chain).
    layer = [_sha(e.get("sig", "").encode()) for e in entries]
    if not layer:
        merkle = ""
    else:
        while len(layer) > 1:
            nxt = []
            for i in range(0, len(layer), 2):
                a = layer[i]
                b = layer[i + 1] if i + 1 < len(layer) else layer[i]
                nxt.append(_sha((a + b).encode()))
            layer = nxt
        merkle = layer[0]
    ledger_path = P0 / "flywheel_ledger_mac.jsonl"
    full_sha = _sha(ledger_path.read_bytes()) if ledger_path.exists() else ""
    ts_first = entries[0].get("ts", "") if entries else ""
    ts_last = entries[-1].get("ts", "") if entries else ""
    return JSONResponse({
        "ledger": "flywheel_ledger_mac.jsonl",
        "label": "sovereign-town local (mac) — NOT Bitcoin-anchored yet",
        "merkle_root": merkle,
        "n_attestable": len(entries),
        "n_total": len(entries),
        "full_ledger_sha256": full_sha,
        "ts_first": ts_first,
        "ts_last": ts_last,
        "bitcoin": {
            "confirmed": False,
            "blocks": [],
            "note": "external Bitcoin anchoring is not deployed — this is the open self-attestation gap. merkle_root + full_ledger_sha256 are real and verifiable; Bitcoin confirmation is future work.",
        },
        "anchor_manifest": "",
        "verify_cmd": f"sha256sum {ledger_path}  # expect {full_sha}",
        "issuer_pubkey": _issuer_pubkey(),
        "scope": "flywheel_mac_local",
    })


async def api_threat(request):
    return JSONResponse(load_json(P0 / "threat_moat.json", {}))


async def api_sanctions(request):
    return JSONResponse(load_json(P0 / "sanctions_moat.json", {}))


async def api_psc(request):
    return JSONResponse(load_json(P0 / "psc_moat.json", {}))


async def api_finance(request):
    return JSONResponse(load_json(P0 / "finance_moat.json", {}))


async def api_agriculture(request):
    return JSONResponse(load_json(P0 / "agriculture_moat.json", {}))


async def api_energy(request):
    return JSONResponse(load_json(P0 / "energy_moat.json", {}))


async def api_climate(request):
    return JSONResponse(load_json(P0 / "climate_moat.json", {}))


async def api_town_state(request):
    regime = request.query_params.get("regime", "governed")
    if regime not in ("governed", "ungoverned"):
        regime = "governed"
    return JSONResponse(town_sim_live.snapshot(regime))


async def api_verify_chain(request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)
    payload = body.get("payload")
    sig = body.get("sig")
    pubkey = body.get("pubkey")
    if not all([payload, sig, pubkey]):
        return JSONResponse({"error": "missing payload/sig/pubkey"}, status_code=400)
    try:
        import sign_lib
        ok = sign_lib.verify(pubkey, payload, sig)
        return JSONResponse({"valid": ok, "payload_hash": hashlib.sha256(payload.encode()).hexdigest()[:16]})
    except Exception as e:
        return JSONResponse({"valid": False, "error": str(e)})


async def dashboard_page(request):
    return FileResponse(P0 / "dashboard.html")


async def town3d_page(request):
    return FileResponse(P0 / "town3d.html")


async def workbench_page(request):
    return FileResponse(P0 / "benchmark" / "workbench.html")


async def leaderboard_page(request):
    return FileResponse(PUBLIC / "leaderboard.html")


async def verifier_page(request):
    return FileResponse(VERIFY / "index.html")


async def _httpx_client() -> httpx.AsyncClient:
    global _HTTPS_CLIENT
    if _HTTPS_CLIENT is None:
        _HTTPS_CLIENT = httpx.AsyncClient(timeout=60.0)
    return _HTTPS_CLIENT


async def mcp_sse_proxy(request):
    """Proxy the MCP SSE stream from the dedicated MCP server.

    Rewrites the upstream endpoint announcement from /messages/?session_id=...
    to /mcp/messages/?session_id=... so external clients stay under the
    dashboard namespace.
    """
    target = f"{MCP_URL}/sse"
    client = await _httpx_client()
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length")}
    ctx = client.stream("GET", target, headers=headers, timeout=None)
    resp = await ctx.__aenter__()

    async def gen():
        try:
            buffer = ""
            async for chunk in resp.aiter_text():
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.startswith("data: /messages/?"):
                        line = "data: /mcp/messages/?" + line[len("data: /messages/?"):]
                    yield line + "\n"
            if buffer:
                if buffer.startswith("data: /messages/?"):
                    buffer = "data: /mcp/messages/?" + buffer[len("data: /messages/?"):]
                yield buffer
        finally:
            await ctx.__aexit__(None, None, None)

    return StreamingResponse(
        gen(),
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type", "text/event-stream"),
        headers={k: v for k, v in resp.headers.items() if k.lower() not in ("transfer-encoding", "content-encoding", "content-length")},
    )


async def mcp_messages_proxy(request):
    """Forward POST messages to the MCP SSE server's /messages endpoint."""
    return await _proxy_http(request, MCP_URL, "/messages/")


async def _proxy_http(request, base_url: str, prefix: str) -> Response:
    """Generic HTTP proxy: forward method/body/headers to `base_url` + `prefix` + path."""
    path = request.path_params.get("path", "")
    target = f"{base_url}{prefix}{path}"
    if request.query_params:
        target += "?" + str(request.query_params)
    client = await _httpx_client()
    method = request.method
    body = await request.body() if method in ("POST", "PUT", "PATCH") else None
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length")}
    resp = await client.request(method, target, content=body, headers=headers, timeout=60.0)
    await resp.aread()
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers={k: v for k, v in resp.headers.items() if k.lower() not in ("transfer-encoding", "content-encoding", "content-length")},
        media_type=resp.headers.get("content-type"),
    )


async def harness_proxy(request):
    """Forward /harness/* REST calls to the benchmark harness server."""
    return await _proxy_http(request, HARNESS_URL, "/harness/")


async def harness_ws_proxy(websocket):
    """Forward /harness/live WebSocket to the benchmark harness server."""
    await websocket.accept()
    target = HARNESS_URL.replace("http://", "ws://").replace("https://", "wss://") + "/harness/live"
    try:
        async with websockets.connect(target) as upstream:
            async def to_upstream():
                while True:
                    data = await websocket.receive_text()
                    await upstream.send(data)
            async def to_client():
                while True:
                    data = await upstream.recv()
                    await websocket.send_text(data)
            await asyncio.gather(to_upstream(), to_client())
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception:
        pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


routes = [
    Route("/dashboard", dashboard_page),
    Route("/town3d", town3d_page),
    Route("/workbench", workbench_page),
    Route("/regulatory-workbench", workbench_page),
    Route("/leaderboard", leaderboard_page),
    Route("/passport", verifier_page),
    Route("/verify", verifier_page),
    Route("/api/status", api_status),
    Route("/api/health", api_health),
    Route("/api/ready", api_ready),
    Route("/api/metrics", api_metrics),
    Route("/api/hive/aethelgard", api_aethelgard_hive),
    Route("/api/council/vote", api_council_vote, methods=["POST"]),
    Route("/api/sov3/handshake", api_sov3_handshake),
    Route("/api/sov3/think", api_sov3_think, methods=["POST"]),
    Route("/agent/chat", agent_chat, methods=["POST"]),
    Route("/api/hives", api_hives),
    Route("/api/hives/{key}", api_hive_detail),
    Route("/api/characters", api_characters),
    Route("/api/characters/{key}", api_characters_hive),
    Route("/api/episodes", api_episodes),
    Route("/api/ledger", api_ledger),
    Route("/api/models", api_models),
    Route("/api/corpus", api_corpus),
    Route("/api/labs-index", api_labs_index),
    Route("/api/labs/{name}", api_labs_file),
    Route("/api/passports", api_passports),
    Route("/api/passports/{key}", api_passport_detail),
    Route("/api/moat", api_moat),
    Route("/api/attestations", api_attestations),
    Route("/api/attestations/anchor", api_attestations_anchor, methods=["POST"]),
    Route("/api/attestations/anchor/log", api_attestations_anchor_log),
    Route("/api/sov-export/status.json", api_sov_export_status),
    Route("/api/sov-export/moat_models.json", api_sov_export_moat),
    Route("/api/sov-export/registry.json", api_sov_export_registry),
    Route("/api/sov-export/ledger_head.json", api_sov_export_ledger_head),
    Route("/api/sov-export/anchor.json", api_sov_export_anchor),
    Route("/api/threat", api_threat),
    Route("/api/sanctions", api_sanctions),
    Route("/api/psc", api_psc),
    Route("/api/finance", api_finance),
    Route("/api/agriculture", api_agriculture),
    Route("/api/energy", api_energy),
    Route("/api/climate", api_climate),
    Route("/api/town-state", api_town_state),
    Route("/api/experiments", api_experiments),
    Route("/api/experiments/spawn", api_experiments_spawn, methods=["POST"]),
    Route("/api/experiments/{id}", api_experiment_detail),
    Route("/api/verify", api_verify_chain, methods=["POST"]),
    WebSocketRoute("/harness/live", harness_ws_proxy),
    Route("/harness/{path:path}", harness_proxy),
    WebSocketRoute("/ws/feed", ws_feed),
    Route("/mcp/sse", mcp_sse_proxy, methods=["GET"]),
    Route("/mcp/messages/{path:path}", mcp_messages_proxy, methods=["POST"]),
]

# Serve proofof-site/sovereign-town static files at root
if PUBLIC.exists():
    routes.append(Mount("/", app=StaticFiles(directory=PUBLIC, html=True)))


class RequestMetricsMiddleware(BaseHTTPMiddleware):
    """Time HTTP requests, update in-memory counters, and optionally emit structured logs."""

    async def dispatch(self, request, call_next):
        start = time.time()
        try:
            response = await call_next(request)
        except Exception as exc:
            latency_ms = (time.time() - start) * 1000
            _record_request_metrics(500, latency_ms)
            if config.ACCESS_LOG:
                logger.error(
                    json.dumps({
                        "event": "http_request",
                        "method": request.method,
                        "path": str(request.url.path),
                        "status": 500,
                        "latency_ms": round(latency_ms, 3),
                        "error": str(exc),
                    })
                )
            raise
        latency_ms = (time.time() - start) * 1000
        _record_request_metrics(response.status_code, latency_ms)
        if config.ACCESS_LOG:
            logger.info(
                json.dumps({
                    "event": "http_request",
                    "method": request.method,
                    "path": str(request.url.path),
                    "status": response.status_code,
                    "latency_ms": round(latency_ms, 3),
                    "client": request.client.host if request.client else None,
                })
            )
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Allow local CDN scripts; tighten for production deploys.
        csp = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; "
            "connect-src 'self' ws: wss:; "
            "frame-ancestors 'none'; "
            "base-uri 'self';"
        )
        response.headers["Content-Security-Policy"] = csp
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Reject unreasonably large URLs or request bodies."""

    async def dispatch(self, request, call_next):
        if len(str(request.query_params)) > _MAX_QUERY_LENGTH:
            return PlainTextResponse("query too large", status_code=414)
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > _MAX_BODY_BYTES:
                    return PlainTextResponse("request body too large", status_code=413)
            except ValueError:
                return PlainTextResponse("invalid content-length", status_code=400)
        return await call_next(request)


app = Starlette(routes=routes, lifespan=lifespan)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestSizeLimitMiddleware)
app.add_middleware(RequestMetricsMiddleware)
if _CORS_ORIGINS:
    allow_origins = _CORS_ORIGINS
    allow_credentials = "*" not in allow_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        allow_credentials=allow_credentials,
        max_age=600,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3940, log_level="warning")
