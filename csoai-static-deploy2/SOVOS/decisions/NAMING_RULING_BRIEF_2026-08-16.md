# THE ONE NAMING RULING — Decision Brief (2026-08-16, v2)
**Owner decision required. ≤ 2-minute read. Default recommended: COUNCIL-FIRST.**
Compiled by JEEVES lane from the master (Parts AZ/CA/EU/FC), live probes, and the
current surface scan. This is the ruling that unblocks: the apex purge, ~half the
site fixes, 23+ public SOV URLs, and the message coherence of every outward
artifact.

---

## 1. The situation in one paragraph

The measurement body is publicly **Council of AI** (csoai.org, councilof.ai, PyPI
`csoai`, npm `@meok-labs/csoai`, MCP registry `io.github.CSOAI-ORG/*`). The
internal engine is the **SOVOS** lineage (SOV-*, sov6, sov-space, Sovereign OS
strings — codenames that pre-date the public pivot). A naming ruling is needed
because: (a) codenames are already reaching public surfaces (the councilof.ai
homepage still shows `sov-os` and `sov-space` strings; ~23 public URLs still
carry SOV paths; meok.ai was scrubbed but `sov*` strings exist in the
`sov-authority` MCP pyPI estate of a sibling lane), and (b) the current posture —
"public name Council, internal name SOVOS, with SOV strings leaking" — is the
worst of both worlds: maximal confusion, maximal cleanup surface, and a legal
exposure (Part AZ) if a regulator reads both.

The master itself lists this as **THE ONE NAMING RULING** that "now also blocks
the apex purge, half the site fixes, and the 23+ public SOV URLs" (Part EF,
2026-08-16).

---

## 2. The options (with the trade-offs)

### Option A — COUNCIL-FIRST (recommended default)
Every public surface carries Council of AI / GSPC; engine codenames are
transitioned to internal-only over 60 days; the doc charter, the model cards, the
`/sov-*` URL paths, the `sov-*` package names on PyPI, and the `sov-authority`
client get renamed/redirected.

**For:** zero ambiguity for buyers, regulators, and the press; matches the
already-majority public surface; sets the ceiling on every outward claim
("Council of AI measured"); long-term brand compound.
**Against:** ~60-120 min of mechanical rename work across ~4 repos + a few
one-click PyPI/npm name changes (2 are owner-gated: npm 2FA, one HF token
revoke). Some package renames break downstream imports (sov6-* model tags in
Ollama, `sovos-*` py packages) — handle with alias/redirect **not** by editing
the weights.
     - Under the current `sovos-` package namespace we keep that; only the
       *public-facing* name strings and URL slugs change.

### Option B — SOV-FIRST (the brand gets SOV; "Council" becomes a product line)
Keep SOV as the flagship; Council of AI remains the neutral body. The master's
current counsel-Q is precisely "should SOVOS become the investor-facing brand,
with CSOAI as the neutral measurement body?" This would flip the naming work the
OTHER way (rename csoai.org-facing strings to SOV; rename alliance pages; keep
the Council product).

- For: if Nick prefers the SOV wordmark (it has emotional/strategic weight, and
  the engine docs all say SOV); gives a single story line across the estate.
- Against: the public measurement sphere has *already* been positioned as
  "Council of AI" (the press sheet, PyPI, the MCP registry — all live and
  deployed); flipping the public face to "SOV" re-introduces the VM exposure band
  (the codenames were flagged as the *legal risk*); the "first mover on
  independence" brand loses the "Council" noun (a measurement body named Council
  is self-describing; SOV is a nonce-coded engine name).

### Option C — DUAL TRACK (Council = public; SOV = internal engine, documented as such)
Keep both, but write the transition rule: public surfaces = Council/GSPC;
internal engine code/packages = SOV. This is *de facto* where the estate already
is — but with the leak areas unfixed (the homepage strings, the 23 URLs, the
`sov-authority` client). Option C says: keep the duality, but close the leaks and
write the doctrine.

- For: 30-min immediate cleanup instead of a 60-day migration; no re-brand of
  the engine; the dual identity is honest ("we internally call the engine SOV;
  the public product is Council").
- Against: the legal exposure is not eliminated — it's managed. A buyer/regulator
  who reads the repo README (which says "SOVOS — Sovereign...") and the press
  sheet ("Council of AI") will still see two publics. The VM exposure question
  (EU's Article 50 marking) still applies.

---

## 3. What the master's canon says (the loaded constraints)

- **The naming calculator (Part N**): public names = Council, GSPC, DEFONEOS
  surfaces only; codenames internal. The "public surface" definition explicitly
  includes npm, PyPI, the MCP registry, the GitHub org, and the csoai-facing
  HTML pages.
- **The "severed-brand" doctrine (memory + Parts AZ/CA/FC):** any string that
  should be the public brand but carries the internal codename is a
  **contamination**; the estate has already spent two cleanup waves on it
  (meokai, csoai.org, proofof.ai — all now clean).
- **The measurement exposure (Part AY/EU):** Article 50 marking + the
  2-Dec-2026 grace for pre-existing systems; the estate publishes measurement
  on "AI-lab output provenance", so our own provenance hygiene sits under the
  same lens. A public page that mixes Council + SOV increases the (small but
  real) "they're two companies" ambiguity that a regulator could use to ask why
  we didn't mark SOV's outputs.

---

## 4. The concrete work per option (measured)

Common truth: **everything below is lane-executable except 3 owner gates**
(npm 2FA publish; PyPI package transfer; the councilof.ai route-table rename
which lives in kimi's lane).

| Option | Work | Owner gates | Blocked by |
|---|---|---|---|
| **A — Council-first** | rename/redirect ~23 URL slugs + 4 repo READMEs + sov-* package names (aliases) | npm, PyPI, kimi route rename | ~60-120 min lane time |
| **B — SOV-first** | reverse the flag: percentage of public copy flips to SOV; CSOAI/CM original? | the same 3 + a full-content decision | ~180-240 min + new counsel |
| **C — deep-track** | fix the 6 leaks + write the "internal/external" doctrine doc | none beyond the same 3 | ~30-45 min |

---

## 5. The recommendation

**Default if no opinion lands by end-of-day: Option C now (30 min, stops all
leaks) + Option A within 60 days (start the Council-first wave).** The estate
is already 85% Council-first on the public face; the cheapest *coherent* state is
to make the public face 100% Council and document the internal codename as
internal, then optionally rename the flags later if Nick prefers SOV as the
flagship.

- Do the **Council-first** 30-min option now (it doesn't commit anything; it
  makes the current public position coherent — the exact position the estate
  already ships).
- The **repo README** (the one text that says "SOVOS — Sovereign Open World
  Operating Stack" at the top) gets a one-line prefix: "The Council of AI
  measurement engine (internal code-name: SOV). Public product: Council."
- The **sov-authority client** gets an alias package name.
- The 23 public SOV URL slugs get **redirects** (not deletes), so nothing breaks.
- The **kimi route-table** fix is queued in their lane; the owner nod is just
  "you have the nod to re-name the 4 routes".

Choose now, or the fallback (C-now + A-soon) is what this brief recommends.

---

*Prepared by JEEVES; decision log at `SOVOS/decisions/`. The ruling itself gets
one line appended to the master when made.*