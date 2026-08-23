# Live board snapshot — 23 Aug 2026 ~18:20 London

## Homepage
- Hashes still `NewHome-v3.r2-DLZkxr7I.js` / `index.r2-D7-ZzZFY.js`
- Still prints **“13 measured of 13”**
- PR 398 locked subtitle NOT live yet

## Badge
- `/api/badge` aria-label: **“GSPC measured: 13 of 14 axes”** ← wrong chrome (fix in flight)

## `/api/gspc`
- schema `csoai.gspc-axes/0.5`
- **14 axes in `axes[]` including `jail`**
- totals: measured_axes 13, quotable 14, items 887
- public_count string: “13 measured of 14 quotable (GSPC ruling 2026-08-18)”
- living_stamp signed from gold-run-3090, updated 2026-08-18T03:22:16Z
- DOI 10.5281/zenodo.21991104
- `measured_in_lane`: slot15 named **instrument-honesty** + human-vs-ai — in-lane only; CEO has NOT named slot-15 publicly

## CEO lock (unchanged)
- Public chrome: 13 measured + jail as measured **floor** + unnamed empty slot-15
- Do not restamp; do not treat jail as 14th scored axis; do not publish instrument-honesty as slot-15 until named
