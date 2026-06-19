# Email Template Verification — 5-Touch Sequence
**Date:** 17 Jun 2026  
**Files:** `~/clawd/hive-mailer/templates/5-touch/day{0,3,7,14,30}.txt`  
**Status:** 2 PASS / 3 FAIL

---

## Template-by-Template Results

### 1. day0.txt — Introduction / Hook
| Check | Result | Notes |
|-------|--------|-------|
| `{{subject}}` placeholder | ✅ PASS | Line 1: `Subject: {{subject}}` |
| `{{company}}` placeholder | ✅ PASS | Line 3: `Hi {{company}} team,` |
| `{{keystone_cert_url}}` placeholder | ✅ PASS | Line 10 |
| Subject line clear | ✅ PASS | "Subject: {{subject}}" — clean template subject |
| Tone | ✅ PASS | Professional, informative, introduces EU AI Act urgency |
| CTA | ✅ PASS | "Would you be open to a 15-min call this week?" — direct |

**Verdict: PASS**

---

### 2. day3.txt — Follow-up / Case Study
| Check | Result | Notes |
|-------|--------|-------|
| `{{subject}}` placeholder | ✅ PASS | Line 1: `Subject: Re: {{subject}}` |
| `{{company}}` placeholder | ✅ PASS | Line 3: `Hi {{company}} team,` |
| `{{keystone_cert_url}}` placeholder | ❌ **FAIL** | **Missing.** Link goes to `https://proofof.ai/case-studies/larchwood-care` — static URL, not parameterised |
| Subject line clear | ✅ PASS | Reply-style subject is appropriate for touch 2 |
| Tone | ✅ PASS | Social proof via Larchwood Care case study |
| CTA | ✅ PASS | "Happy to walk through how this applies to your stack." |

**Verdict: FAIL** — missing `{{keystone_cert_url}}` prevents personalisation of the keystone attestation link.

---

### 3. day7.txt — Regulatory Angle / Education
| Check | Result | Notes |
|-------|--------|-------|
| `{{subject}}` placeholder | ✅ PASS | Line 1: `Subject: Re: {{subject}}` |
| `{{company}}` placeholder | ✅ PASS | Line 3: `Hi {{company}} team,` |
| `{{keystone_cert_url}}` placeholder | ✅ PASS | Line 13 |
| Subject line clear | ✅ PASS | Reply-style, appropriate for touch 3 |
| Tone | ✅ PASS | Educational — breaks down 3 EU AI Act Article 50 requirements |
| CTA | ✅ PASS | "Free to try at: {{keystone_cert_url}}" — implicit but clear |

**Verdict: PASS**

---

### 4. day14.txt — Urgency / Deadline
| Check | Result | Notes |
|-------|--------|-------|
| `{{subject}}` placeholder | ✅ PASS | Line 1: `Subject: Re: {{subject}}` |
| `{{company}}` placeholder | ✅ PASS | Line 3: `Hi {{company}} team,` |
| `{{keystone_cert_url}}` placeholder | ❌ **FAIL** | **Missing.** Link goes to `https://proofof.ai` — generic, no personalised attestation URL |
| Subject line clear | ✅ PASS | Reply-style, appropriate for touch 4 |
| Tone | ✅ PASS | Strong urgency — "46 days away", "€35M or 7% of global turnover" |
| CTA | ✅ PASS | "Don't wait. https://proofof.ai" — urgency-driven |

**Verdict: FAIL** — missing `{{keystone_cert_url}}`. The urgency message loses power without a personalised attestation link.

---

### 5. day30.txt — Break-up / Closing
| Check | Result | Notes |
|-------|--------|-------|
| `{{subject}}` placeholder | ✅ PASS | Line 1: `Subject: Re: {{subject}}` |
| `{{company}}` placeholder | ✅ PASS | Line 3: `Hi {{company}} team,` |
| `{{keystone_cert_url}}` placeholder | ❌ **FAIL** | **Missing.** No personalised attestation link anywhere in template |
| Subject line clear | ✅ PASS | Reply-style, final touch |
| Tone | ✅ PASS | **Break-up/closing confirmed.** Line 5: "Last message from me on this." Line 15: "If now isn't the right time, I understand. My door is open when you're ready." |
| CTA | ✅ PASS | Soft close — leaves door open, lists pricing tiers as final reference |

**Verdict: FAIL** — missing `{{keystone_cert_url}}`. Break-up tone is correct but the template lacks the personalised attestation hook.

---

## Summary

| Template | Placeholders | Tone | CTA | Overall |
|----------|-------------|------|-----|---------|
| day0.txt | ✅ All 3 | ✅ Intro | ✅ Direct call | **PASS** |
| day3.txt | ❌ Missing keystone_cert_url | ✅ Social proof | ✅ Soft follow-up | **FAIL** |
| day7.txt | ✅ All 3 | ✅ Educational | ✅ Free trial link | **PASS** |
| day14.txt | ❌ Missing keystone_cert_url | ✅ Urgency | ✅ Deadline-driven | **FAIL** |
| day30.txt | ❌ Missing keystone_cert_url | ✅ Break-up/closing | ✅ Soft close | **FAIL** |

**Overall: 2/5 PASS, 3/5 FAIL**

---

## Recommendations

1. **Add `{{keystone_cert_url}}` to day3.txt, day14.txt, day30.txt** (critical — same fix across all three). Insert after the pitch paragraph in each template so the personalised attestation link is available at every touchpoint.

2. **Day3.txt** — Replace the static case-study URL with a dynamic `{{keystone_cert_url}}` or add the keystone URL as a second link alongside the case study.

3. **Day14.txt** — After the "€35M penalty" paragraph, add `{{keystone_cert_url}}` as the "Get your free attestation" link so urgency has a direct action.

4. **Day30.txt** — Add `{{keystone_cert_url}}` alongside the pricing tiers or as a "last chance" link in the break-up paragraph.

5. **Consistency audit** — Once placeholders are added, re-verify all 5 templates render correctly with sample data (run through the queue renderer if available).

---

## Sprint 1 SEAL Impact

**3 of 5 templates FAIL** the placeholder completeness check. This does not block the Sprint 1 SEAL if the queue renderer injects `keystone_cert_url` via a fallback/default mechanism (check `queue.jsonl` for per-entry `keystone_cert_url`). However, if the renderer blindly substitutes `{{keystone_cert_url}}` and falls back to empty string, day3/day14/day30 will send broken emails. **Recommend fix before first batch send.**
