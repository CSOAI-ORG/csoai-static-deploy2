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
sys.path.insert(0, str(ROOT))


def _run(args, expect_code=0):
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
        f"{pkg_root}/sovos-hermes-integration/plugins/observability:"
        f"{pkg_root}/sovos-cellar-ingest/src:"
        f"{pkg_root}/sovos-crosswalk/src:"
        f"{pkg_root}/sovos-oscal/src:"
        f"{pkg_root}/sovos-chain/src:"
        f"{pkg_root}/sovos-fisher-rao/src:"
        f"{pkg_root}/sovos-arena/src:"
        f"{pkg_root}/sovos-signal-index/src"
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
    rc, out, _ = _run(["run", "cli@test.com", "--amount", "49900"])
    assert rc == 0
    assert "assessment_id" in out
    assert "cert_" in out
    assert "status: certified" in out
    print("  ✅ sov run works (full certification loop)")


def test_audit():
    rc, out, _ = _run(["audit"])
    assert "pytest" in out or "passed" in out.lower() or "failed" in out.lower()
    print(f"  ✅ sov audit ran (exit={rc})")


def test_ras_offline():
    """sov ras <celex> --offline runs the full wire without network."""
    pkg_root = ROOT / "packages"
    extra = (
        f"{pkg_root}/sovos-cellar-ingest/src:"
        f"{pkg_root}/sovos-crosswalk/src:"
        f"{pkg_root}/sovos-oscal/src:"
        f"{pkg_root}/sovos-chain/src:"
        f"{pkg_root}/sovos-fisher-rao/src:"
        f"{pkg_root}/sovos-arena/src:"
        f"{pkg_root}/sovos-signal-index/src"
    )
    import os
    env = {**os.environ, "PYTHONPATH": extra}
    cmd = ["python3", str(CLI), "ras", "32024R1689", "--offline"]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert r.returncode == 0, f"ras offline failed: {r.stderr}"
    assert "⟁ RAS wire" in r.stdout
    assert "chain verdict" in r.stdout
    assert "OSCAL" in r.stdout
    print(f"  ✅ sov ras --offline works (law→crosswalk→chain→OSCAL)")


def test_ras_help_lists_modes():
    """The ras subcommand advertises --measure + --canary."""
    rc, out, _ = _run(["ras", "--help"])
    assert rc == 0
    assert "--measure" in out
    assert "REAL measurement" in out
    assert "--canary" in out
    print("  ✅ sov ras --help shows --measure mode + --canary gate")


def test_ras_canary_gate_passes():
    """sov ras --canary: instrument discriminates known-good vs known-bad."""
    pkg_root = ROOT / "packages"
    extra = (
        f"{pkg_root}/sovos-arena/src:"
        f"{pkg_root}/sovos-signal-index/src"
    )
    import os
    env = {**os.environ, "PYTHONPATH": extra}
    cmd = ["python3", str(CLI), "ras", "--canary", "--per-axis", "32",
           "--threshold", "1.0"]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    out = r.stdout
    assert r.returncode == 0, (
        f"canary failed rc={r.returncode} stderr={r.stderr}\nstdout={out}"
    )
    assert "CANARY GATE PASSED" in out
    assert "disjoint" in out
    print(f"  ✅ sov ras --canary gate passed (good vs bad separated)")


def main():
    tests = [test_help, test_score, test_run, test_audit,
             test_ras_offline, test_ras_help_lists_modes,
             test_ras_canary_gate_passes]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            import traceback; traceback.print_exc()
            print(f"  ❌ FAIL: {e}")
            failed += 1
    if failed:
        print(f"\n❌ {failed}/{len(tests)} FAILED")
        return 1
    print(f"\n✅ {len(tests)}/{len(tests)} PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
