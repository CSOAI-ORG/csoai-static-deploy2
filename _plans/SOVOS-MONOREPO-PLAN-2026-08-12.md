# SOVOS MONOREPO PLAN — 2026-08-12
*One sovereign source of truth. Doctrine encoded as CI. Distribution preserved by design.*

## 0. Why now
The session's failure modes all trace to scattered state: stale dists (BF), wrong publicDir (BL), number drift (63/200/201, 13/10/11, 300+/81/38 MCP counts), unparked lanes (BX), unreceipted commits (BY). A monorepo with doctrine-as-CI kills the class, not the instances.

## 1. The one decision already made for us
**Distribution repos stay.** The 568 public MCP repos are PyPI/Smithery/registry discovery artifacts — they must remain individual public repos. But they become **read-only mirrors generated from the monorepo** (one README template, one pricing table, one fleet count). That kills G1–G4 at the root: copy lives once, propagates everywhere.

## 2. Layout (evolve `csoai-static-deploy2` into the monorepo — it's already the closest thing)

```
csoai/                              # the sovereign monorepo (private)
├── apps/
│   ├── councilof-ai/               # React/Vite site (current councilof-ai repo merges in)
│   ├── meok/                       # meok.ai + os.meok.ai
│   ├── proofof/                    # FROZEN pending owner disposition — no edits
│   └── campaigns/                  # agisafe, asisecurity, openmoe, safetyof (revive on CF)
├── packages/
│   ├── sovos_league/               # arena, Glicko-2, arena_wire (is_infra_tainted)
│   ├── gspc/                       # bench.py, tail.py, item_gate.py, scorer resolvers
│   ├── crosswalk/                  # charter_crosswalk.py + charter→law maps
│   ├── keystone/                   # HF publish pipeline (with delta-note enforcement)
│   ├── sign/                       # Ed25519 cards, JUDGE.lock, aggregation pinning (BV.3)
│   └── mcp-generators/             # templates that generate the 568 distribution repos
├── banks/                          # gspc-* item sources (single home; HF = publish target)
├── charter/                        # 52-article charter (34 substantive + 18 reserved, BP.3 canon)
├── registry/
│   ├── numbers.json                # A4 — every public number, sourced from signed cards
│   ├── claim-linter-rules.json     # A3 — killed terms, non-canon dates, unratified ordinals
│   ├── deploy-ledger.json          # A2 — repo→CF project→domain→bundle hash→last probe
│   ├── fleet-roster.json           # A6 — pod↔job↔GPU↔ETA (incident-justified P0)
│   └── owner-gates.md              # A7 — the visible queue
├── ops/
│   ├── runbooks/                   # master stack, incident 2026-08-12, recovery
│   ├── master-stack/               # MinIO configs, LaunchAgents, rclone remotes
│   └── pod-doctrine.md             # effect-probe, heredoc, daemonization, durable-streaming rules
└── docs/                           # parts AX–BZ live here too (master register mirrored)
```

## 3. Doctrine-as-CI (the gates that make it sovereign)
| Gate | Rule encoded | Source |
|---|---|---|
| `claim-lint` | killed terms, non-canon dates, unratified axis ordinals, "52-article", registry-mismatched numbers — blocks public-bound copy | A3/BP/BO |
| `numbers-check` | any public number must exist in numbers.json with a signed-card source | A4 |
| `naming-lint` | no `sov-*` / SOVOS / SOV4 / SOVEREIGN / "Sovereign OS" in public artifacts (sites, READMEs, HF cards, PyPI descriptions) | AX/H1/G3 |
| `secret-scan` | gitleaks + trufflehog on every push AND full-history scan weekly (G6) | audit |
| `effect-probe` | post-deploy live grep (cache-busted) must pass before a deploy is "done" | A1/A5 |
| `ratification-gate` | axis/season ordinals only from the ratification log; announcements blocked | BN.3/BF.3 |
| `durability-check` | long runs must register streaming-writes config before start (BX.4: ≤5 min unlanded rows) | BX |
| `counsel-gate` | legal-gold label schemas carry counsel-signoff field; unsigned = COUNSEL-PENDING watermark | BP.5/BX.5 |

## 4. Secrets policy (never again scp'd around pods)
1Password/age-vault as the only home; pods get short-lived scoped tokens via env at job start; `.env.example` only in repo; **HF tokens rotated + minimally scoped this week** (the July HF autonomous-breach makes this urgent, audit §5); OpenRouter/CF/Stripe/RunPod keys in vault with named owners; root MinIO creds never leave the master (BS.3).

## 5. Migration sequence (each step independently reversible)
1. **Week 1:** create `registry/` + doctrine-as-CI in current csoai-static-deploy2 (numbers.json seeds from this session's corrections). Zero moves, pure addition.
2. **Week 1–2:** banks/ + packages/gspc merge (single home for item sources; HF publish via keystone unchanged).
3. **Week 2:** apps/ merge (councilof-ai repo folds in; CF Pages projects repoint at monorepo subdirs — deploy ledger records every mapping).
4. **Week 2–3:** mcp-generators/ — template the MCP README (one fleet count, doctrine-clean claims, counsel-safe wording) and regenerate the 568 distribution repos. **This is the G1–G4 fix.**
5. **Week 3:** charter/ + crosswalk/ + ops/ fold in; master register mirrored to docs/.
6. **Ongoing:** HF/Kaggle remain publish targets (never sources); Zenodo DOI automation (B4) hooks keystone.

## 6. What the monorepo explicitly does NOT do
- Does not merge datasets as weights — the five-conversion ruling (BG) stands; banks are sources, HF is publication.
- Does not make everything public — monorepo is private; public artifacts are generated/mirrored.
- Does not centralize the judge — JUDGE.lock stays a bolted artifact with hash-pinning; the monorepo holds its hash, never its discretion.
- Does not absorb sibling lanes' uncommitted work — migration is lane-coordinated, nothing force-merged.

## 7. Success definition
One clone = full estate context. One CI run = doctrine enforced. One registry = every public number. One ledger = every deploy. Zero copy-paste between surfaces. And the incident class of 2026-08-12 (scattered state causing loss) becomes structurally impossible.
