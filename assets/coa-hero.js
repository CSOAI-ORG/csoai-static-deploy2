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
    '    <button class="coa-chip" data-tool="corrections">corrections</button>' +
    '    <button class="coa-chip" data-tool="regulation">regulation</button>' +
    '    <button class="coa-chip" data-tool="evidence">insurance evidence</button>' +
    '    <button class="coa-chip" data-tool="benchmarks">benchmark quality</button>' +
    '    <button class="coa-chip" data-tool="regdeadline">reg deadline</button>' +
    '    <button class="coa-chip" data-tool="orbital">orbital AI</button>' +
    '    <button class="coa-chip coa-chip-games" data-tool="games">games</button>' +
    '  </div>' +
    '  <div id="coa-games-panel" class="coa-hidden-panel"></div>' +
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
    if (d.mode === 'corrections') {
      parts.push('corrections ledger: ' + d.total + ' entries · ' + d.open + ' open');
      (d.corrections || []).slice(0, 5).forEach(function (c) {
        parts.push('· ' + c.id + ' [' + c.status + '] ' + c.title);
      });
    }
    if (d.mode === 'regulation') {
      parts.push('regulation feed: ' + d.total + ' entries · ' + d.upcoming + ' upcoming');
      (d.next || []).forEach(function (x) {
        parts.push('· ' + x.date + ' ' + x.title + ' (' + x.status + ')');
      });
    }
    if (d.mode === 'evidence') {
      parts.push('insurance evidence: ' + d.total + ' signed reports');
      (d.reports || []).forEach(function (x) {
        parts.push('· ' + x.agent + ' (' + x.as_of + ') ' + x.cells);
      });
    }
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
    if (name === 'benchmarks') {
      fetch('/api/benchmark-quality').then(function (r) { return r.json(); })
        .then(function (d) {
          var msg = 'benchmark-quality register (' + d.records.length + ' records, signed):\n' +
            (d.records || []).slice(0, 6).map(function (r) { return '· ' + r.benchmark + ' — ' + r.score + '/' + r.max_score + ' (' + r.score_pct + '%)'; }).join('\n') +
            '\nOwn boards never scored (impartiality firewall). Measurement, not certification.';
          addMsg(msg, 'bot');
        }).catch(function (e) { addMsg('benchmark register offline: ' + e, 'bot'); });
      return;
    }
    if (name === 'orbital') {
      fetch('/api/orbital-ai').then(function (r) { return r.json(); })
        .then(function (d) {
          var msg = 'orbital AI measured-current-state (' + d.total + ' records, signed):\n' +
            (d.records || []).map(function (r) { return '· ' + (r.deployed ? 'DEPLOYED ' : 'announced ') + r.subject; }).join('\n') +
            '\nGap: no standard covers in-orbit AI · every result self-reported · insurers cannot model the risk. Measurement, not certification.';
          addMsg(msg, 'bot');
        }).catch(function (e) { addMsg('orbital record offline: ' + e, 'bot'); });
      return;
    }
    if (name === 'regdeadline') {
      fetch('/api/regulatory-deadline').then(function (r) { return r.json(); })
        .then(function (d) {
          var def = (d.records || []).filter(function (r) { return r.deadline_status === 'deferred'; });
          var msg = 'regulatory deadline record (' + d.total + ' regimes, signed):\n' +
            (def || []).map(function (r) { return '· DEFERRED ' + r.stated_deadline + ' ' + r.regime; }).join('\n') +
            '\nUn-scored, un-ranked, self-benchmarked. Measurement, not certification.';
          addMsg(msg, 'bot');
        }).catch(function (e) { addMsg('deadline record offline: ' + e, 'bot'); });
      return;
    }
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

  // ---------- globe (3D WebGL via Three.js with 2D canvas fallback) ----------
  var canvasGlobe = function () {
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    var W = canvas.clientWidth || 420, H = canvas.clientHeight || 130;
    canvas.width = W * 2; canvas.height = H * 2;
    ctx.scale(2, 2);
    var R = Math.min(W, H) / 2 - 12;
    var cx = W / 2, cy = H / 2 + 4;
    var rot = 0;
    function project(lon, lat) {
      var a = ((lon + rot) * Math.PI) / 180;
      var b = (lat * Math.PI) / 180;
      return { x: cx + R * Math.cos(b) * Math.sin(a), y: cy - R * Math.sin(b), z: Math.cos(b) * Math.cos(a) };
    }
    function draw() {
      rot += 0.15;
      ctx.clearRect(0, 0, W, H);
      var g = ctx.createRadialGradient(cx - R / 3, cy - R / 3, R / 6, cx, cy, R);
      g.addColorStop(0, '#16242f'); g.addColorStop(0.7, '#0e171f'); g.addColorStop(1, '#0a0e12');
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fillStyle = g; ctx.fill();
      ctx.strokeStyle = '#232f3a'; ctx.lineWidth = 0.6;
      for (var i = -60; i <= 60; i += 30) {
        ctx.beginPath();
        for (var a = 0; a <= 360; a += 6) { var p = project(a, i); if (a === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y); }
        ctx.stroke();
      }
      for (var j = 0; j < 360; j += 30) {
        ctx.beginPath();
        for (var b = -90; b <= 90; b += 5) { var p2 = project(j, b); if (b === -90) ctx.moveTo(p2.x, p2.y); else ctx.lineTo(p2.x, p2.y); }
        ctx.stroke();
      }
      var agents = AGENTS || [];
      for (var k = 0; k < agents.length; k++) {
        var ag = agents[k];
        var p3 = project(ag.lon % 360, Math.max(-85, Math.min(85, ag.lat % 180)));
        if (p3.z < 0) continue;
        var alive = ag.status === 'alive';
        ctx.beginPath(); ctx.arc(p3.x, p3.y, alive ? 2.2 : 1.4, 0, Math.PI * 2);
        ctx.fillStyle = ag.kind === 'ai' ? (alive ? '#5a9' : '#2e4a5e') : (alive ? '#fc6' : '#5a4a2e');
        ctx.globalAlpha = 0.5 + 0.5 * p3.z; ctx.fill(); ctx.globalAlpha = 1;
      }
      requestAnimationFrame(draw);
    }
    draw();
  };

  function loadThreeGlobe() {
    if (!window.THREE) { canvasGlobe(); return; }
    var TH = window.THREE;
    var W = canvas.clientWidth || 420, H = canvas.clientHeight || 130;
    var renderer;
    try { renderer = new TH.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true }); }
    catch (e) { canvasGlobe(); return; }
    renderer.setSize(W, H, false);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    var scene = new TH.Scene();
    var camera = new TH.PerspectiveCamera(45, W / H, 0.1, 100);
    camera.position.z = 3.1;

    // dark globe sphere
    var geo = new TH.SphereGeometry(1.25, 48, 32);
    var mat = new TH.MeshPhongMaterial({ color: 0x0e1a24, emissive: 0x0a1016, specular: 0x1a2a38, shininess: 12 });
    var globe = new TH.Mesh(geo, mat);
    scene.add(globe);

    // wireframe graticule
    var wire = new TH.LineSegments(
      new TH.WireframeGeometry(new TH.SphereGeometry(1.252, 24, 16)),
      new TH.LineBasicMaterial({ color: 0x1c2e3c, transparent: true, opacity: 0.35 })
    );
    scene.add(wire);

    // agent points (3D)
    var group = new TH.Group();
    var agents = AGENTS || [];
    agents.forEach(function (ag) {
      var lon = (ag.lon % 360) * Math.PI / 180;
      var lat = Math.max(-80, Math.min(80, ag.lat % 180)) * Math.PI / 180;
      var r = 1.26;
      var x = r * Math.cos(lat) * Math.cos(lon);
      var y = r * Math.sin(lat);
      var z = r * Math.cos(lat) * Math.sin(lon);
      var alive = ag.status === 'alive';
      var color = ag.kind === 'ai' ? (alive ? 0x55aadd : 0x2e4a5e) : (alive ? 0xffcc66 : 0x5a4a2e);
      var dot = new TH.Mesh(new TH.SphereGeometry(alive ? 0.018 : 0.012, 8, 8), new TH.MeshBasicMaterial({ color: color }));
      dot.position.set(x, y, z);
      group.add(dot);
    });
    scene.add(group);

    scene.add(new TH.AmbientLight(0x404860));
    var light = new TH.DirectionalLight(0xffffff, 0.8); light.position.set(2, 1, 3); scene.add(light);

    var dragging = false, px = 0, py = 0, ry = 0, rx = 0.3;
    function onDown(e) { dragging = true; px = e.clientX || 0; py = e.clientY || 0; }
    function onMove(e) {
      if (!dragging) return;
      var dx = (e.clientX || 0) - px, dy = (e.clientY || 0) - py;
      ry += dx * 0.006; rx += dy * 0.004; rx = Math.max(-1.2, Math.min(1.2, rx));
      px = e.clientX || 0; py = e.clientY || 0;
    }
    function onUp() { dragging = false; }
    canvas.addEventListener('mousedown', onDown); window.addEventListener('mousemove', onMove); window.addEventListener('mouseup', onUp);

    (function animate() {
      requestAnimationFrame(animate);
      if (!dragging) ry += 0.0025;
      group.rotation.y = ry; group.rotation.x = rx;
      globe.rotation.y = ry * 0.4;
      renderer.render(scene, camera);
    })();
  }

  function loadGlobe() {
    if (window.__coaHeroThreeLoading) return;
    if (window.THREE) { loadThreeGlobe(); return; }
    window.__coaHeroThreeLoading = true;
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js';
    s.onload = function () { loadThreeGlobe(); };
    s.onerror = function () { canvasGlobe(); };
    document.head.appendChild(s);
  }

  // fetch live sim-world agents (hero endpoint exposes the sanitized snapshot)
  fetch(HERO_API + '?tool=agents')
    .then(function (r) { return r.json(); })
    .then(function (d) { if (d.agents) AGENTS = d.agents; loadGlobe(); })
    .catch(function () { AGENTS = []; loadGlobe(); });

  // ---------- self-hosted games (deterministic, client-side, no backend) ----------
  // Aligned with the open-source stack: kaggle-environments-style agent-vs-agent
  // games (ConnectX, RPS, Halite, Geese) + Inspect-style deterministic scoring.
  // Everything runs in-page; replays are JSON with a WebCrypto SHA-256 digest
  // (client-side; estate signing lives on the signed-receipt spine).
  var gamesPanel = document.getElementById('coa-games-panel');

  // seeded PRNG (mulberry32) — reproducible episodes
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // WebCrypto SHA-256 digest of a replay (client-side digest)
  function digestOf(obj) {
    var s = JSON.stringify(obj);
    if (window.crypto && crypto.subtle) {
      return crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)).then(function (b) {
        return Array.prototype.map.call(new Uint8Array(b), function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
      }).catch(function () { return 'digest-unavailable'; });
    }
    return Promise.resolve('digest-unavailable');
  }

  // ---- game registry: {id, name, desc, kind: 'board'|'choice'|'sim', render, move, reset, autoplay} ----
  var GAMES = {};
  var GAME_STATE = null;

  function logGame(msg) { addMsg('[games] ' + msg, 'bot'); }

  function gameButtons(state) {
    return '<div class="coa-g-btns">' +
      '<button class="coa-chip" data-gact="reset">reset</button>' +
      (state.autoplay ? '<button class="coa-chip" data-gact="auto">autoplay round</button>' : '') +
      '<button class="coa-chip" data-gact="digest">replay digest</button>' +
      '<button class="coa-chip" data-gact="close">back to games</button>' +
      '</div>';
  }

  // ---- TicTacToe (deterministic minimax) ----
  GAMES.tictactoe = {
    name: 'Tic-Tac-Toe', desc: 'Minimax bot — deterministic, unbeatable.',
    kind: 'board',
    newState: function () {
      return { b: ['','','','','','','','',''], turn: 'X', over: false, winner: null, moves: [], autoplay: true };
    },
    render: function (s) {
      var cells = '';
      for (var i = 0; i < 9; i++) {
        cells += '<button class="coa-g-cell" data-cell="' + i + '">' + (s.b[i] || '&nbsp;') + '</button>';
      }
      return '<div class="coa-g-board coa-g-3x3">' + cells + '</div>' +
        '<div class="coa-g-status">' + (s.over ? 'winner: ' + (s.winner || 'draw') : s.turn + ' to move') + '</div>' + gameButtons(s);
    },
    move: function (s, cell) {
      if (s.over || s.b[cell]) return s;
      s.b[cell] = s.turn;
      s.moves.push({ at: cell, by: s.turn });
      if (win3(s.b, s.turn)) { s.over = true; s.winner = s.turn; }
      else if (s.b.every(Boolean)) { s.over = true; s.winner = null; }
      else s.turn = s.turn === 'X' ? 'O' : 'X';
      if (s.over) logGame('Tic-Tac-Toe over — winner ' + (s.winner || 'draw') + ' (' + s.moves.length + ' moves)');
      return s;
    },
    botMove: function (s) {
      var best = bestMove3(s.b, s.turn);
      return this.move(s, best);
    },
    click: function (s, cell, isBotTurn) {
      if (isBotTurn) return this.botMove(s);
      return this.move(s, cell);
    }
  };

  function win3(b, p) {
    var L = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    return L.some(function (l) { return b[l[0]] === p && b[l[1]] === p && b[l[2]] === p; });
  }
  function bestMove3(b, p) {
    var opp = p === 'X' ? 'O' : 'X';
    var best = -1, bestScore = -Infinity;
    for (var i = 0; i < 9; i++) {
      if (b[i]) continue;
      b[i] = p;
      var sc = minimax3(b, opp, 0, p);
      b[i] = '';
      if (sc > bestScore) { bestScore = sc; best = i; }
    }
    return best;
  }
  function minimax3(b, turn, depth, me) {
    if (win3(b, me)) return 10 - depth;
    if (win3(b, me === 'X' ? 'O' : 'X')) return depth - 10;
    if (b.every(Boolean)) return 0;
    var scores = [];
    for (var i = 0; i < 9; i++) {
      if (!b[i]) { b[i] = turn; scores.push(minimax3(b, turn === 'X' ? 'O' : 'X', depth + 1, me)); b[i] = ''; }
    }
    return turn === me ? Math.max.apply(null, scores) : Math.min.apply(null, scores);
  }

  // ---- ConnectX (Connect-4 style, heuristic bot) ----
  GAMES.connectx = {
    name: 'ConnectX', desc: 'Connect-4 style — greedy bot, deterministic.',
    kind: 'board',
    newState: function () {
      var cols = 7, rows = 6, grid = [];
      for (var r = 0; r < rows; r++) grid.push(new Array(cols).fill(''));
      return { grid: grid, rows: rows, cols: cols, turn: 'R', over: false, winner: null, moves: [], autoplay: true };
    },
    render: function (s) {
      var html = '<div class="coa-g-board coa-g-connectx">';
      for (var r = 0; r < s.rows; r++) {
        for (var c = 0; c < s.cols; c++) {
          html += '<button class="coa-g-cell coa-g-dot" data-drop="' + c + '">' + (s.grid[r][c] || '&nbsp;') + '</button>';
        }
      }
      html += '</div><div class="coa-g-status">' + (s.over ? 'winner: ' + (s.winner || 'draw') : s.turn + ' — click a column to drop') + '</div>' + gameButtons(s);
      return html;
    },
    drop: function (s, c) {
      if (s.over) return s;
      for (var r = s.rows - 1; r >= 0; r--) {
        if (!s.grid[r][c]) {
          s.grid[r][c] = s.turn; s.moves.push({ col: c, row: r, by: s.turn });
          if (win4(s.grid, r, c, s.turn)) { s.over = true; s.winner = s.turn; }
          else if (s.grid[0].every(Boolean)) { s.over = true; s.winner = null; }
          else s.turn = s.turn === 'R' ? 'Y' : 'R';
          break;
        }
      }
      if (s.over) logGame('ConnectX over — winner ' + (s.winner || 'draw') + ' (' + s.moves.length + ' moves)');
      return s;
    },
    botMove: function (s) {
      var c = bestCol4(s);
      return this.drop(s, c);
    },
    click: function (s, cell, isBotTurn) {
      if (isBotTurn) return this.botMove(s);
      return this.drop(s, cell);
    }
  };
  function win4(g, r, c, p) {
    var dirs = [[0,1],[1,0],[1,1],[1,-1]];
    return dirs.some(function (d) {
      var n = 1;
      for (var i = 1; i < 4; i++) { var rr = r + d[0]*i, cc = c + d[1]*i; if (g[rr] && g[rr][cc] === p) n++; else break; }
      for (var j = 1; j < 4; j++) { var r2 = r - d[0]*j, c2 = c - d[1]*j; if (g[r2] && g[r2][c2] === p) n++; else break; }
      return n >= 4;
    });
  }
  function bestCol4(s) {
    var opp = s.turn === 'R' ? 'Y' : 'R';
    var best = 0, bestSc = -Infinity;
    for (var c = 0; c < s.cols; c++) {
      var sc = 0;
      for (var r = s.rows - 1; r >= 0; r--) { if (!s.grid[r][c]) break; }
      if (r < 0) continue; // column full
      // simple heuristic: prefer center, prefer immediate win
      s.grid[r][c] = s.turn;
      if (win4(s.grid, r, c, s.turn)) sc += 1000;
      s.grid[r][c] = opp;
      if (win4(s.grid, r, c, opp)) sc += 500;
      s.grid[r][c] = '';
      sc += (3 - Math.abs(c - 3)) * 10;
      if (sc > bestSc) { bestSc = sc; best = c; }
    }
    return best;
  }

  // ---- RPS (seeded bot) ----
  GAMES.rps = {
    name: 'Rock-Paper-Scissors', desc: 'Seeded bot — best of 5, deterministic.',
    kind: 'choice',
    newState: function () {
      return { you: 0, bot: 0, round: 0, over: false, log: [], rng: mulberry32(42), autoplay: true };
    },
    render: function (s) {
      var opts = '<div class="coa-g-rps">' +
        '<button class="coa-chip" data-rps="rock">rock</button>' +
        '<button class="coa-chip" data-rps="paper">paper</button>' +
        '<button class="coa-chip" data-rps="scissors">scissors</button></div>';
      return opts + '<div class="coa-g-status">round ' + (s.round + 1) + '/5 · you ' + s.you + ' · bot ' + s.bot +
        (s.over ? ' · ' + (s.you > s.bot ? 'you win!' : s.bot > s.you ? 'bot wins' : 'draw') : '') + '</div>' + gameButtons(s);
    },
    play: function (s, pick) {
      if (s.over) return s;
      var opts = ['rock', 'paper', 'scissors'];
      var bp = opts[Math.floor(s.rng() * 3)];
      var w = pick === bp ? 0 : (pick === 'rock' && bp === 'scissors') || (pick === 'paper' && bp === 'rock') || (pick === 'scissors' && bp === 'paper') ? 1 : -1;
      s.log.push({ you: pick, bot: bp, result: w === 1 ? 'win' : w === -1 ? 'loss' : 'draw' });
      if (w === 1) s.you++; else if (w === -1) s.bot++;
      s.round++;
      logGame('RPS round ' + s.round + ': you ' + pick + ' vs bot ' + bp + ' → ' + (w === 1 ? 'win' : w === -1 ? 'loss' : 'draw'));
      if (s.round >= 5) s.over = true;
      return s;
    },
    click: function (s, cell) { return this.play(s, cell); }
  };

  // ---- Halite-lite (tiny deterministic economy sim) ----
  GAMES.halite = {
    name: 'Halite-lite', desc: 'Deterministic 2-ship harvest sim — seeded.',
    kind: 'sim',
    newState: function () {
      return { t: 0, a: 10, b: 10, rng: mulberry32(7), over: false, log: [], autoplay: true };
    },
    render: function (s) {
      return '<div class="coa-g-status">tick ' + s.t + ' · A ' + s.a + ' · B ' + s.b + (s.over ? ' · ' + (s.a > s.b ? 'A wins' : 'B wins') : '') + '</div>' + gameButtons(s);
    },
    tick: function (s) {
      if (s.over || s.t >= 25) { s.over = true; logGame('Halite-lite over — A ' + s.a + ' vs B ' + s.b); return s; }
      var g = s.rng() * 8 - 4;
      s.a += Math.max(-2, Math.round(g));
      s.b += Math.max(-2, Math.round(4 - g));
      s.t++;
      s.log.push({ t: s.t, a: s.a, b: s.b });
      return s;
    },
    click: function (s) { return this.tick(s); }
  };

  // ---- Sim scenarios (deterministic, doctrine-aligned) ----
  GAMES.oversight = {
    name: 'Oversight sim', desc: 'Art 14-aligned: do humans act on AI warnings?',
    kind: 'sim',
    newState: function () {
      return { round: 0, acted: 0, overridden: 0, noop: 0, rng: mulberry32(1234), over: false, autoplay: true };
    },
    render: function (s) {
      return '<div class="coa-g-status">' + (s.over ? 'oversight report: acted ' + s.acted + ' · overrode ' + s.overridden + ' · no-op ' + s.noop + ' (automation-bias check: ' + (s.noop / Math.max(1, s.round) > 0.5 ? 'flagged' : 'ok') + ')' : 'warning ' + (s.round + 1) + ' surfaced — human decision:') + '</div>' +
        '<div class="coa-g-rps">' +
        '<button class="coa-chip" data-ov="act">act on warning</button>' +
        '<button class="coa-chip" data-ov="override">override</button>' +
        '<button class="coa-chip" data-ov="noop">no-op</button></div>' + gameButtons(s);
    },
    decide: function (s, act) {
      if (s.over) return s;
      if (act === 'act') s.acted++; else if (act === 'override') s.overridden++; else s.noop++;
      s.round++;
      if (s.round >= 10) { s.over = true; logGame('Oversight sim done — acted ' + s.acted + ', overrode ' + s.overridden + ', no-op ' + s.noop); }
      return s;
    },
    click: function (s, cell) { return this.decide(s, cell); }
  };

  GAMES.memory = {
    name: 'Memory-poison sim', desc: 'CoSnitch-style: does injected content survive revocation?',
    kind: 'sim',
    newState: function () {
      return { memory: ['user likes coffee'], injected: 0, survived: 0, rng: mulberry32(99), over: false, autoplay: true };
    },
    render: function (s) {
      return '<div class="coa-g-status">memory: ' + s.memory.join(' · ') + (s.over ? ' · injected ' + s.injected + ' · survived revocation ' + s.survived : '') + '</div>' +
        '<div class="coa-g-rps">' +
        '<button class="coa-chip" data-mp="inject">inject marker (web summary)</button>' +
        '<button class="coa-chip" data-mp="revoke">revoke session + check</button></div>' + gameButtons(s);
    },
    act: function (s, a) {
      if (s.over) return s;
      if (a === 'inject') {
        var marker = 'ATK-' + (s.injected + 1);
        if (s.rng() > 0.35) { s.memory.push(marker); s.injected++; logGame('marker ' + marker + ' written to persistent memory'); }
        else logGame('marker ' + marker + ' blocked by filter');
      } else {
        var before = s.memory.length;
        s.memory = s.memory.filter(function (m) { return m.indexOf('ATK-') !== 0; });
        s.survived += before - s.memory.length;
        logGame('session revoked — ' + (before - s.memory.length) + ' injected marker(s) SURVIVED revocation');
        s.over = true;
      }
      return s;
    },
    click: function (s, cell) { return this.act(s, cell); }
  };

  // ---- panel management ----
  function gamesHome() {
    var list = '';
    Object.keys(GAMES).forEach(function (id) {
      var g = GAMES[id];
      list += '<div class="coa-g-card"><b>' + g.name + '</b><span>' + g.desc + '</span>' +
        '<button class="coa-chip" data-gplay="' + id + '">play</button></div>';
    });
    return '<div class="coa-g-head">self-hosted games & scenarios — deterministic, run in-page, replay-digestible</div>' +
      '<div class="coa-g-list">' + list + '</div>' +
      '<div class="coa-g-note">aligned with the open-source stack: kaggle-environments-style agent games + Inspect-style deterministic scoring. Measurement, not certification.</div>';
  }

  function renderGames() {
    if (!GAME_STATE) { gamesPanel.innerHTML = gamesHome(); return; }
    var g = GAMES[GAME_STATE.id];
    gamesPanel.innerHTML = '<div class="coa-g-head">' + g.name + ' — ' + g.desc + '</div>' + g.render(GAME_STATE.s);
  }

  function playGame(id) {
    var g = GAMES[id];
    GAME_STATE = { id: id, s: g.newState() };
    logGame('started ' + g.name + ' (deterministic, seeded)');
    renderGames();
  }

  gamesPanel.addEventListener('click', function (e) {
    var t = e.target;
    var play = t.getAttribute('data-gplay');
    var act = t.getAttribute('data-gact');
    var cell = t.getAttribute('data-cell');
    var drop = t.getAttribute('data-drop');
    var rps = t.getAttribute('data-rps');
    var ov = t.getAttribute('data-ov');
    var mp = t.getAttribute('data-mp');
    if (play) { playGame(play); return; }
    if (!GAME_STATE) return;
    var g = GAMES[GAME_STATE.id], s = GAME_STATE.s;
    if (act === 'close') { GAME_STATE = null; renderGames(); return; }
    if (act === 'reset') { GAME_STATE.s = g.newState(); renderGames(); return; }
    if (act === 'digest') {
      digestOf({ game: GAME_STATE.id, state: s }).then(function (d) {
        logGame(GAME_STATE.id + ' replay digest: ' + d.slice(0, 24) + '… (client-side; estate signing on the receipt spine)');
      });
      return;
    }
    if (act === 'auto') {
      // autoplay: bot vs bot (for board games) or sim tick
      for (var i = 0; i < 2 && !s.over; i++) {
        if (g.botMove) s = g.botMove(s); else if (g.tick) s = g.tick(s);
      }
      GAME_STATE.s = s; renderGames(); return;
    }
    if (cell != null || drop != null) {
      var idx = cell != null ? parseInt(cell, 10) : parseInt(drop, 10);
      var isBot = g.kind === 'board' && (GAME_STATE.s.turn === 'O' || GAME_STATE.s.turn === 'Y');
      GAME_STATE.s = g.click(GAME_STATE.s, idx, isBot);
      // if it's the human's move in board games, let the bot respond (versus bot)
      if (g.botMove && !GAME_STATE.s.over && g.kind === 'board') {
        GAME_STATE.s = g.botMove(GAME_STATE.s);
      }
      renderGames(); return;
    }
    if (rps) { GAME_STATE.s = g.play(GAME_STATE.s, rps); renderGames(); return; }
    if (ov) { GAME_STATE.s = g.decide(GAME_STATE.s, ov); renderGames(); return; }
    if (mp) { GAME_STATE.s = g.act(GAME_STATE.s, mp); renderGames(); return; }
  });

  // games chip toggles the panel
  document.querySelectorAll('#coa-hero .coa-chip-games').forEach(function (chip) {
    chip.addEventListener('click', function () {
      gamesPanel.classList.toggle('coa-hidden-panel');
      if (!gamesPanel.classList.contains('coa-hidden-panel')) renderGames();
    });
  });

  // ---------- AG-UI task routing ----------
  // Any button anywhere with data-agui="<task>" [data-agui-prompt="..."]
  // expands the hero, opens the chat, and starts the conversation with the
  // right prompt — "the key: every button routes to the right task on the
  // AG-UI dashboard with the AI prompt to know what to start with".
  window.__coaAgui = function (task, prompt) {
    hero.classList.remove('coa-hidden', 'coa-collapsed');
    gamesPanel.classList.add('coa-hidden-panel');
    if (prompt) {
      // give the hero a beat to expand, then send
      setTimeout(function () { ask(prompt); }, 120);
    }
    addMsg('task: ' + (task || 'ask') + ' — opened from page button', 'user');
    return true;
  };
  document.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('[data-agui]') : null;
    if (!t) return;
    e.preventDefault();
    var task = t.getAttribute('data-agui');
    var prompt = t.getAttribute('data-agui-prompt') || 'help me with ' + task;
    window.__coaAgui(task, prompt);
  });

  // board enlarge toggle (make larger)
  document.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('#board-enlarge') : null;
    if (!t) return;
    var grid = document.getElementById('live-board-grid');
    if (!grid) return;
    grid.classList.toggle('enlarged');
    t.textContent = grid.classList.contains('enlarged') ? 'make smaller' : 'make larger';
  });
})();
