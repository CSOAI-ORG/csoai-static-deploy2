# DATABASE-RIGHT ASSERTIONS — board_v2 / GovBench / corpus-watch (SI 1997/3032)
**Part DK play #8 · 2026-08-14 · automatic right — needs explicit statements + logs**
**Register**: REAL (assets) · the right arises automatically; this doc is the evidence pack.

---

## §1 THE RIGHT (facts, verified)
UK/EU **sui generis database right** (SI 1997/3032 implementing Dir 96/9/EC; CJEU
C-203/02 British Horseracing Board) arises **automatically** where there is substantial
investment in **obtaining, verifying or presenting** the contents (NOT in *creating*
the data). No registration. Duration 15 years from completion (a substantial new
investment restarts the term). Protects against **extraction / re-utilisation of a
substantial part** of the database.

## §2 WHAT WE ASSERT (the protected databases)
| DB | Description | Investment basis | First-complete | Rows |
|---|---|---|---|---|
| **DB-01 board_v2** | 13-axis GSPC measurement board — per-model × per-item outcomes across the 22-model fleet | obtaining (frozen item banks, canaries), verifying (held-out splits, CIs), presenting (signed cards) | 2026-08-12 | 15,580 |
| **DB-02 GovBench** | Government/public-sector governance item bank + per-model scoring | obtaining (237-item bank), verifying (canary exclusion, label checks) | 2026-06-15 | 4,329 usable |
| **DB-03 corpus-watch** | Organic government data engine: collection + verification + presentation | obtaining (198 sources/30 feeds), verifying (QA checklists), presenting (structured hive data) | ongoing | 49 GB / 16+ datasets |
| **DB-04 CareBench** | Care governance bank | obtaining (201 items + canary), verifying | 2026-06 | 3,138 usable |
| **DB-05 Art5Bench** | Legal/regulatory bank | obtaining (684 items), verifying | 2026-07 | 676 usable |

## §3 WHY THE RIGHT HOLDS (per limb)
- **Obtaining**: item banks were authored/collected through a defined process (frozen
  splits, canaries, label discipline) — documented, dated, OTS-anchored where applicable.
- **Verifying**: held-out split (FlywheelLeak), per-item CIs, canary-exclusion audits —
  this is exactly the "verification" investment the CJEU recognises.
- **Presenting**: the signed-card + registry presentation layer is a structured output
  form, not raw data dumps.

## §4 EXPLICIT ASSERTION (the statement that makes it visible)
> CSOAI Ltd (UK #16939677) asserts the UK/EU sui generis database right in the databases
> identified in §2. These databases result from substantial investment in obtaining,
> verifying and presenting their contents (SI 1997/3032; Dir 96/9/EC Art 7). Any
> extraction or re-utilisation of a substantial part is prohibited without licence.
> Facts within the databases remain quotable with attribution; the database itself and
> its substantial parts are protected.

## §5 SUPPORTING LOGS (keep current — the right's evidence)
- [ ] board_v2 run logs (per-axis, dated, signed to MinIO) — auto by board_v2
- [ ] GovBench bank changelog + canary-exclusion audit notes
- [ ] corpus-watch collection/verification checklists + version logs
- [ ] OTS stamps (`_ip/ots/` — 5 crown jewels anchored 2026-08-14)
- [ ] Held-out split verification (`HELDOUT_VERIFICATION_2026-08-14.md`)

## §6 GATES / HONESTY
- This is an assertion of an automatic right — NOT a registration (none exists).
- Facts within the databases are quotable with attribution; we do not assert rights over
  the *underlying pre-existing public data* (e.g. Land Registry records) — only over the
  collected/verified/presented database as a whole and its substantial parts.
- Counsel confirms wording before any enforcement use.

---
*Companions: `IP_ASSET_REGISTER_2026-08-14.md` (TS-01 corpus, DB section) ·
`IP_WITHOUT_REVENUE_2026-08-14.md` (Part DK) · board_v2 REAL (15,580 rows) · GovBench REAL.*
