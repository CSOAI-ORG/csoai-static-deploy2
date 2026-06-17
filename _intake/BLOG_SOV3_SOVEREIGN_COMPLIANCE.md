# Sovereign AI compliance — why your attestation should be signed, not just asserted

**Meta description:** Ed25519-signed compliance attestations enable offline verification of AI system claims. The difference between saying you are compliant and proving it — without a server call.

---

Every AI company I talk to claims they are compliant. "We follow the EU AI Act." "Our training data is clean." "We respect opt-outs." They put it on a webpage, maybe in a PDF, and call it a day.

Here is the problem: an unsigned assertion has zero cryptographic weight. It is a string of bytes that anyone could have written. If a regulator, a customer, or an auditor asks you to prove you were complaint on a specific date for a specific model version, a PDF on your website is not proof. It is a claim.

The difference between a claim and proof is a signature.

## The attestation model

A compliance attestation is a structured document that states: on this date, for this model version (identified by its hash), with this training data inventory (identified by its hash), the following transparency obligations were met. It includes the model card, the training data summary, the risk assessment reference, and the watermarking methodology used.

That document becomes evidence when two things are true:

1. It is **cryptographically signed** by the entity making the claim.
2. The signature can be **verified offline** by any third party without calling home.

This is not complicated. Ed25519 signatures are a well-known, battle-tested elliptic curve scheme. The signing key is held by the organisation. The verification key is published — in DNS, in a GitHub repository, in a public key server, in a QR code on a business card. Anyone with the message and the signature can verify it using the public key. No server. No API call. No recurring cost.

The attestation document itself is a plain-text or JSON record. Sign it with Ed25519. Publish the signed attestation alongside the public key. The chain of trust is:

- Message: the compliance attestation text (date, model hash, data hash, obligations met)
- Signature: Ed25519 signature over that message
- Verification: anyone with the public key can confirm the message was signed by the holder of the private key
- Trust anchor: the public key is bound to your organisation through DNS, a published keybase profile, or a hardware security module attestation

## Why this matters right now

The EU Code of Practice finalises this month. Article 50 enforces in 47 days. Both require you to publish transparency documentation. Neither specifies the format — yet.

If you ship a plain-text transparency report, you have done the minimum. If you ship an Ed25519-signed compliance attestation with an offline-verifiable chain, you have done something qualitatively different: you have given every regulator, customer, and competitor the ability to verify your claim without asking your permission.

This matters for three specific reasons:

**Regulatory audits.** When the EU AI Act enforcement bodies start conducting audits, they will go through a prioritisation queue. Companies with signed, verifiable attestations demonstrate operational maturity. Companies with PDFs on a /static/compliance page demonstrate compliance theatre. Which one do you think gets audited first?

**Customer procurement.** If you sell AI services to enterprises, your compliance documentation goes through procurement review. A signed attestation with an independent verification path removes friction. The procurement team can verify your claims without scheduling a call. That saves weeks in the sales cycle.

**Public accountability.** Signed attestations are timestamp-verifiable. If someone later claims your training data violated copyright, your signed attestation from the deployment date shows what you claimed, when you claimed it, and that you claimed it under your organisational key. That is an evidence chain, not a press release.

## How to start

The practical steps are:

1. Generate an Ed25519 key pair. Store the private key in a hardware security module or encrypted offline storage — not in a text file on your build server.

2. Publish the public key in a discoverable location: a `/.well-known/ai-compliance.asc` endpoint on your domain is the simplest option. Add a DNSSEC-signed TXT record as a secondary anchor.

3. Define your attestation document schema: date, model version hash (SHA-256 of the model weights), training data root hash (Merkle tree of your dataset inventory), Code of Practice obligations met, Article 50 transparency items, watermarking methodology deployed.

4. Sign each release. Automate it in your CI/CD pipeline. The attestation is generated, signed by a key held in your deployment secrets infrastructure, and published alongside the model.

5. Verify it. Use `openssl` or `ssh-keygen` or any Ed25519 library to confirm your own pipeline produces verifiable signatures. Then publish a verification script so anyone can run it.

Sovereign compliance means you control your evidence chain. A signed attestation is better than an assertion because it converts a marketing claim into a cryptographic fact. In the 47 days before the Article 50 cliff, that is the difference between being ready and being exposed.
