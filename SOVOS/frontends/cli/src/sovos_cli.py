"""sovos — CLI frontend (text-first, no avatar).

Three commands:
  sov score "text"       Score text on the 4 GSPC axes
  sov run "prompt"       Run the certification loop for a customer
  sov audit              Show the latest test results across all packages
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow imports from anywhere in the monorepo
_SOVOS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SOVOS_ROOT / "packages" / "sovos-core" / "src"))
sys.path.insert(0, str(_SOVOS_ROOT / "packages" / "sovos-certification-loop" / "src"))


def cmd_score(args: argparse.Namespace) -> int:
    """Score a governance record (JSON or stub record) on the 4 GSPC axes.

    Usage:
      sov score '{"rbac": true, "sbom": "x", "audit_log": true, ...}'
    """
    from sovos_core.gspc import score_gspc
    text = " ".join(args.text)
    # Accept either JSON or build a stub record from a flat text
    try:
        record = json.loads(text)
    except json.JSONDecodeError:
        # Stub record from text: count keywords → enable capabilities
        words = text.lower().split()
        record = {
            "rbac": "rbac" in words or "role" in words,
            "sbom": "sbom" in text.lower() or "bill of materials" in text.lower(),
            "audit_log": "audit" in words,
            "data_minimisation": "minim" in text.lower() or "gdpr" in text.lower(),
            "human_oversight": "oversight" in words or "human" in words,
            "transparency": "transparency" in words or "explain" in words,
            "robustness": "robust" in words,
            "lawful_basis": "lawful" in words or "gdpr" in words,
        }
    score = score_gspc(record)
    print(f"  GSPC composite: {score.composite:.3f}")
    print(f"  axes: G={score.G:.2f} S={score.S:.2f} P={score.P:.2f} C={score.C:.2f}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Run the certification loop with a customer email + product."""
    from sovos_certification import (
        StripeWebhookStub, OrderStore, RunPodStub, LocalClan,
        GovBenchRunner, C2PASigner, ProofOfAIStub, run_certification_loop,
    )
    payload = {
        "id": f"evt_cli_{abs(hash(args.email)) % 100000}",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "customer_email": args.email,
                "amount_total": args.amount,
                "metadata": {"product_id": args.product},
            },
        },
    }
    stack = {
        "stripe": StripeWebhookStub(),
        "orders": OrderStore(),
        "runpod": RunPodStub(),
        "clan": LocalClan(),
        "gov": GovBenchRunner(),
        "signer": C2PASigner(key_dir=Path.home() / ".sovos_c2pa"),
        "proof": ProofOfAIStub(),
    }
    result = run_certification_loop(payload, **stack)
    print()
    print(f"  Order:        {result.order.order_id}")
    print(f"  Status:       {result.order.status}")
    print(f"  SOV SIGNAL:   {result.gov_eval.mean_sov_signal:.3f}  (pass_rate: {result.gov_eval.pass_rate:.0%})")
    print(f"  Certificate:  {result.certificate.certificate_url}")
    print(f"  Ed25519 sig:  {result.manifest.ed25519_signature[:24]}…")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    """Run all monorepo tests and show summary."""
    import subprocess
    pkg_root = _SOVOS_ROOT / "packages"
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
    cmd = ["python3", "-m", "pytest", str(pkg_root), "-q", "--tb=no"]
    print(f"  $ PYTHONPATH=… {cmd[0]} {cmd[1]} {' '.join(cmd[2:])}")
    r = subprocess.run(cmd, env={"PYTHONPATH": env_path, "PATH": "/usr/bin:/bin:/usr/local/bin"},
                       capture_output=True, text=True)
    out = r.stdout.splitlines()[-1] if r.stdout else ""
    print(f"  {out}")
    return r.returncode


def main() -> int:
    parser = argparse.ArgumentParser(prog="sov", description="SOVOS CLI — text-first governance OS")
    sub = parser.add_subparsers(dest="command", required=True)

    p_score = sub.add_parser("score", help="Score text on the 4 GSPC axes")
    p_score.add_argument("text", nargs="+", help="Text to score")
    p_score.set_defaults(func=cmd_score)

    p_run = sub.add_parser("run", help="Run the certification loop")
    p_run.add_argument("--email", default="buyer@example.com", help="Customer email")
    p_run.add_argument("--amount", type=int, default=49900, help="Amount in cents")
    p_run.add_argument("--product", default="sov-signal-cert-std", help="Product ID")
    p_run.set_defaults(func=cmd_run)

    p_audit = sub.add_parser("audit", help="Run all monorepo tests")
    p_audit.set_defaults(func=cmd_audit)

    args = parser.parse_args()
    print(f"sov v0.1.0 — SOVOS CLI")
    print()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())