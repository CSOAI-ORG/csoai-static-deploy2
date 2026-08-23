"""Tests for meok-sovereign-digital-twin-mcp — sovereign globe + 22 arcana + 33 districts."""
import os, sys, tempfile, importlib
_TEST = tempfile.mkdtemp(prefix="sov_twin_")
os.environ["SOV_TWIN_KEY"] = _TEST + "/k.pem"


def get_fresh():
    if "meok_sovereign_digital_twin_mcp" in sys.modules:
        del sys.modules["meok_sovereign_digital_twin_mcp"]
    import meok_sovereign_digital_twin_mcp as m
    importlib.reload(m)
    return m


def test_globe_init_default():
    m = get_fresh()
    r = m.twin_globe_init()
    assert r["protocol"] == "sovereign-digital-twin/1.0"
    assert r["districts_count"] == 33
    assert r["arcana_count"] == 22
    assert "real" in r["layers"]


def test_globe_init_with_rotation():
    m = get_fresh()
    r = m.twin_globe_init(rotation=45.5)
    assert r["globe"]["rotation"] == 45.5


def test_visualize_default_layer():
    m = get_fresh()
    m.twin_globe_init()
    r = m.twin_visualize()
    assert r["view"]["layer"] == "real"
    assert r["view"]["fps"] == 60
    assert "view_id" in r["view"]


def test_visualize_unknown_layer():
    m = get_fresh()
    r = m.twin_visualize(layer="bogus")
    assert "error" in r
    assert "unknown layer" in r["error"]


def test_visualize_all_layers():
    m = get_fresh()
    m.twin_globe_init()
    for layer in ("real", "urban", "isr", "network", "swarm", "weather", "ontology"):
        r = m.twin_visualize(layer=layer)
        assert r["view"]["layer"] == layer


def test_layer_set():
    m = get_fresh()
    m.twin_globe_init()
    r = m.twin_layer_set(layer="isr")
    assert r["active_layer"] == "isr"
    s = m.twin_status()
    assert s["active_layer"] == "isr"


def test_layer_set_unknown():
    m = get_fresh()
    r = m.twin_layer_set(layer="bogus")
    assert "error" in r


def test_ontology_has_22_arcana_33_districts():
    m = get_fresh()
    r = m.twin_ontology()
    assert r["arcana_count"] == 22
    assert r["districts_count"] == 33
    assert len(r["arcana"]) == 22
    assert len(r["districts"]) == 33
    # arcana[0] is "The Sovereign"
    assert "Sovereign" in r["arcana"][0]["name"]


def test_status_has_engine_and_districts():
    m = get_fresh()
    m.twin_globe_init()
    r = m.twin_status()
    assert r["globe_initialized"] is True
    assert r["districts"] == 33
    assert r["arcana"] == 22
    assert "Cesium" in r["engine"] or "Unreal" in r["engine"]


def test_no_external_deps():
    m = get_fresh()
    src = open(m.__file__).read()
    for blocked in ["ollama", "requests", "urllib.request", "httpx"]:
        assert f"import {blocked}" not in src


def test_signed_outputs_have_kid_sig_ts():
    m = get_fresh()
    for r in [m.twin_globe_init(), m.twin_visualize(), m.twin_layer_set("urban"),
              m.twin_ontology(), m.twin_status()]:
        assert "kid" in r and "sig" in r and "ts" in r


def test_full_workflow():
    """init → visualize → layer_set → visualize new layer → ontology → status."""
    m = get_fresh()
    init = m.twin_globe_init(rotation=30.0)
    assert init["districts_count"] == 33
    v1 = m.twin_visualize(layer="real")
    assert v1["view"]["layer"] == "real"
    ls = m.twin_layer_set(layer="urban")
    assert ls["active_layer"] == "urban"
    v2 = m.twin_visualize(layer="urban")
    assert v2["view"]["layer"] == "urban"
    ont = m.twin_ontology()
    assert ont["arcana_count"] == 22
    st = m.twin_status()
    assert st["views_rendered"] == 2
    assert st["active_layer"] == "urban"