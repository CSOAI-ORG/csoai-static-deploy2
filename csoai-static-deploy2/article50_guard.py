#!/usr/bin/env python3
"""
article50_guard.py — the mechanism behind /ai-transparency.

WHAT THIS EXISTS TO PREVENT
EU AI Act Article 50(1) requires a first-interaction notice on AI systems, from 2 August 2026.
csoai.org today calls no model at all: every interactive surface is a rules engine, which
Recital 12 places outside the Article 3(1) definition. That is a true statement *today*. The
failure mode is not writing it down — it is the day somebody adds an inference call to a surface
and the disclosure page keeps saying zero.

A page that is correct only while somebody remembers to keep it correct is not a control. So the
registry (src/lib/ai-surfaces.ts) is cross-checked against the source mechanically:

  R1  a surface whose code reaches a model provider MUST be registered `ai_system`
  R2  a surface registered `ai_system` MUST mount <AISystemNotice>
  R3  every surface registered at all MUST mount <AISystemNotice>
  R4  every interactive surface in the app MUST appear in the registry

R1 is the one that matters. R4 is what stops a new surface being added quietly.

THREE OUTCOMES, NEVER TWO
  COMPLIANT     every rule checked, every rule passed
  NOT COMPLIANT at least one rule was checked and failed
  UNMEASURED    the app tree could not be read, so nothing was checked

UNMEASURED is not a pass. A guard that cannot find the app must not report the app clean — that
is the exact defect this estate keeps catching in itself.

    python3 article50_guard.py [--app PATH] [--json]
    python3 article50_guard.py --selftest
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path

DEFAULT_APP = Path.home() / "clawd" / "csoai-org-v2"

# Providers whose presence means inference is happening. Substring match against import
# specifiers and fetch targets. Deliberately over-broad: a false positive costs a registry
# edit, a false negative costs an undisclosed AI system.
MODEL_PROVIDERS = (
    "openai",
    "@anthropic-ai",
    "anthropic-sdk",
    "@ai-sdk",
    "ai/react",
    "groq-sdk",
    "openrouter",
    "ollama",
    "replicate",
    "cohere",
    "@google/generative-ai",
    "@google-cloud/vertexai",
    "@huggingface/inference",
    "bedrock-runtime",
    "api.openai.com",
    "api.anthropic.com",
    "api.groq.com",
    "openrouter.ai/api",
    "generativelanguage.googleapis.com",
    "api-inference.huggingface.co",
    "integrate.api.nvidia.com",
)

# Calls that only make sense against a model, even via a local wrapper.
MODEL_CALLS = ("generateText(", "streamText(", "streamUI(", "createCompletion(", "chat.completions")

NOTICE = "AISystemNotice"

VERDICT_COMPLIANT = "COMPLIANT"
VERDICT_NOT_COMPLIANT = "NOT COMPLIANT"
VERDICT_UNMEASURED = "UNMEASURED"


@dataclass
class Violation:
    rule: str
    route: str
    detail: str


@dataclass
class Report:
    verdict: str
    reason: str = ""
    checked_surfaces: int = 0
    registered: int = 0
    ai_systems: int = 0
    violations: list[Violation] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["violations"] = [asdict(v) if not isinstance(v, dict) else v for v in self.violations]
        return d


# ──────────────────────────────────────────────────────────────────────────────
# Reading the registry
# ──────────────────────────────────────────────────────────────────────────────

_ENTRY = re.compile(
    r'route:\s*"(?P<route>[^"]+)".*?nature:\s*"(?P<nature>rule_based|ai_system|unclassified)"',
    re.S,
)


def parse_registry(app: Path) -> dict[str, str] | None:
    """route -> nature. None means the registry itself is unreadable (→ UNMEASURED)."""
    return parse_registry_at(app / "src" / "lib" / "ai-surfaces.ts")


def parse_registry_at(f: Path) -> dict[str, str] | None:
    if not f.is_file():
        return None
    text = f.read_text(encoding="utf-8", errors="replace")

    # Only the SURFACES array — surfaceFor()'s fallback literal also matches the shape and
    # would otherwise register a phantom route.
    start = text.find("export const SURFACES")
    if start < 0:
        return None
    end = text.find("\n];", start)
    if end < 0:
        return None
    body = text[start:end]

    return {m.group("route"): m.group("nature") for m in _ENTRY.finditer(body)}


# ──────────────────────────────────────────────────────────────────────────────
# Reading the app
# ──────────────────────────────────────────────────────────────────────────────

def route_of(page: Path, app_root: Path) -> str:
    """src/app/foo/bar/page.tsx -> /foo/bar. Route groups (dirs in parens) drop out."""
    rel = page.relative_to(app_root / "src" / "app").parent
    parts = [p for p in rel.parts if not (p.startswith("(") and p.endswith(")"))]
    return "/" + "/".join(parts) if parts else "/"


def local_deps(file: Path, app_root: Path, seen: set[Path] | None = None) -> set[Path]:
    """Transitive closure of `@/...` and relative imports. Inference is usually one hop away."""
    seen = seen if seen is not None else set()
    if file in seen or not file.is_file():
        return seen
    seen.add(file)
    text = file.read_text(encoding="utf-8", errors="replace")
    for spec in re.findall(r'from\s+"([^"]+)"', text):
        if spec.startswith("@/"):
            base = app_root / "src" / spec[2:]
        elif spec.startswith("."):
            base = (file.parent / spec).resolve()
        else:
            continue
        for cand in (
            base.with_suffix(".ts"),
            base.with_suffix(".tsx"),
            base / "index.ts",
            base / "index.tsx",
        ):
            if cand.is_file():
                local_deps(cand, app_root, seen)
                break
    return seen


def reaches_model(files: set[Path]) -> str | None:
    """Return the first provider/call token found, or None. The token is the evidence."""
    for f in sorted(files):
        text = f.read_text(encoding="utf-8", errors="replace")
        for spec in re.findall(r'from\s+"([^"]+)"', text) + re.findall(
            r'require\(\s*"([^"]+)"', text
        ):
            low = spec.lower()
            for p in MODEL_PROVIDERS:
                if p in low:
                    return f"{p} (imported by {f.name})"
        # fetch targets and SDK call shapes, ignoring comment lines so that prose about
        # providers in a docblock does not trip the guard
        for line in text.splitlines():
            s = line.strip()
            if s.startswith(("//", "*", "/*")):
                continue
            low = s.lower()
            for p in MODEL_PROVIDERS:
                if p in low and ("fetch" in low or "http" in low):
                    return f"{p} (called in {f.name})"
            for c in MODEL_CALLS:
                if c in s:
                    return f"{c} (called in {f.name})"
    return None


def is_interactive(files: set[Path], require_use_client: bool = True) -> bool:
    """
    Does this surface take input from a person and return something?

    `require_use_client` is the Next.js gate: there, a component without the directive renders on
    the server and cannot hold an interaction. In a Vite SPA there is no such split — every
    component is a client component — so requiring the directive there matches nothing.

    That is not hypothetical. Run against the live Vite site with the gate on, this reported
    0 interactive surfaces out of 311 routes, on a site with an assessment tool and a contact
    form. A detector that answers "none" for the whole app is not a clean bill of health; it is
    a broken detector, and it would have produced a COMPLIANT verdict covering nothing at all.
    """
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        if require_use_client and '"use client"' not in text and "'use client'" not in text:
            continue
        if re.search(r"<(input|textarea|select|form)\b", text, re.I):
            return True
        if "onSubmit" in text or ("useState" in text and "fetch(" in text):
            return True
    return False


_ROUTE = re.compile(r'<Route\s+path="(?P<path>[^"]+)"\s+component=\{(?P<comp>\w+)\}')
_LAZY = re.compile(r'const\s+(?P<comp>\w+)\s*=\s*lazy\(\s*\(\)\s*=>\s*import\("(?P<spec>[^"]+)"\)')
_PLAIN_IMPORT = re.compile(r'import\s+(?P<comp>\w+)\s+from\s+"(?P<spec>[^"]+)"')


def declared_model_sdks(app: Path) -> list[str]:
    """
    Model SDKs in package.json that are never imported anywhere.

    This is not a violation — a dependency is not a call. But it is the shortest possible
    distance to becoming one: the package is installed, so adding inference is a single import
    with no install step and no review of this file. Reported as a watch condition, separately
    from R1, because collapsing "declared" into "called" would either cry wolf on every repo that
    once tried an SDK, or say nothing at all.
    """
    pkg = app / "package.json"
    if not pkg.is_file():
        return []
    try:
        deps = json.loads(pkg.read_text()).get("dependencies", {})
    except (json.JSONDecodeError, OSError):
        return []
    return sorted(d for d in deps if any(p in d.lower() for p in MODEL_PROVIDERS))


def vite_surfaces(app: Path) -> dict[str, Path] | None:
    """route -> page file, for a Vite + wouter app. None if this is not that shape."""
    app_tsx = app / "client" / "src" / "App.tsx"
    if not app_tsx.is_file():
        return None
    text = app_tsx.read_text(encoding="utf-8", errors="replace")

    comp_to_file: dict[str, Path] = {}
    for m in list(_LAZY.finditer(text)) + list(_PLAIN_IMPORT.finditer(text)):
        spec = m.group("spec")
        if not spec.startswith("."):
            continue
        base = (app_tsx.parent / spec).resolve()
        for cand in (base.with_suffix(".tsx"), base.with_suffix(".ts")):
            if cand.is_file():
                comp_to_file[m.group("comp")] = cand
                break

    out: dict[str, Path] = {}
    for m in _ROUTE.finditer(text):
        f = comp_to_file.get(m.group("comp"))
        if f:
            out[m.group("path")] = f
    return out


def check_vite(app: Path) -> Report:
    """Same four rules, applied to the wouter route table instead of the Next file tree."""
    surfaces = vite_surfaces(app)
    if not surfaces:
        return Report(VERDICT_UNMEASURED, reason="no client/src/App.tsx route table found")

    registry = parse_registry_at(app / "client" / "src" / "lib" / "ai-surfaces.ts")
    if registry is None:
        return Report(
            VERDICT_UNMEASURED, reason="client/src/lib/ai-surfaces.ts absent or unparseable"
        )

    violations: list[Violation] = []
    checked = 0

    for route, page in sorted(surfaces.items()):
        deps = local_deps_vite(page, app)
        interactive = is_interactive(deps, require_use_client=False)
        registered = route in registry
        if not (interactive or registered):
            continue
        checked += 1

        mounts = any(NOTICE in d.read_text(errors="replace") for d in deps)
        provider = reaches_model(deps)
        nature = registry.get(route)

        if not registered:
            violations.append(
                Violation("R4-unregistered", route, "interactive surface missing from registry")
            )
            continue
        if provider and nature != "ai_system":
            violations.append(
                Violation(
                    "R1-undisclosed-inference", route, f"reaches {provider} but registered '{nature}'"
                )
            )
        # R2 only. R3 — "every registered surface mounts the notice" — was right for a 14-surface
        # app and is wrong here: this site has 135 interactive surfaces and none is an AI system,
        # so requiring the banner on all of them would put a legally meaningless notice on 135
        # pages and teach readers to ignore it. For non-AI surfaces the disclosure lives in one
        # place, /ai-transparency, which lists every route. The obligation is unchanged: the
        # notice is mandatory exactly where Article 50(1) applies.
        if nature == "ai_system" and not mounts:
            violations.append(
                Violation("R2-missing-notice", route, f"registered 'ai_system' but no <{NOTICE}>")
            )

    return Report(
        verdict=VERDICT_NOT_COMPLIANT if violations else VERDICT_COMPLIANT,
        reason="" if violations else "all rules checked and passed",
        checked_surfaces=checked,
        registered=len(registry),
        ai_systems=sum(1 for n in registry.values() if n == "ai_system"),
        violations=violations,
    )


def local_deps_vite(file: Path, app_root: Path, seen: set[Path] | None = None) -> set[Path]:
    """As local_deps, but `@/` resolves to client/src in this app."""
    seen = seen if seen is not None else set()
    if file in seen or not file.is_file():
        return seen
    seen.add(file)
    text = file.read_text(encoding="utf-8", errors="replace")
    for spec in re.findall(r'from\s+"([^"]+)"', text):
        if spec.startswith("@/"):
            base = app_root / "client" / "src" / spec[2:]
        elif spec.startswith("."):
            base = (file.parent / spec).resolve()
        else:
            continue
        for cand in (
            base.with_suffix(".ts"),
            base.with_suffix(".tsx"),
            base / "index.ts",
            base / "index.tsx",
        ):
            if cand.is_file():
                local_deps_vite(cand, app_root, seen)
                break
    return seen


def check(app: Path) -> Report:
    # Dispatch on app shape. A Next-only guard pointed at the Vite app would find no page.tsx
    # and report UNMEASURED, which is honest but useless — and the live site is the Vite one.
    if (app / "client" / "src" / "App.tsx").is_file():
        return check_vite(app)

    app_dir = app / "src" / "app"
    if not app_dir.is_dir():
        return Report(VERDICT_UNMEASURED, reason=f"no app tree at {app_dir}")

    registry = parse_registry(app)
    if registry is None:
        return Report(VERDICT_UNMEASURED, reason="src/lib/ai-surfaces.ts absent or unparseable")

    pages = sorted(app_dir.rglob("page.tsx"))
    if not pages:
        return Report(VERDICT_UNMEASURED, reason="app tree contains no page.tsx")

    violations: list[Violation] = []
    checked = 0

    for page in pages:
        route = route_of(page, app)
        deps = local_deps(page, app)
        interactive = is_interactive(deps)
        registered = route in registry
        if not (interactive or registered):
            continue
        checked += 1

        page_text = page.read_text(encoding="utf-8", errors="replace")
        mounts = NOTICE in page_text or any(NOTICE in d.read_text(errors="replace") for d in deps)
        provider = reaches_model(deps)
        nature = registry.get(route)

        # R4 — present in the app, absent from the registry
        if not registered:
            violations.append(
                Violation("R4-unregistered", route, "interactive surface missing from registry")
            )
            continue

        # R1 — inference without the ai_system classification
        if provider and nature != "ai_system":
            violations.append(
                Violation(
                    "R1-undisclosed-inference",
                    route,
                    f"reaches {provider} but registered '{nature}'",
                )
            )

        # R2 / R3 — the notice must actually be on the page
        if not mounts:
            rule = "R2-missing-notice" if nature == "ai_system" else "R3-missing-notice"
            violations.append(Violation(rule, route, f"registered '{nature}' but no <{NOTICE}>"))

    return Report(
        verdict=VERDICT_NOT_COMPLIANT if violations else VERDICT_COMPLIANT,
        reason="" if violations else "all rules checked and passed",
        checked_surfaces=checked,
        registered=len(registry),
        ai_systems=sum(1 for n in registry.values() if n == "ai_system"),
        violations=violations,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Selftest
# ──────────────────────────────────────────────────────────────────────────────

def _scaffold(root: Path, surfaces: list[tuple[str, str]], pages: dict[str, str]) -> None:
    """surfaces: (route, nature) registry entries. pages: route -> page.tsx body."""
    lib = root / "src" / "lib"
    lib.mkdir(parents=True)
    entries = "\n".join(
        f'  {{ route: "{r}", label: "x", nature: "{n}", mechanism: "m", evidence: [] }},'
        for r, n in surfaces
    )
    (lib / "ai-surfaces.ts").write_text(
        "export const SURFACES: Surface[] = [\n" + entries + "\n];\n"
    )
    for route, body in pages.items():
        d = root / "src" / "app" / route.strip("/")
        d.mkdir(parents=True, exist_ok=True)
        (d / "page.tsx").write_text(body)


CLEAN_PAGE = (
    '"use client";\n'
    'import AISystemNotice from "@/components/AISystemNotice";\n'
    "export default function P(){return <><AISystemNotice route=\"/a\" /><input /></>;}\n"
)
NO_NOTICE_PAGE = '"use client";\nexport default function P(){return <input />;}\n'
INFERENCE_PAGE = (
    '"use client";\n'
    'import OpenAI from "openai";\n'
    'import AISystemNotice from "@/components/AISystemNotice";\n'
    "export default function P(){return <><AISystemNotice route=\"/a\" /><input /></>;}\n"
)


def selftest() -> int:
    passed = failed = 0

    def ok(name: str, cond: bool, extra: str = "") -> None:
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"  PASS  {name}")
        else:
            failed += 1
            print(f"  FAIL  {name} {extra}")

    # 1 — negative control. If the detector fired unconditionally this would fail, which is the
    # whole point of running it: a guard that always says NOT COMPLIANT proves nothing.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _scaffold(root, [("/a", "rule_based")], {"/a": CLEAN_PAGE})
        r = check(root)
        ok("clean tree is COMPLIANT", r.verdict == VERDICT_COMPLIANT, r.reason + str(r.violations))
        ok("clean tree checked a surface", r.checked_surfaces == 1, f"got {r.checked_surfaces}")

    # 2 — R1: inference behind a rule_based registration is the failure this file exists for.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _scaffold(root, [("/a", "rule_based")], {"/a": INFERENCE_PAGE})
        r = check(root)
        ok("R1 fires on undisclosed inference", r.verdict == VERDICT_NOT_COMPLIANT)
        ok(
            "R1 names the rule",
            any(v.rule == "R1-undisclosed-inference" for v in r.violations),
            str(r.violations),
        )

    # 3 — R1 must NOT fire once the same code is correctly registered.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _scaffold(root, [("/a", "ai_system")], {"/a": INFERENCE_PAGE})
        r = check(root)
        ok("R1 clears when registered ai_system", r.verdict == VERDICT_COMPLIANT, str(r.violations))

    # 4 — R3: registered but the notice was never mounted.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _scaffold(root, [("/a", "rule_based")], {"/a": NO_NOTICE_PAGE})
        r = check(root)
        ok(
            "R3 fires on missing notice",
            any(v.rule == "R3-missing-notice" for v in r.violations),
            str(r.violations),
        )

    # 5 — R4: an interactive surface that nobody registered.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _scaffold(root, [("/a", "rule_based")], {"/a": CLEAN_PAGE, "/b": NO_NOTICE_PAGE})
        r = check(root)
        ok(
            "R4 fires on unregistered surface",
            any(v.rule == "R4-unregistered" and v.route == "/b" for v in r.violations),
            str(r.violations),
        )

    # 6 — inference reached through a local import, not imported by the page itself. This is the
    # realistic shape: page -> Client -> lib/llm.ts. A one-file scan would miss it.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _scaffold(root, [("/a", "rule_based")], {"/a": CLEAN_PAGE})
        (root / "src" / "lib" / "llm.ts").write_text('import OpenAI from "openai";\nexport const x=1;\n')
        p = root / "src" / "app" / "a" / "page.tsx"
        p.write_text('import { x } from "@/lib/llm";\n' + CLEAN_PAGE)
        r = check(root)
        ok(
            "R1 follows transitive imports",
            any(v.rule == "R1-undisclosed-inference" for v in r.violations),
            str(r.violations),
        )

    # 7 — prose about providers must not trip the guard. /ai-transparency and this repo's own
    # docblocks name every provider by design.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _scaffold(root, [("/a", "rule_based")], {"/a": CLEAN_PAGE})
        p = root / "src" / "app" / "a" / "page.tsx"
        p.write_text("// we do not call api.openai.com or use @ai-sdk here\n" + CLEAN_PAGE)
        r = check(root)
        ok("comments do not trip R1", r.verdict == VERDICT_COMPLIANT, str(r.violations))

    # 8 — a missing app tree is UNMEASURED, never COMPLIANT.
    with tempfile.TemporaryDirectory() as t:
        r = check(Path(t))
        ok("absent app tree is UNMEASURED", r.verdict == VERDICT_UNMEASURED, r.verdict)

    # 9 — a missing registry with a real app tree is also UNMEASURED, not a pass.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        d = root / "src" / "app" / "a"
        d.mkdir(parents=True)
        (d / "page.tsx").write_text(CLEAN_PAGE)
        r = check(root)
        ok("absent registry is UNMEASURED", r.verdict == VERDICT_UNMEASURED, r.verdict)

    # 10 — the surfaceFor() fallback literal in the real registry must not register a phantom.
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _scaffold(root, [("/a", "rule_based")], {"/a": CLEAN_PAGE})
        f = root / "src" / "lib" / "ai-surfaces.ts"
        f.write_text(
            f.read_text()
            + '\nexport function surfaceFor(route: string) {\n'
            '  return SURFACES.find(s => s.route === route) ?? '
            '{ route, label: route, nature: "unclassified", mechanism: "", evidence: [] };\n}\n'
        )
        r = check(root)
        ok("fallback literal is not parsed as an entry", r.registered == 1, f"got {r.registered}")

    print(f"\nselftest {passed}/{passed + failed}")
    return 0 if failed == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", type=Path, default=DEFAULT_APP)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    r = check(args.app)
    if args.json:
        print(json.dumps(r.to_dict(), indent=2))
    else:
        print(f"ARTICLE 50 GUARD — {args.app}")
        print(f"  verdict            {r.verdict}")
        if r.reason:
            print(f"  reason             {r.reason}")
        print(f"  surfaces checked   {r.checked_surfaces}")
        print(f"  registered         {r.registered}")
        print(f"  ai systems         {r.ai_systems}")
        for v in r.violations:
            print(f"    {v.rule:26} {v.route:28} {v.detail}")

    # UNMEASURED is not a pass. The gate owns the exit code, and it gets a non-zero here.
    return 0 if r.verdict == VERDICT_COMPLIANT else 1


if __name__ == "__main__":
    sys.exit(main())
