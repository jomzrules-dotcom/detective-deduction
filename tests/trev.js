const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');const root='/tmp/app4p';
const srv=http.createServer((q,s)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u==='/')u='/index.html';const f=path.join(root,u);fs.readFile(f,(e,d)=>{if(e){s.statusCode=404;s.end();}else{if(f.endsWith('.json'))s.setHeader('Content-Type','application/json');s.end(d);}});}).listen(8797);
(async()=>{const b=await chromium.launch();const errs=[];
for(const vp of [{width:1180,height:820},{width:844,height:390}]){
const p=await b.newPage({viewport:vp});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8797/');await p.waitForTimeout(2500);
await p.evaluate(async()=>{const c=CASES[20];await ensureCase(c);loadCase(c);
 const ids=order(); ids.forEach((id,j)=>{S.talking=id;person(id).questions.forEach((q,i)=>{ if(j===2&&i===1) return; S.asked[id+i]=true;if(q.ev&&!S.found.includes(q.ev))S.found.push(q.ev);if(q.s&&!S.stmts.includes(q.s.id))S.stmts.push(q.s.id);});});
 ALL.forEach((s,i)=>S.marks[s.id]=i===1?'unknown':i===4?'fact':s.answer); S.accused=C.culprit;S.screen='verdict';render();confirmVerdict();});
await p.waitForTimeout(800);await p.screenshot({path:`/tmp/rev_result_${vp.width}.png`});
await p.evaluate(()=>{S.nbTab='suspects';openNb();});await p.waitForTimeout(600);await p.screenshot({path:`/tmp/rev_sus_${vp.width}.png`});
await p.evaluate(()=>{S.nbTab='evidence';renderNb();});await p.waitForTimeout(400);await p.screenshot({path:`/tmp/rev_ev_${vp.width}.png`});
const h=await p.evaluate(()=>getComputedStyle(document.getElementById('nbhandle')).display);console.log(vp.width,'handle display',h);
await p.close();}
console.log('errors',errs);await b.close();srv.close();})();
