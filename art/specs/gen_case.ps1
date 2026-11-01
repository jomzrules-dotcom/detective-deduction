# Detective Deduction - paints one whole case from a spec file (case<N>.json), in 3 phases:
#   1) background, full-body sheets (neutral, nervous), object portraits, new evidence icons
#   2) waist-up sheets, each painted FROM that character's full-body sheet (attached as reference)
#   3) only the extra moods the case's mood script uses, each painted FROM the waist-up sheet
# Then cuts everything into dd1/assets/<case>/ and dd1/assets/icons/. Resumable: existing paintings are kept.
#   & gen_case.ps1 -Spec case3.json
param([string]$Spec)
$ErrorActionPreference = 'Continue'
$out = $PSScriptRoot
. "$out\codex_progress.ps1"
$sp = Get-Content (Join-Path $out $Spec) -Raw | ConvertFrom-Json
$C = $sp.case
$S = 'flat vector cartoon style for a friendly mobile detective game, simple clean shapes, thick dark outlines in a darker shade of each colour, soft cel shading with one shadow tone, bright but not neon colours, no text, no letters, no numbers, no watermark.'
$BG = ' The whole lower half of the picture is EMPTY open floor, wide open space where six or seven people will stand side by side in a line. Nothing in the foreground: no objects, furniture, plants or people in the bottom third of the picture. Camera far back at the eye level of a standing child. ' + $S
$FB = 'full body, standing straight and facing the viewer, feet and shoes visible, arms relaxed at the sides, centred, same pose in every frame, on a perfectly flat solid magenta (#FF00FF) background with no shadow and no ground, '
$M2 = 'Exactly 2 frames in one single row with a very wide magenta gap between them, both the same size and height: frame 1 neutral with a small calm smile; frame 2 nervous with raised slanted eyebrows, a small frown and one sweat drop by the temple. '
$MOOD = @{ happy = 'happy: a big open smile, eyes curved happily, one hand slightly raised in a little wave'; sad = 'sad: eyes looking down, eyebrows tilted up in the middle, a small downturned mouth, shoulders dropped'; thinking = 'thinking: one hand on the chin, eyes looking up to one side, mouth a small flat line' }
$gen = "$env:USERPROFILE\.codex\generated_images"
function Paint($jobs, $label) {
  $names = @($jobs.Keys | Where-Object { -not (Test-Path "$out\$_.png") })
  if (-not $names.Count) { return }
  Start-CodexRun "gen_case $C $label" $names
  $running = @()
  foreach ($name in $names) {
    while (($running | Where-Object { $_.State -eq 'Running' }).Count -ge 3) { Start-Sleep -Seconds 3 }
    Set-CodexBatch @(($running | Where-Object { $_.State -eq 'Running' } | ForEach-Object { $_.Name }) + $name)
    $ref = $jobs[$name][1]
    $p = 'Generate exactly one image with your image generation tool, then stop. Do not write code or files. '
    if ($ref) { $p += 'Use the attached image as the reference. ' }
    $p += 'Image: ' + $jobs[$name][0]
    $running += Start-Job -Name $name -ArgumentList $p, "$out\$name.log", $(if ($ref) { "$out\$ref" } else { '' }) -ScriptBlock {
      param($p, $log, $img) if ($img) { codex exec --skip-git-repo-check $p --image $img *> $log } else { codex exec --skip-git-repo-check $p *> $log } }
  }
  $running | Wait-Job | Out-Null
  $dirs = Get-ChildItem $gen -Directory
  foreach ($name in $names) {
    $log = Get-Content "$out\$name.log" -Raw
    $d = $dirs | Where-Object { $log -match [regex]::Escape($_.Name) } | Select-Object -First 1
    if ($d) { $f = Get-ChildItem $d.FullName -File -Filter *.png | Sort-Object LastWriteTime -Descending | Select-Object -First 1; Copy-Item $f.FullName "$out\$name.png" -Force; "$name -> ok"; Add-CodexResult $name $true }
    else { "$name -> no image found"; Add-CodexResult $name $false 'no image in log' }
  }
  Stop-CodexRun
}
# ---------- phase 1 ----------
$j1 = [ordered]@{}
if ($sp.bg) { $j1["${C}_bg"] = @($sp.bg + $BG, $null) }
foreach ($ch in $sp.chars) {
  if ($ch.object) { $j1["${C}_ob_$($ch.id)"] = @("A single $($ch.desc), drawn as a friendly cartoon object with a tiny happy face, front view, centred, on a perfectly flat solid magenta (#FF00FF) background with no shadow and no ground. $S", $null) }
  else { $j1["${C}_fb_$($ch.id)"] = @("A character sheet of $($ch.desc), $FB $M2 $S", $null) }
}
if ($sp.icons.Count) {
  $list = ($sp.icons | ForEach-Object -Begin { $i = 0 } -Process { $i++; "$i) $($_.desc)" }) -join ', '
  $j1["${C}_icons"] = @("A sprite sheet of exactly $($sp.icons.Count) evidence icons in one single row with very wide magenta gaps between them, all the same size, each a single simple object on a perfectly flat solid magenta (#FF00FF) background with no shadow: $list. $S", $null)
}
Paint $j1 'phase 1'
# ---------- phase 2 ----------
$j2 = [ordered]@{}
foreach ($ch in $sp.chars) { if (-not $ch.object) {
  $j2["${C}_ch_$($ch.id)"] = @("A character sheet of exactly the same person as the left figure in the attached image (same face, same skin tone, same hair, same clothes), drawn from the waist up, larger and closer, facing the viewer, centred, same pose in both frames, on a perfectly flat solid magenta (#FF00FF) background with no shadow and no ground. $M2 $S", "${C}_fb_$($ch.id).png") } }
Paint $j2 'phase 2'
# ---------- phase 3 ----------
$j3 = [ordered]@{}
foreach ($ch in $sp.chars) {
  $moods = @($ch.moods | Where-Object { $_ -and $_ -ne 'neutral' -and $_ -ne 'nervous' })
  if ($ch.object -or -not $moods.Count) { continue }
  $n = $moods.Count
  $frames = ($moods | ForEach-Object -Begin { $i = 0 } -Process { $i++; "frame ${i}: $($MOOD[$_])" }) -join '; '
  $row = if ($n -eq 1) { 'Exactly 1 figure, centred.' } else { "Exactly $n frames in one single row with a very wide magenta gap between them, all the same size and height." }
  $j3["${C}_md_$($ch.id)"] = @("A character sheet of exactly the same person as the left figure in the attached image (same face, same skin tone, same hair, same clothes, same size and framing), drawn from the waist up, facing the viewer, centred, on a perfectly flat solid magenta (#FF00FF) background with no shadow and no ground. $row $frames. $S", "${C}_ch_$($ch.id).png")
}
Paint $j3 'phase 3'
# ---------- cut ----------
Add-Type -Path "$out\ArtTool.cs" -ReferencedAssemblies System.Drawing
$a = (Resolve-Path "$out\..\..\assets").Path
New-Item -ItemType Directory -Force "$a\$C", "$a\icons" | Out-Null
$tmp = "$env:TEMP\dd_cut_$C"; New-Item -ItemType Directory -Force $tmp | Out-Null
function Cut2($src, $h, $dstA, $dstB) {
  Get-ChildItem $tmp -File | Remove-Item
  $r = [ArtTool]::FramesBand($src, "$tmp\f_", 2, $h, 256, 40)
  if ($r -like 'found*' -or $r -like 'only*') { return "$r (not cut)" }
  Copy-Item "$tmp\f_0.png" $dstA -Force; Copy-Item "$tmp\f_1.png" $dstB -Force; $r
}
if (Test-Path "$out\${C}_bg.png") { "bg -> " + [ArtTool]::Fit("$out\${C}_bg.png", "$a\$C\bg.png", 1600, 900, 256) }
foreach ($ch in $sp.chars) {
  $id = $ch.id
  if ($ch.object) {
    if (Test-Path "$out\${C}_ob_$id.png") { "$id object -> " + [ArtTool]::Sprite("$out\${C}_ob_$id.png", "$a\$C\${id}_full.png", 700, 256); Copy-Item "$a\$C\${id}_full.png" "$a\$C\${id}_bust.png" -Force }
    continue
  }
  if (Test-Path "$out\${C}_fb_$id.png") { "$id full -> " + (Cut2 "$out\${C}_fb_$id.png" 960 "$a\$C\${id}_full.png" "$a\$C\${id}_full_nervous.png") }
  if (Test-Path "$out\${C}_ch_$id.png") { "$id bust -> " + (Cut2 "$out\${C}_ch_$id.png" 1000 "$a\$C\${id}_bust.png" "$a\$C\${id}_bust_nervous.png") }
  $moods = @($ch.moods | Where-Object { $_ -and $_ -ne 'neutral' -and $_ -ne 'nervous' })
  if ($moods.Count -and (Test-Path "$out\${C}_md_$id.png")) {
    Get-ChildItem $tmp -File | Remove-Item
    if ($moods.Count -eq 1) { $r = [ArtTool]::Sprite("$out\${C}_md_$id.png", "$tmp\f_0.png", 1000, 256) } else { $r = [ArtTool]::FramesBand("$out\${C}_md_$id.png", "$tmp\f_", $moods.Count, 1000, 256, 40) }
    if ($r -like 'found*' -or $r -like 'only*') { "$id moods -> $r (not cut)" }
    else { for ($i = 0; $i -lt $moods.Count; $i++) { Copy-Item "$tmp\f_$i.png" "$a\$C\${id}_bust_$($moods[$i]).png" -Force }; "$id moods -> $r" }
  }
}
if ($sp.icons.Count -and (Test-Path "$out\${C}_icons.png")) {
  Get-ChildItem $tmp -File | Remove-Item
  $isz = if ($sp.iconSize) { [int]$sp.iconSize } else { 128 }
  "icons -> " + [ArtTool]::Frames("$out\${C}_icons.png", "$tmp\i_", $sp.icons.Count, $isz, 256)
  for ($i = 0; $i -lt $sp.icons.Count; $i++) { if (Test-Path "$tmp\i_$i.png") { Copy-Item "$tmp\i_$i.png" "$a\icons\$($sp.icons[$i].name).png" -Force } }
}
"$C done"
