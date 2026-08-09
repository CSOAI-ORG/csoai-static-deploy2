# AI Crawler Discovery Kit — RunPod Operator Runbook

**Directive:** "WORK FROM RUNPOD NEVR MY MAC" (JEEVES session, 5 Aug 2026).
All heavy I/O (HTML inspection, head-block injection, sitemap regen, live
HTTP verification) runs on a RunPod pod. Mac = local file writes only.

---

## What this kit does

AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, OAI-SearchBot,
Meta-ExternalAgent, DeepSeekBot, Cohere-AI, MistralAI-User, Applebot-Extended,
HuggingChatBot, Bravebot, YouBot, DuckAssistBot, Amazonbot, CCBot, plus 15+
others) **do not run JavaScript**. Everything they need to discover, cite, and
rank CSOAI / MEOK content must be present in raw HTML and edge files at the
apex.

This kit delivers, per site:

**Edge files (Layer 0, served as-is from `/`):**
- `robots.txt` — explicit allow for 30+ AI crawlers, with descriptive comments
- `llms.txt` — LLM-native manifest (Answer.AI spec, Sept 2024)
- `llms-full.txt` — full content dump for LLM ingestion (new in 2026)
- `agents.txt` — AI agent traffic declaration (emerging spec, Aug 2025)
- `sitemap-ai.xml` — curated Tier 1-4 sitemap with `ai:` extension namespace
- `.well-known/llm-manifest.json` — machine-readable LLM manifest
- `.well-known/ai-plugin.json` — OpenAI legacy plugin descriptor
- `.well-known/llm-policy.txt` — declarative AI access policy
- `.well-known/security.txt` — security disclosure (RFC 9116)
- `.well-known/change-log.txt` — LLM-readable change log
- `.well-known/agent-card.json` — already exists; left untouched

**HTML upgrades (injected into every page `<head>`):**
- `<link rel="alternate" type="application/llm+json" href="...llm.json">`
- `<meta name="llms-txt" content="/llms.txt">`
- `<meta name="ai-content-declaration" content="human-authored, machine-verifiable, Ed25519-signed">`
- `<meta name="citation-policy" content="CSOAI Ltd (2026). {title}. {url}">`
- `<meta name="revised" content="{ISO8601}">`
- `<meta property="article:modified_time" content="{ISO8601}">`

The injection is idempotent — re-running the script won't double-inject.

---

## How to run on RunPod

### 1. Spin up a CPU pod (no GPU needed)
- Image: `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel` (or any py3.11 image)
- GPU: none (CPU-only is fine — this is pure I/O)
- vCPU: 4, RAM: 16 GB
- Disk: 20 GB
- Cost: ~$0.04/hr for CPU-only

### 2. Install deps
```bash
pip install requests beautifulsoup4 lxml
```

### 3. Clone the relevant deploy directory OR rsync from Mac

Easiest path: keep these files in git (csoai-static-deploy2 already is). Clone
the repo onto the pod. If the deploy isn't in git, rsync from Mac:

```bash
rsync -avz --exclude='.git' --exclude='node_modules' \
  ~/clawd/csoai-static-deploy2/ runpod:/workspace/csoai-static-deploy2/
rsync -avz --exclude='.git' --exclude='node_modules' \
  ~/clawd/meok-ai-landing/ runpod:/workspace/meok-ai-landing/
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='node_modules' \
  ~/clawd/meok-os-deploy/ runpod:/workspace/meok-os-deploy/
```

### 4. Run the script

```bash
python3 scripts/runpod_ai_seo_kit.py \
  --csoai-root /workspace/csoai-static-deploy2 \
  --meok-root /workspace/meok-ai-landing \
  --meok-os-root /workspace/meok-os-deploy \
  --apex-csoai https://www.csoai.org \
  --apex-meok https://meok.ai \
  --apex-meok-os https://os.meok.ai \
  --out /workspace/ai-seo-kit-summary.json
```

The script will:
1. Write all 10 edge files per site
2. Enumerate every `.html` per site and count missing-head files
3. Inject the head-block into every file missing AI meta (idempotent)
4. Regenerate `sitemap.xml` (full enumeration) and `sitemap-ai.xml` (Tier 1-4)
5. HEAD-verify every Tier-1 URL against the live apex
6. Emit a JSON summary to `--out`

Inspect-only mode (no edits, no network):
```bash
python3 scripts/runpod_ai_seo_kit.py --no-inject --no-verify ...
```

Dry-run with live checks but no file edits:
```bash
python3 scripts/runpod_ai_seo_kit.py --no-inject ...
```

### 5. Deploy
Once the summary shows all green, deploy each site's changed files to its
hosting platform:

- **csoai-static-deploy2** → Cloudflare Pages (recent switch per Hermes tick 235)
- **meok-ai-landing** → Vercel
- **meok-os-deploy** → Vercel (`os.meok.ai`)

For csoai (Cloudflare Pages):
```bash
cd /workspace/csoai-static-deploy2
npx wrangler pages deploy . --project-name=csoai-site --branch=main
```

For meok (Vercel):
```bash
cd /workspace/meok-ai-landing
npx vercel deploy --prod --yes
```

### 6. Schedule weekly

The AI-crawler landscape moves. Add a cron on the RunPod pod (or a separate
RunPod cron job):

```cron
0 7 * * 1  cd /workspace/csoai-static-deploy2 && \
  python3 scripts/runpod_ai_seo_kit.py --no-inject > /tmp/ai-seo-monday.log 2>&1
```

(Monday 07:00 UTC = weekly audit, log to disk, no edits — review log, decide
whether to inject if new AI-crawler UA strings appeared upstream.)

---

## Sites covered

| Site             | Deploy dir                     | Apex                  |
|------------------|--------------------------------|-----------------------|
| CSOAI            | `csoai-static-deploy2/`        | https://www.csoai.org |
| MEOK AI Labs     | `meok-ai-landing/`             | https://meok.ai       |
| MEOK OS          | `meok-os-deploy/`              | https://os.meok.ai    |

---

## Red lines (do not auto-edit)

- `.well-known/agent-card.json` — exists, hand-crafted. Script reads but never overwrites.
- Files under `_CLAIM_TICK*` (DEFONEOS sprint state) — never edit.
- `benchmark-results/flywheel/` — blocked in robots.txt, never write to.
- Any file matching the `Disallow:` patterns in robots.txt.

---

## Re-run cost

First full pass: ~5 min (228 csoai HTML + 16 meok HTML + ~30 os.meok HTML).
Subsequent runs: <2 min (idempotent; injection skipped on already-injected files).

Weekly audit: <2 min (inspect-only).

---

## Related surfaces (not part of this script, separate work)

- `defoneos.html` and the ~200 deep-dive packs — already canonical + JSON-LD on most pages. RunPod script auto-detects gaps and patches.
- Hugging Face dataset pages — not on csoai.org apex; covered by HF's own SEO. Out of scope.
- PyPI packages (`meok-*`) — covered by PyPI's own metadata. Out of scope.

---

Last updated: 2026-08-05 by JEEVES.
