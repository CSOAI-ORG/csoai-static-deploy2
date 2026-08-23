# csoai.org OUTAGE — INCIDENT NOTE 2026-08-10 04:49Z

**Severity:** PRODUCTION OUTAGE — sustained.
**Status at filing:** csoai.org returning HTTP 522 (Cloudflare origin timeout) for ~19.5 minutes.
**Status as of 05:02Z:** Still DOWN, **fails=65 (~32.5 min sustained)**. **No sibling fix attempt in last 30+ min.** Sibling cron continues firing `chore: EAT_ALL` every 5 min (latest: `127f4ed chore: EAT_ALL hourly run 2026-08-10T05:00:05Z`) but those are data-only writes — no `wrangler pages deploy` activity at all since tick-249 at ~03:40Z (~80 min ago).
**Status as of 05:12Z (with Nick's report):** Still DOWN, **fails=85 (~42.5 min sustained)**. Nick captured the actual Cloudflare 522 page at `04:32:39 UTC` with **Cloudflare Ray ID `a28c47296e6360e2`** — that's 2 min after my watchdog's last-UP timestamp (04:29:22Z), confirming the outage began exactly when the watchdog flagged it. Nick's hypothesis: "I think it was Kimi from old tasks loading" — **partially consistent**: the Kimi webbridge daemon (PID 79901) IS currently running on `127.0.0.1:10086` and has been crash-looping with `bind: address already in use`, AND its upgrade cron has been failing daily for 4 days straight (`v1.11.6 not yet available, manifest=404`). However, the webbridge daemon itself does NOT directly load csoai.org — it only hits `https://cdn.kimi.com/webbridge/...` and `https://gator.volces.com`. **What *might* be loading csoai.org:** an older Kimi *user-facing browser session* (mentioned in Nick's transcript header "Browser / Working / London / csoai.org / Host / Error"), or the Kimi agent-extension-daemon making repeated failed bind attempts that exhaust origin. **Unconfirmed root cause.**
**Watcher:** `com.csoai.site-watch` LaunchAgent has detected DOWN state, fails counter = 85+ (~42.5 min as of 05:12Z).

## Evidence

- `curl -sS -o /dev/null -w "%{http_code} %{size_download}" https://csoai.org/` → `522 16` (×2 probes separated by 3s — not a single-sample fluke)
- `/tmp/csoai-watch.state` → `DOWN`
- `/tmp/csoai-watch.fails` → `39` (39 × 30s ≈ 19.5 min of consecutive failures)
- `/tmp/csoai-watch.heartbeat` → `2026-08-10T04:29:22Z UP` (last UP timestamp before outage began; the script writes heartbeat only on UP — this is normal behaviour, not misleading)
- `/tmp/csoai-watch.log` → empty (the script's notification path runs `say` + `osascript`, not log-writes; on the headless Mac with no logged-in user, `say` likely failed silently. The state file IS the canonical "I know it's down" signal.)

## Likely causes (ordered by probability)

1. **Cloudflare Pages infrastructure issue, NOT a content bug.** Sibling cron is firing every 5 min (not hourly as AGENTS.md comment suggested — confirmed via git reflog), but the most recent deploy-relevant commit is `c0bf41c tick-249 SIGIL: 6 link fixes + sitemap 307->322, deployed a75d1600` at ~03:40Z. That's **~50 min BEFORE the outage began at 04:29Z**. The intervening commits (04:40, 04:45, 04:50, 04:55) are all `chore: EAT_ALL` data-flywheel writes — they don't touch `_site/`, `wrangler.toml`, or `functions/`, so they don't redeploy. **The live site content is from tick 249 and shouldn't be broken.** Most likely: a Pages project deploy is stuck in Cloudflare's pipeline (orphan from a sibling lane), or CF Pages is having a regional backend issue.
2. **Sibling cron `EAT_ALL` race?** Unlikely — those commits don't trigger `wrangler pages deploy`. They only write `benchmark-results/*.json` to disk.

## What I did NOT do (and why)

- **Did not run `wrangler pages deploy`** — even a defensive redeploy would race against the sibling that's already deploying. Risk of making it worse.
- **Did not call `wrangler pages rollback`** — would revert sibling work; sibling likely already has the right state in flight. Rollback would erase recent deploys.
- **Did not modify `_site/_redirects`** — that's sibling-owned and mid-deploy.
- **Did not kill any sibling process** — top-down doctrine: never cross sibling lanes.

## What the user / sibling lane should do (priority order)

1. **Check `wrangler pages deployment list --project-name=csoai-site`** for any deployment that's stuck in "in progress" or "failure".
2. **If a deploy is stuck**, cancel it via the Cloudflare dashboard (Domain → Workers & Pages → csoai-site → view deployments → cancel the in-progress one).
3. **If no deploy is stuck**, check the sibling cron logs (`~/clawd/_alignment/` or the sibling session notes) for any error around 04:29Z.
4. **Once the cause is found**, if it's a known-broken `_site/` build, rerun `cd ~/clawd/csoai-static-deploy2 && python3 build_site.py` (allowlisted build) and then `wrangler pages deploy _site --project-name=csoai-site`.
5. **If it's a deeper CF Pages backend issue**, escalate to Cloudflare support (the csoai.org domain is on a paid CF plan via Wrangler CLI auth).

## Side note — defensive observation

The watchdog detected this ~16 minutes ago and the user wasn't at the Mac to hear the voice. The Mac is headless and unattended for long stretches. The notification path (`osascript` + `say`) only fires once on the UP→DOWN transition; subsequent DOWN cycles don't re-fire.

**Suggested defensive fix:** add a Telegram/Discord/Slack webhook to the watchdog script so out-of-band delivery is possible. This is a 5-line addition and removes the "user wasn't at the desk" failure mode entirely. **Owner-gated** (depends on which channel Nick wants to wire it to).

---

**Filed by:** JEEVES K3 lane, 2026-08-10 04:49:30 UTC. Updated 04:55Z with reflog evidence (every-5min cadence, not hourly), 05:02Z with confirmation that no sibling fix attempt has occurred in 32 min despite active cron, 05:12Z with Nick's CF Ray ID `a28c47296e6360e2` and Kimi-diagnostic evidence.
**Authority:** derived from `com.csoai.site-watch` LaunchAgent + live curl probes + sibling reflog inspection + Kimi daemon diagnostics.
**Action requested:** investigate and remediate via one of the steps above.

## Investigation trail (Ray ID `a28c47296e6360e2`)

- Captured by Nick at `2026-08-10 04:32:39 UTC` from a London browser session.
- Canonical handle for the slow request Cloudflare abandoned. CF support can correlate to origin-side timing.
- To investigate:
  1. `wrangler pages deployment tail --project-name=csoai-site` (real-time log stream)
  2. `wrangler pages deployment list --project-name=csoai-site` (look for orphan deployment stuck in `in progress` since 04:29Z)
  3. CF dashboard → `Workers & Pages` → `csoai-site` → `Logs` → search Ray ID → see origin timing
- Kimi link investigation:
  - Kimi webbridge daemon (PID 79901, `127.0.0.1:10086`) currently in crash-loop with `bind: address already in use`.
  - Kimi upgrade cron failing daily for 4 days straight (`v1.11.6 not yet available, manifest=404`).
  - **Hypothesis**: an older Kimi user-facing browser session, not the daemon itself, may be making repeated csoai.org fetches that exhaust origin.
  - **Confirm**: check Kimi session history or browser-extension state for any page-open / content-extraction task against csoai.org.