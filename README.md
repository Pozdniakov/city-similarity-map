# Semantic map of world cities

**Live page: https://pozdniakov.github.io/city-similarity-map/** — geographic
similarity network + semantic MDS map, with a cutoff slider and per-city drawer.

A word2vec-based "map" of 124 major world cities: pairwise cosine similarity
between city name vectors is converted to dissimilarity and projected to 2-D
with metric multidimensional scaling. Cities cluster by the company they keep
in news text — which largely reconstructs geography, with informative
exceptions (Dubai leans toward South Asia, London sits between the US and
Europe, Lisbon is pulled away from Iberia by Treaty-of-Lisbon coverage).

## Pipeline

| Step | Script | Output |
|------|--------|--------|
| 1. City list | [cities.py](cities.py) | 124 cities, 9 regions, vocabulary token candidates |
| 2. Vectors | [extract_vectors.py](extract_vectors.py) | `data/city_vectors.npy`, `data/city_index.csv` |
| 3. Similarity + MDS | [run_mds.py](run_mds.py) | `data/similarity_matrix.csv`, `data/dissimilarity_matrix.csv`, `data/mds_coordinates.csv` |
| 4. Plot (MDS map) | [plot_map.py](plot_map.py) | `output/city_map.png`, `output/city_map.html`, `output/artifact_data.json` |
| 5. Plot (geo network) | [plot_geo_network.py](plot_geo_network.py) | `output/geo_network.png`, `output/geo_network.html`, `output/geo_network_data.json` |
| 6. Combined page | [build_combined.py](build_combined.py) | `output/similarity_maps.html` — both views, shared cutoff slider, click-to-pin city drawer |

## Two views

- **Semantic map** ([plot_map.py](plot_map.py)) — cities placed by MDS, so
  *distance itself* encodes dissimilarity; the layout is then rotated onto real
  geography (step 8 below).
- **Geographic network** ([plot_geo_network.py](plot_geo_network.py)) — cities
  at their *true* longitude/latitude on an equirectangular world map, with an
  edge drawn between any pair whose cosine similarity clears a threshold (line
  opacity/width ∝ similarity). The slider spans **0.30–0.86**; the default
  cutoff is **0.50** (451 of 7 626 pairs, avg degree ≈ 7 — dense enough to show
  regional constellations, sparse enough to stay legible). A compact Natural
  Earth 110m land outline (`data/ne_110m_land.geojson`) is simplified and
  embedded so the page needs no external map tiles.
- **Combined page** ([build_combined.py](build_combined.py) →
  `output/similarity_maps.html`) — both views on one page with shared state:
  one cutoff slider drives the network edges and the list split; hovering a
  city previews its top-5 links on *both* charts; clicking pins it and opens a
  side drawer ranking all 123 other cities (region glyph on every row), split
  at the cutoff — links above draw solid, links below draw dashed and faint.
  Ships the full 7 626-pair similarity array inline, so every list is computed
  live.

## Method

1. **Embedding model.** GoogleNews-vectors-negative300: word2vec (skip-gram
   with negative sampling) trained on ~100B words of Google News text
   (circa 2013); 3M-token vocabulary, 300 dimensions, frequent multiword
   phrases merged into single tokens (`New_York`, `Buenos_Aires`). Downloaded
   from the [gensim-data release](https://github.com/RaRe-Technologies/gensim-data/releases/tag/word2vec-google-news-300)
   to `data/word2vec-google-news-300.bin.gz` (1.74 GB, not committed). Under
   the distributional hypothesis, cities mentioned in similar news contexts
   get similar vectors — no geographic information enters the pipeline.
2. **City list.** 124 cities curated by hand (metro population roughly >1M plus
   global prominence), balanced across 9 regions. Region labels are only used
   to color the plot; they play no role in the computation.
3. **Token resolution.** Per city, an ordered candidate list (explicit
   overrides, then the underscored display name and a diacritics-stripped
   variant). `extract_vectors.py` stream-parses the gzipped binary in one pass
   (no gensim, no 3.6 GB in RAM) and matches candidates byte-exactly against
   all 3M vocabulary entries; first present candidate wins. Absences were
   verified by full-vocabulary scans, and ambiguous tokens tested empirically
   (see notes below).
4. **Similarity.** Vectors L2-normalized; full 124×124 cosine-similarity
   matrix (7,626 unique pairs). Observed range −0.06 (Houston–Lisbon) to 0.86
   (Sydney–Melbourne), mean 0.30.
5. **Dissimilarity.** `d = 1 − cos`, zero diagonal, symmetrized. Not
   guaranteed metric (triangle inequality), which SMACOF does not require.
6. **MDS.** Metric MDS via SMACOF (sklearn 1.9), precomputed dissimilarities,
   2 components, classical-MDS (Torgerson) init + stress-majorization
   iterations (max 3000, eps 1e-9) — deterministic. Minimizes raw stress
   Σ(d̂ᵢⱼ − dᵢⱼ)².
7. **Fit diagnostics.** Kruskal stress-1 = √(Σ(d̂ᵢⱼ−dᵢⱼ)²/Σdᵢⱼ²) = **0.347**;
   Pearson r between input dissimilarities and 2-D distances **0.71**
   (Spearman ρ 0.71). A heavily compressed fit — expected when flattening
   high-rank 300-d similarity structure into a plane. Cluster membership and
   adjacency are trustworthy; fine distance differences are not.
8. **Orientation (geographic).** MDS solutions are unique up to rotation/
   reflection/translation, so the raw axes are meaningless. Rather than an
   arbitrary convention, the configuration is aligned to real geography by
   **orthogonal Procrustes** (`cities.CITY_LATLON`): the rotation + reflection
   best mapping the embedding onto each city's true (longitude, latitude), with
   the two geographic axes standardized so E–W and N–S weigh equally. It is a
   rigid transform — every pairwise distance and the stress are preserved
   exactly; only "which way is up" changes. Result: `→` east, `↑` north, with
   E–W correspondence to longitude rising from an arbitrary r = 0.48 to **0.70**
   and N–S flipping right-side-up (r −0.21 → **+0.17**). Latitude stays weak —
   even the best possible rotation cannot exceed r ≈ 0.21, because the semantic
   structure barely encodes north–south (it encodes region/language, which is
   mostly an E–W distinction).
9. **Limitations.** 2013-era corpus (coverage of that period); a token
   conflates every sense of its string (Treaty-of-Lisbon vs Lisbon; `Santiago`
   and `Hyderabad` name several cities); news salience, not geography, drives
   similarity; Mexico City is a two-token composition rather than a native
   token.

## Vocabulary resolution notes

Verified against the full 3M-token vocabulary:

- `Mexico_City`, `New_York_City`, `New_Delhi`, `Ho_Chi_Minh_City` do **not**
  exist as tokens. New York → `New_York`, Delhi → `Delhi`,
  Ho Chi Minh City → `Saigon`; Mexico City uses the `mean(Mexico, City)`
  composition (`COMPOSE_FALLBACK` in cities.py). The all-caps dateline token
  `MEXICO_CITY` exists and ranks its neighbors more cleanly, but dateline-
  register cosines are uniformly depressed (max 0.44), which makes metric MDS
  exile the city to the periphery; the composition places it correctly beside
  Monterrey and Guadalajara.
- St Petersburg uses `Saint_Petersburg`: the more frequent `St._Petersburg`
  token is dominated by St. Petersburg, *Florida* (cos to Tampa 0.68 vs
  Moscow 0.60).
- Kyiv resolves to its own `Kyiv` token even in this 2013-era corpus.

## Run it

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python numpy scipy scikit-learn matplotlib pandas adjustText
curl -L -o data/word2vec-google-news-300.bin.gz \
  https://github.com/RaRe-Technologies/gensim-data/releases/download/word2vec-google-news-300/word2vec-google-news-300.gz
curl -L -o data/ne_110m_land.geojson \
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson
.venv/bin/python extract_vectors.py   # ~2 min: streams the 1.74 GB model once
.venv/bin/python run_mds.py
.venv/bin/python plot_map.py           # semantic (MDS) map
.venv/bin/python plot_geo_network.py   # geographic similarity network
.venv/bin/python build_combined.py     # combined interactive page
```
