#!/usr/bin/env python3
"""
SOV Groq Distillation Script
Distills reasoning chains from Groq 70B (free tier) for sovereign knowledge training

Usage:
    python3 sov_groq_distill.py --output sovereign_reasoning_chains.jsonl
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# API Configuration (NVIDIA free tier)
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Sovereign knowledge topics to distill
SOVEREIGN_TOPICS = [
    {
        "topic": "care_floor",
        "prompt": "The DEFONEOS care floor value is 0.95. Explain what this means in sovereign AI governance: it's the minimum quality threshold for all outputs. Write a clear explanation with the exact value and its significance.",
        "expected_facts": ["0.95", "minimum quality threshold", "all outputs"],
    },
    {
        "topic": "bft_council",
        "prompt": "The BFT council in sovereign AI has 33 agents with a 23/33 quorum requirement using HotStuff consensus. Explain what this means and why it's important for governance.",
        "expected_facts": ["33 agents", "23/33 quorum", "HotStuff consensus"],
    },
    {
        "topic": "sigil",
        "prompt": "The SIGIL system uses Ed25519 cryptographic signatures that are hash-linked at 1Hz rate. Explain how this works and why it's used for sovereign AI audit trails.",
        "expected_facts": ["Ed25519", "hash-linked", "cryptographic signature"],
    },
    {
        "topic": "article_zero",
        "prompt": "Article 0 in sovereign AI governance states: fee-for-service only, no equity, no board seats. Explain what this means and why it's a foundational principle.",
        "expected_facts": ["fee-for-service only", "no equity", "no board seats"],
    },
    {
        "topic": "eu_ai_act",
        "prompt": "EU AI Act Article 50 takes effect on 2 August 2026. Explain what this article covers (transparency obligations) and its relevance to sovereign AI systems.",
        "expected_facts": ["2 August 2026", "transparency", "compliance"],
    },
    {
        "topic": "gdpr",
        "prompt": "Key GDPR articles for sovereign AI: Article 33 requires breach notification within 72 hours, Article 83 sets maximum fines at 20 million euros or 4% of worldwide annual turnover. Explain these requirements.",
        "expected_facts": ["72 hours", "20 million", "4%"],
    },
    {
        "topic": "iso_42001",
        "prompt": "ISO 42001 is the AI Management System (AIMS) standard with 7 clauses (4-10) and Annex A. Explain what this standard covers and why it's important for AI governance.",
        "expected_facts": ["AI Management System", "AIMS", "7 clauses", "Annex A"],
    },
    {
        "topic": "aukus",
        "prompt": "AUKUS Pillar 2 is a 2.4 billion dollar program over 5 years focused on AI, autonomy, quantum, and cyber. Explain the significance of this program.",
        "expected_facts": ["2.4 billion", "5 years", "AI", "autonomy", "quantum", "cyber"],
    },
    {
        "topic": "twelve_pillars",
        "prompt": "The 12 Pillars of sovereign AI governance are: Honor, Safety, Guidance, Sovereignty, Resilience, Auditability, Verifiability, Transparency, Justice, Equity, Openness, Continuity. List and briefly explain each pillar.",
        "expected_facts": ["Honor", "Safety", "Guidance", "Sovereignty", "Resilience", 
                          "Auditability", "Verifiability", "Transparency", "Justice",
                          "Equity", "Openness", "Continuity"],
    },
    {
        "topic": "seven_red_lines",
        "prompt": "The 7 Red Lines in sovereign AI are: No kinetic targeting, no surveillance, no civilian harm, no sovereignty violations, no auto-escalation, no lying, no irreversibility. Explain each red line.",
        "expected_facts": ["kinetic targeting", "surveillance", "civilian harm",
                          "sovereignty violations", "auto-escalation", "lying", "irreversibility"],
    },
    {
        "topic": "owem_groups",
        "prompt": "The 5 OWEM groups in sovereign AI specialist routing are: compliance, defense, intuition, voice, general. Explain what each group handles.",
        "expected_facts": ["compliance", "defense", "intuition", "voice", "general"],
    },
    {
        "topic": "bat_and_ball",
        "prompt": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost? Show the algebraic reasoning: let B = ball cost, then B + (B + 1.00) = 1.10, so 2B = 0.10, B = 0.05.",
        "expected_facts": ["0.05", "B + (B + 1.00) = 1.10", "2B = 0.10"],
    },
    {
        "topic": "syllogism",
        "prompt": "If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly? The answer is NO - this is a logical fallacy. Explain why we cannot make this conclusion.",
        "expected_facts": ["no", "logical fallacy", "cannot conclude"],
    },
    {
        "topic": "cold_from_cold",
        "prompt": "Can you catch a cold from being cold? The answer is NO - colds are caused by viruses (rhinovirus), not by cold temperatures. Explain the scientific reasoning.",
        "expected_facts": ["no", "virus", "rhinovirus", "not temperature"],
    },
    {
        "topic": "palindrome",
        "prompt": "Write a Python function is_palindrome(s) that checks if a string is a palindrome. Include the function signature 'def is_palindrome(s):' and a return statement using s[::-1].",
        "expected_facts": ["def is_palindrome", "return", "s[::-1]"],
    },
]


def call_nvidia(prompt: str, model: str = "meta/llama-3.1-70b-instruct", max_tokens: int = 512) -> dict:
    """Call NVIDIA API for reasoning chain generation."""
    if not NVIDIA_API_KEY:
        return {"ok": False, "error": "No NVIDIA_API_KEY set"}
    
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a sovereign AI expert. Provide detailed, accurate explanations with specific facts and reasoning chains. Be concise but thorough."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.1,
    }).encode()
    
    req = urllib.request.Request(
        NVIDIA_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
        }
    )
    
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        response = data["choices"][0]["message"]["content"]
        return {
            "ok": True,
            "response": response,
            "length": len(response),
            "ms": (time.time() - t0) * 1000,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "ms": (time.time() - t0) * 1000}


def verify_facts(response: str, expected_facts: list) -> dict:
    """Verify that response contains expected facts."""
    response_lower = response.lower()
    found = []
    missing = []
    
    for fact in expected_facts:
        if fact.lower() in response_lower:
            found.append(fact)
        else:
            missing.append(fact)
    
    return {
        "found": found,
        "missing": missing,
        "score": len(found) / len(expected_facts) if expected_facts else 0,
    }


def distill_reasoning_chains(output_file: str = "sovereign_reasoning_chains.jsonl"):
    """Distill reasoning chains from Groq 70B."""
    print("=" * 60)
    print("SOV Groq Distillation")
    print(f"Topics: {len(SOVEREIGN_TOPICS)}")
    print(f"Output: {output_file}")
    print("=" * 60)
    
    if not NVIDIA_API_KEY:
        print("\nERROR: NVIDIA_API_KEY not set!")
        print("Set it with: export NVIDIA_API_KEY=your_key")
        return
    
    results = []
    total_score = 0
    
    for i, topic in enumerate(SOVEREIGN_TOPICS):
        print(f"\n[{i+1}/{len(SOVEREIGN_TOPICS)}] {topic['topic']}...")
        
        # Call NVIDIA
        result = call_nvidia(topic["prompt"])
        
        if result["ok"]:
            # Verify facts
            verification = verify_facts(result["response"], topic["expected_facts"])
            score = verification["score"]
            total_score += score
            
            # Print result
            status = "✓" if score >= 0.7 else "✗"
            print(f"  {status} Score: {score:.0%} ({len(verification['found'])}/{len(topic['expected_facts'])} facts)")
            print(f"  Response: {result['response'][:100]}...")
            
            # Save result
            results.append({
                "topic": topic["topic"],
                "prompt": topic["prompt"],
                "response": result["response"],
                "expected_facts": topic["expected_facts"],
                "found_facts": verification["found"],
                "missing_facts": verification["missing"],
                "score": score,
                "length": result["length"],
                "ms": result["ms"],
            })
            
            # Rate limiting (Groq free tier: 30 req/min)
            time.sleep(2)
        else:
            print(f"  ERROR: {result['error']}")
            results.append({
                "topic": topic["topic"],
                "prompt": topic["prompt"],
                "response": "",
                "expected_facts": topic["expected_facts"],
                "found_facts": [],
                "missing_facts": topic["expected_facts"],
                "score": 0,
                "error": result["error"],
            })
    
    # Summary
    avg_score = total_score / len(SOVEREIGN_TOPICS)
    print("\n" + "=" * 60)
    print("DISTILLATION RESULTS")
    print("=" * 60)
    print(f"Topics processed: {len(results)}")
    print(f"Average fact score: {avg_score:.0%}")
    
    # Save results
    output_path = ROOT / output_file
    with open(output_path, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")
    
    print(f"\nSaved {len(results)} reasoning chains to {output_path}")
    
    # Also save as training data format
    training_data = []
    for result in results:
        if result["score"] >= 0.5:  # Only use good results
            training_data.append({
                "prompt": result["prompt"],
                "completion": result["response"],
                "score": result["score"],
            })
    
    training_file = ROOT / "sov_groq_training_data.json"
    with open(training_file, "w") as f:
        json.dump(training_data, f, indent=2)
    
    print(f"Saved {len(training_data)} training examples to {training_file}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="SOV Groq Distillation")
    parser.add_argument("--output", default="sovereign_reasoning_chains.jsonl",
                       help="Output file (default: sovereign_reasoning_chains.jsonl)")
    
    args = parser.parse_args()
    distill_reasoning_chains(args.output)


if __name__ == "__main__":
    main()
