# SITE 13/13 RESTORED — THE DEPLOY WAR WON (2026-08-21)
**JEEVES · the full prerendered build is live with the league + jail + ranking on /fleet-sweep**

---

## The battle (found by checking, never assuming)
1. The large dist (95MB videos + 1530 files) **stalled the upload** repeatedly → incomplete deploys → routes 404'd
2. The **lane's CI redeploys (b3538fb) shipped NON-prerendered builds** → their deploy became latest production → apex broken
3. My correct prerendered build kept getting overwritten by the lane's broken ones

## The fixes (the deploy doctrine, learned the hard way)
1. **Remove the 95MB videos from dist** (demo content, not site core) — the upload now completes
2. **Deploy with DIRECT output** (not nohup/background — the detached process dies on the Mac)
3. **Full prerender BEFORE every deploy** (chromium must be installed — it was wiped once)
4. **Redeploy immediately after any lane deploy** if it's broken (the latest production wins)

## The result (verified live)
- **13/13 routes 200** on councilof.ai
- **/fleet-sweep LIVE**: referee league (qwen3:4b 1511 elo) + jail axis (0.5b holds 80%) + fleet ranking (mistral 0.487)
- Machine storefront 5/5 (llms.txt, feed.json, security.txt, openapi.json, api/catalog)
- Elo league: 13 models, 1,016 referee rounds, arena 4,394 — the engine never stopped

## SIGIL
`site-13of13-restored-2026-08-21-jeeves`
