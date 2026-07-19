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
| 6. Layout variants | [make_layouts.py](make_layouts.py) | `output/layouts.json` — MDS + UMAP + t-SNE, geo-aligned, with metrics |
| 7. Combined page | [build_combined.py](build_combined.py) | `output/similarity_maps.html`, `docs/index.html` — both views, layout switcher, shared cutoff slider, click-to-pin city drawer |

Supporting study: [dissim_study.py](dissim_study.py) — empirical comparison of
similarity→dissimilarity transforms (see below).

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
5. **Dissimilarity: why `d = 1 − cos`.** Three monotone transforms were
   compared empirically with identical SMACOF runs ([dissim_study.py](dissim_study.py)):

   | transform | stress-1 | recall@10 | Spearman r | layout Δ vs 1−cos |
   |---|---|---|---|---|
   | `1 − cos` | **0.347** | **0.515** | **0.709** | — |
   | `√(2(1−cos))` (chord, metric) | 0.392 | 0.505 | 0.687 | 0.005 |
   | `arccos(cos)` (angle, metric) | 0.384 | 0.511 | 0.692 | 0.003 |

   The textbook objection — `1 − cos` is only a semi-metric — is empirically
   empty here: **0 triangle-inequality violations in 200,000 sampled triples**
   (similarities top out at 0.86, far from the violation regime). It also fits
   its target best, preserves the cosine ranking best, and all three layouts
   are nearly identical anyway (Procrustes disparity ≤ 0.005). The chord would
   be the safer default for datasets with near-duplicates; here the simplest
   transform wins. (Being monotone in each other, all three would give an
   *identical* nonmetric MDS.)
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
9. **Layout alternatives (UMAP, t-SNE).** Computed on the same vectors with
   cosine distance ([make_layouts.py](make_layouts.py)), geo-aligned by the
   same Procrustes step, switchable on the page. They answer a different
   question: neighbourhood preservation recall@10 rises from 0.52 (MDS) to
   0.70 (UMAP, n_neighbors 15) / 0.71 (t-SNE, perplexity 20), but distances
   *between* clusters stop meaning anything — so MDS, the only
   distance-faithful method, stays the default view.
10. **Beyond word2vec.** Kept deliberately as the canonical teaching model
    with ready phrase tokens and instructive quirks. Cleaner alternatives:
    **Wikipedia2Vec** (entity vectors — solves name collisions like
    Santiago/Hyderabad outright), **fastText** (subword information),
    **GloVe** (global co-occurrence counts), modern **sentence/LLM
    embeddings** of city descriptions. Swapping the embedding changes step 1
    only; the rest of the pipeline is unchanged.
11. **Limitations.** 2013-era corpus (coverage of that period); a token
    conflates every sense of its string (Treaty-of-Lisbon vs Lisbon;
    `Santiago` and `Hyderabad` name several cities); news salience, not
    geography, drives similarity; Mexico City is a two-token composition
    rather than a native token; map links are straight lines, not
    great-circle arcs, and equirectangular inflates high latitudes.

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
.venv/bin/python make_layouts.py       # MDS/UMAP/t-SNE layouts + metrics
.venv/bin/python build_combined.py     # combined interactive page (docs/)
```
