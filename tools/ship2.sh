# ship2.sh caseN caseid bgkey icons caseIndex  -> wire art, rebuild packs, test, write /tmp/pubfinal_caseN.json (+ /tmp/remove_caseN.json)
set -e
python3 /home/claude/wire.py $1 $2 $3 $4 >/dev/null
python3 /home/claude/build_packs.py $1 icons
cp /mnt/user-data/outputs/app4/index.html /tmp/app4p/index.html; rm -f /tmp/app4p/assets/packs/*; cp /mnt/user-data/outputs/webp/packs/*.json /tmp/app4p/assets/packs/; cp /mnt/user-data/outputs/webp/manifest.json /tmp/app4p/assets/
node /tmp/tcase.js $5
O=/mnt/user-data/outputs/pub_$1; rm -rf $O && mkdir -p $O/assets/packs
cp /mnt/user-data/outputs/app4/index.html $O/ && cp /mnt/user-data/outputs/webp/manifest.json $O/assets/
python3 -c "
import json,shutil
new=json.load(open('/tmp/packs_new.json')); out=[{'as':'index.html','path':'$O/index.html'},{'as':'assets/manifest.json','path':'$O/assets/manifest.json'}]
for f in new: shutil.copy('/mnt/user-data/outputs/webp/'+f,'$O/assets/'+f); out.append({'as':'assets/'+f,'path':'$O/assets/'+f})
json.dump(out,open('/tmp/pubfinal_$1.json','w')); json.dump(['assets/'+f for f in json.load(open('/tmp/packs_removed.json'))],open('/tmp/remove_$1.json','w'))
print('publish',len(out),'remove',json.load(open('/tmp/remove_$1.json')))"
sleep 2
