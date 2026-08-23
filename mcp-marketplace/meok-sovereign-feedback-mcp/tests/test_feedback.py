import importlib, os, sys, tempfile


def test_smoke():
    os.environ["SOV_KEY"] = tempfile.mkdtemp() + "/k.pem"
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
    if "meok_sovereign_feedback_mcp" in sys.modules: del sys.modules["meok_sovereign_feedback_mcp"]
    m = importlib.import_module("meok_sovereign_feedback_mcp"); importlib.reload(m)
    r = m.feedback_status()
    assert "kid" in r and "sig" in r
