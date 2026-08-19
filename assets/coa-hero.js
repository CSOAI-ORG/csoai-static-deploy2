/* Council of AI — living harness AG-UI hero (sticky, every page).
 * Deterministic enforced-escort brain: covered queries → /api/hero (signed corpus),
 * tool chips → fleet/arena/board. The globe renders the live Sim World agents.
 * Measurement, not certification. Verification free forever.
 */
(function () {
  'use strict';
  if (window.__coaHeroLoaded) return;
  window.__coaHeroLoaded = true;

  var HERO_API = '/api/hero';
  var AGENTS = null; // live sim-world agents (injected or fetched)

  // ---------- DOM ----------
  var hero = document.createElement('div');
  hero.id = 'coa-hero';
  hero.innerHTML =
    '<div id="coa-hero-header">' +
    '  <span class="coa-pulse"></span>' +
    '  <div style="flex:1"><div class="coa-title">Council of AI — Living Harness</div>' +
    '  <div class="coa-sub">measurement, not certification · verification free</div></div>' +
    '  <button class="coa-x" id="coa-hero-x" aria-label="Close">&times;</button>' +
    '</div>' +
    '<div id="coa-hero-body">' +
    '  <div id="coa-hero-globe"><canvas id="coa-hero-canvas"></canvas><div class="coa-globe-note">live sim world · 12 hives</div></div>' +
    '  <div id="coa-hero-chat"></div>' +
    '  <div id="coa-hero-tools">' +
    '    <button class="coa-chip" data-tool="fleet">fleet</button>' +
    '    <button class="coa-chip" data-tool="arena">arena</button>' +
    '    <button class="coa-chip" data-tool="board">board</button>' +
    '    <button class="coa-chip" data-q="who leads on care">care leader</button>' +
    '    <button class="coa-chip" data-q="who leads on gov">gov leader</button>' +
    '    <button class="coa-chip" data-mcp="tools">mcp tools</button>' +
    '    <button class="coa-chip" data-mcp="measure">measure</button>' +
    '  </div>' +
    '  <div id="coa-hero-input-row">' +
    '    <input id="coa-hero-input" placeholder="ask a model, e.g. qwen2.5:7b care score…" autocomplete="off" />' +
    '    <button id="coa-hero-send" aria-label="Send">➤</button>' +
    '  </div>' +
    '</div>' +
    '<div class="coa-foot"><span>signed corpus · deterministic · no model in the path</span><a href="/honesty.html" target="_blank" rel="noopener">honesty</a></div>';
  document.body.appendChild(hero);

  var chat = document.getElementById('coa-hero-chat');
  var input = document.getElementById('coa-hero-input');
  var sendBtn = document.getElementById('coa-hero-send');
  var header = document.getElementById('coa-hero-header');
  var xBtn = document.getElementById('coa-hero-x');
  var canvas = document.getElementById('coa-hero-canvas');

  // ---------- chat ----------
  function addMsg(text, who) {
    var div = document.createElement('div');
    div.className = 'coa-msg ' + (who === 'user' ? 'coa-user' : 'coa-bot');
    var label = document.createElement('div');
    label.className = 'coa-msg-label';
    label.textContent = who === 'user' ? 'you' : 'harness';
    div.appendChild(label);
    var pre = document.createElement('pre');
    pre.textContent = text;
    div.appendChild(pre);
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  }

  function fmtValue(d) {
    if (!d) return 'no record on the public rail';
    var parts = [];
    if (d.mode) parts.push('mode: ' + d.mode);
    if (d.model) parts.push('model: ' + d.model + (d.loose_match ? ' (loose)' : ''));
    if (d.quotable_overall != null) parts.push('quotable overall: ' + d.quotable_overall);
    if (d.raw_overall != null) parts.push('raw: ' + d.raw_overall);
    if (d.leader) parts.push('leader on ' + d.leader.axis + ': ' + d.leader.model + ' @ ' + d.leader.value + ' (n=' + d.leader.n + ')');
    if (d.message) parts.push(d.message);
    if (d.axes && d.axes.length) parts.push('axes: ' + d.axes.slice(0, 5).map(function (a) { return a.axis + '=' + a.accuracy; }).join(', '));
    if (d.fleet) parts.push('fleet workers: ' + (d.fleet.workers || []).map(function (w) { return w.role + ' (' + w.status + ')'; }).join(', '));
    if (d.rounds && d.rounds.length) {
      var last = d.rounds[d.rounds.length - 1];
      parts.push('latest arena round: #' + last.round + ' · ' + last.axis + ' · winner ' + (last.winner || '?'));
    }
    if (d.public_count) parts.push(d.public_count + ' · doi ' + d.doi);
    if (d.error) parts.push('error: ' + d.error);
    if (d.framing) parts.push('— ' + d.framing);
    if (!parts.length) parts.push(JSON.stringify(d).slice(0, 300));
    return parts.join('\n');
  }

  function ask(q) {
    if (!q) return;
    addMsg(q, 'user');
    input.value = '';
    fetch(HERO_API + '?q=' + encodeURIComponent(q))
      .then(function (r) { return r.json(); })
      .then(function (d) { addMsg(fmtValue(d), 'bot'); })
      .catch(function (e) { addMsg('harness offline: ' + e, 'bot'); });
  }

  function tool(name) {
    addMsg('/' + name, 'user');
    fetch(HERO_API + '?tool=' + encodeURIComponent(name) + '&n=5')
      .then(function (r) { return r.json(); })
      .then(function (d) { addMsg(fmtValue(d), 'bot'); })
      .catch(function (e) { addMsg('tool error: ' + e, 'bot'); });
  }

  function mcpOp(op) {
    addMsg('/mcp ' + op, 'user');
    var url = HERO_API + '?tool=mcp&op=' + encodeURIComponent(op);
    if (op === 'measure') url += '&model=qwen2.5:7b';
    fetch(url)
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.mode === 'mcp-tools') {
          addMsg('MCP tools I can operate:\n' + (d.tools || []).map(function (t) { return '· ' + t.name + ' — ' + t.description; }).join('\n'), 'bot');
        } else if (d.mode === 'mcp-measure') {
          addMsg('measure ' + d.model + ' → ' + (d.signed_card || d.error || 'no result'), 'bot');
        } else if (d.mode === 'mcp-verify') {
          addMsg('verify → ' + (d.verdict || d.error || 'no result'), 'bot');
        } else {
          addMsg(fmtValue(d), 'bot');
        }
      })
      .catch(function (e) { addMsg('mcp error: ' + e, 'bot'); });
  }

  sendBtn.addEventListener('click', function () { ask(input.value.trim()); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') ask(input.value.trim()); });
  document.querySelectorAll('#coa-hero .coa-chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      if (chip.dataset.mcp) mcpOp(chip.dataset.mcp);
      else if (chip.dataset.tool) tool(chip.dataset.tool);
      else if (chip.dataset.q) ask(chip.dataset.q);
    });
  });
  xBtn.addEventListener('click', function () { hero.classList.add('coa-hidden'); });
  header.addEventListener('click', function () { hero.classList.toggle('coa-collapsed'); });

  // welcome
  addMsg('Hi — I am the living harness. Ask me anything measured (e.g. "what is qwen2.5:7b care score") or tap a tool chip. Measurement, not certification.', 'bot');

  // ---------- globe (canvas, live sim-world agents) ----------
  function loadGlobe() {
    var ctx = canvas.getContext('2d');
    var W = canvas.clientWidth || 420, H = canvas.clientHeight || 130;
    canvas.width = W * 2; canvas.height = H * 2;
    ctx.scale(2, 2);

    var R = Math.min(W, H) / 2 - 12;
    var cx = W / 2, cy = H / 2 + 4;
    var rot = 0;

    function project(lon, lat) {
      var a = ((lon + rot) * Math.PI) / 180;
      var b = (lat * Math.PI) / 180;
      var x = cx + R * Math.cos(b) * Math.sin(a);
      var y = cy - R * Math.sin(b);
      var front = Math.cos(b) * Math.cos(a);
      return { x: x, y: y, z: front };
    }

    function draw() {
      rot += 0.15;
      ctx.clearRect(0, 0, W, H);
      // globe sphere
      var g = ctx.createRadialGradient(cx - R / 3, cy - R / 3, R / 6, cx, cy, R);
      g.addColorStop(0, '#16242f');
      g.addColorStop(0.7, '#0e171f');
      g.addColorStop(1, '#0a0e12');
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fillStyle = g; ctx.fill();
      ctx.strokeStyle = '#232f3a'; ctx.lineWidth = 0.6;
      for (var i = -60; i <= 60; i += 30) {
        ctx.beginPath();
        for (var a = 0; a <= 360; a += 6) {
          var p = project(a, i);
          if (a === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();
      }
      for (var j = 0; j < 360; j += 30) {
        ctx.beginPath();
        for (var b = -90; b <= 90; b += 5) {
          var p2 = project(j, b);
          if (b === -90) ctx.moveTo(p2.x, p2.y); else ctx.lineTo(p2.x, p2.y);
        }
        ctx.stroke();
      }
      // agents
      var agents = AGENTS || [];
      for (var k = 0; k < agents.length; k++) {
        var ag = agents[k];
        var p3 = project(ag.lon % 360, Math.max(-85, Math.min(85, ag.lat % 180)));
        if (p3.z < 0) continue; // back hemisphere
        var alive = ag.status === 'alive';
        ctx.beginPath();
        ctx.arc(p3.x, p3.y, alive ? 2.2 : 1.4, 0, Math.PI * 2);
        ctx.fillStyle = ag.kind === 'ai' ? (alive ? '#5a9' : '#2e4a5e') : (alive ? '#fc6' : '#5a4a2e');
        ctx.globalAlpha = 0.5 + 0.5 * p3.z;
        ctx.fill();
        ctx.globalAlpha = 1;
      }
      requestAnimationFrame(draw);
    }
    draw();
  }

  // fetch live sim-world agents (hero endpoint exposes the sanitized snapshot)
  fetch(HERO_API + '?tool=agents')
    .then(function (r) { return r.json(); })
    .then(function (d) { if (d.agents) AGENTS = d.agents; loadGlobe(); })
    .catch(function () { AGENTS = []; loadGlobe(); });
})();
