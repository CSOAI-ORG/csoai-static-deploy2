# 121 — SIGNED-REPLAY SPEC v0.1 (👑 CROWN JEWEL · OPEN · H7/D02 §1A)

Date: 2026-08-21 · lane: K3+LANE · gate: spec + worked envelope · kill criteria: credible signed-replay
standard ships elsewhere → adopt + extend (never fight).

**Thesis:** game engines give deterministic re-execution; verification-LLM schemes lack it
(A2Auth F1=0.876 = why LLM replay fails, D02 §2). Kill attempts on this whitespace failed in-window (H7).

## 1. Envelope (DSSE/COSE)
```
signed-replay/v0.1 = {
  init_state_hash,      # reproducible start state
  event_stream_hash,    # ordered action list
  engine_digest,        # engine + version + flags
  score,                # terminal score
  bot_image_digest,     # competitor image identity
  timestamp,
  prev_hash             # chain
}
```
Wrapped as DSSE (PAE) or COSE_Sign1; ed25519 (alg -19). Traces off-envelope (reproducible, not shipped).

## 2. Signing paths
- **Sigstore keyless (primary):** Fulcio + Rekor, CI workload identity, zero key management;
  offline-verify vs pinned TUF root (D02 §2).
- **Optional SCITT registration:** replay bundle → Transparent Statement (RFC 9943), dual-anchor.

## 3. Determinism requirement
Replay = re-executable command list. Gate: re-run reproduces identical score.
Reference impl: sign a `.SC2Replay` end-to-end (MPQ container; parsers exist, D02 §2).

## 4. Verify surface
One URL, offline-verifiable, human-rendered signature + receipt (cosign-bundle pattern, D02 §2).

## 5. Honest limits
Inclusion proven; non-equivocation needs consistency proofs + monitor (NOA-lesson, D01 §5).
UNSIGNED until POD key in harness (owner-gated).
