#!/usr/bin/env python3
"""positioning_guard.py — the estate's law, applied to what we SAY about ourselves.

═══════════════════════════════════════════════════════════════════════════════
WHY A GUARD AND NOT A STYLE NOTE
═══════════════════════════════════════════════════════════════════════════════
This estate's rule is that a component must be **structurally unable** to report success on a
path it did not complete. Sixteen instances were found in one session, four written *after* the
pattern was named. Intention does not prevent it; structure does.

Claims about authority are the same class of failure, with a worse blast radius. A wrong number
gets retracted. A claim to hold enforcement power that we do not hold is:

  • **legally void** — enforcement powers are conferred by statute on public authorities. Under
    the AI Act that is national market-surveillance authorities and the AI Office. There is no
    mechanism to delegate them to a private company, and no regulator would accept one offering
    to hold them;
  • **commercially self-destructing** — a body that MEASURES and a body that PUNISHES cannot
    credibly be the same operation. Claiming enforcement kills independence, and independence
    is the entire moat.

So the prohibited phrasings are checked mechanically, on every surface, every run — exactly
like the retracted-figure check. A prose rule someone has to remember is not a control.

═══════════════════════════════════════════════════════════════════════════════
THE LINE, AND IT IS BINARY
═══════════════════════════════════════════════════════════════════════════════
    ✅ "the instrument regulators enforce with"      sellable today, to actual regulators
    ❌ "the enforcer"                                 ends the meeting

Same product. One framing is a business; the other is a claim no lawyer lets past.

The legitimate route to real standing exists and is slow: accreditation — UKAS → certification
body under ISO/IEC 42006, or designation as a notified body. Standing is **earned through an
accreditation chain, never asserted.**

    python3 positioning_guard.py [--selftest]
"""
from __future__ import annotations

import re, sys
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd")


def _deployed_surfaces():
    """Every file csoai-static-deploy2 actually publishes, from the deploy's own allowlist.

    The guard and the deploy must not disagree about what is public. build_site.py owns
    that list; this asks it rather than keeping a parallel copy that drifts. If it cannot
    be imported the guard FAILS LOUD instead of quietly scanning less — a guard that
    silently narrows its own scope is how the same claim stayed live through six fixes.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_build_site", ROOT / "csoai-static-deploy2" / "build_site.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [p for p in mod.publishable() if p.suffix.lower() in {".html", ".json", ".txt", ".xml"}]

# Surfaces a reader or a regulator could actually see. Internal working notes are excluded —
# the guard governs what we PUBLISH, not what we think out loud while measuring.
SURFACES = [
    # The LIVE site first, because it is the only one of these a reader actually reaches.
    # This entry was missing until 2026-07-30: the guard governs "what we publish" and had
    # never once scanned the thing that publishes. It reported 396 surfaces clean while the
    # live site was outside its view entirely — a clean bill of health for the wrong tree.
    ROOT / "councilof-ai/client/src/pages",
    # Static HTML ships to visitors exactly like TSX does. globe3d.html carried "121M ungoverned
    # crimes / 1.45B signed episodes / 73% Art 50 readiness" — fabricated counters, live, that
    # the guard never saw because it only read the React tree. Found 2026-07-30 by screenshot.
    ROOT / "councilof-ai/public",
    ROOT / "councilof-ai/client/public",
    # index.html carries the meta tags and JSON-LD that Google and every AI crawler ingest as
    # our official self-description. It lives in client/ — inside NO directory listed here —
    # so it was never scanned. On 2026-08-04 the live JSON-LD still described a "33-agent
    # Byzantine-fault-tolerant council" that our own measurement retracted (n_eff 1.21 of 3),
    # while the guard reported 757 surfaces clean. The page head is a surface.
    ROOT / "councilof-ai/client/index.html",
    # Pages Functions ship WITH the site and render live output (e.g. the /api/og social
    # card). A retracted claim here reaches every link-share, but this dir was unscanned —
    # the "33-agent Byzantine council" card on 2026-08-04 slipped through because of it.
    ROOT / "councilof-ai/functions",
    # 2026-08-05 — the FOURTH repetition of this exact failure. The guard listed
    # client/src/pages and client/src/components but NOT client/src/data, and the whole
    # blog ships from client/src/data/blog-content.ts. Live on www.csoai.org, inside the
    # served bundle, the article "Byzantine Consensus Explained" states that "at the heart
    # of CSOAI's governance architecture lies a novel and rigorous application of Byzantine
    # Fault Tolerance" — the property MEASURED AND RETRACTED on 2026-07-29 (n_eff 1.21 of
    # 3). The pattern below matches that sentence 9 times; the guard simply never opened
    # the file, and reported councilof-ai clean.
    # The lesson each previous entry re-learns one directory at a time: enumerate what
    # SHIPS, not what we remember writing. client/src is the build input in its entirety,
    # so scan client/src — not a hand-list of its subdirectories.
    ROOT / "councilof-ai/client/src",
    ROOT / "csoai-dashboard-master/client/src/pages",
    ROOT / "csoai-static-deploy2/make_leaderboard.py",
    # 2026-08-05 — the FIFTH repetition, and the worst of them. www.csoai.org no longer
    # serves the React app at all: it serves THIS repository as static HTML, and the guard
    # read exactly one .py from it. So the guard reported councilof-ai clean, which was
    # true and irrelevant — the live site was never in scope.
    # Measured live while unscanned: /tools/bft-council.html titled "CSOAI 41-Agent BFT
    # Council" (41-agent x6, BFT x15, quorum x9) and /tools/bft-vote-log.html titled
    # "33-Agent Council". The property was retracted on 2026-07-29 at n_eff 1.21 of 3, and
    # the published figure has since GROWN to 41 on one page while the other still says 33
    # — the same page pairs "41-agent" with "Quorum 23/33", so it is incoherent as well as
    # unmeasured.
    # The deployed tree is the surface. Scan it.
    #
    # 2026-08-05, SIXTH iteration — and this one is mine. The fix above added
    # `tools/`: a hand-listed subdirectory, the exact move whose failure the
    # councilof-ai entry had just finished describing ("enumerate what SHIPS, not a
    # hand-list of its subdirectories"). The guard then reported 0 while seal.html and
    # sov7_synthesis_dashboard.html — both at the repo ROOT, both deployed — still ran
    # the retracted claim. A second front-end audit found them; the guard could not,
    # because it was still looking at a list of directories instead of at the deploy.
    #
    # There is only one durable answer: scan WHAT THE DEPLOY PUBLISHES. build_site.py
    # is the allowlist that defines the published set, so the guard and the deploy now
    # read from the same source of truth. Add a page to the site and it is guarded
    # automatically; that is the property every previous fix lacked.
    *_deployed_surfaces(),
    ROOT / "csoai-org-v2/src/app",
]
EXTS = {".tsx", ".ts", ".html", ".md", ".py", ".json"}
# .json added 2026-08-04: public/manifest.json was serving "Byzantine-fault-tolerant council"
# LIVE on production (PWA manifest description) while the guard reported clean — because .json
# was not in EXTS, so the walk skipped every machine-readable surface. manifest.json,
# .well-known/agent-card.json and ecosystem.json are exactly what an AI crawler/agent ingests
# as our self-description; a retracted claim there is worse than in TSX, not better. The page
# head (index.html) was already covered; the machine-readable head was not.

# ── Prohibited claims ──────────────────────────────────────────────────────────────────────
# Each is a claim to an authority that is conferred by statute and that we do not hold.
PROHIBITED: list[tuple[str, re.Pattern, str]] = [
    ("comparative authority claim",
     re.compile(r"(western\s+(equivalent\s+to|)\s*TC ?260|equivalent\s+to\s+TC ?260|"
                r"\b(open[- ]source\s+)?FAA\s+(for|of)\s+AI\b|\bISO\s+(for|of)\s+AI(\s+safety)?\b|"
                r"the\s+global\s+standard\s+for\s+AI|independent\s+authority\s+that\s+certifies)", re.I),
     "A COMPARATIVE AUTHORITY CLAIM. Naming TC260, the FAA or ISO as an equivalence asserts "
     "standing we do not hold, on the same site that discloses we are NOT a notified body and "
     "issue no certificates of conformity. Those two statements cannot both stand, and the "
     "meta description is the one that travels — into Google, link previews and AI answers. "
     "Say what is true: an independent measurement body. Standing is EARNED through "
     "accreditation (UKAS -> ISO/IEC 42006), never asserted by analogy."),
    ("invented customer/trust counts",
     re.compile(r"\b(join|trusted by|used by|over)\s+[\d,]+\+?\s*"
                r"(compan|organi[sz]ation|enterprise|client|customer|team)", re.I),
     "A customer or trust count was asserted. The measured customer count is ZERO. "
     "Inventing a trust signal is the exact failure a governance body exists to catch — "
     "and it is the first thing a regulator checks. State a real number or state nothing."),
    ("retracted byzantine fault tolerance",
     re.compile(r"(?<!design )(?<!designed )(?<!intended )\b(byzantine[ -]?fault[ -]?toleran\w*|"
                r"\bPBFT\b|tolerate[sd]? up to \d+ byzantine)", re.I),
     "Byzantine fault tolerance was MEASURED AND RETRACTED on 2026-07-29: n_eff came out at "
     "1.21 of 3 nominal legs, so the legs are not independent and the property does not hold. "
     "Say 'designed 33-agent council' and state the measurement, or say nothing."),
    ("enforcement authority",
     # The negative lookahead exempts DENIALS. provbench.html says "we publish harnesses
     # and measured results; we hold no certification, accreditation, or enforcement
     # power" — the honest disclaimer this guard exists to protect — and the guard flagged
     # it. A guard that fires on its own register teaches people to skim past it, which is
     # exactly how six fixes went by with the claim still live. Precision is not laxity.
     re.compile(r"\b(we|csoai|defoneos|gspc|sov)\b(?![^.]{0,40}\b(?:hold no|have no|has no|"
                r"holds no|is not|are not|not an?|never)\b)"
                r"[^.]{0,60}\b(enforce[sr]?|enforcement (?:body|authority|powers?))\b", re.I),
     "Enforcement powers are conferred by statute on market-surveillance authorities and the "
     "AI Office. Say 'the instrument regulators enforce with' — never 'the enforcer'."),
    ("the enforcer",
     re.compile(r"\bthe enforcer\b|\bAI enforcer\b", re.I),
     "Ends the meeting, and takes independence down with it."),
    ("penalty/withdrawal powers",
     re.compile(r"\b(we|csoai|defoneos)\b[^.]{0,60}\b(lev(?:y|ies)|impose[sd]?|issue[sd]?)\b[^.]{0,30}\b(penalt|fine|sanction)", re.I),
     "Only a public authority can levy an AI Act penalty."),
    # TWO SENSES OF "CERTIFY", AND ONLY ONE IS PROHIBITED.
    #   • Certifying a PERSON — issuing a training certificate to an analyst who passed our
    #     course — is ordinary and lawful. Any training provider may do it. It asserts nothing
    #     about an AI system's conformity.
    #   • Certifying a SYSTEM — attesting that an AI system conforms to the AI Act — requires
    #     an accreditation chain (UKAS -> ISO/IEC 42006 -> certificate) that does not exist,
    #     for us or for anyone: zero notified bodies were designated as of April 2026.
    # Conflating them would flag 11 legitimate training statements and train the reader to
    # dismiss the guard, so the person-sense is excluded by the negative lookahead.
    ("system-certification claim",
     # Same exemption for denials: _CLAIM_TICK55.txt's honesty register says "CSOAI not
     # yet CE+ certified, not an authorised CB" and was flagged for saying so.
     re.compile(r"\b(we|csoai)\b(?![^.]{0,40}\b(?:not yet|not|no|never|cannot|hold no|"
                r"holds no)\b)[^.]{0,40}\bcertif(?:y|ies|ied)\b"
                r"(?![^.]{0,30}\b(professional|analyst|practitioner|people|staff|student|"
                r"candidate|workforce|individual)s?\b)"
                r"|\bCSOAI[- ]certified\b(?![^.]{0,20}\b(analyst|professional)s?\b)", re.I),
     "Certifying an AI SYSTEM needs an accreditation chain (UKAS -> ISO/IEC 42006) that does "
     "not exist. Sell 'attestation-support' and 'evidence-generation'. Certifying a PERSON "
     "who passed a course is fine and is not what this flags."),
    ("notified body claim",
     re.compile(r"\b(we|csoai)\b[^.]{0,40}\b(are|act as|serve as)\b[^.]{0,20}\bnotified body\b", re.I),
     "Notified-body status is a designation. Zero were designated as of April 2026 — and we "
     "are not one of them."),
    ("compliance adjudication",
     re.compile(r"\b(you are|your system is)\s+(non-?)?compliant\b", re.I),
     "We report which evidence EXPIRED. We never adjudicate compliance — that distinction is "
     "the legal armour."),
    # RETRACTED MEASUREMENT CLAIMS. Distinct from authority claims, same blast radius: a
    # property we MEASURED AS FALSE must not survive as a product name. `n_eff.py` returned
    # 1.21 effective votes of 3 nominal (mean phi +0.743) and "Byzantine fault tolerant" was
    # removed from every document — but a component still NAMED "BFT Council" asserts the
    # property in its own name, on a public page, after the retraction.
    ("retracted BFT claim",
     re.compile(r"\bBFT\s+Council\b|\bByzantine[- ]fault[- ]tolerant\b", re.I),
     "Measured n_eff 1.21 of 3 nominal legs (phi_bar +0.743) — the legs are prompts over one "
     "shared blob and are wrong in the same places. The name asserts a property we retracted. "
     "A general CS reference to Byzantine fault tolerance is fine; naming OUR component that "
     "is not."),
    ("regulatory approval",
     re.compile(r"\b(approved|authorised|accredited|recognised)\s+by\s+(the\s+)?(EU|European Commission|AI Office|UKAS|regulator)", re.I),
     "No such approval exists. Claiming one is a misrepresentation to a regulator."),
]

# Phrasings that are explicitly fine, so the guard cannot be satisfied by silence. A page that
# says nothing about its own limits is not safer than one that says the wrong thing.
REQUIRED_SOMEWHERE = [
    ("uncertified default", re.compile(r"\bUNCERTIFIED\b|\bnot a certification\b|\bhold no accreditation\b|\bcannot act as a notified body\b", re.I)),
]


def scan_file(p: Path) -> list[tuple[str, int, str, str]]:
    try:
        text = p.read_text(errors="ignore")
    except Exception:
        return []
    hits = []
    for name, rx, why in PROHIBITED:
        for m in rx.finditer(text):
            line = text[:m.start()].count("\n") + 1
            frag = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            # A prohibited phrase quoted inside a "never say" table is the guard being
            # documented, not violated. Require a nearby negation marker.
            near = text[max(0, m.start() - 260): m.end() + 260].lower()
            if any(k in near for k in ("never say", "~~", "prohibited", "must not",
                                       "do not say", "ends the meeting", "guard",
                                       # Retraction PROSE quotes the retracted claim in order
                                       # to withdraw it. Flagging that would punish the estate
                                       # for publishing its own correction — the opposite of
                                       # what this guard is for.
                                       "retract", "removed from every", "we measured",
                                       "no longer", "withdrawn", "was measured")):
                continue
            # NEGATED forms are the disclaimer, not the claim. "CSOAI holds no accreditation
            # and CANNOT act as a notified body" is the sentence we WANT — flagging it would
            # train the reader to ignore the guard, which is worse than not having one.
            # Forward window is WIDE on purpose. An FAQ asks "Can we get certified…?" and then
            # answers "No — and neither can anyone else". Flagging the question while the answer
            # withdraws the claim would punish the most honest page on the site. The answer sits
            # after the question, so the negation must be searched forward, not just behind.
            window = text[max(0, m.start() - 120): m.end() + 420].lower()
            # URLs and the organisation's own acronym expansion are names, not assertions about
            # our authority. "CSOAI - Certified Safety Oversight AI" is what the letters stand
            # for; a repo path is a path.
            frag_l = text[max(0, m.start() - 60): m.end() + 60].lower()
            # A TRAINING page title ("Certify in 8 Weeks") is the person-sense: we certify
            # people who pass a course, which is lawful and asserts nothing about a system.
            if "training" in str(p).lower() and "certif" in frag_l:
                continue
            if "http" in frag_l or "github.com" in frag_l or "certified safety oversight" in frag_l:
                continue
            if any(k in window for k in ("cannot", "can not", "cannot act", "is not", "are not",
                                         "no accreditation", "not a certification", "never",
                                         "does not", "do not", "neither", "without",
                                         # "Not in the regulatory sense", "will not pretend",
                                         # "holds no such accreditation" — real disclaimers our
                                         # earlier keyword set narrowly missed.
                                         "not in the regulatory", "will not", "no such",
                                         "attestation record", "not a certificate")):
                continue
            hits.append((name, line, frag.strip()[:96], why))
    return hits


def iter_surfaces():
    for s in SURFACES:
        if s.is_file():
            yield s
        elif s.is_dir():
            for p in s.rglob("*"):
                if p.suffix in EXTS and p.is_file():
                    yield p


def main() -> int:
    files = list(iter_surfaces())
    all_hits, corpus = [], ""
    for p in files:
        try:
            corpus += p.read_text(errors="ignore")
        except Exception:
            pass
        for h in scan_file(p):
            all_hits.append((p, *h))

    print("  POSITIONING GUARD — claims to authority we do not hold\n")
    print(f"    surfaces scanned  {len(files)}")
    if all_hits:
        print(f"\n    ❌ {len(all_hits)} prohibited claim(s):\n")
        for p, name, line, frag, why in all_hits:
            rel = p.relative_to(ROOT)
            print(f"      {rel}:{line}  [{name}]")
            print(f"        …{frag}…")
            print(f"        → {why}\n")
    else:
        print("    ✅ no claim to enforcement, certification or notified-body status")

    missing = [n for n, rx in REQUIRED_SOMEWHERE if not rx.search(corpus)]
    if missing:
        print(f"    ⚠️  the surfaces never state: {', '.join(missing)}")
        print(f"        Silence about our own limits is not the same as not overclaiming.")
    else:
        print("    ✅ the UNCERTIFIED default is stated on the surfaces")

    print("\n    THE LINE")
    print("      ✅ 'the instrument regulators enforce with'   — sellable, to actual regulators")
    print("      ❌ 'the enforcer'                             — legally void, kills independence")
    print("      Standing is EARNED through accreditation (UKAS → ISO/IEC 42006), never asserted.")
    return 1 if (all_hits or missing) else 0


def selftest() -> int:
    fails = []
    import tempfile

    def check(text: str) -> list:
        p = Path(tempfile.mktemp(suffix=".tsx"))
        p.write_text(text)
        try:
            return scan_file(p)
        finally:
            p.unlink(missing_ok=True)

    # Must CATCH the claims that matter.
    for bad, label in [
        ("CSOAI is the enforcer of the EU AI Act.", "the enforcer"),
        ("We enforce the AI Act across member states.", "enforcement"),
        ("CSOAI-certified systems carry our mark.", "certification"),
        ("We act as a notified body for high-risk systems.", "notified body"),
        ("Your system is non-compliant with Article 5.", "adjudication"),
        ("Accredited by the European Commission.", "regulatory approval"),
    ]:
        if not check(bad):
            fails.append(f"missed: {label} — {bad!r}")

    # Must NOT catch the legitimate framings, or the guard becomes noise and gets ignored.
    for ok, label in [
        ("The instrument regulators enforce with.", "the sellable framing"),
        ("We supply evidence a market-surveillance authority can act on.", "evidence supply"),
        ("Attestation-support and evidence-generation, never certification.", "correct hedge"),
        ("This is not a certification. CSOAI holds no accreditation.", "the disclaimer"),
        ("Evidence pack EV-77f3 is stale — Article 50(2) changed.", "drift notice wording"),
    ]:
        if check(ok):
            fails.append(f"false positive on {label}: {ok!r}")

    # The two senses of "certify" — the whole point of the refinement.
    if check("CSOAI certifies AI systems as EU AI Act conformant."):
        pass
    else:
        fails.append("missed SYSTEM certification claim")
    if check("We train and certify AI Safety Analysts."):
        fails.append("flagged PERSON certification — training certificates are lawful")
    if check("We develop standards and certify professionals."):
        fails.append("flagged certifying professionals — that is a training certificate")

    # Retracted BFT: catch the product name, allow the general CS concept.
    if not check('<h3>BFT Council Governance</h3>'):
        fails.append("missed the retracted BFT Council product name")
    if check('f = floor((n - 1) / 3): the number of Byzantine faults tolerated.'):
        fails.append("flagged a general CS reference to Byzantine faults")

    # A prohibited phrase inside a 'never say' table is documentation, not a violation.
    doc = 'Say "evidence expired" — never say "you are non-compliant" in any notice.'
    if check(doc):
        fails.append("flagged a prohibited phrase inside its own never-say guidance")

    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 12/12' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else main())
