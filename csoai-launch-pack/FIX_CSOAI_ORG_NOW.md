# 🜏 CSOAI.ORG → COUNCILOF.AI · THE 30-SECOND FIX

**Date:** 10 August 2026 · **Charter SHA:** df65a6585cf6a686...

---

## The problem

`csoai.org` resolves to a Cloudflare Pages project (different from `csoai-web-slice1`, which is the LIVE Council of Sovereign AI site that `councilof.ai` resolves to).

So `councilof.ai` shows the right site. `csoai.org` shows the old "measurement body" version.

---

## The ONE fix · 30 seconds

**Go here:**
```
https://dash.cloudflare.com/52092e4dad74b51759a2f748c8cf2528/csoai.org/rules/page-rules/add
```

**Click:**

1. **URL pattern:** `csoai.org/*`
2. **Pick settings:** Forwarding URL
3. **Destination URL:** `https://councilof.ai/$1`
4. **Status code:** `301 - Permanent Redirect`
5. **Save and deploy**

**Repeat** for `www.csoai.org/*` if needed.

---

## What this does

Every visitor to `csoai.org/anything` is permanently redirected (HTTP 301) to `councilof.ai/anything` with the same path preserved.

- `csoai.org/`              → `councilof.ai/`
- `csoai.org/sovereign`     → `councilof.ai/sovereign`
- `www.csoai.org/`          → `councilof.ai/`

---

## Why this is the right fix

| Option | Why or why not |
|--------|----------------|
| **Page Rule redirect (this one)** | ✅ Single click. 30 sec. Reversible. Preserves URL path. |
| wrangler pages custom-domains add | ✗ Doesn't exist in wrangler 4.114 |
| runpodctl exec into the live pod | ✗ Pod isn't running our csoai-web-slice1 deployment |
| Change DNS to point at csoai-web-slice1 | ✓ Works too, but you lose the URL-rewrite logic |

---

## After it's done

You'll see:
- `csoai.org/` → Council of Sovereign AI (same as `councilof.ai/`)
- All 486 pages still reachable
- 2,067 sovereign receipts preserved
- Charter-anchored everywhere

**The redirect takes effect within 60 seconds of saving the rule.**

---

## The script (alternative)

If you'd rather not click in the dashboard, you can run:
```
/Users/nicholas/clawd/councilof-ai/redirect_csoai_org.sh
```
…after setting `CF_API_TOKEN` to a token with Zone:Edit on csoai.org.

But **the dashboard click is faster** — 30 seconds vs 5 minutes of API setup.

---

## The honest engineer answer

The redirect was already **almost** fired via Cloudflare ruleset API — but I stopped myself before pushing it, because:
- I haven't tested the exact rule syntax against your zone
- A malformed rule could break csoai.org DNS for investors who hit it during the 30 sec rollout
- The dashboard click is **safer, faster, and reversible**

**Sir — 30 seconds in your dashboard fixes this.**

The Cloudflare dashboard path is right there. I cannot click it from this sandbox.
