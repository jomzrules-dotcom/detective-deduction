const fs=require('fs');const h=fs.readFileSync('/mnt/user-data/outputs/app4/index.html','utf8');
const s=h.indexOf('const CASES');const e=h.indexOf('\n];',s);const pre=h.slice(h.indexOf('<script>')+8,s);
const vm=require('vm');const ctx={};vm.createContext(ctx);vm.runInContext(pre+'\n'+h.slice(s,e+3).replace('const CASES','this.CASES')+'\n'+h.slice(h.indexOf('const MOODS'),h.indexOf('};',h.indexOf('const MOODS'))+2).replace('const MOODS','this.MOODS'),ctx);
const specs={};for(const f of fs.readdirSync('/mnt/user-data/outputs/gen').filter(f=>/^case\d+\.json$/.test(f))){const j=JSON.parse(fs.readFileSync('/mnt/user-data/outputs/gen/'+f));specs[j.case]=j;}
const caseDir={cheese:'case21',surprise:'case22',harmonica:'case23',trainset:'case24',topper:'case25',pumpkin:'case26',ferry:'case27',page:'case28',tag:'case29',openkey:'case30',bird:'case11',shortcut:'case12',copy:'case13',orchid:'case14',medal:'case15',song:'case16',quiz:'case17',letter:'case18',clock:'case19',jackets:'case20'};
const iconsAll=new Set(Object.keys(JSON.parse(fs.readFileSync('/mnt/user-data/outputs/webp/manifest.json')).icons));Object.values(specs).forEach(sp=>sp.icons.forEach(i=>iconsAll.add(i.name)));
let bad=0;const say=(c,m)=>{bad++;console.log(c,m)};
const ids=new Set();
for(const c of ctx.CASES.filter(c=>c.n>=11)){ if(ids.has(c.id))say(c.id,'dup id');ids.add(c.id);
 const ev=Object.keys(c.evidence), given=new Set();
 for(const [wid,w] of Object.entries(c.witnesses)){ if(w.questions.length!==3)say(c.id,wid+' qcount'); w.questions.forEach(q=>{if(q.ev){if(!c.evidence[q.ev])say(c.id,'missing ev '+q.ev);given.add(q.ev);}}); if(!c.chars[wid])say(c.id,'nochar '+wid);}
 ev.forEach(k=>{if(!given.has(k))say(c.id,'card never given '+k); if(!iconsAll.has(c.evidence[k].icon))say(c.id,'icon? '+c.evidence[k].icon);});
 let liars=0, stIds=new Set();
 for(const [sid,su] of Object.entries(c.suspects)){ if(!c.chars[sid])say(c.id,'nochar '+sid); if(su.questions.length!==3)say(c.id,sid+' st count'); let lied=false;
  su.questions.forEach(q=>{const st=q.s; if(stIds.has(st.id))say(c.id,'dup st '+st.id); stIds.add(st.id); if(!['fact','lie','unknown'].includes(st.answer))say(c.id,'ans '+st.id);
   if(st.answer!=='unknown'){const refs=(st.reason.match(/E\d+/g)||[]); if(!refs.length)say(c.id,'no ref '+st.id); refs.forEach(r=>{if(!c.evidence[r])say(c.id,'bad ref '+r+' in '+st.id)});} if(st.answer==='lie')lied=true;});
  if(lied)liars++;
  if(sid!==c.culprit){ if(!su.wrong||!su.clear)say(c.id,'no wrong/clear '+sid); (su.clear||[]).forEach(r=>{if(!c.evidence[r])say(c.id,'clear ref '+r)});}
 }
 if(!c.suspects[c.culprit])say(c.id,'culprit not suspect');
 // moods vs spec
 const m=ctx.MOODS[c.id]||{};
 for(const [id,v] of Object.entries(m)){ const ch=c.chars[id]; if(!ch){say(c.id,'mood for unknown '+id);continue;} const [cid,who]=(ch.art||c.id+'/'+id).split('/'); const sp=specs[caseDir[cid]]; const sc=sp&&sp.chars.find(x=>x.id===who); if(!sc){say(c.id,'no spec char '+id);continue;}
  const have=new Set(['neutral','nervous',...(sc.moods||[])]); [v.greet,...(v.q||[]),v.wrong].filter(Boolean).forEach(md=>{if(!have.has(md))say(c.id,`mood ${id}:${md} not painted`)});}
 Object.keys(c.chars).forEach(id=>{const ch=c.chars[id];const [cid,who]=(ch.art||c.id+'/'+id).split('/');const sp=specs[caseDir[cid]];if(!sp||!sp.chars.find(x=>x.id===who))say(c.id,'char not in art spec '+id)});
 console.log(c.n,c.id,'suspects',Object.keys(c.suspects).length,'liars',liars,'cards',ev.length,'stmts',stIds.size);
}
console.log('problems',bad);
