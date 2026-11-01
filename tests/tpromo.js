const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');const root='/tmp/app4p';
const srv=http.createServer((q,s)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u==='/')u='/index.html';const f=path.join(root,u);fs.readFile(f,(e,d)=>{if(e){s.statusCode=404;s.end();}else{if(f.endsWith('.json'))s.setHeader('Content-Type','application/json');s.end(d);}});}).listen(8799);
(async()=>{const b=await chromium.launch();const errs=[];
for(const vp of [{width:1180,height:820},{width:390,height:844}]){
const p=await b.newPage({viewport:vp});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8799/');await p.evaluate(()=>localStorage.clear());await p.reload();await p.waitForTimeout(2500);await p.evaluate(()=>Promise.all(CASES.map(ensureCase)));
await p.screenshot({path:`/tmp/files_hub_${vp.width}.png`});
const ready=await p.evaluate(()=>CASES.filter(caseReady).map(c=>c.n));console.log('ready',ready);
// solve 1-9 then play 10
await p.evaluate(()=>{CASES.slice(0,9).forEach(c=>progress[c.id]={stars:3,score:1});saveProgress();
 loadCase(CASES[9]);order().forEach(id=>{S.talking=id;person(id).questions.forEach((q,i)=>{S.asked[id+i]=true;if(q.ev&&!S.found.includes(q.ev))S.found.push(q.ev);if(q.s&&!S.stmts.includes(q.s.id))S.stmts.push(q.s.id);});});
 ALL.forEach(s=>S.marks[s.id]=s.answer);S.accused=C.culprit;S.screen='verdict';render();confirmVerdict();});
await p.waitForTimeout(2200);await p.screenshot({path:`/tmp/files_promo_${vp.width}.png`});
await p.evaluate(()=>closePromo(1));await p.waitForTimeout(500);await p.screenshot({path:`/tmp/files_hub2_${vp.width}.png`});
await p.close();}
console.log('errors',errs);await b.close();srv.close();})();
