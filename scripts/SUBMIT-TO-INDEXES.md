# llms.txt Submission Checklist

Submit the kit's discovery files to AI-bot indexes so the bots learn about the
apex within minutes rather than waiting for organic discovery.

## One-time setup

```bash
# 1. Generate IndexNow key (hex, 32 chars)
KEY=$(openssl rand -hex 16)
echo "$KEY" > ~/clawd/INDEXNOW_KEY.txt

# 2. Host the key file at each apex (CF Pages serves .txt from root)
for apex in csoai-static-deploy2 meok-ai-landing meok-os-deploy; do
  cp ~/clawd/INDEXNOW_KEY.txt ~/clawd/$apex/${KEY}.txt
done
# After deploy: curl https://www.csoai.org/${KEY}.txt must return the key.
```

## Bing IndexNow (5 min)

Covers Bing + Yandex + Seznam + Naver; Bing powers ChatGPT search + Copilot +
DuckDuckGo. IndexNow-submitted URLs crawl within minutes.

```bash
bash scripts/indexnow_ping.sh "$(cat ~/clawd/INDEXNOW_KEY.txt)"
```

Expected: 3 apexes, each returning HTTP 200 with body `{"ok":true,...}` or empty.

## llmstxt.directory + Awesome-LLMS.txt (manual, 15 min)

The canonical llms.txt indexes. PR each apex:

| URL | Submission method |
|---|---|
| https://www.csoai.org/llms.txt | PR to github.com/llmstxt/llmstxt.directory |
| https://meok.ai/llms.txt         | PR to github.com/llmstxt/llmstxt.directory |
| https://os.meok.ai/llms.txt     | PR to github.com/llmstxt/llmstxt.directory |
| (all 3)                          | PR to github.com/awesome-llms-txt/awesome-llms-txt |

PR body template:
```
Adds: <apex> — <one-line description>
Canonical: <apex>
Manifest: <apex>/.well-known/llm-manifest.json
License: CC-BY-4.0
```

## Operator-portal submissions (manual, 15 min)

Each AI vendor has a bot-info page; submitting our apex to those pages gets us
listed in their bot-discovery directories.

| Vendor | URL to submit | Notes |
|---|---|---|
| OpenAI | https://platform.openai.com/docs/plugins/bot | submit apex for GPTBot verify |
| Anthropic | https://www.anthropic.com/claude-bot | submit apex for ClaudeBot verify |
| Perplexity | https://docs.perplexity.ai/guides/bots | submit apex for PerplexityBot verify |
| Google Search Console | https://search.google.com/search-console | robots.txt tester (paste https://www.csoai.org/robots.txt) |
| Common Crawl | https://commoncrawl.org/big-data/contact | email — 2-week response |

## Citation-discovery (AEO follow-up, optional)

After 7 days, spot-check whether AI answers cite the apex:

1. Open ChatGPT (web, not API)
2. Ask 8 prompts derived from the apex's most-cited surfaces:
   - "What does CSOAI measure?"
   - "What is MEOK OS?"
   - "EU AI Act Article 43 self-assessment route?"
   - ...
3. Record cited URLs into `~/clawd/benchmark-results/ai-citation-spot-check.csv`
4. Diff against sitemap-ai.xml Tier 1 — flag any Tier-1 surface that's not
   being cited, since the kit should make them all citable.

Cadence: initial baseline at ship-time, then every 14 days.

## Weekly cron (pod-side, post-deploy)

```cron
0 7 * * 1  cd /workspace/csoai-static-deploy2 && \
  python3 scripts/runpod_ai_seo_kit.py --no-inject --no-verify \
    --out /workspace/ai-seo-audit-$(date +\%Y-\%m-\%d).json && \
  rclone copy /workspace/ai-seo-audit-$(date +\%Y-\%m-\%d).json \
    gdrive:SOV/ai-seo-audit/ --transfers 4 --checkers 4
```

(Monday 07:00 UTC = off-peak; runs inspect-only, no edits, no network probes.)

## What this checklist does NOT do

- Cannot make OpenAI/Anthropic/Perplexity actually train on the apex — that's
  the bot's crawl-cadence decision. CCBot going through is the single
  highest-leverage signal we can send (per D21 durable memory).
- Cannot guarantee citation. AI citation depends on bot prompt-matching, not
  our kit alone. The kit maximises the *chance* of citation by being
  discoverable + machine-readable + redundant across 5 manifest formats.
- Does NOT fix MX + DMARC for councilof.ai / sovereign.wiki — that's a
  separate Nick gate (see alignment doc).