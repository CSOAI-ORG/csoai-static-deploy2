/* @csoai/sdk — app-style SDK: import + use the Council OS from any app.
 *   import { csoai } from './sdk.mjs';
 *   const board = await csoai.board(); const card = await csoai.attest({sector:'bond',subject:'UK Gilt'});
 */
const H='https://csoai-gspc.pages.dev';
const GET=async(u)=> (await fetch(H+u)).json();
const POST=async(u,b)=>(await fetch(H+u,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(b)})).json();
export const csoai={
  board: ()=>GET('/api/gspc'),
  instruments: ()=>GET('/api/instruments'),
  route: (uri)=>GET('/api/route?uri='+encodeURIComponent(uri)),
  signal: (axis='gov',jur='EU')=>GET('/api/signal?axis='+axis+'&jurisdiction='+jur),
  sovSignal: ()=>GET('/api/sov-signal'),
  attest: (obj)=>POST('/api/attest',obj),
  dvp: (obj)=>POST('/api/dvp',obj),
  underwrite: (obj)=>POST('/api/underwrite',obj),
  crosswalk: (obj)=>POST('/api/crosswalk',obj),
  cobol: (obj)=>POST('/api/cobol',obj),
  verify: (card)=>POST('/api/verify',card)
};
export default csoai;
