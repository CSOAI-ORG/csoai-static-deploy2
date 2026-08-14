# CYBER ESSENTIALS — READINESS TRACKER (G-Cloud 15 prerequisite)
**Part DJ Move 3 · drafted 2026-08-14 · action window: NOW — G-Cloud 15 ~Sept 2026**
**Register**: posture REAL where checked · certification GATED (owner submit + cost)
**Why**: G-Cloud 15 (≈£14bn UK public cloud spend) now requires Cyber Essentials as a
hard prerequisite; lead time is weeks (self-assessment + certification-body validation).
Miss this window → 12-month lockout from the procurement door. This tracker is the
evidence pack that turns "we'll do it later" into a checklist with dates.

---

## WHAT CYBER ESSENTIALS IS (facts)
- UK government-backed baseline cyber security certification (NCSC scheme).
- Two levels: **Cyber Essentials** (self-assessment + external scan) and **Cyber
  Essentials Plus** (external hands-on validation). G-Cloud 15 requires CE (Plus
  recommended for higher-value lots).
- Cost: CE ≈ £300–500 via a certification body (5-assessor market, IASME/NCSC
  registered); CE Plus ≈ £1,500–2,500.
- **Lead time**: self-assessment ~2–4 weeks for a small org; certification-body
  validation ~1–2 weeks after. Realistically 4–6 weeks end-to-end → must start NOW
  for a Sept G-Cloud 15 window.

## THE 5 CONTROLS (what the self-assessment asks)
1. **Boundary firewalls & internet gateways** — inbound/outbound filtering; deny-by-default.
2. **Secure configuration** — remove/disable unused accounts, services, default creds;
   patch policy.
3. **User access control** — least privilege; MFA on cloud/email/admin; leavers offboarded.
4. **Malware protection** — AV/EDR on endpoints; deny execution of untrusted payloads.
5. **Patch management** — supported OS/apps, patched within scheme windows (14 days
   critical/30 standard).

## OUR ESTATE — honest posture map (what CE will probe)
| Asset | Posture (REAL) | CE control | Action |
|---|---|---|---|
| GitHub org (code) | 2FA + private repos | Access control | ✅ done; document |
| Cloudflare (workers/pages) | MFA, tokens scoped | Access control | ✅ done |
| RunPod pods | SSH-key-only, per-pod keys | Access control | ✅ done; document key inventory |
| A100/3090 root SSH | key auth, port-scoped | Secure config | ✅ done |
| Oracle Cloud (evac micros) | key auth | Access control | ✅ |
| Mac (Nicholas) | FileVault?, admin account | Secure config / malware | ❓ **check + enable** |
| 1Password/SSO | [FILL] | Access control | ❓ |
| Backups | MinIO master + OTS | — | ✅ 3-copy doctrine |
| Patch cadence | ad-hoc | Patch management | ⚠️ **document a 14/30-day patch note** |
| Email (Gmail/domain) | [FILL 2FA] | Access control | ❓ |
| AV/EDR on Mac | XProtect default | Malware | ✅ default; document |

## 4-WEEK ACTION PLAN (owner-led, lane-prep)
| Week | Action | Who |
|---|---|---|
| W1 (now) | Enroll with an IASME/NCSC certification body; get the self-assessment questions | Owner |
| W1 | Fill posture map (above) — lane can produce the evidence pack | Lane |
| W2 | Fix the ❓ items: FileVault, email 2FA, SSO inventory, patch note | Owner/lane |
| W2 | Document boundary firewalls (Cloudflare WAF rules, SSH ports) | Lane |
| W3 | Submit self-assessment; schedule external vulnerability scan | Owner |
| W3–4 | Address scan findings; book CE Plus validation if G-Cloud high-value lots | Owner |
| W4+ | Receive certificate → G-Cloud 15 application ready | Owner |

## EVIDENCE PACK (lane can assemble this week — zero-gate)
- [ ] Key inventory (SSH keys, tokens, CI secrets) — from `~/.runpod/ssh`, `.ssh/config`, CI vars
- [ ] Access control list (who can touch what — solo founder + named lanes)
- [ ] Firewall/WAF rules summary (Cloudflare + SSH port config)
- [ ] Patch note template (14-day critical / 30-day standard)
- [ ] Backup + OTS proof-of-existence note (3-copy doctrine, `_ip/ots/`)
- [ ] MFA evidence (GitHub/Cloudflare/email)

## GATES
- **Owner**: enrolment, any payment (£300–500), submission.
- **Lane**: the full evidence pack above (zero-gate, this week).
- Cost note: CE is the cheapest credential in the whole GTM stack and unblocks the
  largest procurement door (G-Cloud 15) + a Cyber-Essentials badge for the site.

---
*Companions: `GTM_2026-08-14.md` (Part DG — G-Cloud deferred until ISO justified, but CE
is the cheap prerequisite that removes the lockout risk at ~£400) · Part DJ (this move) ·
`AI_GROWTH_LAB_APPLICATION_2026-08-14.md` (parallel UK public-sector window).*
