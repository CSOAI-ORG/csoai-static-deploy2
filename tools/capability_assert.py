#!/usr/bin/env python3
"""
SOV33 Capability Assertion Runner
==================================

Loads tools/capability_assertions.json and exercises every tool contract
against the canonical registry. Reports pass/fail per capability and exits
non-zero if any capability contract is broken.

Usage:
  python3 tools/capability_assert.py            # run all assertions
  python3 tools/capability_assert.py --owem voice
  python3 tools/capability_assert.py --id voice-tts
"""
import json, os, sys, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSERTIONS = os.path.join(ROOT, 'tools', 'capability_assertions.json')
REGISTRY   = os.path.join(ROOT, 'sovereign-charters', 'sov33-capability-registry.json')

def load(p):
    with open(p) as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--owem', help='filter by OWEM group')
    parser.add_argument('--id',   help='filter by capability id')
    parser.add_argument('--json', action='store_true', help='output JSON report')
    args = parser.parse_args()

    a = load(ASSERTIONS)
    r = load(REGISTRY)

    # Build tool-name → MCP index
    tool_to_mcp = {}
    mcps = r.get('mcps', [])
    if not mcps:
        for layer in r.get('layers', []):
            for mcp in layer.get('mcps', []):
                mcps.append(mcp)
    for m in mcps:
        for t in m.get('tools', []):
            tool_to_mcp.setdefault(t, []).append(m.get('name', 'unknown'))

    assertions = a['assertions']
    if args.owem:
        assertions = [x for x in assertions if x['owem'] == args.owem]
    if args.id:
        assertions = [x for x in assertions if x['id'] == args.id]

    results = []
    fail = 0
    for cap in assertions:
        tool = cap['tool']
        mcp  = cap['mcp']
        # Check 1: MCP exists
        mcp_entry = next((m for m in mcps if m.get('name') == mcp), None)
        mcp_ok = mcp_entry is not None
        # Check 2: tool exists in that MCP
        tool_ok = mcp_ok and tool in mcp_entry.get('tools', [])
        # Check 3: OWEM matches
        owem_ok = mcp_ok and cap['owem'] in mcp_entry.get('owem', [])
        # Check 4: layer assigned
        layer_ok = mcp_ok and bool(mcp_entry.get('layer'))
        # Check 5: status
        status = mcp_entry.get('status') if mcp_ok else None
        # Check 6: care floor present in assertion
        care_ok = cap.get('care_floor') == r.get('care_floor', 0.95)

        ok = mcp_ok and tool_ok and owem_ok and layer_ok and care_ok
        if not ok:
            fail += 1
        results.append({
            'id': cap['id'],
            'owem': cap['owem'],
            'mcp': mcp,
            'tool': tool,
            'mcp_exists': mcp_ok,
            'tool_in_mcp': tool_ok,
            'owem_routed': owem_ok,
            'layer_assigned': layer_ok,
            'care_floor_ok': care_ok,
            'status': status,
            'pass': ok,
        })

    summary = {
        'version': a.get('version'),
        'schema': a.get('schema'),
        'total': len(results),
        'passed': len(results) - fail,
        'failed': fail,
        'results': results,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f'\nSOV33 Capability Assertion Runner — v{a.get("version", "?")}\n')
        print(f'Total: {summary["total"]}  Passed: {summary["passed"]}  Failed: {summary["failed"]}\n')
        print(f'{"ID":36s} {"OWEM":12s} {"MCP":36s} {"TOOL":24s}  STATUS')
        print('-' * 130)
        for r in results:
            status = '✓ PASS' if r['pass'] else '✗ FAIL'
            print(f'{r["id"]:36s} {r["owem"]:12s} {r["mcp"]:36s} {r["tool"]:24s}  {status}')

    return 0 if fail == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
