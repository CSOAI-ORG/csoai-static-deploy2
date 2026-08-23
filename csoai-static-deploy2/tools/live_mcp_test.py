#!/usr/bin/env python3
"""
live_mcp_test.py — Live MCP Server Test Harness
================================================

For each live MCP in the registry:
  1. Contract check: name/ring/layer/owem/generals/tools all match canonical frame.
  2. Port probe: best-effort TCP connect to conventional MCP ports.
  3. Output: pass/fail summary + per-MCP detail.

Usage:
  python3 tools/live_mcp_test.py
  python3 tools/live_mcp_test.py --json
  python3 tools/live_mcp_test.py --mcp sov-identity-attestation
"""
import os, json, sys, socket, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG_PATH = os.path.join(ROOT, 'sovereign-charters', 'sov33-capability-registry.json')

CONVENTIONAL_PORTS = (8765, 7654, 3000, 8080, 9090)

def probe_port(host='127.0.0.1', timeout=0.1):
    """Return first reachable conventional MCP port, or None."""
    for port in CONVENTIONAL_PORTS:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return port
        except (ConnectionRefusedError, socket.timeout, OSError):
            continue
    return None

def main():
    parser = argparse.ArgumentParser(description='Live MCP test harness')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--mcp', help='test a single MCP by name')
    args = parser.parse_args()

    reg = json.load(open(REG_PATH))
    canonical_layers = {l['id'] for l in reg['layers']}
    canonical_owems = {o['id'] for o in reg['owem_groups']}

    mcps = [m for m in reg['mcps'] if m.get('status') == 'live']
    if args.mcp:
        mcps = [m for m in mcps if m['name'] == args.mcp]
        if not mcps:
            print(f'No live MCP named {args.mcp!r}', file=sys.stderr)
            return 1

    results = []
    for m in mcps:
        issues = []
        if m['ring'] not in (0, 1, 2):
            issues.append(f'ring={m["ring"]} not in (0,1,2)')
        if m['layer'] not in canonical_layers:
            issues.append(f'layer={m["layer"]} not in canonical layers')
        for o in m['owem']:
            if o not in canonical_owems:
                issues.append(f'owem={o} not canonical')
        for g in m.get('generals', []):
            if not (isinstance(g, int) and 1 <= g <= 12):
                issues.append(f'general={g} out of range')
        if not m.get('tools'):
            issues.append('zero tools')
        if not m.get('purpose'):
            issues.append('no purpose')

        port = probe_port()
        results.append({
            'name': m['name'],
            'ring': m['ring'],
            'layer': m['layer'],
            'owem': m['owem'],
            'generals': m['generals'],
            'tools': len(m['tools']),
            'status': m['status'],
            'contract_ok': not issues,
            'contract_issues': issues,
            'port_reachable': port is not None,
            'port': port,
        })

    if args.json:
        print(json.dumps({'total': len(results), 'results': results}, indent=2))
        return 0

    print(f'\n== Live MCP Test Harness ==')
    print(f'Live MCPs tested: {len(results)}')
    pass_n = sum(1 for r in results if r['contract_ok'])
    port_n = sum(1 for r in results if r['port_reachable'])
    print(f'Contract pass:    {pass_n}/{len(results)}')
    print(f'Port reachable:   {port_n}/{len(results)} (best-effort, conventional MCP ports)\n')
    print(f'{"NAME":40s} {"RING":5s} {"LAYER":5s} {"OWEM":18s} {"TOOLS":6s} {"CONTRACT":9s} {"PORT":6s}')
    print('-' * 110)
    for r in results:
        contract = '✓' if r['contract_ok'] else f'✗ ({", ".join(r["contract_issues"])})'
        port = str(r['port']) if r['port'] else '-'
        print(f'{r["name"]:40s} {r["ring"]!s:5s} {r["layer"]:5s} {",".join(r["owem"]):18s} {r["tools"]:6d} {contract:9s} {port:6s}')
    return 0 if pass_n == len(results) else 1

if __name__ == '__main__':
    sys.exit(main())
