#!/usr/bin/env python3
"""send_press_resend.py — Send 1,076 emails via Resend API.

Prerequisites:
1. RESEND_API_KEY exported (from ~/.meok/meok-api/config.yaml)
2. Press list at iCloud SOV3-Launch/PRESS_LIST_1076.csv
3. Email body at PASSPORT_LAUNCH_13JUN/06-press-list-email.md

Usage:
  export RESEND_API_KEY=re_xxx
  python3 send_press_resend.py [--dry-run] [--limit 50]

Rate limit: Resend allows 2 req/sec on free tier, 100/sec on Pro.
1,076 emails at 100/sec = 11 seconds. With 2/sec = 9 minutes.
"""

import os, csv, time, json, sys, argparse
import requests

PRESS_CSV = "/Users/nicholas/Library/Mobile Documents/com~apple~CloudDocs/SOV3-Launch/PRESS_LIST_1076.csv"
BODY_FILE = "/Users/nicholas/clawd/PASSPORT_LAUNCH_13JUN/06-press-list-email.md"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=999999)
    args = parser.parse_args()

    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: RESEND_API_KEY not set. Use --dry-run or export it.")
        sys.exit(1)

    # Load contacts
    contacts = []
    with open(PRESS_CSV, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("email", "").strip()
            if not email or "@" not in email: continue
            first = (row.get("name_org", "").split()[0] if row.get("name_org") else "there")
            contacts.append({"email": email, "first": first})
    contacts = contacts[:args.limit]
    print(f"Loaded {len(contacts)} contacts")

    # Load body
    with open(BODY_FILE) as f:
        body_template = f.read()

    subject = "Open source — the missing A2A primitive, 49 days before the EU cliff"

    sent = 0
    failed = 0
    for c in contacts:
        body = body_template.replace("{first_name}", c["first"])

        if args.dry_run:
            print(f"  [DRY] {c['email']} ({c['first']})")
            sent += 1
            continue

        try:
            r = requests.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "from": "Nick Templeman <press@meok.ai>",
                    "to": [c["email"]],
                    "subject": subject,
                    "text": body,
                    "reply_to": "press@meok.ai",
                },
                timeout=10
            )
            if r.status_code in (200, 201):
                sent += 1
                if sent % 100 == 0:
                    print(f"  Sent: {sent} / Failed: {failed}")
            else:
                failed += 1
                print(f"  FAIL {c['email']}: {r.status_code} {r.text[:100]}")
        except Exception as e:
            failed += 1
            print(f"  EXCEPTION {c['email']}: {e}")

        time.sleep(0.5)  # 2 req/sec — Resend free tier limit

    print(f"\n=== DONE: sent={sent} failed={failed} ===")

if __name__ == "__main__":
    main()
