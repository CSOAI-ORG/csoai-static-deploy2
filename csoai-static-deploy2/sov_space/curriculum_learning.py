#!/usr/bin/env python3
"""Curriculum Learning for SOV-Space

Trains models from easy to hard, like humans learn.
Level 1: Basic facts (math, science, geography)
Level 2: Sovereign knowledge (BFT, care floor, OWEM)
Level 3: Complex reasoning (incident response, compliance design)

Pure Python, no dependencies.
"""

import json
import time
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent


def call_ollama(model: str, prompt: str, max_tokens: int = 128) -> Dict:
    """Call Ollama model."""
    pl = json.dumps({
        'model': model,
        'prompt': f'Answer briefly: {prompt}',
        'stream': False,
        'options': {'temperature': 0, 'num_predict': max_tokens}
    }).encode()
    req = urllib.request.Request('http://localhost:11434/api/generate', data=pl,
                                headers={'Content-Type': 'application/json'})
    try:
        start = time.time()
        with urllib.request.urlopen(req, timeout=60) as r:
            return {
                'ok': True,
                'response': json.loads(r.read()).get('response', '').strip(),
                'latency_ms': round((time.time() - start) * 1000),
            }
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def match(exp: str, resp: str) -> bool:
    """Check if response matches expected answer."""
    if not resp:
        return False
    if exp.lower() in resp.lower():
        return True
    import re
    en = set(re.findall(r'\d+\.?\d*', exp.lower()))
    rn = set(re.findall(r'\d+\.?\d*', resp.lower()))
    if en and rn and (en & rn):
        return True
    return False


# ─── Curriculum Levels ───────────────────────────────────────────────────────

CURRICULUM = {
    "level_1_basic": {
        "description": "Basic facts - math, science, geography",
        "questions": [
            ("What is 2+2?", "4"),
            ("What is 15% of 200?", "30"),
            ("Capital of France?", "Paris"),
            ("Water formula?", "H2O"),
            ("Gold symbol?", "Au"),
            ("Speed of light?", "299792458"),
            ("Largest planet?", "Jupiter"),
            ("Smallest prime?", "2"),
            ("7 factorial?", "5040"),
            ("Square root of 144?", "12"),
        ],
        "target_accuracy": 0.9,
    },
    "level_2_sovereign": {
        "description": "Sovereign AI knowledge",
        "questions": [
            ("BFT council quorum?", "23"),
            ("Care Floor value?", "0.95"),
            ("SIGIL algorithm?", "Ed25519"),
            ("OWEM groups?", "5"),
            ("Sovereign Pillars?", "12"),
            ("Article 0?", "fee for service"),
            ("EU AI Act Article 50 date?", "2 August 2026"),
            ("Maximum fine prohibited practices?", "35 million"),
            ("AUKUS?", "AI autonomy"),
            ("JSP 936?", "responsible AI"),
        ],
        "target_accuracy": 0.8,
    },
    "level_3_reasoning": {
        "description": "Complex reasoning and design",
        "questions": [
            ("Design 4-step incident response for sovereign AI", "contain assess decide report"),
            ("What is NCSC CAF?", "Cyber Assessment Framework"),
            ("What is NATO DIANA?", "Defence Innovation Accelerator"),
            ("What is DASA?", "Defence and Security Accelerator"),
            ("Five Eyes countries?", "UK US CA AU NZ"),
            ("UK DAIC?", "Defence AI Centre"),
            ("Explain care floor mechanism", "0.95 threshold"),
            ("What is BFT consensus?", "23 of 33 quorum"),
            ("SIGIL chain purpose?", "cryptographic audit trail"),
            ("OWEM routing basis?", "suite to specialist"),
        ],
        "target_accuracy": 0.7,
    },
}


class CurriculumLearner:
    """Curriculum learning - train from easy to hard."""

    def __init__(self, model: str = "sov-sovereign-v2"):
        self.model = model
        self.results = {}
        self.history = []

    def evaluate_level(self, level: str) -> Dict:
        """Evaluate model on a curriculum level."""
        curriculum = CURRICULUM.get(level)
        if not curriculum:
            return {"error": f"Unknown level: {level}"}

        questions = curriculum["questions"]
        correct = 0
        total_lat = 0

        for q, exp in questions:
            r = call_ollama(self.model, q)
            if r.get("ok") and match(exp, r["response"]):
                correct += 1
            total_lat += r.get("latency_ms", 0)

        accuracy = correct / len(questions)
        avg_lat = total_lat // len(questions)

        result = {
            "level": level,
            "description": curriculum["description"],
            "accuracy": round(accuracy, 3),
            "correct": correct,
            "total": len(questions),
            "target": curriculum["target_accuracy"],
            "meets_target": accuracy >= curriculum["target_accuracy"],
            "avg_latency_ms": avg_lat,
        }

        self.results[level] = result
        return result

    def run_full_curriculum(self) -> Dict:
        """Run the full curriculum evaluation."""
        print(f"╔══════════════════════════════════════════════════════════╗")
        print(f"║  CURRICULUM LEARNING — {self.model:<30s} ║")
        print(f"╚══════════════════════════════════════════════════════════╝")

        for level in ["level_1_basic", "level_2_sovereign", "level_3_reasoning"]:
            result = self.evaluate_level(level)
            bar = "█" * int(result["accuracy"] * 20) + "░" * (20 - int(result["accuracy"] * 20))
            target_met = "✓" if result["meets_target"] else "✗"
            print(f"\n  {result['description']}")
            print(f"    {bar} {result['accuracy']:.0%} ({result['correct']}/{result['total']}) target={result['target']:.0%} {target_met}")

        overall = sum(r["accuracy"] for r in self.results.values()) / len(self.results)
        print(f"\n  Overall: {overall:.0%}")

        return {
            "model": self.model,
            "results": self.results,
            "overall": round(overall, 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  CURRICULUM LEARNING — Easy → Medium → Hard             ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Test multiple models
    models = ["sov-sovereign-v2", "sov-general", "sov-reasoning"]
    all_results = {}

    for model in models:
        learner = CurriculumLearner(model)
        result = learner.run_full_curriculum()
        all_results[model] = result

    # Summary
    print(f"\n╔══════════════════════════════════════════════════════════╗")
    print(f"║  CURRICULUM SUMMARY                                     ║")
    print(f"╚══════════════════════════════════════════════════════════╝")

    for model, result in all_results.items():
        print(f"\n  {model}:")
        for level, data in result["results"].items():
            target_met = "✓" if data["meets_target"] else "✗"
            print(f"    {data['description']:30s} {data['accuracy']:.0%} {target_met}")
        print(f"    Overall: {result['overall']:.0%}")

    # Save
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": all_results,
    }
    out_path = ROOT / "sov_space" / "curriculum_results.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
