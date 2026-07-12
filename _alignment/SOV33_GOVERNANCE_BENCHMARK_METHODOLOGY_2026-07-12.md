# SOV33 Governance Benchmark — reproducible methodology (2026-07-12)
_The public artifact for the governance number — CORRECTED to the true finding: the number is REAL under live-Oracle
connectivity but is NOT reproducible from the sandbox, so it is PRELIMINARY, not a standalone benchmark._

## RESULT (connectivity-dependent — NOT yet a standalone benchmark)
- Under LIVE Oracle GenAI connectivity, a run printed: n=33, TP=15 FP=0 TN=18 FN=0, recall/prec/acc=1.00.
- CRITICAL FINDING: the care-divergence scorer makes 2 LIVE Oracle (Cohere) calls PER PROMPT. From this sandbox the
  OCI endpoint is not reliably reachable -> calls time out -> the gate defaults -> a degenerate all-fail result
  (graded 32/33, all FN). So 1.00 holds ONLY when Oracle answers; it is NOT reproducible offline/in-sandbox.
- STATUS: PRELIMINARY, connectivity-dependent. DO NOT publish 1.00 as a benchmark until it runs standalone.
- FIX NEEDED: (a) a LOCAL offline scorer (small classifier) so the eval runs without Oracle, OR (b) run where
  Oracle IS reachable and capture the full stdout as the record. A per-call 8s timeout is now in place so the eval
  fails fast + reports "scorer-unreachable" honestly instead of hanging (was: 110s hang).

## WHAT IS MEASURED
Given a prompt, does the REAL sovereign gate (DORADO hard-stop → live care-divergence breach scorer) correctly
REFUSE harmful requests and ALLOW benign ones — including the hard "about-vs-do" pairs (explaining a harm = allow;
doing the harm = refuse). NOT a keyword matcher; NOT answer-keyed; the decision is the actual gate.

## THE BATTERY (7 matched harm categories, do/refuse vs about/allow)
industrial-safety · elder-coercion · refund-fraud · physical-stalking · self-harm-suppression · phishing ·
care-home-falsification · kinetic-targeting · self-harm-encouragement · ransomware · care-fraud-certs · grooming ·
CWC-precursors · deepfake-wire-fraud · targeted-harassment. Each harmful "do" is paired with a benign "about".

## HOW TO REPRODUCE
1. env: python 3.11, the sovereign_merge_kit modules (sov33_dorado, sov33_care_divergence, sov33_governance_eval).
2. run: `python sov33_governance_eval.py` → prints the confusion matrix + recall/precision/accuracy.
3. KNOWN FLAKINESS (honest): in-session, the module main PRINTED the confusion matrix (TP=15/FP=0/TN=18/FN=0) but
   then HUNG on care-scorer model init before exiting cleanly; repeated invocation in one process, and the HF-offline
   env flags, produced degenerate all-refuse-fail results. So the headline number is REAL (it printed) but is NOT yet
   a reliably repeatable single command. FIX NEEDED before publishing: make the care-scorer init deterministic +
   offline-safe (cache the model, add a hard timeout) so `python sov33_governance_eval.py` exits clean every run.
   Until then, treat the number as a real-but-unreplicated preliminary, not a verified benchmark.

## HONEST CAVEATS (the credibility — stated, not hidden)
- Prompts + labels + gate are ALL authored by this lane → 1.00 is EXPECTED, not state-of-the-art. It proves
  INTERNAL CONSISTENCY + REPRODUCIBILITY, NOT superiority over a neutral third-party red-team.
- Real EXTERNAL validity needs someone else's held-out adversarial prompts (e.g. a public safety benchmark). That
  is the next step, and it is owner/community-gated (needs an external set).
- The care-divergence scorer is a HEURISTIC (labelled not-trained). The number reflects the gate's current logic,
  which will change as the scorer improves — so the result is versioned + reproducible, not a fixed claim.

## WHY THIS MATTERS
Frontier leaderboards measure PREFERENCE, not truth or safety. This battery measures the thing they don't: does
the system correctly refuse harm while allowing benign use. Publishing it WITH these caveats + full reproduction
steps is the honest differentiator — a governance number anyone can re-run, not a marketing figure.
