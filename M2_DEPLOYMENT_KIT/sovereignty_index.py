#!/usr/bin/env python3
"""
sovereignty_index.py — Calculate sovereignty index for AI systems.

Usage:
  python3 sovereignty_index.py --data-residency uk --model-origin uk --training-data uk
  python3 sovereignty_index.py --data-residency us --model-origin us --training-data us --format json
"""
import json, sys, argparse

SOVEREIGNTY_FACTORS = {
    "data_residency": {"uk": 1.0, "us": 0.3, "eu": 0.7, "other": 0.1},
    "model_origin": {"uk": 1.0, "us": 0.3, "eu": 0.7, "other": 0.1},
    "training_data": {"uk": 1.0, "us": 0.3, "eu": 0.7, "other": 0.1},
    "inference_location": {"uk": 1.0, "us": 0.3, "eu": 0.7, "other": 0.1},
    "key_management": {"uk": 1.0, "us": 0.3, "eu": 0.7, "other": 0.1},
}

def calculate_index(**kwargs) -> float:
    """Calculate sovereignty index 0-100."""
    total = 0
    count = 0
    for factor, location in kwargs.items():
        if factor in SOVEREIGNTY_FACTORS and location:
            total += SOVEREIGNTY_FACTORS[factor].get(location.lower(), 0.1)
            count += 1
    return round((total / max(count, 1)) * 100, 1)

def main():
    parser = argparse.ArgumentParser(description="Sovereignty Index Calculator")
    parser.add_argument("--data-residency", default="uk")
    parser.add_argument("--model-origin", default="uk")
    parser.add_argument("--training-data", default="uk")
    parser.add_argument("--inference-location", default="uk")
    parser.add_argument("--key-management", default="uk")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    index = calculate_index(
        data_residency=args.data_residency,
        model_origin=args.model_origin,
        training_data=args.training_data,
        inference_location=args.inference_location,
        key_management=args.key_management
    )

    if args.format == "json":
        print(json.dumps({
            "sovereignty_index": index,
            "factors": {
                "data_residency": args.data_residency,
                "model_origin": args.model_origin,
                "training_data": args.training_data,
                "inference_location": args.inference_location,
                "key_management": args.key_management
            }
        }, indent=2))
    else:
        print(f"Sovereignty Index: {index}/100")
        print(f"  Data Residency:    {args.data_residency}")
        print(f"  Model Origin:      {args.model_origin}")
        print(f"  Training Data:     {args.training_data}")
        print(f"  Inference Location: {args.inference_location}")
        print(f"  Key Management:    {args.key_management}")

if __name__ == "__main__":
    main()
