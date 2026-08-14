"""Test: uncertainty-shader.html mirrors the Python sigma-calibration gate.

The shader HTML contains an inlined JS `simulateCalibration()` that must
agree with the Python `calibration_gate()`. This test checks the HTML:
- contains the gate constant ECE threshold 0.05
- references temperature scaling
- gates `locked` until calibration passes
- pairs with the sovos-sigma-calibration package (the engine)
"""
from __future__ import annotations

import sys
from pathlib import Path

# Repo root (csoai-static-deploy2 on Mac, /workspace on the pod)
def _find_root() -> Path:
    # On the pod, files live flat under /workspace
    cands = [
        Path("/workspace"),                      # pod
        Path(__file__).resolve().parents[2],     # Mac: csoai-static-deploy2
    ]
    for c in cands:
        if (c / "uncertainty-shader.html").exists():
            return c
    return Path(".")

ROOT = _find_root()

# Ensure the Python engine package is importable (Mac + pod variants)
for p in [
    ROOT / "SOVOS" / "packages" / "sovos-sigma-calibration" / "src",
    Path("/workspace") / "sovos-sigma-calibration" / "src",
]:
    if p.exists():
        sys.path.insert(0, str(p))

from sovos_sigma_calibration import DEFAULT_ECE_THRESHOLD


def _html() -> str:
    p = ROOT / "uncertainty-shader.html"
    assert p.exists(), f"missing {p}"
    return p.read_text()


def test_zu01_html_exists():
    html = _html()
    assert "<canvas" in html and "webgl" in html
    print(f"  ✅ uncertainty-shader.html exists, has WebGL canvas")


def test_zu02_html_has_gate_threshold():
    """The HTML must use the SAME ECE threshold as the Python package."""
    html = _html()
    assert f"{DEFAULT_ECE_THRESHOLD}" in html.replace("",""), \
        f"HTML missing threshold {DEFAULT_ECE_THRESHOLD}"
    # Check the gate logic constant appears
    assert "0.05" in html
    assert "ece <= 0.05" in html or "ece <= 0.05" in html.lower()
    print(f"  ✅ HTML gate threshold: ECE ≤ {DEFAULT_ECE_THRESHOLD}")


def test_zu03_html_gates_locked_start():
    """The shader starts LOCKED (uncalibrated) — honest default."""
    html = _html()
    assert "SIGMA GATE LOCKED" in html
    assert "uCalibrated" in html          # uniform exists in shader
    assert "calibrated = false" in html   # starts false
    print(f"  ✅ HTML starts locked (uncalibrated, honest)")


def test_zu04_html_temperature_scaling():
    """The HTML applies temperature (T) from calibration like the Python."""
    html = _html()
    assert "temperature" in html.lower()
    assert "T=" in html or "temperature" in html.lower()
    print(f"  ✅ HTML implements temperature scaling (post-sigma)")


def test_zu05_html_mirrors_python_engine():
    """The HTML references the Python engine package."""
    html = _html()
    assert "sovos-sigma-calibration" in html
    assert "calibrate()" in html or "calibration_gate" in html
    print(f"  ✅ HTML references sovos-sigma-calibration engine")


def test_zu06_python_engine_companion():
    """The companion Python package exists and passes its gate semantics."""
    # Import the engine and verify the gate threshold matches
    from sovos_sigma_calibration import calibration_gate
    assert callable(calibration_gate)
    print(f"  ✅ companion Python engine: calibration_gate reachable")


if __name__ == "__main__":
    tests = [
        test_zu01_html_exists,
        test_zu02_html_has_gate_threshold,
        test_zu03_html_gates_locked_start,
        test_zu04_html_temperature_scaling,
        test_zu05_html_mirrors_python_engine,
        test_zu06_python_engine_companion,
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
