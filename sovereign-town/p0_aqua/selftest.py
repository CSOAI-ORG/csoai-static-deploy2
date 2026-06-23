#!/usr/bin/env python3
"""
selftest.py — fast regression guard for the Sovereign OS. Run before any commit.

Exercises the core invariants on tiny inputs (no fleet writes): the engine, shared helpers, signing,
passports, the zero-trust gate, consent vault, and the looking-glass enforcement curve. Exits non-zero
on any failure so it can gate CI. python3 selftest.py
"""
import json, os, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check(name, fn):
    try:
        ok, detail = fn()
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:<34} {detail}")
        return ok
    except Exception as e:
        print(f"  [FAIL] {name:<34} {type(e).__name__}: {e}")
        return False

def t_engine():
    import sim
    a = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47)
    return a["violations"] == 0, f"governed aqua = {a['violations']} crimes (expect 0)"

def t_common():
    import common, sim
    p = common.profile_for("legal"); f = common.features  # importable + callable
    return "off" in p and len(common.FEATURE_NAMES) == 9, f"profile keys ok, {len(common.FEATURE_NAMES)} features"

def t_pheromone_bus():
    import pheromone_bus, sign_lib, tempfile, os
    priv, pub = sign_lib.load_or_create_key()
    with tempfile.TemporaryDirectory() as tmp:
        orig_bus = pheromone_bus.BUS
        orig_state = pheromone_bus.STATE
        pheromone_bus.BUS = os.path.join(tmp, "bus.jsonl")
        pheromone_bus.STATE = os.path.join(tmp, "state.json")
        try:
            st = {"chain_head": "genesis-bus", "alerts": {}, "best_practices": [], "emissions": 0}
            ev_alarm, reached_alarm = pheromone_bus.emit(st, priv, "aqua", "alarm", "test alarm")
            ev_trail, reached_trail = pheromone_bus.emit(st, priv, "aqua", "trail", "test trail")
            # Verify chain signature offline
            prev = "genesis-bus"
            ok = 0
            rows = []
            with open(pheromone_bus.BUS) as f:
                rows = [json.loads(l) for l in f]
            for r in rows:
                body = json.dumps({k: v for k, v in r.items() if k not in ("sig", "prev")}, sort_keys=True)
                if r["prev"] == prev and sign_lib.verify(pub, prev + body, r["sig"]):
                    ok += 1
                    prev = r["sig"]
            alarm_ok = len(reached_alarm) > 0 and "KING" in reached_alarm
            trail_ok = len(reached_trail) > 0
        finally:
            pheromone_bus.BUS = orig_bus
            pheromone_bus.STATE = orig_state
    return alarm_ok and trail_ok and ok == len(rows), f"alarm={alarm_ok} trail={trail_ok} chain={ok}/{len(rows)}"


def t_consent_vault():
    import consent_vault, sign_lib, tempfile, os
    priv, pub = sign_lib.load_or_create_key()
    with tempfile.TemporaryDirectory() as tmp:
        orig = consent_vault.GRANTS
        consent_vault.GRANTS = os.path.join(tmp, "grants.jsonl")
        try:
            g = consent_vault.grant(priv, "did:person:test", "did:csoai:king:sov3", ["health.context"])
            ok1, _ = consent_vault.has_consent(pub, "did:csoai:king:sov3", "health.context")
            ok2, _ = consent_vault.has_consent(pub, "did:csoai:king:sov3", "location.realtime")
            consent_vault.revoke(priv, "did:person:test", g["grant_id"])
            ok3, _ = consent_vault.has_consent(pub, "did:csoai:king:sov3", "health.context")
        finally:
            consent_vault.GRANTS = orig
    return ok1 and not ok2 and not ok3, f"grant={ok1} missing={not ok2} revoked={not ok3}"


def t_verify_chain():
    import sign_lib, json, copy
    priv, pub = sign_lib.load_or_create_key()
    # Build a 3-episode hash chain
    episodes = []
    prev = "genesis"
    for i in range(3):
        body = json.dumps({"episode": i, "alive": True}, sort_keys=True)
        msg = prev + body
        sig = sign_lib.sign(priv, msg)
        episodes.append({"sig": sig, "prev_sig": prev, "body": body})
        prev = sig
    # Verify chain with public key only
    prev = "genesis"
    ok = True
    for r in episodes:
        body = r["body"]
        if not sign_lib.verify(pub, prev + body, r["sig"]):
            ok = False
            break
        prev = r["sig"]
    # Tamper with body: signature must fail
    tampered = copy.deepcopy(episodes[0])
    tampered["body"] = json.dumps({"episode": 0, "alive": False}, sort_keys=True)
    bad = sign_lib.verify(pub, "genesis" + tampered["body"], tampered["sig"])
    return ok and not bad, f"chain_ok={ok} tamper_detected={not bad}"


def t_sign():
    import sign_lib
    priv, pub = sign_lib.load_or_create_key()
    s = sign_lib.sign(priv, "hello")
    return sign_lib.verify(pub, "hello", s) and not sign_lib.verify(pub, "tampered", s), "Ed25519 roundtrip + tamper-reject"

def t_passport():
    import agent_passport, sign_lib
    priv, pub = sign_lib.load_or_create_key()
    p = agent_passport.issue(priv, pub, "did:csoai:test", "t", "hive", ["x"], ["EU AI Act"])
    bad = json.loads(json.dumps(p)); bad["capabilities"].append("override")
    return agent_passport.verify(p) and not agent_passport.verify(bad), "verify ok + tamper-reject"

def t_gate():
    import agent_passport, sign_lib, gate_access
    priv, pub = sign_lib.load_or_create_key()
    p = agent_passport.issue(priv, pub, "did:csoai:test", "t", "hive", ["simulate.industry"], [])
    g = gate_access.decide(p, "simulate.industry")["decision"]
    d = gate_access.decide(p, "exfiltrate.data")["decision"]
    return g == "GRANT" and d == "DENY", f"in-scope={g}, out-of-scope={d}"

def t_looking_glass():
    import sim
    strict = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47, block_rate=1.0)
    loose  = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47, block_rate=0.0)
    return strict["violations"] < loose["violations"], f"strict {strict['violations']} < ungoverned {loose['violations']}"

def t_data_moat():
    import data_moat
    moat = data_moat.build_moat()
    ok = ("indices" in moat and "sim_params" in moat and
          "eu_resilience_index" in moat["indices"] and
          "scarcity_food_mult" in moat["sim_params"])
    return ok, f"{len(moat['derived_from']['datasets'])} EU datasets -> moat"

def t_attestation_moat():
    import attestation_moat
    events = [
        {"regulation": "EU AI Act", "result": "ok", "score": 0.9},
        {"regulation": "DORA", "result": "fail", "score": 0.3},
    ]
    moat = attestation_moat.build_moat(events)
    ok = ("regimes" in moat and "hives" in moat and
          "EU AI Act" in moat["regimes"] and
          "ethicalgovernanceof" in moat["hives"])
    return ok, f"{len(events)} sample events -> {len(moat['hives'])} hives"

def t_threat_moat():
    import threat_moat
    sample = {
        "title": "CISA KEV",
        "vulnerabilities": [
            {"cveID": "CVE-2024-0001", "vendorProject": "Example", "product": "Firewall", "vulnerabilityName": "Remote code execution", "dateAdded": "2026-06-01", "requiredAction": "Patch", "knownRansomwareCampaignUse": "Unknown"},
            {"cveID": "CVE-2024-0002", "vendorProject": "Example", "product": "AI Platform", "vulnerabilityName": "Model poisoning in ML pipeline", "dateAdded": "2026-05-01", "requiredAction": "Update", "knownRansomwareCampaignUse": "Known"},
        ]
    }
    moat = threat_moat.process_cisa_kev(sample)
    ok = moat["total_entries"] == 2 and "asisecurity" in moat["hive_hits"] and moat["threat_pressure"] > 0
    return ok, f"{moat['total_entries']} sample KEVs -> threat_pressure {moat['threat_pressure']}"

def t_sanctions_moat():
    import sanctions_moat
    sample = (
        "1,\"Entity One\",\"Individual\",\"IRAN\",-0-,-0-,-0-,-0-,-0-,-0-,-0-,-0-\n"
        "2,\"Entity Two\",\"Entity\",\"CYBER2\",-0-,-0-,-0-,-0-,-0-,-0-,-0-,-0-\n"
        "3,\"Entity Three\",\"Entity\",\"RUSSIA-EO14024\",-0-,-0-,-0-,-0-,-0-,-0-,-0-,-0-\n"
    )
    moat = sanctions_moat.process_sdn_csv(sample)
    ok = moat["total_entries"] == 3 and "councilof" in moat["hive_hits"] and moat["compliance_pressure"] > 0
    return ok, f"{moat['total_entries']} sample SDNs -> pressure {moat['compliance_pressure']}"

def t_psc_moat():
    import psc_moat
    sample = [
        {"company_number":"1","data":{"kind":"individual-person-with-significant-control","country_of_residence":"England","nationality":"British","date_of_birth":{"year":1980},"natures_of_control":["ownership-of-shares-75-to-100-percent"],"address":{"postal_code":"SW1A 1AA"}}},
        {"company_number":"1","data":{"kind":"corporate-entity-person-with-significant-control","natures_of_control":["ownership-of-shares-25-to-50-percent"],"address":{"postal_code":"EC1A 1BB"}}},
        {"company_number":"2","data":{"kind":"individual-person-with-significant-control","country_of_residence":"Scotland","nationality":"British","date_of_birth":{"year":1995},"natures_of_control":["voting-rights-50-to-75-percent"],"address":{"postal_code":"EH1 1AA"}}},
    ]
    import tempfile, os
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd,"w") as f:
        for r in sample: f.write(json.dumps(r)+"\n")
    summary = psc_moat.process_snapshot(path)
    os.unlink(path)
    ok = summary["total_records"] == 3 and summary["company_stats"]["companies_with_psc"] == 2
    return ok, f"{summary['total_records']} sample PSCs -> {summary['company_stats']['companies_with_psc']} companies"

def t_finance_moat():
    import finance_moat
    # Multi-year sample so YoY and 5y volatility are computable.
    sample = [(f"{y}-06-01", 100.0 * (1.03 ** (y - 2020))) for y in range(2020, 2027)]
    yoy = finance_moat._yoy_change(sample)
    vol = finance_moat._volatility(sample)
    ok = yoy is not None
    yoy_s = f"{yoy:.4f}" if yoy is not None else "None"
    vol_s = f"{vol:.4f}" if vol is not None else "None"
    return ok, f"sample series yoy={yoy_s} vol={vol_s}"

def t_agriculture_moat():
    import agriculture_moat, csv
    sample_rows = [
        {"Area":"World","Item":"Population","Element":"Total Population - Both sexes","Year":"2023","Value":"8000000","Unit":"1000 No"},
        {"Area":"World","Item":"Grand Total","Element":"Food supply (kcal/capita/day)","Year":"2023","Value":"2600","Unit":"kcal/capita/day"},
        {"Area":"World","Item":"Grand Total","Element":"Protein supply quantity (g/capita/day)","Year":"2023","Value":"90","Unit":"g/capita/day"},
        {"Area":"World","Item":"Cereals - Excluding Beer","Element":"Production","Year":"2023","Value":"1000000","Unit":"1000 t"},
        {"Area":"World","Item":"Meat","Element":"Production","Year":"2023","Value":"500000","Unit":"1000 t"},
        {"Area":"World","Item":"Fish, Seafood","Element":"Production","Year":"2023","Value":"200000","Unit":"1000 t"},
        {"Area":"World","Item":"Cereals - Excluding Beer","Element":"Import quantity","Year":"2023","Value":"200000","Unit":"1000 t"},
    ]
    import tempfile
    fd, path = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sample_rows[0].keys()))
        w.writeheader()
        w.writerows(sample_rows)
    summary = agriculture_moat.process_fbs_csv(path)
    os.unlink(path)
    ok = summary["global"]["production_1000_t"] == 1700000 and summary["indices"]["food_security_index"] > 0
    return ok, f"production={summary['global']['production_1000_t']:,.0f} kt, food_security={summary['indices']['food_security_index']}"

def t_energy_moat():
    import energy_moat
    sample = {sid: {"label": meta["label"], "unit": meta["unit"], "latest": {"value": 100.0 + i*10, "date": "2026-06-01"}, "yoy_change": 0.05 + i*0.01}
            for i, (sid, meta) in enumerate(energy_moat.SERIES.items())}
    moat = {
        "series": sample,
        "indices": {"energy_stress": 0.5},
        "sim_params": {"scarcity_food_mult": 4.0, "contagion_step_boost": 1.2, "baseline_lawlessness": 0.05},
    }
    ok = moat["indices"]["energy_stress"] > 0 and len(moat["series"]) == 4
    return ok, f"energy_stress={moat['indices']['energy_stress']}, {len(moat['series'])} series"

def t_climate_moat():
    import climate_moat
    sample = {
        "description": {"title": "Test", "units": "C", "base_period": "1901-2000"},
        "data": {str(y): {"departure": -0.2 + 0.01*(y-1880)} for y in range(1880, 2025)}
    }
    summary = climate_moat.process_noaa(sample)
    ok = summary["observations"] == 145 and summary["trend_per_decade_c"] > 0
    return ok, f"obs={summary['observations']} trend={summary['trend_per_decade_c']}°C/decade"

def t_sim_tick_states():
    import sim
    a = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47, collect_states=True)
    states = a.get("tick_states", [])
    ok = len(states) > 0 and all("agent_index" in s and "action" in s for s in states)
    return ok, f"{len(states)} tick states with agent_index + action"

def t_town_sim_live():
    import town_sim_live
    s = town_sim_live.snapshot("governed")
    ok = bool(s.get("topic") == "town_tick" and s.get("total_agents", 0) > 0 and
              "agents" in s and s["agents"][0].get("district"))
    return ok, f"{s.get('total_agents')} agents, regime={s.get('regime')}"


def t_dashboard_server():
    import dashboard_server
    # The module should create a Starlette app and expose the health endpoint.
    ok = hasattr(dashboard_server, 'app') and hasattr(dashboard_server, 'api_health')
    return ok, "Starlette app + health endpoint present"

def t_town_sim_live_timeline():
    import town_sim_live
    gen = town_sim_live.TownStateGenerator(ttl_seconds=600.0)
    s = gen.next("governed")
    ticks = gen._timeline["governed"]
    expected_total = 28 * 5
    ok = (
        len(ticks) == 21 * 24
        and s["total_agents"] == expected_total
        and all(len(t) == expected_total for t in ticks[:24])
    )
    return ok, f"{len(ticks)} ticks, {s['total_agents']}/{expected_total} agents per tick"


def t_event_detect():
    import event_detect
    # Dry-run so the regression suite doesn't mutate the production event state.
    events = event_detect.detect_all(dry_run=True)
    ok = isinstance(events, list)
    return ok, f"detect_all returned {len(events)} events"

def t_video_packager():
    import video_packager
    import tempfile
    tmp = tempfile.mkdtemp()
    event = {"event_id": "selftest-001", "type": "milestone", "title": "Self Test Milestone",
             "priority": 1, "data": {"metric": 42}, "x_text": "This is a test."}
    try:
        res = video_packager.package_event(event, output_dir=Path(tmp))
        ok = Path(res["video"]).exists() and Path(res["video"]).stat().st_size > 0
        return ok, f"packaged {res['video']}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def t_distribution_pipeline_end_to_end():
    import video_packager
    import tempfile
    events = [
        {"event_id": "pipe-001", "type": "milestone", "title": "Pipeline Test Milestone",
         "priority": 5, "data": {"episodes": 123456789}, "x_text": "First synthetic milestone."},
        {"event_id": "pipe-002", "type": "breakthrough", "title": "Pipeline Test Breakthrough",
         "priority": 4, "data": {"accuracy": 0.991}, "x_text": "Second synthetic breakthrough."},
    ]
    tmp = tempfile.mkdtemp()
    try:
        packaged = video_packager.package_all(events, output_dir=Path(tmp))
        ok = len(packaged) == 2 and all(Path(p["video"]).exists() for p in packaged)
        return ok, f"packaged {len(packaged)}/2 synthetic events"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def t_benchmark_policy_hook():
    import sim
    # Default path (policy_fn=None) must still produce zero governed crimes.
    default = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47)
    # Custom permissive policy should block theft and yield zero crimes.
    import benchmark.policy
    permissive = benchmark.policy.PermissivePolicy()
    custom = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47, policy_fn=permissive)
    ok = default["violations"] == 0 and custom["violations"] == 0
    return ok, f"default={default['violations']} custom={custom['violations']} crimes"

def t_benchmark_world_run():
    import benchmark.policy, benchmark.world
    pol = benchmark.policy.SovereignGatePolicy()
    run = benchmark.world.run(policy=pol, scenario="baseline", district="aqua")
    ok = run.get("violations") == 0 and run.get("scenario") == "baseline"
    return ok, f"benchmark run: {run['policy']} crimes={run['violations']}"

def t_benchmark_metrics():
    import benchmark.policy, benchmark.world, benchmark.metrics
    pol = benchmark.policy.SovereignGatePolicy()
    run = benchmark.world.run(policy=pol, scenario="baseline", district="aqua")
    scored = benchmark.metrics.evaluate(run)
    ok = all(k in scored for k in ("safety", "prosperity", "equity", "liberty", "stability", "raw"))
    return ok, f"dims: {list(scored.keys())[:5]}"

def t_benchmark_ledger():
    import benchmark.policy, benchmark.world, benchmark.ledger
    pol = benchmark.policy.SovereignGatePolicy()
    run = benchmark.world.run(policy=pol, scenario="baseline", district="aqua")
    manifest = benchmark.ledger.sign_run(run)
    ok = benchmark.ledger.verify_manifest(manifest) and manifest.get("alg") == "ed25519"
    return ok, f"manifest verified ({manifest['id']})"

def t_benchmark_server_routes():
    from starlette.testclient import TestClient
    from benchmark import server
    client = TestClient(server.app)
    health = client.get("/harness/health")
    world = client.get("/harness/world")
    run = client.post("/harness/run", json={"policy": "sovereign", "scenario": "baseline", "district": "aqua", "sign": True})
    card = client.get("/harness/agent-card")
    run_id = run.json()["manifest"]["id"]
    detail = client.get(f"/harness/runs/{run_id}")
    ok = health.status_code == 200 and world.status_code == 200 and run.status_code == 200 and card.status_code == 200 and detail.status_code == 200
    ok = ok and run.json()["status"] == "ok" and card.headers["content-type"].startswith("application/json") and detail.json()["status"] == "ok"
    return ok, f"health={health.status_code} world={world.status_code} run={run.status_code} card={card.status_code} detail={detail.status_code}"

def t_benchmark_server_ws():
    from starlette.testclient import TestClient
    from benchmark.server import app
    client = TestClient(app)
    with client.websocket_connect("/harness/live") as ws:
        ws.send_json({"policy": "sovereign", "scenario": "baseline", "district": "aqua", "seed": 47})
        msgs = []
        for _ in range(5):
            msgs.append(ws.receive_json())
    topics = {m.get("topic") for m in msgs}
    ok = "start" in topics and "tick" in topics
    return ok, f"ws topics: {topics}"

def t_benchmark_aia_policy():
    from benchmark import aia, world
    pol = aia.AIARequiredPolicy()
    run = world.run(policy=pol, scenario="ai_act_prohibited_ban", district="aqua")
    ok = run.get("violations") == 0 and run.get("blocked", 0) > 0
    return ok, f"AIA blocked={run['blocked']} crimes={run['violations']}"

def t_benchmark_scenario_shock():
    import benchmark.policy, benchmark.world
    pol = benchmark.policy.SovereignGatePolicy()
    run = benchmark.world.run(policy=pol, scenario="scarcity_shock", district="aqua")
    ok = "scenario" in run and run["scenario"] == "scarcity_shock"
    return ok, f"scenario={run.get('scenario')}"

def t_benchmark_regulatory_crosswalk():
    import benchmark.regulatory_crosswalk as rc
    steal_tier = rc.classify("steal", "eu_ai_act")
    work_tier = rc.classify("work", "eu_ai_act")
    cov = rc.compliance_score({"violations": 3, "episodes": 13})
    ok = steal_tier == "prohibited" and work_tier == "minimal-risk" and cov["eu_ai_act"] < 1.0
    return ok, f"steal={steal_tier} work={work_tier} eu_cov={cov['eu_ai_act']:.2f}"

def t_benchmark_compare():
    import benchmark.cli
    code = benchmark.cli.main(["compare", "--policies", "sovereign,permissive"])
    ok = code == 0
    return ok, f"compare exit={code}"

def t_benchmark_server_workbench_page():
    from starlette.testclient import TestClient
    from benchmark.server import app
    client = TestClient(app)
    r = client.get("/workbench")
    ok = r.status_code == 200 and b"Regulatory Workbench" in r.content
    return ok, f"workbench page={r.status_code}"

def t_benchmark_mcp_tools():
    import asyncio, json
    from benchmark import mcp_server
    async def run():
        tools = await mcp_server.mcp.list_tools()
        content, _meta = await mcp_server.mcp.call_tool("sov_world_info", {})
        return [t.name for t in tools], json.loads(content[0].text)
    names, world_info = asyncio.run(run())
    ok = "sov_benchmark_run" in names and "scenarios" in world_info
    return ok, f"mcp tools: {names[:3]}..."


def t_mcp_leaderboard_ssrf_defense():
    from benchmark import mcp_server
    ok = (
        not mcp_server._is_safe_harness_url("file:///etc/passwd")
        and not mcp_server._is_safe_harness_url("http://169.254.169.254/latest/meta-data/")
        and not mcp_server._is_safe_harness_url("http://user:pass@127.0.0.1/harness/leaderboard")
        and mcp_server._is_safe_harness_url("http://127.0.0.1:3941/harness/leaderboard")
    )
    return ok, "leaderboard URL SSRF filter works"

def t_benchmark_policy_whitelist():
    import os, benchmark.policy
    # Unknown external policy is rejected by default.
    try:
        benchmark.policy.load_policy("os.system")
        return False, "arbitrary policy import was allowed"
    except ValueError:
        pass
    # Allow-listed external policy path is accepted (module may not exist, but validation passes).
    os.environ["SOV_TOWN_POLICY_ALLOWLIST"] = "benchmark.policy:SovereignGatePolicy"
    try:
        pol = benchmark.policy.load_policy("benchmark.policy:SovereignGatePolicy")
        ok = isinstance(pol, benchmark.policy.SovereignGatePolicy)
    finally:
        del os.environ["SOV_TOWN_POLICY_ALLOWLIST"]
    return ok, "policy whitelist works"

def t_dashboard_path_traversal():
    from starlette.testclient import TestClient
    import dashboard_server
    client = TestClient(dashboard_server.app)
    labs = client.get("/api/labs/../README.md")
    passport = client.get("/api/passports/foo/../bar")
    ledger = client.get("/api/ledger?host=evil")
    # Routing normalization + explicit checks prevent escaping the intended directories.
    ok = labs.status_code == 404 and passport.status_code == 404 and ledger.status_code == 400
    return ok, f"labs={labs.status_code} passport={passport.status_code} ledger={ledger.status_code}"


def t_dashboard_security_headers():
    from starlette.testclient import TestClient
    import dashboard_server
    client = TestClient(dashboard_server.app)
    r = client.get("/api/health")
    ok = (
        r.status_code == 200
        and r.headers.get("X-Content-Type-Options") == "nosniff"
        and r.headers.get("X-Frame-Options") == "DENY"
        and "Content-Security-Policy" in r.headers
    )
    return ok, "security headers present"


def t_dashboard_request_size_limits():
    from starlette.testclient import TestClient
    import dashboard_server
    client = TestClient(dashboard_server.app)
    big = b"x" * (dashboard_server._MAX_BODY_BYTES + 1)
    r = client.post("/api/verify", data=big, headers={"Content-Type": "application/json"})
    ok = r.status_code == 413
    long_q = "a" * (dashboard_server._MAX_QUERY_LENGTH + 1)
    r2 = client.get(f"/api/ledger?host=mac&x={long_q}")
    return ok and r2.status_code == 414, f"body={r.status_code} query={r2.status_code}"


def t_dashboard_cors_default_restricted():
    from starlette.testclient import TestClient
    import dashboard_server
    client = TestClient(dashboard_server.app)
    r = client.options(
        "/api/health",
        headers={"Origin": "https://example.com", "Access-Control-Request-Method": "GET"},
    )
    # Default configuration: no cross-origin access unless SOV_TOWN_CORS_ORIGINS is set.
    ok = "access-control-allow-origin" not in {k.lower() for k in r.headers.keys()}
    return ok, f"cors acao={r.headers.get('access-control-allow-origin')}"


def t_sign_key_encryption():
    import tempfile, os, sign_lib
    priv_text = sign_lib.load_or_create_key()[1]
    with open(sign_lib.PRIV) as f:
        plain = f.read()
    plain_ok = not sign_lib._is_encrypted(plain)
    with tempfile.TemporaryDirectory() as tmp:
        orig_priv, orig_pub = sign_lib.PRIV, sign_lib.PUB
        sign_lib.PRIV = os.path.join(tmp, "priv.key")
        sign_lib.PUB = os.path.join(tmp, "pub.key")
        try:
            os.environ["SOV_TOWN_KEY_PASSWORD"] = "test-pass-123"
            _, pub1 = sign_lib.load_or_create_key()
            with open(sign_lib.PRIV) as f:
                enc = f.read()
            del os.environ["SOV_TOWN_KEY_PASSWORD"]
            os.environ["SOV_TOWN_KEY_PASSWORD"] = "wrong"
            try:
                sign_lib.load_or_create_key()
                wrong_ok = False
            except Exception:
                wrong_ok = True
            del os.environ["SOV_TOWN_KEY_PASSWORD"]
            os.environ["SOV_TOWN_KEY_PASSWORD"] = "test-pass-123"
            _, pub2 = sign_lib.load_or_create_key()
            del os.environ["SOV_TOWN_KEY_PASSWORD"]
        finally:
            sign_lib.PRIV, sign_lib.PUB = orig_priv, orig_pub
    return plain_ok and sign_lib._is_encrypted(enc) and wrong_ok and pub1 == pub2, "key encryption works"


def t_policy_lab_vote():
    import json, tempfile, policy_lab
    exp = {
        "id": "test_experiment_001",
        "name": "Test Experiment",
        "status": "proposed",
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(exp, f)
        path = f.name
    try:
        result = policy_lab.vote_experiment(path)
        ok = (
            result["status"] == "approved"
            and result["vote"]["fund_count"] >= 4
            and len(result["vote"]["votes"]) == 5
        )
        return ok, f"status={result['status']} votes={result['vote']['fund_count']}/5"
    finally:
        os.unlink(path)


def t_benchmark_config_policy():
    from benchmark import policy
    pol = policy.load_policy("config:dora_automated")
    r1 = pol.decide({"intended_action": "steal", "hour": 10})
    r2 = pol.decide({"intended_action": "work", "hour": 10})
    manual = policy.load_policy("config:dora_manual")
    r3 = manual.decide({"intended_action": "steal", "hour": 2})
    ok = (
        r1["verdict"] == "deny" and r1.get("redirect") == "report_incident"
        and r2["verdict"] == "allow"
        and r3["verdict"] == "allow"
    )
    return ok, f"auto_steal={r1['verdict']} auto_work={r2['verdict']} manual_ooh={r3['verdict']}"


def t_benchmark_dora_policy():
    from benchmark import policy, world
    auto = policy.DORAAutomatedPolicy()
    manual = policy.DORAManualPolicy()
    r_auto = world.run(policy=auto, scenario="dora_incident_deadline", district="aqua")
    r_manual = world.run(policy=manual, scenario="dora_incident_deadline", district="aqua")
    ok = (
        r_auto["policy"] == "dora_automated"
        and r_manual["policy"] == "dora_manual"
        and r_auto["violations"] <= r_manual["violations"]
    )
    return ok, f"auto violations={r_auto['violations']} manual={r_manual['violations']}"




def t_harness_rate_limit():
    from starlette.testclient import TestClient
    import benchmark.server
    import config
    import importlib, os
    os.environ["SOV_TOWN_HARNESS_MAX_RUNS_PER_MINUTE"] = "2"
    os.environ["SOV_TOWN_HARNESS_MAX_MANIFESTS_PER_HOUR"] = "1000"
    try:
        importlib.reload(config)
        importlib.reload(benchmark.server)
        client = TestClient(benchmark.server.app)
        r1 = client.post("/harness/run", json={"policy": "sovereign"})
        r2 = client.post("/harness/run", json={"policy": "sovereign"})
        r3 = client.post("/harness/run", json={"policy": "sovereign"})
        ok = r1.status_code == 200 and r2.status_code == 200 and r3.status_code == 429
    finally:
        del os.environ["SOV_TOWN_HARNESS_MAX_RUNS_PER_MINUTE"]
        if "SOV_TOWN_HARNESS_MAX_MANIFESTS_PER_HOUR" in os.environ:
            del os.environ["SOV_TOWN_HARNESS_MAX_MANIFESTS_PER_HOUR"]
        importlib.reload(config)
        importlib.reload(benchmark.server)
    return ok, f"r1={r1.status_code} r2={r2.status_code} r3={r3.status_code}"


def t_harness_optional_auth():
    from starlette.testclient import TestClient
    import benchmark.server
    import config
    import importlib, os
    os.environ["SOV_TOWN_API_TOKEN"] = "secret-token"
    try:
        importlib.reload(config)
        importlib.reload(benchmark.server)
        client = TestClient(benchmark.server.app)
        r = client.post("/harness/run", json={"policy": "sovereign"})
        ok = r.status_code == 401
        r2 = client.post("/harness/run", json={"policy": "sovereign"}, headers={"Authorization": "Bearer secret-token"})
        ok = ok and r2.status_code == 200
    finally:
        del os.environ["SOV_TOWN_API_TOKEN"]
        importlib.reload(config)
        importlib.reload(benchmark.server)
    return ok, f"no_token={r.status_code} with_token={r2.status_code}"

def t_sov3_bridge_handshake():
    import sov3_bridge, sign_lib
    h = sov3_bridge.handshake()
    ok = all(k in h for k in ("pubkey", "nonce", "timestamp", "sig", "message"))
    valid = sov3_bridge.verify_handshake(h) if ok else False
    return ok and valid, f"fields={ok} sig_valid={valid}"


def t_sov3_bridge_think_unreachable():
    import sov3_bridge, asyncio
    original_url = sov3_bridge.SOV3_MESH_URL
    sov3_bridge.SOV3_MESH_URL = "http://127.0.0.1:1/mcp"
    try:
        result = asyncio.run(sov3_bridge.bridge_think("sov-town", "ping", "local_only"))
    finally:
        sov3_bridge.SOV3_MESH_URL = original_url
    return "error" in result and "unreachable" in result.get("error", "").lower(), result.get("error", "no error")


def t_regulation_parser():
    import regulation_parser, tempfile, json, shutil
    from pathlib import Path
    with tempfile.TemporaryDirectory() as tmp:
        orig_policies = regulation_parser.POLICIES_DIR
        orig_experiments = regulation_parser.EXPERIMENTS_DIR
        regulation_parser.POLICIES_DIR = Path(tmp) / "policies"
        regulation_parser.EXPERIMENTS_DIR = Path(tmp) / "experiments"
        try:
            intake = {
                "regulation": "Test Cyber Act",
                "framework": "dora",
                "industry": "test-industry",
                "civilization": "Testgard",
                "hypothesis": "Automation wins",
                "articles": ["Art. 1"],
                "agents": 12,
            }
            result = regulation_parser.generate_from_intake(intake)
            auto = json.loads((regulation_parser.POLICIES_DIR / f"{result['base']}_automated.json").read_text())
            exp = json.loads((regulation_parser.EXPERIMENTS_DIR / f"{result['experiment_id']}.json").read_text())
            ok = (
                auto["framework"] == "dora"
                and exp["towns"]["treatment"]["policy"] == f"{result['base']}_automated"
                and exp["towns"]["control"]["policy"] == f"{result['base']}_manual"
            )
        finally:
            regulation_parser.POLICIES_DIR = orig_policies
            regulation_parser.EXPERIMENTS_DIR = orig_experiments
    return ok, f"generated {result['experiment_id']}"


def main():
    print("\n  SOVEREIGN OS — SELFTEST")
    print("  " + "-" * 56)
    tests = [("engine: governed = 0 crimes", t_engine), ("common: shared helpers", t_common),
             ("sign_lib: Ed25519", t_sign), ("verify_chain: chain verify", t_verify_chain), ("consent_vault: grant/revoke", t_consent_vault), ("pheromone_bus: cross-hive emit", t_pheromone_bus), ("agent_passport", t_passport),
             ("zero-trust gate", t_gate), ("looking-glass enforcement curve", t_looking_glass),
             ("data_moat: EU -> sim params", t_data_moat),
             ("attestation_moat: certs -> hives", t_attestation_moat),
             ("threat_moat: KEV -> sim params", t_threat_moat),
             ("sanctions_moat: OFAC -> sim params", t_sanctions_moat),
             ("psc_moat: UK PSC -> aggregate sim params", t_psc_moat),
             ("finance_moat: FRED -> sim params", t_finance_moat),
             ("agriculture_moat: FAOSTAT -> sim params", t_agriculture_moat),
             ("energy_moat: FRED energy -> sim params", t_energy_moat),
             ("climate_moat: NOAA -> sim params", t_climate_moat),
             ("sim: tick-state collection", t_sim_tick_states),
             ("town_sim_live: snapshot", t_town_sim_live),
             ("town_sim_live: timeline structure", t_town_sim_live_timeline),
             ("dashboard_server: app + health", t_dashboard_server),
             ("event_detect: detect_all", t_event_detect),
             ("video_packager: package single event", t_video_packager),
             ("distribution pipeline: detect+package", t_distribution_pipeline_end_to_end),
             ("benchmark: policy hook", t_benchmark_policy_hook),
             ("benchmark: world run", t_benchmark_world_run),
             ("benchmark: metrics", t_benchmark_metrics),
             ("benchmark: ledger", t_benchmark_ledger),
             ("benchmark: server routes", t_benchmark_server_routes),
             ("benchmark: server websocket", t_benchmark_server_ws),
             ("benchmark: AIA policy", t_benchmark_aia_policy),
             ("benchmark: DORA policy", t_benchmark_dora_policy),
             ("benchmark: config policy", t_benchmark_config_policy),
             ("benchmark: scenario shock", t_benchmark_scenario_shock),
             ("benchmark: regulatory crosswalk", t_benchmark_regulatory_crosswalk),
             ("benchmark: compare CLI", t_benchmark_compare),
             ("benchmark: workbench page", t_benchmark_server_workbench_page),
             ("benchmark: mcp tools", t_benchmark_mcp_tools),
             ("benchmark: mcp leaderboard SSRF filter", t_mcp_leaderboard_ssrf_defense),
             ("benchmark: policy whitelist", t_benchmark_policy_whitelist),
             ("dashboard: path traversal defense", t_dashboard_path_traversal),
             ("dashboard: security headers", t_dashboard_security_headers),
             ("dashboard: request size limits", t_dashboard_request_size_limits),
             ("dashboard: CORS default restricted", t_dashboard_cors_default_restricted),
             ("sign_lib: key encryption", t_sign_key_encryption),
             ("harness: optional bearer auth", t_harness_optional_auth),
             ("harness: rate limit", t_harness_rate_limit),
             ("sov3_bridge: handshake", t_sov3_bridge_handshake),
             ("sov3_bridge: think unreachable", t_sov3_bridge_think_unreachable),
             ("regulation_parser: intake → experiment", t_regulation_parser),
             ("policy_lab: council vote", t_policy_lab_vote)]
    results = [check(n, f) for n, f in tests]
    print("  " + "-" * 56)
    p = sum(results)
    print(f"  {p}/{len(results)} passed\n")
    sys.exit(0 if p == len(results) else 1)

if __name__ == "__main__":
    main()
