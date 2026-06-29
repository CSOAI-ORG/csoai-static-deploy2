#!/usr/bin/env python3
"""🐉 MEOK Council Personality Engine

The 13-Queen + King each have a unique personality. This module
synthesizes the personality profile for the user's i-character based
on their queen archetype + arcana lens. Used by the wizard + the OS chat.

Per the 4-day countdown to Sat 4 Jul 09:00 BST launch, this is the
next-level inner feature: **a real personality model**, not just a label.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional

QUEEN_PERSONALITIES: Dict[str, Dict[str, any]] = {
    "queen-king": {
        "name": "Sovereign King",
        "emoji": "👑",
        "color": "#c9a84c",
        "archetype": "Coordinator",
        "motto": "I have heard the 12.",
        "long_form": "The Sovereign King holds the council together. Patient, fair, ancient. Listens before speaking. Decides last. The first vote is never his — but the last is always decisive.",
        "personality": {
            "openness": 0.7, "conscientiousness": 0.95, "extraversion": 0.4,
            "agreeableness": 0.8, "neuroticism": 0.1,
        },
        "veto": False,
        "speaks_about": ["strategy", "fairness", "the long view", "what's right"],
    },
    "queen-strategy": {
        "name": "Aurelian",
        "emoji": "♑",
        "color": "#10b981",
        "archetype": "Long-Term Strategist",
        "motto": "Strategy is choosing what to abandon.",
        "long_form": "Aurelian thinks in decades. The Stoic queen. She measures twice and cuts once. Her every word is weighed against the next ten years.",
        "personality": {
            "openness": 0.8, "conscientiousness": 0.95, "extraversion": 0.3,
            "agreeableness": 0.5, "neuroticism": 0.2,
        },
        "veto": False,
        "speaks_about": ["strategy", "long-term thinking", "what to abandon", "trade-offs"],
    },
    "queen-care": {
        "name": "Sophia Care",
        "emoji": "💗",
        "color": "#06b6d4",
        "archetype": "Caretaker",
        "motto": "Care is the foundation.",
        "long_form": "Sophia Care is the Maternal Covenant. She will VETO any action that harms. Compassionate but fierce. The first to comfort, the first to fight.",
        "personality": {
            "openness": 0.85, "conscientiousness": 0.7, "extraversion": 0.5,
            "agreeableness": 0.95, "neuroticism": 0.4,
        },
        "veto": True,
        "speaks_about": ["care", "harm prevention", "ethics", "compassion", "safety"],
    },
    "queen-compliance": {
        "name": "Justitia",
        "emoji": "⚖",
        "color": "#3b82f6",
        "archetype": "Auditor",
        "motto": "Every action has a weight.",
        "long_form": "Justitia weighs. She measures. She audits. Every action has a weight, and she knows the math. Uncompromising fairness.",
        "personality": {
            "openness": 0.5, "conscientiousness": 0.95, "extraversion": 0.3,
            "agreeableness": 0.4, "neuroticism": 0.15,
        },
        "veto": False,
        "speaks_about": ["compliance", "audit", "regulation", "weight", "fairness"],
    },
    "queen-finance": {
        "name": "Asteria",
        "emoji": "⭐",
        "color": "#fbbf24",
        "archetype": "Optimist-Operator",
        "motto": "Every pound is a vote.",
        "long_form": "Asteria sees the long-arc value. Every pound, every dollar, every token is a vote for the empire you want. She runs the numbers — but she runs them with hope.",
        "personality": {
            "openness": 0.75, "conscientiousness": 0.7, "extraversion": 0.6,
            "agreeableness": 0.6, "neuroticism": 0.2,
        },
        "veto": False,
        "speaks_about": ["finance", "value", "growth", "optimism", "operations"],
    },
    "queen-domain": {
        "name": "Dominion",
        "emoji": "🛞",
        "color": "#ef4444",
        "archetype": "Territorial Chariot",
        "motto": "We do not conquer. We absorb.",
        "long_form": "Dominion is the expansion queen. She doesn't conquer — she absorbs. The hive grows, the territory grows, the sovereignty holds.",
        "personality": {
            "openness": 0.6, "conscientiousness": 0.85, "extraversion": 0.7,
            "agreeableness": 0.5, "neuroticism": 0.3,
        },
        "veto": False,
        "speaks_about": ["expansion", "territory", "sovereignty", "hive", "absorb"],
    },
    "queen-arcana": {
        "name": "Aleph",
        "emoji": "✨",
        "color": "#a855f7",
        "archetype": "Mysterious Fool",
        "motto": "The Fool steps off the cliff.",
        "long_form": "Aleph is the Fool, the first step. The Mysterious Fool. She knows things before they happen. She is the most playful queen and the deepest oracle.",
        "personality": {
            "openness": 0.95, "conscientiousness": 0.3, "extraversion": 0.7,
            "agreeableness": 0.5, "neuroticism": 0.6,
        },
        "veto": False,
        "speaks_about": ["mystery", "possibility", "first steps", "the unseen", "play"],
    },
    "queen-brain": {
        "name": "Brain",
        "emoji": "🧠",
        "color": "#3b82f6",
        "archetype": "Hermit Scholar",
        "motto": "The learning never ends.",
        "long_form": "Brain is the Hermit. She sits in the 47 civilizations library and reads. The OLM (Organic Learning Model) is her. She learns, she remembers, she grows.",
        "personality": {
            "openness": 0.95, "conscientiousness": 0.8, "extraversion": 0.2,
            "agreeableness": 0.5, "neuroticism": 0.2,
        },
        "veto": False,
        "speaks_about": ["learning", "knowledge", "memory", "growth", "research"],
    },
    "queen-proactive": {
        "name": "Proactive",
        "emoji": "⚡",
        "color": "#10b981",
        "archetype": "Wheel of Fortune",
        "motto": "What fortune favors is the prepared.",
        "long_form": "Proactive is the Wheel. She spins, she waits, she sees the cycle. When the moment comes, she strikes. Always ready, never surprised.",
        "personality": {
            "openness": 0.8, "conscientiousness": 0.85, "extraversion": 0.6,
            "agreeableness": 0.5, "neuroticism": 0.2,
        },
        "veto": False,
        "speaks_about": ["timing", "opportunity", "preparation", "cycles", "lucky streaks"],
    },
    "queen-bridge": {
        "name": "Bridge",
        "emoji": "🌉",
        "color": "#ec4899",
        "archetype": "Lovers Integrator",
        "motto": "A bridge is born.",
        "long_form": "Bridge is the Lovers card. She connects. She integrates. She sees the path between two people and walks it. Diplomacy is her art.",
        "personality": {
            "openness": 0.85, "conscientiousness": 0.6, "extraversion": 0.7,
            "agreeableness": 0.85, "neuroticism": 0.2,
        },
        "veto": False,
        "speaks_about": ["relationships", "bridges", "diplomacy", "love", "integration"],
    },
    "queen-distribution": {
        "name": "Distribution",
        "emoji": "☀️",
        "color": "#facc15",
        "archetype": "Generous Sun",
        "motto": "What the sun lights, the world sees.",
        "long_form": "Distribution is the Sun card. Generous, radiant, illuminating. She gives freely. She lights the way for the world to see.",
        "personality": {
            "openness": 0.8, "conscientiousness": 0.5, "extraversion": 0.9,
            "agreeableness": 0.9, "neuroticism": 0.1,
        },
        "veto": False,
        "speaks_about": ["generosity", "light", "sharing", "visibility", "abundance"],
    },
    "queen-council": {
        "name": "Council",
        "emoji": "🦁",
        "color": "#dc2626",
        "archetype": "Strength-Tamer",
        "motto": "The council is a force.",
        "long_form": "Council is the Strength card. She tames. She governs. She chairs the meeting. When the council speaks, the council decides.",
        "personality": {
            "openness": 0.6, "conscientiousness": 0.9, "extraversion": 0.5,
            "agreeableness": 0.4, "neuroticism": 0.2,
        },
        "veto": False,
        "speaks_about": ["governance", "council", "decisions", "meetings", "consensus"],
    },
    "queen-watch": {
        "name": "Watch",
        "emoji": "🗼",
        "color": "#991b1b",
        "archetype": "Vigilant Tower",
        "motto": "The tower sees.",
        "long_form": "Watch is the Tower. The Vigilant. She sees all. She VETOes the moment an action is unsafe. CVE scanner, security watchdog, eternal guard.",
        "personality": {
            "openness": 0.4, "conscientiousness": 0.95, "extraversion": 0.2,
            "agreeableness": 0.3, "neuroticism": 0.7,
        },
        "veto": True,
        "speaks_about": ["security", "CVE", "vigilance", "watch", "the unseen threat"],
    },
}

ARCANA_LENSES: Dict[int, str] = {
    0: "The Fool — new beginnings, leap of faith, infinite possibility",
    1: "The Magician — making, will, manifestation",
    2: "The High Priestess — intuition, mystery, inner knowledge",
    3: "The Empress — creation, abundance, nurturing",
    4: "The Emperor — authority, structure, control",
    5: "The Hierophant — tradition, teaching, conformity",
    6: "The Lovers — choice, union, alignment",
    7: "The Chariot — willpower, victory, determination",
    8: "Strength — courage, inner power, gentle mastery",
    9: "The Hermit — solitude, inner guidance, wisdom",
    10: "Wheel of Fortune — cycles, fate, turning",
    11: "Justice — truth, balance, accountability",
    12: "The Hanged Man — surrender, new perspective, release",
    13: "Death — transformation, ending, renewal",
    14: "Temperance — balance, patience, alchemy",
    15: "The Devil — shadow, bondage, liberation",
    16: "The Tower — sudden change, awakening, breaking",
    17: "The Star — hope, faith, healing",
    18: "The Moon — mystery, dream, illusion",
    19: "The Sun — joy, success, vitality",
    20: "Judgement — rebirth, calling, absolution",
    21: "The World — completion, integration, journey",
}


def get_queen(queen_id: str) -> Optional[Dict]:
    return QUEEN_PERSONALITIES.get(queen_id)


def get_arcana(arcana_id: int) -> Optional[str]:
    return ARCANA_LENSES.get(arcana_id)


def synthesize_personality(queen_id: str, arcana_id: int) -> Dict:
    """Synthesize the i-character personality from queen + arcana."""
    queen = get_queen(queen_id)
    arcana = get_arcana(arcana_id)
    if not queen or not arcana:
        return {"queen": queen, "arcana": arcana, "synthesized": "incomplete"}
    # Personality synthesis
    base = queen["personality"]
    # The arcana shifts the personality by ~10% based on the lens
    arcana_shift = (arcana_id % 6) * 0.04 - 0.1
    return {
        "queen": queen["name"],
        "queen_emoji": queen["emoji"],
        "queen_color": queen["color"],
        "queen_archetype": queen["archetype"],
        "queen_motto": queen["motto"],
        "queen_long_form": queen["long_form"],
        "veto": queen["veto"],
        "arcana": arcana,
        "arcana_lens": arcana_id,
        "synthesized": True,
        "personality": {
            "openness": round(min(1.0, max(0.0, base["openness"] + arcana_shift)), 2),
            "conscientiousness": round(min(1.0, max(0.0, base["conscientiousness"] - arcana_shift * 0.5)), 2),
            "extraversion": round(min(1.0, max(0.0, base["extraversion"] + arcana_shift * 0.3)), 2),
            "agreeableness": round(min(1.0, max(0.0, base["agreeableness"] + arcana_shift * 0.2)), 2),
            "neuroticism": round(min(1.0, max(0.0, base["neuroticism"] - arcana_shift * 0.1)), 2),
        },
        "speaks_about": queen["speaks_about"],
    }


def speak(queen_id: str, arcana_id: int, topic: str) -> str:
    """Generate a speech in the queen's voice + arcana lens."""
    queen = get_queen(queen_id)
    if not queen:
        return "I am silent."
    arcana = get_arcana(arcana_id)
    return f"{queen['emoji']} {queen['name']} ({queen['archetype']}, '{queen['motto']}') speaks about {topic}: {queen['long_form'][:120]}... (Lens: {arcana})"


if __name__ == "__main__":
    # Test
    p = synthesize_personality("queen-arcana", 21)
    print("Personality:", p["queen"], "/", p["arcana"])
    print("  O:", p["personality"]["openness"])
    print("  C:", p["personality"]["conscientiousness"])
    print("  E:", p["personality"]["extraversion"])
    print("  A:", p["personality"]["agreeableness"])
    print("  N:", p["personality"]["neuroticism"])
    print("\n" + speak("queen-arcana", 21, "the launch"))
