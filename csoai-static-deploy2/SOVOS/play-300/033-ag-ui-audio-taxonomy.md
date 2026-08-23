# 033–034 — AG-UI AUDIO EVENT TAXONOMY (draft → proposal)

Date: 2026-08-21 · lane: K3 (taxonomy) / K3+LANE (PR, external) · ⏰ weeks · REAL: zero audio events
in AG-UI, docs promise "upcoming" (H3/D04 §3). First credible proposal owns the category (I7).

## 1. Event types (mirror START→CONTENT→END convention)
| Event | Payload | Purpose |
|---|---|---|
| `AUDIO_MESSAGE_START` | messageId, mime, sampleRate, channels | session open |
| `AUDIO_MESSAGE_CHUNK` | messageId, chunkIndex, base64 data | streaming audio |
| `AUDIO_MESSAGE_END` | messageId | session close |
| `TRANSCRIPT_DELTA` | messageId, delta, isFinal | text alignment |

Keyed by `messageId`; audio and transcript deltas share the id so clients align voice↔text.

## 2. Barge-in semantics (the differentiator)
- `INTERRUPTION` event + playback-flush point + heard-so-far accounting.
- Cites LiveKit / Pipecat / AssemblyAI patterns (D04 §3).

## 3. Demand proof (breakage citations)
- PR #2476 (audio), #2447/#2448, #2029 — link all in the proposal.
- File issue first per CONTRIBUTING; tag code owners; co-implement.

## 4. Reference impl
TS SDK fork implementing the four event types, round-trip demo (LANE, M).

## 5. Fallback & metrics
- Standalone audio mini-spec under our name if the host stalls 14 days (step 054).
- Cross-post on engineering blog at filing; metrics row: issues/PRs/maintainer responses.

## Honest state
UNSIGNED until POD key in harness. The PR itself is external (GitHub, Claude merge lane).
