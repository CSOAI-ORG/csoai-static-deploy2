// MEOK Sovereign — overlay content script. The Sovereign rides on ANY site, as a
// small circle with your AI character in it. Tap to talk (voice) or open to type.
// Talks only to your own governed brain (os.meok.ai). No data leaves to anyone else.
(function () {
  if (window.__meokSov) return; window.__meokSov = true;
  const API = "https://os.meok.ai";
  const GOLD = "#c9a84c";
  let voiceOn = false, listening = false;

  // ── the character circle (minimised state) ──
  const orb = document.createElement("div");
  orb.id = "meok-orb"; orb.title = "MEOK Sovereign — tap to talk, double-tap to open";
  orb.style.cssText = `position:fixed;bottom:22px;right:22px;z-index:2147483647;width:58px;height:58px;border-radius:50%;
    overflow:hidden;cursor:pointer;background:radial-gradient(circle at 40% 32%,#fff7d6,#e9d9a6);
    box-shadow:0 6px 24px rgba(0,0,0,.38),0 0 0 2px ${GOLD}, 0 0 22px ${GOLD}66;transition:transform .2s,box-shadow .3s;user-select:none`;
  const face = document.createElement("img");
  face.src = API + "/api/avatar?queen_id=queen-care&size=120";
  face.style.cssText = "width:100%;height:100%;object-fit:cover;object-position:center 30%;pointer-events:none";
  face.onerror = () => { orb.textContent = "🐉"; orb.style.display = "flex"; orb.style.alignItems = "center"; orb.style.justifyContent = "center"; orb.style.fontSize = "28px"; orb.style.color = GOLD; orb.style.background = "radial-gradient(circle at 38% 32%,#2a2218,#0e0c08)"; };
  orb.appendChild(face);
  orb.onmouseenter = () => orb.style.transform = "scale(1.08)";
  orb.onmouseleave = () => orb.style.transform = "scale(1)";

  // ── the panel (expanded state) ──
  const panel = document.createElement("div");
  panel.id = "meok-panel";
  panel.style.cssText = `position:fixed;bottom:90px;right:22px;z-index:2147483647;width:340px;max-width:92vw;height:470px;max-height:74vh;
    display:none;flex-direction:column;background:#FFFCF5;color:#2a1a14;border:1px solid ${GOLD};border-radius:18px;overflow:hidden;
    box-shadow:0 22px 64px rgba(0,0,0,.42);font-family:-apple-system,Segoe UI,Roboto,sans-serif`;
  panel.innerHTML = `
    <div style="background:linear-gradient(135deg,#1a1410,#3a2e1a);color:${GOLD};padding:12px 14px;display:flex;align-items:center;gap:9px;font-weight:800">
      <span style="font-size:18px">🜂</span> Sovereign
      <span style="margin-left:auto;font-weight:500;font-size:11px;opacity:.7">on this page</span>
      <span id="meok-min" title="Minimise to character" style="cursor:pointer;font-size:16px;opacity:.85">—</span>
    </div>
    <div id="meok-log" style="flex:1;overflow:auto;padding:14px;display:flex;flex-direction:column;gap:9px;font-size:13.5px;line-height:1.5"></div>
    <div style="display:flex;gap:8px;padding:12px;border-top:1px solid #eee2c8;align-items:center">
      <span id="meok-mic" title="Speak" style="cursor:pointer;font-size:18px;width:36px;height:36px;display:flex;align-items:center;justify-content:center;border-radius:50%;border:1px solid #e0d4b0">🎤</span>
      <input id="meok-in" placeholder="Speak or type…" style="flex:1;border:1px solid #e0d4b0;border-radius:10px;padding:9px 12px;font-size:13.5px;outline:none">
      <button id="meok-send" style="border:none;background:${GOLD};color:#1a1410;font-weight:800;border-radius:10px;padding:0 13px;cursor:pointer">➤</button>
    </div>`;

  document.documentElement.append(orb, panel);
  const log = panel.querySelector("#meok-log"), input = panel.querySelector("#meok-in"), micBtn = panel.querySelector("#meok-mic");

  function say(who, html) {
    const m = document.createElement("div");
    m.style.cssText = who === "me"
      ? "align-self:flex-end;background:#1a1410;color:#f5f0e6;padding:8px 12px;border-radius:13px 13px 3px 13px;max-width:85%"
      : "align-self:flex-start;background:#f3ecda;padding:8px 12px;border-radius:13px 13px 13px 3px;max-width:90%";
    m.innerHTML = html; log.appendChild(m); log.scrollTop = log.scrollHeight; return m;
  }
  function pulse(on) { orb.style.boxShadow = on ? `0 6px 24px rgba(0,0,0,.38),0 0 0 3px ${GOLD},0 0 34px ${GOLD}` : `0 6px 24px rgba(0,0,0,.38),0 0 0 2px ${GOLD},0 0 22px ${GOLD}66`; }
  function speak(t) { try { if (!voiceOn || !window.speechSynthesis) return; const txt = String(t).replace(/<[^>]+>/g, " ").trim(); if (!txt) return; const u = new SpeechSynthesisUtterance(txt); u.rate = 1.02; const v = speechSynthesis.getVoices().find(x => /en-GB/i.test(x.lang)) || speechSynthesis.getVoices().find(x => /^en/i.test(x.lang)); if (v) u.voice = v; pulse(true); u.onend = () => pulse(false); speechSynthesis.cancel(); speechSynthesis.speak(u); } catch (e) {} }

  function openPanel(show) { panel.style.display = (show ?? panel.style.display === "none") ? "flex" : "none"; if (panel.style.display === "flex" && !log.childElementCount) { say("ai", "I'm your Sovereign — here on <b>" + location.hostname + "</b>. Speak or type; I'll find the right tool. Your data stays yours."); input.focus(); } }
  // single tap = talk; double tap = open the panel
  let tapT = 0;
  orb.onclick = () => { const now = Date.now(); if (now - tapT < 300) { openPanel(true); tapT = 0; } else { tapT = now; setTimeout(() => { if (tapT) { startVoice(); tapT = 0; } }, 310); } };
  panel.querySelector("#meok-min").onclick = () => openPanel(false);

  async function send(v) {
    v = (v || input.value).trim(); if (!v) return; input.value = "";
    if (panel.style.display !== "flex") openPanel(true);
    say("me", v.replace(/[<>&]/g, c => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c])));
    const t = say("ai", "…");
    try {
      const r = await fetch(API + "/api/chat", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: v, queen_id: "queen-king", arcana_lens: 21, persona: "The user is on " + location.hostname + ". Help in context." }) });
      const d = await r.json(); const ans = d.response || "…"; t.innerHTML = ans.replace(/</g, "&lt;"); speak(ans);
      const tr = await (await fetch(API + "/api/tools?q=" + encodeURIComponent(v) + "&limit=3")).json();
      if (tr.matches && tr.matches.length) { const box = say("ai", "🧰 <b>Tools for this:</b><br>"); box.innerHTML += tr.matches.map(m => `<a href="${API}/sovspace.html?q=${encodeURIComponent(m.name)}" target="_blank" style="display:inline-block;margin:4px 4px 0 0;padding:2px 9px;border:1px solid ${GOLD};border-radius:999px;color:#8a6f2e;text-decoration:none;font-size:12px">${m.name}</a>`).join(""); }
    } catch (e) { t.innerHTML = "I'm here — try once more."; }
  }
  panel.querySelector("#meok-send").onclick = () => send();
  input.addEventListener("keydown", e => { if (e.key === "Enter") send(); });

  // ── voice in (Web Speech) ──
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  function startVoice() {
    voiceOn = true;
    if (!SR) { openPanel(true); say("ai", "Your browser doesn't support voice input here — type to me instead."); return; }
    if (listening) return; const rec = new SR(); rec.lang = "en-GB"; rec.interimResults = false; rec.maxAlternatives = 1;
    listening = true; pulse(true); openPanel(true); say("ai", "<i>listening…</i>");
    rec.onresult = e => { const txt = e.results[0][0].transcript; const last = log.lastChild; if (last && /listening/.test(last.textContent)) last.remove(); send(txt); };
    rec.onend = () => { listening = false; pulse(false); };
    rec.onerror = () => { listening = false; pulse(false); };
    rec.start();
  }
  micBtn.onclick = startVoice;
})();
