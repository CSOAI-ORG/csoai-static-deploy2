# PyPI PURGE MEMO — for Nick (K3 plan #3, verified 2026-08-19)
**From:** JEEVES (K3) · **Action needed:** yank ONE package · **Verified live, never assumed**

---

## The package to yank
**`meek-3-and-sov3-connection-mcp` v1.0.0** — EXISTS on PyPI (verified HTTP 200 via pypi.org JSON API, 2026-08-19).

- **Why:** the name carries `sov3` — an internal codename. Per the naming lock (canon: *internal codenames never ship publicly*), this is a brand-purge breach on a public distribution surface.
- **Tags/description:** carries sov-space, sovereign, csoai framing.
- **The purge-list scan (K3 plan #3):** `sov3-connection`, `sovos-core`, `sov33`, `sov3` → all 404 (clean). This ONE package is the only leak.

## What to do (Nick, ~2 min)
1. `pip index versions meek-3-and-sov3-connection-mcp` (confirm)
2. PyPI → project → **yank release 1.0.0** (or delete the project — owner call)
3. If the package is live/used: republish as `meek-3-and-csoai-connection-mcp` (public brand) with a deprecation notice on the old name.

## What's already clean (verified, no action)
- sovos-core / sov33 / sov3 / sov3-connection → 404 (not published)
- The estate's HF/Kaggle/GitHub org surfaces were checked in prior audits

## SIGIL
`pypi-purge-memo-2026-08-19-jeeves`
