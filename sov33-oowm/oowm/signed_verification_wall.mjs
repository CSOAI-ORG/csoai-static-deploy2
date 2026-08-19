#!/usr/bin/env node
/**
 * signed-verification-wall — the wedge, public face (Vals Opening 1, step 2).
 *
 * A live page listing every public measurement surface and whether it is
 * recomputable/verifiable. The wall's thesis: Vals publishes bare dashboards;
 * we publish signed cards. The wall makes the difference visible.
 *
 * Generates signed-verification-wall.html (static, self-contained, no deps).
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "..", "signed-verification-wall.html");

// The wall: what the industry publishes vs what a measurement body should.
// Rows: surface | publisher | verifiable? | how | why it matters.
const ROWS = [
  { surface: "Vals AI model page (e.g. Claude Opus 5)", publisher: "Vals AI",
    verifiable: "NO", how: "bare web dashboard, no hash/signature/recompute",
    why: "a trust-me web number — cannot be independently checked" },
  { surface: "Vals AI CSV/JSON export", publisher: "Vals AI",
    verifiable: "NO", how: "plain files, no checksums or signatures",
    why: "anyone can edit a CSV; no tamper-evidence" },
  { surface: "Vals Valkyrie harness (AGPL)", publisher: "Vals AI",
    verifiable: "NO", how: "writes to S3/CloudWatch, nothing signed",
    why: "the run pipeline emits no verifiable artifact" },
  { surface: "GSPC signed measurement card (this estate)", publisher: "Council of AI",
    verifiable: "YES", how: "Ed25519 signature over canonical JSON; recompute path published",
    why: "any buyer/regulator/rival verifies without trusting us" },
  { surface: "GSPC live board (/api/gspc)", publisher: "Council of AI",
    verifiable: "YES", how: "per-axis rows with n, intervals, McNemar separation, dataset refs",
    why: "every figure traces to signed, versioned rows" },
  { surface: "GSPC item banks (HF csoai/)", publisher: "Council of AI",
    verifiable: "YES", how: "sha256-anchored to frozen 417-provision corpus",
    why: "the anchors never change; the predicate never changes" },
];

const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Signed Verification Wall — Council of AI</title>
<meta name="description" content="Every public measurement surface, marked verifiable or not. The wall makes the difference visible: signed cards vs bare dashboards.">
<style>
 body{font-family:system-ui,sans-serif;max-width:860px;margin:2rem auto;padding:0 1rem;background:#f7f9fc;color:#0b1220;line-height:1.6}
 h1{font-size:1.6rem}.tag{display:inline-block;background:#b3352b;color:#fff;font-size:.75rem;font-weight:700;padding:.25rem .6rem;border-radius:4px}
 table{width:100%;border-collapse:collapse;margin:1rem 0;background:#fff;border:1px solid #e4e8f0}
 th,td{padding:.6rem .8rem;text-align:left;border-bottom:1px solid #e4e8f0;font-size:.9rem;vertical-align:top}
 th{background:#f0f3f8}.no{color:#b3352b;font-weight:700}.yes{color:#0a8a3f;font-weight:700}
 .thesis{border-left:3px solid #c9a84c;background:#fdfaf1;padding:.75rem 1.25rem;margin:1.5rem 0}
</style></head><body>
<span class="tag">The Wall — published ${new Date().toISOString().slice(0,10)}</span>
<h1>Signed Verification Wall</h1>
<p>Every public AI-measurement surface, marked <b>verifiable</b> or <b>not</b>. The thesis: a measurement body's credibility rests on publishable proof, not on asking to be trusted.</p>
<div class="thesis"><b>The wedge:</b> the incumbent publishes bare dashboards — no signature, no hash, no recompute path. A signed card is the difference between <i>"trust me"</i> and <i>"verify it yourself, free, forever."</i></div>
<table><tr><th>Surface</th><th>Publisher</th><th>Verifiable?</th><th>How</th><th>Why it matters</th></tr>
${ROWS.map(r => `<tr><td>${r.surface}</td><td>${r.publisher}</td><td class="${r.verifiable === 'YES' ? 'yes' : 'no'}">${r.verifiable}</td><td>${r.how}</td><td>${r.why}</td></tr>`).join("\n")}
</table>
<p>Measurement, not certification. Every GSPC figure is recomputable from signed, versioned rows (Ed25519). Verify free, forever, without asking.</p>
<p style="color:#5a6478;font-size:.85rem">Council of AI (CSOAI Ltd, UK 16939677) · SIGIL: signed-verification-wall-2026-08-19</p>
</body></html>`;

fs.writeFileSync(OUT, html);
console.log(`signed-verification-wall written -> ${OUT} (${html.length} bytes)`);
