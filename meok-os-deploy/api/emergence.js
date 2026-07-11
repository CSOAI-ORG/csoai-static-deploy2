// Proxy the free-OCI emergence tick over HTTPS (the universe page is https; the micro is http →
// mixed-content blocked in-browser). Server-side fetch has no such block. Free, always-on.
export default async function handler(req,res){
  res.setHeader('Access-Control-Allow-Origin','*'); res.setHeader('Cache-Control','public, max-age=15');
  try{ const ctl=new AbortController(); const to=setTimeout(()=>ctl.abort(),3000);
    const r=await fetch('http://145.241.232.16:8080/status',{signal:ctl.signal}); clearTimeout(to);
    const d=await r.json(); return res.status(200).json({ ok:true, ...d, via:'free-oci-micro' });
  }catch(e){ return res.status(200).json({ ok:false, tick:null, note:'emergence micro waking ('+String(e.message||e).slice(0,40)+')' }); }
}
