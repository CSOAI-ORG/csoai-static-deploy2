"""Tests for sovos-oscal-exporter — ChainResult → OSCAL assessment-results."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sovos_oscal_exporter import (
    OSCAL_JSON_VERSION, OSCAL_UUID_REGEX,
    Observation, Finding,
    chain_result_to_finding, chain_result_to_observation,
    build_assessment_results, dump_assessment_results, self_test,
)


class CR:
    """A ChainResult-shaped object."""
    def __init__(self, d, permitted, source="birth:iokfarm", chain_id="aa11bb22cc33dd44ee55ff00", inputs_sha="a"*24):
        self.distance = d
        self.fisher_rao_distance = d
        self.threshold = 1.0
        self.is_permitted = permitted
        self.source = source
        self.chain_id = chain_id
        self.inputs_sha = inputs_sha


def test_oe01_observation_shape():
    """An observation has uuid, methods, subjects, props, timestamps."""
    cr = CR(0.0845, True)
    o = chain_result_to_observation(cr)
    assert isinstance(o, Observation)
    assert OSCAL_UUID_REGEX.match(o.uuid)
    assert "SOV-SIGNAL-CONTINUOUS" in o.methods
    assert o.props  # has chain-id + distance props
    props = {p["name"]: p["value"] for p in o.props}
    assert props["sovos-chain-id"] == "aa11bb22cc33dd44ee55ff00"
    assert props["fisher-rao-distance"] == "0.0845"
    print(f"  ✅ observation: uuid {o.uuid[:8]}…, method, props ok")


def test_oe02_finding_good_satisfied():
    """A permitted ChainResult → finding status 'satisfied'."""
    cr = CR(0.0845, True)
    o = chain_result_to_observation(cr)
    f = chain_result_to_finding(cr, o.uuid)
    assert isinstance(f, Finding)
    assert f.targets[0]["status"]["state"] == "satisfied"
    assert "0.0845" in f.targets[0]["status"]["remarks"]
    # related observation links back
    assert f.related_observations[0]["observation-uuid"] == o.uuid
    print(f"  ✅ good finding: status satisfied (d=0.0845 ≤ 1.0)")


def test_oe03_finding_bad_not_satisfied():
    """A far (non-permitted) ChainResult → 'not-satisfied'."""
    cr = CR(2.7876, False)
    o = chain_result_to_observation(cr)
    f = chain_result_to_finding(cr, o.uuid)
    assert f.targets[0]["status"]["state"] == "not-satisfied"
    assert "2.7876" in f.targets[0]["status"]["remarks"]
    print(f"  ✅ bad finding: status not-satisfied (d=2.7876 > 1.0)")


def test_oe04_unknown_permitted_treats_not_satisfied():
    """A ChainResult with is_permitted=None → not-satisfied (unmeasured = no evidence)."""
    class CRUnknown:
        distance = 0.0
        threshold = 1.0
        is_permitted = None
        source = "birth:csoai"
        chain_id = "c" * 24
        inputs_sha = "d" * 24
    cr = CRUnknown()
    o = chain_result_to_observation(cr)
    f = chain_result_to_finding(cr, o.uuid)
    assert f.targets[0]["status"]["state"] == "not-satisfied"
    print(f"  ✅ unknown verdict → not-satisfied (honest: no evidence)")


def test_oe05_assessment_results_structure():
    """The package has SSP + metadata (oscal-version) + results with obs+findings."""
    pkg = build_assessment_results(
        [CR(0.0845, True), CR(2.7876, False)], title="audit")
    assert "system-security-plan" in pkg
    ar = pkg["assessment-results"]
    assert ar["metadata"]["oscal-version"] == OSCAL_JSON_VERSION
    results = ar["results"]
    assert len(results) == 1
    assert len(results[0]["observations"]) == 2
    assert len(results[0]["findings"]) == 2
    print(f"  ✅ package: SSP + OSCAL {OSCAL_JSON_VERSION} + 2 obs + 2 findings")


def test_oe06_article_zero_prop():
    """article_zero=true is recorded as a package prop."""
    pkg = build_assessment_results([CR(0.1, True)], article_zero=True)
    props = {p["name"]: p["value"] for p in pkg["assessment-results"]["results"][0]["props"]}
    assert props["article-zero"] == "true"
    print(f"  ✅ article-zero flag recorded")


def test_oe07_passed_count_prop():
    """The package records how many assessed entities passed."""
    pkg = build_assessment_results([CR(0.0845, True), CR(0.2, True), CR(5.0, False)])
    props = {p["name"]: p["value"] for p in pkg["assessment-results"]["results"][0]["props"]}
    assert props["assessed-entities"] == "3"
    assert props["passed"] == "2"
    print(f"  ✅ assessed-entities=3, passed=2")


def test_oe08_dump_is_json():
    """dump_assessment_results produces valid JSON."""
    pkg = build_assessment_results([CR(0.0845, True)])
    text = dump_assessment_results(pkg)
    parsed = json.loads(text)
    assert "assessment-results" in parsed
    print(f"  ✅ dump → valid JSON ({len(text)} bytes)")


def test_oe09_ssp_chain_id_deterministic():
    """The SSP chain-id is 24 hex, deterministic per exact package."""
    a = build_assessment_results([CR(0.0845, True)], title="t")
    b = build_assessment_results([CR(0.0845, True)], title="t")
    assert a["system-security-plan"]["chain-id"] == b["system-security-plan"]["chain-id"]
    assert len(a["system-security-plan"]["chain-id"]) == 24
    print(f"  ✅ SSP chain-id is 24-char hex, deterministic")


def test_oe10_evidence_is_chain_anchored():
    """Each observation carries the signed ChainResult id as relevant evidence."""
    cr = CR(0.0845, True, chain_id="feed00112233445566778899")
    o = chain_result_to_observation(cr)
    href = o.relevant_evidence[0]["href"]
    assert "feed00112233445566778899" in href
    print(f"  ✅ evidence anchored to chain-id: {href}")


def test_oe11_self_test():
    """self_test returns a complete picture."""
    info = self_test()
    assert info["has_ssp"] is True
    assert info["oscal_version"] == OSCAL_JSON_VERSION
    assert info["good_is_satisfied"] == "satisfied"
    assert info["bad_is_not_satisfied"] == "not-satisfied"
    assert info["ssp_chain_id_len"] == 24
    print(f"  ✅ self_test: good='{info['good_is_satisfied']}', "
          f"bad='{info['bad_is_not_satisfied']}', n_obs={info['n_observations']}")


if __name__ == "__main__":
    tests = [
        test_oe01_observation_shape,
        test_oe02_finding_good_satisfied,
        test_oe03_finding_bad_not_satisfied,
        test_oe04_unknown_permitted_treats_not_satisfied,
        test_oe05_assessment_results_structure,
        test_oe06_article_zero_prop,
        test_oe07_passed_count_prop,
        test_oe08_dump_is_json,
        test_oe09_ssp_chain_id_deterministic,
        test_oe10_evidence_is_chain_anchored,
        test_oe11_self_test,
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
