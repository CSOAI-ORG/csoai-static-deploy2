# engine/functions — NOT published

Moved here from the repo root on 2026-09-14 (governor). Cloudflare `wrangler pages deploy`
auto-bundles a `functions/` directory found in the working directory, and Pages Functions run
ahead of `_redirects`. When an agent ran `wrangler pages deploy _site` from the repo root at
~01:48Z on 14 Sep, the Functions bundle shipped and the owner-ruled catch-all
(`/* https://councilof.ai/:splat 308!`, #55/#57, 2026-09-01) stopped firing: csoai.org served
the old landing page instead of redirecting to councilof.ai.

Rules (owner ruling 2026-09-01, one public website = councilof.ai):
- csoai.org is deployed ONLY by `csoai-site-deploy.yml` in CSOAI-ORG/councilof-ai
  (build_site.py allowlist → strip functions → wrangler). No agent runs wrangler for this project.
- `_site/` is a build output (`.gitignore` line "_site/"). It was force-committed with an old
  `_redirects` that lacks the catch-all; it is untracked in this same change so a stale build
  can never be deployed as-is.
- Nothing under engine/ is served on csoai.org. If an /api/* endpoint is wanted, it belongs in
  CSOAI-ORG/councilof-ai `functions/api/` behind its gates, not here.
