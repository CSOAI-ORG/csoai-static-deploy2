#!/usr/bin/env python3
"""send_ietf_scitt.py — one-command dispatcher for the IETF SCITT engagement post.

Usage:
  python3 send_ietf_scitt.py            # dry-run: prints the rendered email + SMTP status, does NOT send
  python3 send_ietf_scitt.py --send     # the irreversible action

Sends from the configured SMTP account (env: SMTP_HOST/PORT/USER/PASSWORD/FROM_EMAIL)
and FROM_EMAIL must be nicholas@csoai.org. If SMTP is not configured it exits non-zero
with an honest message — it NEVER fabricates a send.
"""
from __future__ import annotations

import os
import smtplib
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

HERE = Path(__file__).resolve().parent
EML = HERE / "outreach" / "IETF_SCITT_ENGAGEMENT_2026-08-26.eml"
TO = "scitt@ietf.org"
CC = ["agent2agent@ietf.org", "agentproto@ietf.org"]
FROM = os.environ.get("FROM_EMAIL", "nicholas@csoai.org")


def _env_hint() -> dict:
    return {
        "SMTP_HOST": os.environ.get("SMTP_HOST", ""),
        "SMTP_PORT": os.environ.get("SMTP_PORT", "587"),
        "SMTP_USER": "set" if os.environ.get("SMTP_USER") else "",
        "SMTP_PASSWORD": "set" if os.environ.get("SMTP_PASSWORD") else "",
        "FROM_EMAIL": FROM,
    }


def _smtp_ready() -> bool:
    return bool(os.environ.get("SMTP_HOST") and os.environ.get("SMTP_USER")
                and os.environ.get("SMTP_PASSWORD"))


def main() -> int:
    eml = EML.read_text(encoding="utf-8")
    subject = next((l.split(":", 1)[1].strip() for l in eml.splitlines()
                    if l.lower().startswith("subject:")), "Deployed SCITT-compatible measurement estate")
    body = "\n".join(l for l in eml.splitlines()
                     if not l.lower().startswith(("from:", "to:", "cc:", "subject:"))).strip()

    print("=" * 70)
    print("IETF SCITT engagement post")
    print("=" * 70)
    print(f"  To:  {TO}")
    print(f"  Cc:  {', '.join(CC)}")
    print(f"  Sub: {subject}")
    print(f"  EML: {EML}")
    print("=" * 70)
    print("SMTP status:", {k: ("SET" if v else "MISSING") for k, v in _env_hint().items()})
    print("=" * 70)
    print(body)
    print("=" * 70)

    if not _smtp_ready():
        print("\n[BLOCKED] SMTP is not configured (need SMTP_HOST, SMTP_USER, SMTP_PASSWORD).")
        print("  Set them for nicholas@csoai.org (e.g. Zoho/Postmark/Resend), then re-run with --send.")
        print("  Nothing was sent. This tool never fabricates a send.")
        return 2

    if "--send" not in sys.argv:
        print("\n[DRY-RUN] No --send flag — nothing transmitted. Run with --send to fire.")
        return 0

    msg = EmailMessage()
    msg["From"] = FROM
    msg["To"] = TO
    msg["Cc"] = ", ".join(CC)
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="csoai.org")
    msg.set_content(body)

    try:
        with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", "587")),
                          timeout=30) as s:
            s.ehlo()
            s.starttls()
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            s.send_message(msg)
        print("\n[SENT] IETF SCITT engagement post dispatched.")
        return 0
    except Exception as e:
        print(f"\n[FAILED] {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
