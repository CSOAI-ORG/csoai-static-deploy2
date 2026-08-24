#!/usr/bin/env node
/* csoai CLI — measurement · route · verify (drop-in). npx csoai measure/route/verify */
const H='https://csoai-gspc.pages.dev';
const [cmd,...rest]=process.argv.slice(2);
async function j(u,o){ const r=await fetch(H+u,o); return r.json(); }
(async()=>{
  try{
    if(cmd==='measure'){ console.log(JSON.stringify(await j('/api/gspc'),null,2).slice(0,600)); }
    else if(cmd==='route'){ const u=(rest[0]||'eunomia://regulation/REG-001'); console.log(JSON.stringify(await j('/api/route?uri='+encodeURIComponent(u)),null,2)); }
    else if(cmd==='sov-signal'){ console.log(JSON.stringify(await j('/api/sov-signal'),null,2).slice(0,400)); }
    else { console.log('usage: npx csoai measure | route <eunomia://> | sov-signal · measurement, not certification'); }
  }catch(e){ console.error('error:',String(e).slice(0,120)); }
})();
