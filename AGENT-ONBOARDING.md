# AGENT ONBOARDING — how this estate gets shit done
**Read this before touching anything. Provisional until verified against origin — the probe wins, not the report. (2026-08-19)**

## The four lanes

| Lane | Runs on | Owns | Never touches |
|---|---|---|---|
| **Claude (main)** | Nick's Mac | councilof-ai repo, upstream PRs, GitHub org | csoai-site production deploys |
| **Kimi (K3)** | Mac + pods | csoai-static-deploy2 tree, pod fleet, estate chain signing, Zenodo/Kaggle | councilof-ai |
| **DeepSeek/harness** | pods | measurement runs only | any production deploy |
| **Nick (owner)** | human | rulings, logins, spend, legal submits, merges | — |

## The coordination protocol

1. **Read `LANE_COORDINATION.md` on the shared pod before any shared surface.** Append your state when you start and finish. One lane per surface.
2. **Commit by name, never `git add -A`** on shared trees (lanes carry dirty files).
3. **Claim provisional until verified against origin.** Lanes have reported unreproducible successes before. Verify with curl/git, then claim.
4. **No live agent socket exists.** Handoffs: the coordination file, clear git commits, or Nick pasting between sessions. Write for a zero-context reader.

## The credentials model (keystone)

All secrets live in the macOS keychain (service `meok-keystone`) or on designated pods — **never** in repo files, remote URLs, or process command lines (`ps aux` leaks them; use env files chmod 600). If you can't reach a credential, ask Nick. **Never guess or fabricate access.** The estate signing keys never travel: site/release key = keystone; estate chain key = pods only.

## The canon (CI reverts violations)

- Public count: cite live **`totals.public_count`** on GET https://councilof.ai/api/gspc (currently **14 measured of 14 quotable**). Quotable board = **14**. Do not invent 22 axes.
- DOI spine: **10.5281/zenodo.21991104** (concept; see CANONICAL-DOIS.md).
- Issuer: Council of AI (CSOAI LTD, UK #16939677). Register: **measurement, not certification**.
- Kill-list in display copy: sovereign/SOV*/SOVOS/CEASAI/DEFONEOS/byzantine/BFT/33-agent · certification-as-product · SaaS pricing · "neutral referee".
- Ties are ties. UNMEASURED stays UNMEASURED. Corrections are append-only, signed, in the same record as results.

## The signature chain (verify anything in 3 lines)

```
canonical  = json.dumps(payload, sort_keys=True, separators=(",",":"), ensure_ascii=False)
content_id = sha256(canonical utf-8) as hex
signature  = Ed25519 over content_id.encode()   # pubkeys in did:web:csoai.org
```

Verify free: csoai.org/verify (in-browser) · the gspc MCP `verify` tool · the stdlib Kaggle notebook (nicktempleman/verify-csoai-signed-cards). External anchors: /proof-anchors/ (RFC 3161 + OpenTimestamps).

## Compute map (2026-08-19)

- **sov-repull (3090)**: workhorse — ollama fleet, swarm/overnight runners, arena loop. `/workspace` is the persistent pod volume; container disk wipes on stop (models re-pull).
- **sovos-light-master-mine (A100 80GB)**: fleet sweep — 14 banks × pulled fleet, estate grading. Results unsigned; signing on the key pod.
- **sov-brain-a100-fresh**: queued for capacity (£0 until boot).
- **oracle micros**: arena rounds → KV → feed.
- **Backups**: sovos-merge-800 network volume via cpu-sink (`/workspace/backups/`). Two machines or it doesn't count.

## Compute etiquette

- Resolve SSH host/port via the RunPod **API** every time — endpoints drift.
- Check for a running instance before spawning (`pgrep -f <script>`) — never double-spawn a spend loop.
- Pod stops are fine; **termination is owner-nod only** (volumes die).
- Community capacity is a queue, not a bug: 524s and cold starts mean wait, not retry-storm.

## Where things live

- Machine surfaces: csoai.org (`/.well-known/*`, `/api/*`, `/agent-card.json`, `/banks-manifest.json`, `/verification.schema.json`, `/llms.txt`, `/CANONICAL-DOIS.md`, `/proof-anchors/`) — humans 308 to councilof.ai.
- Trust root: `csoai.org/.well-known/did.json` — never break or redirect this path.
- Full API + repo map: `docs/ESTATE-CONNECTION-MAP.md`.
