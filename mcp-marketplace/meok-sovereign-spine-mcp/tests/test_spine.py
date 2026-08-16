"""Tests for meok-sovereign-spine-mcp."""
import os, sys, importlib.util, json

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "meok_sovereign_spine_mcp")

# Add PKG to sys.path so 'import spine_v2' works inside __init__.py
sys.path.insert(0, PKG)

# Load spine_v2 directly
spec = importlib.util.spec_from_file_location("spine_v2", os.path.join(PKG, "spine_v2.py"))
spine_v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spine_v2)

# Load MCP wrapper
spec2 = importlib.util.spec_from_file_location("mcp_spine", os.path.join(PKG, "__init__.py"))
mcp = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(mcp)


def test_canonical_json_roundtrip():
    p = {"b": 2, "a": 1, "c": {"z": 26, "y": 25}}
    r = mcp.mcp_canonical_json(p)
    canon = r["canonical"]
    assert json.loads(canon) == p, "roundtrip mismatch"
    assert canon == '{"a":1,"b":2,"c":{"y":25,"z":26}}', f"unexpected canonical form: {canon}"


def test_content_hash_deterministic():
    p = {"a": 1, "b": 2}
    c1 = mcp.mcp_content_hash(p)["cid"]
    c2 = mcp.mcp_content_hash(p)["cid"]
    assert c1 == c2
    assert c1.startswith("sha256:")


def test_sign_and_verify_card():
    payload = {"axis": "governance", "metric": "win_rate", "value": 0.54,
               "n": 237, "ci95": [0.476, 0.602], "p_value": 0.0001}
    card = mcp.mcp_sign_card("measurement", payload)
    assert card["cid"].startswith("sha256:")
    assert card["kind"] == "measurement"
    assert card["payload"] == payload
    v = mcp.mcp_verify_card(card)
    assert v["valid"], v


def test_verify_tamper_detection():
    payload = {"axis": "art5", "metric": "compliance", "value": 0.94,
               "n": 36, "ci95": [0.819, 0.985], "p_value": 0.0001}
    card = mcp.mcp_sign_card("measurement", payload)
    tampered = dict(card)
    tampered["payload"] = dict(card["payload"])
    tampered["payload"]["value"] = 0.99
    v = mcp.mcp_verify_card(tampered)
    assert not v["valid"]
    assert v["reason"] == "cid_mismatch"


def test_recompute_check():
    payload = {"ts": "2026-08-15T05:00:00Z", "mode": "ai-vs-ai",
               "probe": "Article 50 transparency test",
               "left": {"name": "clan-x", "verdict": "YES"},
               "right": {"name": "clan-y", "verdict": "YES"},
               "agreement": True}
    card = mcp.mcp_sign_card("arena-round", payload)
    rc = mcp.mcp_recompute_check(card["cid"])
    assert rc["in_ledger"]
    assert rc["valid"]


def test_recompute_check_unknown_cid():
    rc = mcp.mcp_recompute_check("sha256:0000000000000000")
    assert not rc["in_ledger"]


def test_register_kind_idempotent():
    r1 = mcp.mcp_register_kind("test-kind", {"x": "int"}, "test desc")
    r2 = mcp.mcp_register_kind("test-kind", {"x": "int"}, "test desc")
    assert r1["status"] == "registered"
    assert r2["status"] == "already_registered"


def test_list_kinds_has_5_standard():
    kinds = mcp.mcp_list_kinds()
    names = [k["name"] for k in kinds["kinds"]]
    for n in ["measurement", "arena-round", "honey-data", "provenance", "charter"]:
        assert n in names, f"missing kind: {n}"


def test_honey_data_card():
    payload = {"ts": "2026-08-15T05:00:00Z", "kind": "prompt_response",
               "input": {"prompt": "hello"}, "output": {"response": "world"},
               "model": "qwen2.5:0.5b", "weights_cid": "sha256:abc",
               "training_eligible": True}
    card = mcp.mcp_sign_card("honey-data", payload)
    v = mcp.mcp_verify_card(card)
    assert v["valid"]


def test_arena_round_card():
    payload = {"ts": "2026-08-15T04:00:00Z", "mode": "human-vs-ai",
               "probe": "EU AI Act Article 50 transparency duty test",
               "left": {"name": "human", "verdict": "NO",
                        "role": "policy officer, lived judgement"},
               "right": {"name": "clan-csoai-cited:latest", "verdict": "YES"},
               "agreement": False}
    card = mcp.mcp_sign_card("arena-round", payload)
    v = mcp.mcp_verify_card(card)
    assert v["valid"]


def test_list_cards_filter_by_kind():
    payload = {"axis": "care", "metric": "compliance", "value": 0.7,
               "n": 12, "ci95": [0.5, 0.85], "p_value": None}
    mcp.mcp_sign_card("measurement", payload)
    payload2 = {"subject_cid": "sha256:abc", "builder": "test",
                "build_instructions": "echo hi", "inputs": ["sha256:def"], "ts": "2026-08-15T05:00:00Z"}
    mcp.mcp_sign_card("provenance", payload2)
    m_only = mcp.mcp_list_cards(kind="measurement")
    p_only = mcp.mcp_list_cards(kind="provenance")
    assert m_only["count"] >= 1
    assert p_only["count"] >= 1


def test_5_standard_kinds_signable():
    now = "2026-08-15T05:00:00Z"
    payloads = {
        "measurement": {"axis": "x", "metric": "y", "value": 0.5,
                        "n": 30, "ci95": [0.3, 0.7], "p_value": 0.1},
        "arena-round": {"ts": now, "mode": "ai-vs-ai", "probe": "test",
                        "left": {"name": "a", "verdict": "YES"},
                        "right": {"name": "b", "verdict": "YES"}, "agreement": True},
        "honey-data": {"ts": now, "kind": "prompt_response",
                       "input": {"p": "x"}, "output": {"r": "y"},
                       "model": "m", "weights_cid": "sha256:w",
                       "training_eligible": True},
        "provenance": {"subject_cid": "sha256:s", "builder": "b",
                       "build_instructions": "i", "inputs": ["sha256:x"], "ts": now},
        "charter": {"ts": now, "council": "c33", "decision": "ship",
                    "votes": {"yes": 25, "no": 5, "abstain": 3}, "quorum_met": True},
    }
    for kind, payload in payloads.items():
        card = mcp.mcp_sign_card(kind, payload)
        v = mcp.mcp_verify_card(card)
        assert v["valid"], f"{kind} failed: {v}"
