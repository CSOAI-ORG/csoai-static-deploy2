# SOVOS — Sovereign Open World Operating Stack

The canonical substrate of CSOAI. **See [`MASTER_MANIFEST.md`](./MASTER_MANIFEST.md) for the complete inventory of all 38 packages, the data layer, the api layer, the deploy layer, the published layer, and the wiring topology.**

```
SOVOS/
├── MASTER_MANIFEST.md           ← start here
├── packages/                    ← 38 runtime packages (pip install -e .)
├── data/                        ← operational data (charters, hive)
├── api/                         ← Vercel serverless endpoints (7)
├── deploy/                      ← host configs (a100/, m2-deployment-kit/)
├── frontends/                   ← public HTML surfaces (arenas.html, etc.)
├── published/                   ← published artefacts (sovereign-wiki/)
├── pyproject.toml               ← unified install for all 38 packages
└── README.md                    ← this file
```

## How a new agent picks this up

1. **Read `MASTER_MANIFEST.md`** — it tells you every package, where it was absorbed from, where it lives, and what it does.
2. **Clone the repo** at branch `jv-wave8-production`. Anything you find on a pod under `/workspace/csoai-static-deploy2/` is a **mirror** of this repo. Any pod-side edits that contradict this tree are bugs.
3. **For A100 pod**: `SOVOS/deploy/a100/README.md` has the bring-up recipe (single command).
4. **For measurement**: `SOVOS/packages/sovos-arena/` is the measurement front; `SOVOS/packages/sovos-signal-index/` is the Mahalanobis-to-permitted calibration; `SOVOS/packages/sovos-chain/` + `sovos-fisher-rao/` + `sovos-jspace-hyperbolic/` is the chain math; `SOVOS/packages/sovos-oscal/` emits the attestation.
5. **For the hive kernel (Rust)**: `SOVOS/packages/sovos-hive/rust-kernel/`.
6. **For public-facing tools**: `arenas.html`, `cpo-calculator.html`, `injection-scanner.html`, `birth.html`, `bus-portal.html`.

## The 13 GSPC axes (the contract)

`gov, prv, agi, asi, mcp, oss, mach, care, xr, det, art5, swarm, affect` — these
are the substrate-wide measurement axes. Every package that emits a
score, an attestation, a chain verdict, or a SIGIL uses this set.

*For the rest, see MASTER_MANIFEST.md.*

*One tree. One truth. One substrate.*
