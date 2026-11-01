# gitpush.sh "message"  -> sync the live game build into the GitHub repo and push
set -e
R=/home/claude/dd-repo
cp /mnt/user-data/outputs/app4/index.html /mnt/user-data/outputs/app4/sw.js /mnt/user-data/outputs/app4/manifest.webmanifest $R/docs/
cp /mnt/user-data/outputs/webp/manifest.json $R/docs/assets/manifest.json
rm -f $R/docs/assets/packs/*.json && cp /mnt/user-data/outputs/webp/packs/*.json $R/docs/assets/packs/
cp /tmp/app4p/assets/ui/*.webp $R/docs/assets/ui/ 2>/dev/null || true
cp /mnt/user-data/outputs/app4/assets/ui/*.webp $R/docs/assets/ui/ 2>/dev/null || true
cp /mnt/user-data/outputs/gen/*.json $R/art/specs/
cp /home/claude/build_packs.py /home/claude/wire.py /home/claude/ship2.sh /home/claude/gitpush.sh $R/tools/
cd $R && git add -A
if git diff --cached --quiet; then echo "nothing to push"; exit 0; fi
git -c user.name="jomzrules-dotcom" -c user.email="jomzrules@gmail.com" commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0168xnT4yVrkw3NkwTxGmDWn"
git push -q origin main && git log --oneline -1
