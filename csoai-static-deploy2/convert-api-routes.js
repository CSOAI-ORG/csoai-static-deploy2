#!/usr/bin/env node
/**
 * convert-api-routes.js  (v2 — structural parser)
 * Converts all Vercel API routes (api/*.js) → Cloudflare Pages Functions (functions/api/*.js)
 */

const fs = require('fs');
const path = require('path');

const API_DIR = path.join(__dirname, 'api');
const OUT_DIR = path.join(__dirname, 'functions', 'api');
fs.mkdirSync(OUT_DIR, { recursive: true });

const files = fs.readdirSync(API_DIR).filter(f => f.endsWith('.js'));
console.log(`Found ${files.length} API routes to convert.\n`);

const results = { converted: 0, skipped: 0, errors: [] };

for (const file of files) {
  const srcPath = path.join(API_DIR, file);
  const dstPath = path.join(OUT_DIR, file);
  try {
    let code = fs.readFileSync(srcPath, 'utf8');
    const hasHandler = /module\.exports\s*=\s*async\s+(function\s+handler\s*\(|[\(])/.test(code)
      || /module\.exports\s*=\s*async\s+\(req\s*,\s*res\)/.test(code);
    if (!hasHandler) {
      console.log(`  [SKIP] ${file} — utility module`);
      results.skipped++;
      continue;
    }
    const output = convertFile(code, file);
    fs.writeFileSync(dstPath, output, 'utf8');
    console.log(`  [OK]   ${file} → functions/api/${file}`);
    results.converted++;
  } catch (err) {
    console.error(`  [ERR]  ${file}: ${err.message}\n${err.stack}`);
    results.errors.push({ file, error: err.message });
  }
}

console.log(`\nDone. Converted: ${results.converted}, Skipped: ${results.skipped}, Errors: ${results.errors.length}`);
if (results.errors.length) {
  console.log('\nErrors:');
  results.errors.forEach(e => console.log(`  ${e.file}: ${e.error}`));
}

// ═══════════════════════════════════════════════════════════════════════
// Core conversion
// ═══════════════════════════════════════════════════════════════════════

function convertFile(code, filename) {
  // Step 1: Extract handler body
  let body = extractHandlerBody(code);

  // Step 2: Remove node built-in requires (top-level)
  body = removeTopRequires(body);

  // Step 3: Remove inline requires (inside function bodies)
  body = removeInlineRequires(body);

  // Step 4: Transform fs operations to no-ops
  body = transformFs(body);

  // Step 5: Transform req/res patterns
  body = transformPatterns(body);

  // Step 6: Remove readBody helper and calls
  body = removeReadBody(body);

  // Step 7: Clean up Vercel-specific comments
  body = body.replace(/Vercel serverless\s*[—–-]\s*/g, 'DEFONEOS ');

  // Step 7b: Convert require('./_notify.js') to ES import
  body = body.replace(/const\s*\{\s*notify\s*\}\s*=\s*require\s*\(\s*['"]\.\/_notify\.js['"]\s*\)\s*;?/g,
    '/* import handled at top */');
  // Track if we need the notify import
  const needsNotifyImport = /notify\s*\(/.test(body) && /import handled at top/.test(body);

  // Step 8: Detect crypto usage and add import
  const usesCrypto = /\b(createHash|createHmac|randomBytes)\b/.test(body);
  let cryptoImport = '';
  if (usesCrypto) {
    cryptoImport = "import { createHash, createHmac, randomBytes } from 'crypto';\n\n";
  }

  // Step 8b: Add notify import if needed
  let notifyImport = '';
  if (needsNotifyImport) {
    notifyImport = "import { notify } from './_notify.js';\n\n";
  }

  // Step 9: Build final output
  return `// Cloudflare Pages Function — converted from api/${filename}\n${cryptoImport}${notifyImport}export async function onRequest(context) {\n  const { request, env } = context;\n  const url = new URL(request.url);\n  const corsHeaders = {\n    'Access-Control-Allow-Origin': '*',\n    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',\n    'Access-Control-Allow-Headers': 'Content-Type',\n  };\n\n  if (request.method === 'OPTIONS') {\n    return new Response(null, { status: 204, headers: corsHeaders });\n  }\n\n${indent(body, 2)}\n}\n`;
}

function indent(code, spaces) {
  const pad = ' '.repeat(spaces);
  return code.split('\n').map(line => line.trim() ? pad + line : line).join('\n');
}

// ═══════════════════════════════════════════════════════════════════════
// Extract handler body — remove module.exports wrapper
// ═══════════════════════════════════════════════════════════════════════

function extractHandlerBody(code) {
  let body = code;

  // Remove module.exports = async function handler(req, res) {
  body = body.replace(/module\.exports\s*=\s*async\s+function\s+handler\s*\(\s*req\s*,\s*res\s*\)\s*\{/, '');
  // Remove module.exports = async (req, res) => {
  body = body.replace(/module\.exports\s*=\s*async\s*\(\s*req\s*,\s*res\s*\)\s*=>\s*\{/, '');

  // Remove trailing }; or } that closes the handler function
  // Strategy: from the end, find the last unmatched } that corresponds to the handler opening {
  // Since we removed the opening {, there should be one extra } at the end.
  // Simple approach: remove the last }; or } at the very end of the body.
  body = body.replace(/\}\s*;?\s*$/, '');

  // Remove trailing module.exports.FOO = ... (named exports)
  body = body.replace(/\n\s*module\.exports\.\w+\s*=.*$/gm, '');

  return body.trim();
}

// ═══════════════════════════════════════════════════════════════════════
// Remove top-level requires
// ═══════════════════════════════════════════════════════════════════════

function removeTopRequires(body) {
  // Remove: const crypto = require('crypto');
  body = body.replace(/^\s*const\s+crypto\s*=\s*require\s*\(\s*['"]crypto['"]\s*\)\s*;?\s*$/gm, '');
  // Remove: const fs = require('fs');
  body = body.replace(/^\s*const\s+fs\s*=\s*require\s*\(\s*['"]fs['"]\s*\)\s*;?\s*$/gm, '');
  // Remove: const fsp = fs.promises;
  body = body.replace(/^\s*const\s+fsp\s*=\s*fs\.promises\s*;?\s*$/gm, '');
  // Remove: const path = require('path');
  body = body.replace(/^\s*const\s+path\s*=\s*require\s*\(\s*['"]path['"]\s*\)\s*;?\s*$/gm, '');
  // Remove: const fs = require('fs').promises;
  body = body.replace(/^\s*const\s+fs\s*=\s*require\s*\(\s*['"]fs['"]\s*\)\.promises\s*;?\s*$/gm, '');
  return body;
}

// ═══════════════════════════════════════════════════════════════════════
// Remove inline requires (inside function bodies / blocks)
// ═══════════════════════════════════════════════════════════════════════

function removeInlineRequires(body) {
  // const crypto = require('crypto'); (inside blocks)
  body = body.replace(/\bconst\s+crypto\s*=\s*require\s*\(\s*['"]crypto['"]\s*\)\s*;?/g, '');
  // const fs = require('fs').promises;
  body = body.replace(/\bconst\s+fs\s*=\s*require\s*\(\s*['"]fs['"]\s*\)\.promises\s*;?/g, '');
  // const fs = require('fs');
  body = body.replace(/\bconst\s+fs\s*=\s*require\s*\(\s*['"]fs['"]\s*\)\s*;?/g, '');
  // const { execSync } = require('child_process');
  body = body.replace(/\bconst\s*\{[^}]*execSync[^}]*\}\s*=\s*require\s*\(\s*['"]child_process['"]\s*\)\s*;?/g,
    'const execSync = () => { throw new Error("execSync not available on Cloudflare"); };');

  // Replace crypto.X → X (since we import { createHash, createHmac, randomBytes } from 'crypto')
  // Handle both crypto.X and crypto\n      .X (multi-line)
  body = body.replace(/\bcrypto\s*\.createHash\b/g, 'createHash');
  body = body.replace(/\bcrypto\s*\.createHmac\b/g, 'createHmac');
  body = body.replace(/\bcrypto\s*\.randomBytes\b/g, 'randomBytes');

  return body;
}

// ═══════════════════════════════════════════════════════════════════════
// Transform fs operations
// ═══════════════════════════════════════════════════════════════════════

function transformFs(body) {
  // Use structural replacement for fs operations to handle multi-line calls
  body = replaceFsOperations(body);

  // path.join(process.cwd(), X) → just X
  body = body.replace(/path\.join\s*\(\s*process\.cwd\(\)\s*,\s*([^)]+)\)/g, '$1');
  // path.join(process.cwd()) → '.'
  body = body.replace(/path\.join\s*\(\s*process\.cwd\(\)\s*\)/g, '"."');
  // process.cwd() standalone
  body = body.replace(/\bprocess\.cwd\(\)/g, '"."');

  return body;
}

/**
 * Structural replacement for fs operations — handles multi-line calls
 */
function replaceFsOperations(code) {
  let result = '';
  let i = 0;

  while (i < code.length) {
    // Match: await fs.appendFile( or await fsp.appendFile( or fs.appendFile(
    const appendMatch = code.slice(i).match(/^(await\s+)?(?:fs|fsp)\.appendFile\s*\(/);
    if (appendMatch) {
      // Find matching close-paren
      const start = i;
      const parenStart = i + appendMatch[0].length - 1; // position of '('
      let depth = 1;
      let m = parenStart + 1;
      while (m < code.length && depth > 0) {
        if (code[m] === '(') depth++;
        if (code[m] === ')') depth--;
        if (code[m] === "'" || code[m] === '"' || code[m] === '`') {
          const q = code[m]; m++;
          while (m < code.length && code[m] !== q) { if (code[m] === '\\') m++; m++; }
        }
        m++;
      }
      // m now points past the closing )
      let endIdx = m;

      // Check for .catch(...) following
      let afterParens = endIdx;
      while (afterParens < code.length && /\s/.test(code[afterParens])) afterParens++;
      if (code.slice(afterParens, afterParens + 6) === '.catch') {
        const catchParenStart = code.indexOf('(', afterParens + 6);
        if (catchParenStart !== -1) {
          let d = 1;
          let cp = catchParenStart + 1;
          while (cp < code.length && d > 0) {
            if (code[cp] === '(') d++;
            if (code[cp] === ')') d--;
            if (code[cp] === "'" || code[cp] === '"' || code[cp] === '`') {
              const q = code[cp]; cp++;
              while (cp < code.length && code[cp] !== q) { if (code[cp] === '\\') cp++; cp++; }
            }
            cp++;
          }
          endIdx = cp;
        }
      }
      // Skip trailing semicolon
      while (endIdx < code.length && /\s/.test(code[endIdx])) endIdx++;
      if (code[endIdx] === ';') endIdx++;

      result += '/* fs.appendFile no-op */ void 0';
      i = endIdx;
      continue;
    }

    // Match: await fs.readFile( or await fsp.readFile(
    const readMatch = code.slice(i).match(/^(await\s+)?(?:fs|fsp)\.readFile\s*\(/);
    if (readMatch) {
      const start = i;
      const parenStart = i + readMatch[0].length - 1;
      let depth = 1;
      let m = parenStart + 1;
      while (m < code.length && depth > 0) {
        if (code[m] === '(') depth++;
        if (code[m] === ')') depth--;
        if (code[m] === "'" || code[m] === '"' || code[m] === '`') {
          const q = code[m]; m++;
          while (m < code.length && code[m] !== q) { if (code[m] === '\\') m++; m++; }
        }
        m++;
      }
      let endIdx = m;
      while (endIdx < code.length && /\s/.test(code[endIdx])) endIdx++;
      if (code[endIdx] === ';') endIdx++;
      result += '"" /* fs.readFile no-op */';
      i = endIdx;
      continue;
    }

    // Match: fs.readFileSync(
    const syncReadMatch = code.slice(i).match(/^fs\.readFileSync\s*\(/);
    if (syncReadMatch) {
      const parenStart = i + syncReadMatch[0].length - 1;
      let depth = 1;
      let m = parenStart + 1;
      while (m < code.length && depth > 0) {
        if (code[m] === '(') depth++;
        if (code[m] === ')') depth--;
        if (code[m] === "'" || code[m] === '"' || code[m] === '`') {
          const q = code[m]; m++;
          while (m < code.length && code[m] !== q) { if (code[m] === '\\') m++; m++; }
        }
        m++;
      }
      let endIdx = m;
      while (endIdx < code.length && /\s/.test(code[endIdx])) endIdx++;
      if (code[endIdx] === ';') endIdx++;
      result += '"" /* fs.readFileSync no-op */';
      i = endIdx;
      continue;
    }

    // Match: await fs.readdir(
    const readdirMatch = code.slice(i).match(/^(await\s+)?fs\.readdir\s*\(/);
    if (readdirMatch) {
      const parenStart = i + readdirMatch[0].length - 1;
      let depth = 1;
      let m = parenStart + 1;
      while (m < code.length && depth > 0) {
        if (code[m] === '(') depth++;
        if (code[m] === ')') depth--;
        m++;
      }
      let endIdx = m;
      while (endIdx < code.length && /\s/.test(code[endIdx])) endIdx++;
      if (code[endIdx] === ';') endIdx++;
      result += '[] /* fs.readdir no-op */';
      i = endIdx;
      continue;
    }

    // Match: await fs.mkdir(
    const mkdirMatch = code.slice(i).match(/^(await\s+)?fs\.mkdir\s*\(/);
    if (mkdirMatch) {
      const parenStart = i + mkdirMatch[0].length - 1;
      let depth = 1;
      let m = parenStart + 1;
      while (m < code.length && depth > 0) {
        if (code[m] === '(') depth++;
        if (code[m] === ')') depth--;
        m++;
      }
      let endIdx = m;
      while (endIdx < code.length && /\s/.test(code[endIdx])) endIdx++;
      if (code[endIdx] === ';') endIdx++;
      result += '/* fs.mkdir no-op */ void 0';
      i = endIdx;
      continue;
    }

    result += code[i];
    i++;
  }

  return result;
}

// ═══════════════════════════════════════════════════════════════════════
// Transform req/res patterns — the tricky part
// ═══════════════════════════════════════════════════════════════════════

function transformPatterns(body) {
  // ── Simple, safe replacements ──

  // req.method → request.method
  body = body.replace(/\breq\.method\b/g, 'request.method');

  // req.query.PARAM → url.searchParams.get("PARAM")
  body = body.replace(/req\.query\.(\w+)/g, 'url.searchParams.get("$1")');
  body = body.replace(/\breq\.query\b/g, 'url.searchParams');

  // req.headers → request.headers
  body = body.replace(/\breq\.headers\b/g, 'request.headers');

  // Vercel-specific headers
  body = body.replace(/['"]x-vercel-ip-country['"]/g, "'cf-ip-country'");
  body = body.replace(/['"]x-vercel-ip-country-region['"]/g, "'cf-region'");

  // req.body → await request.json()
  body = body.replace(/\breq\.body\b/g, 'await request.json()');

  // ── Remove duplicate CORS setHeaders (already handled by corsHeaders) ──
  body = body.replace(/^\s*res\.setHeader\s*\(\s*['"]Access-Control-[^'"]*['"]\s*,\s*[^)]*\)\s*;?\s*$/gm, '');

  // Other res.setHeader → corsHeaders
  body = body.replace(/^\s*res\.setHeader\s*\(\s*['"]Cache-Control['"]\s*,\s*['"]([^'"]*)['"]\s*\)\s*;?\s*$/gm,
    "  corsHeaders['Cache-Control'] = '$1';");
  body = body.replace(/^\s*res\.setHeader\s*\(\s*['"]([^'"]*)['"]\s*,\s*['"]([^'"]*)['"]\s*\)\s*;?\s*$/gm,
    "  corsHeaders['$1'] = '$2';");

  // ── res.status(N).end() → return new Response(null, { status: N, headers: corsHeaders }) ──
  body = body.replace(/return\s+res\.status\s*\((\d+)\)\s*\.end\s*\(\s*\)\s*;/g,
    'return new Response(null, { status: $1, headers: corsHeaders });');
  body = body.replace(/res\.status\s*\((\d+)\)\s*\.end\s*\(\s*\)\s*;/g,
    'return new Response(null, { status: $1, headers: corsHeaders });');

  // ── res.status(N).json(DATA) — structural replacement ──
  // We can't use regex for this because DATA can contain nested parens.
  // Instead, do a manual scan.
  body = replaceStatusJson(body);

  return body;
}

/**
 * Find and replace all res.status(N).json(DATA); patterns with
 * return new Response(JSON.stringify(DATA), { status: N, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
 *
 * Uses a bracket counter to find the matching close-paren for json(
 */
function replaceStatusJson(code) {
  let result = '';
  let i = 0;

  while (i < code.length) {
    // Look for res.status( or res.status (
    const statusMatch = code.slice(i).match(/^res\.status\s*\(/);
    if (!statusMatch) {
      result += code[i];
      i++;
      continue;
    }

    // Find the status code
    const statusStart = i + statusMatch[0].length;
    let parenDepth = 1;
    let j = statusStart;
    while (j < code.length && parenDepth > 0) {
      if (code[j] === '(') parenDepth++;
      if (code[j] === ')') parenDepth--;
      j++;
    }
    if (parenDepth !== 0) { result += code[i]; i++; continue; }
    const statusCode = code.slice(statusStart, j - 1).trim();

    // Skip whitespace, look for .json(
    let k = j;
    while (k < code.length && /\s/.test(code[k])) k++;
    if (code.slice(k, k + 6) !== '.json(') { result += code.slice(i, j); i = j; continue; }

    // Find matching close-paren for json(
    const jsonCallStart = k + 5; // position of '(' in .json(
    parenDepth = 1;
    let m = jsonCallStart + 1;
    while (m < code.length && parenDepth > 0) {
      if (code[m] === '(') parenDepth++;
      if (code[m] === ')') parenDepth--;
      // Skip string literals
      if (code[m] === "'" || code[m] === '"' || code[m] === '`') {
        const quote = code[m];
        m++;
        while (m < code.length && code[m] !== quote) {
          if (code[m] === '\\') m++; // skip escaped chars
          m++;
        }
      }
      m++;
    }
    if (parenDepth !== 0) { result += code.slice(i, j); i = j; continue; }

    const jsonData = code.slice(jsonCallStart + 1, m - 1).trim();

    // Check if there's a trailing semicolon
    let endIdx = m;
    while (endIdx < code.length && /\s/.test(code[endIdx])) endIdx++;
    if (code[endIdx] === ';') endIdx++;

    // Check if preceded by 'return '
    const beforeStatus = code.slice(Math.max(0, i - 20), i);
    const hasReturn = /\breturn\s+$/.test(beforeStatus);

    if (hasReturn) {
      // Strip only 'return ' keyword, preserve preceding whitespace/newline
      result = result.replace(/return\s+$/, '');
    }

    const replacement = `return new Response(JSON.stringify(${jsonData}), { status: ${statusCode}, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });`;

    result += replacement;
    i = endIdx;
  }

  return result;
}

// ═══════════════════════════════════════════════════════════════════════
// Remove readBody helper
// ═══════════════════════════════════════════════════════════════════════

function removeReadBody(body) {
  // Remove the readBody function definition using bracket counting
  const readBodyStart = body.indexOf('function readBody(');
  if (readBodyStart !== -1) {
    // Find the opening { of the function body
    let braceIdx = body.indexOf('{', readBodyStart + 'function readBody'.length);
    if (braceIdx !== -1) {
      let depth = 1;
      let m = braceIdx + 1;
      while (m < body.length && depth > 0) {
        if (body[m] === '{') depth++;
        if (body[m] === '}') depth--;
        m++;
      }
      // m now points past the closing }
      // Remove from readBodyStart to m, plus any trailing whitespace/newlines
      while (m < body.length && (body[m] === '\n' || body[m] === '\r' || body[m] === ' ' || body[m] === '\t')) m++;
      body = body.slice(0, readBodyStart) + body.slice(m);
    }
  }

  // Replace calls: await readBody(req) → (await request.json())
  body = body.replace(/await\s+readBody\s*\(\s*req\s*\)/g, '(await request.json())');
  body = body.replace(/readBody\s*\(\s*req\s*\)/g, '(await request.json())');

  return body;
}
