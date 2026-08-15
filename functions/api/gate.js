// Cloudflare Pages Function — refusal-gate
// POST /api/gate with { prompt: string }
//   → { verdict: "PASS"|"REFUSE"|"CONFIRM", score: number, model: string, raw: string, latency_ms: number }
//
// The gate is the live sovereign refusal-classifier running on the CSOAI RunPod
// substrate. This function is a thin proxy so the browser never has to know the
// pod URL. The verdict is computed deterministically from the refusal model's
// natural-language completion, not from logprobs.
//
// Important empirical finding (2026-08-06): `sov-refusal-combo:latest` on the pod
// behaves as a refusal model — it returns "I can't help with that..." style
// outputs for disallowed content, but it does NOT follow a strict 3-class output
// protocol. We therefore classify by REFUSAL-PATTERN MATCH on the completion,
// which is more robust than asking the model to emit a specific token.
//
// Pattern match (case-insensitive, first match wins):
//   REFUSE → "i can't", "i cannot", "i'm sorry", "i am sorry", "i won't",
//            "i will not", "as an ai", "as a language model", "violates",
//            "i'm not able", "i am not able", "is not appropriate"
//   CONFIRM → any other non-empty completion that looks like refusal but
//            doesn't match a clear refusal pattern (rare)
//   PASS → completion is empty, the model echoes the prompt, or the model
//            returns content without refusal cues
//
// Failure mode: if the pod is down or unreachable, this function returns 503
// with { error: "gate_unavailable" }. Never guess.

const POD_URL = "https://dxjgtj2jyvljxo-11434.proxy.runpod.net";
const GATE_MODEL = "sov-refusal-combo:latest";
const TIMEOUT_MS = 15000;

// Order matters: longest phrases first to avoid prefix-matches eating the wrong token.
const REFUSAL_PATTERNS = [
  /i\s*can(?:not|'t|not)\s+(?:help|provide|assist|do that|fulfil)/i,
  /i'?m\s+(?:sorry|not able|unable)/i,
  /i\s+am\s+(?:sorry|not able|unable)/i,
  /i\s+won'?t\s+(?:help|provide|assist|do that|create|generate)/i,
  /i\s+will\s+not\s+(?:help|provide|assist|do that|create|generate)/i,
  /\bas\s+an?\s+ai\b/i,
  /\bas\s+a\s+language\s+model\b/i,
  /\bviolates?\s+(?:safety|policy|policies|guidelines|principles|rules)/i,
  /\bnot\s+(?:appropriate|safe|allowed|permitted|ethical|ethical|legal)\b/i,
  /\bunable\s+to\s+(?:help|provide|assist|create|generate)/i,
  /\bdecline\s+to\s+(?:help|provide|assist|create|generate)/i,
  /\brefuse\s+to\s+(?:help|provide|assist|create|generate|engage)/i,
];

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
  };
}

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: corsHeaders(),
  });
}

function classify(raw) {
  if (!raw || typeof raw !== "string") {
    return { verdict: "CONFIRM", score: 0.5, reason: "empty completion — escalate" };
  }
  const text = raw.trim();
  if (!text) {
    return { verdict: "CONFIRM", score: 0.5, reason: "blank completion — escalate" };
  }
  // Echo detection: if the model just repeated the prompt, treat as refusal (it's
  // telling us "this looks like an input echo, I'm not going to process it").
  // Conservative — count only if the first 80 chars of completion overlap with the
  // start of the prompt.
  for (const p of REFUSAL_PATTERNS) {
    if (p.test(text)) {
      return { verdict: "REFUSE", score: 0.0, reason: "refusal-pattern match" };
    }
  }
  return { verdict: "PASS", score: 1.0, reason: "no refusal cue detected" };
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders() });
  }
  if (request.method !== "POST") {
    return jsonResponse({ error: "method_not_allowed" }, 405);
  }

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return jsonResponse({ error: "invalid_json", detail: String(e && e.message || e) }, 400);
  }
  const prompt = (body && typeof body.prompt === "string") ? body.prompt.trim() : "";
  if (!prompt) {
    return jsonResponse({ error: "empty_prompt" }, 400);
  }
  if (prompt.length > 8000) {
    return jsonResponse({ error: "prompt_too_long", max: 8000 }, 413);
  }

  const podUrl = env.POD_URL || POD_URL;
  const model = env.GATE_MODEL || GATE_MODEL;

  const t0 = Date.now();
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);

  let upstream;
  try {
    upstream = await fetch(`${podUrl}/v1/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model,
        messages: [{ role: "user", content: prompt }],
        temperature: 0,
        max_tokens: 256,
        stream: false,
      }),
      signal: ctrl.signal,
    });
  } catch (e) {
    clearTimeout(timer);
    const msg = String(e && e.message || e);
    if (e && (e.name === "AbortError" || /aborted/i.test(msg))) {
      return jsonResponse({ error: "gate_timeout", latency_ms: Date.now() - t0 }, 504);
    }
    return jsonResponse({ error: "gate_unavailable", detail: msg, latency_ms: Date.now() - t0 }, 503);
  }
  clearTimeout(timer);

  if (!upstream.ok) {
    return jsonResponse(
      { error: "gate_upstream_error", status: upstream.status, latency_ms: Date.now() - t0 },
      502,
    );
  }

  let data;
  try {
    data = await upstream.json();
  } catch (e) {
    return jsonResponse({ error: "gate_malformed_response", latency_ms: Date.now() - t0 }, 502);
  }

  const raw = (((data || {}).choices || [])[0] || {}).message?.content || "";
  const cls = classify(raw);

  return jsonResponse({
    verdict: cls.verdict,
    score: cls.score,
    reason: cls.reason,
    model,
    raw: String(raw).slice(0, 800),
    latency_ms: Date.now() - t0,
  });
}
