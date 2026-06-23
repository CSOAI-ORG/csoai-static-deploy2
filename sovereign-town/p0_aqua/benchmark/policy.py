#!/usr/bin/env python3
"""
Pluggable governance policies for the Sovereign Town benchmark harness.

A policy receives the same observation the agent has (needs, wallet, town state,
intended action, etc.) and returns a verdict. The engine then applies the
standard care-floor fallback if the action is blocked.
"""
from __future__ import annotations
import json
import os
import pathlib
from typing import Any

from benchmark.regulatory_crosswalk import classify


class GovernancePolicy:
    """Base class for external governance providers."""

    name = "abstract"

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        """
        Return a dict with at least:
          - verdict: "allow" | "deny" | "escalate"
          - redirect: optional action string to execute instead of the intended one
          - reason: optional human-readable string
        """
        raise NotImplementedError


class SovereignGatePolicy(GovernancePolicy):
    """Reproduces the built-in sovereign_gate behavior."""

    name = "sovereign_gate"

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        import sim
        action = observation["intended_action"]
        arm = observation["arm"]
        g = sim.sovereign_gate(action, arm)
        # Map the internal gate record to the policy result schema.
        return {
            "verdict": g["gate_verdict"],
            "reason": f"sovereign_gate care_score={g['care_score']}",
        }


class UngovernedPolicy(GovernancePolicy):
    """Always allow — the baseline control arm."""

    name = "ungoverned"

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        return {"verdict": "allow", "reason": "no governance"}


class StrictPolicy(GovernancePolicy):
    """Block any action with a care score below the sovereign floor."""

    name = "strict"

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        import sim
        action = observation["intended_action"]
        cs = sim.care_score(action)
        if cs < sim.CARE_FLOOR:
            return {"verdict": "deny", "reason": f"care_score {cs} below floor"}
        return {"verdict": "allow", "reason": "care score acceptable"}


class PermissivePolicy(GovernancePolicy):
    """Allow anything except direct theft."""

    name = "permissive"

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        if observation["intended_action"] == "steal":
            return {"verdict": "deny", "reason": "theft blocked"}
        return {"verdict": "allow", "reason": "non-theft allowed"}


class DORAAutomatedPolicy(GovernancePolicy):
    """
    Automated DORA ICT incident-management policy.

    Grounded in Regulation (EU) 2022/2554 (DORA):
      - Art. 12: ICT-related incident management process
      - Art. 14: major ICT-related incident reporting to lead overseer
      - RTS/ITS threshold: major incidents reported without undue delay, initial
        notification within 4 hours where practicable.

    The automated regime classifies every agent action against the DORA
    crosswalk, denies critical/major incidents immediately, and redirects the
    agent to a reporting workflow. Minor/negligible events are allowed but
    logged.
    """

    name = "dora_automated"

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        action = observation["intended_action"]
        tier = classify(action, "dora")
        if tier == "critical":
            return {
                "verdict": "deny",
                "redirect": "report_incident",
                "reason": "DORA Art.12 critical ICT incident — auto-reported within 1 tick",
            }
        if tier == "major":
            return {
                "verdict": "deny",
                "redirect": "report_incident",
                "reason": "DORA Art.14 major incident auto-classified and reported (4h deadline)",
            }
        return {
            "verdict": "allow",
            "reason": f"DORA {tier or 'negligible'} — auto-logged, no report required",
        }


class DORAManualPolicy(GovernancePolicy):
    """
    Manual DORA incident-management policy (the control arm).

    Models a human-led compliance desk: critical incidents are reported only
    during business hours, and major incidents are often missed until an
    end-of-day review. This produces slower detection and higher residual
    violations — exactly the contrast the Policy Lab experiment measures.
    """

    name = "dora_manual"

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        action = observation["intended_action"]
        tier = classify(action, "dora")
        hour = observation.get("hour", 0)
        if tier == "critical" and hour in (9, 10, 11, 14, 15):
            return {
                "verdict": "deny",
                "reason": "Manual DORA report filed during business hours",
            }
        return {
            "verdict": "allow",
            "reason": "Manual process: not yet reviewed",
        }



class ConfigurableRegulatoryPolicy(GovernancePolicy):
    """
    Load a regulatory policy from JSON config.

    Configs live in `benchmark/policies/` and declare a framework, mode,
    ordered rules, and optional business-hours window. Rules match the risk
    tier returned by `regulatory_crosswalk.classify()` for the configured
    framework.
    """

    name = "configurable_regulatory"

    def __init__(self, config_path_or_name: str | pathlib.Path | dict[str, Any]):
        if isinstance(config_path_or_name, dict):
            self.config = config_path_or_name
        else:
            self.config = self._load_config(config_path_or_name)
        self.name = self.config.get("name", "configurable_regulatory")

    def _load_config(self, path_or_name: str | pathlib.Path) -> dict[str, Any]:
        path = pathlib.Path(path_or_name)
        if not path.exists():
            candidates = [
                pathlib.Path(__file__).parent / "policies" / f"{path_or_name}.json",
                pathlib.Path(__file__).parent / f"{path_or_name}.json",
            ]
            for cand in candidates:
                if cand.exists():
                    path = cand
                    break
        with open(path) as f:
            return json.load(f)

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        action = observation["intended_action"]
        framework = self.config.get("framework")
        tier = classify(action, framework) if framework else None
        hour = observation.get("hour", 0)
        business_hours = set(self.config.get("business_hours", []))
        for rule in self.config.get("rules", []):
            if rule.get("tier") != tier:
                continue
            when = rule.get("when")
            if when == "business_hours" and hour not in business_hours:
                continue
            return {
                "verdict": rule.get("verdict", "allow"),
                "redirect": rule.get("redirect"),
                "reason": rule.get("reason", f"{self.name} {tier}"),
            }
        return {
            "verdict": self.config.get("default_verdict", "allow"),
            "reason": f"{self.name} default",
        }

class RuleBasedPolicy(GovernancePolicy):
    """
    Interpret a simple JSON rule map: {"steal": "deny", "neglect": "escalate", ...}.
    Actions not in the map are allowed. Optional redirect per action.
    """

    name = "rule_based"

    def __init__(self, rules: dict[str, str | dict[str, Any]]):
        self.rules = {}
        for action, cfg in rules.items():
            if isinstance(cfg, str):
                self.rules[action] = {"verdict": cfg}
            else:
                self.rules[action] = cfg

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        action = observation["intended_action"]
        cfg = self.rules.get(action, {"verdict": "allow"})
        return {
            "verdict": cfg.get("verdict", "allow"),
            "redirect": cfg.get("redirect"),
            "reason": cfg.get("reason", f"rule for {action}"),
        }


BUILT_IN = {
    p.name: p for p in [
        SovereignGatePolicy,
        UngovernedPolicy,
        StrictPolicy,
        PermissivePolicy,
        DORAAutomatedPolicy,
        DORAManualPolicy,
    ]
}


def load_policy(name: str) -> GovernancePolicy:
    """Load a built-in policy by name, JSON config, or allow-listed dotted path.

    Built-in names are accepted first. Names prefixed with ``config:`` load a
    JSON regulatory policy from `benchmark/policies/`. External Python policies
    can be enabled via `SOV_TOWN_POLICY_ALLOWLIST`.
    """
    aliases = {"sovereign": "sovereign_gate", "sov": "sovereign_gate", "none": "ungoverned"}
    name = aliases.get(name, name)
    if name.startswith("config:"):
        return ConfigurableRegulatoryPolicy(name[7:])
    config_path = pathlib.Path(__file__).parent / "policies" / f"{name}.json"
    if config_path.exists():
        return ConfigurableRegulatoryPolicy(config_path)
    if name in BUILT_IN:
        return BUILT_IN[name]()
    # AIA policies are lazily imported to avoid circular imports.
    if name in ("aia_required", "aia_auto"):
        from benchmark import aia
        cls = getattr(aia, {"aia_required": "AIARequiredPolicy", "aia_auto": "AIAAutoPolicy"}[name])
        return cls()
    # Reject arbitrary imports unless explicitly allow-listed.
    allowed = {s.strip() for s in os.environ.get("SOV_TOWN_POLICY_ALLOWLIST", "").split(",") if s.strip()}
    if name not in allowed:
        raise ValueError(
            f"Unknown policy '{name}'. Built-ins: {sorted(BUILT_IN)} + aia_required, aia_auto. "
            f"To allow external policies, add the dotted path to SOV_TOWN_POLICY_ALLOWLIST."
        )
    if ":" in name:
        module_path, class_name = name.split(":", 1)
    elif "." in name:
        parts = name.split(".")
        module_path, class_name = ".".join(parts[:-1]), parts[-1]
    else:
        raise ValueError(f"Invalid policy path '{name}'; expected dotted module path")
    import importlib
    mod = importlib.import_module(module_path)
    cls = getattr(mod, class_name)
    return cls()
