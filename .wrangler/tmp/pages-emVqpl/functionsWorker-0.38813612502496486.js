var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// api/eat-tick.js
var TASKS = {
  verify: /* @__PURE__ */ __name(async (env) => {
    const baseUrl = env?.SITE_URL || "https://csoai-sovereign.pages.dev";
    try {
      const r = await fetch(`${baseUrl}/api/daily-golden`, { signal: AbortSignal.timeout(15e3) });
      const j = await r.json();
      return {
        task: "verify",
        started_at: (/* @__PURE__ */ new Date()).toISOString(),
        golden: j.pass + "/" + (j.pass + j.fail) + " ok",
        pass: j.pass,
        fail: j.fail,
        total_ms: j.total_ms
      };
    } catch (e) {
      return { task: "verify", started_at: (/* @__PURE__ */ new Date()).toISOString(), error: e.message };
    }
  }, "verify"),
  status: /* @__PURE__ */ __name(async (env) => {
    const baseUrl = env?.SITE_URL || "https://csoai-sovereign.pages.dev";
    try {
      const r = await fetch(`${baseUrl}/api/eat-status`, { signal: AbortSignal.timeout(1e4) });
      return await r.json();
    } catch (e) {
      return { task: "status", started_at: (/* @__PURE__ */ new Date()).toISOString(), error: e.message };
    }
  }, "status")
};
async function onRequest(context) {
  const { request, env } = context;
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Send-Key",
    "Content-Type": "application/json"
  };
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }
  const provided = (request.headers.get("x-send-key") || "").trim();
  const expected = env?.SEND_KEY || env?.SIGNUP_WEBHOOK_SECRET || "";
  if (expected && provided !== expected) {
    return new Response(JSON.stringify({ error: "Invalid X-Send-Key" }), { status: 401, headers });
  }
  if (request.method === "GET") {
    return new Response(
      JSON.stringify({
        ok: true,
        available_tasks: Object.keys(TASKS),
        usage: 'POST /api/eat-tick with body { task: "verify" } or X-Send-Key header for auth'
      }),
      { status: 200, headers }
    );
  }
  if (request.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
  }
  let body = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const taskName = (body.task || "verify").toString();
  const fn = TASKS[taskName];
  if (!fn) {
    return new Response(
      JSON.stringify({ error: "unknown task", available: Object.keys(TASKS) }),
      { status: 400, headers }
    );
  }
  const t0 = Date.now();
  let result;
  try {
    result = await fn(env);
  } catch (e) {
    result = { error: e.message };
  }
  const ms = Date.now() - t0;
  const tick_record = {
    tick_id: "eat_" + crypto.randomUUID().replace(/-/g, "").slice(0, 16),
    task: taskName,
    started_at: new Date(t0).toISOString(),
    elapsed_ms: ms,
    result
  };
  const encoder = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest("SHA-512", encoder.encode(JSON.stringify(tick_record)));
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  tick_record.sigil_chain_hash = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  return new Response(JSON.stringify({ ok: true, tick: tick_record }), { status: 200, headers });
}
__name(onRequest, "onRequest");

// api/health.js
async function onRequest2(context) {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json"
  };
  if (context.request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }
  return new Response(
    JSON.stringify({
      status: "ok",
      platform: "cloudflare-pages",
      project: "csoai-static-deploy2",
      pages: parseInt(context.env?.PAGE_COUNT || "752", 10),
      phase: 100,
      sigil: "tick-180",
      deployed: (/* @__PURE__ */ new Date()).toISOString()
    }),
    { status: 200, headers }
  );
}
__name(onRequest2, "onRequest");

// api/leaderboard.js
var HMAC_SECRET = "csoai-sov33-leaderboard-default-2026-sovereign-hmac";
var BENCHMARKS = ["mmlu", "gsm8k", "aime", "ifeval", "bbh"];
var SOV33_BASELINES = {
  sov33_small: { mmlu: 0.642, gsm8k: 0.581, aime: 0.187, ifeval: 0.713, bbh: 0.524 },
  sov33_large: { mmlu: 0.781, gsm8k: 0.812, aime: 0.413, ifeval: 0.832, bbh: 0.711 }
};
var COMPETITORS = [
  { id: "gpt-4o", mmlu: 0.887, gsm8k: 0.962, ifeval: 0.847, source: "gpt-4o model card (2024-08)" },
  { id: "claude-3.5-sonnet", mmlu: 0.882, gsm8k: 0.961, ifeval: 0.876, source: "claude-3.5-sonnet model card (2024-10)" },
  { id: "llama-3.1-405b", mmlu: 0.886, gsm8k: 0.964, ifeval: 0.857, source: "llama-3.1-405b model card (2024-07)" },
  { id: "deepseek-v3", mmlu: 0.882, gsm8k: 0.89, ifeval: 0.831, source: "deepseek-v3 technical report (2024-12)" },
  { id: "qwen2.5-72b", mmlu: 0.86, gsm8k: 0.91, ifeval: 0.84, source: "qwen2.5-72b model card (2024-09)" }
];
async function hmacSigil(payloadObj) {
  const canonical = JSON.stringify(payloadObj, Object.keys(payloadObj).sort());
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(HMAC_SECRET),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, encoder.encode(canonical));
  return Array.from(new Uint8Array(sig)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
__name(hmacSigil, "hmacSigil");
async function onRequest3(context) {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
    "Cache-Control": "no-store"
  };
  if (context.request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }
  if (context.request.method !== "GET") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
  }
  const tsIso = (/* @__PURE__ */ new Date()).toISOString();
  const boards = {};
  for (const model of ["sov33_small", "sov33_large"]) {
    boards[model] = {};
    for (const b of BENCHMARKS) {
      boards[model][b] = {
        score: SOV33_BASELINES[model][b],
        runs: 0,
        source: "published-baseline"
      };
    }
  }
  const flatten = /* @__PURE__ */ __name((obj) => {
    const out = {};
    for (const b of BENCHMARKS) out[b] = obj[b].score;
    return out;
  }, "flatten");
  const payload = {
    sov33_small: flatten(boards.sov33_small),
    sov33_large: flatten(boards.sov33_large),
    compared_to: COMPETITORS,
    runs_aggregated: 0,
    benchmarks_tracked: BENCHMARKS,
    benchmark_breakdown: boards,
    timestamp: tsIso
  };
  const sigil = await hmacSigil(payload);
  return new Response(
    JSON.stringify({
      status: "leaderboard_readout",
      ...payload,
      sigil_algo: "HMAC-SHA256",
      sigil,
      note: "Cloudflare Pages Function \u2014 scores reflect published SOV33 baseline. Submit benchmark runs via POST /api/benchmark-run to populate with live data."
    }),
    { status: 200, headers }
  );
}
__name(onRequest3, "onRequest");

// api/sov-bridge.js
var OLLAMA_URL = "http://localhost:11434";
function mockChatResponse(messages) {
  const last = messages[messages.length - 1];
  const content = last?.content || "No input provided.";
  return {
    id: `chatcmpl-mock-${Date.now()}`,
    object: "chat.completion",
    created: Math.floor(Date.now() / 1e3),
    model: "sov33-bridge-mock",
    choices: [
      {
        index: 0,
        message: {
          role: "assistant",
          content: `[SOV Bridge Mock] Received ${messages.length} message(s). Last: "${content.slice(0, 120)}". Ollama is not reachable from this environment \u2014 deploy to a worker with local Ollama access for live responses.`
        },
        finish_reason: "stop"
      }
    ],
    usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 }
  };
}
__name(mockChatResponse, "mockChatResponse");
async function onRequest4(context) {
  const { request, env } = context;
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Content-Type": "application/json"
  };
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }
  if (request.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed \u2014 use POST" }), { status: 405, headers });
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON body" }), { status: 400, headers });
  }
  const messages = body.messages || [];
  const model = body.model || "sov33-master-v2:latest";
  const ollamaUrl = env?.OLLAMA_URL || OLLAMA_URL;
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15e3);
    const r = await fetch(`${ollamaUrl}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model,
        messages: messages.map((m) => ({ role: m.role, content: m.content })),
        stream: false
      }),
      signal: controller.signal
    });
    clearTimeout(timeout);
    if (r.ok) {
      const data = await r.json();
      const reply = data.message?.content || "";
      return new Response(
        JSON.stringify({
          id: `chatcmpl-sov-${Date.now()}`,
          object: "chat.completion",
          created: Math.floor(Date.now() / 1e3),
          model: data.model || model,
          choices: [
            {
              index: 0,
              message: { role: "assistant", content: reply },
              finish_reason: "stop"
            }
          ],
          usage: {
            prompt_tokens: data.prompt_eval_count || 0,
            completion_tokens: data.eval_count || 0,
            total_tokens: (data.prompt_eval_count || 0) + (data.eval_count || 0)
          },
          ollama_total_duration_ms: data.total_duration ? Math.round(data.total_duration / 1e6) : null
        }),
        { status: 200, headers }
      );
    }
  } catch {
  }
  return new Response(JSON.stringify(mockChatResponse(messages)), { status: 200, headers });
}
__name(onRequest4, "onRequest");

// api/stats.js
async function onRequest5(context) {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
    "Cache-Control": "public, max-age=60"
  };
  if (context.request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }
  if (context.request.method !== "GET") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
  }
  const signupTotal = parseInt(context.env?.SIGNUP_TOTAL || "0", 10) || 0;
  const pageCount = parseInt(context.env?.PAGE_COUNT || "226", 10) || 226;
  return new Response(
    JSON.stringify({
      signups: {
        total: signupTotal,
        week: 0,
        day: 0,
        source: signupTotal > 0 ? "live" : "conservative-baseline"
      },
      empire: {
        pages: pageCount,
        mcps: "30/30",
        repos: "15/15",
        sigil_chain: "live",
        sov3_mesh_port: 3101,
        bft_council_quorum: "23/33",
        data_corpus_gb: 49,
        care_floor: 0.95,
        sigma_audit: null
      },
      pipeline: {
        defence_primes_evaluating: 7,
        defence_primes_evaluating_source: "illustrative \u2014 clear of any one prime until converted",
        regulators_in_cooperation: 3,
        regulators_in_cooperation_source: "illustrative \u2014 confirmed pipeline not public"
      },
      sovereign: {
        key_alias: "d75a9801\u20267511a",
        sigil_algo: "Ed25519",
        pqc_target: "ML-DSA-65",
        pqc_migration_year: 2027,
        sigil_per_day: 86400
      },
      timestamp: (/* @__PURE__ */ new Date()).toISOString(),
      note: "Cloudflare Pages Function. Baked Empire numbers reflect real substrate state. Pipeline numbers are explicitly illustrative."
    }),
    { status: 200, headers }
  );
}
__name(onRequest5, "onRequest");

// api/_middleware.js
var CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Send-Key",
  "Access-Control-Max-Age": "86400"
};
async function onRequest6(context) {
  if (context.request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  const response = await context.next();
  const newResponse = new Response(response.body, response);
  for (const [k, v] of Object.entries(CORS_HEADERS)) {
    newResponse.headers.set(k, v);
  }
  return newResponse;
}
__name(onRequest6, "onRequest");

// ../.wrangler/tmp/pages-emVqpl/functionsRoutes-0.21208462680316198.mjs
var routes = [
  {
    routePath: "/api/eat-tick",
    mountPath: "/api",
    method: "",
    middlewares: [],
    modules: [onRequest]
  },
  {
    routePath: "/api/health",
    mountPath: "/api",
    method: "",
    middlewares: [],
    modules: [onRequest2]
  },
  {
    routePath: "/api/leaderboard",
    mountPath: "/api",
    method: "",
    middlewares: [],
    modules: [onRequest3]
  },
  {
    routePath: "/api/sov-bridge",
    mountPath: "/api",
    method: "",
    middlewares: [],
    modules: [onRequest4]
  },
  {
    routePath: "/api/stats",
    mountPath: "/api",
    method: "",
    middlewares: [],
    modules: [onRequest5]
  },
  {
    routePath: "/api",
    mountPath: "/api",
    method: "",
    middlewares: [onRequest6],
    modules: []
  }
];

// ../../../.npm/_npx/32026684e21afda6/node_modules/path-to-regexp/dist.es2015/index.js
function lexer(str) {
  var tokens = [];
  var i = 0;
  while (i < str.length) {
    var char = str[i];
    if (char === "*" || char === "+" || char === "?") {
      tokens.push({ type: "MODIFIER", index: i, value: str[i++] });
      continue;
    }
    if (char === "\\") {
      tokens.push({ type: "ESCAPED_CHAR", index: i++, value: str[i++] });
      continue;
    }
    if (char === "{") {
      tokens.push({ type: "OPEN", index: i, value: str[i++] });
      continue;
    }
    if (char === "}") {
      tokens.push({ type: "CLOSE", index: i, value: str[i++] });
      continue;
    }
    if (char === ":") {
      var name = "";
      var j = i + 1;
      while (j < str.length) {
        var code = str.charCodeAt(j);
        if (
          // `0-9`
          code >= 48 && code <= 57 || // `A-Z`
          code >= 65 && code <= 90 || // `a-z`
          code >= 97 && code <= 122 || // `_`
          code === 95
        ) {
          name += str[j++];
          continue;
        }
        break;
      }
      if (!name)
        throw new TypeError("Missing parameter name at ".concat(i));
      tokens.push({ type: "NAME", index: i, value: name });
      i = j;
      continue;
    }
    if (char === "(") {
      var count = 1;
      var pattern = "";
      var j = i + 1;
      if (str[j] === "?") {
        throw new TypeError('Pattern cannot start with "?" at '.concat(j));
      }
      while (j < str.length) {
        if (str[j] === "\\") {
          pattern += str[j++] + str[j++];
          continue;
        }
        if (str[j] === ")") {
          count--;
          if (count === 0) {
            j++;
            break;
          }
        } else if (str[j] === "(") {
          count++;
          if (str[j + 1] !== "?") {
            throw new TypeError("Capturing groups are not allowed at ".concat(j));
          }
        }
        pattern += str[j++];
      }
      if (count)
        throw new TypeError("Unbalanced pattern at ".concat(i));
      if (!pattern)
        throw new TypeError("Missing pattern at ".concat(i));
      tokens.push({ type: "PATTERN", index: i, value: pattern });
      i = j;
      continue;
    }
    tokens.push({ type: "CHAR", index: i, value: str[i++] });
  }
  tokens.push({ type: "END", index: i, value: "" });
  return tokens;
}
__name(lexer, "lexer");
function parse(str, options) {
  if (options === void 0) {
    options = {};
  }
  var tokens = lexer(str);
  var _a = options.prefixes, prefixes = _a === void 0 ? "./" : _a, _b = options.delimiter, delimiter = _b === void 0 ? "/#?" : _b;
  var result = [];
  var key = 0;
  var i = 0;
  var path = "";
  var tryConsume = /* @__PURE__ */ __name(function(type) {
    if (i < tokens.length && tokens[i].type === type)
      return tokens[i++].value;
  }, "tryConsume");
  var mustConsume = /* @__PURE__ */ __name(function(type) {
    var value2 = tryConsume(type);
    if (value2 !== void 0)
      return value2;
    var _a2 = tokens[i], nextType = _a2.type, index = _a2.index;
    throw new TypeError("Unexpected ".concat(nextType, " at ").concat(index, ", expected ").concat(type));
  }, "mustConsume");
  var consumeText = /* @__PURE__ */ __name(function() {
    var result2 = "";
    var value2;
    while (value2 = tryConsume("CHAR") || tryConsume("ESCAPED_CHAR")) {
      result2 += value2;
    }
    return result2;
  }, "consumeText");
  var isSafe = /* @__PURE__ */ __name(function(value2) {
    for (var _i = 0, delimiter_1 = delimiter; _i < delimiter_1.length; _i++) {
      var char2 = delimiter_1[_i];
      if (value2.indexOf(char2) > -1)
        return true;
    }
    return false;
  }, "isSafe");
  var safePattern = /* @__PURE__ */ __name(function(prefix2) {
    var prev = result[result.length - 1];
    var prevText = prefix2 || (prev && typeof prev === "string" ? prev : "");
    if (prev && !prevText) {
      throw new TypeError('Must have text between two parameters, missing text after "'.concat(prev.name, '"'));
    }
    if (!prevText || isSafe(prevText))
      return "[^".concat(escapeString(delimiter), "]+?");
    return "(?:(?!".concat(escapeString(prevText), ")[^").concat(escapeString(delimiter), "])+?");
  }, "safePattern");
  while (i < tokens.length) {
    var char = tryConsume("CHAR");
    var name = tryConsume("NAME");
    var pattern = tryConsume("PATTERN");
    if (name || pattern) {
      var prefix = char || "";
      if (prefixes.indexOf(prefix) === -1) {
        path += prefix;
        prefix = "";
      }
      if (path) {
        result.push(path);
        path = "";
      }
      result.push({
        name: name || key++,
        prefix,
        suffix: "",
        pattern: pattern || safePattern(prefix),
        modifier: tryConsume("MODIFIER") || ""
      });
      continue;
    }
    var value = char || tryConsume("ESCAPED_CHAR");
    if (value) {
      path += value;
      continue;
    }
    if (path) {
      result.push(path);
      path = "";
    }
    var open = tryConsume("OPEN");
    if (open) {
      var prefix = consumeText();
      var name_1 = tryConsume("NAME") || "";
      var pattern_1 = tryConsume("PATTERN") || "";
      var suffix = consumeText();
      mustConsume("CLOSE");
      result.push({
        name: name_1 || (pattern_1 ? key++ : ""),
        pattern: name_1 && !pattern_1 ? safePattern(prefix) : pattern_1,
        prefix,
        suffix,
        modifier: tryConsume("MODIFIER") || ""
      });
      continue;
    }
    mustConsume("END");
  }
  return result;
}
__name(parse, "parse");
function match(str, options) {
  var keys = [];
  var re = pathToRegexp(str, keys, options);
  return regexpToFunction(re, keys, options);
}
__name(match, "match");
function regexpToFunction(re, keys, options) {
  if (options === void 0) {
    options = {};
  }
  var _a = options.decode, decode = _a === void 0 ? function(x) {
    return x;
  } : _a;
  return function(pathname) {
    var m = re.exec(pathname);
    if (!m)
      return false;
    var path = m[0], index = m.index;
    var params = /* @__PURE__ */ Object.create(null);
    var _loop_1 = /* @__PURE__ */ __name(function(i2) {
      if (m[i2] === void 0)
        return "continue";
      var key = keys[i2 - 1];
      if (key.modifier === "*" || key.modifier === "+") {
        params[key.name] = m[i2].split(key.prefix + key.suffix).map(function(value) {
          return decode(value, key);
        });
      } else {
        params[key.name] = decode(m[i2], key);
      }
    }, "_loop_1");
    for (var i = 1; i < m.length; i++) {
      _loop_1(i);
    }
    return { path, index, params };
  };
}
__name(regexpToFunction, "regexpToFunction");
function escapeString(str) {
  return str.replace(/([.+*?=^!:${}()[\]|/\\])/g, "\\$1");
}
__name(escapeString, "escapeString");
function flags(options) {
  return options && options.sensitive ? "" : "i";
}
__name(flags, "flags");
function regexpToRegexp(path, keys) {
  if (!keys)
    return path;
  var groupsRegex = /\((?:\?<(.*?)>)?(?!\?)/g;
  var index = 0;
  var execResult = groupsRegex.exec(path.source);
  while (execResult) {
    keys.push({
      // Use parenthesized substring match if available, index otherwise
      name: execResult[1] || index++,
      prefix: "",
      suffix: "",
      modifier: "",
      pattern: ""
    });
    execResult = groupsRegex.exec(path.source);
  }
  return path;
}
__name(regexpToRegexp, "regexpToRegexp");
function arrayToRegexp(paths, keys, options) {
  var parts = paths.map(function(path) {
    return pathToRegexp(path, keys, options).source;
  });
  return new RegExp("(?:".concat(parts.join("|"), ")"), flags(options));
}
__name(arrayToRegexp, "arrayToRegexp");
function stringToRegexp(path, keys, options) {
  return tokensToRegexp(parse(path, options), keys, options);
}
__name(stringToRegexp, "stringToRegexp");
function tokensToRegexp(tokens, keys, options) {
  if (options === void 0) {
    options = {};
  }
  var _a = options.strict, strict = _a === void 0 ? false : _a, _b = options.start, start = _b === void 0 ? true : _b, _c = options.end, end = _c === void 0 ? true : _c, _d = options.encode, encode = _d === void 0 ? function(x) {
    return x;
  } : _d, _e = options.delimiter, delimiter = _e === void 0 ? "/#?" : _e, _f = options.endsWith, endsWith = _f === void 0 ? "" : _f;
  var endsWithRe = "[".concat(escapeString(endsWith), "]|$");
  var delimiterRe = "[".concat(escapeString(delimiter), "]");
  var route = start ? "^" : "";
  for (var _i = 0, tokens_1 = tokens; _i < tokens_1.length; _i++) {
    var token = tokens_1[_i];
    if (typeof token === "string") {
      route += escapeString(encode(token));
    } else {
      var prefix = escapeString(encode(token.prefix));
      var suffix = escapeString(encode(token.suffix));
      if (token.pattern) {
        if (keys)
          keys.push(token);
        if (prefix || suffix) {
          if (token.modifier === "+" || token.modifier === "*") {
            var mod = token.modifier === "*" ? "?" : "";
            route += "(?:".concat(prefix, "((?:").concat(token.pattern, ")(?:").concat(suffix).concat(prefix, "(?:").concat(token.pattern, "))*)").concat(suffix, ")").concat(mod);
          } else {
            route += "(?:".concat(prefix, "(").concat(token.pattern, ")").concat(suffix, ")").concat(token.modifier);
          }
        } else {
          if (token.modifier === "+" || token.modifier === "*") {
            throw new TypeError('Can not repeat "'.concat(token.name, '" without a prefix and suffix'));
          }
          route += "(".concat(token.pattern, ")").concat(token.modifier);
        }
      } else {
        route += "(?:".concat(prefix).concat(suffix, ")").concat(token.modifier);
      }
    }
  }
  if (end) {
    if (!strict)
      route += "".concat(delimiterRe, "?");
    route += !options.endsWith ? "$" : "(?=".concat(endsWithRe, ")");
  } else {
    var endToken = tokens[tokens.length - 1];
    var isEndDelimited = typeof endToken === "string" ? delimiterRe.indexOf(endToken[endToken.length - 1]) > -1 : endToken === void 0;
    if (!strict) {
      route += "(?:".concat(delimiterRe, "(?=").concat(endsWithRe, "))?");
    }
    if (!isEndDelimited) {
      route += "(?=".concat(delimiterRe, "|").concat(endsWithRe, ")");
    }
  }
  return new RegExp(route, flags(options));
}
__name(tokensToRegexp, "tokensToRegexp");
function pathToRegexp(path, keys, options) {
  if (path instanceof RegExp)
    return regexpToRegexp(path, keys);
  if (Array.isArray(path))
    return arrayToRegexp(path, keys, options);
  return stringToRegexp(path, keys, options);
}
__name(pathToRegexp, "pathToRegexp");

// ../../../.npm/_npx/32026684e21afda6/node_modules/wrangler/templates/pages-template-worker.ts
var escapeRegex = /[.+?^${}()|[\]\\]/g;
function* executeRequest(request) {
  const requestPath = new URL(request.url).pathname;
  for (const route of [...routes].reverse()) {
    if (route.method && route.method !== request.method) {
      continue;
    }
    const routeMatcher = match(route.routePath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const mountMatcher = match(route.mountPath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const matchResult = routeMatcher(requestPath);
    const mountMatchResult = mountMatcher(requestPath);
    if (matchResult && mountMatchResult) {
      for (const handler of route.middlewares.flat()) {
        yield {
          handler,
          params: matchResult.params,
          path: mountMatchResult.path
        };
      }
    }
  }
  for (const route of routes) {
    if (route.method && route.method !== request.method) {
      continue;
    }
    const routeMatcher = match(route.routePath.replace(escapeRegex, "\\$&"), {
      end: true
    });
    const mountMatcher = match(route.mountPath.replace(escapeRegex, "\\$&"), {
      end: false
    });
    const matchResult = routeMatcher(requestPath);
    const mountMatchResult = mountMatcher(requestPath);
    if (matchResult && mountMatchResult && route.modules.length) {
      for (const handler of route.modules.flat()) {
        yield {
          handler,
          params: matchResult.params,
          path: matchResult.path
        };
      }
      break;
    }
  }
}
__name(executeRequest, "executeRequest");
var pages_template_worker_default = {
  async fetch(originalRequest, env, workerContext) {
    let request = originalRequest;
    const handlerIterator = executeRequest(request);
    let data = {};
    let isFailOpen = false;
    const next = /* @__PURE__ */ __name(async (input, init) => {
      if (input !== void 0) {
        let url = input;
        if (typeof input === "string") {
          url = new URL(input, request.url).toString();
        }
        request = new Request(url, init);
      }
      const result = handlerIterator.next();
      if (result.done === false) {
        const { handler, params, path } = result.value;
        const context = {
          request: new Request(request.clone()),
          functionPath: path,
          next,
          params,
          get data() {
            return data;
          },
          set data(value) {
            if (typeof value !== "object" || value === null) {
              throw new Error("context.data must be an object");
            }
            data = value;
          },
          env,
          waitUntil: workerContext.waitUntil.bind(workerContext),
          passThroughOnException: /* @__PURE__ */ __name(() => {
            isFailOpen = true;
          }, "passThroughOnException")
        };
        const response = await handler(context);
        if (!(response instanceof Response)) {
          throw new Error("Your Pages function should return a Response");
        }
        return cloneResponse(response);
      } else if ("ASSETS") {
        const response = await env["ASSETS"].fetch(request);
        return cloneResponse(response);
      } else {
        const response = await fetch(request);
        return cloneResponse(response);
      }
    }, "next");
    try {
      return await next();
    } catch (error) {
      if (isFailOpen) {
        const response = await env["ASSETS"].fetch(request);
        return cloneResponse(response);
      }
      throw error;
    }
  }
};
var cloneResponse = /* @__PURE__ */ __name((response) => (
  // https://fetch.spec.whatwg.org/#null-body-status
  new Response(
    [101, 204, 205, 304].includes(response.status) ? null : response.body,
    response
  )
), "cloneResponse");
export {
  pages_template_worker_default as default
};
