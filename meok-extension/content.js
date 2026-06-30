// MEOK Sovereign — overlay content script. Injects a floating Sovereign on ANY site.
// Talks to the live governed brain (os.meok.ai/api/chat) + tool router (/api/tools).
// No data leaves to anyone but your own sovereign endpoint.
(function () {
  if (window.__meokSov) return; window.__meokSov = true;
  const API = "https://os.meok.ai";
  const GOLD = "#c9a84c";

  // floating orb
  const orb = document.createElement("div");
  orb.id = "meok-orb";
  orb.title = "MEOK Sovereign";
  orb.innerHTML = "🐉";
  orb.style.cssText = `position:fixed;bottom:22px;right:22px;z-index:2147483647;width:54px;height:54px;border-radius:50%;
    background:radial-gradient(circle at 38% 32%, #2a2218, #0e0c08);color:${GOLD};display:flex;align-items:center;justify-content:center;
    font-size:26px;cursor:pointer;box-shadow:0 6px 24px rgba(0,0,0,.4),0 0 0 1px ${GOLD}55, 0 0 22px ${GOLD}55;
    transition:transform .2s; user-select:none`;
  orb.onmouseenter = () => orb.style.transform = "scale(1.08)";
  orb.onmouseleave = () => orb.style.transform = "scale(1)";

  // panel
  const panel = document.createElement("div");
  panel.id = "meok-panel";
  panel.style.cssText = `position:fixed;bottom:88px;right:22px;z-index:2147483647;width:340px;max-width:92vw;height:460px;max-height:72vh;
    display:none;flex-direction:column;background:#FFFCF5;color:#2a1a14;border:1px solid ${GOLD};border-radius:16px;overflow:hidden;
    box-shadow:0 20px 60px rgba(0,0,0,.4);font-family:-apple-system,Segoe UI,Roboto,sans-serif`;
  panel.innerHTML = `
    <div style="background:linear-gradient(135deg,#1a1410,#3a2e1a);color:${GOLD};padding:12px 14px;display:flex;align-items:center;gap:9px;font-weight:800">
      <span style="font-size:18px">🐉</span> MEOK Sovereign
      <span style="margin-left:auto;font-weight:500;font-size:11px;opacity:.7">on this page</span>
      <span id="meok-x" style="cursor:pointer;font-size:18px;opacity:.8">×</span>
    </div>
    <div id="meok-log" style="flex:1;overflow:auto;padding:14px;display:flex;flex-direction:column;gap:9px;font-size:13.5px;line-height:1.5"></div>
    <div style="display:flex;gap:8px;padding:12px;border-top:1px solid #eee2c8">
      <input id="meok-in" placeholder="Ask your Sovereign…" style="flex:1;border:1px solid #e0d4b0;border-radius:10px;padding:9px 12px;font-size:13.5px;outline:none">
      <button id="meok-send" style="border:none;background:${GOLD};color:#1a1410;font-weight:800;border-radius:10px;padding:0 14px;cursor:pointer">➤</button>
    </div>`;

  document.documentElement.append(orb, panel);
  const log = panel.querySelector("#meok-log");
  const input = panel.querySelector("#meok-in");

  function say(who, html) {
    const m = document.createElement("div");
    m.style.cssText = who === "me"
      ? "align-self:flex-end;background:#1a1410;color:#f5f0e6;padding:8px 12px;border-radius:13px 13px 3px 13px;max-width:85%"
      : "align-self:flex-start;background:#f3ecda;padding:8px 12px;border-radius:13px 13px 13px 3px;max-width:90%";
    m.innerHTML = html; log.appendChild(m); log.scrollTop = log.scrollHeight; return m;
  }
  function toggle(show) {
    panel.style.display = (show ?? panel.style.display === "none") ? "flex" : "none";
    if (panel.style.display === "flex" && !log.childElementCount) {
      say("ai", "I'm your Sovereign — here on <b>" + location.hostname + "</b>. Ask me anything, and I'll find the right tool from your fleet. Your data stays yours.");
      input.focus();
    }
  }
  orb.onclick = () => toggle();
  panel.querySelector("#meok-x").onclick = () => toggle(false);

  async function send() {
    const v = input.value.trim(); if (!v) return; input.value = "";
    say("me", v.replace(/[<>&]/g, c => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c])));
    const t = say("ai", "…");
    try {
      const r = await fetch(API + "/api/chat", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: v, queen_id: "queen-king", arcana_lens: 21,
          persona: "The user is on the website " + location.hostname + ". Help them in context." })
      });
      const d = await r.json();
      t.innerHTML = (d.response || "…").replace(/</g, "&lt;");
      // surface matching sovereign tools
      const tr = await (await fetch(API + "/api/tools?q=" + encodeURIComponent(v) + "&limit=3")).json();
      if (tr.matches && tr.matches.length) {
        const box = say("ai", "🧰 <b>Tools for this:</b><br>");
        box.innerHTML += tr.matches.map(m =>
          `<a href="${API}/sovspace.html?q=${encodeURIComponent(m.name)}" target="_blank" style="display:inline-block;margin:4px 4px 0 0;padding:2px 9px;border:1px solid ${GOLD};border-radius:999px;color:#8a6f2e;text-decoration:none;font-size:12px">${m.name}</a>`).join("");
      }
    } catch (e) { t.innerHTML = "I'm here — try once more."; }
  }
  panel.querySelector("#meok-send").onclick = send;
  input.addEventListener("keydown", e => { if (e.key === "Enter") send(); });
})();
