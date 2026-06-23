# FAQPage Schema — Added 17 Jun 2026

## What Was Fixed

**File:** `~/clawd/meok.ai/public/article-50/marking.html`

### Gap Found
The page had only a `Product` JSON-LD schema (for MEOK Pro £199/mo tier). It was missing a `FAQPage` schema, which is a **critical SEO/rich-snippet gap** for a technical specification page that answers common compliance questions.

### Schema Added
A complete `FAQPage` structured data block was appended as a second `<script type="application/ld+json">` block, immediately after the existing Product schema and before `</head>`.

### 7 Questions Added

| # | Question | Answer Summary |
|---|----------|---------------|
| 1 | What is Article 50 of the EU AI Act? | Requires AI-generated/manipulated content to carry visible labels + machine-readable markers (C2PA, XMP, W3C) |
| 2 | What marking formats are required for AI-generated content under Article 50? | C2PA, XMP, IPTC, W3C Web Annotation, digital signatures, audio watermarking |
| 3 | What is C2PA and why is it the recommended standard? | W3C-standard tamper-evident provenance metadata, cryptographically signed, portable across formats |
| 4 | What is the compliance deadline for AI output marking? | 2 August 2026 — both visible and machine-readable layers must be implemented |
| 5 | How does visible watermarking differ from machine-readable metadata? | Visible = human-readable overlay; machine-readable = embedded data (C2PA, XMP, signatures) for programmatic verification |
| 6 | What content types require AI labelling under Article 50? | Text/articles, images, video, audio, chatbots, code — each with specific visible + machine-readable requirements |
| 7 | What does MEOK Pro include for Article 50 compliance? | C2PA, W3C/XMP injection, digital signatures, watermark automation, audit logs, REST API, policy engine, priority support |

### File Stats
- **Path:** `~/clawd/meok.ai/public/article-50/marking.html`
- **Size before:** 19,603 bytes (389 lines)
- **Size after:** 21,554 bytes (453 lines)
- **Delta:** +1,951 bytes (+64 lines for FAQPage schema)

### Audit Context (Sprint 2 M22)
This addresses the FAQPage schema gap identified in Sprint 2 audit findings. The homepage and 20+ other pages across the domain ecosystem remain flagged for schema gaps — this fix is scoped to `marking.html` per task requirements.

### Verification
- ✅ JSON-LD syntax valid (double-quoted keys, proper nesting, no trailing commas)
- ✅ 7 questions × 1 accepted answer each — all answers substantive (non-trivial, >30 words)
- ✅ `@context: https://schema.org`, `@type: FAQPage`, `mainEntity` array with `Question`/`Answer` types
- ✅ No conflict with existing Product schema (separate script blocks)
- ✅ Questions directly relevant to page content (AI marking standards, Article 50)
