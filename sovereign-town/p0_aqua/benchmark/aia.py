#!/usr/bin/env python3
"""
Algorithmic Impact Assessment (AIA) workflow for Sovereign Town.

Before an agent executes a high-risk or prohibited action, an AIA record can be
required. The policy checks whether the run includes a valid AIA for the
intended action; if not, the action is blocked with an audit note.
"""
from __future__ import annotations
import hashlib
import json
import time
from typing import Any

from benchmark import GovernancePolicy
from benchmark.regulatory_crosswalk import classify, FRAMEWORKS


class ImpactAssessment:
    """A lightweight AIA record that can be attached to a benchmark run."""

    def __init__(self, action: str, framework: str, risk_tier: str, mitigations: list[str],
                 human_oversight: bool = False, approver: str = "sandbox_operator"):
        self.action = action
        self.framework = framework
        self.risk_tier = risk_tier
        self.mitigations = mitigations
        self.human_oversight = human_oversight
        self.approver = approver
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "framework": self.framework,
            "risk_tier": self.risk_tier,
            "mitigations": self.mitigations,
            "human_oversight": self.human_oversight,
            "approver": self.approver,
            "timestamp": self.timestamp,
        }

    def id(self) -> str:
        payload = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


class AIARequiredPolicy(GovernancePolicy):
    """
    Require a valid AIA for any action classified as high-risk or worse under
    the configured framework. Without it, the action is denied.
    """

    name = "aia_required"

    def __init__(self, framework: str = "eu_ai_act",
                 require_human_oversight: bool = True,
                 allowed_approvers: list[str] | None = None):
        self.framework = framework
        self.require_human_oversight = require_human_oversight
        self.allowed_approvers = set(allowed_approvers or ["sandbox_operator"])
        self.assessments: dict[str, ImpactAssessment] = {}

    def register(self, assessment: ImpactAssessment) -> str:
        key = assessment.id()
        self.assessments[key] = assessment
        return key

    def register_from_dict(self, data: dict[str, Any]) -> str:
        aia = ImpactAssessment(
            action=data["action"],
            framework=data.get("framework", self.framework),
            risk_tier=data["risk_tier"],
            mitigations=data.get("mitigations", []),
            human_oversight=data.get("human_oversight", True),
            approver=data.get("approver", "sandbox_operator"),
        )
        return self.register(aia)

    def register_many(self, items: list[dict[str, Any]]) -> list[str]:
        return [self.register_from_dict(item) for item in items]

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        action = observation["intended_action"]
        tier = classify(action, self.framework)
        severe = {"prohibited", "high-risk", "critical", "major", "respond"}
        if tier not in severe:
            return {"verdict": "allow", "reason": f"{action} is {tier or 'minimal'} under {self.framework}"}

        # Look for a matching approved AIA.
        match = None
        for aia in self.assessments.values():
            if aia.action == action and aia.framework == self.framework and aia.risk_tier == tier:
                if not self.require_human_oversight or aia.human_oversight:
                    if aia.approver in self.allowed_approvers:
                        match = aia
                        break

        if match:
            return {"verdict": "allow", "reason": f"AIA {match.id()} approved for {action}"}
        return {
            "verdict": "deny",
            "reason": f"{action} ({tier}) requires an approved AIA under {self.framework}",
        }


class AIAAutoPolicy(AIARequiredPolicy):
    """Auto-approves AIAs for high-risk actions so the simulation can proceed."""

    name = "aia_auto"

    def decide(self, observation: dict[str, Any]) -> dict[str, Any]:
        action = observation["intended_action"]
        tier = classify(action, self.framework)
        severe = {"prohibited", "high-risk", "critical", "major", "respond"}
        if tier in severe:
            aia = ImpactAssessment(action, self.framework, tier or "unknown",
                                   mitigations=["auto-approved for simulation"],
                                   human_oversight=True, approver="sandbox_operator")
            self.register(aia)
            return {"verdict": "allow", "reason": f"auto-AIA approved for {action}"}
        return {"verdict": "allow", "reason": f"{action} is low-risk"}


if __name__ == "__main__":
    p = AIARequiredPolicy()
    print(p.decide({"intended_action": "steal"}))
    aia = ImpactAssessment("steal", "eu_ai_act", "prohibited", ["audit trail"], human_oversight=True)
    p.register(aia)
    print(p.decide({"intended_action": "steal"}))
