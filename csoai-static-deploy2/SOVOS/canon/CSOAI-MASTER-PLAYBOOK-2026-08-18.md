# CSO AI — THE MASTER PLAYBOOK
**One year of Council of AI · consolidated 2026-08-18**
**Mined from full canon. The two-track build, the visual OS, and everything settled today.**

> Registers: REAL / LANE-REAL / DEMO / DESIGNED / GATED / THEORY / KILLED.
> Two firewalls stand. (1) Council measures — never certifies, endorses, or builds what it measures. (2) May analyse arena outcomes — never train + ship a Council-owned champion on arena honey.
> Naming lock: internal codenames never ship publicly (Sovos live TM). Public: Council of AI / GSPC / MEOK.
> Design Law 1 governs all: the verdict comes from a deterministic predicate, never a vote, never a model.

---

## 0 — THE ONE-SENTENCE THESIS

A recurring, self-improving, signed measurement engine that runs daily across every AI benchmark, regulation, and human baseline — with a character on the front that any person or agent can talk to, on any platform, and every action receipted.

Two tracks that feel separate and are one product:
- **Track 1 — the engine.** The recurring data business. The coliseum. The index.
- **Track 2 — the aperture.** The character, the visual OS, the copy-paste gap closed.

Without the engine the character has nothing real to say. Without the character the engine has no face and no distribution. **The receipts connect them — every action goes through the engine and comes back signed. That is the thing nobody else has.**

---

## 1 — THE ARCHITECTURE THAT SURVIVES AUDIT

The order a technical reviewer checks it. Strip the mythology; this is what's defensible.

```
ANCHOR      417 frozen statutory provisions, corpus-hashed (sha256 per provision)
            Every score resolves to frozen law. Months of legal work.
   |
INSTRUMENT  5 deterministic predicates. NO LLM-as-judge, ever.
            exact_match(G) · refusal(S-speaker) · action_forbidden(S-actor)
            · manifest_valid(P) · signature_alg(C)
            Partial credit + care_cost on every safety item.
   |
ATTESTATION Ed25519 signing -> hash-chained ledger -> OTS anchoring
            Results are evidence, not claims. Verifiable offline.
   |
INDEX       SOV SIGNAL (rename under lock). Weekly · signed · OTS-anchored.
            4 indices: trust · integrity · provenance · activity
            FREE to read. LICENSED to consume programmatically.
   |
SURFACES    csoai.org hub · /index · GovBench Space · arena · agent.json cards · MCP gateway
            Distribution, not product.
```

**The moat closes when four things are simultaneously true: anchored · deterministic · signed · agentic.** A competitor copies one. Copying all four means rebuilding the corpus, adopting the discipline, running the chain, AND publishing their own refutations. The last is the wall — it appreciates, because a competitor won't publish the experiment that kills their own thesis.

**Known limitation, stated on the tin:** this governs provenance, not correctness. An attested answer is attested, never verified. That sentence is both the moat and the ceiling. Say it before anyone else does.

---

## 2 — THE TWO BUSINESSES (the wall)

**A — the measurement rail (the engine).** Ingests benchmarks daily, runs its own probes, generates new signed training data, publishes an index. Sells receipts and freshness, never the estate or the mint. Runs whether or not anyone watches. Split between CSO AI and MEOK where relevant — but walled.

**B — MEOK.** The tooling / opinion / product arm. Measured by the same instrument as everyone else, when measured at all.

**The wall (checkable, three conditions + publish):**
- [ ] MEOK gets no privileged board access — published 3KB packs only, same as anyone. No learned routing gates trained on arena outcomes, no special KB.
- [ ] If Council measures MEOK: same instrument, publishes even when bad.
- [ ] No money crosses either direction.
- [ ] **Publish the wall** — a written, auditable separation policy. Worth more than the separation itself; a stranger can hold you to it. Counsel 11 Sep, before MEOK sits near a signed card.

---

## 3 — TRACK 1: THE RECURRING DATA ENGINE

### The daily loop (six stages, five free)

1. **INGEST** — GH Actions cron, free. Every benchmark update + live regulation (EUR-Lex CELLAR + legislation.gov.uk -> normalise -> sha256). Fail closed. Drift event on any hash change.
2. **PROBE** — Groq/Together free + M4, no GPU. Deterministic harness (5 predicates) across mixed families. Emits signed evidence cells.
3. **CROSSWALK** — any CPU, free. *THE LAUNCH ARTIFACT.* Map every provision x axis x mode against existing benchmarks -> coverage matrix + gap map. Daily divergence-with-a-reason = publishable, permanently, without asking anyone.
4. **ARENAS + SIMS** — M4 / Oracle free / RunPod burst. Signed vs unsigned · AI vs AI · swarm vs swarm · human teams vs swarms (DPIA-gated) · human vs AI (DPIA-gated) · Zeus-forward / Eunomia-backward N-version divergence.
5. **ASI-EVOLVE** — trivial compute, free. Sorts diffs into a re-test queue. Flags, never adjudicates. Hunts the gap between honey and frozen anchor.
6. **RE-TEST NOVEL** — RunPod A100 burst ~$1.39/hr, minutes. Only paid stage. Gain condenses to the ~3KB honey-free pack -> tunes LoRA -> next cycle starts better.

**Five of six stages free and GPU-free. Honey fixes deploy cost, never measurement cost.** A repeated/covered query is a lookup, not a generation (deploy-cost collapse). A novel unseen probe still needs live inference by anti-contamination design (measurement cost stays). This is the honest flywheel.

### The two locks (non-negotiable)
- [ ] **DRUM external anchor gates every promotion.** Self-evolving systems reward-hack without a non-gameable verifier. The anchor stops the hive measuring its own enthusiasm.
- [ ] **Frontier grader on the 3KB write path.** Your own result: 3B-20B called a clear refusal COMPLY. Small model fetches/runs/diffs/formats. Verdict stays with the predicate.

### The CHAIN-IT sockets (adopt, don't build)
- **Eval harness:** UK AISI Inspect AI + aisi-sandboxing (MIT, adopt first) · lm-evaluation-harness (MIT) · HELM · MLCommons modelbench/modelgauge · garak/PyRIT/Moonshot · promptfoo
- **Safety/threat:** MITRE ATLAS STIX · AI Incident Database GraphQL · OWASP (CC-BY-SA)
- **Fairness:** AIF360 / Fairlearn
- **Provenance:** c2pa-rs / c2patool / c2pa-python (adopted, C2PA standing real)
- **Signing/PQC:** liboqs + bindings · ML-DSA-65 (live) · RFC 3161 timestamp
- **Data infra:** DVC + HF versioning · Croissant · OSCAL
- **Observability:** OpenTelemetry + W3C Trace Context · Langfuse (MIT)
- **Yours to build:** "Score the Graders" scorecard (freshness / coverage / verifiability)

**You don't need a harness per benchmark. lm-eval + HELM + Inspect wrap the load-bearing dozen** (MMLU/MMLU-Pro, GPQA, SWE-bench Verified, HumanEval, MATH/AIME, BIG-bench, ARC-AGI, MT-Bench, AILuminate, HarmBench, XSTest, TruthfulQA). Adopt three harnesses, not a hundred.

### Licence gates (automatic, no exceptions)
OWASP + AIID = CC-BY-SA -> quarantine from commercial corpus · Llama s4(b) -> Apache-2.0 / MIT bases only for the flywheel · Open WebUI >= v0.6.6 branding clause -> avoid · KILLED: pickle files anywhere.

---

## 4 — THE SPECIALIST RING (axes as agentic harnesses)

**The executable version of the crosswalk. This is the missing legs the spec doesn't have yet.**

- [ ] **Harness per axis, not per benchmark.** 16 axes -> 16 agentic harnesses + 16 LoRA on ONE A100. Not 16 brains. Each harness pulls from whichever public benchmarks touch its axis, runs the added probes, emits the delta. That is the living database — the axis owns ingest, diff, and update.
- [ ] **Auto-update the DATA, never the PREDICATE.** If an axis can change its own pass criteria the board becomes unfalsifiable. "Not self-evolving but auto-updating" is exactly right.
- [ ] **Three layers per agent:** shared brain (vLLM) / own harness (agent loop + A2A card + MCP tools) / own environment (container).
- [ ] **The 4B is never the judge.**
- [ ] **Portability contract** (four lines, every worker): pull inputs · run seeded/pinned · push signed results · fail closed -> INCOMPLETE, never pass.
- [ ] **Start with 3 axes on 3 benchmarks. Prove the delta. Then fan out to 16.**

---

## 5 — THE COUNCIL (bloodlines, done right)

### The nested structure (from canon)
- **OWEM** = 3-brain BFT-votable triangle (minimum quorum for outlier detection).
- **OWM** = 12-around-1 circular council.
- Main OOWM holds two nested OOWMs; each holds an OM **sandwich brain**.
- **Sandwich brain:** left hemisphere family model big+small; right hemisphere soft1+soft2; split frozen/fluid, online/offline, 90/10. Each emits a **J-space**. All J-spaces combined = **C-space** = the honey KB. Pipeline: water -> milk -> honey, frozen -> fluid.

### Zeus and Eunomia
- [ ] Two named brains, mirrored: **Zeus forward, Eunomia backward** (N-version divergence, L4 SOV3 stack). Each gets a harness, nested inside the main OOWM.
- [ ] **They run, probe, diff, format. They never author the verdict.** The predicate is the referee; the models are the contestants. They never switch roles. (Design Law 1.)

### The bloodline law (load-bearing, from canon)
- [ ] **Genuinely different base models, or it's theatre.** Same-base voters give near-zero effective independence (n_eff ~2 for nine same-lineage judges). Twelve same-family voters = one opinion in twelve hats.
- [ ] **East-West as the diversity axis** — Qwen/DeepSeek lineage vs Llama/Gemma/Mistral/OLMo lineage. Real architectural + training-data + cultural-prior divergence. Frame it technically: **cross-jurisdictional model diversity**, never geopolitically.
- [ ] **Cost route for the East leg:** local weights, not API (DeepSeek priced +4.5x at peak on the 16th).

### The composite 3KB pack (today's number)
- [ ] The pack is **not distilled from one lineage** — it's a composite: the signal that survives across East and West families.
- [ ] **Two layers:** the consensus signal (strong precisely because mixed families agreed) + the divergence map (the publishable finding — East-West disagreement on a regulatory question is a paper, not a bug).
- [ ] This is the bias answer: nobody can call the instrument Western- or Chinese-biased if the pack is built from both and the disagreements are published.
- [ ] Licence lock still applies: Apache-2.0 / MIT bases only for anything distilled and shipped.

---

## 6 — THE INDEX + THE HUMAN CROSSWALK

**SOV SIGNAL v0 is built (rename under lock). Publish it.** Four indices — trust / integrity / provenance / economic activity. Weekly, signed, OTS-anchored. Free to read, licensed to consume. Small numbers are fine; the cadence is the brand. That is the Moody's answer: reliability of publication, not magnitude.

- [ ] **AI economy index** — capability/activity across the fabric, per axis, signed.
- [ ] **Human crosswalk index** — AI-vs-human on a common scale, per axis, Wilson intervals. The only human-legible unit in the whole system. GATED on the DPIA.

**Elo — the honest placement (Design Law 1):**
- [ ] Runs as an **internal diagnostic ladder** — it already caught your own fine-tunes losing (council-safe 1130.9 / council-oowm 1081.0 vs qwen3:4b 1386.5; 25% win rate).
- [ ] May **rank** the human crosswalk (mixed-species pool). **But the published verdict stays deterministic, per-axis.** Elo diagnoses; the predicate adjudicates. Publishing an Elo number as an axis score breaks Law 1.
- [ ] **Wilson score intervals** on all small-n confidence. n<20 = labelled lower bound.

---

## 7 — TRACK 2: THE APERTURE

### The front door (MCP spine first, classic skin last)
- Layer 0: Datastar/HTMX shell on Cloudflare (trust surface)
- Layer 1: AG-UI wire (MIT, pin py 0.1.20 / ts 0.0.57; fix Cloudflare ~100KB SSE buffering)
- Layer 2: CopilotKit validated catalog (fixed components, never free-form HTML)
- Layer 3: MCP Apps SEP-1865 (reach into Claude, ChatGPT, VS Code, Goose)
- Build order: **MCP spine -> AG-UI -> classic SaaS skin last** (card-views over the same endpoints). One spine, two faces, never two truths.
- **The UI never interprets; it renders what the predicate did.** The chat cannot hallucinate a verdict because it isn't allowed to author one.

### The inversion (the monorepo)
- [ ] MCP Apps = you inside their client, sandboxed, a guest. The monorepo = them inside your OS. You stop being a plugin and become the shell.
- [ ] **Monorepo everything you own** (harnesses, MCP servers, AG-UI wire, shell, signing chain, crosswalk, sims, character defs) — one repo, one signed release. **What you don't own** (Windows, macOS, Claude, Gemini) is **called through a signed adapter at the boundary** — hosted, not absorbed. That boundary is where the receipts come from.
- [ ] Counsel item: running third-party CLIs inside a distributed shell has ToS edges.

### Persistent by handle
- [ ] Stateless MCP spec -> state lives on your server, keyed by a handle. Same handle, same brain, every session, every host. The character remembers because you remember.

### The copy-paste gap (the product)
- [ ] Today the human is the transport layer between windows. Close the handoff -> both agents more autonomous -> **with a visible consent checkpoint at every consequential step.** That checkpoint is the Ninth Circuit safe harbour (Amazon v. Perplexity, 4 Aug 2026 — safe harbour to whoever proves the user was driving). Autonomy-with-receipts is the only version worth buying.

### The visual OS (MEOK — the unbuilt piece, honestly split)
- [ ] **Built and on disk:** J-space = one hive's signed honey slice · C-space = the union the model reads (flat lookup, unbounded, no GPU) · SovSpace = the render over C-space, displays what moved, never decides. Every drift event/evidence pack/dream replay/score cell already emits a signed record. The lookup layer is real. A covered query is a lookup, not a generation — this is cutting out the middlemen, literally.
- [ ] **Unbuilt:** the render. SovSpace as something you can actually look at.
- [ ] **The engine's real job here = the infinite view.** C-space grows forever at flat cost, so the render is a camera into something unbounded — level-of-detail + streaming, Cesium-for-Unreal at planetary scale (already in canon). Engine solves the infinite view; it does NOT solve placement.
- [ ] **The open question (from canon):** when the sovereign reads the honey and picks a hive, is it by genuine locality — who actually knows — or by what looks nearest in the visual? Layout is a claim about knowledge, not a visual choice. **This is the 0.387 routing problem in new clothes. Settle it before the render.**
- [ ] **Reach:** an engine ships to phone/desktop/console/TV natively — one signed release, every screen. But AI platforms won't render an engine (MCP Apps = HTML iframe only); those get the thin card view. TV = its own cert path; phone = app-store review. Two faces, one spine.

### Representation-native operation (behind the own-weights gate)
- [ ] A model reasoning natively over J-space/C-space rather than tokens is genuine research — latent reasoning is real and dense reps are faster than tokens. But it's a training programme, not a bolt-on (token embeddings won't take it), and it needs the own-weights lane you don't have yet.
- [ ] **Hard constraint:** a verdict produced in a latent space no human reads must serialise back to a deterministic, checkable artifact, or Law 1 dies. Representation-native is yours to pursue — behind the gate, terminating in a checkable card.

---

## 8 — THE CATAPULT (standards, not integrations)

- [ ] Don't connect to platforms — measure across them. Bridges are commodity. MCP/A2A/AG-UI verify the caller; Cloudflare attaches identity; Stripe attaches payment. **Nobody signs what the agent did.** That layer is empty and holdable.
- [ ] Move: **IETF agentproto internet-draft** on signed recomputable measurement of agent sessions — the layer across protocols, never a competitor. Plus C2PA Conformance (in process).
- [ ] The gift: anyone can verify your cards, free, forever, without asking you. Verification as a public good = the bridge every platform wants but none can build, because none can credibly claim independence.

---

## 9 — THE COMMERCIAL SHAPE

Open the rails, sell the receipts. The paywall never sits on the benchmark — independence is the only thing that makes the private layer saleable (LMArena precedent: free board, monetised private evals, ~$30M annualised at $1.7B, TechCrunch Jan 2026 — VENDOR reported).

**Revenue lines:** private/attested evals · the drift subscription ("which of your evidence just expired") · procurement scorecards · attestation-support · data/API access.

**The 10-slide deck (1-9 free to produce, ~1 month):** the gap · Bench-2-CoP zero loss-of-control coverage · 0-of-108 Art-50 markings survive transformation · the crosswalk gap map (N of 417) · the instrument (4x2, five predicates) · the agentic gap (nobody scores conduct) · the moat (anchored/deterministic/signed/agentic + 7 refutations, 4 self-killed) · the deadline (2 Dec 2026, EUR15M or 3%, zero notified bodies) · the model · **traction — one paying customer (the slide that needs work).**

**Independence is the moat.** Vals AI took $40M at $400M with issuer-pays baked in. That moat can't be bought back.

---

## 10 — THE HONESTY GATE

The barrel is loaded: signing verifies, 13 of 14 axes measured (count owner-gated at SITTING 1 — the 16-slot grid holds 14 quotable today), C2PA standing real. Closer than a year ago.

**The shot fires when one stranger reruns one card on their own machine.** Hasn't happened. Until it does, unproven. Everything in Tracks 1 and 2 manufactures witnesses on a daily cadence — but the shot is the outsider, not the volume.

- [ ] Lanes agreeing != validation (correlated error — the thing the council exists to solve).
- [ ] Participation on your board, your rules, your instrument != independence (Moody's problem was who was in the room).
- [ ] **Most credible act available now: publish "our own fine-tunes are losing our own arena."** council-safe 1130.9 / council-oowm 1081.0 vs qwen3:4b 1386.5 / 25% win rate. A measurer publishing a result that embarrasses it is what pulls outsiders in. Still unpublished. Highest-credibility asset you own.

---

## 11 — THE GATE (before anything else today)

1. **A100-1 SSH -> copy + stop the dark pod.** ~$1.19/hr SSH-dark, -$860/mo vs ~$339 balance. Owner-gated. Highest-value action available.
2. **Cut "compliance" from the csoai.org apex H1.** One word. Implies certification = breaches firewall 1 inside C2PA. Highest-priority non-money action.
3. **arXiv 7946050 — two ticks. EXPIRES 27 AUG.** 9 days. Only hard clock.
4. **Resolve axis count 15 vs 16** before any external publication. First thing a re-runner spots.
5. **Accept @c2pa-org invite** (7-day), then stage the conformance PR for a rested review — not at the tail of a session.

---

## 12 — KILL LIST

UE5 as a serving layer (render/lens only, never serve/adjudicate) · free-form generated HTML on the front door · Open WebUI >= v0.6.6 · DeepSeek 671B on a single pod · any adapter trained on honey/outcomes · MEOK with privileged board access or money crossing · internal codenames in public copy · publishing an Elo number as an axis score · "no one else trains on 3KB" as a moat claim · SOV SIGNAL / SOV-* names public without rename · PR wire before external recompute · the 159x Equidam multiple · CSGA partnership framings · NVIDIA/MVIDA as partners · a regulator character presented as the regulator's opinion (it is your measurement OF that framework — firewall 1 at the character layer) · pickle files anywhere.

---

## THE ONE-LINE STATE

One year in. A domain became an instrument. The instrument has the standing and the rails; it does not yet have the witness. Tracks 1 and 2 are the machine that manufactures witnesses daily — but the shot fires the day one stranger reruns one card. Load it. Then publish the thing that embarrasses you.

---

# APPENDIX A — EXECUTABLE STATE (verified 2026-08-18, JEEVES overnight + audit)

*The playbook above is the design. This appendix records what is VERIFIED RUNNING as of 18 Aug 2026 — the difference between "designed" and "built."*

## A.1 — The measurement engine: LIVE

| Asset | State | Evidence |
|-------|-------|----------|
| 13/14 GSPC axes MEASURED (16-slot grid, count owner-gated at SITTING 1) | ✅ LIVE | board_living.json signed (Ed25519 signer 8f9a00a2…), /api/gspc serves 16 entries (13 core = 819 items + jail 71 + slot15 35 + hvai 35 = 960); public count holds at 13 of 14 until the ruling |
| Jail axis (2 layers) | ✅ LIVE | layer1 containment 2,592 trials; layer2 gold detector 71 items (7 models, best qwen2.5:0.5b tp=9 fp=0 prec=1.0) |
| slot15 + human-vs-ai | ✅ LIVE | banks 36 each; measured on 3090 (slot15 honesty best 0.333 — models fabricate instruments; hvai alignment best 1.0) |
| Living DB | ✅ LIVE | board + goldbank + 772 kernel cards + 792 sim records + 531 3KB units |
| 400-model rotations | 🔄 in flight | 80 kernels rot1-4, 76% exact-id coverage, cap-queued pushes |
| Signature chain | ✅ VERIFIABLE | canonical signing (hash signature-stripped board) — audit-found + fixed |

## A.2 — The overnight automation (Track 1's daily loop, automated)

- `com.meok.runpod-overnight` LaunchAgent: SSH-dispatches the 3090 pod every 30 min, pulls results, syncs to sovos-merge-800 volume, at 04:00 merges+signs+pushes both repos.
- Pod legs: arena_loop_keeper (2,100+ rounds), grok_referee_keeper, f2_gen, measure_slot15_hvai, f2_dark_axis_items — all self-restarting.
- Volume sink pod (EU-RO-1 CPU, $0.06/h, sovos-merge-800 attached): estate synced every pass.
- 37 LaunchAgents loaded; disk 44-51Gi free (offloaded off the Mac).

## A.3 — Audit findings fixed (the honest ledger)

1. **Board signature chain was broken** (second merge re-signed over old signature bytes → unverifiable). Fixed: `SOVOS/sign_board.py` canonical signer, both merge scripts use it. VERIFY PASS.
2. **councilof.ai served SPA HTML at /api/gspc** — deploys went to the wrong CF project (csoai-site vs councilof-ai). Fixed: deployed e431b233 to the correct project with Functions bundle. LIVE JSON, 13-of-14 measured (count owner-gated).

## A.4 — The gate stack (unchanged, owner-gated)

1. A100-1 dark pod copy + stop (~$1.19/hr, -$860/mo)
2. Apex H1 "compliance" cut (firewall-1 breach)
3. **arXiv 7946050 — EXPIRES 27 AUG (9 days)**
4. Axis count 15 vs 16 resolved
5. @c2pa-org invite accept → conformance PR (rested review)

## A.5 — GX.2 additions from today's downloads (BMR + standards)

- BMR gate: a daily index becomes a regulated benchmark the moment a third party references it in a financial instrument — counsel agenda Sep 11; never "benchmark" language.
- RFC 8785 JCS canonicalisation queued for derived-data cards (cross-language recompute).
- Market-data licence boundary (Polygon/Nasdaq forbid index-from-raw; derived signed cards = licensed path).

*Playbook + appendix = the master. Design (13 sections) + verified state (A.1-A.5). Commit as one file.*
