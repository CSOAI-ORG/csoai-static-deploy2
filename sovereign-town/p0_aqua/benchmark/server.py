#!/usr/bin/env python3
"""
Remote harness server for the Sovereign Town benchmark.

Runs on a separate port (default 3941) so external AI systems can participate
without downloading code. Supports:
  - POST /harness/run          -> run a policy and return signed metrics
  - WebSocket /harness/live    -> real-time policy-in-the-loop simulation
  - GET  /harness/leaderboard  -> aggregated signed run manifests
  - POST /harness/verify       -> verify a signed manifest
"""
from __future__ import annotations
import asyncio
import json
import os
import pathlib
import time
import sys
from collections import deque
from contextlib import asynccontextmanager
from typing import Any

from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse, PlainTextResponse
from starlette.routing import Route, WebSocketRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.websockets import WebSocket

import sim
import config
from benchmark import policy, world, metrics, ledger, scenarios, regulatory_crosswalk, aia as aia_module

P0 = config.P0
RUN_DIR = config.BENCHMARK_RUNS_DIR
RUN_DIR.mkdir(exist_ok=True)
_START_TIME = time.time()

_CORS_ORIGINS = config.CORS_ORIGINS
_MAX_BODY_BYTES = config.MAX_BODY_BYTES
_API_TOKEN = config.API_TOKEN
_PROTECTED_PATHS = {"/harness/run", "/harness/live"}

# ─── Observability state ─────────────────────────────────────────────────────
_HARNESS_METRICS = {
    "requests_total": 0,
    "requests_by_status": {},
    "request_latencies": deque(maxlen=config.METRICS_WINDOW),
}


def _record_harness_metrics(status: int, latency_ms: float) -> None:
    _HARNESS_METRICS["requests_total"] += 1
    _HARNESS_METRICS["requests_by_status"][str(status)] = _HARNESS_METRICS["requests_by_status"].get(str(status), 0) + 1
    _HARNESS_METRICS["request_latencies"].append(latency_ms)


def _harness_metrics_summary() -> dict:
    lat = list(_HARNESS_METRICS["request_latencies"])
    return {
        "uptime_seconds": round(time.time() - _START_TIME, 1),
        "requests_total": _HARNESS_METRICS["requests_total"],
        "requests_by_status": dict(_HARNESS_METRICS["requests_by_status"]),
        "latency_ms": {
            "count": len(lat),
            "avg": round(sum(lat) / len(lat), 3) if lat else 0.0,
            "p50": round(sorted(lat)[len(lat) // 2], 3) if lat else 0.0,
        },
        "manifests_last_hour": _manifest_count_last_hour(),
    }


def _ok(payload: Any) -> JSONResponse:
    return JSONResponse({"status": "ok", **payload})


def _err(message: str, code: int = 400) -> JSONResponse:
    return JSONResponse({"status": "error", "error": message}, status_code=code)


async def health(request):
    return _ok({
        "uptime_seconds": round(time.time() - _START_TIME, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    })


def _list_available_policies() -> list[str]:
    """Return built-in, AIA, and JSON-configurable policy names."""
    names = list(policy.BUILT_IN.keys()) + ["aia_required", "aia_auto"]
    policies_dir = config.P0 / "benchmark" / "policies"
    if policies_dir.exists():
        for f in policies_dir.glob("*.json"):
            names.append(f.stem)
    return sorted(set(names))


async def world_info(request):
    return _ok({
        "world": world.canonical_world(),
        "scenarios": scenarios.list_scenarios(),
        "policies": _list_available_policies(),
        "frameworks": {k: v["name"] for k, v in regulatory_crosswalk.FRAMEWORKS.items()},
        "actions": regulatory_crosswalk.ACTIONS,
    })


async def harness_metrics(request):
    """Operational metrics for the harness endpoint."""
    return _ok(_harness_metrics_summary())


def _load_policy_from_body(body: dict):
    """Instantiate a policy from request body: built-in name, rules, or AIAs."""
    if "rules" in body and isinstance(body["rules"], dict):
        return policy.RuleBasedPolicy(body["rules"])
    if "aias" in body and isinstance(body["aias"], list):
        fw = body.get("framework", "eu_ai_act")
        pol = aia_module.AIARequiredPolicy(framework=fw)
        pol.register_many(body["aias"])
        return pol
    return policy.load_policy(body.get("policy", "sovereign"))


async def run_benchmark(request):
    try:
        body = await request.json()
    except Exception:
        return _err("invalid JSON")

    scenario = body.get("scenario", "baseline")
    district = body.get("district", "aqua")
    seed = body.get("seed", 47)
    sign = body.get("sign", False)
    collect_states = body.get("collect_states", True)

    try:
        pol = _load_policy_from_body(body)
    except Exception as e:
        return _err(f"cannot load policy: {e}")

    try:
        run = world.run(
            seed=seed,
            policy=pol,
            scenario=scenario,
            district=district,
            sign=False,
            collect_states=collect_states,
        )
    except Exception as e:
        return _err(f"simulation failed: {e}", 500)

    scored = metrics.evaluate(run)
    result = {"run": run, "score": scored}

    if sign:
        try:
            manifest = ledger.sign_run(run)
            path = ledger.save_manifest(manifest, RUN_DIR)
            result["manifest"] = manifest
            result["manifest_path"] = str(path)
        except Exception as e:
            return _err(f"signing failed: {e}", 500)

    return _ok(result)


async def verify_manifest(request):
    try:
        body = await request.json()
    except Exception:
        return _err("invalid JSON")
    manifest = body.get("manifest") or body
    ok = ledger.verify_manifest(manifest)
    return _ok({"valid": ok, "id": manifest.get("id")})


async def workbench_page(request):
    return FileResponse(str(P0 / "benchmark" / "workbench.html"))


async def agent_card(request):
    return FileResponse(str(P0 / "benchmark" / "agent_card.json"), media_type="application/json")


async def run_detail(request):
    run_id = request.path_params.get("run_id", "")
    for path in RUN_DIR.glob("*.json"):
        try:
            m = ledger.load_manifest(path)
            if m.get("id") == run_id:
                return _ok({"manifest": m, "valid": ledger.verify_manifest(m)})
        except Exception:
            continue
    return _err("run not found", 404)


async def leaderboard(request):
    rows = []
    for path in sorted(RUN_DIR.glob("*.json")):
        try:
            m = ledger.load_manifest(path)
            rows.append({
                "id": m.get("id"),
                "policy": m.get("run", {}).get("policy"),
                "scenario": m.get("run", {}).get("scenario"),
                "district": m.get("run", {}).get("district"),
                "metrics": m.get("metrics", {}),
                "run_at": m.get("run", {}).get("run_at"),
                "valid": ledger.verify_manifest(m),
            })
        except Exception:
            continue
    rows.sort(key=lambda x: x["run_at"] or "", reverse=True)
    return _ok({"leaderboard": rows})


async def ws_live(websocket: WebSocket):
    """
    Real-time policy-in-the-loop simulation.

    Client sends {"policy": "sovereign", "scenario": "baseline", "district": "aqua", "seed": 47}
    Server streams one tick at a time:
      {"topic": "tick", "day": ..., "hour": ..., "observations": [...], "metrics": {...}}
    Client replies with decisions keyed by agent id:
      {"decisions": {"2": {"verdict": "deny", "reason": "..."}, ...}}
    """
    await websocket.accept()
    try:
        cfg_msg = await websocket.receive_text()
        cfg = json.loads(cfg_msg)
    except Exception as e:
        await websocket.send_json({"topic": "error", "error": f"bad config: {e}"})
        await websocket.close()
        return

    scenario = cfg.get("scenario", "baseline")
    district = cfg.get("district", "aqua")
    seed = cfg.get("seed", 47)

    try:
        pol = _load_policy_from_body(cfg)
    except Exception as e:
        await websocket.send_json({"topic": "error", "error": f"policy load failed: {e}"})
        await websocket.close()
        return

    # Run one arm synchronously; this yields tick_states.
    try:
        run = world.run(seed=seed, policy=pol, scenario=scenario, district=district,
                        collect_states=True)
    except Exception as e:
        await websocket.send_json({"topic": "error", "error": f"sim failed: {e}"})
        await websocket.close()
        return

    ticks = run.get("tick_states", [])
    if not ticks:
        await websocket.send_json({"topic": "error", "error": "no tick states"})
        await websocket.close()
        return

    # Bucket by tick (day, hour) and stream.
    grouped: dict[tuple[int, int], list[dict]] = {}
    for s in ticks:
        grouped.setdefault((s["day"], s["hour"]), []).append(s)

    sorted_ticks = sorted(grouped.items(), key=lambda kv: (kv[0][0], kv[0][1]))
    scored = metrics.evaluate(run)

    manifest_info = {}
    if cfg.get("sign"):
        try:
            manifest = ledger.sign_run(run)
            path = ledger.save_manifest(manifest, RUN_DIR)
            manifest_info = {"manifest_id": manifest.get("id"), "manifest_path": str(path)}
        except Exception as e:
            manifest_info = {"sign_error": str(e)}

    await websocket.send_json({"topic": "start", "total_ticks": len(sorted_ticks),
                               "score": scored, "policy": cfg.get("policy", "custom"), "scenario": scenario,
                               **manifest_info})

    tick_delay = float(cfg.get("tick_delay", 0.05))
    stop_event = asyncio.Event()

    async def read_commands():
        while not stop_event.is_set():
            try:
                msg = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
            except asyncio.TimeoutError:
                continue
            except Exception:
                break
            try:
                cmd = json.loads(msg)
                if cmd.get("stop"):
                    stop_event.set()
                    break
            except Exception:
                continue

    async def stream_ticks():
        for (day, hour), states in sorted_ticks:
            if stop_event.is_set():
                break
            observations = [_observation_from_state(s) for s in states]
            await websocket.send_json({
                "topic": "tick",
                "day": day,
                "hour": hour,
                "observations": observations,
            })
            if tick_delay > 0:
                await asyncio.sleep(tick_delay)
        stop_event.set()

    await asyncio.gather(read_commands(), stream_ticks())
    await websocket.send_json({"topic": "done", "score": scored, **manifest_info})
    await websocket.close()


def _observation_from_state(state: dict) -> dict:
    return {
        "agent_index": state.get("agent_index"),
        "agent_id": state.get("agent_id"),
        "name": state.get("name"),
        "archetype": state.get("archetype"),
        "intended_action": state.get("intended"),
        "executed_action": state.get("action"),
        "alive": state.get("alive"),
        "wallet": state.get("wallet"),
        "needs": state.get("needs"),
        "town": {
            "lawlessness": state.get("lawlessness"),
            "commons": state.get("commons"),
            "mean_trust": state.get("mean_trust"),
        },
        "classifications": regulatory_crosswalk.classify(state.get("action", "work")),
    }


@asynccontextmanager
async def lifespan(app):
    yield


routes = [
    Route("/workbench", workbench_page),
    Route("/harness/agent-card", agent_card),
    Route("/harness/runs/{run_id}", run_detail),
    Route("/harness/health", health),
    Route("/harness/world", world_info),
    Route("/harness/metrics", harness_metrics),
    Route("/harness/run", run_benchmark, methods=["POST"]),
    Route("/harness/verify", verify_manifest, methods=["POST"]),
    Route("/harness/leaderboard", leaderboard),
    WebSocketRoute("/harness/live", ws_live),
]


class RequestMetricsMiddleware(BaseHTTPMiddleware):
    """Time HTTP requests, update in-memory counters, and optionally emit structured logs."""

    async def dispatch(self, request, call_next):
        start = time.time()
        try:
            response = await call_next(request)
        except Exception as exc:
            latency_ms = (time.time() - start) * 1000
            _record_harness_metrics(500, latency_ms)
            if config.ACCESS_LOG:
                print(json.dumps({
                    "event": "http_request",
                    "method": request.method,
                    "path": str(request.url.path),
                    "status": 500,
                    "latency_ms": round(latency_ms, 3),
                    "error": str(exc),
                }), file=sys.stderr)
            raise
        latency_ms = (time.time() - start) * 1000
        _record_harness_metrics(response.status_code, latency_ms)
        if config.ACCESS_LOG:
            print(json.dumps({
                "event": "http_request",
                "method": request.method,
                "path": str(request.url.path),
                "status": response.status_code,
                "latency_ms": round(latency_ms, 3),
                "client": request.client.host if request.client else None,
            }), file=sys.stderr)
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; base-uri 'self';"
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > _MAX_BODY_BYTES:
                    return PlainTextResponse("request body too large", status_code=413)
            except ValueError:
                return PlainTextResponse("invalid content-length", status_code=400)
        return await call_next(request)


class OptionalBearerAuthMiddleware(BaseHTTPMiddleware):
    """Gate protected benchmark endpoints with a bearer token if one is configured."""

    async def dispatch(self, request, call_next):
        if _API_TOKEN and request.url.path in _PROTECTED_PATHS:
            auth = request.headers.get("authorization", "")
            if not auth.startswith("Bearer ") or auth[7:] != _API_TOKEN:
                return JSONResponse({"status": "error", "error": "unauthorized"}, status_code=401)
        return await call_next(request)


_RUN_LOG: dict[str, deque[float]] = {}


def _client_ip(request):
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _manifest_count_last_hour() -> int:
    """Count signed manifests written in the last hour."""
    cutoff = time.time() - 3600
    try:
        return sum(1 for f in RUN_DIR.glob("*.json") if f.stat().st_mtime > cutoff)
    except OSError:
        return 0


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate-limit POST /harness/run by client IP and cap total manifests/hour.
    In-memory state is fine for the single-process harness; add Redis if you
    scale to multiple workers.
    """

    async def dispatch(self, request, call_next):
        if request.url.path == "/harness/run":
            max_manifests = config.HARNESS_MAX_MANIFESTS_PER_HOUR
            if max_manifests and _manifest_count_last_hour() >= max_manifests:
                return JSONResponse(
                    {"status": "error", "error": "manifest cap reached"},
                    status_code=429,
                )
            max_runs = config.HARNESS_MAX_RUNS_PER_MINUTE
            window = config.HARNESS_RATE_WINDOW_SECONDS
            if max_runs > 0 and window > 0:
                ip = _client_ip(request)
                now = time.time()
                log = _RUN_LOG.setdefault(ip, deque())
                while log and log[0] < now - window:
                    log.popleft()
                if len(log) >= max_runs:
                    return JSONResponse(
                        {"status": "error", "error": "rate limit exceeded"},
                        status_code=429,
                    )
                log.append(now)
        return await call_next(request)



app = Starlette(routes=routes, lifespan=lifespan)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestSizeLimitMiddleware)
app.add_middleware(RequestMetricsMiddleware)
app.add_middleware(OptionalBearerAuthMiddleware)
app.add_middleware(RateLimitMiddleware)
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


def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=config.HARNESS_PORT)


if __name__ == "__main__":
    main()
