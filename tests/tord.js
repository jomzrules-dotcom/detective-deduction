const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');const root='/tmp/app4p';
const srv=http.createServer((q,s)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u==='/')u='/index.html';const f=path.join(root,u);fs.readFile(f,(e,d)=>{if(e){s.statusCode=404;s.end();}else{if(f.endsWith('.json'))s.setHeader('Content-Type','application/json');s.end(d);}});}).listen(8796);
(async()=>{const b=await chromium.launch();const errs=[];const p=await b.newPage({viewport:{width:1180,height:820}});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8796/');await p.evaluate(()=>localStorage.clear());await p.reload();await p.waitForTimeout(2500);
const r=await p.evaluate(()=>{progress={};progress[CASES[0].id]={stars:2,score:1};saveProgress();render();return CASES.slice(0,4).map(c=>[c.n,caseOpen(c)]);});console.log(JSON.stringify(r));
await p.waitForTimeout(500);await p.screenshot({path:'/tmp/ord_hub.png'});
const t=await p.evaluate(()=>{loadCase(CASES[3]);return !!C;});console.log('loaded locked case?',t);
await p.evaluate(()=>{unlockAll=true;});console.log('unlockAll opens 10:',await p.evaluate(()=>caseOpen(CASES[9])));
console.log('errors',errs);await b.close();srv.close();})();
