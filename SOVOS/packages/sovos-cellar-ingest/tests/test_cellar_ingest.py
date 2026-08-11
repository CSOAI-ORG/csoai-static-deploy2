"""Tests for sovos-cellar-ingest — EUR-Lex CELLAR → regulation vectors."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest

from sovos_cellar_ingest import (
    CELEX_RE, SOVOS_CELLAR_ENDPOINT, SOVOS_CELLAR_RESOURCE,
    LawDocument, celex_to_vector, fetch_celex_rdf, ingest_celex,
    parse_celex_graph, _type_from_celex, _year_from_celex, self_test,
)

# A tiny ATOM-style CELLAR RDF sample for offline parse tests
SAMPLE_RDF = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:dc="http://purl.org/dc/elements/1.1/"
         xmlns:dcterms="http://purl.org/dc/terms/">
  <rdf:Description rdf:about="https://publications.europa.eu/resource/celex/32024R1689">
    <dc:title xml:lang="en">Regulation (EU) 2024/1689 of the European Parliament and of the Council</dc:title>
    <dc:title xml:lang="fr">Règlement (UE) 2024/1689 du Parlement européen et du Conseil</dc:title>
    <dcterms:issued>2024-06-13</dcterms:issued>
  </rdf:Description>
</rdf:RDF>"""


def test_ci01_celex_regex():
    """CELEX regex accepts real shapes, rejects junk."""
    assert CELEX_RE.match("32024R1689")
    assert CELEX_RE.match("32024L1433")   # Directive
    assert CELEX_RE.match("32025D0001")   # Decision
    assert not CELEX_RE.match("hello")
    assert not CELEX_RE.match("32024R")
    print(f"  ✅ CELEX regex: 32024R1689 / 32024L1433 pass, junk rejected")


def test_ci02_parse_cellar_offline():
    """Offline RDF parse extracts title (EN), year, type."""
    doc = parse_celex_graph(SAMPLE_RDF, lang="EN")
    assert doc.celex == "32024R1689"
    assert "Regulation (EU) 2024/1689" in doc.title
    assert doc.publication_year == 2024
    assert doc.instrument_type == "Regulation"
    assert doc.uri == f"{SOVOS_CELLAR_RESOURCE}32024R1689"
    print(f"  ✅ offline parse: title='{doc.title[:40]}…', year=2024, type=Regulation")


def test_ci03_parse_cellar_french_title():
    """Language-specific title selection."""
    doc = parse_celex_graph(SAMPLE_RDF, lang="FR")
    assert "Règlement" in doc.title
    print(f"  ✅ FR title selected: '{doc.title[:40]}…'")


def test_ci04_vector_deterministic():
    """The same CELEX+lang+title → same vector."""
    v1 = celex_to_vector("32024R1689", title="T", language="EN")
    v2 = celex_to_vector("32024R1689", title="T", language="EN")
    assert v1 == v2
    assert len(v1) == 8
    print(f"  ✅ vector deterministic, dim=8")


def test_ci05_vector_language_rotates():
    """Different language → different vector (multilingual Procrustes)."""
    v_en = celex_to_vector("32024R1689", title="T", language="EN")
    v_fr = celex_to_vector("32024R1689", title="T", language="FR")
    assert v_en != v_fr
    print(f"  ✅ language namespace rotation: EN ≠ FR")


def test_ci06_vector_differs_per_celex():
    """Different laws → different vectors (regulations as clans)."""
    v_ai = celex_to_vector("32024R1689", language="EN")
    v_gdpr = celex_to_vector("32016R0679", language="EN")
    assert v_ai != v_gdpr
    print(f"  ✅ AI Act ≠ GDPR vectors (distinct axes)")


def test_ci07_year_and_type_parsers():
    """Year/type extraction from CELEX shapes."""
    assert _year_from_celex("32024R1689") == 2024
    assert _year_from_celex("32016R0679") == 2016
    assert _type_from_celex("32024R1689") == "Regulation"
    assert _type_from_celex("32024L1433") == "Directive"
    print(f"  ✅ year/type: 32024R1689→2024/Regulation, 32024L1433→Directive")


def test_ci08_ingest_offline_builds_bus_payload():
    """ingest_celex(fetch=False) produces a Bus-compatible vector."""
    doc = ingest_celex("32024R1689", fetch=False, lang="EN")
    assert doc.vector  # filled
    assert abs(max(abs(c) for c in doc.vector)) < 1.0
    bv = doc.to_bus_vector(layer="honey")
    assert bv["source"] == f"cellar:{doc.celex}"
    assert bv["layer"] == "honey"
    assert bv["payload"]["celex"] == "32024R1689"
    assert bv["payload"]["instrument_type"] == "Regulation"
    print(f"  ✅ offline ingest → honey Bus payload (source=cellar:32024R1689)")


def test_ci09_ingest_to_bus_redis():
    """When sovos-bus-redis is importable, ingest appends to the Bus."""
    bus_mod = None
    try:
        import sovos_bus_redis
        bus_mod = sovos_bus_redis
    except ImportError:
        pass
    if bus_mod is None:
        print("  ⚠️  sovos-bus-redis not on path — skip Bus append test")
        return
    from sovos_bus_redis import RedisBus
    bus = RedisBus(use_fakeredis=True)
    doc = ingest_celex("32024R1689", bus=bus, fetch=False, layer="honey")
    rows = bus.read_by_source(f"cellar:32024R1689")
    assert len(rows) == 1
    assert rows[0].layer == "honey"
    assert rows[0].payload["celex"] == "32024R1689"
    print(f"  ✅ Bus append: 1 honey event for 32024R1689 (fakeredis)")


def test_ci10_celex_validation():
    """Invalid CELEX → ValueError on live fetch path."""
    try:
        fetch_celex_rdf("nonsense")
        assert False, "should have raised"
    except ValueError as e:
        assert "invalid CELEX" in str(e)
    print(f"  ✅ invalid CELEX → ValueError")


def test_ci11_self_test():
    """self_test returns a complete picture."""
    info = self_test()
    assert info["deterministic"] is True
    assert info["lang_rotates"] is True
    assert info["in_ball"] is True
    assert info["year"] == 2024
    assert info["instrument_type"] == "Regulation"
    print(f"  ✅ self_test: deterministic, lang-rotates, year=2024, Regulation")


if __name__ == "__main__":
    tests = [
        test_ci01_celex_regex,
        test_ci02_parse_cellar_offline,
        test_ci03_parse_cellar_french_title,
        test_ci04_vector_deterministic,
        test_ci05_vector_language_rotates,
        test_ci06_vector_differs_per_celex,
        test_ci07_year_and_type_parsers,
        test_ci08_ingest_offline_builds_bus_payload,
        test_ci09_ingest_to_bus_redis,
        test_ci10_celex_validation,
        test_ci11_self_test,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            import traceback; traceback.print_exc()
            print(f"  ❌ FAIL {t.__name__}: {e}")
    print(f"\n{'✅' if passed == len(tests) else '❌'} {passed}/{len(tests)} PASSED")