"""sovos CLI smoke tests."""
import subprocess
import sys
from pathlib import Path

# Tests live at: SOVOS/frontends/cli/tests/test_cli.py
# CLI lives at:   SOVOS/frontends/cli/src/sovos_cli.py
# Both are children of: SOVOS/frontends/cli/
_THIS_DIR = Path(__file__).resolve().parent          # .../frontends/cli/tests
_CLI_DIR = _THIS_DIR.parent                          # .../frontends/cli
CLI = _CLI_DIR / "src" / "sovos_cli.py"
ROOT = _CLI_DIR.parent.parent                         # SOVOS/
sys.path.insert(0, str(ROOT))  # so test_cli.py can be imported from CLI dir


def _run(args, expect_code=0):
    """Run sov CLI as subprocess, return (returncode, stdout, stderr)."""
    cmd = ["python3", str(CLI)] + args
    pkg_root = ROOT / "packages"
    env_path = (
        f"{pkg_root}/sovos-core/src:"
        f"{pkg_root}/sovos-jspace-move/src:"
        f"{pkg_root}/sovos-jspace-hyperbolic/src:"
        f"{pkg_root}/sovos-mcp-servers/sov33-benchmark/src:"
        f"{pkg_root}/sovos-certification-loop/src:"
        f"{pkg_root}/sovos-mcp-servers/eu-ai-act-mcp/src:"
        f"{pkg_root}/sovos-mcp-servers/mcp-injection-scanner/src:"
        f"{pkg_root}/sovos-mcp-servers/openmoe-bft/src:"
        f"{pkg_root}/sovos-hermes-integration/plugins/observability"
    )
    import os
    env = {**os.environ, "PYTHONPATH": env_path}
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def test_help():
    rc, out, _ = _run(["--help"])
    assert rc == 0
    assert "SOVOS" in out
    print("  ✅ --help works")


def test_score():
    rc, out, _ = _run(["score", "hello", "world"])
    assert rc == 0
    assert "GSPC composite" in out
    print("  ✅ sov score works")


def test_run():
    rc, out, _ = _run(["run", "--email", "cli@test.com", "--amount", "49900"])
    assert rc == 0
    assert "SOV SIGNAL" in out
    assert "Certificate" in out
    assert "cert_" in out
    print("  ✅ sov run works (full certification loop)")


def test_audit():
    rc, out, _ = _run(["audit"])
    # audit may return non-zero if tests fail; we just check it RAN
    assert "pytest" in out or "passed" in out.lower() or "failed" in out.lower()
    print(f"  ✅ sov audit ran (exit={rc})")


def main():
    tests = [test_help, test_score, test_run, test_audit]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"  ❌ FAIL: {e}")
            failed += 1
    if failed:
        print(f"\n❌ {failed}/{len(tests)} FAILED")
        return 1
    print(f"\n✅ {len(tests)}/{len(tests)} PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())