#!/usr/bin/env python3
"""
SOV33 Capability Registry Verifier
==================================

Validates /Users/nicholas/clawd/csoai-static-deploy2/sovereign-charters/sov33-capability-registry.json
against the canonical SOV3 substrate rules:

  - All 12 layers present and ordered L0 -> L11
  - All 5 OWEM groups defined and only those referenced by mcps[].owem
  - All 12 numbered generals (1..12) mapped to mythological equivalents
  - Every MCP has: name, ring, layer, owem, generals, status, tools (>=1), purpose
  - Ring ∈ {0, 1, 2, "G"} (Greenfield)
  - Layer must be a canonical layer id from layers[]
  - owem entries must exist in owem_groups[]
  - generals entries must be ints in 1..12
  - status ∈ {live, stage, planned, retired}
  - Tools within an MCP must be unique
  - Aliases must not collide with other canonical names
  - Every MCP should have at least one OWEM entry that owns it
  - Hard-stops list must be 7 entries (DORADO red lines)

Outputs a pass/fail report and exits non-zero on any failure.

Usage:
  python3 tools/verify_capability_registry.py
"""
import json, os, sys
from collections import Counter

REGISTRY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'sovereign-charters', 'sov33-capability-registry.json'
)

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)

def fail(msg, errors):
    errors.append(msg)
    print(f"  ✗ FAIL: {msg}")

def ok(msg):
    print(f"  ✓ {msg}")

def main():
    print(f"\n=== SOV33 Capability Registry Verifier ===")
    print(f"Path: {REGISTRY_PATH}\n")

    try:
        r = load_registry()
    except Exception as e:
        print(f"FATAL: cannot load registry: {e}")
        return 2

    errors = []
    warnings = []

    # ----- FRAMEWORK -----
    print("[1] Canonical Frame")
    if r.get('canonical_frame') != '12-layer-maternal-sovereign-stack':
        fail(f"canonical_frame = {r.get('canonical_frame')!r}", errors)
    else:
        ok("canonical_frame = '12-layer-maternal-sovereign-stack'")

    if r.get('care_floor') != 0.95:
        fail(f"care_floor = {r.get('care_floor')!r} (expected 0.95)", errors)
    else:
        ok("care_floor = 0.95")

    if r.get('bft_quorum_default') != '23/33':
        fail(f"bft_quorum_default = {r.get('bft_quorum_default')!r}", errors)
    else:
        ok("bft_quorum_default = 23/33")

    # ----- LAYERS -----
    print("\n[2] Layers (must be 12, ordered L0..L11)")
    layers = r.get('layers', [])
    if len(layers) != 12:
        fail(f"expected 12 layers, found {len(layers)}", errors)
    else:
        ok(f"12 layers present")
    expected_ids = [f"L{i}" for i in range(12)]
    actual_ids = [l['id'] for l in layers]
    if actual_ids != expected_ids:
        fail(f"layer order {actual_ids} != {expected_ids}", errors)
    else:
        ok("layers ordered L0..L11")

    layer_ids_set = set(actual_ids)
    for l in layers:
        for field in ['id', 'name', 'definition', 'owner']:
            if field not in l:
                fail(f"layer {l.get('id','?')} missing field {field!r}", errors)

    # ----- OWEM GROUPS -----
    print("\n[3] OWEM Groups (must be 5)")
    owems = r.get('owem_groups', [])
    if len(owems) != 5:
        fail(f"expected 5 OWEM groups, found {len(owems)}", errors)
    else:
        ok("5 OWEM groups")
    owem_ids = {o['id'] for o in owems}
    expected_owem_ids = {'compliance','defense','intuition','voice','general'}
    if owem_ids != expected_owem_ids:
        fail(f"OWEM ids {owem_ids} != {expected_owem_ids}", errors)
    else:
        ok(f"OWEM ids = {sorted(owem_ids)}")

    # ----- GENERALS -----
    print("\n[4] Generals (12 numbered regulatory roster)")
    generals = r.get('generals_regulatory_roster', [])
    if len(generals) != 12:
        fail(f"expected 12 generals, found {len(generals)}", errors)
    else:
        ok("12 generals")
    expected_ids = list(range(1, 13))
    actual_ids = sorted(g['id'] for g in generals)
    if actual_ids != expected_ids:
        fail(f"general ids {actual_ids} != {expected_ids}", errors)
    else:
        ok("general ids 1..12 complete")
    myth_set = set(g['mythological_equivalent'] for g in generals)
    if len(myth_set) != 12:
        fail(f"mythological roster has duplicates: {myth_set}", errors)
    else:
        ok("12 unique mythological equivalents (Athena/Hermes/Apollo/etc.)")

    # ----- HARD STOPS -----
    print("\n[5] Hard stops (must be 7 red lines)")
    stops = r.get('hard_stops', [])
    if len(stops) != 7:
        fail(f"expected 7 hard stops, found {len(stops)}", errors)
    else:
        ok(f"7 hard stops")
        for i, s in enumerate(stops, 1):
            print(f"     {i}. {s}")

    # ----- MCPS -----
    print("\n[6] MCPs (each must satisfy schema)")
    mcps = r.get('mcps', [])
    print(f"     total MCPs: {len(mcps)}")
    canonical_names = set()
    all_aliases = set()
    ring_counts = Counter()
    layer_counts = Counter()
    status_counts = Counter()
    tool_names_global = []

    for i, m in enumerate(mcps):
        name = m.get('name', f'<unnamed-{i}>')
        prefix = f"mcp[{name}]"

        # Required fields
        for field in ['name','ring','layer','owem','generals','status','tools','purpose']:
            if field not in m:
                fail(f"{prefix}: missing field {field!r}", errors)

        if name in canonical_names:
            fail(f"{prefix}: duplicate canonical name {name!r}", errors)
        canonical_names.add(name)

        # Aliases
        for alias in m.get('alias', []):
            if alias in canonical_names:
                fail(f"{prefix}: alias {alias!r} collides with canonical name", errors)
            if alias in all_aliases:
                fail(f"{prefix}: alias {alias!r} duplicates another alias", errors)
            all_aliases.add(alias)

        # Ring
        ring = m.get('ring')
        if ring not in (0, 1, 2, 'G'):
            fail(f"{prefix}: ring {ring!r} not in (0,1,2,'G')", errors)
        ring_counts[ring] += 1

        # Layer
        layer = m.get('layer')
        if layer not in layer_ids_set:
            fail(f"{prefix}: layer {layer!r} not in canonical layers", errors)
        layer_counts[layer] += 1

        # OWEM
        owem_list = m.get('owem', [])
        if not owem_list:
            fail(f"{prefix}: empty owem list", errors)
        for o in owem_list:
            if o not in owem_ids:
                fail(f"{prefix}: owem {o!r} not in canonical OWEM ids", errors)

        # Generals
        gen_list = m.get('generals', [])
        if not gen_list:
            warnings.append(f"{prefix}: empty generals list (no BFT coverage)")
        for g_id in gen_list:
            if not isinstance(g_id, int) or not (1 <= g_id <= 12):
                fail(f"{prefix}: general id {g_id!r} not in 1..12", errors)

        # Status
        status = m.get('status')
        if status not in ('live','stage','planned','retired'):
            fail(f"{prefix}: status {status!r} not in (live,stage,planned,retired)", errors)
        status_counts[status] += 1

        # Tools
        tools = m.get('tools', [])
        if not tools:
            fail(f"{prefix}: zero tools", errors)
        if len(set(tools)) != len(tools):
            fail(f"{prefix}: duplicate tools within MCP", errors)
        for t in tools:
            if not isinstance(t, str) or not t.replace('_','').isalnum():
                fail(f"{prefix}: tool {t!r} not snake_case identifier", errors)
            tool_names_global.append((name, t))

    print(f"     ring distribution: {dict(ring_counts)}")
    print(f"     layer distribution: {dict(sorted(layer_counts.items()))}")
    print(f"     status distribution: {dict(status_counts)}")

    # Cross-MCP tool name uniqueness
    seen_tools = {}
    for mcp, tool in tool_names_global:
        if tool in seen_tools and seen_tools[tool] != mcp:
            warnings.append(f"tool {tool!r} appears in both {mcp} and {seen_tools[tool]}")
        seen_tools[tool] = mcp

    # ----- CHECK FOR ALL NAMED MCPs IN THE REGISTRY APPEAR ON THE SITE -----
    print("\n[7] Backlink coverage (every MCP name should appear on the site)")
    site_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_files = []
    for root, dirs, files in os.walk(site_root):
        # skip .git, .backups, public
        if any(skip in root for skip in ['.git','.backups','node_modules','__pycache__']):
            continue
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    # Concatenate all HTML for substring search
    site_text = ''
    for path in html_files:
        try:
            with open(path) as fh:
                site_text += fh.read() + '\n'
        except Exception:
            pass

    missing = []
    for m in mcps:
        if m['name'] not in site_text:
            missing.append(m['name'])
    print(f"     MCPs with at least one site reference: {len(mcps) - len(missing)}/{len(mcps)}")
    if missing:
        warnings.append(f"{len(missing)} MCPs have no site reference yet (likely staged greenfield MCPs)")
        for m in missing[:5]:
            print(f"     ⚠ no reference: {m}")
        if len(missing) > 5:
            print(f"     … and {len(missing)-5} more")

    # ----- SUMMARY -----
    print("\n=== SUMMARY ===")
    print(f"  MCPs:                {len(mcps)}")
    print(f"  Tools:               {len(tool_names_global)}")
    print(f"  Live MCPs:           {status_counts.get('live',0)}")
    print(f"  Staged MCPs:         {status_counts.get('stage',0)}")
    print(f"  Ring 0 (Core):       {ring_counts.get(0,0)}")
    print(f"  Ring 1 (Sensors):    {ring_counts.get(1,0)}")
    print(f"  Ring 2 (Civil):      {ring_counts.get(2,0)}")
    print(f"  Greenfield:          {ring_counts.get('G',0)}")
    print()
    print(f"  Errors:   {len(errors)}")
    print(f"  Warnings: {len(warnings)}")

    if errors:
        print("\n=== ERRORS ===")
        for e in errors:
            print(f"  ✗ {e}")
        return 1

    if warnings:
        print("\n=== WARNINGS ===")
        for w in warnings:
            print(f"  ⚠ {w}")

    print("\n✓ Registry verification PASSED")
    return 0

if __name__ == '__main__':
    sys.exit(main())
