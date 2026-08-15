#!/usr/bin/env python3
"""greenfield_eater_fast.py — concurrent version using BrowserContext parallel pages.

Scales to hundreds/thousands of sites by reusing a single Chrome context.
Default: 8 parallel pages.
"""
from __future__ import annotations

import argparse, asyncio, json, sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed")
    sys.exit(1)

HERE = Path(__file__).resolve().parent
OUT = HERE / "benchmark-results" / "greenfield_eater"
OUT.mkdir(parents=True, exist_ok=True)

PREDICATES = [
    "cookie_consent", "provenance_marking", "human_oversight",
    "data_transparency", "ai_disclosure",
]


async def test_site(context, url: str) -> dict:
    result = {
        "url": url, "tested_at": datetime.now(timezone.utc).isoformat(),
        "predicates": {}, "score": 0, "passed": 0, "failed": 0,
    }
    page = await context.new_page()
    try:
        page.set_default_timeout(15000)
        resp = await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        result["http_status"] = resp.status if resp else None
        result["page_title"] = await page.title()
        body_text = ""
        try:
            body_text = await page.inner_text("body", timeout=5000)
            body_text = body_text[:30000]
        except Exception:
            pass

        # Cookie consent
        try:
            cookie_found = False
            for sel in ["button:has-text('Accept')", "[id*='cookie']", "[class*='cookie']", "[id*='consent']"]:
                try:
                    if await page.locator(sel).count() > 0:
                        cookie_found = True; break
                except Exception: pass
            result["predicates"]["cookie_consent"] = {"passed": cookie_found}
        except Exception:
            result["predicates"]["cookie_consent"] = {"passed": False}

        # C2PA / provenance
        c2pa_found = "C2PA" in body_text or "provenance" in body_text.lower()
        result["predicates"]["provenance_marking"] = {"passed": c2pa_found}

        # Human oversight
        oversight_found = any(p in body_text.lower() for p in ["human oversight", "human review", "human-in-the-loop"])
        result["predicates"]["human_oversight"] = {"passed": oversight_found}

        # Privacy policy
        privacy_found = False
        for sel in ["a:has-text('Privacy')", "a[href*='privacy']"]:
            try:
                if await page.locator(sel).count() > 0:
                    privacy_found = True; break
            except Exception: pass
        result["predicates"]["data_transparency"] = {"passed": privacy_found}

        # AI disclosure
        ai_found = any(p in body_text.lower() for p in ["ai-powered", "powered by ai", "uses ai", "machine learning", "automated decision"])
        result["predicates"]["ai_disclosure"] = {"passed": ai_found}

        for p in result["predicates"].values():
            if p.get("passed"): result["passed"] += 1
            else: result["failed"] += 1
        result["score"] = round(100 * result["passed"] / len(PREDICATES), 1)

    except Exception as e:
        result["error"] = str(e)[:200]
    finally:
        await page.close()
    return result


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sites", required=True, help="File with URLs")
    ap.add_argument("--limit", type=int, default=500)
    ap.add_argument("--parallel", type=int, default=8)
    args = ap.parse_args()

    sites = []
    with open(args.sites) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                sites.append(line)
    sites = sites[:args.limit]
    print(f"Fast Eater — {len(sites)} sites, {args.parallel} parallel")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )

        # Chunk sites for parallel execution
        results = []
        chunks = [sites[i:i+args.parallel] for i in range(0, len(sites), args.parallel)]
        for ci, chunk in enumerate(chunks):
            tasks = [test_site(context, url) for url in chunk]
            chunk_results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in chunk_results:
                if isinstance(r, dict):
                    results.append(r)
                    if "error" in r:
                        print(f"  [{len(results)}/{len(sites)}] {r['url'][:40]:40s}  ERROR: {r['error'][:50]}")
                    else:
                        print(f"  [{len(results)}/{len(sites)}] {r['url'][:40]:40s}  {r['score']}%")
            print(f"  --- chunk {ci+1}/{len(chunks)} done ---")

        await browser.close()

    summary = {
        "tested_at": datetime.now(timezone.utc).isoformat(),
        "n_sites": len(sites),
        "results": results,
        "summary": {
            "mean_score": round(sum(r.get("score", 0) for r in results) / len(results), 1) if results else 0,
            "total_passed": sum(r.get("passed", 0) for r in results),
            "total_failed": sum(r.get("failed", 0) for r in results),
        },
    }

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    (OUT / f"site_results_{ts}.json").write_text(json.dumps(summary, indent=2))
    (OUT / "latest.json").write_text(json.dumps(summary, indent=2))
    print(f"\n=== RESULTS ===")
    print(f"  Sites: {len(sites)}")
    print(f"  Mean score: {summary['summary']['mean_score']}%")
    print(f"  Total passed: {summary['summary']['total_passed']}")
    print(f"  Total failed: {summary['summary']['total_failed']}")


if __name__ == "__main__":
    asyncio.run(main())