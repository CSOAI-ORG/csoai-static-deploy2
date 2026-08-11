"""sovos-cli — text-first CLI for the SOVOS governance OS.

Commands:
  sov score '{"...": ...}'     Score a governance record on the 4 GSPC axes
  sov score --keys             Print the 13 ETSI principle keys + sample record
  sov score <text>             Auto-build a record from keywords in <text>
  sov run <email>              Run the certification loop with a customer email
  sov audit                    Run all monorepo tests
  sov ras <celex> [--offline]  Run the full RAS wire: law → crosswalk → chain
                                 → OSCAL assessment-results

v0.2.0 changes:
- Fixed `--keys` flag that prints the 13 ETSI principle keys + a sample record
- The docstring example was wrong — it used invented keys instead of the real
  ETSI EN 304 223 keys (sovos_core.gspc.ETSI_304_223_PRINCIPLES). Score 0.000
  was the bug. Now fixed by exposing the real keys + sample record.
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


# The 13 ETSI EN 304 223 principle keys (mirror of sovos_core.gspc).
# Each principle requires ALL its keys to be truthy in the record.
# Surface these so users can build a valid record.
ETSI_KEYS = [
    ("P01", "Secure by design",          ["threat_model", "design_review", "owner"]),
    ("P02", "Data governance",            ["data_map", "retention_policy", "lawful_basis"]),
    ("P03", "Identity & access",          ["rbac", "mfa", "least_privilege"]),
    ("P04", "Secure SDLC",                ["code_review", "dependency_scan", "unit_tests"]),
    ("P05", "Supply chain",               ["sbom", "vendor_audit", "provenance"]),
    ("P06", "Monitoring & logging",       ["audit_log", "monitoring", "anomaly_detection"]),
    ("P07", "Vulnerability mgmt",         ["vuln_scan", "patch_sla"]),
    ("P08", "Incident response",          ["incident_plan", "containment_procedure", "recovery"]),
    ("P09", "Config mgmt",                ["config_scan", "baseline"]),
    ("P10", "Continuity",                 ["backup", "failover", "rpo"]),
    ("P11", "Human oversight",            ["human_review", "escalation_path", "named_owner"]),
    ("P12", "Decommissioning",            ["data_erasure", "credential_revocation", "asset_disposal"]),
    ("P13", "Continuous improvement",     ["pdca_record", "independent_audit"]),
]


def sample_record() -> dict:
    """Build a sample record that satisfies ALL 13 principles (score = 1.0)."""
    r = {}
    for _, _, keys in ETSI_KEYS:
        for k in keys:
            r[k] = True
    return r


def cmd_score(args: argparse.Namespace) -> int:
    """Score a governance record on the 4 GSPC axes."""
    from sovos_core.gspc import score_gspc

    if getattr(args, "keys", False):
        # Print the keys + sample record
        print("  GSPC scoring uses 13 ETSI EN 304 223 principles.")
        print("  Each principle requires ALL its keys to be truthy in the record.")
        print()
        for pid, title, keys in ETSI_KEYS:
            print(f"  {pid} {title}:")
            print(f"     keys: {', '.join(keys)}")
        print()
        print("  Sample record (satisfies ALL 13 principles, score = 1.0):")
        print("  " + json.dumps(sample_record(), indent=2).replace("\n", "\n  "))
        return 0

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
    print(f"  GSPC composite: {score.composite:.3f}  (grade: {score.grade})")
    print(f"  axes: G={score.G:.2f} S={score.S:.2f} P={score.P:.2f} C={score.C:.2f}")
    print(f"  passed: {len(score.passed_principles)}/13 ETSI principles")
    if not score.passed_principles and score.composite == 0.0:
        print()
        print("  ⚠️  Score is 0.000. Did you use the right keys?")
        print("  Run: sov score --keys    (to see the 13 principle keys + sample record)")
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
                "amount_total": args.amount_cents,
                "metadata": {"product_id": args.product},
            }
        }
    }
    # Stub implementations
    stripe = StripeWebhookStub()
    orders = OrderStore()
    runpod = RunPodStub()
    clan = LocalClan()
    govbench = GovBenchRunner()
    c2pa = C2PASigner()
    proof = ProofOfAIStub()
    result = run_certification_loop(payload, stripe, orders, runpod, clan,
                                    govbench, c2pa, proof)
    print(f"  cert_id: {result.certificate.certificate_id}")
    print(f"  status: {result.order.status}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    """Run all monorepo tests."""
    import subprocess
    print("  Running all monorepo tests...")
    result = subprocess.run(
        ["python3", "-m", "pytest", "packages/", "-q", "--tb=no"],
        cwd=str(_SOVOS_ROOT),
        capture_output=True, text=True,
    )
    print(result.stdout[-2000:] if result.stdout else "(no output)")
    if result.returncode != 0:
        print(f"  FAIL: pytest exit {result.returncode}")
        return result.returncode
    print("  ✅ All tests pass")
    return 0


def cmd_ras(args: argparse.Namespace) -> int:
    """Run the full RAS wire: law → crosswalk → chain → OSCAL.

    sov ras 32024R1689 [--offline]

    Steps:
      1. Ingest the CELEX from CELLAR (live) or build a stub (offline).
      2. Seed a crosswalk atlas from the law document.
      3. Run a chain verdict against a permitted manifold.
      4. Export the verdict to an OSCAL assessment-results document.
    """
    try:
        import numpy as np
        from sovos_cellar_ingest import ingest_celex
        from sovos_crosswalk import from_cellar_docs, builtin_euai_atlas, obstruction_set
        from sovos_chain import chain
        from sovos_oscal import ChainObservation, assessment_results, dump
    except ImportError as e:
        print(f"  ❌ RAS wire needs the RAS packages (are they on PYTHONPATH?): {e}")
        return 2

    celex = args.celex.upper()
    offline = bool(getattr(args, "offline", False))
    print(f"⟁ RAS wire — {celex} ({'offline stub' if offline else 'live CELLAR'})")

    # 1. Law
    doc = ingest_celex(celex, fetch=not offline, lang="EN")
    print(f"  1. law: {doc.instrument_type} {doc.publication_year} — {doc.title[:60]}")

    # 2. Crosswalk
    atlas = from_cellar_docs([doc])
    eu = builtin_euai_atlas()
    obs = obstruction_set(eu, atlas)
    print(f"  2. crosswalk: {len(atlas.rows)} cellar row(s); "
          f"obstructed vs builtin={obs['n_obstructed']} shared={obs['n_shared']}")

    # 3. Chain verdict
    #    A deployer at the permitted manifold (near identity) → compliant.
    permitted = np.eye(4)
    candidate = {"vector": [0.95, 0.95, 0.95, 0.95],
                 "source": "deployer:acme", "layer": "milk"}
    r = chain(candidate, permitted_state=permitted, threshold=1.0)
    print(f"  3. chain verdict: d={r.fisher_rao_distance:.4f} "
          f"permitted={r.is_permitted}")

    # 4. OSCAL
    obs_o = ChainObservation(
        chain_id=r.chain_id, source="deployer:acme", layer="milk",
        vector=list(candidate["vector"]),
        distance=r.fisher_rao_distance, threshold=1.0,
        is_permitted=bool(r.is_permitted),
        control_id=f"CELEX-{celex}",
    )
    pkg = assessment_results([obs_o],
                             title=f"{celex} conformity assessment")
    print(f"  4. OSCAL: oscal-version={pkg['oscal-version']}, "
          f"ssp-chain-id={pkg['system-security-plan'].get('chain-id','')}")
    if offline:
        print()
        print(dump(pkg))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="sov",
        description="SOVOS CLI — text-first governance OS",
    )
    parser.add_argument("--version", action="version", version="sov v0.2.0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_score = sub.add_parser("score", help="Score a governance record on the 4 GSPC axes")
    p_score.add_argument("--keys", action="store_true", help="Print the 13 ETSI principle keys + sample record")
    p_score.add_argument("text", nargs="*", help="JSON record OR plain text (keyword-based stub)")
    p_score.set_defaults(func=cmd_score)

    p_run = sub.add_parser("run", help="Run the certification loop")
    p_run.add_argument("email", help="Customer email")
    p_run.add_argument("--product", default="sov-signal-cert-std", help="Product ID")
    p_run.add_argument("--amount-cents", type=int, default=5000, help="Amount in cents")
    p_run.set_defaults(func=cmd_run)

    p_audit = sub.add_parser("audit", help="Run all monorepo tests")
    p_audit.set_defaults(func=cmd_audit)

    p_ras = sub.add_parser("ras", help="Run the full RAS wire: law → crosswalk → chain → OSCAL")
    p_ras.add_argument("celex", help="CELEX id, e.g. 32024R1689 (EU AI Act)")
    p_ras.add_argument("--offline", action="store_true", help="Use an offline law stub (no CELLAR fetch)")
    p_ras.set_defaults(func=cmd_ras)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
