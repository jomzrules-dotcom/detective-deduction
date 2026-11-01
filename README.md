# Detective Deduction

A detective game that trains kids' critical thinking. Players interview witnesses to collect evidence cards, mark each suspect statement as **Fact**, **Lie** or **Unknown**, then accuse the culprit and earn up to 3 stars.

Cases come in Case Files of 10. Finishing a file promotes the player (Neighborhood → Town → City Detective, then a stripe per file). Cases unlock one at a time, in order.

| Case File | Cases | Theme |
| --- | --- | --- |
| 1 | 1–10 | The Neighborhood |
| 2 | 11–20 | Town Festival Week |
| 3 | 21–30 | Market Street (art for 26–30 in progress) |

## Play it

The game is a single-page web app in `docs/` (published by GitHub Pages: https://jomzrules-dotcom.github.io/detective-deduction/). Serve that folder with any static server, for example:

```
cd docs
python3 -m http.server 8000
```

Then open http://localhost:8000. It also works as an installable app (landscape, full screen) on phones.

## How it's built

- `docs/index.html`: the whole game (cases, moods, case board, notebook, scoring).
- `docs/assets/packs/`: the art, one pack per case (WebP images inside JSON, hashed file names). The game loads only the packs a case needs.
- `docs/assets/manifest.json`: which images and packs exist.
- `art/specs/caseN.json`: the art brief for each case (backgrounds, characters, moods, icons) that Codex paints from.
- `tools/`: scripts that turn Codex's PNGs into WebP, build the packs and ship a case.
- `tests/`: Playwright checks (every case solvable to 3 stars, data validation, notebook review, unlock order, promotion screen).

All art is painted by Codex from the specs. Cases are written to the rules in the story writer brief.
