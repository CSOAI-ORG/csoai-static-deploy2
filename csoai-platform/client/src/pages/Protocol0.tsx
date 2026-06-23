import { useState } from "react";
import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";

export default function Protocol0Page() {
  const [sigilResult, setSigilResult] = useState<any>(null);
  const [didInput, setDidInput] = useState("did:sigil:example");
  const [didDoc, setDidDoc] = useState<any>(null);
  const [message, setMessage] = useState("hello protocol 0");
  const [signature, setSignature] = useState("");
  const [publicKey, setPublicKey] = useState("");
  const [verifyResult, setVerifyResult] = useState<any>(null);
  const [agentCard, setAgentCard] = useState<any>(null);
  const [envelopeResult, setEnvelopeResult] = useState<any>(null);

  const createSigil = trpc.protocol0.identity.createSigil.useMutation({
    onSuccess: setSigilResult,
  });
  const resolveDid = trpc.protocol0.identity.resolveDid.useQuery(
    { did: didInput },
    { enabled: false },
  );
  const verifySignature = trpc.protocol0.identity.verifySignature.useMutation({
    onSuccess: setVerifyResult,
  });
  const agentCardQuery = trpc.protocol0.discovery.agentCard.useQuery(undefined, {
    enabled: false,
  });
  const sendEnvelope = trpc.protocol0.communication.sendEnvelope.useMutation({
    onSuccess: setEnvelopeResult,
  });

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="mx-auto max-w-5xl space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Protocol 0 Tools</h1>
          <p className="text-muted-foreground">
            Agent-native identity, discovery, messaging, trust, transaction, and governance endpoints.
          </p>
        </div>

        <Tabs defaultValue="identity">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="identity">Identity</TabsTrigger>
            <TabsTrigger value="discovery">Discovery</TabsTrigger>
            <TabsTrigger value="messaging">Messaging</TabsTrigger>
            <TabsTrigger value="governance">Governance</TabsTrigger>
          </TabsList>

          <TabsContent value="identity" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Create Sigil</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button onClick={() => createSigil.mutate({})}>Generate Ed25519 Sigil</Button>
                {sigilResult && (
                  <pre className="rounded-md bg-muted p-4 text-xs overflow-auto">
                    {JSON.stringify(sigilResult, null, 2)}
                  </pre>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Resolve DID</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Input value={didInput} onChange={(e) => setDidInput(e.target.value)} />
                  <Button onClick={() => resolveDid.refetch().then((r) => setDidDoc(r.data))}>
                    Resolve
                  </Button>
                </div>
                {didDoc && (
                  <pre className="rounded-md bg-muted p-4 text-xs overflow-auto">
                    {JSON.stringify(didDoc, null, 2)}
                  </pre>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Verify Signature</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-2">
                  <Label>Message</Label>
                  <Input value={message} onChange={(e) => setMessage(e.target.value)} />
                </div>
                <div className="grid gap-2">
                  <Label>Signature (base64url)</Label>
                  <Input value={signature} onChange={(e) => setSignature(e.target.value)} />
                </div>
                <div className="grid gap-2">
                  <Label>Public Key (base64url)</Label>
                  <Input value={publicKey} onChange={(e) => setPublicKey(e.target.value)} />
                </div>
                <Button
                  onClick={() =>
                    verifySignature.mutate({ message, signature, publicKey })
                  }
                >
                  Verify
                </Button>
                {verifyResult && (
                  <Badge variant={verifyResult.valid ? "default" : "destructive"}>
                    {verifyResult.valid ? "Valid" : "Invalid"}
                  </Badge>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="discovery" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>A2A Agent Card</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button onClick={() => agentCardQuery.refetch().then((r) => setAgentCard(r.data))}>
                  Fetch Agent Card
                </Button>
                {agentCard && (
                  <pre className="rounded-md bg-muted p-4 text-xs overflow-auto">
                    {JSON.stringify(agentCard, null, 2)}
                  </pre>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="messaging" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Send Protocol 0 Envelope</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button
                  onClick={() =>
                    sendEnvelope.mutate({
                      envelope: {
                        version: "0.1.0",
                        messageId: crypto.randomUUID(),
                        sender: "did:sigil:sender123",
                        recipient: "did:sigil:recipient456",
                        timestamp: new Date().toISOString(),
                        type: "HELLO",
                        payload: { note: "test envelope" },
                      },
                      signature: "test-signature-stub",
                    })
                  }
                >
                  Send Test Envelope
                </Button>
                {envelopeResult && (
                  <pre className="rounded-md bg-muted p-4 text-xs overflow-auto">
                    {JSON.stringify(envelopeResult, null, 2)}
                  </pre>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="governance" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Submit Signed Vote</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Use the <code>protocol0.governance.submitVote</code> mutation to cast a
                  cryptographically signed vote. Wire it to a real proposal flow to finish the
                  integration.
                </p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
