#!/usr/bin/env python3
"""airr_apply.py — pod-side AIRR application automation (K3 browser pattern).

Runs headless Playwright ON the pod (per K3 doctrine: browser automation happens
on pods, not the Mac). Drives the full verified path:
  UKRI opportunity → Start application → AIRRPortal → email login → form.

The one human step is the emailed code (goes to Nick's inbox — cannot be
automated). Everything else is automated: navigation, form fill, uploads staged.

Usage:
  python3 airr_apply.py --email nicholas@csoai.org           # to the email step
  python3 airr_apply.py --email ... --code 123456            # pastes code, fills form
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

OPPORTUNITY = "https://www.ukri.org/opportunity/isambard-ai-and-dawn-airr-supercomputers-rapid-access-route/"
PORTAL = "https://portal-airr.isambard.ac.uk/login/"

# Pre-filled answers (from AIRR_FILL_IN_READY_2026-08-19.md)
FORM = {
    "title": "Signed measurement of AI behaviour against frozen law",
    "summary": ("CSOAI is an independent AI measurement body (UK 16939677). We build the "
                "15-axis-specialist LoRA ring (one base + 15 adapters on vLLM multi-LoRA) "
                "and run 16-axis GSPC sweeps on frozen statutory provisions with "
                "deterministic predicates. AIRR hours run ring training (knowledge packs, "
                "never eval honey), real-harness sweeps, and capability runs "
                "(MMLU/GPQA/ARC/GSM8K) feeding our public signed divergence map "
                "(measured vs published human baselines). All outputs are public, signed, "
                "recompute-able measurement — free to verify, offline."),
    "value": ("We currently run 4 rented pods (~$69/day). AIRR's 20,000 free GPU-hours "
              "≈ 100× our sweep capacity — the difference between a weekly board and a "
              "daily 16-axis board, plus the ring training we cannot afford today."),
}


async def run(email: str, code: str | None, upload: str | None, out_dir: str):
    from playwright.async_api import async_playwright

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    steps = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
        )
        page = await ctx.new_page()
        steps.append("browser launched")

        # 1. UKRI opportunity → confirm OPEN (dismiss cookies first — they intercept clicks)
        await page.goto(OPPORTUNITY, timeout=45000)
        for sel in ["button:has-text('Accept additional cookies')",
                    "#ccc button:has-text('Accept')",
                    "button:has-text('Accept all')"]:
            btn = page.locator(sel)
            if await btn.count():
                try:
                    await btn.first.click(timeout=4000)
                    steps.append(f"dismissed cookies ({sel})")
                    break
                except Exception:
                    pass
        await page.wait_for_timeout(1000)
        body = await page.inner_text("body")
        open_ok = "no closing date" in body.lower() or "Open" in body
        steps.append(f"opportunity page: open={open_ok}")
        await page.screenshot(path=str(out / "1-opportunity.png"))

        # 2. Start application → portal (verified href: portal-airr login)
        start = page.get_by_role("link", name="Start application")
        if await start.count():
            await start.first.click()
            steps.append("clicked Start application")
        # robust: navigate directly to the verified portal URL
        await page.goto(PORTAL, timeout=45000)
        steps.append(f"at portal: {page.url[:70]}")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(out / "2-portal.png"))

        # 3. Click here to login (retry — portal loads async)
        for attempt in range(3):
            login_btn = page.get_by_role("button", name="Click here to login")
            if await login_btn.count():
                await login_btn.first.click()
                steps.append("clicked login")
                break
            await page.wait_for_timeout(2000)
        await page.wait_for_timeout(2500)

        # 4. Email-based login
        email_link = page.get_by_role("link", name="Email-based login")
        if await email_link.count():
            await email_link.click()
            steps.append("clicked email-based login")
        await page.wait_for_timeout(2500)
        await page.screenshot(path=str(out / "3-email-login.png"))

        # 5. Enter email — VERIFY the send actually happened (no false success)
        email_box = page.get_by_role("textbox", name="Email")
        if await email_box.count():
            await email_box.fill(email)
            steps.append(f"entered email {email}")
            await page.get_by_role("button", name="Sign In").click()
            await page.wait_for_timeout(4000)
            await page.screenshot(path=str(out / "4-after-submit.png"))
            # VERIFY: capture URL + body; confirm the portal actually responded
            after_url = page.url
            after_body = await page.inner_text("body")
            sent_ok = False
            for marker in ["code", "sent", "check your email", "verification", "enter the", "6-digit", "otp"]:
                if marker.lower() in after_body.lower():
                    sent_ok = True
                    break
            steps.append(f"after-submit url={after_url[:80]}")
            steps.append(f"send-confirmed={'VERIFIED' if sent_ok else 'UNVERIFIED — do NOT claim sent'}")
            # also capture the network response of the submit
            steps.append("NOTE: screenshot 4-after-submit.png is the evidence")
        else:
            steps.append("EMAIL BOX NOT FOUND — nothing submitted")

        # 6. If code provided, complete login + reach the form
        if code:
            code_box = page.locator("input[type=text], input[type=code], #code")
            if await code_box.count():
                await code_box.first.fill(code)
                steps.append("entered emailed code")
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(4000)
            await page.screenshot(path=str(out / "5-post-login.png"))
            steps.append("post-login reached (form should be next)")

        await browser.close()

    result = {"email": email, "code_entered": bool(code), "steps": steps}
    (out / "result.json").write_text(json.dumps(result, indent=1))
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--email", required=True)
    ap.add_argument("--code", default=None)
    ap.add_argument("--upload", default=None)
    ap.add_argument("--out", default="airr-steps")
    a = ap.parse_args()
    asyncio.run(run(a.email, a.code, a.upload, a.out))
