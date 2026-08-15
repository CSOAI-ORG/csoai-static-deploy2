# Compliance Calendar — UK small-co obligations + estate ops (v1, 2026-08-15)

The operational discipline that keeps the institution on the rails. Monthly
GitHub Actions cron opens reminder issues 30 days out.

## UK statutory (CSOAI LTD, 16939677)

| Obligation | Cadence | Notes |
|---|---|---|
| ICO data protection fee | **Annual** | Tier 1 = **£52/yr** (post-17-Feb-2025 rise; canon had £40 — **verify at payment**) |
| Companies House confirmation statement | **Annual** | CSOAI LTD |
| Companies House accounts | **Annual** | Small co — micro-entity accounts possible |
| CT600 corporation tax | Annual | Due 12 months after year end |
| VAT registration | Event-triggered | Only if > £90k turnover |
| Payroll/PAYE | If hiring | n/a currently |

## Estate ops calendar

| Obligation | Cadence | Owner |
|---|---|---|
| Ed25519 key rotation | Annual review | CISO |
| TLS/domain renewal | 30-day reminder | COO |
| Card re-attestation (quoted models) | Quarterly | measurement cron |
| Oracle always-free health check | Weekly | COO |
| RunPod budget review | Weekly | CFO |
| Transparency report | Annual | CEO |
| Error statistics publication | Quarterly | CISO |
| Methodology review | Annual | CEO + CISO |
| DPIA review | Annual or on material change | CLO |
| arXiv endorsement expiry check | **2026-08-27** | CEO |

## The mechanism

- `compliance-calendar.md` versioned in the policies repo (this file)
- GitHub Actions cron: on the 1st of each month, open issues for items due
  within the next 30 days
- Every completion is a signed commit with the evidence attached