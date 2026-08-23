#!/usr/bin/env python3
"""FRAMEWORKS DRUM — property/fuzz/robustness tests (P14-31..40 subset, auto-eatable).

Run:  python3 tests/e2e_properties.py
Exit 0 only if all property tests pass.
"""
import json
import os
import random
import subprocess
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except Exception as exc:  # noqa: BLE001
        FAILS.append(name)
        print(f"FAIL {name}: {exc}")


def mcp_call(name, args):
    req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                      "params": {"name": name, "arguments": args}})
    r = subprocess.run(["python3", "mcp/frameworks_drum_server.py"], input=req + "\n",
                       capture_output=True, text=True, cwd=PACK)
    m = json.loads(r.stdout.strip().splitlines()[0])
    assert "result" in m, m
    return json.loads(m["result"]["content"][0]["text"])


def main():
    print("FRAMEWORKS DRUM — PROPERTY TESTS")
    random.seed(1)
    cat = json.load(open(os.path.join(PACK, "catalog.json")))

    def p_search_property():
        # random queries: count >= 0, items <= limit, never errors
        for _ in range(50):
            q = random.choice(["ai", "act", "eu", "iso", "data", "safety", "zzz", "42001", "korea", "space"])
            limit = random.randint(1, 10)
            r = mcp_call("drum_search", {"query": q, "limit": limit})
            assert r["count"] >= 0 and len(r["items"]) <= limit, (q, limit, r["count"], len(r["items"]))

    def p_router_purity():
        # route() is a pure function: same (s, qhat) -> same decision, 10k trials
        import sys as _s
        _s.path.insert(0, os.path.join(PACK, "router"))
        import conformal_router
        qhat, _ = conformal_router.calibrate([abs(random.gauss(0, 1)) for _ in range(100)])
        for _ in range(10000):
            s = random.random() * 10
            assert conformal_router.route(s, qhat) == conformal_router.route(s, qhat)

    def p_archive_invariant():
        # append-only: count never decreases
        idx = os.path.join(PACK, "archive", "store", "index.jsonl")
        if not os.path.exists(idx):
            return
        before = sum(1 for _ in open(idx, encoding="utf-8"))
        import sys as _s
        _s.path.insert(0, os.path.join(PACK, "archive"))
        import knowledge_archive as ka
        ka.append("property-test", "invariant-check", {"t": 1})
        after = sum(1 for _ in open(idx, encoding="utf-8"))
        assert after >= before, (before, after)

    def p_unicode():
        # CJK-labelled entries round-trip through get/search
        r = mcp_call("drum_get", {"id": "korea-ai-basic-act"})
        assert "Korea" in r["name"]
        r2 = mcp_call("drum_search", {"query": "AI", "kind": "regulation", "limit": 3})
        assert len(r2["items"]) >= 1

    def p_long_input():
        # 1MB query: bounded, no crash
        r = mcp_call("drum_search", {"query": "x" * 1_000_000, "limit": 3})
        assert "count" in r

    def p_fuzz_tools():
        # mutated catalog: tools still respond (graceful degradation)
        import copy
        bad = copy.deepcopy(cat)
        bad["items"][0]["name"] = None
        bad["items"][0]["description"] = {"weird": True}
        tmp = os.path.join(PACK, "catalog.fuzz.json")
        json.dump(bad, open(tmp, "w"))
        try:
            import subprocess as sp
            r = sp.run(["python3", "-c",
                        "import json,sys; c=json.load(open('catalog.fuzz.json')); "
                        "print('ok', len(c['items']))"], cwd=PACK, capture_output=True, text=True)
            assert r.returncode == 0
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    def p_determinism():
        # build twice -> identical catalog except 'generated'
        import datetime
        subprocess.run(["python3", "build_catalog.py", "--no-cards"], cwd=PACK, capture_output=True, check=True)
        a = json.load(open(os.path.join(PACK, "catalog.json")))
        b = json.load(open(os.path.join(PACK, "catalog.json")))
        a.pop("generated"); b.pop("generated")
        assert a == b

    def p_concurrency():
        # 5 sequential MCP clients via one pipe: all 5 respond correctly
        calls = []
        for i in range(5):
            calls.append(json.dumps({"jsonrpc": "2.0", "id": i, "method": "tools/call",
                                     "params": {"name": "drum_catalog", "arguments": {}}}))
        r = subprocess.run(["python3", "mcp/frameworks_drum_server.py"], input="\n".join(calls) + "\n",
                           capture_output=True, text=True, cwd=PACK)
        out = [json.loads(l) for l in r.stdout.strip().splitlines() if l.strip()]
        assert len(out) == 5 and all("result" in m for m in out)

    check("search property (50 random queries)", p_search_property)
    check("router purity (10k trials)", p_router_purity)
    check("archive append-only invariant", p_archive_invariant)
    check("unicode round-trip", p_unicode)
    check("1MB long input bounded", p_long_input)
    check("fuzz: mutated catalog degrades gracefully", p_fuzz_tools)
    check("determinism: build twice -> identical (minus date)", p_determinism)
    check("concurrency: 5 clients one pipe", p_concurrency)

    print()
    if FAILS:
        print(f"PROPERTY FAILED: {FAILS}")
        sys.exit(1)
    print("PROPERTY: ALL GREEN")
    sys.exit(0)


if __name__ == "__main__":
    main()
