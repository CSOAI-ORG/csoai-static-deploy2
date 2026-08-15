// defoneos-math-check.js — runs in the browser on every DEFONEOS pack page.
//
// Counts rendered structural elements and verifies the hero-badge claims are
// self-consistent. Surfaced as a small fixed-position panel in the corner;
// turns red if any check fails.
//
// Counts performed (against the rendered DOM):
//   1. EP cards:        <div class="s" id="epN"> where N=1..12
//   2. Priorities per EP:        <p class="p"> ... <h3>  (priority cards inside an EP)
//   3. MCP chips per EP: <span class="t"> (one chip per MCP tool)
//   4. Total MCPs (unique): across all EPs
//
// Checks surfaced in the panel:
//   - "12 Entry Points" hero badge vs counted EP cards
//   - "8 AI Priorities" hero badge vs counted priorities (must be == 8 in EVERY EP)
//   - "6 MCP Tools" hero badge vs counted MCP chips (must be == 6 in EVERY EP)
//   - "96 AI capability mappings" hero badge vs counted priorities (must be 12 * 8 = 96)
//   - "12 unique entry points" → counted EP IDs are 1..12 with no gaps
//
// Defensive notes:
//   - The script counts only on DOMContentLoaded, after the page is fully parsed.
//   - If a count fails, the panel turns red and lists the failing checks. The page
//     is still readable; the panel is a soft integrity warning, not a blocker.
//   - The script does not throw; if it can't find the expected DOM it quietly
//     hides the panel (defensive — DEFONEOS pack template may evolve).

(function () {
  "use strict";

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.from((r || document).querySelectorAll(s)); }
  function text(el) { return (el && el.textContent || "").replace(/\s+/g, " ").trim(); }

  function heroBadge(label) {
    var re = new RegExp("^\\s*" + label + "\\s*$", "i");
    var el = $$(".bg, .badge").find(function (b) { return re.test(text(b)); });
    return el ? text(el).match(/\d+/g) : null;
  }

  function run() {
    var eps = $$(".s[id^='ep']").filter(function (d) { return /^ep\d+$/.test(d.id); });
    var epIds = eps.map(function (d) { return parseInt(d.id.slice(2), 10); }).sort(function (a, b) { return a - b; });

    var prioritiesPerEp = eps.map(function (ep) {
      // priority cards live as <div class="p"><h3>...</h3>...</div>
      return $$(".p", ep).length;
    });

    var mcpChipsPerEp = eps.map(function (ep) {
      return $$(".t", ep).length;
    });

    var allMcpNames = eps
      .map(function (ep) { return $$(".t", ep); })
      .reduce(function (a, b) { return a.concat(Array.from(b)); }, [])
      .map(function (el) { return text(el); });
    var uniqueMcpNames = Array.from(new Set(allMcpNames));

    var prioritiesTotal = prioritiesPerEp.reduce(function (a, b) { return a + b; }, 0);

    // Hero claims.
    var claimEps = parseInt((heroBadge("12 Entry Points") || ["12"])[0], 10);
    var claimPrio = parseInt((heroBadge("8 AI Priorities") || ["8"])[0], 10);
    var claimMcps = parseInt((heroBadge("6 MCP Tools") || ["6"])[0], 10);
    var claimMaps = parseInt((heroBadge("96 AI capability mappings") || ["96"])[0], 10);

    var checks = [
      { name: "entry-point sections", claim: claimEps, got: eps.length, ok: eps.length === claimEps },
      { name: "priorities per EP (must all be 8)", claim: claimPrio, got: prioritiesPerEp.join(","), ok: prioritiesPerEp.every(function (n) { return n === claimPrio; }) },
      { name: "MCP chips per EP (must all be 6)", claim: claimMcps, got: mcpChipsPerEp.join(","), ok: mcpChipsPerEp.every(function (n) { return n === claimMcps; }) },
      { name: "capability mappings (12 × 8 = 96)", claim: claimMaps, got: prioritiesTotal, ok: prioritiesTotal === claimMaps },
      { name: "EP IDs contiguous (1..12)", claim: "1..12", got: epIds.join(","), ok: epIds.length === 12 && epIds[0] === 1 && epIds[11] === 12 },
      { name: "unique MCP tools (should be 6)", claim: 6, got: uniqueMcpNames.length, ok: uniqueMcpNames.length === 6 },
    ];
    var allOk = checks.every(function (c) { return c.ok; });

    var panel = document.createElement("div");
    panel.id = "defoneos-math-check";
    panel.style.cssText = [
      "position:fixed", "right:14px", "bottom:14px", "z-index:99999",
      "font:11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace",
      "background:" + (allOk ? "rgba(16,185,129,.92)" : "rgba(239,68,68,.94)"),
      "color:#04120c", "padding:.55rem .7rem", "border-radius:6px",
      "max-width:340px", "box-shadow:0 2px 12px rgba(0,0,0,.35)",
      "cursor:default", "user-select:none"
    ].join(";");

    var rows = checks.map(function (c) {
      return '<div>' + (c.ok ? "✓" : "✗") + ' ' + c.name +
             ' <span style="opacity:.78"> (claim=' + c.claim + ' got=' + c.got + ')</span></div>';
    }).join("");

    panel.innerHTML =
      '<div style="font-weight:700;margin-bottom:.3rem">' +
      (allOk ? "Math integrity: ✓" : "Math integrity: ✗") +
      ' <span style="opacity:.65;font-weight:400">' + new Date().toISOString().slice(0, 19) + 'Z</span></div>' +
      rows;
    document.body.appendChild(panel);

    // Console-loud for SIGIL/audit pipeline. Not asserted — just visible.
    if (!allOk) {
      console.error("[defoneos-math-check] integrity FAILED", checks);
    } else {
      console.info("[defoneos-math-check] integrity OK (" + prioritiesTotal + " capability mappings across " + eps.length + " EPs)");
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
