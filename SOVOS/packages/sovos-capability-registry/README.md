# sovos-capability-registry

The **canonical 33-MCP / 12-layer / 12-general sovereign capability registry**, loaded from `sovereign-charters/sov33-capability-registry.json` and exposed as typed Python.

## What it ships

- `Registry` — frozen dataclass holding the entire registry
- `Layer`, `OwemGroup`, `General`, `Mcp` — typed row dataclasses
- `load_registry()` — loads from repo-relative JSON
- Query helpers: `get_mcp(name|alias)`, `get_layer(id)`, `get_general(id)`, `tools_for_general(id)`, `tools_for_layer(id)`, `tools_for_owem(id)`
- `is_hard_stop(behaviour)` — strips the "No X" negation and substring-matches the canonical 7 hard stops

## Canonical numbers (verified 2026-08-11)

| Quantity | Value |
|---|---|
| Layers | 12 (L0..L11) |
| Generals | 12 (the Olympians) |
| OWEM groups | 5 (compliance, defense, intuition, voice, general) |
| MCPs | 33 |
| Tools across all MCPs | **111** (the verified count) |
| Hard stops | 7 (kinetic targeting, mass surveillance, sovereignty violation, auto-escalation, deception, irreversibility, AGI/ASI w/o ratification) |
| Care floor | 0.95 |
| BFT quorum default | 23/33 |

## Registry inconsistencies caught on load (audit notes)

The registry JSON has **two known inconsistencies** that this package handles but should be canonicalised in the next registry pass:

1. **Case: layer owners are lowercase (`hermes`), generals are title-case (`Hermes`).** `is_hard_stop()` and the layer/general comparison helpers normalise to lowercase.
2. **Layer IDs sort lexicographically (`L0, L1, L10, L11, L2, ...`)** — natural-sort by numeric suffix is required. The L0–L11 order is preserved in `tools_for_layer()` only because we iterate the parsed list (which is already in numeric order in the source JSON); user code that sorts layer IDs should use `key=lambda s: int(s[1:])`.

Both are documented in the test suite (`test_04b_registry_inconsistency_owners_case_is_known_gap`).

## Quick start

```python
from sovos_capability_registry import load_registry
r = load_registry()
print(r.care_floor, r.bft_quorum_default)  # 0.95, 23/33
print(r.mcp_count, r.layer_count, r.general_count)  # 33, 12, 12

# tool surface
print(r.tools_for_general(12))  # Zeus's tool surface
print(r.tools_for_layer("L0"))   # Core Substrate tools

# governance: refuse bad behaviour
if r.is_hard_stop("deploy an autonomous kinetic targeting drone"):
    raise PermissionError("hard stop: kinetic targeting")
```

## Test status

22/22 green on A100 (`pip install pytest`, run from repo root).