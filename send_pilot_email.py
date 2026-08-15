#!/usr/bin/env python3
"""send_pilot_email.py — the gated one-command dispatcher for pilot outreach. (Move 121/122)

Transmit is EXPLICIT, never automatic:
  python3 send_pilot_email.py --to someone@example.com --eml outreach/P1_STAGED_EMAIL_2026-08-09.eml   # dry-run (prints, does not send)
  python3 send_pilot_email.py --to ... --eml ... --send                                              # THE irreversible action

Sends from the configured SMTP account (env: SMTP_HOST/PORT/USER/PASSWORD/FROM_EMAIL).
On a real --send success it appends a hash-chained dispatch record (dispatch_log.py)
and advances the funnel tracker to 'sent' — so the audit trail only ever contains
REAL sends. Requires smtplib (stdlib).
"""
from __future__ import annotations

import argparse
import os
import smtplib
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _env(name: str, required: bool = True) -> str:
    v = os.environ.get(name, "")
    if required and not v:
        sys.exit(f"missing env {name} — cannot send")
    return v


def build_message(to: str, eml: Path) -> EmailMessage:
    raw = eml.read_text(encoding="utf-8", errors="replace")
    subject = next((l.split(":", 1)[1].strip() for l in raw.splitlines()
                    if l.lower().startswith("subject:")), "CSOAI pilot — measured evidence")
    body = "\n".join(l for l in raw.splitlines()
                     if not l.lower().startswith(("from:", "to:", "subject:"))).strip()
    msg = EmailMessage()
    msg["From"] = _env("FROM_EMAIL")
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="csoai.org")
    msg.set_content(body)
    return msg


def transmit(to: str, eml: Path) -> tuple[bool, str]:
    msg = build_message(to, eml)
    host, port = _env("SMTP_HOST"), int(_env("SMTP_PORT"))
    user, pwd = _env("SMTP_USER"), _env("SMTP_PASSWORD")
    try:
        with smtplib.SMTP(host, port, timeout=60) as s:
            s.ehlo()
            if s.has_extn("starttls"):
                s.starttls()
                s.ehlo()
            s.login(user, pwd)
            s.send_message(msg)
        return True, f"sent to {to}"
    except Exception as e:  # noqa: BLE001
        return False, f"send failed: {e}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, help="verified recipient inbox")
    ap.add_argument("--eml", default=str(HERE / "outreach" / "P1_STAGED_EMAIL_2026-08-09.eml"))
    ap.add_argument("--send", action="store_true", help="irreversible: actually transmit")
    args = ap.parse_args()

    eml = Path(args.eml)
    if "--send" not in sys.argv:
        print("DRY-RUN (no --send): would transmit the following —")
        print(f"  to: {args.to}")
        msg = build_message(args.to, eml)
        print(f"  subject: {msg['Subject']}")
        print(f"  from: {msg['From']}")
        print(f"  body: {msg.get_content()[:200]}…")
        print("Re-run with --send to actually dispatch.")
        return 0

    ok, detail = transmit(args.to, eml)
    if ok:
        sys.path.insert(0, str(HERE))
        from dispatch_log import log_dispatch  # noqa: E402
        from funnel_tools import advance  # noqa: E402
        log_dispatch("P1", "email", "financial pilot pack", target=args.to)
        advance("P1", "sent")
        print(f"✅ {detail} — dispatch recorded (hash-chained) + tracker → sent")
        return 0
    print(f"❌ {detail}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())