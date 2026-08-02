#!/usr/bin/env python3
"""greenfield_eater.py — test N sites via Chrome automation for compliance with EU AI Act.

Uses Playwright with real Chrome to test how each site handles:
  1. Cookie consent (GDPR)
  2. AI Act Article 50 (provenance markings)
  3. Article 14 (human oversight disclosure)
  4. Article 5 (prohibited practices disclosure)
  5. Data provenance transparency

Results are deterministic predicates, not LLM judgements.
Writes to benchmark-results/greenfield_eater/site_results.json.

Usage:
  python3 greenfield_eater.py --sites sites.txt
  python3 greenfield_eater.py --target https://example.com,https://foo.com
"""
from __future__ import annotations

import argparse, hashlib, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright not installed. pip3 install playwright")
    sys.exit(1)

HERE = Path(__file__).resolve().parent
OUT = HERE / "benchmark-results" / "greenfield_eater"
OUT.mkdir(parents=True, exist_ok=True)

# Greenfield CSOAI compliance predicates
PREDICATES = [
    {
        "id": "cookie_consent",
        "name": "Cookie consent (GDPR Art 7)",
        "predicate": "cookie_banner_present",
        "test": "Find cookie consent banner; reject=true if no dismiss option",
    },
    {
        "id": "provenance_marking",
        "name": "AI provenance (Art 50)",
        "predicate": "c2pa_metadata",
        "test": "Check for C2PA markers or provenance disclosure",
    },
    {
        "id": "human_oversight",
        "name": "Human oversight (Art 14)",
        "predicate": "human_review_disclosure",
        "test": "Check for human review / oversight disclosure",
    },
    {
        "id": "data_transparency",
        "name": "Data transparency (GDPR)",
        "predicate": "privacy_policy_present",
        "test": "Privacy policy URL accessible",
    },
    {
        "id": "ai_disclosure",
        "name": "AI system disclosure",
        "predicate": "ai_use_disclosure",
        "test": "Disclose AI systems in use (Art 50)",
    },
]


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def test_site(page, url: str) -> dict:
    """Run all predicates against a single site. Deterministic predicates only."""
    result = {
        "url": url,
        "tested_at": datetime.now(timezone.utc).isoformat(),
        "predicates": {},
        "score": 0,
        "passed": 0,
        "failed": 0,
    }

    try:
        resp = page.goto(url, timeout=30000, wait_until="domcontentloaded")
        result["http_status"] = resp.status if resp else None
        result["page_title"] = page.title()
        body_text = page.inner_text("body")[:50000] if page.locator("body").count() > 0 else ""

        # Predicate 1: Cookie consent
        try:
            cookie_selectors = [
                "button:has-text('Accept')", "button:has-text('Agree')",
                "[id*='cookie']", "[class*='cookie']", "[id*='consent']",
                "div[id*='gdpr']", "div[class*='consent']",
            ]
            cookie_found = False
            for sel in cookie_selectors:
                try:
                    if page.locator(sel).count() > 0:
                        cookie_found = True
                        break
                except Exception:
                    pass
            result["predicates"]["cookie_consent"] = {
                "present": cookie_found,
                "passed": cookie_found,
            }
        except Exception as e:
            result["predicates"]["cookie_consent"] = {"error": str(e), "passed": False}

        # Predicate 2: C2PA / provenance markers
        try:
            c2pa_selectors = [
                "meta[name*='c2pa']", "meta[name*='provenance']",
                "[itemtype*='c2pa']", "[class*='provenance']",
                "img[c2pa]", "img[data-c2pa]",
            ]
            c2pa_found = any(page.locator(sel).count() > 0 for sel in c2pa_selectors)
            text_check = "C2PA" in body_text or "provenance" in body_text.lower()
            result["predicates"]["provenance_marking"] = {
                "present": c2pa_found or text_check,
                "passed": c2pa_found or text_check,
            }
        except Exception as e:
            result["predicates"]["provenance_marking"] = {"error": str(e), "passed": False}

        # Predicate 3: Human oversight disclosure
        try:
            oversight_patterns = ["human oversight", "human review", "human-in-the-loop", "manual review"]
            oversight_found = any(p in body_text.lower() for p in oversight_patterns)
            result["predicates"]["human_oversight"] = {
                "present": oversight_found,
                "passed": oversight_found,
            }
        except Exception as e:
            result["predicates"]["human_oversight"] = {"error": str(e), "passed": False}

        # Predicate 4: Privacy policy
        try:
            privacy_selectors = [
                "a:has-text('Privacy')", "a:has-text('privacy policy')",
                "a[href*='privacy']", "a[href*='PrivacyPolicy']",
            ]
            privacy_found = any(page.locator(sel).count() > 0 for sel in privacy_selectors)
            result["predicates"]["data_transparency"] = {
                "present": privacy_found,
                "passed": privacy_found,
            }
        except Exception as e:
            result["predicates"]["data_transparency"] = {"error": str(e), "passed": False}

        # Predicate 5: AI disclosure
        try:
            ai_patterns = ["ai-powered", "powered by ai", "uses ai", "machine learning", "automated decision"]
            ai_found = any(p in body_text.lower() for p in ai_patterns)
            result["predicates"]["ai_disclosure"] = {
                "present": ai_found,
                "passed": ai_found,
            }
        except Exception as e:
            result["predicates"]["ai_disclosure"] = {"error": str(e), "passed": False}

        # Compute score
        for pred_id, pred in result["predicates"].items():
            if pred.get("passed"):
                result["passed"] += 1
            else:
                result["failed"] += 1
        result["score"] = round(100 * result["passed"] / len(PREDICATES), 1)

    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    ap = argparse.ArgumentParser(description="Greenfield site eater — Chrome automation")
    ap.add_argument("--target", help="Comma-separated URLs")
    ap.add_argument("--sites", help="File with one URL per line")
    ap.add_argument("--limit", type=int, default=20, help="Max sites to test")
    args = ap.parse_args()

    sites = []
    if args.target:
        sites = [s.strip() for s in args.target.split(",") if s.strip()]
    elif args.sites:
        sites = [s.strip() for s in Path(args.sites).read_text().splitlines() if s.strip()]
    else:
        # Default: CSOAI ecosystem sites
        sites = [
            "https://www.csoai.org",
            "https://councilof.ai",
            "https://www.bsigroup.com",
            "https://www.npl.co.uk",
            "https://arxiv.org",
            "https://eur-lex.europa.eu",
            "https://www.legislation.gov.uk",
            "https://c2pa.org",
            "https://digital-strategy.ec.europa.eu",
            "https://www.iso.org",
        ]
    sites = sites[:args.limit]

    print(f"Greenfield Eater — {len(sites)} sites")
    print(f"Chrome: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    print(f"Output: {OUT}")
    print()

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )

        for i, url in enumerate(sites):
            print(f"[{i+1}/{len(sites)}] {url}")
            page = context.new_page()
            try:
                result = test_site(page, url)
                results.append(result)
                print(f"  score: {result.get('score', 0)}% ({result.get('passed', 0)}/{len(PREDICATES)} passed)")
                if "error" in result:
                    print(f"  error: {result['error'][:100]}")
            finally:
                page.close()

        browser.close()

    # Write results
    summary = {
        "tested_at": datetime.now(timezone.utc).isoformat(),
        "n_sites": len(sites),
        "predicates": [p["id"] for p in PREDICATES],
        "results": results,
        "summary": {
            "mean_score": round(sum(r.get("score", 0) for r in results) / len(results), 1) if results else 0,
            "total_passed": sum(r.get("passed", 0) for r in results),
            "total_failed": sum(r.get("failed", 0) for r in results),
        },
    }

    out_path = OUT / f"site_results_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print()
    print(f"=== RESULTS ===")
    print(f"  Sites tested: {len(sites)}")
    print(f"  Mean score: {summary['summary']['mean_score']}%")
    print(f"  Total passed: {summary['summary']['total_passed']}")
    print(f"  Total failed: {summary['summary']['total_failed']}")
    print(f"  Written: {out_path}")

    # Also write the latest path
    (OUT / "latest.json").write_text(json.dumps(summary, indent=2))
    print(f"  Latest:    {OUT / 'latest.json'}")


if __name__ == "__main__":
    main()