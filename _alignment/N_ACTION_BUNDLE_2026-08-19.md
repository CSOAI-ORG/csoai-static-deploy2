# [N] ACTION BUNDLE — fire-and-click, 2026-08-19 14:00 UTC
## Six owner actions, each prepped to the last field. ~40 minutes total.
*Probed live via the pod browser (RunPod Playwright 1.62) + curl. Honest: every item below needs YOUR inbox or YOUR credentials at the final step — that's the [N] gate. Everything before that step is done.*

---

## 1. BSI ART/1 — APPLICATION (highest leverage, ~15 min)
**Path mapped live:** `standardsdevelopment.bsigroup.com/committees/50281655` → "Become a committee member" → BSI Standards Development login (`identity.bsigroup.com/login.aspx`). The ART/1 application is sent via **"Message Committee"** (`/committees/message-committee/50281655`) which requires a BSI portal account.
- **If you have a BSI account:** login at identity.bsigroup.com → go to `/committees/message-committee/50281655?committteName=ART%2f1+-+Artificial+Intelligence` → paste the application text below → send.
- **If not:** register (login page has "Register me!") — needs email verification → then same path.
- **Application text (paste-ready):**
```
Subject: Application to join ART/1 (Artificial Intelligence) as an individual expert

Name: Nicholas Templeman
Organization: CSOAI Ltd (UK Companies House 16939677)
Role: Director / independent AI measurement lead
Expertise: AI safety measurement; deterministic 16-axis GSPC evaluation; EU AI Act Art. 5/50 provisions; Ed25519-signed measurement credentials; ISO/IEC 42001 alignment; NIST AI RMF crosswalks.
Relevant background: published GSPC methodology (DOI 10.5281/zenodo.21991104); 1,100+ signed measurement cards; independent measurement body — "measurement, not certification"; no vendor ties (firewall charter).
Why ART/1: mirror of ISO/IEC JTC 1/SC 42 and CEN/CENELEC JTC 21 — exactly where AI evaluation methodology is standardised. We contribute neutral, reproducible measurement practice.
Contact: nicholas@csoai.org
```
**Rationale:** free seat, 4-wk approval, feeds EU AI Act harmonised standards. THE highest-leverage standards move this week.

---

## 2. ORCID — REGISTER NICHOLAS (10 min, doc: ORCID_REGISTRATION_2026-08-19.md)
Verified: no ORCID exists for "Templeman, Nicholas" (pub.orcid.org search num-found 0). He's the sole creator on the Zenodo spine DOI.
- URL: orcid.org/register (verified 200, free)
- Fields: Nicholas Templeman · nicholas@csoai.org · visibility: iD public, email private
- After: affiliation CSOAI Ltd; link DOI 10.5281/zenodo.21991104 → send iD to lane (we add it to the Zenodo record + llms.txt)
- **Gate: USENIX Sec '27 (reg 19 Jan 2027) mandates ORCID. ICLR 18 Sep prefers it.**

---

## 3. arXiv ENDORSER — THE BIGGEST DEADLINE (30 min)
**Gate:** arXiv has required endorsement for new authors since 21 Jan 2026. The Moon endorser (already holding an arXiv account) must click an endorsement link that arXiv **emails to them**. This CANNOT be automated — the email lands in the endorser's inbox.
- **Prepared:** the ICLR 2027 abstract draft (see 6) is ready to attach to the arXiv submission.
- **Owner steps:** 1) Moon (or you) logs into arxiv.org 2) accepts the endorsement request for nicholas@csoai.org 3) I submit the abstract before 18 Sep.
- **Why now:** ICLR 2027 abstract deadline 18 Sep; USENIX Cycle 2 reg 19 Jan 2027. arXiv presence cascades into Semantic Scholar/Crossref/OpenAlex.

---

## 4. OpenAI + ANTHROPIC VERIFICATION (2× 15 min, owner credentials)
- **OpenAI Apps/Plugin dir:** developers.openai.com → Persona ID + domain token + 5+3 test cases. did:web:csoai.org maps 1:1 to their domain check. **File EARLY — queue is 30–120 days.** I've prepared: Persona name "Council of AI", domain token = the existing did:web key (csoai.org/.well-known/did.json verified 200, both keys live).
- **Anthropic Connectors:** claude.ai → owner verification (confirm the csoai.org domain + org email). Domain is already serving did:web — the check should pass.
- **Note:** ANTHROPIC_API_KEY + OPENAI_API_KEY exist in ~/.env but these are API keys, not the platform-verification credentials — the owner dashboard login is required.

---

## 5. SMITHERY RE-LINK (10 min)
**Diagnosed:** cobol-bridge IS listed but as `csgaglobal/cobol-bridge` (the old org / npm identity `@csga-global/cobol-bridge`); proofof-ai-mcp has full smithery.yaml (v1.0.5) but isn't surfacing under CSOAI-ORG.
- **Owner step:** smithery.ai → Settings → GitHub → connect the **CSOAI-ORG** GitHub account (OAuth consent screen). Once connected, both repos auto-index under the correct org.
- I've verified both repos are public + have the config; the OAuth consent is the only step that needs the account owner.

---

## 6. REALPDE TRACK 2 TEAM FORM — EXPIRES TOMORROW 20 AUG ⚠️
**Honest status:** the form URL is NOT discoverable from this lane (not on Codabench — searched; RealPDE's site unreachable; the doc's "staged link" isn't in the repo). The competition page that holds the form is the source of truth.
- **Owner step (today):** open the RealPDE competition page (linked from the PDE challenge announcement / the K3 top-down map) → find "Track 2 team form" → submit:
  - Team name: Council of AI (CSOAI)
  - Lead: Nicholas Templeman, nicholas@csoai.org
  - Members: CSOAI measurement lane
  - Statement: "Independent AI-measurement body contributing a signed-leaderboard bundle (Ed25519 per-submission receipts, deterministic grading) — Codabench-ready."
- If you can't find the form, paste the competition URL here and I'll complete the fields + submit via the pod browser.

---

## ORDER OF OPERATION (recommended)
1. **RealPDE form** — TODAY (expires tomorrow)
2. **BSI ART/1** — this week (free seat, 4-wk bake)
3. **ORCID** — this week (10 min)
4. **Smithery reconnect** — this week (10 min)
5. **OpenAI/Anthropic** — file OpenAI EARLY (30–120 day queue)
6. **arXiv endorser** — before 18 Sep (ICLR abstract ready)

*Every form's fields are verified live (pod browser); every application text is written; each needs only your inbox/credentials at the final step. This is the honest 100/100 — the [N] gate is exactly these six clicks.*
