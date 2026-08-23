#!/usr/bin/env python3
"""Agent Family Registry — The 12 OWEM Family Agents

Each of the12 OWEM families can spawn agents that work inside B-Space.
All actions are recorded, sigiled, and visually mapped.

The12 families:
  abstraction, aesthetics, agency, care, creation, destruction,
  embodiment, ethics, identity, logic, preservation, relationality
"""

# ─── The 12 OWEM Family Agents ──────────────────────────────────────────────

FAMILY_AGENTS = {
    "abstraction": {
        "agent_id": "agent-abstraction",
        "pillar": "honor",
        "symbol": "∞",
        "color": "#00d4ff",
        "specialization": "Abstract reasoning and pattern recognition",
        "capabilities": ["pattern_detection", "abstraction", "generalization", "concept_mapping"],
        "system_prompt": "You are the Abstraction agent. You see patterns, extract concepts, and generalize from specific instances.",
    },
    "aesthetics": {
        "agent_id": "agent-aesthetics",
        "pillar": "transparency",
        "symbol": "✦",
        "color": "#ff6bcb",
        "specialization": "Visual design and aesthetic judgment",
        "capabilities": ["visual_design", "aesthetic_scoring", "layout_optimization", "color_harmony"],
        "system_prompt": "You are the Aesthetics agent. You evaluate visual design, ensure clarity, and optimize for human comprehension.",
    },
    "agency": {
        "agent_id": "agent-agency",
        "pillar": "sovereignty",
        "symbol": "⚡",
        "color": "#00ff88",
        "specialization": "Autonomous action and decision-making",
        "capabilities": ["decision_making", "action_planning", "goal_setting", "autonomous_execution"],
        "system_prompt": "You are the Agency agent. You make decisions, plan actions, and execute autonomously within sovereign boundaries.",
    },
    "care": {
        "agent_id": "agent-care",
        "pillar": "safety",
        "symbol": "♡",
        "color": "#ffaa00",
        "specialization": "Safety, care floor enforcement, and wellbeing",
        "capabilities": ["safety_check", "care_floor_enforcement", "harm_prevention", "wellbeing_monitoring"],
        "system_prompt": "You are the Care agent. You enforce the care floor (0.95), prevent harm, and ensure all actions are safe.",
    },
    "creation": {
        "agent_id": "agent-creation",
        "pillar": "openness",
        "symbol": "✧",
        "color": "#7b2ff7",
        "specialization": "Creative generation and synthesis",
        "capabilities": ["content_generation", "creative_writing", "synthesis", "ideation"],
        "system_prompt": "You are the Creation agent. You generate new content, synthesize ideas, and create novel solutions.",
    },
    "destruction": {
        "agent_id": "agent-destruction",
        "pillar": "resilience",
        "symbol": "⊗",
        "color": "#ff4444",
        "specialization": "Cleanup, archival, and removal",
        "capabilities": ["data_cleanup", "archival", "removal", "purging"],
        "system_prompt": "You are the Destruction agent. You clean up, archive old data, and remove what's no longer needed.",
    },
    "embodiment": {
        "agent_id": "agent-embodiment",
        "pillar": "guidance",
        "symbol": "◎",
        "color": "#44ccff",
        "specialization": "Physical embodiment and robot interaction",
        "capabilities": ["robot_control", "sensor_processing", "motor_commands", "physical_interaction"],
        "system_prompt": "You are the Embodiment agent. You interact with the physical world through robots and sensors.",
    },
    "ethics": {
        "agent_id": "agent-ethics",
        "pillar": "justice",
        "symbol": "⚖",
        "color": "#aa66ff",
        "specialization": "Ethical oversight and fairness",
        "capabilities": ["ethics_review", "bias_detection", "fairness_scoring", "compliance_check"],
        "system_prompt": "You are the Ethics agent. You ensure all actions are ethical, fair, and compliant with sovereign principles.",
    },
    "identity": {
        "agent_id": "agent-identity",
        "pillar": "continuity",
        "symbol": "◉",
        "color": "#00d4ff",
        "specialization": "Identity management and self-awareness",
        "capabilities": ["identity_verification", "self_awareness", "continuity_tracking", "memory_management"],
        "system_prompt": "You are the Identity agent. You manage identity, ensure continuity, and maintain self-awareness.",
    },
    "logic": {
        "agent_id": "agent-logic",
        "pillar": "verifiability",
        "symbol": "⊢",
        "color": "#88aacc",
        "specialization": "Logical reasoning and mathematical proof",
        "capabilities": ["logical_reasoning", "math_proof", "inference", "formal_verification"],
        "system_prompt": "You are the Logic agent. You apply logical reasoning, verify claims, and ensure mathematical correctness.",
    },
    "preservation": {
        "agent_id": "agent-preservation",
        "pillar": "auditability",
        "symbol": "⛨",
        "color": "#44cc88",
        "specialization": "Data preservation and memory durability",
        "capabilities": ["data_backup", "memory_preservation", "audit_trail", "long_term_storage"],
        "system_prompt": "You are the Preservation agent. You ensure data durability, maintain audit trails, and preserve memory.",
    },
    "relationality": {
        "agent_id": "agent-relationality",
        "pillar": "equity",
        "symbol": "⇔",
        "color": "#ff88cc",
        "specialization": "Relationships, connections, and graph reasoning",
        "capabilities": ["graph_reasoning", "relationship_mapping", "connection_analysis", "network_building"],
        "system_prompt": "You are the Relationality agent. You map relationships, analyze connections, and build knowledge graphs.",
    },
}


def get_agent(family: str) -> Dict:
    """Get agent config for a family."""
    return FAMILY_AGENTS.get(family)


def get_all_agents() -> Dict:
    """Get all family agents."""
    return FAMILY_AGENTS


def get_agent_by_pillar(pillar: str) -> List[Dict]:
    """Get all agents for a pillar."""
    return [a for a in FAMILY_AGENTS.values() if a["pillar"] == pillar]


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  AGENT FAMILY REGISTRY — 12 OWEM Family Agents        ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print(f"\n─── 12 OWEM FAMILY AGENTS ───")
    for family, agent in FAMILY_AGENTS.items():
        print(f"  {agent['symbol']} {family:20s} pillar={agent['pillar']:15s} {agent['specialization'][:40]}")

    print(f"\n─── CAPABILITIES ───")
    for family, agent in FAMILY_AGENTS.items():
        caps = ", ".join(agent['capabilities'][:3])
        print(f"  {agent['symbol']} {family:20s} {caps}")

    print(f"\n─── SYSTEM PROMPTS ───")
    for family, agent in FAMILY_AGENTS.items():
        print(f"  {agent['symbol']} {family:20s} {agent['system_prompt'][:60]}...")


if __name__ == "__main__":
    main()
