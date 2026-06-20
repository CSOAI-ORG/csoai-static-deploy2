# M55: Post-Launch Roadmap & Handoff — 17 June 2026

**Scope:** Draft roadmap for after 4 July 2026 launch — EU AI Act Article 50 countdown, customer onboarding, ops schedule.

**Status:** Pre-launch draft

**STOP_DEPLOY** — staged only, not yet active.

---

## 1. Launch Day: 4 July 2026

| Time (BST) | Event | Owner |
|:----------:|-------|:-----:|
| 00:00 | MEOK goes live. All Sprint 1–4 assets public | Hermes Agent |
| 00:01 | Birthday launch page active → redirect from meok.ai | DNS |
| 08:00 | Social announcement: LinkedIn, Twitter/X | TBD |
| 09:00 | Free attestation directory live (200 certs) | Attestation Engine |
| 12:00 | First customer pipeline opens | TBD |
| 18:00 | Launch retrospective / metrics check | Hermes Agent |

---

## 2. EU AI Act Article 50 — 30-Day Countdown

### Context

The EU AI Act **Article 50** (Transparency obligations) comes into full effect **2 August 2026** — roughly 30 days after MEOK launch. This creates a natural urgency window for compliance adoption.

### Countdown Timeline

| Date | Days to Deadline | Milestone |
|:----:|:----------------:|-----------|
| 4 Jul | 29 | MEOK Launch |
| 11 Jul | 22 | Week 1 post-launch — customer onboarding wave 1 |
| 18 Jul | 15 | Week 2 — enterprise outreach, compliance webinar |
| 25 Jul | 8 | Week 3 — final compliance push, media coverage |
| 1 Aug | 1 | Last day before Article 50 enforcement |
| **2 Aug** | **0** | **Article 50 comes into force** |

### MEOK Positioning During Countdown

- Every piece of outreach should reference **"Article 50 takes effect 2 August"**
- Countdown timer on `/article-50/` pages
- Blog post: "29 days until EU AI Act transparency rules apply — what you need to do"
- Email drip campaign: 4-part series (weekly) covering Article 50 obligations

---

## 3. Post-Launch Roadmap (Weeks 1–12)

### Week 1: 4–10 Jul

| Action | Detail | Owner |
|--------|--------|-------|
| Launch day execution | Go-live checklist, announcements, cert directory live | Hermes Agent |
| H3 Stripe closure | Complete Stripe dashboard → enable Pro/Enterprise payments | TBD |
| Customer onboarding pipeline | First customer intake: qualification → attestation → cert issuance | TBD |
| Blog: launch post | "MEOK is live — EU AI Act compliance in 17 days" | Content |
| Social proof seed | Reach out to first 5 beta users for testimonials | TBD |

### Week 2: 11–17 Jul

| Action | Detail | Owner |
|--------|--------|-------|
| Article 50 countdown email 1 | "29 days to comply — are you ready?" | Marketing |
| Industry outreach | Finance + Healthcare verticals — direct email | Sales |
| Compliance directory submission | Submit MEOK to EU AI Act compliance directories | TBD |
| Blog: Article 50 deep-dive | "What Article 50 means for your AI systems" | Content |
| Pricing — switch from test → live | Stripe live keys, remove "staging" labels | Dev |

### Week 3: 18–24 Jul

| Action | Detail | Owner |
|--------|--------|-------|
| Article 50 countdown email 2 | "22 days — transparency obligations explained" | Marketing |
| Mid-launch metrics review | Page views, attestation downloads, sign-ups | Analytics |
| Customer case study (first) | If any customer onboarded, publish case study | Content |
| Legal vertical outreach | Law firms, legaltech — Article 50 impact on legal AI | Sales |

### Week 4: 25 Jul – 2 Aug

| Action | Detail | Owner |
|--------|--------|-------|
| Article 50 countdown email 3 | "8 days — final compliance checklist" | Marketing |
| Article 50 countdown email 4 | "Tomorrow is the deadline — here's how to certify" | Marketing |
| **2 Aug — Article 50 enforcement** | Monitor compliance inquiries, press mentions | All |
| Emergency response plan | Handle any press/regulatory questions | TBD |

### Weeks 5–8: Aug (Post-Enforcement)

| Action | Detail |
|--------|--------|
| Compliance surge handling | Scale attestation generation if inbound demand spikes |
| Enterprise tier launches | Full enterprise onboarding with custom pricing |
| API release | Public API for attestation verification |
| Partner programme | Compliance consultancy partnerships |
| Blog: "We predicted this" | Article 50 enforcement retrospective |

### Weeks 9–12: Aug–Sep

| Action | Detail |
|--------|--------|
| EU Code of Practice review | Align with any updates to Code of Practice |
| International expansion | UK ICO alignment, GDPR intersection |
| Certification marketplace | Full cert directory, search, filter by vertical |
| MRR tracking begins | Honest accounting: first paying customers expected |
| Sprint 5 planning | Post-launch feature roadmap |

---

## 4. Customer Onboarding Pipeline

### Pipeline Stages

```
Inquiry → Qualification → Free Attestation → Pro Trial → Paid Subscription
   |            |                |                 |              |
   v            v                v                 v              v
  Form      Eligibility     10 free certs     14-day         £29/mo or
  submit    check           issued            Pro trial     Enterprise
```

### Stage Details

| Stage | Gate | Trigger | Action |
|-------|:----:|---------|--------|
| **1. Inquiry** | Contact form on /pricing/ or lead magnet | User submits form | Auto-respond with free attestation offer + info pack |
| **2. Qualification** | Eligibility check (vertical, AI usage, EU presence) | Inquiry received | Qualify within 24 hr — reject or advance |
| **3. Free Attestation** | Issue 10 free keystone attestations | Qualified | Batch-generate attestations, email cert links |
| **4. Pro Trial** | 14-day free trial of Pro tier | Attestations delivered | Send trial invite, schedule onboarding call |
| **5. Paid Subscription** | Payment processed (Stripe) | Trial ends or upgrade requested | Convert to paid, issue full cert suite |

### Pipeline Automation Targets

| Metric | Target |
|--------|:------:|
| Time from inquiry → qualification | < 24 hr |
| Time from qualification → attestation issuance | < 1 hr (batch) |
| Trial → paid conversion rate | > 20% |
| First paying customer | By end of Week 3 post-launch |

---

## 5. Post-Launch Ops Schedule

### Daily (Launch Week)

| Time | Task |
|:----:|------|
| 09:00 | Check attestation generation logs, verify no batch failures |
| 10:00 | Review contact form submissions (pipeline stage: inquiry) |
| 12:00 | Social media check — mentions, questions, issues |
| 15:00 | Metrics check — page views, cert downloads, sign-ups |
| 18:00 | End-of-day status update |

### Weekly (Post-Launch)

| Day | Task |
|:---:|------|
| Monday | Pipeline review: inquiries → conversions, blockers identified |
| Tuesday | Content publishing: blog post, social, outreach |
| Wednesday | Compliance check: EU AI Act updates, Code of Practice changes |
| Thursday | Outreach: direct email to target verticals |
| Friday | Metrics report: MRR (honest), certs issued, pipeline velocity |
| Weekend | Automated monitoring only — no manual ops |

### Monthly

| Task | Frequency |
|------|:---------:|
| Full sprint retrospective | Monthly |
| Stripe payout reconciliation | Monthly |
| Attestation renewal checks (1-year expiry) | Monthly |
| EU AI Act regulatory monitoring | Monthly |
| Infrastructure cost review | Monthly |

---

## 6. Honest Accounting & Metrics Tracking

### Key Metrics (Post-Launch)

| Metric | Launch Day | Week 1 Target | Month 1 Target |
|--------|:----------:|:-------------:|:--------------:|
| MRR | £0 | £0 (free tier only) | £500–2,000 |
| Free attestations issued | 200 | 250 | 500+ |
| Paid subscribers | 0 | 0 | 10–50 |
| Unique site visitors | — | 1,000 | 10,000 |
| Cert verification requests | — | 100 | 500 |
| Pipeline inquiries | — | 20 | 100+ |

### Cost Tracking

| Item | Est. Monthly Cost | Note |
|------|:-----------------:|------|
| GitHub Pages hosting | £0 | Free tier |
| Namecheap domain renewal | ~£8.50/yr | ~£0.71/mo |
| Namecheap DNS | £0 | Included |
| npm packages | £0 (public) | Free for public packages |
| Stripe fees | 1.4% + 20p | Per transaction only |
| Hermes Agent infra | £0 | Self-hosted |
| **Total fixed cost** | **~£0.71/mo** | |

---

## 7. Key Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Article 50 enforcement delays or changes | Medium | Low | EU AI Act is passed law — enforcement date is fixed |
| Stripe not ready by launch | Low | Medium | Launch with Free tier only; Pro/Enterprise go live when Stripe is ready |
| Low initial traffic | Medium | Medium | SEO, lead magnets, industry outreach — 20 verticals = broad surface area |
| Customer onboarding pipeline empty | Medium | High | Pre-seed outreach during Sprint 4; 200 free attestations as incentive |
| Competing compliance tools | Low | Low | MEOK is earliest mover for Article 50 specific compliance |
| Hermes Agent capacity | Low | Medium | Agent can scale — monitor batch generation performance |

---

## 8. Immediate Actions (Pre-Launch)

| # | Action | Owner | Deadline |
|:-:|--------|:-----:|:--------:|
| 1 | Complete Stripe dashboard | TBD | 3 Jul |
| 2 | Generate 200 free attestations (batch) | Hermes Agent | 3 Jul |
| 3 | Close H1 DNS (apex A records) | Dev | 3 Jul |
| 4 | Create npm automation token → publish packages | Dev | 3 Jul |
| 5 | Pre-write launch blog posts (3 drafts) | Content | 3 Jul |
| 6 | Set up email capture / pipeline forms | Dev | 4 Jul |
| 7 | Confirm first beta user list | TBD | 4 Jul |

---

*Prepared: 17 June 2026 · Sprint 4 DRAGON MODE · STOP_DEPLOY — staged only*
