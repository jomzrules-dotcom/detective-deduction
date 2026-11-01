# usage: python3 wire.py case3 wallet cafe icon1,icon2  -> converts staged PNGs to WebP, updates manifest, writes publish/commit lists
import sys,os,json,glob
from PIL import Image
case,cid,bgkey,icons=sys.argv[1],sys.argv[2],sys.argv[3],[i for i in sys.argv[4].split(',') if i]
src='/mnt/user-data/uploads/Colab/detective-deduction/dd1/assets'; out='/mnt/user-data/outputs/webp'
os.makedirs(f'{out}/{case}',exist_ok=True)
m=json.load(open(f'{out}/manifest.json')); files=[]
def conv(rel):
    dst=rel[:-4]+'.webp'; Image.open(f'{src}/{rel}').save(f'{out}/{dst}','WEBP',quality=86,method=6); files.append(dst); return dst
for p in sorted(glob.glob(f'{src}/{case}/*.png')):
    rel=p[len(src)+1:]; name=os.path.basename(p)[:-4]
    if name=='bg': m['backgrounds'][bgkey]=conv(rel); continue
    who,kind=name.split('_',1)
    key=f'{cid}/{who}'
    if kind.startswith('full'):
        mood='nervous' if kind=='full_nervous' else 'neutral'; m['figures'].setdefault(key,{})[mood]=conv(rel)
    else:
        mood={'bust':'neutral'}.get(kind,kind.replace('bust_','')); m['portraits'].setdefault(key,{})[mood]=conv(rel)
for i in icons:
    if os.path.exists(f'{src}/icons/{i}.png'): m['icons'][i]=conv(f'icons/{i}.png')
json.dump(m,open(f'{out}/manifest.json','w'),indent=1)
pub=[{'as':'index.html','path':'/mnt/user-data/outputs/app4/index.html'},{'as':'assets/manifest.json','path':f'{out}/manifest.json'}]+[{'as':'assets/'+f,'path':f'{out}/{f}'} for f in files]
com=[{'stagedPath':'/mnt/user-data/outputs/app4/index.html','devicePath':'C:\\Users\\SS\\Desktop\\Colab\\detective-deduction\\dd1\\index.html'},{'stagedPath':f'{out}/manifest.json','devicePath':'C:\\Users\\SS\\Desktop\\Colab\\detective-deduction\\dd1\\assets\\manifest.json'}]+[{'stagedPath':f'{out}/{f}','devicePath':'C:\\Users\\SS\\Desktop\\Colab\\detective-deduction\\dd1\\assets\\'+f.replace('/','\\')} for f in files]
json.dump(pub,open(f'/tmp/pub_{case}.json','w')); json.dump(com,open(f'/tmp/com_{case}.json','w'))
# copy into the local test site
import shutil
for f in files: os.makedirs(os.path.dirname(f'/tmp/app4t/assets/{f}'),exist_ok=True); shutil.copy(f'{out}/{f}',f'/tmp/app4t/assets/{f}')
shutil.copy(f'{out}/manifest.json','/tmp/app4t/assets/manifest.json'); shutil.copy('/mnt/user-data/outputs/app4/index.html','/tmp/app4t/index.html')
print(case,'files',len(files),'figures',sum(1 for k in m['figures'] if k.startswith(cid+'/')),'portraits',sum(len(v) for k,v in m['portraits'].items() if k.startswith(cid+'/')))
