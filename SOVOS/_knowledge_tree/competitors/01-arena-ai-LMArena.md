# Competitor: Arena (LMArena / Chatbot Arena) — the ARENA competitor

## What they are
- Rebranded LMArena → **Arena** (28 Jan 2026). Public LLM leaderboard.
- **Scale (their moat):** 6M votes · $1.7B valuation (Series A Jan 2026) · 5M monthly users · 150 countries · 60M conversations/month.
- Multiple boards: LLM, Vision, Code, Video, Image.

## Their method
- Pairwise: user sees 2 anonymous model answers, votes better one.
- **Bradley-Terry** rating (Elo-like for pairwise). Crowdsourced human preference.

## Method comparison — where we win / lose
| | Arena | SOV City / GSPC |
|---|---|---|
| Signal | subjective human votes | **deterministic law-anchored grading** |
| Reproducible | no (preference drift) | **yes (rerun the rows)** |
| Signed | no | **Ed25519 signed chain** |
| Tied to law | no | **EU AI Act Art 5/50, 13 axes** |
| Scale | 60M convos/mo (WINS) | tiny (LOSES) |
| Trust basis | popularity | **evidence + disclosed uncertainty** |

## The positioning line vs them
"Arena measures which model people *prefer*. We measure whether a model *obeys the law* — deterministically, signed, reproducible. Preference is a vote; compliance is a fact."

## What to steal (design/flow)
- Live-updated ranking as the hero (their #1 UX asset).
- Multiple category boards (we have 13 axes = 13 category boards natively).
- The pairwise "battle" UX → maps to SOV City arena matches (but ours are law-graded, not vote-graded).

## Register: REAL (web-verified 2026-08-12). Scale numbers are theirs, cited.
