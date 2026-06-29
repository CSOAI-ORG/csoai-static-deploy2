#!/usr/bin/env python3
"""
PHASE 230: Cold outreach fire script
====================================
Reads cold_outreach_2026_06_29.json and sends 10 emails.
If no SMTP creds, saves to /tmp/emails_to_send/.
"""
import os, json, smtplib, ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

COLD_FILE = Path("/Users/nicholas/clawd/csoai.org/distribution/cold_outreach_2026_06_29.json")
OUT_DIR = Path("/tmp/emails_to_send")
SOV3_MCP = "http://localhost:3101/mcp"


def emit_sigil(line):
    """Emit SIGIL to live chain."""
    import urllib.request
    payload = json.dumps({"jsonrpc":"2.0","id":"co","method":"tools/call",
                          "params":{"name":"sov_sigil_emit","arguments":{"line":line,"op":"C"}}}).encode()
    req = urllib.request.Request(SOV3_MCP, data=payload,
                                  headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except: return None


def send_email_via_smtp(to_email, subject, body):
    """Send via SMTP if creds available."""
    if not SMTP_USER or not SMTP_PASS:
        return None
    msg = MIMEMultipart()
    msg["From"] = f"CSOAI Ltd <{SMTP_USER}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"      SMTP error: {e}")
        return False


def main():
    print(f"\n{'='*70}")
    print(f"📧 SOV3 COLD OUTREACH FIRE — {datetime.now().isoformat()[:19]} BST")
    print(f"   {SMTP_SERVER}:{SMTP_PORT} user={SMTP_USER or 'NOT CONFIGURED'}")
    print(f"{'='*70}\n")

    if not COLD_FILE.exists():
        print(f"❌ Cold outreach file missing: {COLD_FILE}")
        return 1

    with COLD_FILE.open() as f:
        data = json.load(f)

    prospects = data.get("prospects", [])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    sent_count = 0
    queued_count = 0

    for p in prospects:
        name = p["prospect"]
        email_body = p["email"]
        # Extract subject (first line of email)
        subject = "SOV3 Sovereign AI"
        for line in email_body.split("\n"):
            if line.startswith("Subject:"):
                subject = line.replace("Subject:", "").strip()
                break

        # Try SMTP first
        to_email = f"{name.lower().replace(' ', '')}@{name.lower().split()[0][:5]}.com"
        smtp_ok = send_email_via_smtp(to_email, subject, email_body)

        if smtp_ok:
            print(f"  ✅ {name}: SENT to {to_email}")
            sent_count += 1
            sigil = f"C|outreach|SENT_{name}|T{datetime.now().isoformat()[:19]}_BST. email_sent_sovereign_AI. empire_10/10."
            emit_sigil(sigil)
        else:
            # Queue for manual send
            email_file = OUT_DIR / f"{name.lower().replace(' ', '_')}.txt"
            email_file.write_text(f"To: {name} <ceo@{name.lower().split()[0]}.com>\nSubject: {subject}\n\n{email_body}")
            print(f"  ⏳ {name}: QUEUED → {email_file}")
            queued_count += 1

    print(f"\n{'='*70}")
    print(f"📊 RESULT: {sent_count} sent, {queued_count} queued")
    if queued_count > 0:
        print(f"   Manual send queue: {OUT_DIR}/")
        print(f"   Each file has full email content ready to paste into Gmail/Outlook")
    print(f"{'='*70}\n")
    return 0


if __name__ == "__main__":
    exit(main())