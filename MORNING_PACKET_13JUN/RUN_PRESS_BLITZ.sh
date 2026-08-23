#!/bin/bash
# PRESS BLITZ RUN SCRIPT — 13 Jun 2026
# Run this once you've reviewed the AppleScript drafts OR
# if you prefer direct send via SMTP (after Resend key rotation)

set -e

DIST=/Users/nicholas/clawd/PASSPORT_LAUNCH_13JUN

echo "=== PRESS BLITZ OPTIONS ==="
echo ""
echo "1. AppleScript (Mail.app drafts) — no key needed"
echo "   Test:  osascript $DIST/press_blitz_test.applescript"
echo "   Full:  osascript $DIST/press_blitz.applescript"
echo ""
echo "2. Direct SMTP via Resend (after key rotation)"
echo "   export RESEND_API_KEY=re_xxx"
echo "   python3 $DIST/send_press_resend.py"
echo ""
echo "3. Manual send from Mail.app (you click)"
echo "   After #1 runs, open Mail.app → Drafts, Cmd+A, Cmd+Shift+D"
echo ""
echo "=== ESTIMATED TIME ==="
echo "  Test:  5 min"
echo "  Full:  15 min"
echo "  Review + send: 10 min"
echo "  Total: ~30 min for 1,076 emails sent"
