# usage: python3 build_packs.py [folder ...]   (no args = all folders)
# Packs /mnt/user-data/outputs/webp/<folder>/*.webp into one JSON {path: base64} per folder,
# named with a content hash so phone caches never show stale art. Also builds a small thumbnails pack
# of every background for the case board. Updates manifest.json "packs" and "thumbs".
import sys,os,json,base64,hashlib,io,glob,shutil
from PIL import Image
W='/mnt/user-data/outputs/webp'; P=W+'/packs'; os.makedirs(P,exist_ok=True)
m=json.load(open(W+'/manifest.json')); m.setdefault('packs',{})
folders=sys.argv[1:] or sorted(d for d in os.listdir(W) if os.path.isdir(f'{W}/{d}') and d!='packs')
new=[]; removed=[]
def write(name,obj):
    raw=json.dumps(obj,separators=(',',':')).encode(); h=hashlib.sha1(raw).hexdigest()[:8]
    fn=f'packs/{name}.{h}.json'
    for old in glob.glob(f'{P}/{name}.*.json'):
        if not old.endswith(f'.{h}.json'): removed.append('packs/'+os.path.basename(old)); os.remove(old)
    if not os.path.exists(f'{W}/{fn}'): open(f'{W}/{fn}','wb').write(raw)
    new.append(fn); return fn
for d in folders:
    obj={f'{d}/{f}':base64.b64encode(open(f'{W}/{d}/{f}','rb').read()).decode() for f in sorted(os.listdir(f'{W}/{d}')) if f.endswith('.webp')}
    if obj: m['packs'][d]=write(d,obj)
th={}
for k,p in m['backgrounds'].items():
    im=Image.open(f'{W}/{p}').convert('RGB'); im.thumbnail((400,225)); b=io.BytesIO(); im.save(b,'WEBP',quality=72); th[p]=base64.b64encode(b.getvalue()).decode()
m['thumbs']=write('thumbs',th)
json.dump(m,open(W+'/manifest.json','w'),indent=1)
# mirror into local test site
os.makedirs('/tmp/app4t/assets/packs',exist_ok=True)
for f in new: shutil.copy(f'{W}/{f}',f'/tmp/app4t/assets/{f}')
shutil.copy(W+'/manifest.json','/tmp/app4t/assets/manifest.json')
json.dump(new,open('/tmp/packs_new.json','w')); json.dump(removed,open('/tmp/packs_removed.json','w')); print('packs',len(new),sum(os.path.getsize(f'{W}/{f}') for f in new)//1024,'KB')
