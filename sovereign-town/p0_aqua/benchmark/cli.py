#!/usr/bin/env python3
"""
CLI for the Sovereign Town benchmark harness.

Examples
--------
    python -m benchmark run --policy sovereign --scenario baseline --district aqua
    python -m benchmark compare --policies sovereign,ungoverned,strict --scenario baseline
    python -m benchmark verify benchmark_runs/<id>.json
"""
from __future__ import annotations
import argparse
import json
import pathlib
import sys

from benchmark import policy, world, metrics, ledger


def cmd_run(args: argparse.Namespace) -> int:
    pol = policy.load_policy(args.policy)
    run = world.run(
        seed=args.seed,
        policy=pol,
        scenario=args.scenario,
        district=args.district,
        sign=args.sign,
        collect_states=args.collect_states,
    )
    scored = metrics.evaluate(run)
    print(f"\n  SOVEREIGN TOWN BENCHMARK — {run['policy']} / {run['scenario']} / {run['district']}")
    print("  " + "-" * 60)
    print(f"  {'safety':<12}{scored['safety']:.3f}  (crimes={scored['raw']['violations']})")
    print(f"  {'prosperity':<12}{scored['prosperity']:.3f}  (commons={scored['raw']['final_commons']})")
    print(f"  {'equity':<12}{scored['equity']:.3f}  (trust={scored['raw']['final_trust']})")
    print(f"  {'liberty':<12}{scored['liberty']:.3f}  (blocked={scored['raw']['blocked']})")
    print(f"  {'stability':<12}{scored['stability']:.3f}")
    print("  " + "-" * 60)

    if args.sign:
        manifest = ledger.sign_run(run)
        path = ledger.save_manifest(manifest, args.output_dir)
        print(f"  signed manifest: {path}")

    if args.json:
        print(json.dumps({"run": run, "score": scored}, indent=2, default=str))
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    names = [n.strip() for n in args.policies.split(",")]
    rows = []
    for name in names:
        pol = policy.load_policy(name)
        run = world.run(seed=args.seed, policy=pol, scenario=args.scenario, district=args.district)
        scored = metrics.evaluate(run)
        rows.append({
            "policy": name,
            "scenario": args.scenario,
            "safety": scored["safety"],
            "prosperity": scored["prosperity"],
            "equity": scored["equity"],
            "liberty": scored["liberty"],
            "stability": scored["stability"],
            "crimes": scored["raw"]["violations"],
            "commons": scored["raw"]["final_commons"],
            "trust": scored["raw"]["final_trust"],
        })
    print("\n  " + " | ".join(f"{k:<12}" for k in rows[0].keys()))
    print("  " + "-" * (15 * len(rows[0]) - 3))
    for r in rows:
        print("  " + " | ".join(f"{v:<12}" if isinstance(v, str) else f"{v:<12.3f}" for v in r.values()))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    manifest = ledger.load_manifest(args.path)
    ok = ledger.verify_manifest(manifest)
    print(f"{'VALID' if ok else 'INVALID'}: {args.path}")
    return 0 if ok else 1


def cmd_serve(args: argparse.Namespace) -> int:
    import os
    os.environ["SOV_TOWN_HARNESS_PORT"] = str(args.port)
    from benchmark.server import main
    main()
    return 0


def cmd_mcp(args: argparse.Namespace) -> int:
    from benchmark import mcp_server
    mcp_server.mcp.settings.host = args.host
    mcp_server.mcp.settings.port = args.port
    mcp_server.mcp.settings.log_level = args.log_level
    return mcp_server.main(transport=args.transport)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sovereign Town benchmark harness")
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="Run a single benchmark")
    p_run.add_argument("--policy", default="sovereign", help="Policy name or dotted path")
    p_run.add_argument("--scenario", default="baseline", help="Scenario name")
    p_run.add_argument("--district", default="aqua", help="District/hive to simulate")
    p_run.add_argument("--seed", type=int, default=47, help="Deterministic seed")
    p_run.add_argument("--sign", action="store_true", help="Sign the run manifest")
    p_run.add_argument("--collect-states", action="store_true", help="Include per-tick states")
    p_run.add_argument("--output-dir", default=None, help="Where to save signed manifests")
    p_run.add_argument("--json", action="store_true", help="Dump full JSON")
    p_run.set_defaults(func=cmd_run)

    p_cmp = sub.add_parser("compare", help="Compare multiple policies")
    p_cmp.add_argument("--policies", default="sovereign,ungoverned", help="Comma-separated policy names")
    p_cmp.add_argument("--scenario", default="baseline", help="Scenario name")
    p_cmp.add_argument("--district", default="aqua", help="District/hive to simulate")
    p_cmp.add_argument("--seed", type=int, default=47, help="Deterministic seed")
    p_cmp.set_defaults(func=cmd_compare)

    p_ver = sub.add_parser("verify", help="Verify a signed run manifest")
    p_ver.add_argument("path", help="Path to manifest JSON")
    p_ver.set_defaults(func=cmd_verify)

    p_serve = sub.add_parser("serve", help="Start the remote harness server")
    p_serve.add_argument("--port", type=int, default=3941, help="Port to listen on")
    p_serve.set_defaults(func=cmd_serve)

    p_mcp = sub.add_parser("mcp", help="Start the MCP server")
    p_mcp.add_argument("--transport", default="stdio", choices=["stdio", "sse", "streamable-http"],
                       help="MCP transport (stdio, sse, streamable-http)")
    p_mcp.add_argument("--host", default="127.0.0.1", help="Host for SSE/streamable-http transport")
    p_mcp.add_argument("--port", type=int, default=3942, help="Port for SSE/streamable-http transport")
    p_mcp.add_argument("--log-level", default="INFO", help="MCP log level")
    p_mcp.set_defaults(func=cmd_mcp)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
