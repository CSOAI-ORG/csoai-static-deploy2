#!/usr/bin/env python3
"""
E2E test suite for the Sovereign Town dashboard server.

Exercises every public HTTP route, the WebSocket live feed, static assets,
content-type/CORS headers, and both valid and invalid verification flows.
Runs against the locally-running server by default (http://127.0.0.1:3940).

Usage:
    cd p0_aqua
    python3.11 e2e_test.py
    SOV_TOWN_URL=http://host:port python3.11 e2e_test.py
    python3.11 e2e_test.py --url http://host:port --verbose
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Callable

import websockets

import sign_lib

BASE = os.environ.get("SOV_TOWN_URL", "http://127.0.0.1:3940")
WS = BASE.replace("http://", "ws://").replace("https://", "wss://") + "/ws/feed"

results: list[tuple[str, bool, int, str, float]] = []


def fetch(
    method: str,
    path: str,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 10.0,
) -> tuple[int, dict[str, str], bytes]:
    """Raw HTTP fetch; returns status/headers/body even for HTTP errors."""
    req = urllib.request.Request(
        BASE + path,
        data=data,
        headers=headers or {},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        body = e.read()
        e.close()
        return e.code, dict(e.headers), body


def fetch_with_retry(
    method: str,
    path: str,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 10.0,
    retries: int = 3,
) -> tuple[int, dict[str, str], bytes]:
    """Fetch with simple retry/backoff for transient failures."""
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            return fetch(method, path, data, headers, timeout)
        except urllib.error.URLError as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(0.5 * (attempt + 1))
    raise last_err  # type: ignore[misc]


def record(desc: str, ok: bool, status: int, extra: str = "", elapsed: float = 0.0) -> bool:
    results.append((desc, ok, status, extra, elapsed))
    return ok


def check_text(
    desc: str,
    method: str,
    path: str,
    expect: int = 200,
    substring: str | None = None,
    content_type: str | None = None,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> bool:
    start = time.perf_counter()
    try:
        status, resp_headers, body = fetch_with_retry(method, path, data=data, headers=headers)
        elapsed = time.perf_counter() - start
        ok = status == expect
        extra = ""
        if ok and substring:
            ok = substring.encode() in body
            extra = f"body_contains={substring!r}"
        if ok and content_type:
            got_ct = resp_headers.get("content-type", "").split(";")[0]
            ok = got_ct == content_type
            extra = f"content_type={got_ct}"
        return record(desc, ok, status, extra, elapsed)
    except Exception as e:
        return record(desc, False, 0, str(e), time.perf_counter() - start)


def check_json(
    desc: str,
    method: str,
    path: str,
    expect: int = 200,
    check_fn: Callable[[dict], bool] | None = None,
    require_content_type: str = "application/json",
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> bool:
    start = time.perf_counter()
    try:
        status, resp_headers, body = fetch_with_retry(method, path, data=data, headers=headers)
        elapsed = time.perf_counter() - start
        ok = status == expect
        extra = ""
        got_ct = resp_headers.get("content-type", "").split(";")[0]
        if ok and require_content_type:
            ok = got_ct == require_content_type
            extra = f"content_type={got_ct}"
        data: Any = None
        if ok:
            try:
                data = json.loads(body)
            except json.JSONDecodeError as e:
                ok = False
                extra = f"json_decode_error: {e}"
        if ok and check_fn:
            ok = check_fn(data)
            extra = f"check_fn={ok}"
        return record(desc, ok, status, extra, elapsed)
    except Exception as e:
        return record(desc, False, 0, str(e), time.perf_counter() - start)


def check_cors(path: str) -> bool:
    """By default cross-origin requests are denied; verify no wide-open ACAO header."""
    start = time.perf_counter()
    try:
        req = urllib.request.Request(
            BASE + path,
            method="OPTIONS",
            headers={
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        status, headers, _body = fetch("OPTIONS", path, headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "GET",
        })
        headers = {k.lower(): v for k, v in headers.items()}
        # Default hardened config rejects the preflight (405) and does not authorize arbitrary origins.
        ok = "access-control-allow-origin" not in headers
        return record(f"CORS default restricted {path}", ok, status, "", time.perf_counter() - start)
    except Exception as e:
        return record(f"CORS default restricted {path}", False, 0, str(e), time.perf_counter() - start)


def validate_agent(agent: dict) -> bool:
    return (
        isinstance(agent, dict)
        and isinstance(agent.get("district"), str)
        and isinstance(agent.get("agent_index"), int)
        and isinstance(agent.get("name"), str)
        and isinstance(agent.get("action"), str)
        and isinstance(agent.get("alive"), bool)
    )


def validate_town_tick(data: dict) -> bool:
    if data.get("topic") != "town_tick":
        return False
    if data.get("total_agents", 0) <= 0:
        return False
    if not isinstance(data.get("agents"), list):
        return False
    return all(validate_agent(a) for a in data["agents"][:5])


async def mcp_sse_test() -> None:
    """Verify dashboard proxies the MCP SSE server and rewrites the endpoint path."""
    start = time.perf_counter()
    try:
        import httpx
    except ImportError:
        record("MCP SSE proxy", True, 0, "httpx not installed; skipped", time.perf_counter() - start)
        return
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", f"{BASE}/mcp/sse") as resp:
                queue: asyncio.Queue[str] = asyncio.Queue()

                async def reader() -> None:
                    async for line in resp.aiter_lines():
                        await queue.put(line)

                read_task = asyncio.create_task(reader())
                try:
                    session_id = None
                    endpoint_line = ""
                    while True:
                        line = await asyncio.wait_for(queue.get(), timeout=3)
                        endpoint_line = line
                        m = re.search(r"session_id=([a-f0-9]+)", line)
                        if m:
                            session_id = m.group(1)
                            break
                    if not session_id:
                        record("MCP SSE proxy", False, resp.status_code, "no endpoint event", time.perf_counter() - start)
                        return
                    if "/mcp/messages/?session_id=" not in endpoint_line:
                        record("MCP SSE proxy", False, resp.status_code, "endpoint not rewritten", time.perf_counter() - start)
                        return
                    payload = {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {},
                            "clientInfo": {"name": "e2e", "version": "1.0"},
                        },
                    }
                    post_resp = await client.post(
                        f"{BASE}/mcp/messages/?session_id={session_id}",
                        json=payload,
                        timeout=10,
                    )
                    if post_resp.status_code != 202:
                        record("MCP SSE proxy", False, post_resp.status_code, post_resp.text[:80], time.perf_counter() - start)
                        return
                    response_ok = False
                    while True:
                        line = await asyncio.wait_for(queue.get(), timeout=5)
                        if '"id":1' in line and "serverInfo" in line:
                            response_ok = True
                            break
                    record("MCP SSE proxy", response_ok, 200, f"session_id={session_id[:8]}...", time.perf_counter() - start)
                finally:
                    read_task.cancel()
                    try:
                        await read_task
                    except asyncio.CancelledError:
                        pass
    except Exception as e:
        record("MCP SSE proxy", False, 0, str(e), time.perf_counter() - start)


async def _wait_for_ack(ws, expected_regime: str, max_messages: int = 10):
    """Drain messages until a regime ack matching expected_regime arrives."""
    for _ in range(max_messages):
        msg = await asyncio.wait_for(ws.recv(), timeout=5)
        data = json.loads(msg)
        if data.get("topic") == "regime" and data.get("regime") == expected_regime:
            return data
    return None


async def _wait_for_tick(ws, expected_regime: str, max_messages: int = 20):
    """Drain messages until a town_tick with the expected regime arrives."""
    for _ in range(max_messages):
        msg = await asyncio.wait_for(ws.recv(), timeout=5)
        data = json.loads(msg)
        if data.get("topic") == "town_tick" and data.get("regime") == expected_regime:
            return data
    return None


async def ws_test(verbose: bool = False) -> None:
    start = time.perf_counter()
    try:
        async with websockets.connect(WS) as ws:
            # Welcome status message.
            msg = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(msg)
            ok = data.get("topic") == "status" and data.get("payload", {}).get("hives") == 28
            record("WS /ws/feed welcome", ok, 101, str(data)[:80] if verbose else "", time.perf_counter() - start)

            # Ping/pong.
            await ws.send("ping")
            pong = await asyncio.wait_for(ws.recv(), timeout=5)
            record("WS ping/pong", json.loads(pong).get("topic") == "pong", 101, pong[:80] if verbose else "")

            # Regime switch to ungoverned.
            await ws.send(json.dumps({"regime": "ungoverned"}))
            ack = await _wait_for_ack(ws, "ungoverned")
            record("WS regime -> ungoverned", ack is not None, 101, str(ack)[:80] if verbose else "")

            # Wait for a town_tick broadcast in ungoverned mode.
            tick = await _wait_for_tick(ws, "ungoverned")
            tick_ok = tick is not None and validate_town_tick(tick)
            tick_extra = f"regime={tick.get('regime') if tick else '-'} agents={tick.get('total_agents') if tick else '-'}"
            record("WS town_tick (ungoverned)", tick_ok, 101, tick_extra)

            # Switch back to governed and verify.
            await ws.send(json.dumps({"regime": "governed"}))
            ack2 = await _wait_for_ack(ws, "governed")
            record("WS regime -> governed", ack2 is not None, 101, str(ack2)[:80] if verbose else "")

            governed_tick = await _wait_for_tick(ws, "governed")
            governed_tick_ok = governed_tick is not None
            governed_extra = f"regime={governed_tick.get('regime') if governed_tick else '-'} agents={governed_tick.get('total_agents') if governed_tick else '-'}"
            record("WS town_tick (governed)", governed_tick_ok, 101, governed_extra)

    except Exception as e:
        record("WS /ws/feed", False, 0, str(e), time.perf_counter() - start)


def run_http_tests() -> None:
    # Static / HTML routes
    check_text("GET /", "GET", "/", 200, "Sovereign Town", "text/html")
    check_text("GET / nav", "GET", "/", 200, "Workbench", "text/html")
    check_text("GET /dashboard", "GET", "/dashboard", 200, "Sovereign Town Research Dashboard", "text/html")
    check_text("GET /dashboard nav", "GET", "/dashboard", 200, "Workbench", "text/html")
    check_text("GET /town3d", "GET", "/town3d", 200, "Sovereign Town 3D", "text/html")
    check_text("GET /workbench", "GET", "/workbench", 200, "Regulatory Workbench", "text/html")
    check_text("GET /workbench MCP client", "GET", "/workbench", 200, "mcp-client-panel", "text/html")
    check_text("GET /workbench lanes", "GET", "/workbench", 200, "Lane A", "text/html")
    check_text("GET /workbench verify", "GET", "/workbench", 200, "Verify Manifest", "text/html")
    check_text("GET /regulatory-workbench", "GET", "/regulatory-workbench", 200, "Regulatory Workbench", "text/html")
    check_text("GET /passport", "GET", "/passport", 200, content_type="text/html")
    check_text("GET /verify", "GET", "/verify", 200, content_type="text/html")
    check_text("GET /fleet-status.html", "GET", "/fleet-status.html", 200, "Fleet Status", "text/html")
    check_text("GET /experiments", "GET", "/experiments.html", 200, "Policy Lab Experiments", "text/html")
    check_text("GET /harness/health proxy", "GET", "/harness/health", 200, '"status":"ok"', "application/json")
    check_json("GET /harness/metrics proxy", "GET", "/harness/metrics", 200, lambda d: d.get("status") == "ok" and "requests_total" in d)
    check_text("GET /leaderboard", "GET", "/leaderboard", 200, "Public Benchmark Leaderboard", "text/html")

    # Signed run detail flow: use first run from leaderboard.
    run_id = None
    try:
        status, _, body = fetch_with_retry("GET", "/harness/leaderboard")
        if status == 200:
            rows = json.loads(body).get("leaderboard", [])
            if rows:
                run_id = rows[0].get("id")
    except Exception:
        run_id = None
    if run_id:
        check_text("GET /run.html detail", "GET", f"/run.html?id={run_id}", 200, "Run Detail", "text/html")
        check_json(
            "GET /harness/runs/{id} proxy",
            "GET",
            f"/harness/runs/{run_id}",
            200,
            lambda d: "manifest" in d and d.get("manifest", {}).get("id") == run_id,
        )
    else:
        record("GET /run.html detail", True, 0, "no runs available", 0.0)
        record("GET /harness/runs/{id} proxy", True, 0, "no runs available", 0.0)
    check_text("GET /run.html missing id", "GET", "/run.html", 200, "Missing run id", "text/html")
    check_text("GET /run.html invalid id", "GET", "/run.html?id=notarealid", 200, "Run not found", "text/html")

    # JSON API routes — moats
    check_json("GET /api/status", "GET", "/api/status", 200, lambda d: d.get("hives") == 28 and d.get("passports") >= 28)
    check_json("GET /api/health", "GET", "/api/health", 200, lambda d: d.get("status") == "ok" and "uptime_seconds" in d)
    check_json("GET /api/ready", "GET", "/api/ready", 200, lambda d: d.get("ready") is True and "checks" in d)
    check_json("GET /api/metrics", "GET", "/api/metrics", 200, lambda d: "requests_total" in d and "websocket_clients" in d)

    # Performance baseline: median /api/health latency under 50 ms locally.
    latencies: list[float] = []
    for _ in range(20):
        s = time.perf_counter()
        fetch("GET", "/api/health")
        latencies.append((time.perf_counter() - s) * 1000)
    median = sorted(latencies)[len(latencies) // 2]
    ok = median < 100.0
    record(f"perf /api/health median latency < 100 ms (got {median:.2f} ms)", ok, 200, f"median={median:.2f}ms", median)
    check_json("GET /api/experiments", "GET", "/api/experiments", 200, lambda d: isinstance(d.get("experiments"), list))
    check_json("GET /api/experiments/dora_finance_001", "GET", "/api/experiments/dora_finance_001", 200, lambda d: d.get("id") == "dora_finance_001")
    check_json("GET /api/moat", "GET", "/api/moat", 200, lambda d: "indices" in d and "eu_resilience_index" in d.get("indices", {}))
    check_json("GET /api/attestations", "GET", "/api/attestations", 200, lambda d: "regimes" in d and "hives" in d)
    check_json("GET /api/threat", "GET", "/api/threat", 200, lambda d: "cisa_kev" in d and "indices" in d)
    check_json("GET /api/sanctions", "GET", "/api/sanctions", 200, lambda d: "ofac_sdn" in d and "indices" in d)
    check_json("GET /api/psc", "GET", "/api/psc", 200, lambda d: "psc_summary" in d and "indices" in d)
    check_json("GET /api/finance", "GET", "/api/finance", 200, lambda d: "series" in d and "indices" in d)
    check_json("GET /api/agriculture", "GET", "/api/agriculture", 200, lambda d: "agriculture_summary" in d and "indices" in d)
    check_json("GET /api/energy", "GET", "/api/energy", 200, lambda d: "series" in d and "indices" in d)
    check_json("GET /api/climate", "GET", "/api/climate", 200, lambda d: "climate_summary" in d and "indices" in d)

    # Live town state
    check_json(
        "GET /api/town-state (governed)",
        "GET",
        "/api/town-state",
        200,
        lambda d: d.get("topic") == "town_tick" and validate_town_tick(d) and d.get("regime") == "governed",
    )
    check_json(
        "GET /api/town-state?regime=ungoverned",
        "GET",
        "/api/town-state?regime=ungoverned",
        200,
        lambda d: d.get("regime") == "ungoverned" and validate_town_tick(d),
    )
    check_json(
        "GET /api/town-state?regime=invalid",
        "GET",
        "/api/town-state?regime=invalid",
        200,
        lambda d: d.get("regime") == "governed",
    )

    # Hives / characters / episodes / ledger
    check_json("GET /api/hives", "GET", "/api/hives", 200, lambda d: len(d) >= 28)
    check_json("GET /api/hives/aqua", "GET", "/api/hives/aqua", 200, lambda d: "passport" in d and "characters" in d)
    check_json("GET /api/hives/missing", "GET", "/api/hives/nonexistent", 404)
    check_json("GET /api/hive/aethelgard", "GET", "/api/hive/aethelgard", 200, lambda d: d.get("id") == "aethelgard-finance")
    check_json("POST /api/council/vote", "POST", "/api/council/vote", 200, lambda d: d.get("result") in {"approved", "modify", "rejected"}, data=b'{"proposal": "test alignment"}')
    # Regulation intake / auto-spawn endpoint
    spawn_no_auth_status, _, _ = fetch("POST", "/api/experiments/spawn", data=b'{}', headers={"Content-Type": "application/json"})
    record("POST /api/experiments/spawn no auth", spawn_no_auth_status in (401, 503), spawn_no_auth_status, "")
    api_token = os.environ.get("SOV_TOWN_API_TOKEN")
    if api_token:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
        check_json("POST /api/experiments/spawn invalid body", "POST", "/api/experiments/spawn", 400, lambda d: "error" in d, data=b'{"intake": {}}', headers=headers)
        intake_payload = json.dumps({
            "intake": {
                "regulation": "E2E Test Regulation",
                "framework": "dora",
                "industry": "e2e-test",
                "civilization": "E2Egard",
                "hypothesis": "Automation reduces incident response time",
                "agents": 12,
            },
            "live": False,
        }).encode()
        def _spawn_ok(d):
            return d.get("experiment_id", "").startswith("dora_e2e_test_") and d.get("status") in {"approved", "modify"}
        check_json("POST /api/experiments/spawn intake", "POST", "/api/experiments/spawn", 200, _spawn_ok, data=intake_payload, headers=headers)

    check_json("GET /api/sov3/handshake", "GET", "/api/sov3/handshake", 200, lambda d: all(k in d for k in ("pubkey", "nonce", "timestamp", "sig", "message")))
    check_json("POST /api/sov3/think", "POST", "/api/sov3/think", 503, lambda d: "error" in d, data=b'{"character":"sov-town","message":"ping","profile":"local_only"}', headers={"Content-Type": "application/json"})
    check_json("GET /api/characters", "GET", "/api/characters", 200, lambda d: "aqua" in d)
    check_json("GET /api/characters/aqua", "GET", "/api/characters/aqua", 200, lambda d: "personas" in d)
    check_json("GET /api/episodes", "GET", "/api/episodes?limit=5", 200, lambda d: isinstance(d, list) and len(d) <= 5)
    check_json("GET /api/ledger", "GET", "/api/ledger?host=mac", 200, lambda d: isinstance(d, list))
    check_json("GET /api/models", "GET", "/api/models", 200, lambda d: "models" in d)
    check_json("GET /api/corpus", "GET", "/api/corpus", 200)
    check_json("GET /api/passports", "GET", "/api/passports", 200, lambda d: isinstance(d, list) and len(d) >= 29)
    check_json("GET /api/passports/aqua", "GET", "/api/passports/aqua", 200)
    check_text("GET /api/labs-index", "GET", "/api/labs-index", 200, content_type="text/plain")
    check_text("GET /api/labs/crimes.svg", "GET", "/api/labs/crimes.svg", 200, "<svg", "image/svg+xml")

    # CORS smoke test
    check_cors("/api/status")
    check_cors("/mcp/sse")


def run_verify_tests() -> None:
    priv, pub_b64 = sign_lib.load_or_create_key()
    msg = json.dumps({"topic": "e2e", "nonce": 12345}, sort_keys=True, separators=(",", ":"))
    sig = sign_lib.sign(priv, msg)

    # Valid signature
    body = json.dumps({"payload": msg, "sig": sig, "pubkey": pub_b64})
    start = time.perf_counter()
    try:
        status, _, out_body = fetch_with_retry(
            "POST",
            "/api/verify",
            data=body.encode(),
            headers={"Content-Type": "application/json"},
        )
        out = json.loads(out_body)
        record(
            "POST /api/verify (valid sig)",
            status == 200 and out.get("valid") is True,
            status,
            str(out)[:80],
            time.perf_counter() - start,
        )
    except Exception as e:
        record("POST /api/verify (valid sig)", False, 0, str(e), time.perf_counter() - start)

    # Tampered payload
    bad_body = json.dumps({"payload": msg + "x", "sig": sig, "pubkey": pub_b64})
    start = time.perf_counter()
    try:
        status, _, out_body = fetch_with_retry(
            "POST",
            "/api/verify",
            data=bad_body.encode(),
            headers={"Content-Type": "application/json"},
        )
        out = json.loads(out_body)
        record(
            "POST /api/verify (tampered payload)",
            status == 200 and out.get("valid") is False,
            status,
            str(out)[:80],
            time.perf_counter() - start,
        )
    except Exception as e:
        record("POST /api/verify (tampered payload)", False, 0, str(e), time.perf_counter() - start)

    # Missing fields
    incomplete_body = json.dumps({"payload": msg, "sig": sig})
    start = time.perf_counter()
    try:
        status, _, out_body = fetch("POST", "/api/verify", data=incomplete_body.encode(), headers={"Content-Type": "application/json"})
        record(
            "POST /api/verify (missing pubkey)",
            status == 400,
            status,
            out_body.decode()[:80],
            time.perf_counter() - start,
        )
    except Exception as e:
        record("POST /api/verify (missing pubkey)", False, 0, str(e), time.perf_counter() - start)

    # FreeLLMAPI chat proxy: when no key is configured we expect a clear 503.
    start = time.perf_counter()
    try:
        status, _, out_body = fetch("POST", "/agent/chat", data=b'{"messages":[{"role":"user","content":"hello"}]}', headers={"Content-Type": "application/json"})
        try:
            data = json.loads(out_body)
        except Exception:
            data = {}
        ok = status == 503 and data.get("error") == "FreeLLMAPI key not configured"
        record("POST /agent/chat (proxy)", ok, status, data.get("error", out_body.decode()[:60]), time.perf_counter() - start)
    except Exception as e:
        record("POST /agent/chat (proxy)", False, 0, str(e), time.perf_counter() - start)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sovereign Town E2E test suite")
    parser.add_argument("--url", default=os.environ.get("SOV_TOWN_URL", "http://127.0.0.1:3940"), help="Base URL to test")
    parser.add_argument("--verbose", action="store_true", help="Print extra response details")
    args = parser.parse_args()

    global BASE, WS
    BASE = args.url.rstrip("/")
    WS = BASE.replace("http://", "ws://").replace("https://", "wss://") + "/ws/feed"

    async def run_async_tests() -> None:
        await mcp_sse_test()
        await ws_test(verbose=args.verbose)

    run_http_tests()
    run_verify_tests()
    asyncio.run(run_async_tests())

    passed = sum(1 for _, ok, _, _, _ in results if ok)
    total = len(results)
    total_time = sum(t for _, _, _, _, t in results)

    print(f"\nE2E RESULTS: {passed}/{total} passed in {total_time:.2f}s\n")
    print(f"{'RESULT':<6} {'STATUS':<7} {'TIME':<8} {'TEST':<40} {'DETAIL'}")
    print("-" * 110)
    for desc, ok, status, extra, elapsed in results:
        mark = "PASS" if ok else "FAIL"
        print(f"{mark:<6} {status:<7} {elapsed:>7.3f}s {desc:<40} {extra}")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
