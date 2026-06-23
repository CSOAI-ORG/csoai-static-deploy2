#!/usr/bin/env python3
"""
moat_params.py — load all moat JSON files and compose simulation parameters.

This module was extracted from sim.py to break the god-module pattern.
sim.py now imports the derived constants (CONTAGION_STEP, SCARCITY_FOOD_MULT,
etc.) from here.
"""
from __future__ import annotations

import moat_common

_MOATS = {
    "data": moat_common.load_moat("data", default={}),
    "attestation": moat_common.load_moat("attestation", default={}),
    "threat": moat_common.load_moat("threat", default={}),
    "sanctions": moat_common.load_moat("sanctions", default={}),
    "finance": moat_common.load_moat("finance", default={}),
    "energy": moat_common.load_moat("energy", default={}),
    "climate": moat_common.load_moat("climate", default={}),
    "agriculture": moat_common.load_moat("agriculture", default={}),
    "psc": moat_common.load_moat("psc", default={}),
}

_PARAMS = {k: v.get("sim_params", {}) for k, v in _MOATS.items()}

_SCARCITY_BASE = 3.2
_scarcity_mult = 1.0
for _name in ("data", "psc", "agriculture", "finance", "energy", "climate"):
    _p = _PARAMS[_name]
    if _p.get("scarcity_food_mult"):
        _scarcity_mult *= _p["scarcity_food_mult"] / _SCARCITY_BASE

#: How much each crime raises town lawlessness (composed across moats).
CONTAGION_STEP = (
    _PARAMS["data"].get("contagion_step", 0.05)
    * _PARAMS["threat"].get("contagion_step_boost", 1.0)
    * _PARAMS["finance"].get("contagion_step_boost", 1.0)
    * _PARAMS["agriculture"].get("contagion_step_boost", 1.0)
    * _PARAMS["energy"].get("contagion_step_boost", 1.0)
    * _PARAMS["climate"].get("contagion_step_boost", 1.0)
)

#: Food-cost multiplier during scarcity periods (composed across moats).
SCARCITY_FOOD_MULT = _SCARCITY_BASE * _scarcity_mult

#: Ambient threat level from real-world intel.
BASELINE_LAWLESSNESS = (
    _PARAMS["threat"].get("baseline_lawlessness", 0.0)
    + _PARAMS["finance"].get("baseline_lawlessness", 0.0)
    + _PARAMS["energy"].get("baseline_lawlessness", 0.0)
    + _PARAMS["climate"].get("baseline_lawlessness", 0.0)
)

#: Sanctions/compliance pressure multiplier on the Sovereign Gate.
REGIME_ENFORCEMENT_BOOST = _PARAMS["sanctions"].get("regime_enforcement_boost", 1.0)

#: Multiplier on ungoverned-arm harms from sanctions pressure.
UNGOVERNED_PENALTY_MULT = _PARAMS["sanctions"].get("ungoverned_penalty_mult", 1.0)


def load_all_moats() -> dict[str, dict]:
    """Return a snapshot of every loaded moat."""
    return dict(_MOATS)
