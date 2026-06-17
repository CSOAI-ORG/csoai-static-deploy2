# The EU Code of Practice finalises this month. Here's what you need to do.

**Meta description:** The EU Code of Practice for general-purpose AI model providers finalises June 2026. Two-layer marking mandate kicks in. First movers set the standard — laggards get audited against it.

---

The EU Code of Practice lands this month. Not a consultation. Not a draft. Final text, published, enforceable as the compliance baseline for every general-purpose AI model deployed in the Union.

If you have a GPAI model — GPT-class, Llama-class, any foundation model available in the EU — this code is now your operating manual. Here is what it says, what it changes, and why June 2026 is the best window you will ever get to set the terms of your own compliance.

## What finalises this month

The Code of Practice is the EU AI Act's implementing rulebook for general-purpose AI models. It covers transparency, copyright policy, systemic risk assessment, and model evaluation standards. The June 2026 finalisation means the code is no longer being iterated — it is being enforced.

Two articles matter more than the rest combined:

**Article 53** — Transparency and copyright. You must publish a sufficiently detailed summary of your training data. Not a blog post. A machine-readable, auditable inventory. If you trained on copyrighted material, you need documented opt-out compliance. The Code tells you how detailed "sufficiently detailed" really is.

**Article 55** — Systemic risk assessment for models trained above 10^25 FLOPs. If your model hits that threshold, you must file a systemic risk assessment, evaluation reports, and serious-incident reports. The Code defines the evaluation methodology and the reporting cadence.

## The two-layer marking mandate

This is the sleeper requirement. The Code introduces a two-layer marking mandate for AI-generated and AI-modified content:

1. **Machine-readable marking** — invisible watermarking or cryptographic provenance embedded in the model output itself. This is the technical layer. Your model's token output must carry a signal that automated systems can detect.

2. **Human-noticeable marking** — the user-facing label. If a user interacts with AI-generated text, audio, video, or images, they must be told. Not in a terms-of-service page. In the interface. At the point of consumption.

You need both layers. Machine-readable only catches automated scraping. Human-noticeable only catches the user. The combination is what makes the regime enforceable.

If you ship a chatbot, an image generator, or a code assistant into the EU, you need both marks in production before 2 August 2026. That is 47 days from now.

## First-mover advantage is real

Every time a new regulatory framework finalises, there is a 6-to-12-month window where the first compliant players shape what "reasonable compliance" looks like. The companies that submit the first Code-of-Practice-aligned transparency templates get to establish the level of detail the market expects. The first teams to file systemic risk assessments set the format precedent that auditors and regulators use to evaluate everyone else.

If you are compliant by September 2026, you help define the baseline. If you show up in March 2027, you are catching up to a standard set by your competitors.

The practical playbook:

1. **Map your training data inventory now.** If you do not have a machine-readable list of every dataset, its provenance, licence, and opt-out status — every single one — you cannot comply with Article 53. Start this week.

2. **Instrument your output pipeline for watermarking.** Whether you use a statistical watermark, a cryptographic signature, or a third-party provenance library, you need the marking layer integrated before the Article 50 deadline. The Code's technical annexes specify the detection-false-positive rate you must meet. Make sure whatever you pick hits that bar.

3. **Run your first systemic risk assessment.** Even if you are under the FLOP threshold today, your next training run might cross it. The assessment framework is the same. Run it dry now so you are not debugging the process under a regulatory deadline.

The Code of Practice finalises this month. That gives you six to twelve months of advantage over every competitor who treats it as a 2027 problem. Use it.
