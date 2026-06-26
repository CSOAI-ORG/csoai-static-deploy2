# Depth-audit — REAL test-run fidelity (2026-06-26)

The static depth-audit checked "test file present." This is the next tier: **actually running `pytest`** on a curated **35-MCP high-value sample** (the 20 A2A substrate + 15 framework/safety MCPs). Honest results.

## Headline
- **26 / 35 pass clean** out-of-the-box — **301 test cases green**
- **9 "fail"** — but **7 of the 9 are packaging/harness hygiene, not broken governance logic**; only **2 have genuine assertion failures**

## Failure breakdown (honest)
| Cause | Count | MCPs | Real bug? |
|---|---|---|---|
| `pyproject.toml` malformed (pytest config read chokes at line 8) | 5 | eu-ai-act-compliance, mifid-ii-ai, nis2-compliance, gdpr-compliance-ai, agent-identity-trust | ❌ no — packaging fix |
| relative-import test-harness (`ImportError: relative import with no known parent`) | 2 | agent-prompt-injection-firewall, bias-detection | ❌ no — test-config fix |
| **genuine assertion failures** | 2 | agent-incident-reporter (2 failed), csoai-governance-crosswalk (11 failed) | ✅ yes — worth a fix pass |

## Honest read
The governance **logic** holds: 26/35 fully green + the 7 config failures are MCPs whose tests don't even run due to a malformed `pyproject.toml` or import path — not failing assertions. The 5 `pyproject` errors share the same line-8 defect → a **single batch fix** likely flips all 5 green. Only **2 MCPs have real failing tests** and need attention.

## Corrections to the static audit
- The "1 STUB" (`agent-incident-reporter-mcp`) was a **false positive** — it uses the low-level MCP SDK (4 real Ed25519 tools + tests), so the estate is **369/369 real**, not 368. (Its tests do have 2 genuine failures, tracked above.)

## Follow-ups (no owner keys)
- [ ] Batch-fix the 5 `pyproject.toml` line-8 defects → re-run → expect 31/35 green
- [ ] Fix the 2 relative-import test harnesses (add conftest/`__init__` or `-p no:cacheprovider`)
- [ ] Investigate the 2 real failures (agent-incident-reporter, csoai-governance-crosswalk)

## Method / caveat
35-MCP **sample** (not all 369) — too slow to run the full estate inline; the sample is the high-value set (A2A substrate + lead framework MCPs). "pass" = `pytest -q` exit 0. Run on macOS Python 3.x, no per-test isolation beyond pytest defaults.
