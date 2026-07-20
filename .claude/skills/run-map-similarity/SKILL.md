---
name: run-map-similarity
description: Build, run, screenshot, and drive the city-similarity map (map_similarity_claude). Use when asked to run this project, rebuild the page, take a screenshot of the map, switch the layout (MDS/PCA/t-SNE/UMAP), move the cutoff slider, pin a city, or verify a change to build_combined.py / combined_template.html.
---

This project renders **one self-contained interactive HTML page**
(`docs/index.html`) — a world map of 124 cities laid out by word2vec similarity,
with three linked views (geographic network, semantic map, clustered matrix), a
shared cutoff slider, a layout switcher, and a click-to-pin city drawer. All data
is **inlined** in the page (no external fetches), so `file://` works and no web
server is needed to view it.

Drive it with the committed driver
**`.claude/skills/run-map-similarity/driver.py`**, which uses the installed
Google Chrome in headless mode to build the page and screenshot it in any
interaction state. All paths below are relative to the repo root
`map_similarity_claude/`; run every command from there.

> Environment note: verified on **macOS** (Chrome at
> `/Applications/Google Chrome.app`), Python 3.11 via a `uv` venv. The driver
> also falls back to `chromium`/`google-chrome` on PATH.

## Prerequisites

- **Google Chrome** (or Chromium) — the driver's screenshot/DOM engine.
- **Python 3.11** in `.venv` with the pinned deps. The venv is committed-adjacent;
  create it on a fresh clone with `uv`:

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

You do **not** need the 1.74 GB word2vec model to run or rebuild the page — all
intermediate outputs (`data/*.csv`, `data/city_vectors.npy`, `output/layouts.json`,
`data/ne_110m_land.geojson`) are committed. The model is only for regenerating
vectors from scratch (see *Full pipeline* below — not exercised here).

## Run (agent path) — the driver

The page is prebuilt at `docs/index.html`, but rebuild it after any change to
`build_combined.py` or `combined_template.html`:

```bash
.venv/bin/python .claude/skills/run-map-similarity/driver.py build
```

Screenshot the whole page (auto-measures height — the page is ~13 000 px tall):

```bash
.venv/bin/python .claude/skills/run-map-similarity/driver.py shot /tmp/map.png
```

Screenshot a **specific interaction state** — layout, cutoff, and a pinned city
(this drives the page's real event handlers, then captures):

```bash
.venv/bin/python .claude/skills/run-map-similarity/driver.py shot /tmp/dubai.png \
  --layout UMAP --cutoff 0.65 --pin Dubai
```

- `--layout` ∈ `MDS` `PCA` `t-SNE` `UMAP`
- `--cutoff` a float in **0.30–0.86** (slider default 0.50)
- `--pin` an exact city name (e.g. `Dubai`, `Lisbon`, `Sydney`) — opens the side
  drawer with that city's full 123-city similarity ranking.

Then **look at the PNG** (read it) to confirm your change rendered.

Fixed top-of-page viewport instead of the full page:

```bash
.venv/bin/python .claude/skills/run-map-similarity/driver.py shot /tmp/top.png --size 1400x900
```

Assert on rendered content without eyeballing (post-JS DOM to stdout):

```bash
.venv/bin/python .claude/skills/run-map-similarity/driver.py dom | grep -c 'Abu Dhabi'
```

### Live click-driving (hover, keyboard, pixel-accurate scrolled views)

The driver's single-shot capture can't do hover previews or mid-page scroll
positions. For those, serve the page and drive it with the Claude Browser MCP:

```bash
.venv/bin/python -m http.server 8731 --directory docs
# then, in the browser tool: navigate to http://localhost:8731/index.html
```

Everything is client-side, so you can inspect/drive state directly, e.g. via the
browser's JS console:

```js
document.getElementById('thr').value = 0.65;                       // cutoff slider
document.getElementById('thr').dispatchEvent(new Event('input', {bubbles:true}));
[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='UMAP').click();
[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='Dubai').click();
```

## Run (human path)

Open `docs/index.html` (or `output/similarity_maps.html`) directly in a browser —
double-click it, no server needed. Useless for an automated agent, which should
use the driver above.

## Full pipeline (documented, not run here — needs the 1.74 GB model)

Only needed to regenerate the embeddings/similarity from scratch. Downloads a
1.74 GB model and streams it once (~2 min). Not exercised in authoring this
skill; the fast rebuild above covers everything downstream of `output/layouts.json`.

```bash
curl -L -o data/word2vec-google-news-300.bin.gz \
  https://github.com/RaRe-Technologies/gensim-data/releases/download/word2vec-google-news-300/word2vec-google-news-300.gz
.venv/bin/python extract_vectors.py   # streams the 1.74 GB model
.venv/bin/python run_mds.py
.venv/bin/python make_layouts.py      # MDS/PCA/UMAP/t-SNE + metrics
.venv/bin/python build_combined.py    # -> docs/index.html
```

## Gotchas

- **`build_combined.py` crashes on a hardcoded scratchpad path.** It writes an
  artifact copy to an absolute `SCRATCH = "/private/tmp/claude-501/.../scratchpad/
  semantic-city-map.html"` baked in from an old session. On any machine where that
  dir doesn't exist, running `build_combined.py` directly dies with
  `FileNotFoundError` *after* it has already written `docs/index.html`. The driver's
  `build` command works around this by recreating that dir first — **always build
  via the driver**, or `mkdir -p` the path yourself. (Better long-term: make that
  write relative / defensive in `build_combined.py`.)
- **Headless Chrome `--screenshot` ignores scroll and only captures the top
  viewport.** A below-the-fold change (e.g. the layout switcher, deep in the
  Explore section ~2 000 px down) is invisible in a default 1400×1000 shot — the
  image is byte-identical to the hero. That's why `shot` defaults to a **full-page**
  capture (measures `document.scrollHeight`, sizes the window to it). Use `--size`
  only when you specifically want the top viewport.
- **The pinned drawer and the scrollspy rail are `position:fixed`.** In a full-page
  shot they render as a full-height strip down the side (the drawer shows the whole
  123-city ranking top-to-bottom). That's expected, not a rendering bug.
- **`.claude/` is otherwise gitignored.** `.gitignore` was changed from `.claude/`
  to `.claude/*` + `!.claude/skills/` so this skill is tracked while
  `settings.local.json` etc. stay ignored. Keep that negation if you touch
  `.gitignore`.
- **The 1.74 GB word2vec model is not committed** (`.gitignore`) — the fast
  rebuild path deliberately doesn't need it.

## Troubleshooting

- **`docs/index.html missing — run driver.py build first`** — you ran `shot`/`dom`
  before `build`, or on a clone where the page wasn't committed. Run
  `driver.py build`.
- **`chrome failed:` / `Google Chrome not found`** — Chrome isn't at the default
  macOS path. Install it, or edit the `CHROME` constant at the top of `driver.py`.
- **A `shot` PNG is ~6 KB / blank** — you passed a small `--size` with a pinned
  city or expected a below-the-fold element; the region wasn't in frame. Drop
  `--size` to get the reliable full-page capture.
- **Build works via driver but crashes when run directly** — that's the hardcoded
  `SCRATCH` path above; use the driver's `build`.
