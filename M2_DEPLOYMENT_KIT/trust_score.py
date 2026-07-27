#!/usr/bin/env python3
"""
trust_score.py — Calculate trust score for AI deployments.

Usage:
  python3 trust_score.py --care-floor 0.95 --bft-quorum 23 --sigil-signed true
"""
import json, sys, argparse

def calculate_trust(care_floor: float, bft_quorum: int, sigil_signed: bool,
                    human_oversight: bool = True, documentation: bool = True) -> float:
    score = 0.0
    if care_floor >= 0.95: score += 30
    elif care_floor >= 0.90: score += 20
    if bft_quorum >= 23: score += 25
    elif bft_quorum >= 17: score += 15
    if sigil_signed: score += 20
    if human_oversight: score += 15
    if documentation: score += 10
    return min(score, 100)

def main():
    parser = argparse.ArgumentParser(description="Trust Score Calculator")
    parser.add_argument("--care-floor", type=float, default=0.95)
    parser.add_argument("--bft-quorum", type=int, default=23)
    parser.add_argument("--sigil-signed", type=bool, default=True)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    score = calculate_trust(args.care_floor, args.bft_quorum, args.sigil_signed)

    if args.format == "json":
        print(json.dumps({"trust_score": score}, indent=2))
    else:
        print(f"Trust Score: {score}/100")

if __name__ == "__main__":
    main()
