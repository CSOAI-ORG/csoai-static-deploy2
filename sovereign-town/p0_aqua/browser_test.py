"""
Browser-level end-to-end tests for the Sovereign Town dashboard surface.

Requires Playwright and the local services to be running:
    dashboard (:3940), harness (:3941), mcp sse (:3942)

Run:
    cd p0_aqua
    source .venv-playwright/bin/activate
    pytest browser_test.py --headed       # visible browser
    pytest browser_test.py                # headless (default)
"""
from __future__ import annotations

import os
import urllib.request

import pytest
from playwright.sync_api import expect

BASE = os.environ.get("SOV_TOWN_URL", "http://127.0.0.1:3940")


def _services_alive() -> bool:
    """Quick probe: dashboard + harness + mcp sse must answer."""
    try:
        for path in ("/api/health", "/harness/health", "/mcp/sse"):
            req = urllib.request.Request(BASE + path, method="GET")
            if path == "/mcp/sse":
                # SSE endpoint is a long-lived stream; just check it accepts the connection.
                req = urllib.request.Request(BASE + path, method="HEAD")
            with urllib.request.urlopen(req, timeout=3) as r:
                if r.status not in (200, 405):
                    return False
        return True
    except Exception:
        return False


@pytest.fixture(scope="session", autouse=True)
def skip_if_services_down():
    if not _services_alive():
        pytest.skip("Sovereign Town services are not all running (dashboard :3940, harness :3941, mcp sse :3942)")


def test_dashboard_nav(page):
    """Dashboard nav links reach Workbench and Leaderboard."""
    page.goto(BASE + "/dashboard")
    page.locator("nav a[href='/workbench']").click()
    page.wait_for_url("**/workbench")
    expect(page.locator("h1")).to_contain_text("Regulatory Workbench")

    page.goto(BASE + "/dashboard")
    page.locator("nav a[href='/leaderboard']").click()
    page.wait_for_url("**/leaderboard")
    expect(page.locator("h1")).to_contain_text("Public Benchmark Leaderboard")


def test_workbench_mcp_client(page):
    """The embedded MCP client can connect, list tools, and call one."""
    page.goto(BASE + "/workbench")
    expect(page.locator("#mcp-client-panel")).to_be_visible()

    # Scroll the MCP panel into view so the click is reliable.
    page.locator("#mcp-client-panel").scroll_into_view_if_needed()
    page.locator("#mcp-connect").click()

    expect(page.locator("#mcp-status")).to_have_text("connected", timeout=15000)

    page.locator("#mcp-tool").select_option("sov_world_info")
    page.locator("#mcp-load-example").click()
    page.locator("#mcp-call").click()

    # The tool returns JSON containing the list of scenarios.
    expect(page.locator("#mcp-log")).to_contain_text("scenarios", timeout=15000)


def test_leaderboard_to_run_detail(page):
    """Public leaderboard loads signed runs and links to a human-readable detail page."""
    page.goto(BASE + "/leaderboard")
    # Wait for at least one row to appear.
    rows = page.locator("#board tbody tr")
    expect(rows).not_to_have_count(0, timeout=10000)

    link = page.locator("#board tbody tr:first-child td a").first
    href = link.get_attribute("href")
    assert href and href.startswith("/run.html?id="), f"unexpected run link: {href}"
    page.goto(BASE + href)
    expect(page.locator("h1")).to_contain_text("Run Detail")
    expect(page.locator(".badge")).to_be_visible()


def test_run_detail_invalid_id(page):
    """Missing/invalid run ids show a helpful error instead of a blank page."""
    page.goto(BASE + "/run.html?id=notarealid")
    expect(page.locator("#root")).to_contain_text("Run not found")


def test_town3d_loads(page):
    """The 3D town viewer renders a canvas."""
    page.goto(BASE + "/town3d")
    expect(page.locator("canvas").first).to_be_visible(timeout=10000)


