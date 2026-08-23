# SSL.COM REPLY DRAFT — v2 (learned from full thread + conformance state) — 2026-08-18

To: Kervin Sanchez <kervin@ssl.com>, c2pa-delivery@ssl.com
From: Nicholas Templeman <nicholas@csoai.org>
Subject: Re: C2PA inquiry : SSL.com

---

Hi Kervin,

Thanks for the follow-ups — and apologies for the radio silence; this one's been
moving on several fronts at once.

The project is **active**, and there's a material update since my last email:

1. **CSOAI's C2PA Contributor membership is now active** (onboarding completed
   this week — GitHub org, Slack, and task-force invitations received).
2. **We've signed the Generator Product legal agreement** for the C2PA Conformance
   Program and are completing the **Conformance Intake Form** now. So the
   **own-certificate route is back as our primary path** — revising the
   API-first direction in my 11 Aug email. We intend to be a conformant
   generator product signing under our own C2PA claim-signing certificate,
   with "Publisher: CSOAI" on the content.

Given that, the questions that still gate our decision (you may have answered
these in materials I haven't yet matched to the thread — happy to be pointed at
them if so):

1. **Certificate + pricing**: pre-launch-startup tier pricing for one Level 1
   claim-signing certificate, and what happens at volume (we expect low
   thousands of signed assets/month scaling from there).
2. **Issuance process + timeline**: once the Conformance Letter lands, your
   steps 2–4 (CSR → validation → issuance) — realistic end-to-end time, and
   whether the portal/IV validation can run in parallel with our conformance
   evaluation.
3. **Video**: segment-level / per-frame manifest capability and any limits
   (we sign AI-rendered video with per-segment provenance).
4. **Non-media assets**: later we want credentials on JSON manifests from
   autonomous agents (structured decision records) — is there a route for
   non-media C2PA claim signing?
5. **Future key migration**: if we later move to per-agent signing keys under
   our own certificate, issued credentials remain valid (no re-signing
   requirement)?

Our timeline: Conformance Intake Form submitted this week → evaluation →
Conformance Letter. If you can confirm the above, we'll firm up the purchase
decision within a week of the letter.

Best regards,
Nick Templeman
CSOAI Ltd (UK 16939677) — nicholas@csoai.org

---

## Why this version (the learn)
- **Membership active** (onboarding Aug 17) → conformance program open → own-cert route viable again.
- **Agreement already signed Aug 4** (Conformance Admin email, ID 6518) → the "you don't need conformance via API" pivot from Kervin's Aug 10 email is now secondary: we're already committed to conformance.
- **Kervin's 5 questions from the Aug 11 email were never answered** → re-ask, tightened to the own-cert path.
- cc c2pa-delivery@ssl.com per their instruction.
- Firewall: SSL.com is a vendor for OUR OWN signing keys — no neutrality conflict (we take no money from ranked entities).
- **Action item (Nick): complete the Conformance Intake Form** — https://docs.google.com/forms/d/e/1FAIpQLSfwZG9I1SVQq-oLPTgY4XQ7TCKPHJOzpmjRMGgWgWpCR-0Q4Q/viewform
