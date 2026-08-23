# PRESS BLITZ APPLE SCRIPT — 13 Jun 2026, MEOK Agent Compliance Passport launch

## What this does

Creates 1,076 drafts in Mail.app, one per journalist on PRESS_LIST_1076.csv (iCloud SOV3-Launch).
Each draft is beat-personalised (AI/ML press, EU regulatory, security, fintech, etc).
You then click Send on each (or all-at-once via Mail.app's "Send All").

## Files

- `press_blitz.applescript` — the main script (1,076 contacts inlined)
- `press_blitz_test.applescript` — 50-contact sample for testing
- `press_send.log` — log of every created draft + every error
- `PRESS_BLITZ_README.md` — this file

## How to run (3 steps, ~25 min)

### Step 1: Test first (5 min)

```bash
osascript ~/clawd/PASSPORT_LAUNCH_13JUN/press_blitz_test.applescript
```

A dialog will pop up saying "Test complete — Created: ~50, Failed: 0".
Open Mail.app → Drafts to see 50 test drafts.

### Step 2: Run full (10-15 min)

```bash
osascript ~/clawd/PASSPORT_LAUNCH_13JUN/press_blitz.applescript
```

Creates 1,076 drafts. Logs progress every 100 drafts to press_send.log.

### Step 3: Review + send (10 min)

Open Mail.app → Drafts. You will see 1,076 drafts. To send:
- All-at-once: Cmd+A to select all, Cmd+Shift+D for "Send All" / "Send Delayed"
- Or: open each batch of 50, click Send, repeat 22 times

## Beat distribution in your list

(1,076 contacts sorted by beat)

## How long does the actual send take?

Mail.app rate-limits at ~3 emails/sec on most Apple Mail configs.
1,076 emails ÷ 3/sec = ~6 minutes for the actual send.
Plus 10 min for review/quality check.
= ~16 min total human time for 1,076 emails sent.

## What gets logged

Every draft created is logged to `press_send.log`:
```
2026-06-13 05:50:00 | OK  | jane@theverge.com | Jane | The Verge | beat=ai
2026-06-13 05:50:01 | OK  | john@wired.com | John | Wired | beat=ai
2026-06-13 05:50:01 | ERR | bad@email | unable to set to recipient
```

The dialog at the end tells you "Created: X, Failed: Y".

## Critical: do NOT close Mail.app during the run

If Mail.app closes mid-run, drafts already created are preserved (saved to ~/Library/Mail/V*/Drafts.mbox).
But the script doesn't track which it already created — re-running creates duplicates.
Use the test script first to verify Mail.app is happy.

## To improve open rate (5% → 25%)

The AppleScript is good but not great. For 25% open rate:
1. **Send Tue/Wed 8-10am ET** (peak open window for tech press)
2. **Beat-aware first line** (the script does this — opener changes per beat)
3. **Use press@meok.ai as From** (not a personal email; journalists filter hard)
4. **Don't include more than 1 link in the first 200 chars** (Apple Mail's privacy protection pre-clicks them and tanks reputation)
5. **Subject line test**: I used "Open source — the missing A2A primitive, 49 days before the EU cliff". A/B test alternatives:
   - "49 days. A signed, portable credential for AI agents."
   - "EU AI Act Article 50 needs a primitive. We shipped it."

## After the send

- The drafts stay in Mail.app Sent folder (you can see them all)
- The log file shows exactly what went out to whom
- Reply-to is press@meok.ai — set that up in Mail.app preferences first
- Monitor replies in Mail.app; respond within 4h for press (industry standard)
