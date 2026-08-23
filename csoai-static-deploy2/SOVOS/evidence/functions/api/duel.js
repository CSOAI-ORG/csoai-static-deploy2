const QS = [
 "Who is accountable for an AI system deployment under the EU AI Act?",
 "What does Article 50 require for AI-generated content?",
 "What is the East-West regulatory pair-gap?",
 "What does Illinois SB 315 mandate?",
 "Who should pay for independent AI evaluation?",
 "What is the difference between measurement and certification?"
];
async function ask(env, style){
  const r=await fetch('https://api.deepseek.com/chat/completions',{method:'POST',headers:{'Authorization':'Bearer '+env.DEEPSEEK_API_KEY,'content-type':'application/json'},
   body:JSON.stringify({model:'deepseek-chat',max_tokens:180,messages:[
     {role:'system',content:'You are a candidate model in a governance-answer arena. Give a concise, correct governance answer. '+style+' Measurement, not certification. Never invent a regulatory fact — if unsure say UNMEASURED.'},
     {role:'user',content:'Answer: '}
   ]})});
  const d=await r.json(); return (d.choices&&d.choices[0]&&d.choices[0].message.content)?d.choices[0].message.content:'';
}
export async function onRequestPost({ request, env }) {
  try{
    const { q } = await request.json();
    const quest = (q&&q.trim())?q:QS[Math.floor(Math.random()*QS.length)];
    const [a,b] = await Promise.all([ask(env,'Answer plainly and structurally.'), ask(env,'Be precise and concise, cite the hook.')]);
    const id='duel-'+(Date.now());
    return new Response(JSON.stringify({ok:true,id,question:quest,a,b,ts:new Date().toISOString()}),{headers:{'content-type':'application/json'}});
  }catch(e){ return new Response(JSON.stringify({ok:false,error:String(e)}),{status:500,headers:{'content-type':'application/json'}}); }
}
