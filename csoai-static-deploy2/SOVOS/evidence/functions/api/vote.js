export async function onRequestPost({ request, env }) {
  try{ const b=await request.json(); const id='vote-'+(Date.now());
    await env.CSOAI_LEADS.put(id, JSON.stringify({...b,ts:new Date().toISOString()}));
    return new Response(JSON.stringify({ok:true,id}),{headers:{'content-type':'application/json'}});
  }catch(e){ return new Response(JSON.stringify({ok:false,error:String(e)}),{status:500,headers:{'content-type':'application/json'}}); }
}
