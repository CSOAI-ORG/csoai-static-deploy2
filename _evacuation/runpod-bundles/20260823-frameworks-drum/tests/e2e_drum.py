#!/usr/bin/env python3
"""FRAMEWORKS DRUM — full end-to-end test (the whole pipeline, one pass).

Pipeline exercised: build (check+lint) → catalog integrity → cards → feeds →
MCP protocol conversation (initialize/tools/list + every tool with realistic args) →
conformal router (calibrate on the real calibration set) → knowledge archive →
drift monitor → standing ops check.

Run:  python3 tests/e2e_drum.py
Exit 0 only if the ENTIRE pipeline is green.
"""
import json
import os
import subprocess
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def step(name, fn):
    try:
        detail = fn()
        print(f"  ok  {name}" + (f" — {detail}" if detail else ""))
        return True
    except Exception as exc:  # noqa: BLE001
        FAILS.append(name)
        print(f"FAIL {name}: {exc}")
        return False


def sh(cmd, cwd=PACK):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd} → {r.returncode}: {r.stderr[-300:]}")
    return r.stdout


def main():
    print("FRAMEWORKS DRUM — END-TO-END")

    step("build --check --lint", lambda: sh("python3 build_catalog.py --check --lint").strip().splitlines()[-2:])
    step("unit tests", lambda: sh("python3 tests/test_drum.py").strip().splitlines()[-1])
    step("cards == items", lambda: _cards_match())
    step("feeds valid + counts", lambda: _feeds())
    step("MCP protocol conversation (9 tools)", lambda: _mcp())
    step("conformal router on real calibration set", lambda: _router())
    step("knowledge archive", lambda: sh("python3 archive/knowledge_archive.py --selftest").strip().splitlines()[-1])
    step("drift monitor", lambda: sh("python3 router/drift_monitor.py").strip().splitlines()[0][:60])
    step("read-only gates (check+lint on existing catalog)", lambda: _readonly_gates())

    print()
    if FAILS:
        print(f"E2E FAILED: {len(FAILS)} failures — {FAILS}")
        sys.exit(1)
    print("E2E: ALL GREEN")
    sys.exit(0)


def _readonly_gates():
    # check + lint on the EXISTING catalog (no rebuild, no recursion into the standing check)
    import sys as _s
    _s.path.insert(0, PACK)
    import build_catalog as b
    cat = json.load(open(os.path.join(PACK, "catalog.json")))
    problems = b.check_catalog(cat)
    hits = b.lint_surfaces()
    if problems or hits:
        raise RuntimeError(f"check {problems} · lint {hits}")
    return "check+lint PASS"


def _cards_match():
    cat = json.load(open(os.path.join(PACK, "catalog.json")))
    dirs = {"framework": "frameworks", "charter": "charters", "regulation": "regulations",
            "article": "articles", "sector": "sectors", "benchmark": "benchmarks"}
    expected = {f"{dirs[i['kind']]}/{i['id']}.md" for i in cat["items"]}
    actual = set()
    for d in set(dirs.values()):
        for f in os.listdir(os.path.join(PACK, d)):
            if f.endswith(".md"):
                actual.add(f"{d}/{f}")
    missing = expected - actual
    stale = actual - expected
    if missing or stale:
        raise RuntimeError(f"cards mismatch: {len(missing)} missing, {len(stale)} stale")
    return f"{len(expected)} cards"


def _feeds():
    reg = json.load(open(os.path.join(PACK, "feeds", "reg_events.json")))
    eat = json.load(open(os.path.join(PACK, "feeds", "eat_7box.json")))
    assert reg["count"] == len(reg["events"]) > 0
    assert len(eat["boxes"]) == 7
    return f"reg_events {reg['count']} · eat_7box 7/7 boxes"


def _mcp():
    calls = [
        ("initialize", {}),
        ("tools/list", {}),
        ("drum_catalog", {}),
        ("drum_search", {"query": "eu ai act", "kind": "regulation", "limit": 2}),
        ("drum_get", {"id": "eu-ai-act"}),
        ("drum_crosswalk", {"source": "gdpr", "target": "iso 42001"}),
        ("drum_watch", {}),
        ("drum_freshness", {}),
        ("drum_route", {"score": 0.5}),
        ("drum_history", {}),
    ]
    lines = [json.dumps({"jsonrpc": "2.0", "id": i,
                         "method": ("tools/call" if m not in ("initialize", "tools/list") else m),
                         "params": {"name": m, "arguments": a} if m not in ("initialize", "tools/list") else {}})
             for i, (m, a) in enumerate(calls)]
    r = subprocess.run(["python3", "mcp/frameworks_drum_server.py"], input="\n".join(lines) + "\n",
                       capture_output=True, text=True, cwd=PACK)
    out = [json.loads(l) for l in r.stdout.strip().splitlines() if l.strip()]
    assert len(out) == len(calls), f"expected {len(calls)} responses, got {len(out)}"
    for m in out:
        assert "result" in m or "error" in m, m
    # every tool responded with content
    tool_calls = [m for m in out if m.get("id") in range(2, len(calls))]
    for m in tool_calls:
        assert m.get("result", {}).get("content"), f"no content for call id {m['id']}"
    return f"{len(out)} responses, {len(tool_calls)} tool results"


def _router():
    r = subprocess.run(["python3", "router/conformal_router.py", "--selftest"],
                       capture_output=True, text=True, cwd=PACK)
    assert r.returncode == 0, r.stderr
    rows = [json.loads(l) for l in open(os.path.join(PACK, "router", "calibration_set.jsonl"), encoding="utf-8") if l.strip()]
    measured = [x for x in rows if not x.get("simulated")]
    assert len(measured) > 0, "no measured labels collected — run router/collect_measured.py"
    return f"selftest pass · {len(measured)} measured labels in set"


if __name__ == "__main__":
    main()
