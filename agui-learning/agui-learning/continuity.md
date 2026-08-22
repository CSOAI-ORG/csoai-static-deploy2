# CONTINUITY Axis — Competitor & Peer Learning Report

**Prepared for:** Council of AI (CSOAI) — GSPC CONTINUITY axis
**Scope:** hash-chained ledgers, anchor/immutability, ongoing re-attestation, timestamp anchoring
**Method:** web_search + curl verification; verified claims only; no accounts, no submissions.
**Honesty note:** every claim below is tied to a public source. Where a product's "permanence" is economic rather than cryptographic (Arweave, IPFS), that is stated explicitly and not overstated.

---

## 1. The 10 Competitors / Peers (summary table)

| # | Competitor | Category | What it does (one line) | Software shape | ONE thing CSOAI could adopt |
|---|---|---|---|---|---|
| 1 | **Sigstore** (Rekor + Cosign + Fulcio) | Rekor/Sigstore — transparency log | Keyless signing of software artifacts + an append-only public log of every signature | Go binaries: `cosign`, `rekor-cli`, `rekor-server`; REST API; Apache-2.0 | Show a **log-inclusion proof** (signed entry + Merkle proof), not just a bare hash |
| 2 | **OpenTimestamps** | Bitcoin timestamping (trustless) | Commits data hashes into the Bitcoin blockchain via Merkle aggregation; anyone can verify without trusting a server | Python CLI (`ots`), calendar servers, `.ots` receipt; Bitcoin as anchor | Display the **anchor path** — calendar → Bitcoin tx id → block height |
| 3 | **Arweave** | Permanent storage (blockweave) | Pay-once, store-forever on a "blockweave"; miners must recall random prior blocks (replication incentive) | Permaweb HTTP gateway, Arweave node (Erlang), AR token, ArNS naming | **Pay-once endowment** → commit each card hash with a guaranteed minimum retention promise |
| 4 | **IPFS** | Content addressing (not a ledger) | Files addressed by CID (hash of content); immutable content, mutable names via IPNS; permanence only when pinned | Kubo (Go daemon), HTTP RPC + gateway, CIDv1, IPNS | **Content addressing** — anchor by CID so any byte change changes the identifier |
| 5 | **Hedera Consensus Service (HCS)** | Consensus / ordering | Public aBFT hashgraph that timestamps + orders submitted messages (hashes) with a running hash chain | Hiero consensus nodes (open source), SDKs (JS/Java/Go), topic submit/subscribe | **Fair-ordered consensus timestamp + running hash + sequence number** per record |
| 6 | **SCITT** (RFC 9943) | Supply-chain claims ledger (IETF std) | Standard architecture: append-only ledger of signed "claims" + countersigned "receipts" | Standards (RFC + I-D), language-agnostic reference APIs (scrapi) | **Claim + Receipt separation** — emit a machine-readable inclusion receipt per record |
| 7 | **ProvenDB** | Provenance-ledger product | MongoDB-compatible DB where every document version is hash-anchored to a blockchain | DBaaS + API (Southbank Software), SDKs, blockchain anchors | **Version-anchored history** — expose per-record version chain with hashes |
| 8 | **CodeNotary immudb** (`immudb` + `vcn`) | Attestation-ledger SaaS | Tamperproof immutable DB (KV/SQL/document) with Merkle proofs + `vcn` artifact attestation | Go server (`immudb`), SDKs, `vcn` CLI, CodeNotary ledger SaaS | **Continuous attestation** — live trust/untrust status + re-attestation, not a one-time hash |
| 9 | **OriginStamp** | Anchor (BTCTimestamp) SaaS | Aggregates thousands of hashes into one Merkle root anchored to Bitcoin; issues timestamp certificates | REST API + web app, SDKs, certificate PDFs, multi-chain anchors | **Submit-hash → get-cert** one-click UX with a shareable certificate link |
| 10 | **Guardtime KSI** | Tamper-evident logging (keyless) | Keyless Signature Infrastructure: hashes folded into a global Merkle tree; integrity + time without private keys | C/C++ `libksi`, KSI gateway/aggregator, HSM integration, on-prem/SaaS | **Keyless timestamp** — time proven by inclusion in a *published* global root hash (no key to expire) |

*Notable mention (not counted in the 10):* **Google Trillian** — the verifiable, transparent Merkle-tree log underlying Certificate Transparency and a reference model for Rekor/SCITT-style ledgers ([google.github.io/trillian](https://google.github.io/trillian/)). Relevant if CSOAI wants a self-hosted log rather than a public chain.

---

## 2. Per-competitor detail (verified)

### 1. Sigstore (Rekor / Cosign / Fulcio)
- **What it does:** Free, open-source signing + transparency service for software supply chains. `cosign` signs artifacts; `fulcio` issues short-lived (10-minute) *keyless* certificates bound to an OIDC identity (GitHub, Google, etc.); `rekor` is the public, append-only transparency log of every signature.
- **User flow:** `cosign sign <image>` → Fulcio issues an ephemeral cert from your OIDC identity → signature + cert are appended to the Rekor log → `cosign verify <image>` checks signature validity *and* log inclusion.
- **Docs:** [docs.sigstore.dev](https://docs.sigstore.dev/about/security/), [github.com/sigstore/rekor](https://github.com/sigstore/rekor)
- **Software shape:** Go CLI + server binaries, REST API, Merkle-tree log, Apache-2.0. Rekor's log is public and queryable (`rekor-cli search`).
- **Adopt for Continuity UI:** the "chain-verify input" should return a **transparency-log inclusion proof** (the signed log entry + its Merkle/consistency proof), so verification does not require trusting CSOAI's own database.

### 2. OpenTimestamps
- **What it does:** Trustless, scalable, distributed timestamping. It commits a hash of your data into the Bitcoin blockchain through Merkle aggregation — verifiable *without trusting the OTS servers or a third-party clock*.
- **User flow:** `ots stamp file` → the hash goes to calendar servers, which aggregate many hashes and commit a single Merkle root into a Bitcoin transaction → you receive a `.ots` receipt → `ots verify file receipt.ots` proves existence at that time.
- **Docs:** [opentimestamps.org](https://opentimestamps.org), [github.com/opentimestamps](https://github.com/opentimestamps)
- **Software shape:** Python CLI (`ots`), calendar servers, `.ots` receipt format; Bitcoin is the trust anchor.
- **Adopt for Continuity UI:** show the **full anchor path** — calendar aggregation → Bitcoin transaction id → block height — so a user can independently confirm "this was anchored at block N" in a public explorer.

### 3. Arweave
- **What it does:** "Pay once, store forever" permanent storage on a *blockweave*. Miners must prove they can recall random previous blocks (Proof of Access), creating a replication incentive. Permanence is **economic** (an endowment funds ~200 years of storage), not a cryptographic guarantee.
- **User flow:** upload data (directly or via a bundler such as Irys) → pay AR tokens as a storage endowment → transaction is mined into the weave → retrieve by transaction id via a gateway.
- **Docs:** [docs.arweave.org](https://docs.arweave.org/developers/development/overview.md), [arweave.com](https://www.arweave.com/blog/permanent-storage-on-arweave)
- **Software shape:** permaweb HTTP gateway, Arweave node (Erlang), AR token, ArNS (Arweave Name System).
- **Adopt for Continuity UI:** the **endowment model** — CSOAI could price each benchmark card's anchor as a one-time "permanent retention" commitment, and surface "guaranteed retained until <date>" instead of an unspecified blob.

### 4. IPFS
- **What it does:** Content-addressed P2P storage. A file is addressed by its **CID** (hash of the content), so identical content has one address and any byte change yields a different address. IPFS *itself is not a ledger and does not guarantee permanence* — data persists only while pinned.
- **User flow:** `ipfs add file` → returns a CID → `ipfs get <CID>` retrieves it → "pin" to keep it alive; HTTP gateways serve CIDs in the browser.
- **Docs:** [docs.ipfs.tech](https://docs.ipfs.tech), [github.com/ipfs/kubo](https://github.com/ipfs/kubo)
- **Software shape:** Kubo (Go daemon), HTTP RPC + public gateways, CIDv1, IPNS for mutable names.
- **Adopt for Continuity UI:** reference every record by **content address (CID)** so integrity is self-evident — the identifier *is* the hash, and a mismatch cannot be silently ignored.

### 5. Hedera Consensus Service (HCS)
- **What it does:** A public asynchronous-Byzantine-fault-tolerant (aBFT) *hashgraph* network. HCS provides **consensus timestamping and fair ordering** of submitted messages/hashes (it stores order, not the data itself). Each message gets a consensus timestamp, a sequence number, and joins a **running SHA-384 hash chain**.
- **User flow:** create a topic → `submitMessage` (the message or a hash) → receive consensus timestamp + sequence number + running hash → query the topic to prove ordering/timing.
- **Docs:** [hedera.com/service/consensus-service](https://hedera.com/service/consensus-service/), [github.com/hiero-ledger/hiero-consensus-node](https://github.com/hiero-ledger/hiero-consensus-node)
- **Software shape:** open-source consensus nodes (now under the **Hiero** project), SDKs (JS/Java/Go), topic/submit/subscribe API.
- **Adopt for Continuity UI:** the **running hash + monotonic sequence number** pattern — every Continuity event shows a chainable `prevHash → thisHash` plus a sequence number, making order and continuity provable at a glance.

### 6. SCITT (RFC 9943)
- **What it does:** The IETF standard architecture for Supply Chain Integrity, Transparency, and Trust. A **Transparency Service** maintains an append-only ledger of signed **Claims** and returns a **Receipt** (a countersigned inclusion proof) to the submitter; verifiers check the receipt against the ledger.
- **User flow:** Issuer submits a signed Claim → the Transparency Service registers it and returns a Receipt → a Verifier later checks the Receipt + Claim against the ledger without needing the issuer online.
- **Docs:** [RFC 9943](https://www.rfc-editor.org/rfc/rfc9943) (architecture), [draft-ietf-scitt-scrapi](https://www.ietf.org/archive/id/draft-ietf-scitt-scrapi-09.html) (Reference APIs, now at Proposed Standard).
- **Software shape:** language-agnostic standards + reference APIs; multiple implementations; designed for cross-vendor interoperability.
- **Adopt for Continuity UI:** the **Claim + Receipt** split — every Continuity record should produce a downloadable, machine-readable receipt (signed inclusion proof) independent of the human-readable text, exactly as SCITT mandates.

### 7. ProvenDB
- **What it does:** A blockchain-anchored, MongoDB-compatible document database. Every version of every document is hashed and anchored to a blockchain (e.g., Hedera), producing provable provenance, immutable version history, and proof of existence.
- **User flow:** store JSON documents through a MongoDB-compatible API → each write is versioned and hash-anchored to a blockchain → retrieve a version's proof / full history → verify in an explorer.
- **Docs:** [provendb.com](https://provendb.com), [github.com/SouthbankSoftware](https://github.com/SouthbankSoftware) (incl. `provenlogs`)
- **Software shape:** DBaaS + API from Southbank Software, SDKs, blockchain anchors; MongoDB wire-compatible.
- **Adopt for Continuity UI:** **version-anchored history** — expose each record's full hash-chained version list, so users can click into "who changed what, when, and what it was anchored to."

### 8. CodeNotary immudb (immudb + vcn)
- **What it does:** An open-source, zero-trust **tamperproof immutable database** (key-value / SQL / document) where every entry is hashed and Merkle-chained, enabling verifiable history. Companion tool `vcn` **notarizes** files/artifacts against a trust chain, returning a signed attestation with status (`TRUSTED` / `UNTRUSTED` / `UNSUPPORTED`).
- **User flow:** store data (KV/SQL) → entries get hashes provable via Merkle consistency proofs → `vcn notarize <artifact>` returns a signed attestation → `vcn verify <artifact>` re-checks it later.
- **Docs:** [immudb.io](https://immudb.io), [github.com/codenotary/immudb](https://github.com/codenotary/immudb), [docs.codenotary.com](https://docs.codenotary.com)
- **Software shape:** Go server (`immudb`), SDKs, `vcn` CLI, CodeNotary ledger SaaS; recently added PostgreSQL-compatible immutable audit trails.
- **Adopt for Continuity UI:** **continuous attestation** — a live status line ("attested / unverified / untrusted") plus scheduled re-attestation, instead of a one-shot hash printed once.

### 9. OriginStamp
- **What it does:** A blockchain timestamping SaaS ("Anchor / BTCTimestamp" class). It aggregates thousands of submitted hashes into a single Merkle root and anchors it into the Bitcoin blockchain (plus other chains), issuing a tamper-proof **timestamp certificate** with an independent proof.
- **User flow:** submit a file or hash (web app or REST API) → hashes are aggregated → the Merkle root is anchored to a Bitcoin transaction → you receive a certificate (PDF) + proof → verify via public tools.
- **Docs:** [originstamp.com](https://originstamp.com/en/timestamp), [docs.originstamp.com](https://docs.originstamp.com)
- **Software shape:** REST API + web app, SDKs (JS/Python/etc.), certificate PDFs, multi-chain anchors.
- **Adopt for Continuity UI:** the **submit-hash → get-certificate** one-click flow — a "Anchor to Bitcoin" button that returns a shareable, independently verifiable certificate link.

### 10. Guardtime KSI
- **What it does:** **Keyless Signature Infrastructure (KSI) blockchain.** Data hashes are folded into a globally distributed Merkle tree; a KSI signature proves *integrity and time* without any private key that can expire or be compromised. Deployed in Estonia's e-government, healthcare, and defence contexts.
- **User flow:** hash data → the KSI service aggregates it into the global hash tree → returns a KSI signature (root hash + proof path, the root being **published** in media and a blockchain) → verify against the published root.
- **Docs:** [guardtime.com](https://guardtime.com), KSI white paper ([ePrint 2013/834](https://eprint.iacr.org/archive/2013/834/1387220873.pdf))
- **Software shape:** C/C++ library (`libksi`), KSI gateway/aggregator services, HSM integration, on-prem + SaaS.
- **Adopt for Continuity UI:** the **keyless, published-root timestamp** — time is proven by inclusion in a *publicly published* root hash (no key to rotate), which fits CSOAI's "neutral, no central secret" posture.

---

## 3. What CSOAI should adopt — 5 concrete improvements for the AG UI Continuity chat window

> Themes requested: **chain-verify input**, **anchor status**, **re-attestation scheduling**. The five below cover those three plus the two highest-value patterns from the peer set (receipt-first output; running-hash + sequence).

1. **Chain-verify input box (from Sigstore/Rekor + SCITT).**
   Add a "Verify" field where a user pastes a card id, hash, or receipt. The UI recomputes the hash and walks the chain backwards, checking `prevHash === hash(previous record)` at every link, and renders a green check / red break per link — *plus* an inclusion proof (log entry + Merkle path) so verification does not depend on trusting CSOAI's own store. This is the Rekor "verify against the public log" behavior and the SCITT "check the Receipt against the ledger" behavior.

2. **Anchor-status badge with a visible anchor path (from OpenTimestamps + OriginStamp).**
   Every record shows an "anchor status" line: `Unanchored` → `Queued` → `Anchored`, and once anchored, the *path* is shown (`calendar → Bitcoin tx <id> → block <height>`), so a user can independently confirm in a public explorer. This converts "we say it's anchored" into "here is where it is anchored."

3. **Re-attestation scheduling control (from CodeNotary vcn / immudb).**
   Add a schedule + status for ongoing re-attestation: interval selector (e.g., hourly / daily / per epoch), "last attested <time>", "next attestation <time>", and an "Attest now" button. Model the live status on `vcn`'s `TRUSTED / UNTRUSTED / UNSUPPORTED`, so a record can *fall out* of attestation visibly rather than being trusted forever.

4. **Receipt-first output — emit a machine-readable receipt per event (from SCITT + OpenTimestamps).**
   Every Continuity event writes two artifacts side by side: the human-readable text *and* a downloadable, signed, machine-readable **receipt** (inclusion proof / Merkle path / `.ots`-style file). One-click copy/download. This makes every record independently verifiable offline, which is the core SCITT Claim+Receipt contract.

5. **Running-hash + sequence header (from Hedera HCS).**
   Put a monotonic **sequence number** and a **running hash chain** in the Continuity window header: each event displays `#N · prev <short-hash> → this <short-hash>`, following the HCS "sequence number + running SHA-384 hash" pattern. Continuity becomes self-evident and re-orderings/omissions are immediately visible to the user, and the chain can be anchored periodically (tie-in to #2 and #3).

---

## Source index (verified)
- Sigstore security model: https://docs.sigstore.dev/about/security/ · Rekor repo: https://github.com/sigstore/rekor
- OpenTimestamps: https://opentimestamps.org · Wikipedia: https://en.wikipedia.org/wiki/OpenTimestamps
- Arweave permanent storage: https://www.arweave.com/blog/permanent-storage-on-arweave · docs: https://docs.arweave.org
- IPFS/Kubo: https://docs.ipfs.tech · https://github.com/ipfs/kubo · pinning: https://docs.pinata.cloud/ipfs-101/what-is-ipfs
- Hedera HCS: https://hedera.com/service/consensus-service/ · Hiero consensus node: https://github.com/hiero-ledger/hiero-consensus-node
- SCITT: RFC 9943 https://www.rfc-editor.org/rfc/rfc9943 · Reference APIs draft-ietf-scitt-scrapi: https://datatracker.ietf.org/doc/draft-ietf-scitt-scrapi/
- ProvenDB: https://provendb.com · https://github.com/SouthbankSoftware
- immudb: https://immudb.io · https://github.com/codenotary/immudb · CodeNotary docs: https://docs.codenotary.com
- OriginStamp: https://originstamp.com/en/timestamp · https://docs.originstamp.com
- Guardtime KSI: https://guardtime.com · white paper: https://eprint.iacr.org/archive/2013/834/1387220873.pdf
- Trillian (notable mention): https://google.github.io/trillian/
