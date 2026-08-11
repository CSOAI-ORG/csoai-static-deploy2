"""sovos_capability_registry — 33-MCP / 12-layer / 12-general sovereign registry.

The canonical sovereign capability registry. Loads:
  - 12 layers (L0 Core Substrate → L11 Deployment)
  - 12 generals (Zeus, Hera, Hermes, Athene, ...)
  - 5 OWEM groups (compliance, defense, intuition, voice, general)
  - 33 MCPs (sigil-chain-mcp, sovereign-brain-mcp, ...)
  - 7 hard stops (kinetic targeting, mass surveillance, ...)
  - care_floor = 0.95
  - bft_quorum_default = 23/33

This is the single source of truth for "what can the sovereign substrate
do, what must it never do, and who authorises each tool."

This package is the Pythonic wrapper; the registry lives at
`sovereign-charters/sov33-capability-registry.json` and is loaded
relative to repo root.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


REGISTRY_PATH_DEFAULT = (
    Path(__file__).resolve().parents[5]
    / "sovereign-charters"
    / "sov33-capability-registry.json"
)


@dataclass(frozen=True)
class Layer:
    id: str
    name: str
    definition: str
    owner: str  # the Greek god name


@dataclass(frozen=True)
class OwemGroup:
    id: str
    name: str
    description: str
    tools: List[str]


@dataclass(frozen=True)
class General:
    id: int
    name: str
    mythological_equivalent: str
    jurisdiction: str


@dataclass(frozen=True)
class Mcp:
    name: str
    aliases: List[str]
    ring: int
    layer: str  # "L0".."L11"
    owem: List[str]
    generals: List[int]
    status: str
    tools: List[str]
    purpose: str


@dataclass(frozen=True)
class Registry:
    canonical_frame: str
    care_floor: float
    bft_quorum_default: str  # e.g. "23/33"
    layers: List[Layer]
    owem_groups: List[OwemGroup]
    generals: List[General]
    hard_stops: List[str]
    mcps: List[Mcp]

    @property
    def layer_count(self) -> int:
        return len(self.layers)

    @property
    def general_count(self) -> int:
        return len(self.generals)

    @property
    def mcp_count(self) -> int:
        return len(self.mcps)

    @property
    def owem_count(self) -> int:
        return len(self.owem_groups)

    @property
    def hard_stop_count(self) -> int:
        return len(self.hard_stops)

    def get_mcp(self, name: str) -> Optional[Mcp]:
        for m in self.mcps:
            if m.name == name or name in m.aliases:
                return m
        return None

    def get_layer(self, layer_id: str) -> Optional[Layer]:
        for l in self.layers:
            if l.id == layer_id:
                return l
        return None

    def get_general(self, gid: int) -> Optional[General]:
        for g in self.generals:
            if g.id == gid:
                return g
        return None

    def tools_for_general(self, gid: int) -> List[str]:
        out: List[str] = []
        for m in self.mcps:
            if gid in m.generals:
                out.extend(m.tools)
        return out

    def tools_for_layer(self, layer_id: str) -> List[str]:
        out: List[str] = []
        for m in self.mcps:
            if m.layer == layer_id:
                out.extend(m.tools)
        return out

    def tools_for_owem(self, owem_id: str) -> List[str]:
        for g in self.owem_groups:
            if g.id == owem_id:
                return list(g.tools)
        return []

    def is_hard_stop(self, behaviour: str) -> bool:
        """Normalise the hard-stop rule ("No X or Y (with explanation)") and
        substring-match the core concept (or any parenthetical keyword).

        Each hard stop is a NEGATIVE rule phrased as "No X..." or
        "No X (explanation)". We strip the leading "No ", the " or Y" tail,
        and consider two candidate substrings:
          - the core rule (e.g. "sovereignty violations")
          - any 2+ word phrase from the parenthetical explanation
            (e.g. "override human authority")
        Behaviour matches if it contains ANY candidate.

        Example: "No sovereignty violations (override human authority)"
        → candidates = {"sovereignty violations", "override human authority"}
        → behaviour "the agent must override human authority here" matches.
        """
        import re
        bl = behaviour.lower()
        for h in self.hard_stops:
            raw = h.lower()
            if raw.startswith("no "):
                raw = raw[3:]
            # split " or " — first clause is the core rule
            core = raw.split(" or ")[0]
            # collect candidate substrings:
            candidates = set()
            # 1) the core, with parenthetical stripped
            core_clean = re.sub(r"\s*\([^)]*\)\s*", " ", core).strip()
            if core_clean:
                candidates.add(core_clean)
            # 2) any phrase inside parens
            for paren in re.findall(r"\(([^)]+)\)", core):
                # also strip "must be able to" type prose from the paren
                # take the first 3+ word phrase
                words = paren.split()
                if len(words) >= 2:
                    candidates.add(" ".join(words[:3]).rstrip(",."))
                    candidates.add(" ".join(words[:2]))
            # match if any candidate appears in behaviour
            if any(c and c in bl for c in candidates):
                return True
        return False


def load_registry(path: Optional[Path] = None) -> Registry:
    p = path or REGISTRY_PATH_DEFAULT
    if not p.exists():
        raise FileNotFoundError(
            f"registry not found at {p}. "
            f"Expected sovereign-charters/sov33-capability-registry.json in repo root."
        )
    d = json.loads(p.read_text())

    layers = [Layer(**l) for l in d.get("layers", [])]
    owem = [OwemGroup(**g) for g in d.get("owem_groups", [])]
    generals = [General(**g) for g in d.get("generals_regulatory_roster", [])]
    hard_stops = list(d.get("hard_stops", []))
    mcps = []
    for m in d.get("mcps", []):
        mcps.append(Mcp(
            name=m["name"],
            aliases=list(m.get("alias", [])),
            ring=m.get("ring", 0),
            layer=m.get("layer", ""),
            owem=list(m.get("owem", [])),
            generals=list(m.get("generals", [])),
            status=m.get("status", "unknown"),
            tools=list(m.get("tools", [])),
            purpose=m.get("purpose", ""),
        ))

    return Registry(
        canonical_frame=d.get("canonical_frame", ""),
        care_floor=float(d.get("care_floor", 0.95)),
        bft_quorum_default=d.get("bft_quorum_default", "23/33"),
        layers=layers,
        owem_groups=owem,
        generals=generals,
        hard_stops=hard_stops,
        mcps=mcps,
    )


__all__ = [
    "Layer",
    "OwemGroup",
    "General",
    "Mcp",
    "Registry",
    "load_registry",
    "REGISTRY_PATH_DEFAULT",
]