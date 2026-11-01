const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');const root='/tmp/app4p';
const srv=http.createServer((q,s)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u==='/')u='/index.html';const f=path.join(root,u);fs.readFile(f,(e,d)=>{if(e){s.statusCode=404;s.end();}else{if(f.endsWith('.json'))s.setHeader('Content-Type','application/json');s.end(d);}});}).listen(8795);
(async()=>{const b=await chromium.launch();const errs=[];
for(const vp of [{width:1180,height:820},{width:844,height:390}]){
const p=await b.newPage({viewport:vp});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8795/');await p.evaluate(()=>localStorage.clear());await p.reload();await p.waitForTimeout(2500);
await p.evaluate(()=>{CASES.slice(0,13).forEach(c=>progress[c.id]={stars:c.n%4?3:2,score:1});saveProgress();fileExp=0;render();});
await p.waitForTimeout(700);await p.screenshot({path:`/tmp/cab_${vp.width}.png`});
await p.evaluate(()=>openDrawer(2));await p.waitForTimeout(300);await p.screenshot({path:`/tmp/cab_pull_${vp.width}.png`});
await p.waitForTimeout(900);await p.screenshot({path:`/tmp/cab_open_${vp.width}.png`});
await p.close();}
console.log('errors',errs);await b.close();srv.close();})();
