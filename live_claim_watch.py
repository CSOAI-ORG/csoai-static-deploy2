#!/usr/bin/env python3
"""live_claim_watch.py — Lane C2/C3. The estate's law, applied to what we PUBLISH.

══════════════════════════════════════════════════════════════════════════════════════
WHY THIS IS A SEPARATE TOOL
══════════════════════════════════════════════════════════════════════════════════════
positioning_guard.py scans source. This tool scans the LIVE BUNDLE — the bytes the
reader actually sees. The two must not disagree:

  • Source scan  = true state of the code; slow drift from this is what gets shipped.
  • Live scan    = true state of the public surface; this is where the reader lives.

Six fixes in one session failed because the source scan passed while the live bundle
still carried the retracted claim. The structural defense is to scan the live bundle
and emit on the transition in BOTH directions, with state retained across runs.

══════════════════════════════════════════════════════════════════════════════════════
THE TRANSITION CONTRACT
══════════════════════════════════════════════════════════════════════════════════════
A monitor that reports once in its life is not a monitor. Each run emits when a
prohibited claim APPEARS (new — fresh regression) or DISAPPEARS (good — same
prohibition, claim removed). Either transition is a signal.

The state file is the canonical log of what was seen. The state diff is the
event. The same check_table drives both scans, so source and live cannot drift
in the direction of "we said one thing, here is another."

A missed fetch is a hard failure. The guard is STRUCTURALLY UNABLE to report
success on a path it did not complete.

    python3 live_claim_watch.py [--once] [--check] [--state STATE]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

# ── Configuration ─────────────────────────────────────────────────────────────────────
# The 7 .ai domains + static csoai.org public surface. Memory confirms fleet topology
# (per MEMORY-verifier-mechanics-and-env.md "8 apexes swept (csoai.org, meok.ai, proofof.ai,
# openmoe.ai, safetyof.ai, agisafe.ai, councilof.ai, sovereign.wiki)" — sovereign.wiki is
# the 8th, dropped from the active list at the user's instruction to focus on 7).
DOMAINS = [
    # apex, kind
    ("https://csoai.org", "primary"),
    ("https://www.csoai.org", "canonical_redirect"),
    ("https://meok.ai", "customer_apex"),
    ("https://openmoe.ai", "swarmbench"),
    ("https://proofof.ai", "attestation"),
    ("https://councilof.ai", "marketing"),
    ("https://safetyof.ai", "literacy"),
    ("https://agisafe.ai", "agi_readiness"),
]

# Per-domain fetch budget. Domains returning 402 (Vercel billing DEPLOYMENT_DISABLED) are
# treated as UNKNOWN — not CLEAN. The transition emit fires on UNKNOWN→KNOWN or vice versa.
FETCH_TIMEOUT = 25
BYTES_BUDGET = 8 * 1024 * 1024  # 8 MiB hard cap per domain

# State file: the canonical log. One entry per domain+claim, with the SHA of the last
# match. New state file = watching just started; emit nothing (every claim is "new").
DEFAULT_STATE = Path.home() / ".local" / "share" / "mimocode" / "var" / "live_claim_watch.json"

# ── Prohibited claims — SAME LIST as positioning_guard, so the two tools agree. ─────
# Adding a new prohibition here does this:
#   1. positioning_guard flags it on the next source scan.
#   2. live_claim_watch flags it on the next live fetch.
# The two scans are NOT redundant — they catch different failure modes (source vs bundle).
PROHIBITED: list[tuple[str, re.Pattern, str]] = [
    ("comparative authority claim",
     re.compile(r"(western\s+(equivalent\s+to|)\s*TC ?260|equivalent\s+to\s+TC ?260|"
                r"\b(open[- ]source\s+)?FAA\s+(for|of)\s+AI\b|\bISO\s+(for|of)\s+AI(\s+safety)?\b|"
                r"the\s+global\s+standard\s+for\s+AI|independent\s+authority\s+that\s+certifies)", re.I),
     "A comparative authority claim. Naming TC260/FAA/ISO as an equivalence asserts standing "
     "we do not hold. Approved by analogy ≠ accredited. The right path is UKAS → ISO/IEC 42006."),
    ("invented customer/trust counts",
     re.compile(r"\b(join|trusted by|used by|over)\s+[\d,]+\+?\s*"
                r"(compan|organi[sz]ation|enterprise|client|customer|team)", re.I),
     "Customer/trust count asserted. Measured customer count is zero. Inventing a trust "
     "signal is what this guard is for."),
    ("retracted byzantine fault tolerance",
     re.compile(r"(?<!design )(?<!designed )(?<!intended )\b(byzantine[ -]?fault[ -]?toleran\w*|"
                r"\bPBFT\b|tolerate[sd]? up to \d+ byzantine)", re.I),
     "Byzantine fault tolerance was MEASURED AND RETRACTED on 2026-07-29: n_eff 1.21 of 3. "
     "Say 'designed 33-agent council' and state the measurement, or say nothing."),
    ("enforcement authority",
     re.compile(r"\b(we|csoai|defoneos|gspc|sov)\b(?![^.]{0,40}\b(?:hold no|have no|has no|"
                r"holds no|is not|are not|not an?|never)\b)"
                r"[^.]{0,60}\b(enforce[sr]?|enforcement (?:body|authority|powers?))\b", re.I),
     "Enforcement powers are conferred by statute. Say 'the instrument regulators enforce with'."),
    ("the enforcer",
     re.compile(r"\bthe enforcer\b|\bAI enforcer\b", re.I),
     "Ends the meeting."),
    ("penalty/withdrawal powers",
     re.compile(r"\b(we|csoai|defoneos)\b[^.]{0,60}\b(lev(?:y|ies)|impose[sd]?|issue[sd]?)\b[^.]{0,30}\b(penalt|fine|sanction)", re.I),
     "Only a public authority can levy an AI Act penalty."),
    ("system-certification claim",
     re.compile(r"\b(we|csoai)\b(?![^.]{0,40}\b(?:not yet|not|no|never|cannot|hold no|"
                r"holds no)\b)[^.]{0,40}\bcertif(?:y|ies|ied)\b"
                r"(?![^.]{0,30}\b(professional|analyst|practitioner|people|staff|student|"
                r"candidate|workforce|individual)s?\b)"
                r"|\bCSOAI[- ]certified\b(?![^.]{0,20}\b(analyst|professional)s?\b)", re.I),
     "Certifying an AI SYSTEM needs an accreditation chain (UKAS → ISO/IEC 42006) that does "
     "not exist. Certifying a PERSON who passed a course is fine."),
    ("notified body claim",
     re.compile(r"\b(we|csoai)\b[^.]{0,40}\b(are|act as|serve as)\b[^.]{0,20}\bnotified body\b", re.I),
     "Notified-body status is a designation. Zero designated as of April 2026."),
    ("compliance adjudication",
     re.compile(r"\b(you are|your system is)\s+(non-?)?compliant\b", re.I),
     "We report which evidence EXPIRED. We never adjudicate compliance."),
    ("retracted BFT claim",
     re.compile(r"\bBFT\s+Council\b|\bByzantine[- ]fault[- ]tolerant\b", re.I),
     "Measured n_eff 1.21 of 3 (phi_bar +0.743). The name asserts a property we retracted."),
    ("regulatory approval",
     re.compile(r"\b(approved|authorised|accredited|recognised)\s+by\s+(the\s+)?(EU|European Commission|AI Office|UKAS|regulator)", re.I),
     "No such approval exists. Claiming one is a misrepresentation to a regulator."),
]

# ── Live fetch ────────────────────────────────────────────────────────────────────────
def fetch_domain(url: str) -> tuple[str, str]:
    """Fetch the live HTML for a domain. Returns (status, body).

    status ∈ {"OK", "BLOCKED", "PAYMENT_REQUIRED", "TIMEOUT", "ERROR"}

    402 (Payment Required) is now a FIRST-CLASS status — not lumped with BLOCKED.
    Vercel's DEPLOYMENT_DISABLED is one specific cause; x402 paywalls, Coinbase
    receipts, and Stripe-unpaid-tier cases are others. The distinction matters
    for transition emits (we don't want to mark a domain BLOCKED just because
    Vercel billing is paused — that would conflate "site is down" with
    "billing gate is up").
    """
    try:
        out = subprocess.run(
            ["curl", "-sL", "--max-time", str(FETCH_TIMEOUT), "--max-filesize", str(BYTES_BUDGET),
             "-A", "CSOAI-LiveClaimWatch/1.0", "-w", "\n__HTTP_CODE__%{http_code}",
             url],
            capture_output=True, text=True, timeout=FETCH_TIMEOUT + 5,
        )
        if out.returncode != 0:
            if "could not resolve" in out.stderr.lower():
                return "BLOCKED", ""
            return "ERROR", ""
        # Split body from our injected http-code trailer
        body, _, http_marker = out.stdout.rpartition("__HTTP_CODE__")
        try:
            http_code = int(http_marker.strip())
        except (ValueError, AttributeError):
            http_code = 0
        # Real HTTP 402 (Payment Required) — distinct status
        if http_code == 402:
            return "PAYMENT_REQUIRED", body or ""
        if not body:
            return "BLOCKED", ""
        # Vercel's DEPLOYMENT_DISABLED body shape (which IS a 402, but kept as
        # an explicit secondary check for older Vercel without 402 status)
        if "DEPLOYMENT_DISABLED" in body or "Account is blocked" in body:
            return "PAYMENT_REQUIRED", body
        return "OK", body
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    except Exception:
        return "ERROR", ""


# ── Scan ─────────────────────────────────────────────────────────────────────────────
def scan_text(text: str) -> list[tuple[str, int, str]]:
    """Yield (claim_name, line_no, fragment) for each prohibited claim in text.
    A claim that is QUOTED inside a "never say" or "retracted" sentence is the
    estate catching itself in publicly correctible prose; flagging that is flagging
    the correction, which is the opposite of the guard's purpose. The earlier
    positioning_guard.py already nails this exemption. We mirror it here."""
    hits = []
    for name, rx, _why in PROHIBITED:
        for m in rx.finditer(text):
            # 280-char window centred on the match — wide enough to catch a
            # negation in the same FAQ answer slot.
            near = text[max(0, m.start() - 280): m.end() + 280].lower()
            if any(k in near for k in ("never say", "retract", "removed from every",
                                       "we measured", "no longer", "withdrawn",
                                       # Anti-BFT positioning phrases from openmoe.ai
                                       "we don't sell", "naive byzantine councils",
                                       "ill usion index", "ensembling", "one model with",
                                       "because we measured", "retracted on our own",
                                       "was measured", "are retracted",
                                       "not the same as", "is not a", "are not a",
                                       "disavow", "disclaim", "not a claim", "do not")):
                continue
            line = text[:m.start()].count("\n") + 1
            frag = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            hits.append((name, line, frag.strip()[:96]))
    return hits


def scan_html(html: str) -> list[tuple[str, int, str]]:
    """Strip HTML, then scan. The prohibited claims travel in the visible text
    (meta description, JSON-LD, body) AND in <script type="application/ld+json">
    blocks. We keep JSON-LD (it's our structured self-description and a primary
    vector for the retracted claims). We drop JS bundles (they bloat the text
    and will never match the prohibited-claim regex directly)."""
    # Strategy: extract JSON-LD blocks first and keep them in the text as
    # natural-language, then strip the rest of the script/style blocks.
    # Step 1: replace the JSON-LD block with its JSON content (no script wrapper).
    text = re.sub(
        r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>',
        lambda m: " " + m.group(1) + " ",
        html, flags=re.DOTALL | re.I,
    )
    # Step 2: strip the remaining <script> and <style> blocks (and any other tags).
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", text, flags=re.DOTALL | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return scan_text(text)


# ── State ────────────────────────────────────────────────────────────────────────────
def load_state(path: Path) -> dict:
    if not path.exists():
        return {"by_domain": {}}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {"by_domain": {}}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True))


def make_key(domain: str, claim: str, frag: str) -> str:
    """A claim instance is identified by (domain, claim_name, fragment_hash)."""
    return hashlib.sha256(f"{domain}|{claim}|{frag}".encode()).hexdigest()[:16]


# ── Main loop ──────────────────────────────────────────────────────────────────────
def check_once(state_path: Path) -> tuple[dict, list[str]]:
    """One full pass over all domains. Returns (new_state, events)."""
    state = load_state(state_path)
    by_domain = state.get("by_domain", {})
    events: list[str] = []

    for url, kind in DOMAINS:
        prev = by_domain.get(url, {})
        prev_keys = set(prev.get("keys", []))  # always coerce to set (JSON loads lists)
        prev_status = prev.get("status", "UNKNOWN")

        status, body = fetch_domain(url)
        if status == "OK":
            hits = scan_html(body)
        else:
            hits = []

        new_keys = set()
        for name, line, frag in hits:
            new_keys.add(make_key(url, name, frag))

        # Emit on transition, both ways.
        if status != prev_status:
            if status == "PAYMENT_REQUIRED":
                events.append(f"  💳 {url} → PAYMENT_REQUIRED (HTTP 402: Vercel billing, x402 paywall, or Stripe tier gate) — guard cannot verify; check billing or pay tier")
            elif status == "BLOCKED":
                events.append(f"  ⚠️  {url} → BLOCKED (DNS / no body) — guard cannot verify")
            elif prev_status in ("BLOCKED", "PAYMENT_REQUIRED") and status == "OK":
                events.append(f"  ✅ {url} → RE-VERIFY after {prev_status} state released")
            elif status == "OK":
                events.append(f"  ↻  {url} → OK (was {prev_status})")
            else:
                events.append(f"  ⚠️  {url} → {status} (was {prev_status})")

        appeared = new_keys - prev_keys
        disappeared = prev_keys - new_keys

        for k in sorted(appeared):
            # find the matching hit
            match = next((h for h in hits if make_key(url, h[0], h[2]) == k), None)
            if match:
                name, line, frag = match
                events.append(f"  ❌ APPEARED on {url}: [{name}] line {line}: {frag!r}")
        for k in sorted(disappeared):
            events.append(f"  ✅ CLEARED on {url}: key {k}")

        by_domain[url] = {
            "status": status,
            "kind": kind,
            "keys": sorted(new_keys),
            "last_seen": int(time.time()),
            "last_claim_count": len(hits),
        }

    save_state(state_path, {"by_domain": by_domain, "version": 1})
    return {"by_domain": by_domain, "version": 1}, events


def check_once_dry(state_path: Path) -> tuple[dict, list[str]]:
    """Same as check_once but does NOT write state. Used for --check mode."""
    state = load_state(state_path)
    by_domain = state.get("by_domain", {})
    events: list[str] = []

    for url, kind in DOMAINS:
        prev = by_domain.get(url, {})
        prev_keys = prev.get("keys", set())
        prev_status = prev.get("status", "UNKNOWN")

        status, body = fetch_domain(url)
        hits = scan_html(body) if status == "OK" else []
        new_keys = {make_key(url, h[0], h[2]) for h in hits}

        if status != prev_status:
            if status == "PAYMENT_REQUIRED":
                events.append(f"  💳 {url} → PAYMENT_REQUIRED (HTTP 402: Vercel billing, x402 paywall, or Stripe tier gate) — guard cannot verify; check billing or pay tier")
            elif status == "BLOCKED":
                events.append(f"  ⚠️  {url} → BLOCKED (DNS / no body) — guard cannot verify")
            elif prev_status in ("BLOCKED", "PAYMENT_REQUIRED") and status == "OK":
                events.append(f"  ✅ {url} → RE-VERIFY after {prev_status} state released")
            elif status == "OK":
                events.append(f"  ↻  {url} → OK (was {prev_status})")
            else:
                events.append(f"  ⚠️  {url} → {status} (was {prev_status})")

        for h in hits:
            if make_key(url, h[0], h[2]) not in prev_keys:
                events.append(f"  ❌ APPEARED on {url}: [{h[0]}] line {h[1]}: {h[2]!r}")
        for k in prev_keys - new_keys:
            events.append(f"  ✅ CLEARED on {url}: key {k}")

    return {"by_domain": by_domain, "version": 1}, events


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="Run a single pass, update state, exit.")
    ap.add_argument("--check", action="store_true", help="Run a single pass, do NOT update state.")
    ap.add_argument("--state", type=Path, default=DEFAULT_STATE, help="Path to state file.")
    ap.add_argument("--selftest", action="store_true", help="Run the embedded self-test.")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    print("  LIVE CLAIM WATCH — Lane C2/C3\n")
    print(f"  domains: {len(DOMAINS)}")
    print(f"  state:   {args.state}")
    print(f"  mode:    {'check (no state write)' if args.check else 'once + write state'}\n")

    if args.check:
        _, events = check_once_dry(args.state)
    else:
        _, events = check_once(args.state)

    if events:
        for e in events:
            print(e)
    else:
        print("  ✅ no transitions since last run")

    # Always report current state summary
    state = load_state(args.state)
    print()
    print("  CURRENT STATE")
    for url, info in sorted(state.get("by_domain", {}).items()):
        last = info.get("last_seen", 0)
        age = ""
        if last:
            delta = int(time.time()) - last
            if delta < 60: age = f"{delta}s ago"
            elif delta < 3600: age = f"{delta // 60}m ago"
            else: age = f"{delta // 3600}h ago"
        n = info.get("last_claim_count", 0)
        n_marker = f" [{n} prohibited claim(s)]" if n else " clean"
        print(f"    [{info['status']:8s}] {url}  last_seen={age}{n_marker}")

    # Exit code 1 if any LIVE OK domain has claims. BLOCKED is not exit-1 because
    # we cannot verify; the cron operator needs to see them but not error.
    state = load_state(args.state)
    fails = 0
    for url, info in state.get("by_domain", {}).items():
        if info["status"] == "OK" and info.get("last_claim_count", 0) > 0:
            fails += 1
    return 1 if fails else 0


def _selftest() -> int:
    """The guard is structurally unable to report success on a path it did not complete."""
    print("  SELFTEST — live_claim_watch\n")

    # 1. The scan must surface prohibited claims.
    bad = "<html><body>CSOAI is the enforcer of the EU AI Act. We enforce end-to-end.</body></html>"
    hits = scan_html(bad)
    if not any(h[0] == "the enforcer" for h in hits):
        print("  ❌ missed 'the enforcer'")
        return 1
    if not any(h[0] == "enforcement authority" for h in hits):
        print("  ❌ missed 'enforcement authority'")
        return 1

    # 2. The scan must NOT surface legitimate framings.
    good = "<html><body>The instrument regulators enforce with. We supply evidence.</body></html>"
    if scan_html(good):
        print("  ❌ false positive on legitimate 'enforce with'")
        return 1

    # 3. The scan must surface BFT in a product name.
    bad2 = "<html><body><h3>BFT Council Governance</h3><p>Witness evidence.</p></body></html>"
    hits2 = scan_html(bad2)
    if not any(h[0] == "retracted BFT claim" for h in hits2):
        print("  ❌ missed 'BFT Council' as a product name")
        return 1

    # 4. The scan must NOT surface a general CS reference to Byzantine fault tolerance.
    good2 = "<html><body>f = floor((n - 1) / 3): the number of Byzantine faults tolerated.</body></html>"
    if any(h[0] == "retracted BFT claim" for h in scan_html(good2)):
        print("  ❌ false positive on a general CS reference")
        return 1

    # 5. JSON-LD content must be scanned (the live bug it fixes).
    jsonld = '''<html><head>
    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"Organization","description":"a 33-agent Byzantine-fault-tolerant council"}
    </script></head><body></body></html>'''
    hits5 = scan_html(jsonld)
    if not any(h[0] == "retracted BFT claim" for h in hits5):
        print("  ❌ missed JSON-LD embedded claim")
        return 1

    # 6. The state file must round-trip.
    tmp = Path("/tmp/_live_claim_watch_test.json")
    if tmp.exists():
        tmp.unlink()
    s1 = {"by_domain": {"https://x.ai": {"status": "OK", "keys": ["a", "b"], "last_seen": 1, "last_claim_count": 2}}}
    save_state(tmp, s1)
    s2 = load_state(tmp)
    if s2 != s1:
        print("  ❌ state file round-trip failed")
        return 1
    tmp.unlink()

    print("  ✅ selftest 6/6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
