#!/usr/bin/env python3
"""
charter_amender.py — Amend DEFONEOS charter articles.

Usage:
  python3 charter_amender.py --article 0 --action status
  python3 charter_amender.py --article 1 --action verify
"""
import json, sys, argparse, hashlib

CHARTER_ARTICLES = {
    0: {"name": "Fee-for-Service Only", "status": "binding", "text": "No equity, no board seats, no success fees"},
    1: {"name": "Defence of the Realm", "status": "binding", "text": "Defence of the realm, not offence against it"},
    2: {"name": "Data Sovereignty", "status": "binding", "text": "Zero bytes leave UK jurisdiction without BFT approval"},
    3: {"name": "Human Oversight", "status": "binding", "text": "Human-in-the-loop for all consequential decisions"},
    4: {"name": "Transparency", "status": "binding", "text": "All reasoning traces SIGIL-recorded and auditable"},
    5: {"name": "Proportionality", "status": "binding", "text": "Response proportionate to threat level"},
    6: {"name": "Red Lines", "status": "binding", "text": "7 immutable red lines, never bypassed"},
    7: {"name": "Accountability", "status": "binding", "text": "Named human accountability for every decision"},
}

def main():
    parser = argparse.ArgumentParser(description="Charter Amender")
    parser.add_argument("--article", type=int, required=True)
    parser.add_argument("--action", choices=["status", "verify", "text"], default="status")
    args = parser.parse_args()

    article = CHARTER_ARTICLES.get(args.article)
    if not article:
        print(f"Article {args.article} not found")
        sys.exit(1)

    if args.action == "status":
        print(f"Article {args.article}: {article['name']} — {article['status']}")
    elif args.action == "verify":
        h = hashlib.sha256(article["text"].encode()).hexdigest()[:16]
        print(f"Article {args.article} hash: {h}")
    elif args.action == "text":
        print(f"Article {args.article}: {article['text']}")

if __name__ == "__main__":
    main()
