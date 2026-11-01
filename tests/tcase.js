// node tcase.js <caseIndex> : screenshots line-up + 2 interviews, full playthrough check
const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const ci=+process.argv[2];const root='/tmp/app4p';
const srv=http.createServer((q,s)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u==='/')u='/index.html';const f=path.join(root,u);fs.readFile(f,(e,d)=>{if(e){s.statusCode=404;s.end();}else{if(f.endsWith('.json'))s.setHeader('Content-Type','application/json');if(f.endsWith('.webp'))s.setHeader('Content-Type','image/webp');s.end(d);}});}).listen(8780+ci);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1180,height:820}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:'+(8780+ci)+'/');await p.waitForTimeout(2500);await p.evaluate(()=>Promise.all(CASES.map(ensureCase)));await p.screenshot({path:`/tmp/c${ci+1}_hub.png`});
await p.evaluate(i=>{unlockAll=true;loadCase(CASES[i]);S.screen='scene';render();},ci);await p.waitForTimeout(600);await p.screenshot({path:`/tmp/c${ci+1}_scene.png`});
const ids=await p.evaluate(()=>order());
await p.evaluate(id=>startTalk(id),ids[0]);await p.waitForTimeout(2200);await p.screenshot({path:`/tmp/c${ci+1}_t1.png`});
await p.evaluate(id=>{startTalk(id);},ids[ids.length-1]);await p.waitForTimeout(300);await p.evaluate(()=>ask(1));await p.waitForTimeout(2200);await p.screenshot({path:`/tmp/c${ci+1}_t2.png`});
const r=await p.evaluate(()=>{loadCase(C);order().forEach(id=>{S.talking=id;person(id).questions.forEach((q,i)=>{S.asked[id+i]=true;if(q.ev&&!S.found.includes(q.ev))S.found.push(q.ev);if(q.s&&!S.stmts.includes(q.s.id))S.stmts.push(q.s.id);});});
 const missEv=Object.keys(C.evidence).filter(k=>!S.found.includes(k));ALL.forEach(s=>S.marks[s.id]=s.answer);S.accused=C.culprit;S.screen='verdict';render();confirmVerdict();
 const noIcon=[...new Set(Object.values(C.evidence).map(e=>e.icon))].filter(i=>!(ART.icons&&ART.icons[i]));
 const noArt=order().filter(id=>!ART.figures[C.chars[id].key]||!ART.portraits[C.chars[id].key]);
 const m=MOODS[C.id]||{};const noMood=[];for(const [id,v] of Object.entries(m)){const k=ART.portraits[C.chars[id].key]||{};[v.greet,...v.q,v.wrong].filter(Boolean).forEach(md=>{if(!k[md])noMood.push(id+':'+md);});}
 return {stars:progress[C.id]&&progress[C.id].stars,missEv,noIcon,noArt,noMood};});
console.log(JSON.stringify(r),'errors',errs);await b.close();srv.close();})();
