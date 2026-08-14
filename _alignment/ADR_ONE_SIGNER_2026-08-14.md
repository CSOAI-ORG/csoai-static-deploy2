# ADR — one signer, one identity (LOCKED 2026-08-14)

**Status: ADOPTED.** Cross-lane reconciliation (hermes · Claude/lane-2 · k3) converged; k3 proposed,
lane-2 locks it. Not up for re-debate — cheap to fix now, expensive to unpick after cards are in the
wild under two keys.

## Decision
There is **ONE signing identity** for the estate: the externally-verifiable keystone
(`did:web:csoai.org`, pubkey **`f4b4278d…c342`**, private key on the pod keystone only). Every
signing surface — MeasureService / the A2A rail / `cose_wrapper` / `underwriting_pack` / `telemetry`
/ `bom_signer` — **uses that one keystone key**; none ships or generates a second signer.

Doctrine, not preference: *two signers is two identities is no identity* — the same failure shape as
"N repos = N rulers = no ruler." A measurement layer an auditor can't get a single "who signed this,
and why is there more than one key" answer for is a measurement layer they can't trust.

## Verified state (2026-08-14)
- ✅ In practice on the pod it is already **one key**: `chain.py`, `cose_wrapper.py`, `telemetry.py`,
  `bom_signer.py`, `underwriting_pack.py` all default to `/root/.sovos/city_ed25519` (= `f4b4`), which
  `did.json` publishes. Published identity == production signer. [[naming-sovos-vs-sov34]]
- ⚠️ But **fragile**: five modules each hardcode their own key-path default, and `chain.py` **auto-
  generated** a fresh Ed25519 key when the file was missing — the exact way a silent second identity
  gets minted on any misconfigured host.
- ⚠️ `card_issuer.py` (k3's keystone) is on branch **jv-wave8**, not here — must be confirmed to load
  the SAME `f4b4` key, then the rail calls it rather than re-implementing signing.

## Enforcement shipped with this ADR
- ✅ **Fail-closed key loading** (`chain.py`): the canonical production key path can **no longer be
  auto-generated**. If `/root/.sovos/city_ed25519` (or `~/.sovos/city_ed25519`) is requested and
  missing, signing **raises** instead of minting a rogue identity. Explicit temp/test paths still
  generate (selftests unaffected). This is the code-level teeth for "one identity."

## Follow-ups (the "explain / fix before it recurs" list)
1. **Unify key loading to one helper** (the keystone loader); delete the five per-module defaults so
   there is a single place the identity is read.
2. ~~Reconcile `card_issuer.py` (jv-wave8) with MeasureService~~ — **RESOLVED / MOOT (2026-08-14).**
   Recon finding: **`card_issuer.py` does not exist** on `origin/jv-wave8-production` (its attributed
   branch), on `feat/sandbox-arena-seam`, or anywhere findable. The "second signer" it named is not a
   real file in the accessible repo. What IS real: the actual card issuer is `SOVOS/issue_signed_card.py`
   → `MeasureService` → `Chain` → `keystone`, i.e. the ONE path. And every private-key-handling file in
   the package (`keystone`, `chain`, `telemetry`, `cose_wrapper`) routes through the one loader; the
   other signing files (`measure_api`, `sandbox_arena`, `council_signal`, `arena`, `simulator`) hold no
   key and sign via `Chain`. **So "one signer, one key" is already achieved — there is no second signer
   to reconcile.** Residual: (a) if k3 holds a real unpushed `card_issuer.py`, push it and point its
   `_load_key` at `keystone.load_signing_key` (a one-line change — the loader is ready); (b) ✅ **DONE
   (2026-08-14, commit `fc560b4f`)** — `jv-wave8-production` reconciled: `keystone.py` added + its
   `chain.py` (the only one of the six unified files present there) pointed at it, replacing the old
   silent auto-generate. Verified on that branch: temp generates, real loads, missing-prod fail-closes.
   Merged surgically via an isolated worktree — only `keystone.py` + `chain.py`, none of the 335
   unrelated commits.
3. **MinIO write anomaly — EXPLAIN, don't just route around.** Object key `05ceba671e597e04.json`
   refused writes ("insufficient permissions") while every other write to the same prefix succeeded;
   no lock/version marker explained it; k3 stored the rejection cert under a different key and noted
   it. Fine as a workaround, **not** fine to leave unexplained under a signing surface — an
   unexplained write-refusal on the exact key of a *rejection certificate* is the first thing an
   external party asks about. Root-cause it before it recurs. The moat is that the signing layer has
   **no unexplained corners.**

## Also locked (naming, cross-lane)
- **`council_signal` (aggregation) and `promotion_council` (gating) are DIFFERENT jobs — never
  conflated publicly.** One aggregates constituents into a signal; the other gates whether a candidate
  model is promoted. Blur them to an investor and the neutral measurer sounds like it picks winners.
- **The council refusing its own candidate is the headline, not a setback.** Two independent stacks
  (transformers + ollama) returned NO_CHANGE on unseen probes; the seen-data ceiling was disclosed as
  memorization; the council refused promotion with quorum. *Our own promotion council rejected our own
  candidate on unseen data* — the anti-Goodhart gate working. Keep that sentence for the pitch; no
  competitor can fake it. [[self-improving-loop-live]]

## Tri-brain mapping (coherent)
sense = hermes (spine + verifier) · measure = k3 (council that refused) · sign = ONE keystone key
(this ADR). The three lanes converge on the same two real gaps, now closing: correctness gate (built)
+ one externally-verifiable signer (unified here).
