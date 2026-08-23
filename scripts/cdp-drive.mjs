#!/usr/bin/env node
/* cdp-drive.mjs — minimal Chrome DevTools Protocol driver for the user's logged-in browser.
 * Usage: node cdp-drive.mjs <cmd> [args...]
 *   list                     — list page targets
 *   new <url>                — open a tab
 *   nav <tabId> <url>        — navigate a tab
 *   title <tabId>            — get document title
 *   text <tabId>             — get body innerText (visible text)
 *   html <tabId>             — get document HTML
 *   url <tabId>              — get current URL
 *   eval <tabId> <js>        — evaluate JS (JSON-stringify result)
 *   cookie <domain>          — list cookies for a domain (from CDP Network domain)
 *   click <tabId> <selector> — click first match
 *   type <tabId> <selector> <text> — set input value (native setter + input event)
 *   wait <ms>
 */
import http from "node:http";

const CDP = "http://localhost:9222";

function getJSON(path) {
  return new Promise((res, rej) => {
    http.get(CDP + path, (r) => {
      let d = ""; r.on("data", (c) => (d += c)); r.on("end", () => { try { res(JSON.parse(d)); } catch (e) { rej(e); } });
    }).on("error", rej);
  });
}

function httpJson(method, path, body) {
  return new Promise((res, rej) => {
    const req = http.request({ host: "localhost", port: 9222, path, method }, (r) => {
      let d = ""; r.on("data", (c) => (d += c)); r.on("end", () => { try { res(JSON.parse(d)); } catch (e) { rej(e); } });
    });
    req.on("error", rej);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}


async function resolveTarget(idOrDash) {
  const targets = await getJSON("/json/list");
  if (idOrDash && idOrDash !== "-") {
    const t = targets.find((t) => t.id === idOrDash);
    if (!t) throw new Error("target not found: " + idOrDash);
    return t;
  }
  const page = targets.find((t) => t.type === "page");
  if (!page) throw new Error("no page target");
  return page;
}

let ws = null;
let msgId = 0;
const pending = new Map();

async function connect(wsUrl) {
  const { default: WebSocket } = await import("ws");
  ws = new WebSocket(wsUrl);
  await new Promise((res, rej) => { ws.on("open", res); ws.on("error", rej); });
  ws.on("message", (data) => {
    const m = JSON.parse(data.toString());
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  });
}

function send(method, params = {}) {
  return new Promise((res, rej) => {
    const id = ++msgId;
    pending.set(id, (m) => (m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result)));
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function pageTarget() {
  const targets = await getJSON("/json/list");
  const page = targets.find((t) => t.type === "page" && !t.url.startsWith("chrome://"));
  if (!page) throw new Error("no page target (open one with: new <url>)");
  return page;
}

async function main() {
  const [cmd, ...args] = process.argv.slice(2);
  switch (cmd) {
    case "list": {
      const ts = await getJSON("/json/list");
      ts.filter((t) => t.type === "page").forEach((t) => console.log(`${t.id}  ${t.title.slice(0, 40)}  ${t.url.slice(0, 70)}`));
      break;
    }
    case "new": {
      const t = await httpJson("PUT", "/json/new?" + encodeURIComponent(args[0] || "about:blank"));
      console.log(t.id);
      break;
    }
    case "nav": {
      const page = await resolveTarget(args[0]);
      await connect(page.webSocketDebuggerUrl);
      await send("Page.navigate", { url: args[1] });
      await new Promise((r) => setTimeout(r, args[2] ? parseInt(args[2]) : 2500));
      console.log("navigated");
      break;
    }
    case "title":
    case "text":
    case "html":
    case "url": {
      const page = await resolveTarget(args[0]);
      await connect(page.webSocketDebuggerUrl);
      if (cmd === "title") { const r = await send("Runtime.evaluate", { expression: "document.title", returnByValue: true }); console.log(r.result.value); }
      if (cmd === "text") { const r = await send("Runtime.evaluate", { expression: "document.body.innerText", returnByValue: true }); console.log(String(r.result.value || "").slice(0, 6000)); }
      if (cmd === "html") { const r = await send("Runtime.evaluate", { expression: "document.documentElement.outerHTML", returnByValue: true }); console.log(String(r.result.value || "").slice(0, 8000)); }
      if (cmd === "url") { const r = await send("Runtime.evaluate", { expression: "location.href", returnByValue: true }); console.log(r.result.value); }
      break;
    }
    case "eval": {
      const page = await resolveTarget(args[0]);
      await connect(page.webSocketDebuggerUrl);
      const r = await send("Runtime.evaluate", { expression: args[1], returnByValue: true, awaitPromise: true });
      console.log(typeof r.result.value === "string" ? r.result.value : JSON.stringify(r.result.value, null, 1));
      break;
    }
    case "cookie": {
      const page = await pageTarget();
      await connect(page.webSocketDebuggerUrl);
      const r = await send("Network.getAllCookies");
      const dom = args[0] || "";
      r.cookies.filter((c) => c.domain.includes(dom)).forEach((c) => console.log(`${c.domain}  ${c.name}=${c.value.slice(0, 20)}...`));
      break;
    }
    case "click": {
      const page = await resolveTarget(args[0]);
      await connect(page.webSocketDebuggerUrl);
      const r = await send("Runtime.evaluate", { expression: `(()=>{const e=document.querySelector(${JSON.stringify(args[1])});if(!e)return 'NO MATCH';e.click();return 'clicked';})()`, returnByValue: true });
      console.log(r.result.value);
      break;
    }
    case "type": {
      const page = await resolveTarget(args[0]);
      await connect(page.webSocketDebuggerUrl);
      const sel = args[1], val = args[2];
      const r = await send("Runtime.evaluate", { expression: `(()=>{const e=document.querySelector(${JSON.stringify(sel)});if(!e)return 'NO MATCH';const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;s.call(e,${JSON.stringify(val)});e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));return 'typed';})()`, returnByValue: true });
      console.log(r.result.value);
      break;
    }
    case "wait": {
      await new Promise((r) => setTimeout(r, parseInt(args[0]) || 3000));
      console.log("waited");
      break;
    }
    default:
      console.log("unknown cmd");
  }
  process.exit(0);
}

main().catch((e) => { console.error("ERR:", e.message); process.exit(1); });
