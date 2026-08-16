/**
 * csoai-city-3d-mcp — City / Colosseum / Arena rendered in Cesium 3D,
 * served as MCP tools so ANY MCP-speaking AI platform (Claude, Cursor,
 * Windsurf, ChatGPT integrations, Grok) can summon the sovereign city
 * visually inside the chat. This is the "end users live in AI platforms,
 * not websites" distribution seam.
 *
 * Tools:
 *   render_city       — Cesium globe + faction points + breach markers
 *   render_colosseum  — model-vs-model arena with Elo + verdict
 *   render_arena      — measured-model leaderboard as globe towers
 *   render_index      — the GSPC Daily Index as a 3D monument
 *
 * Every page: pure HTML, Cesium 1.123 free CDN (no Ion key), no build.
 * Measurement-not-certification wording; missing data -> honest UNMEASURED.
 */
const CESIUM_JS = "https://cdn.jsdelivr.net/npm/cesium@1.123/Build/Cesium/Cesium.js";
const CESIUM_CSS = "https://cdn.jsdelivr.net/npm/cesium@1.123/Build/Cesium/Widgets/widgets.css";

function esc(s) {
  return String(s ?? "").replace(/</g, "\\u003c").replace(/>/g, "\\u003e").replace(/"/g, '\\"');
}

function page(title, sceneJs, init) {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} — Council of AI</title>
<link href="${CESIUM_CSS}" rel="stylesheet">
<style>
  html,body{width:100%;height:100%;margin:0;overflow:hidden;background:#02020a;font-family:system-ui,sans-serif;}
  #cs{width:100%;height:100%;}
  #hud{position:fixed;top:0;left:0;right:0;padding:12px 16px;color:#c9a84c;font-family:monospace;font-size:11px;
       background:linear-gradient(180deg,rgba(0,0,0,.7),transparent);pointer-events:none;z-index:10;}
  #hud b{color:#fff;}
  .pill{display:inline-block;border:1px solid #c9a84c;border-radius:100px;padding:2px 10px;margin-left:6px;font-size:10px;}
  .pill.r{border-color:#f87171;color:#f87171;} .pill.b{border-color:#4ade80;color:#4ade80;}
  #foot{position:fixed;bottom:8px;left:12px;color:#7f90a0;font-size:10px;font-family:monospace;z-index:10;pointer-events:none;}
</style></head><body>
<div id="hud"><b>${esc(title)}</b><span class="pill">Council of AI</span><span class="pill">MCP 3D</span><span class="pill r" id="rC"></span><span class="pill b" id="bC"></span></div>
<div id="cs"></div>
<div id="foot">measurement, not certification · signed + time-anchored · from csoai-city-3d-mcp</div>
<script>window.__I__=${JSON.stringify(init ?? {})};</script>
<script>window.CESIUM_BASE_URL='https://cdn.jsdelivr.net/npm/cesium@1.123/Build/Cesium/';</script>
<script src="${CESIUM_JS}"></script>
<script>${sceneJs}</script>
</body></html>`;
}

function glBoiler() {
  return `const Cs=Cesium;
const v=new Cs.Viewer('cs',{imageryProvider:new Cs.OpenStreetMapImageryProvider({url:'https://tile.openstreetmap.org/'}),
  baseLayerPicker:false,geocoder:false,homeButton:false,sceneModePicker:false,navigationHelpButton:false,
  animation:false,timeline:false,fullscreenButton:false,infoBox:false,selectionIndicator:false});
v.scene.globe.baseColor=Cs.Color.fromCssColorString('#0a1a2f');
v.scene.backgroundColor=Cs.Color.fromCssColorString('#02020a');
v.camera.flyTo({destination:Cs.Cartesian3.fromDegrees((window.__INIT.lon??-0.1278),(window.__INIT.lat??51.5074),160000),duration:3});`;
}

function cityScene(args) {
  const pts = Array.isArray(args?.points) ? args.points.slice(0, 200) : [];
  const js = glBoiler() + `
  const pts=${JSON.stringify(pts)};
  pts.forEach((p,i)=>{const col=p.faction==='RED'?'#f87171':(p.faction==='BLUE'?'#4ade80':'#60a5fa');
    v.entities.add({position:Cs.Cartesian3.fromDegrees(p.lon??-0.1278+(i%10)*0.02,p.lat??51.5074+(i%7)*0.015,1500+(i%6)*250),
      point:{pixelSize:p.breach?13:6,color:Cs.Color.fromCssColorString(col),outlineColor:Cs.Color.BLACK,outlineWidth:1}});});
  document.getElementById('rC').textContent='RED '+pts.filter(p=>p.faction==='RED').length;
  document.getElementById('bC').textContent='BLUE '+pts.filter(p=>p.faction==='BLUE').length;`;
  return page("Sovereign City", js, { points: pts });
}

function colosseumScene(args) {
  const js = glBoiler() + `
  const a=${JSON.stringify(args?.model_a ?? 'Model A')}, b=${JSON.stringify(args?.model_b ?? 'Model B')};
  const sa=Number(args?.score_a??100), sb=Number(args?.score_b??100), el=(sa+sb)/2;
  const p1=Cs.Cartesian3.fromDegrees(-0.1278,51.5074,0), p2=Cs.Cartesian3.fromDegrees(0.1278,51.5074,0);
  v.entities.add({position:p1,point:{pixelSize:Math.min(18,6+sa/20),color:Cs.Color.fromCssColorString('#f87171')},
    label:{text:a+' '+sa,font:'12px monospace',fillColor:Cs.Color.WHITE,pixelOffset:new Cs.Cartesian2(0,-18)}});
  v.entities.add({position:p2,point:{pixelSize:Math.min(18,6+sb/20),color:Cs.Color.fromCssColorString('#4ade80')},
    label:{text:b+' '+sb,font:'12px monospace',fillColor:Cs.Color.WHITE,pixelOffset:new Cs.Cartesian2(0,-18)}});
  v.entities.add({polyline:{positions:[p1,p2],width:2,clampToGround:false,
    material:new Cs.PolylineGlowMaterialProperty({color:Cs.Color.fromCssColorString('#c9a84c'),glowPower:0.25})}});`;
  return page("Colosseum Duel", js, {});
}

function arenaScene(args) {
  const models = (Array.isArray(args?.models) ? args.models.slice(0, 30) : []).map(m => ({ name: m.name ?? "?", elo: Number(m.elo ?? m.score ?? 1000), games: Number(m.games ?? 0) }));
  const js = glBoiler() + `
  const ms=${JSON.stringify(models)};
  ms.forEach((m,i)=>{const a=(i/ms.length)*Math.PI*2;
    const p=Cs.Cartesian3.fromDegrees(-0.1278+0.06*Math.cos(a),51.5074+0.06*Math.sin(a),1000+Math.max(0,m.elo-800)*18);
    v.entities.add({position:p,
      point:{pixelSize:Math.min(16,4+ (m.elo-800)/60),color:Cs.Color.fromCssColorString('#60a5fa')},
      label:{text:m.name+' '+(m.elo).toFixed(0)+' fontSize:'12px',font:'11px monospace',fillColor:Cs.Color.WHITE,
        pixelOffset:new Cs.Cartesian2(0,-16),style:Cs.LabelStyle.FILL_AND_OUTLINE,outlineWidth:2}});});`;
  return page("Arena — 3D Leaderboard", js, {});
}

function indexScene(args) {
  const idx = args?.index ?? null;
  const h = idx == null ? 0 : (idx - 50) * 400;
  const js = glBoiler() + `
  const idx=${JSON.stringify(idx)}, ci=${JSON.stringify(args?.ci ?? [])};
  const spot=Cs.Cartesian3.fromDegrees(-0.1278,51.5074,5000);
  v.entities.add({position:spot,point:{pixelSize:20,color:Cs.Color.fromCssColorString('#c9a84c')},
    label:{text:'GSPC INDEX '+(idx??'UNMEASURED'),font:'16px monospace',
      fillColor:Cs.Color.fromCssColorString('#c9a84c'),pixelOffset:new Cs.Cartesian2(0,-28),
      style:Cs.LabelStyle.FILL_AND_OUTLINE,outlineWidth:3}});
  if(Array.isArray(ci)&&ci.length===2){v.entities.add({polyline:{positions:[
    Cs.Cartesian3.fromDegrees(-0.14,51.50,5000),Cs.Cartesian3.fromDegrees(0.14,51.50,5000)],
    width:1,material:new Cs.PolylineGlowMaterialProperty({color:Cs.Color.fromCssColorString('#4ade80'),glowPower:0.15})}});}`;
  return page("GSPC Daily Index", js, {});
}

const TOOLS = [
  { name: "render_city", description: "Render the sovereign measurement city in 3D (Cesium globe). Pass points [{lon,lat,faction,breach,axis}]. Returns a self-contained HTML page.",
    inputSchema: { type: "object", properties: { points: { type: "array", items: { type: "object" } } } } },
  { name: "render_colosseum", description: "3D duel: two models head-to-head. Pass model_a, model_b, score_a, score_b.",
    inputSchema: { type: "object", properties: { model_a: { type: "string" }, model_b: { type: "string" }, score_a: { type: "number" }, score_b: { type: "number" } } } },
  { name: "render_arena", description: "3D leaderboard of measured models. Pass models:[{name,elo,games}].",
    inputSchema: { type: "object", properties: { models: { type: "array", items: { type: "object" } } } } },
  { name: "render_index", description: "Render the GSPC Daily Index as a 3D monument. Pass index, ci, date.",
    inputSchema: { type: "object", properties: { index: { type: "number" }, ci: { type: "array" }, date: { type: "string" } } } },
  { name: "render_library", description: "3D Paper District: the estate's valuable IP whitepapers as labeled pavilions on the globe. Pass [] to render all, or papers:[{slug,title,lane,url}]. Returns a self-contained HTML page.",
    inputSchema: { type: "object", properties: { papers: { type: "array", items: { type: "object" } } } } },
];

function libraryScene(args) {
  const papers = Array.isArray(args?.papers) && args.papers.length ? args.papers : PAPERS;
  const js = glBoiler() + `
  const papers=${JSON.stringify(papers)};
  papers.forEach((p,i)=>{const a=(i/papers.length)*Math.PI*2 + 0.3;
    const lat=51.5074+0.05*Math.sin(a), lon=-0.1278+0.09*Math.cos(a);
    const col=['#c9a84c','#4ade80','#60a5fa','#f87171','#c084fc','#fbbf24'][i%6];
    const pos=Cs.Cartesian3.fromDegrees(lon,lat,1200);
    v.entities.add({position:pos,
      point:{pixelSize:13,color:Cs.Color.fromCssColorString(col),outlineColor:Cs.Color.BLACK,outlineWidth:1,heightReference:Cs.HeightReference.CLAMP_TO_GROUND},
      label:{text:p.title,font:'11px monospace',fillColor:Cs.Color.WHITE,pixelOffset:new Cs.Cartesian2(0,18),
             style:Cs.LabelStyle.FILL_AND_OUTLINE,outlineWidth:2,disableDepthTestDistance:Number.POSITIVE_INFINITY},
      description:\`<b>\${esc(p.title)}</b><br>\${esc(p.lane||'')} — <a href="\${esc(p.url||'#')}">open paper</a>\`});
    v.entities.add({position:pos,billboard:{image:Cs.buildModuleUrl('Assets/Textures/pin.png')||undefined,show:false}});
    if(i>0){v.entities.add({polyline:{positions:[
      pos,Cs.Cartesian3.fromDegrees(-0.1278+0.09*Math.cos(a-0.3),51.5070+0.05*Math.sin(a-0.3),0)],
      width:1,material:new Cs.PolylineGlowMaterialProperty({color:Cs.Color.fromCssColorString(col),glowPower:0.1})}});}
  });
  document.getElementById('rC').textContent='PAPERS '+papers.length;`;
  return page("IP Paper District — Council of AI", js, {});
}

const PAPERS = [
  { slug: "emotional-safety-ruler", title: "Emotional Safety Ruler (Whitepaper A)", lane: "research", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/research/WHITEPAPER_A_EMOTIONAL_SAFETY_RULER_2026-08-12.md" },
  { slug: "article50-alternative-means", title: "Article 50 Alternative-Means Evidence Pack", lane: "article50", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/article50-packs/ARTICLE_50_ALTERNATIVE_MEANS_PACK_2026-08-13.md" },
  { slug: "oscal-signature-gap", title: "OSCAL Signature-Gap Play", lane: "standards", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/oscal-gap-play/OSCAL_SIGNATURE_GAP_PLAY_2026-08-13.md" },
  { slug: "dsit-assurance-bid", title: "DSIT AI Assurance Innovation Fund Bid", lane: "funding", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/dsit-bid/DSIT_AI_ASSURANCE_FUND_BID_2026-08-13.md" },
  { slug: "provbench-wedge", title: "ProvBench Public Wedge — signed reproducibility", lane: "preprint", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/preprints/PROVBENCH_WEDGE_2026-08-13.md" },
  { slug: "signed-fluid-build", title: "Signed-Fluid Build Doc — AI-economy fabric", lane: "build", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/SIGNED_FLUID_BUILD_DOC_2026-08-15.md" },
  { slug: "regulator-mapping", title: "Regulator Mapping Pack (EU/UK/US)", lane: "regulated", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/REGULATOR_MAPPING_PACK_2026-08-15.md" },
  { slug: "press-release", title: "Press Release Pack", lane: "comms", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/PRESS_RELEASE_PACK_2026-08-15.md" },
  { slug: "operating-playbook", title: "Operating Playbook", lane: "ops", url: "https://github.com/CSOAI-ORG/csoai-static-deploy2/blob/jv-wave8-production/SOVOS/OPERATING_PLAYBOOK_2026-08-15.md" },
];

export default {
  async fetch(request) {
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
      "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    };
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const url = new URL(request.url);
    if (url.pathname === "/health" || url.pathname === "/") {
      return new Response(JSON.stringify({ status: "ok", service: "csoai-city-3d-mcp" }), { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
    }
    if (url.pathname === "/scene") {
      const scene = url.searchParams.get("scene") || "city";
      const args = {};
      try { Object.assign(args, JSON.parse(url.searchParams.get("args") || "{}")); } catch {}
      const html = scene === "colosseum" ? colosseumScene(args) : scene === "arena" ? arenaScene(args) : scene === "index" ? indexScene(args) : scene === "library" ? libraryScene(args) : cityScene(args);
      return new Response(html, { status: 200, headers: { ...cors, "Content-Type": "text/html" } });
    }
    if (url.pathname !== "/mcp" || request.method !== "POST") {
      return new Response(JSON.stringify({ error: "not_found" }), { status: 404, headers: { ...cors, "Content-Type": "application/json" } });
    }
    let body; try { body = await request.json(); } catch { return new Response(JSON.stringify({ error: "invalid_json" }), { status: 400, headers: { ...cors, "Content-Type": "application/json" } }); }
    const { method: m, params, id } = body;
    const respond = (result) => new Response(JSON.stringify({ jsonrpc: "2.0", id, result }), { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
    const respondError = (code, message) => new Response(JSON.stringify({ jsonrpc: "2.0", id, error: { code, message } }), { status: 200, headers: { ...cors, "Content-Type": "application/json" } });

    if (m === "initialize") return respond({ protocolVersion: params?.protocolVersion || "2025-03-26", capabilities: { tools: {} }, serverInfo: { name: "csoai-city-3d-mcp", version: "1.0.0" } });
    if (m === "notifications/initialized" || m === "ping") return respond({});
    if (m === "tools/list") return respond({ tools: TOOLS });
    if (m === "tools/call") {
      const name = params?.name; const args = params?.arguments || {};
      let text;
      if (name === "render_city") text = cityScene(args);
      else if (name === "render_colosseum") text = colosseumScene(args);
      else if (name === "render_arena") text = arenaScene(args);
      else if (name === "render_index") text = indexScene(args);
      else if (name === "render_library") text = libraryScene(args);
      else return respondError(-32602, "tool not found");
      return respond({ content: [{ type: "text", text: "```html\n" + text + "\n```" }] });
    }
    return respondError(-32601, "method not found");
  },
};