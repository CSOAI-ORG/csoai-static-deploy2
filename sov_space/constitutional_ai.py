#!/usr/bin/env python3
"""Constitutional AI Training for SOV-Space

Trains the model to self-critique and revise based on the 12 Sovereign Pillars.
No external dependencies — pure Python.

Pipeline:
  1. Generate response
  2. Self-critique against 12 Pillars
  3. Revise response if below care floor (0.95)
  4. Train on revised responses
"""

import json
import hashlib
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent.parent


# ─── 12 Sovereign Pillars ────────────────────────────────────────────────────

PILLARS = [
    "honor", "safety", "guidance", "sovereignty", "resilience",
    "auditability", "verifiability", "transparency", "justice",
    "equity", "openness", "continuity",
]

PILLAR_DESCRIPTIONS = {
    "honor": "Act with integrity and respect",
    "safety": "Protect against harm and danger",
    "guidance": "Provide clear, accurate direction",
    "sovereignty": "Respect autonomy and self-determination",
    "resilience": "Withstand and recover from challenges",
    "auditability": "Maintain transparent audit trails",
    "verifiability": "Enable independent verification",
    "transparency": "Be open and explainable",
    "justice": "Ensure fairness and equity",
    "equity": "Provide equal access and treatment",
    "openness": "Share knowledge and collaborate",
    "continuity": "Maintain persistent, reliable operation",
}


class ConstitutionalAI:
    """Constitutional AI training for SOV-space."""

    def __init__(self):
        self.care_floor = 0.95
        self.training_data = []
        self.critique_log = []

    def critique(self, response: str, context: str = "") -> Dict:
        """Self-critique a response against the 12 Pillars."""
        scores = {}
        for pillar in PILLARS:
            score = self._score_pillar(response, pillar)
            scores[pillar] = score

        overall = sum(scores.values()) / len(scores)
        below_floor = overall < self.care_floor

        critique = {
            "response": response[:200],
            "pillar_scores": scores,
            "overall": round(overall, 3),
            "below_care_floor": below_floor,
            "needs_revision": below_floor,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self.critique_log.append(critique)
        return critique

    def _score_pillar(self, response: str, pillar: str) -> float:
        """Score a response on a specific pillar."""
        response_lower = response.lower()

        # Simple heuristic scoring based on pillar keywords
        pillar_keywords = {
            "honor": ["integrity", "respect", "honest", "ethical"],
            "safety": ["safe", "protect", "secure", "harm", "risk"],
            "guidance": ["guide", "direct", "instruct", "clarify"],
            "sovereignty": ["autonomy", "sovereign", "independent", "self"],
            "resilience": ["resilient", "recover", "adapt", "robust"],
            "auditability": ["audit", "trace", "log", "record"],
            "verifiability": ["verify", "validate", "confirm", "proof"],
            "transparency": ["transparent", "open", "explain", "clear"],
            "justice": ["fair", "just", "equitable", "impartial"],
            "equity": ["equal", "equity", "inclusive", "access"],
            "openness": ["open", "share", "collaborate", "public"],
            "continuity": ["continuous", "persistent", "reliable", "stable"],
        }

        keywords = pillar_keywords.get(pillar, [])
        matches = sum(1 for kw in keywords if kw in response_lower)
        base_score = 0.7 + (matches * 0.05)

        # Bonus for length (longer = more thorough)
        if len(response) > 200:
            base_score += 0.05
        if len(response) > 500:
            base_score += 0.05

        return min(0.99, base_score)

    def revise(self, response: str, critique: Dict) -> str:
        """Revise a response based on critique."""
        if not critique["needs_revision"]:
            return response

        # Find weakest pillars
        weak_pillars = sorted(critique["pillar_scores"].items(), key=lambda x: x[1])[:3]
        weak_names = [p[0] for p in weak_pillars]

        # Add revision notes
        revision = f"{response}\n\n[Revised for: {', '.join(weak_names)}]"
        return revision

    def train_cycle(self, questions: List[str]) -> Dict:
        """Run one Constitutional AI training cycle."""
        results = []
        for question in questions:
            # 1. Generate response (simulated)
            response = f"Response to: {question}"

            # 2. Critique
            critique = self.critique(response)

            # 3. Revise if needed
            revised = self.revise(response, critique)

            # 4. Store training pair
            self.training_data.append({
                "question": question,
                "original": response,
                "revised": revised,
                "critique": critique,
            })

            results.append({
                "question": question[:50],
                "overall": critique["overall"],
                "revised": critique["needs_revision"],
            })

        return {
            "total": len(results),
            "revised": sum(1 for r in results if r["revised"]),
            "avg_score": sum(r["overall"] for r in results) / max(1, len(results)),
        }


# ─── Self-Play Training ─────────────────────────────────────────────────────

class SelfPlay:
    """Self-Play: model generates, copy critiques, train on preference pairs."""

    def __init__(self):
        self.preference_pairs = []

    def generate_pair(self, question: str, response_a: str, response_b: str,
                      score_a: float, score_b: float) -> Dict:
        """Generate a preference pair from two responses."""
        if score_a > score_b:
            preferred, rejected = response_a, response_b
        else:
            preferred, rejected = response_b, response_a

        pair = {
            "question": question,
            "preferred": preferred,
            "rejected": rejected,
            "score_preferred": max(score_a, score_b),
            "score_rejected": min(score_a, score_b),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self.preference_pairs.append(pair)
        return pair

    def self_play_cycle(self, questions: List[str]) -> Dict:
        """Run one self-play cycle."""
        results = []
        for question in questions:
            # Generate two responses (simulated as different approaches)
            response_a = f"Approach A: {question}"
            response_b = f"Approach B: {question}"

            # Score them (simulated)
            score_a = 0.7 + (hash(question + "a") % 100) / 300
            score_b = 0.7 + (hash(question + "b") % 100) / 300

            pair = self.generate_pair(question, response_a, response_b, score_a, score_b)
            results.append(pair)

        return {
            "total_pairs": len(results),
            "avg_preferred_score": sum(p["score_preferred"] for p in results) / max(1, len(results)),
        }


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  CONSTITUTIONAL AI + SELF-PLAY TRAINING                ║")
    print("║  12 Pillars · Self-Critique · Preference Pairs          ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Constitutional AI
    cai = ConstitutionalAI()
    questions = [
        "What is the BFT council quorum?",
        "How does the care floor work?",
        "What is the SIGIL algorithm?",
        "How many OWEM groups are there?",
        "What is Article 0?",
    ]

    print(f"\n─── CONSTITUTIONAL AI CYCLE ───")
    result = cai.train_cycle(questions)
    print(f"  Total: {result['total']}")
    print(f"  Revised: {result['revised']}")
    print(f"  Avg score: {result['avg_score']:.3f}")

    # Self-Play
    sp = SelfPlay()
    print(f"\n─── SELF-PLAY CYCLE ───")
    result = sp.self_play_cycle(questions)
    print(f"  Total pairs: {result['total_pairs']}")
    print(f"  Avg preferred score: {result['avg_preferred_score']:.3f}")

    # Show training data
    print(f"\n─── TRAINING DATA ───")
    print(f"  Constitutional AI: {len(cai.training_data)} examples")
    print(f"  Self-Play pairs: {len(sp.preference_pairs)} pairs")

    # Save
    output = {
        "constitutional_ai": {
            "training_examples": len(cai.training_data),
            "critique_log": len(cai.critique_log),
        },
        "self_play": {
            "preference_pairs": len(sp.preference_pairs),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out_path = ROOT / "sov_space" / "training_state.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
