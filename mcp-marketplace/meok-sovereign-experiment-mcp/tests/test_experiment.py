"""Tests for meok-sovereign-experiment-mcp — A/B experiment harness with Wilson CI + McNemar exact."""
import os, sys, tempfile, importlib
_TEST = tempfile.mkdtemp(prefix="sov_exp_")
os.environ["SOV_EXP_KEY"] = _TEST + "/k.pem"


def get_fresh():
    if "meok_sovereign_experiment_mcp" in sys.modules:
        del sys.modules["meok_sovereign_experiment_mcp"]
    import meok_sovereign_experiment_mcp as m
    importlib.reload(m)
    return m


def test_register_basic():
    m = get_fresh()
    r = m.exp_register(
        control="qwen2.5:7b", variant="council-safe:latest",
        axis="safety", items=["i1", "i2", "i3"], hypothesis="council beats base"
    )
    assert r["eid"].startswith("e-")
    assert r["control"] == "qwen2.5:7b"
    assert r["variant"] == "council-safe:latest"
    assert r["axis"] == "safety"
    assert len(r["items"]) == 3
    assert r["status"] == "registered"


def test_register_no_eid_then_use_provided():
    m = get_fresh()
    r = m.exp_register(
        control="a", variant="b", axis="prov", items=["x"], eid="e-custom"
    )
    assert r["eid"] == "e-custom"


def test_record_one():
    m = get_fresh()
    r = m.exp_register("c", "v", "ax", ["i1", "i2"])
    rec = m.exp_record(r["eid"], "i1", winner="variant",
                       control_correct=True, variant_correct=False)
    assert "recorded" in rec
    assert rec["n"] == 1
    assert rec["recorded"]["agree"] is False


def test_record_unknown_eid():
    m = get_fresh()
    r = m.exp_record("e-nope", "i1", winner="control",
                     control_correct=True, variant_correct=False)
    assert "error" in r


def test_analyze_insufficient_samples():
    m = get_fresh()
    r = m.exp_register("c", "v", "ax", ["i1"])
    rec = m.exp_record(r["eid"], "i1", winner="control",
                       control_correct=True, variant_correct=False)
    a = m.exp_analyze(r["eid"])
    assert a["n"] == 1
    assert a["label"] == "UNMEASURED"
    assert a["verdict"] == "INSUFFICIENT_SAMPLES"


def test_analyze_with_enough_samples_no_significant_diff():
    m = get_fresh()
    items = [f"i{i}" for i in range(60)]
    r = m.exp_register("c", "v", "prov", items)
    eid = r["eid"]
    # 30 control wins, 30 variant wins (no significant diff)
    for i in range(60):
        winner = "control" if i < 30 else "variant"
        m.exp_record(eid, items[i], winner=winner,
                     control_correct=(i < 30), variant_correct=(i >= 30))
    a = m.exp_analyze(eid)
    assert a["n"] == 60
    assert a["label"] == "MEASURED"
    assert a["control"]["wins"] == 30
    assert a["variant"]["wins"] == 30
    # win rates should be ~0.5 each
    assert 0.45 <= a["control"]["win_rate"] <= 0.55
    assert 0.45 <= a["variant"]["win_rate"] <= 0.55
    # mcNemar should be high (no significant diff)
    assert a["mcnemar_p"] > 0.05


def test_analyze_variant_wins_significantly():
    m = get_fresh()
    items = [f"i{i}" for i in range(60)]
    r = m.exp_register("c", "v", "prov", items)
    eid = r["eid"]
    # variant wins 50, control wins 10 (variant wins significantly)
    for i in range(60):
        winner = "variant" if i < 50 else "control"
        m.exp_record(eid, items[i], winner=winner,
                     control_correct=(i >= 50), variant_correct=(i < 50))
    a = m.exp_analyze(eid)
    assert a["label"] == "MEASURED"
    assert a["variant"]["wins"] == 50
    assert a["control"]["wins"] == 10
    assert a["verdict"] == "VARIANT_WINS"


def test_list_experiments():
    m = get_fresh()
    m.exp_register("c1", "v1", "ax1", ["i"])
    m.exp_register("c2", "v2", "ax2", ["i"])
    r = m.exp_list()
    assert r["count"] == 2
    assert len(r["experiments"]) == 2


def test_conclude_with_insufficient_samples():
    m = get_fresh()
    r = m.exp_register("c", "v", "ax", ["i"])
    c = m.exp_conclude(r["eid"])
    assert "error" in c


def test_conclude_full_flow():
    m = get_fresh()
    items = [f"i{i}" for i in range(60)]
    r = m.exp_register("c", "v", "prov", items, hypothesis="v wins")
    eid = r["eid"]
    for i in range(60):
        m.exp_record(eid, items[i], winner="variant",
                     control_correct=False, variant_correct=True)
    c = m.exp_conclude(eid, signer="council-bft")
    assert c["verdict"] == "VARIANT_WINS"
    assert c["signer"] == "council-bft"
    assert "conclusion_sig" in c
    assert "conclusion_kid" in c


def test_no_external_deps():
    m = get_fresh()
    src = open(m.__file__).read()
    for blocked in ["ollama", "requests", "urllib.request", "httpx"]:
        assert f"import {blocked}" not in src


def test_signed_outputs_have_kid_sig_ts():
    m = get_fresh()
    r = m.exp_register("c", "v", "ax", ["i"])
    assert "kid" in r and "sig" in r and "ts" in r
    rec = m.exp_record(r["eid"], "i", winner="control",
                       control_correct=True, variant_correct=False)
    assert "kid" in rec and "sig" in rec
    lst = m.exp_list()
    assert "kid" in lst and "sig" in lst


def test_full_workflow():
    """exp_register → 60 records → exp_analyze → exp_conclude → exp_list."""
    m = get_fresh()
    items = [f"q{i}" for i in range(60)]
    r = m.exp_register("base", "sov", "care", items, hypothesis="sov care better")
    eid = r["eid"]
    for i in range(60):
        m.exp_record(eid, items[i], winner="variant",
                     control_correct=False, variant_correct=True)
    a = m.exp_analyze(eid)
    assert a["verdict"] == "VARIANT_WINS"
    c = m.exp_conclude(eid, signer="round-table")
    assert "conclusion_sig" in c
    lst = m.exp_list()
    matching = [x for x in lst["experiments"] if x["eid"] == eid]
    assert len(matching) == 1
    assert matching[0]["label"] == "MEASURED"