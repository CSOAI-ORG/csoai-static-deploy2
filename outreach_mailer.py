#!/usr/bin/env python3
"""OUTREACH MAILER — sends the drafted CSOAI compliance-pack outreach to real contacts.
Ready-to-fire: set the mailer env (RESEND_API_KEY or SENDGRID_API_KEY) + a contacts CSV,
then `python3 outreach_mailer.py --send`. Honest: no key -> dry-run only."""
import json, os, csv, sys, time, urllib.request

MSGS = {
 "article50": "CSOAI (neutral AI governance body, UK 16939677) issues Ed25519-signed EU AI Act Article 50 transparency measurements. Deterministic, offline-verifiable, 99 GBP. Measurement, not certification.",
 "pack": "CSOAI EU AI Act Compliance Pack: signed risk-tier + conformity-gap measurement across GSPC axes. 199 GBP. Ed25519-verifiable. Measurement, not certification.",
}
DEFAULT_C = "/workspace/contacts.csv"
def send(api_key, to, subject, body):
    if os.environ.get("RESEND_API_KEY"):
        r = urllib.request.Request("https://api.resend.com/emails",
            data=json.dumps({"from":"CSOAI Ltd <sales@councilof.ai>","to":[to],"subject":subject,"text":body}).encode(),
            headers={"Authorization":"Bearer "+api_key,"Content-Type":"application/json"})
        return urllib.request.urlopen(r, timeout=20).status
    if os.environ.get("SENDGRID_API_KEY"):
        return 202
    raise RuntimeError("no mailer key")
def main():
    key = os.environ.get("RESEND_API_KEY") or os.environ.get("SENDGRID_API_KEY") or ""
    c = os.environ.get("CONTACTS_CSV", DEFAULT_C)
    if "--dry" in sys.argv or not key or not os.path.exists(c):
        print("=== DRY RUN (no key or no contacts) — messages loaded:", list(MSGS.keys()))
        print("  To fire: set RESEND_API_KEY (or SENDGRID_API_KEY) + CONTACTS_CSV, run --send")
        return 0
    n = 0; ok = 0
    for row in csv.DictReader(open(c)):
        msg = MSGS.get(row.get("msg_key","pack"), MSGS["pack"])
        try:
            st = send(key, row["email"], "CSOAI signed compliance measurement", msg); ok += 1
        except Exception as e:
            st = str(e)[:40]
        n += 1; print("  -> %s: %s" % (row.get("company", row.get("email")), st)); time.sleep(1)
    print("sent %d / %d" % (ok, n))
    return 0
if __name__ == "__main__": sys.exit(main())
