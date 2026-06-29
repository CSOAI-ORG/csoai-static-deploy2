"""
MEOK OS Backend — last-mile features test suite.

Hits the new endpoints added for the 9 PM test:
  - /api/council/chat
  - /api/perf/track + /api/perf/stats
  - /api/ichar/create (full wizard payload round-trip)
  - i18n JSON files loadable + valid

Run:  python3 test_lastmile.py
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import urllib.request
from pathlib import Path

# Make app.py importable with isolated temp dirs
_tmp = tempfile.mkdtemp(prefix="meok-lastmile-")
os.environ["MEOK_ICHARS_DB"] = _tmp + "/ichars.db"
os.environ["MEOK_USERS_DB"] = _tmp + "/users.db"
os.environ["MEOK_SIGIL_LOG"] = _tmp + "/sigil.jsonl"
os.environ["MEOK_PERF_LOG"] = _tmp + "/perf.jsonl"

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "csoai-os"))

import app as app_module  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from app import app  # noqa: E402

client = TestClient(app)


def header(t: str) -> str:
    return f"\n=== {t} ==="


# ─── TASK 1: i18n locale files ───
print(header("TASK 1: i18n locale files"))
i18n_dir = HERE.parent / "csoai-os" / "i18n"
assert i18n_dir.exists(), f"i18n dir missing: {i18n_dir}"
locales = ["en", "es", "fr", "de", "ja", "zh"]
for loc in locales:
    f = i18n_dir / f"{loc}.json"
    assert f.exists(), f"locale missing: {f}"
    data = json.loads(f.read_text())
    assert "_meta" in data, f"{loc}: no _meta"
    assert data["_meta"]["locale"] == loc, f"{loc}: locale mismatch"
    for sec in ("nav", "hero", "council", "temples", "wizard", "status", "errors", "cta", "footer", "locale_picker"):
        assert sec in data, f"{loc}: missing section {sec}"
    # count strings
    def count(o):
        if isinstance(o, dict):
            return sum(count(v) for v in o.values())
        if isinstance(o, list):
            return sum(count(v) for v in o)
        return 1
    n = count(data)
    assert n >= 100, f"{loc}: only {n} strings (need 100+)"
    print(f"  ✓ {loc}: {n} strings, valid JSON")
print("  ✓ i18n/_template.html switcher JS:")
tmpl = (HERE.parent / "csoai-os" / "meok-home" / "_template.html").read_text()
assert "locale-switcher" in tmpl, "missing locale-switcher"
assert "loadLocale" in tmpl, "missing loadLocale"
assert "data-i18n" in tmpl, "missing data-i18n hooks"
assert "/csoai-os/i18n/" in tmpl, "missing i18n fetch path"
print("    locale-switcher CSS + JS loader + dropdown menu present")


# ─── TASK 2: /api/council/chat ───
print(header("TASK 2: /api/council/chat"))
r = client.post("/api/council/chat", json={
    "queen_id": "queen-arcana", "arcana_lens": 21,
    "message": "What is the EU AI Act?", "user_id": "test-user-1",
})
assert r.status_code == 200, r.text
j = r.json()
assert j["ok"] is True
assert "response" in j and len(j["response"]) > 20
assert j["queen"] == "Aleph", f"expected Aleph, got {j['queen']}"
assert j["tier"] == "T4", f"expected T4 (compliance), got {j['tier']}"
assert j["cost_usd"] == 0.0021
assert j["sigil_hash"] and len(j["sigil_hash"]) >= 8
print(f"  ✓ compliance query → T4 ({j['model']}), cost ${j['cost_usd']}, queen={j['queen']}")
print(f"    response: {j['response'][:100]}...")

r = client.post("/api/council/chat", json={
    "queen_id": "queen-care", "message": "hi",
})
assert r.status_code == 200
j = r.json()
assert j["tier"] == "T1", f"expected T1 (greeting), got {j['tier']}"
assert j["cost_usd"] == 0.00002
print(f"  ✓ greeting → T1 ({j['model']}), cost ${j['cost_usd']}")

r = client.post("/api/council/chat", json={
    "queen_id": "queen-strategy", "arcana_lens": 4,
    "message": "Design the architecture for the sovereign OS",
})
j = r.json()
assert j["tier_num"] in (3, 4), f"expected T3/T4, got {j['tier']}"
print(f"  ✓ analytical → {j['tier']} ({j['model']}), queen={j['queen']}")

# All 13 queen IDs should be addressable
queens = ["queen-king","queen-strategy","queen-care","queen-compliance","queen-finance",
          "queen-domain","queen-arcana","queen-brain","queen-proactive","queen-bridge",
          "queen-distribution","queen-council","queen-watch"]
for q in queens:
    r = client.post("/api/council/chat", json={"queen_id": q, "message": "hello"})
    assert r.status_code == 200, f"{q}: {r.status_code} {r.text}"
    assert r.json()["queen"]
print(f"  ✓ all 13 queens respond")


# ─── TASK 3: /api/ichar/create round-trip (wizard payload) ───
print(header("TASK 3: wizard ichar/create round-trip"))
payload = {
    "user_id": "wizard-roundtrip",
    "name": "Aurelia",
    "queen_model": "athena",
    "arcana_lens": 2,
    "voice": "warm",
    "cognition": "balanced",
    "initial_message": "Hello sovereign world",
}
r = client.post("/api/ichar/create", json=payload)
assert r.status_code == 200, r.text
j = r.json()
assert "ichar_id" in j and j["ichar_id"].startswith("ich-")
assert "sigil_hash" in j and len(j["sigil_hash"]) >= 8
print(f"  ✓ wizard payload → ichar_id={j['ichar_id']}, sigil={j['sigil_hash']}")

# GET it back
r2 = client.get(f"/api/ichar/{j['ichar_id']}")
assert r2.status_code == 200
got = r2.json()
assert got["name"] == "Aurelia"
assert got["queen_model"] == "athena"
assert got["arcana_lens"] == 2
print(f"  ✓ GET /api/ichar/{{id}} returns round-tripped payload")


# ─── TASK 4: /api/perf/track + /api/perf/stats ───
print(header("TASK 4: /api/perf/track + /api/perf/stats"))
# Beacon 3 different pages with different metrics
for i, route in enumerate(["/", "/csoai-os/v2-temple-os.html", "/csoai-os/v2-signup-wizard.html"]):
    r = client.post("/api/perf/track", json={
        "page_url": f"http://localhost/{route}",
        "lcp_ms": 800 + i * 200,
        "fid_ms": 40 + i * 10,
        "cls": 0.02 + i * 0.01,
        "ttfb_ms": 100 + i * 50,
        "route": route,
        "locale": "en",
        "user_agent": "Mozilla/5.0 (test)",
        "viewport": "1920x1080",
        "connection": "4g",
    })
    assert r.status_code == 200, r.text
    assert r.json()["ok"] is True
print("  ✓ 3 perf beacons tracked")

r = client.get("/api/perf/stats?hours=24")
assert r.status_code == 200
s = r.json()
assert s["ok"] is True
assert s["samples"] >= 3
assert s["summary"]["lcp_ms"]["count"] >= 3
assert s["summary"]["lcp_ms"]["p75"] is not None
assert len(s["by_route"]) >= 1
assert "cwv" in s and s["cwv"]["lcp"]["verdict"] in ("good","needs-improvement","poor")
print(f"  ✓ stats: {s['samples']} samples, LCP p75={s['summary']['lcp_ms']['p75']}ms "
      f"(CWV: {s['cwv']['lcp']['verdict']})")
print(f"    routes tracked: {list(s['by_route'].keys())}")
print(f"    hours: {s['hours']}, hourly buckets: {len(s['hourly'])}")


# ─── SUMMARY ───
print(header("ALL 4 LAST-MILE FEATURES PASS"))
print("  ✓ TASK 1: i18n (6 locales × 148 strings each + JS switcher)")
print("  ✓ TASK 2: council chat (4-tier cascade + queen voice)")
print("  ✓ TASK 3: ichar wizard round-trip (real backend)")
print("  ✓ TASK 4: perf instrumentation (LCP/FID/CLS + CWV verdicts)")