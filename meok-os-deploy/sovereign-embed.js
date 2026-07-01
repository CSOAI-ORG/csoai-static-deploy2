/*! sovereign-embed.js — drop the Sovereign into ANY site in one line.
 *  CSOAI Ltd UK · MIT. Adds a governed AI-OS dock (chat + sidebar + actions) that speaks
 *  to the SHARED sovereign backend (os.meok.ai/api/*). Public users meet SOV3; the master
 *  SOV33 (King · Hive · SIGIL · Horus) governs & learns behind it.
 *
 *  USE:
 *    <script>window.SOVEREIGN_CONFIG={ brand:'CSOAI', accent:'#c9a84c',
 *      sections:[{label:'Home',href:'/'},{label:'Graph',href:'/graph'},{label:'Plans',href:'/plans'}],
 *      commands:{ open_graph:()=>location.href='/graph' } };</script>
 *    <script src="https://os.meok.ai/sovereign-embed.js" defer></script>
 *
 *  That's it: a 🐉 orb (bottom-right), a chat panel, an optional ☰ sidebar from `sections`,
 *  and the Sovereign takes real actions via `window.sovereignOSCommands` + /api/orchestrate.
 */
(function () {
  'use strict';
  if (window.__SOVEREIGN_EMBED__) return; window.__SOVEREIGN_EMBED__ = true;
  var CFG = window.SOVEREIGN_CONFIG || {};
  var API = (CFG.endpoint || 'https://os.meok.ai/api').replace(/\/$/, '');
  var ACCENT = CFG.accent || '#c9a84c';
  var BRAND = CFG.brand || 'CSOAI';
  var CITIZEN = CFG.citizenId || 'csoai-web';
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); };

  /* ---------- what the Sovereign SEES (host can override window.getScreenContext) ---------- */
  if (typeof window.getScreenContext !== 'function') {
    window.getScreenContext = function () {
      var heads = [].slice.call(document.querySelectorAll('h1,h2')).slice(0, 6).map(function (h) { return (h.textContent || '').trim().slice(0, 60); }).filter(Boolean);
      return { surface: BRAND.toLowerCase() + '-web', url: location.pathname, title: document.title,
        headings: heads, doctrine: 'sovereign', brain: 'sandwich', care_floor: 0.95,
        selected_node: (window.__sovNode || null) };
    };
  }
  /* ---------- what the Sovereign can DO (host commands merge in) ---------- */
  window.sovereignOSCommands = Object.assign({
    navigate: function (a) { if (a && a.href) location.href = a.href; return { ok: 1 }; },
    open_section: function (a) { var s = (CFG.sections || []).find(function (x) { return (x.id || x.label || '').toLowerCase() === String(a && a.id || '').toLowerCase(); }); if (s && s.href) location.href = s.href; return { ok: !!s }; },
    scroll_to: function (a) { try { document.querySelector(a.sel).scrollIntoView({ behavior: 'smooth' }); } catch (e) {} return { ok: 1 }; },
    utter: function () { return { ok: 1 }; }
  }, CFG.commands || {});

  /* ---------- shared sovereign services (same backend as MEOK/DEFONEOS) ---------- */
  window.sovereign = {
    ctx: window.getScreenContext,
    ask: function (message) { return post('/orchestrate', { message: message, context: window.getScreenContext(), citizen: CITIZEN }); },
    govern: function (q) { return fetch(API + '/govern?q=' + encodeURIComponent(q)).then(j); },
    validate: function (message) { return post('/bridge', { message: message }); },
    sign: function (action) { return post('/sign', { action: action }); },
    verify: function (o) { return post('/verify', o); },
    nodes: function () { return fetch(API + '/nodes').then(j); }
  };
  function j(r) { return r.json(); }
  function post(p, b) { return fetch(API + p, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(b) }).then(j); }

  /* ---------- UI: orb + chat + optional sidebar ---------- */
  var css = document.createElement('style'); css.textContent =
    '.sv-orb{position:fixed;right:18px;bottom:18px;z-index:2147483000;width:56px;height:56px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:26px;background:radial-gradient(circle at 50% 38%,#1a2440,#0a1530);box-shadow:0 8px 24px rgba(0,0,0,.32);border:2px solid ' + ACCENT + '}' +
    '.sv-panel{position:fixed;right:18px;bottom:84px;z-index:2147483000;width:min(380px,92vw);max-height:70vh;display:none;flex-direction:column;background:#fffdf8;border:1px solid ' + ACCENT + ';border-radius:16px;box-shadow:0 18px 50px rgba(0,0,0,.3);overflow:hidden;font-family:-apple-system,system-ui,sans-serif}' +
    '.sv-panel.on{display:flex}.sv-head{display:flex;align-items:center;gap:9px;padding:12px 14px;background:linear-gradient(135deg,#1a1410,#3a2e1a);color:' + ACCENT + '}' +
    '.sv-head b{color:#fff}.sv-head .x{margin-left:auto;cursor:pointer;color:#caa}' +
    '.sv-log{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:8px;font-size:14px;color:#2a1a14}' +
    '.sv-msg{padding:8px 11px;border-radius:11px;max-width:88%;line-height:1.45}.sv-msg.ai{background:#f4efe2;align-self:flex-start}.sv-msg.me{background:' + ACCENT + ';color:#1a1410;align-self:flex-end}' +
    '.sv-bar{display:flex;gap:6px;padding:10px;border-top:1px solid #eadfc6}.sv-bar input{flex:1;border:1px solid #eadfc6;border-radius:999px;padding:8px 13px;font:14px inherit;outline:none}' +
    '.sv-bar button{border:0;background:' + ACCENT + ';color:#1a1410;width:36px;border-radius:50%;font-weight:800;cursor:pointer}' +
    '.sv-foot{font-size:10.5px;color:#8a7350;text-align:center;padding:0 0 8px}' +
    '.sv-ham{position:fixed;left:14px;top:14px;z-index:2147483000;width:36px;height:34px;border-radius:9px;border:1px solid ' + ACCENT + ';background:#fffdf8;cursor:pointer;font-size:17px;display:flex;align-items:center;justify-content:center}' +
    '.sv-nav{position:fixed;top:0;left:0;bottom:0;z-index:2147483001;width:270px;max-width:84vw;background:#fffdf8;border-right:1px solid ' + ACCENT + ';box-shadow:14px 0 40px rgba(0,0,0,.18);transform:translateX(-104%);transition:transform .3s;overflow-y:auto;padding:16px 0;font-family:-apple-system,system-ui,sans-serif}' +
    '.sv-nav.on{transform:none}.sv-nav h4{margin:0;padding:14px 18px 6px;font-size:11px;letter-spacing:.06em;color:#8a7350;font-weight:800}' +
    '.sv-nav a{display:flex;gap:10px;padding:10px 18px;color:#2a1a14;text-decoration:none;font-weight:600;font-size:14px;cursor:pointer}.sv-nav a:hover{background:rgba(201,168,76,.12)}' +
    '.sv-scrim{position:fixed;inset:0;z-index:2147483000;background:rgba(20,14,10,.3);display:none}.sv-scrim.on{display:block}';
  document.head.appendChild(css);

  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; }
  var orb = el('div', 'sv-orb', CFG.face || '🐉'); orb.title = 'Ask ' + BRAND + ' Sovereign';
  var panel = el('div', 'sv-panel');
  panel.appendChild(el('div', 'sv-head', '<span>' + (CFG.face || '🐉') + '</span><b>' + esc(BRAND) + ' Sovereign</b><span class="x">✕</span>'));
  var log = el('div', 'sv-log'); panel.appendChild(log);
  var bar = el('div', 'sv-bar', '<input placeholder="Ask anything — I run this site"><button>➤</button>'); panel.appendChild(bar);
  panel.appendChild(el('div', 'sv-foot', 'governed &amp; Ed25519-signed by ' + esc(BRAND) + ' · SOV3'));
  document.body.appendChild(orb); document.body.appendChild(panel);

  function say(who, html) { var m = el('div', 'sv-msg ' + who, html); log.appendChild(m); log.scrollTop = log.scrollHeight; return m; }
  function toggle(on) { panel.classList.toggle('on', on == null ? !panel.classList.contains('on') : on); if (panel.classList.contains('on') && !log.children.length) say('ai', "I'm your <b>" + esc(BRAND) + " Sovereign</b> — I run this site, know what's on screen, and act for you. Try “what governs a bank”, “verify a badge”, or “take me to plans”."); }
  orb.onclick = function () { toggle(); };
  panel.querySelector('.x').onclick = function () { toggle(false); };
  var input = bar.querySelector('input');
  function send() { var v = (input.value || '').trim(); if (!v) return; input.value = ''; say('me', esc(v)); var t = say('ai', '…');
    window.sovereign.ask(v).then(function (d) {
      t.innerHTML = esc((d && d.say) || 'On it.');
      if (d && d.actions) d.actions.forEach(function (a) { try { var fn = window.sovereignOSCommands[a.command]; if (fn) fn(a.args || {}); } catch (e) {} });
    }).catch(function () { t.innerHTML = 'I hear you — I can explain governance, verify signatures, or navigate. (Reconnecting.)'; }); }
  bar.querySelector('button').onclick = send; input.addEventListener('keydown', function (e) { if (e.key === 'Enter') send(); });

  /* optional sidebar/menu from config.sections — so nobody rebuilds nav */
  if (Array.isArray(CFG.sections) && CFG.sections.length) {
    var ham = el('div', 'sv-ham', '☰'); ham.title = 'Menu';
    var scrim = el('div', 'sv-scrim'); var nav = el('div', 'sv-nav');
    nav.appendChild(el('h4', null, esc(BRAND) + ' · Sovereign OS'));
    CFG.sections.forEach(function (s) { var a = el('a', null, (s.icon ? s.icon + ' ' : '') + esc(s.label || '')); a.onclick = function () { if (s.href) location.href = s.href; else if (s.action && window.sovereignOSCommands[s.action]) window.sovereignOSCommands[s.action]({}); nav.classList.remove('on'); scrim.classList.remove('on'); }; nav.appendChild(a); });
    nav.appendChild(el('a', null, '🐉 Ask the Sovereign')).onclick = function () { nav.classList.remove('on'); scrim.classList.remove('on'); toggle(true); };
    document.body.appendChild(ham); document.body.appendChild(scrim); document.body.appendChild(nav);
    ham.onclick = function () { nav.classList.add('on'); scrim.classList.add('on'); };
    scrim.onclick = function () { nav.classList.remove('on'); scrim.classList.remove('on'); };
  }
})();
