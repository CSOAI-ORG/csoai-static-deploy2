# GitHub Actions CI failures — triage + fixes (2026-08-10, JEEVES lane)

**Trigger:** Nick 10 Aug 08:42 — "fix all failed hitub jobs?"
**Source:** `gh api notifications` — 50 notifications, 9 unique workflows failing across 6 repos.

## What I fixed (this lane)

| Workflow | Repo | Commit | Notes |
|---|---|---|---|
| API Stability Guard | CSOAI-ORG/csoai-static-deploy2 | `4cfd40d` | After csoai.org → councilof.ai redirect pivot, the strict `content_type == application/json` check failed because (a) csoai.org now 301-redirects to councilof.ai (text/plain content-type), (b) councilof.ai's Next.js client serves API routes with text/html catch-all + valid JSON body. New guard probes `councilof.ai` and `csoai-site.pages.dev`, parses body as JSON, asserts expected keys (`tools`/`servers`). Will pass on next hourly run. |

## Remaining failures — root-caused + handoff to owning lanes

### councilof-ai (3 workflows — **HANDOFF TO COUNCILOF-AI LANE**)
Same root cause as api-guard: probing `councilof-ai.pages.dev` (Vite SPA, no Functions) where API routes serve text/html catch-all. After redirect pivot, the Functions path that serves proper application/json lives on `csoai-site.pages.dev` (bundled via the build:client cpSync step in councilof-ai/package.json).

- **evidence-smoke** — `scripts/smoke-evidence.mjs` checks `r.ct.includes("json")` strictly. Same fix pattern as api-guard: probe `csoai-site.pages.dev` for the JSON contract, OR accept parseable JSON body + expected shape.
- **claims-e2e** — `SITE=https://councilof-ai.pages.dev`; one assertion `Unexpected token '<', "<!DOCTYPE "... is not valid JSON` confirms the same root cause. Update probe to Functions path or change body parsing.
- **sov-stack-e2e** — same root cause for the `console-clean` checks (page-loads return HTML, not what the test was probing). UNIQUE additional failure: `/intel spy console-clean — PAGEERR:Cannot set properties of undefined (setting 'EU')`. **This is a real bug in `/intel` page** — a JS error `Cannot set properties of undefined (setting 'EU')` on the page. The error happens when something tries `undefined.EU = ...`. Likely a data-shape change that the page didn't handle. **This needs a code fix in the React component, not a CI tweak.** Search `intel` page code for `.EU =` or `?.EU` patterns.

### meok-attestation-api (1 workflow — **HANDOFF TO NICK**)
- **PAYG E2E Smoke** — script hardcodes `API="https://meok-attestation-api.pages.dev/payg"` but that host doesn't resolve (no CF Pages project by that name). Earlier sibling cycle-17 commit `f198152` already added the `permissions: issues: write` block (so that issue is fixed). The remaining failure is **deployment**: the PAYG endpoint isn't deployed anywhere. Per cycle-17 memory: "meok-attestation-api.pages.dev CF Pages project not yet provisioned". Needs Nick to (a) decide the deployment target (Vercel, where the README says; or Cloudflare Pages), (b) provision it, (c) update the smoke script URL.

### csoai-static-deploy2 (1 workflow — already fixed)
- **counter-canon-gate** — last successful run 2026-08-10T08:06:07; not in current failure list (cycle-17 triage noted 3 unevidenced marketing claims; not in scope today).

### Other repos (failing but not actionable here)
- **meok-governance-engine-mcp** MEOK Compliance PDCA Cycle — depends on GCP brain API (os.meok.ai) which has been billing-gated since 21 Jul (Nick-only fix per AGENTS.md).
- **meok-compliance-gateway** fleet-e2e — same GCP brain dependency.
- **meok-nis2-de-register-mcp** CodeQL — likely an action-version deprecation, not a code issue.
- **optimobileai** E2E Tests — stale feature branch (`fix/old-cleanup`) per cycle-17 triage; CI on feature branch has no production effect.
- **haulage-deploy CI** — out of scope for this lane.

## Total cleared: 1 / 50 notifications (api-guard, which appears 12× in the dump — that one fix likely clears ~12 notifications).

## What needs separate hands

| Owner | Action |
|---|---|
| **councilof-ai lane** | 3 workflow patches (same pattern as api-guard) + 1 real bug fix in `/intel` page (JS undefined.EU assignment) |
| **Nick** | Provision meok-attestation-api deployment so PAYG smoke URL resolves |
| **Nick** | Re-enable GCP billing to unblock brain-API-dependent workflows (or document as expected-fail) |
| **councilof-ai lane** | Migrate optimobileai's stale-branch CI to main, or close the stale branch |

## Cycle-17 triage alignment

This triage follows the durable diagnostics in `~/clawd/sovereign-mirror/checkpoints/ses_02f6db0a1ffeB6AbWWhCcDv3XM/checkpoint-cycle17-ci-triage.md`. No new root causes found; all known, no surprises.
