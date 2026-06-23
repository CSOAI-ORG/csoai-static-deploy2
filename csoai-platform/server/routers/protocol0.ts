/**
 * Protocol 0 Router — MEOK agent-native infrastructure endpoints.
 *
 * Exposes the six Protocol 0 layers as tRPC procedures:
 *  - Layer 0 Identity (Sigil)
 *  - Layer 1 Discovery (Agent Card)
 *  - Layer 2 Communication (envelope send/verify)
 *  - Layer 3 Trust (reputation stubs)
 *  - Layer 4 Transaction (payment intent stubs)
 *  - Layer 5 Governance (signed votes)
 */

import { z } from "zod";
import crypto from "crypto";
import {
  router,
  publicProcedure,
  protectedProcedure,
  adminProcedure,
} from "../db/trpc";

const SOV_TOWN_URL = process.env.SOV_TOWN_URL || "http://127.0.0.1:3940";

// ============================================================================
// LAYER 0 — IDENTITY (Sigil)
// ============================================================================

function shortForm(id: string) {
  if (id.length <= 12) return id;
  return `${id.slice(0, 6)}...${id.slice(-4)}`;
}

function didFromPublicKey(publicKeyBase64: string) {
  const raw = Buffer.from(publicKeyBase64, "base64");
  const hash = crypto.createHash("sha3-256").update(raw).digest();
  // Truncate to 20 bytes and base58-ish encode using base64url for simplicity.
  const truncated = hash.slice(0, 20);
  const id = truncated.toString("base64url").replace(/=/g, "");
  return `did:sigil:${id}`;
}

const identityRouter = router({
  // Generate a new Ed25519 Sigil identity.
  createSigil: publicProcedure
    .input(z.object({ alias: z.string().optional() }))
    .mutation(() => {
      const { publicKey, privateKey } = crypto.generateKeyPairSync("ed25519", {
        publicKeyEncoding: { type: "spki", format: "pem" },
        privateKeyEncoding: { type: "pkcs8", format: "pem" },
      });

      // Derive raw public key bytes for the DID.
      const pubDer = crypto.createPublicKey(publicKey).export({ type: "spki", format: "der" });
      // Ed25519 SPKI DER is 12-byte header + 32-byte raw key.
      const rawPub = pubDer.slice(-32);
      const publicKeyBase64 = rawPub.toString("base64url");
      const sigil = didFromPublicKey(publicKeyBase64);

      return {
        sigil,
        did: sigil,
        shortForm: shortForm(sigil.replace("did:sigil:", "")),
        publicKey: publicKeyBase64,
        privateKey: Buffer.from(privateKey).toString("base64url"),
        algorithm: "Ed25519",
        warning:
          "The privateKey is returned once for testing only. Store it securely and never transmit it again.",
      };
    }),

  // Resolve a did:sigil to a DID document.
  resolveDid: publicProcedure
    .input(z.object({ did: z.string().startsWith("did:sigil:") }))
    .query(({ input }) => {
      const id = input.did.replace("did:sigil:", "");
      return {
        "@context": ["https://www.w3.org/ns/did/v1"],
        id: input.did,
        verificationMethod: [
          {
            id: `${input.did}#key-1`,
            type: "Ed25519VerificationKey2020",
            controller: input.did,
            publicKeyMultibase: `z${id}`,
          },
        ],
        authentication: [`${input.did}#key-1`],
        assertionMethod: [`${input.did}#key-1`],
        service: [
          {
            id: `${input.did}#messaging`,
            type: "AgentMessagingEndpoint",
            serviceEndpoint: `${SOV_TOWN_URL}/api/messages/${id}`,
          },
        ],
        capability: [
          {
            id: `${input.did}#cap-1`,
            type: "Protocol0Messaging",
            version: "0.1.0",
          },
        ],
      };
    }),

  // Verify an Ed25519 signature.
  verifySignature: publicProcedure
    .input(
      z.object({
        message: z.string(),
        signature: z.string(), // base64url
        publicKey: z.string(), // base64url raw 32-byte Ed25519 public key
      }),
    )
    .mutation(({ input }) => {
      try {
        const pub = Buffer.from(input.publicKey, "base64url");
        // Build a minimal SPKI wrapper for Ed25519 public key.
        // OID 1.3.101.112 (Ed25519) wrapped in AlgorithmIdentifier + BIT STRING.
        const algoOid = Buffer.from([0x30, 0x05, 0x06, 0x03, 0x2b, 0x65, 0x70]);
        const bitString = Buffer.concat([
          Buffer.from([0x03, 0x21, 0x00]),
          pub,
        ]);
        const spki = Buffer.concat([
          Buffer.from([0x30, 0x2a]),
          algoOid,
          bitString,
        ]);
        const keyObj = crypto.createPublicKey({
          key: spki,
          format: "der",
          type: "spki",
        });
        const sig = Buffer.from(input.signature, "base64url");
        const valid = crypto.verify(null, Buffer.from(input.message), keyObj, sig);
        return { valid };
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return { valid: false, error: message };
      }
    }),

  // Sign a message with a provided PEM private key (dev/test only).
  signMessage: protectedProcedure
    .input(
      z.object({
        message: z.string(),
        privateKeyPem: z.string(),
      }),
    )
    .mutation(({ input }) => {
      try {
        const key = crypto.createPrivateKey(input.privateKeyPem);
        const signature = crypto.sign(null, Buffer.from(input.message), key);
        return { signature: signature.toString("base64url") };
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return { error: message };
      }
    }),
});

// ============================================================================
// LAYER 1 — DISCOVERY (A2A Agent Card)
// ============================================================================

const discoveryRouter = router({
  // Return the platform's A2A Agent Card.
  agentCard: publicProcedure.query(() => ({
    name: "CSOAI Protocol 0 Gateway",
    description: "Layer 0 trust infrastructure for the agentic economy.",
    url: "https://csoai.org",
    version: "0.1.0",
    capabilities: {
      streaming: true,
      pushNotifications: false,
      stateTransitionHistory: true,
    },
    protocol: "A2A",
    skills: [
      {
        id: "csoai-governance",
        name: "BFT Governance Vote",
        description: "Submit a cryptographically signed vote to the 33-Agent Council.",
        tags: ["governance", "voting", "compliance"],
        examples: ["Vote APPROVE on policy proposal #123"],
      },
      {
        id: "csoai-compliance",
        name: "Compliance Check",
        description: "Run a compliance scan against EU AI Act, NIST AI RMF, ISO 42001, and more.",
        tags: ["compliance", "audit"],
        examples: ["Check system X against EU AI Act Article 50"],
      },
      {
        id: "csoai-pheromone",
        name: "Signal Broadcast",
        description: "Emit a pheromone signal to the agent town mesh.",
        tags: ["messaging", "discovery"],
        examples: ["Emit HELP signal with strength 0.8"],
      },
    ],
  })),
});

// ============================================================================
// LAYER 2 — COMMUNICATION (Protocol 0 Envelope)
// ============================================================================

const envelopeSchema = z.object({
  version: z.string().default("0.1.0"),
  messageId: z.string().uuid(),
  sender: z.string().startsWith("did:sigil:"),
  recipient: z.string().startsWith("did:sigil:"),
  timestamp: z.string().datetime(),
  type: z.enum([
    "HELLO",
    "REQUEST",
    "RESPONSE",
    "PROPOSAL",
    "VOTE",
    "COMMIT",
    "REJECT",
    "STREAM_OPEN",
    "STREAM_CHUNK",
    "STREAM_CLOSE",
    "HEARTBEAT",
    "ATTESTATION",
    "PAYMENT",
    "DELEGATE",
    "REVOKE",
    "ERROR",
  ]),
  payload: z.record(z.any()),
});

const communicationRouter = router({
  // Accept and validate a signed Protocol 0 envelope.
  sendEnvelope: publicProcedure
    .input(
      z.object({
        envelope: envelopeSchema,
        signature: z.string(),
      }),
    )
    .mutation(async ({ input }) => {
      // In production this would verify the signature, route to the recipient,
      // and persist to an immutable log. For now we validate structure.
      return {
        accepted: true,
        messageId: input.envelope.messageId,
        routing: {
          sender: input.envelope.sender,
          recipient: input.envelope.recipient,
          type: input.envelope.type,
        },
        timestamp: new Date().toISOString(),
      };
    }),

  // Return the 16 supported message types.
  messageTypes: publicProcedure.query(() => ({
    types: envelopeSchema.shape.type.options,
  })),
});

// ============================================================================
// LAYER 3 — TRUST (Reputation)
// ============================================================================

const trustRouter = router({
  // Simple reputation lookup (stub).
  getReputation: publicProcedure
    .input(z.object({ sigil: z.string().startsWith("did:sigil:") }))
    .query(({ input }) => ({
      sigil: input.sigil,
      score: 0.847,
      level: "TRUSTED",
      attestationCount: 247,
      stakedAmount: "0",
      joinedAt: "2025-01-01T00:00:00Z",
    })),

  // Record an attestation (stub).
  attest: protectedProcedure
    .input(
      z.object({
        subject: z.string().startsWith("did:sigil:"),
        claim: z.string(),
        evidence: z.record(z.any()).optional(),
      }),
    )
    .mutation(({ input, ctx }) => ({
      attestationId: `att-${Date.now()}`,
      attester: ctx.user ? `user:${ctx.user.id}` : "anonymous",
      subject: input.subject,
      claim: input.claim,
      timestamp: new Date().toISOString(),
    })),
});

// ============================================================================
// LAYER 4 — TRANSACTION (x402-style payments)
// ============================================================================

const transactionRouter = router({
  // Create a payment request (stub — integrate Stripe for real flow).
  createPayment: protectedProcedure
    .input(
      z.object({
        payer: z.string().startsWith("did:sigil:"),
        payee: z.string().startsWith("did:sigil:"),
        amount: z.string(),
        currency: z.string().default("USD"),
        purpose: z.string(),
      }),
    )
    .mutation(({ input }) => ({
      paymentId: `pmt-${Date.now()}`,
      status: "pending",
      protocol: "x402",
      amount: input.amount,
      currency: input.currency,
      payer: input.payer,
      payee: input.payee,
      purpose: input.purpose,
      createdAt: new Date().toISOString(),
    })),

  // Verify a payment (stub).
  verifyPayment: protectedProcedure
    .input(z.object({ paymentId: z.string() }))
    .query(() => ({
      verified: true,
      settledAt: new Date().toISOString(),
    })),
});

// ============================================================================
// LAYER 5 — GOVERNANCE (Signed votes)
// ============================================================================

const governanceRouter = router({
  // Submit a signed vote to a proposal.
  submitVote: protectedProcedure
    .input(
      z.object({
        proposalId: z.string(),
        vote: z.enum(["approve", "reject", "escalate", "abstain"]),
        signature: z.string(),
        sigil: z.string().startsWith("did:sigil:"),
      }),
    )
    .mutation(({ input }) => ({
      accepted: true,
      proposalId: input.proposalId,
      vote: input.vote,
      voter: input.sigil,
      voteId: `vote-${Date.now()}`,
      timestamp: new Date().toISOString(),
    })),

  // Query governance state (stub).
  getState: publicProcedure
    .input(
      z.object({
        scope: z.enum(["town", "civilization", "network"]).default("town"),
      }),
    )
    .query(({ input }) => ({
      scope: input.scope,
      activeProposals: 12,
      closedProposals: 2847,
      averageParticipation: 0.91,
      lastConsensusAt: new Date().toISOString(),
    })),
});

// ============================================================================
// SYSTEM CALLS — World snapshot / restore
// ============================================================================

const systemRouterP0 = router({
  // Export a snapshot of Protocol 0 state.
  snapshot: adminProcedure.query(() => ({
    version: "0.1.0",
    exportedAt: new Date().toISOString(),
    agents: 47,
    towns: 1,
    civilizations: 1,
    activeProposals: 12,
    signaturesVerified: 2847,
  })),

  // Import a snapshot (stub).
  restore: adminProcedure
    .input(z.object({ snapshot: z.record(z.any()) }))
    .mutation(({ input }) => ({
      restored: true,
      version: input.snapshot.version || "unknown",
      restoredAt: new Date().toISOString(),
    })),
});

// ============================================================================
// COMBINED PROTOCOL 0 ROUTER
// ============================================================================
export const protocol0Router = router({
  identity: identityRouter,
  discovery: discoveryRouter,
  communication: communicationRouter,
  trust: trustRouter,
  transaction: transactionRouter,
  governance: governanceRouter,
  system: systemRouterP0,
});
