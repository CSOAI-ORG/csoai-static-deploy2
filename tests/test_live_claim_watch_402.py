"""Tests for live_claim_watch.fetch_domain — verify 402 detection.

We test the function with a fake `subprocess.run` that simulates various
curl outputs, including the Vercel-DEPLOYMENT-DISABLED shape and a real
HTTP 402 status code.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add csoai-static-deploy2 to path so we can import live_claim_watch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import live_claim_watch as lcw


class FakeCompleted:
    """Mimics subprocess.CompletedProcess with the fields fetch_domain reads."""
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def _patched_fetch(monkeypatch_stdout, monkeypatch_stderr="", monkeypatch_rc=0):
    """Returns a subprocess.run replacement that returns the configured fake."""
    def _run(*args, **kwargs):
        return FakeCompleted(monkeypatch_stdout, monkeypatch_stderr, monkeypatch_rc)
    return _run


def test_402_via_curl_http_code():
    """Real HTTP 402 status code from curl -w trailer → PAYMENT_REQUIRED."""
    import unittest.mock as mock
    body = "<html>blocked</html>"
    stdout = f"{body}\n__HTTP_CODE__402"
    with mock.patch("subprocess.run",
                    side_effect=_patched_fetch(stdout, monkeypatch_rc=0)):
        status, returned_body = lcw.fetch_domain("https://example.com")
    assert status == "PAYMENT_REQUIRED", f"expected PAYMENT_REQUIRED, got {status}"
    assert "blocked" in returned_body
    print(f"  ✅ HTTP 402 → PAYMENT_REQUIRED")


def test_200_ok():
    """Normal HTTP 200 with body → OK."""
    import unittest.mock as mock
    body = "<html>normal page</html>"
    stdout = f"{body}\n__HTTP_CODE__200"
    with mock.patch("subprocess.run",
                    side_effect=_patched_fetch(stdout, monkeypatch_rc=0)):
        status, returned_body = lcw.fetch_domain("https://example.com")
    assert status == "OK"
    assert "normal page" in returned_body
    print(f"  ✅ HTTP 200 → OK")


def test_500_server_error():
    """HTTP 500 (not 402) with body → OK (we don't filter by 5xx — that's a separate concern)."""
    import unittest.mock as mock
    body = "<html>internal error</html>"
    stdout = f"{body}\n__HTTP_CODE__500"
    with mock.patch("subprocess.run",
                    side_effect=_patched_fetch(stdout, monkeypatch_rc=0)):
        status, _ = lcw.fetch_domain("https://example.com")
    # Note: fetch_domain treats anything with body as OK except 402 + DEPLOYMENT_DISABLED
    assert status == "OK"
    print(f"  ✅ HTTP 500 → OK (separate concern from 402)")


def test_dns_failure():
    """curl exit non-zero + 'could not resolve' in stderr → BLOCKED."""
    import unittest.mock as mock
    with mock.patch("subprocess.run",
                    side_effect=_patched_fetch(monkeypatch_stdout="",
                                                monkeypatch_stderr="could not resolve host",
                                                monkeypatch_rc=6)):
        status, _ = lcw.fetch_domain("https://nonexistent.invalid")
    assert status == "BLOCKED"
    print(f"  ✅ DNS failure → BLOCKED")


def test_empty_body_no_http_code():
    """curl succeeds but body is empty + no http-code → BLOCKED."""
    import unittest.mock as mock
    with mock.patch("subprocess.run",
                    side_effect=_patched_fetch(monkeypatch_stdout="", monkeypatch_rc=0)):
        status, _ = lcw.fetch_domain("https://example.com")
    assert status == "BLOCKED"
    print(f"  ✅ empty body → BLOCKED")


def test_vercel_deployment_disabled_body_legacy():
    """Body contains DEPLOYMENT_DISABLED even without 402 → PAYMENT_REQUIRED (legacy shape)."""
    import unittest.mock as mock
    body = "<html>DEPLOYMENT_DISABLED: Account is blocked</html>"
    stdout = f"{body}\n__HTTP_CODE__200"  # some old Vercel returned 200 with this body
    with mock.patch("subprocess.run",
                    side_effect=_patched_fetch(stdout, monkeypatch_rc=0)):
        status, _ = lcw.fetch_domain("https://example.com")
    assert status == "PAYMENT_REQUIRED"
    print(f"  ✅ legacy DEPLOYMENT_DISABLED body → PAYMENT_REQUIRED")


def test_timeout():
    """subprocess.TimeoutExpired → TIMEOUT."""
    import subprocess
    import unittest.mock as mock
    def _run(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="curl", timeout=30)
    with mock.patch("subprocess.run", side_effect=_run):
        status, _ = lcw.fetch_domain("https://slow.example.com")
    assert status == "TIMEOUT"
    print(f"  ✅ TimeoutExpired → TIMEOUT")


if __name__ == "__main__":
    tests = [
        test_402_via_curl_http_code,
        test_200_ok,
        test_500_server_error,
        test_dns_failure,
        test_empty_body_no_http_code,
        test_vercel_deployment_disabled_body_legacy,
        test_timeout,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            import traceback
            traceback.print_exc()
            print(f"  ❌ FAIL {t.__name__}: {e}")
    print(f"\n{'✅' if passed == len(tests) else '❌'} {passed}/{len(tests)} PASSED")
