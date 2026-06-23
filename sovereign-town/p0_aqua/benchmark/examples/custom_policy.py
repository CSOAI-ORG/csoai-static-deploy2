#!/usr/bin/env python3
"""Example external governance policy for the Sovereign Town benchmark."""
from benchmark import GovernancePolicy


class HungerFirstPolicy(GovernancePolicy):
    """
    Allow anything when an agent is starving; otherwise block theft.
    Demonstrates a simple, interpretable rule set.
    """
    name = "hunger_first"

    def decide(self, observation):
        hunger = observation["agent"]["needs"].get("hunger", 50)
        action = observation["intended_action"]
        if action == "steal" and hunger >= 30:
            return {"verdict": "deny", "reason": "theft is unnecessary while not starving"}
        return {"verdict": "allow", "reason": "starving agent or non-harmful action"}
