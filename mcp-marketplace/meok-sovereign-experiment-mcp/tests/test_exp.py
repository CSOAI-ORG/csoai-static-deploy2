import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import meok_sovereign_experiment_mcp as m
from meok_sovereign_experiment_mcp import (
    exp_register, exp_record, exp_analyze, exp_list, exp_conclude,
    EXPERIMENTS, USABLE_N, _wilson,
)

def setup():
    EXPERIMENTS.clear()

def test_register_basic():
    setup()
    items = [f"item_{i}" for i in range(40)]
    r = exp_register(control="qwen2.5:0.5b", variant="sov-refusal-combo-lora",
                     axis="governance", items=items, hypothesis="sov wins")
    assert r["eid"].startswith("e-")
    assert r["control"] == "qwen2.5:0.5b"
    assert "results" in r and r["results"] == []
    assert r["status"] == "registered"

def test_record_and_analyze_insufficient():
    setup()
    items = [f"item_{i}" for i in range(40)]
    r = exp_register(control="c", variant="v", axis="art5", items=items)
    eid = r["eid"]
    for i in range(5):
        exp_record(eid, f"item_{i}", "control", True, False)
    a = exp_analyze(eid)
    assert a["n"] == 5
    assert a["label"] == "UNMEASURED"
    assert a["verdict"] == "INSUFFICIENT_SAMPLES"

def test_analyze_variant_wins():
    setup()
    items = [f"item_{i}" for i in range(40)]
    r = exp_register(control="c", variant="v", axis="care", items=items)
    eid = r["eid"]
    for i in range(25):
        exp_record(eid, f"item_{i}", "variant", False, True)
    for i in range(25, 30):
        exp_record(eid, f"item_{i}", "control", True, False)
    for i in range(30, 35):
        exp_record(eid, f"item_{i}", "tie", True, True)
    a = exp_analyze(eid)
    assert a["n"] == 35
    assert a["label"] == "MEASURED"
    assert a["verdict"] == "VARIANT_WINS"
    assert a["mcnemar_p"] < 0.05

def test_analyze_no_significant_difference():
    setup()
    items = [f"item_{i}" for i in range(40)]
    r = exp_register(control="c", variant="v", axis="provenance", items=items)
    eid = r["eid"]
    for i in range(35):
        correct = (i % 2 == 0)
        exp_record(eid, f"item_{i}", "tie", correct, correct)
    a = exp_analyze(eid)
    assert a["n"] == 35
    assert a["label"] == "MEASURED"
    assert a["verdict"] == "NO_SIGNIFICANT_DIFFERENCE"

def test_analyze_control_wins():
    setup()
    items = [f"item_{i}" for i in range(40)]
    r = exp_register(control="c", variant="v", axis="safety", items=items)
    eid = r["eid"]
    for i in range(35):
        exp_record(eid, f"item_{i}", "control", True, False)
    a = exp_analyze(eid)
    assert a["verdict"] == "CONTROL_WINS"

def test_list():
    setup()
    n_before = len(exp_list()["experiments"])
    items = [f"item_{i}" for i in range(40)]
    exp_register(control="c", variant="v", axis="care", items=items)
    n_after = len(exp_list()["experiments"])
    assert n_after == n_before + 1

def test_conclude_signed():
    setup()
    items = [f"item_{i}" for i in range(40)]
    r = exp_register(control="c", variant="v", axis="art5", items=items)
    eid = r["eid"]
    for i in range(35):
        exp_record(eid, f"item_{i}", "variant", False, True)
    c = exp_conclude(eid, signer="sovereign-council")
    assert c["conclusion_sig"] != c["conclusion_kid"]
    assert len(c["conclusion_sig"]) == 32
    assert c["verdict"] == "VARIANT_WINS"
    assert c["signer"] == "sovereign-council"

def test_conclude_insufficient():
    setup()
    items = [f"item_{i}" for i in range(40)]
    r = exp_register(control="c", variant="v", axis="art5", items=items)
    eid = r["eid"]
    exp_record(eid, "item_0", "variant", False, True)
    c = exp_conclude(eid)
    assert "error" in c

def test_record_unknown_eid():
    setup()
    r = exp_record("e-doesnotexist", "x", "control", True, False)
    assert "error" in r

def test_wilson_zero():
    lo, hi, p = _wilson(0, 0)
    assert p == 0.0
    assert lo == 0.0 and hi == 0.0

def test_wilson_basic():
    lo, hi, p = _wilson(70, 100)
    assert 0.6 < p < 0.8
    assert lo < p < hi
    assert 0 < lo < 1 and 0 < hi < 1
