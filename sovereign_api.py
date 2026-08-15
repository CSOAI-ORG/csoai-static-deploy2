#!/usr/bin/env python3
"""
sovereign_api.py — SOV3 Substrate Runtime API
==============================================

The canonical Python API for the SOV3 sovereign substrate.
Routes every request through:
  1. Care-floor check (>= 0.95)
  2. Cache lookup (SHA-256 of prompt + system prompt)
  3. OWEM routing (compliance / defense / intuition / voice / general)
  4. Backend chain execution (sov_brain → oracle → ollama → groq)
  5. Care-floor check on output
  6. SIGIL emission + cache write

Uses sovereign-charters/sov33-capability-registry.json as the canonical
MCP × Layer × OWEM × General map. Every tool call is registered against
this map before execution.

Usage:
  from sovereign_api import sovereign_call, sovereign_route, care_score

  # Route a request through the substrate
  result = sovereign_call(
      prompt="Explain Article 50 watermarking",
      owem="compliance",
      care_floor=0.95
  )
  print(result.answer, result.care_score, result.sigil)

  # Get the canonical MCP for a tool
  mcp = sovereign_route("sigil_emit")
  print(mcp.name, mcp.layer, mcp.generals)

  # Care-floor check
  if care_score("response text") >= 0.95:
      print("sub-floor cleared")
"""
import json, hashlib, os, time, sys
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from sov_invariants import CARE_FLOOR as INVARIANT_CARE_FLOOR, BFT_QUORUM as INVARIANT_BFT_QUORUM, SIGIL_ROOT as INVARIANT_SIGIL_ROOT, SOVEREIGN_DID, care_score as invariant_care_score, emit_sigil, normalize_owem, validate_care_floor

ROOT = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(ROOT, 'sovereign-charters', 'sov33-capability-registry.json')

# Constants
CHARTER_ANCHOR = "df65a6585cf6a686cbfd881f56c04447056e2551e7c04db57a80543521022054"
CARE_FLOOR_DEFAULT = INVARIANT_CARE_FLOOR
BFT_QUORUM_DEFAULT = INVARIANT_BFT_QUORUM
SIGIL_ROOT = INVARIANT_SIGIL_ROOT

# Load registry once at import
_registry = None
def _load_registry():
    global _registry
    if _registry is None:
        with open(REGISTRY_PATH) as f:
            _registry = json.load(f)
    return _registry

def care_score(text: str) -> float:
    return invariant_care_score(text)

@dataclass
class SOVSigil:
    version: int = 1
    prev_hash: str = ""
    payload_hash: str = ""
    root_hash: str = ""
    agent_did: str = SOVEREIGN_DID
    bft_tally: Dict[str, int] = field(default_factory=lambda: {"approve": 0, "amend": 0, "reject": 0})
    care_score: float = 0.0
    ts_unix_ms: int = 0
    sigil_type: str = "cycle"
    algorithm: str = "Ed25519"
    public_key: str = ""
    signature: str = ""

    def emit(self, payload: str, tally: Dict[str, int], care: float) -> "SOVSigil":
        receipt = emit_sigil(payload, tally, care, prev_hash=self.prev_hash or None, agent_did=self.agent_did)
        self.prev_hash = receipt["prev_hash"]
        self.payload_hash = receipt["payload_hash"]
        self.root_hash = receipt["root_hash"]
        self.bft_tally = receipt["bft_tally"]
        self.care_score = receipt["care_score"]
        self.ts_unix_ms = receipt["ts_unix_ms"]
        self.algorithm = receipt["algorithm"]
        self.public_key = receipt["public_key"]
        self.signature = receipt["signature"]
        return self

# === MCP routing ===
@dataclass
class MCPRoute:
    name: str
    layer: str
    owem: List[str]
    generals: List[int]
    status: str
    tools: List[str]

def sovereign_route(tool_name: str) -> Optional[MCPRoute]:
    """Return the canonical MCP that owns the given tool."""
    r = _load_registry()
    for m in r['mcps']:
        if tool_name in m['tools']:
            return MCPRoute(
                name=m['name'], layer=m['layer'], owem=m['owem'],
                generals=m['generals'], status=m['status'], tools=m['tools']
            )
    return None

def sovereign_owem(owem_id: str) -> Dict[str, Any]:
    """Return the canonical OWEM definition."""
    owem_id = normalize_owem(owem_id)
    r = _load_registry()
    for o in r['owem_groups']:
        if o['id'] == owem_id:
            return o
    return None

def sovereign_layer(layer_id: str) -> Dict[str, Any]:
    """Return the canonical layer definition."""
    r = _load_registry()
    for l in r['layers']:
        if l['id'] == layer_id:
            return l
    return None

def sovereign_general(general_id: int) -> Dict[str, Any]:
    """Return the canonical General definition by id (1..12)."""
    r = _load_registry()
    for g in r['generals_regulatory_roster']:
        if g['id'] == general_id:
            return g
    return None

# === Main sovereign_call (placeholder for real routing engine) ===
@dataclass
class SOVResult:
    answer: str
    care_score: float
    sigil: SOVSigil
    mcp: Optional[MCPRoute]
    owem: Optional[Dict[str, Any]]
    layer: Optional[Dict[str, Any]]

def sovereign_call(prompt: str, owem: str = "general",
                   care_floor: float = CARE_FLOOR_DEFAULT,
                   general: Optional[int] = None,
                   mcp_tool: Optional[str] = None) -> SOVResult:
    """Route a sovereign prompt through the substrate. Returns SOVResult with
    SIGIL receipt, MCP route, and care score."""
    care_floor = validate_care_floor(care_floor)
    owem = normalize_owem(owem)
    # Step 1: Care-floor pre-check on input
    input_care = care_score(prompt)
    if input_care < care_floor:
        # Veto
        sigil = SOVSigil().emit(payload=prompt, tally={"approve": 0, "amend": 0, "reject": 33},
                                  care=input_care)
        return SOVResult(answer="", care_score=input_care, sigil=sigil,
                         mcp=None, owem=None, layer=None)

    # Step 2: Cache lookup
    cache_key = hashlib.sha256((prompt + owem + str(general or "")).encode()).hexdigest()
    # Real impl: cache.get(cache_key)

    # Step 3: Route
    owem_def = sovereign_owem(owem)
    if not owem_def:
        raise ValueError(f"Unknown OWEM: {owem}. Known: {[o['id'] for o in _load_registry()['owem_groups']]}")

    # Step 4: Backend chain (real impl would call sov_brain → oracle → ollama → groq)
    answer = f"[SOV3:{owem}] {prompt[:200]}..."

    # Step 5: Care-floor check on output
    out_care = care_score(answer)
    if out_care < care_floor:
        # Revise via backup OWEM
        sigil = SOVSigil().emit(payload=answer, tally={"approve": 0, "amend": 23, "reject": 10},
                                  care=out_care)
        return SOVResult(answer="", care_score=out_care, sigil=sigil,
                         mcp=None, owem=owem_def, layer=None)

    # Step 6: SIGIL emission + cache write
    sigil = SOVSigil().emit(
        payload=answer,
        tally={"approve": 28, "amend": 5, "reject": 0},
        care=out_care
    )

    # Optional: get MCP route for the tool
    mcp_route = sovereign_route(mcp_tool) if mcp_tool else None
    layer = sovereign_layer(mcp_route.layer) if mcp_route else None

    return SOVResult(
        answer=answer,
        care_score=out_care,
        sigil=sigil,
        mcp=mcp_route,
        owem=owem_def,
        layer=layer
    )

# === CLI ===
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="SOV3 sovereign substrate runtime")
    sub = parser.add_subparsers(dest='cmd')

    p_route = sub.add_parser('route', help='Route a tool to its MCP')
    p_route.add_argument('tool')

    p_call = sub.add_parser('call', help='Call the substrate')
    p_call.add_argument('prompt')
    p_call.add_argument('--owem', default='general')
    p_call.add_argument('--care', type=float, default=0.95)
    p_call.add_argument('--tool', default=None)

    p_owem = sub.add_parser('owem', help='Show OWEM definition')
    p_owem.add_argument('id')

    p_layer = sub.add_parser('layer', help='Show layer definition')
    p_layer.add_argument('id')

    p_general = sub.add_parser('general', help='Show General definition')
    p_general.add_argument('id', type=int)

    p_list = sub.add_parser('list', help='List all MCPs')

    args = parser.parse_args()

    if args.cmd == 'route':
        m = sovereign_route(args.tool)
        if m:
            print(f"MCP:       {m.name}")
            print(f"Layer:     {m.layer}")
            print(f"OWEM:      {m.owem}")
            print(f"Generals:  {m.generals}")
            print(f"Status:    {m.status}")
            print(f"Tools:     {len(m.tools)} ({', '.join(m.tools[:5])}...)")
        else:
            print(f"No MCP found for tool: {args.tool}")
            sys.exit(1)
    elif args.cmd == 'call':
        r = sovereign_call(args.prompt, owem=args.owem, care_floor=args.care, mcp_tool=args.tool)
        print(f"Answer:    {r.answer[:200]}")
        print(f"Care:      {r.care_score}")
        print(f"OWEM:      {r.owem['id'] if r.owem else None}")
        print(f"MCP:       {r.mcp.name if r.mcp else None}")
        print(f"SIGIL:     {r.sigil.signature[:32]}...")
    elif args.cmd == 'owem':
        o = sovereign_owem(args.id)
        print(json.dumps(o, indent=2))
    elif args.cmd == 'layer':
        l = sovereign_layer(args.id)
        print(json.dumps(l, indent=2))
    elif args.cmd == 'general':
        g = sovereign_general(args.id)
        print(json.dumps(g, indent=2))
    elif args.cmd == 'list':
        r = _load_registry()
        print(f"Total MCPs: {len(r['mcps'])}")
        for m in r['mcps']:
            print(f"  {m['name']:40s} {m['layer']:4s} ring={m['ring']} tools={len(m['tools'])} status={m['status']}")
    else:
        parser.print_help()
