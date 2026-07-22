# Could language reconstruct a map of the world?

**Live page: https://pozdniakov.github.io/city-similarity-map/** — deliberately
both a teaching demo and a small standalone investigation: a geographic
similarity network, a semantic map (MDS / PCA / t-SNE / UMAP),
and a clustered similarity matrix, with a shared cutoff slider and per-city drawer.

A word2vec-based "map" of 124 major world cities: pairwise cosine similarity
between city name vectors is converted to dissimilarity and projected to 2-D
with metric multidimensional scaling. Cities cluster by the company they keep
in news text — which recovers the world's broad *regional* structure well
(within-region geography stays blurry; a decomposition on the page shows where
the signal lives), with informative exceptions (Dubai's ties reach from the
Gulf into South Asia, London sits between the US and Europe, Lisbon is pulled
away from Iberia by Treaty-of-Lisbon coverage).

## Pipeline

| Step | Script | Output |
|------|--------|--------|
| 1. City list | [cities.py](cities.py) | 124 cities, 9 regions, vocabulary token candidates |
| 2. Vectors | [extract_vectors.py](extract_vectors.py) | `data/city_vectors.npy`, `data/city_index.csv` |
| 3. Similarity + MDS | [run_mds.py](run_mds.py) | `data/similarity_matrix.csv`, `data/dissimilarity_matrix.csv`, `data/mds_coordinates.csv` |
| 4. Plot (MDS map) | [plot_map.py](plot_map.py) | `output/city_map.png`, `output/city_map.html`, `output/artifact_data.json` |
| 5. Plot (geo network) | [plot_geo_network.py](plot_geo_network.py) | `output/geo_network.png`, `output/geo_network.html`, `output/geo_network_data.json` |
| 6. Layout variants | [make_layouts.py](make_layouts.py) | `output/layouts.json` — MDS + PCA + t-SNE + UMAP, geo-aligned, with metrics |
| 7. Combined page | [build_combined.py](build_combined.py) | `output/similarity_maps.html`, `docs/index.html` — all three views, layout switcher, shared cutoff slider, click-to-pin city drawer |

Supporting studies: [dissim_study.py](dissim_study.py) — empirical comparison
of similarity→dissimilarity transforms; [compute_intervals.py](compute_intervals.py)
— seed sweep at the shown configurations plus a separate MDS init-sensitivity
sweep (`output/intervals.json`); [robustness_study.py](robustness_study.py) —
between/within-region decomposition of geo-fidelity, region-collapse
counterfactual, geographic neighbour recall, city-level bootstrap, and the
rotation scan behind the latitude ceiling (`output/robustness.json`).

## Three linked views

The [combined page](https://pozdniakov.github.io/city-similarity-map/) presents
one similarity matrix three ways, with shared state (one cutoff slider, one
selection):

- **Geographic network** ([plot_geo_network.py](plot_geo_network.py)) — cities
  at their *true* longitude/latitude on an equirectangular world map, with an
  edge drawn between any pair whose cosine similarity clears the cutoff (line
  opacity/width ∝ similarity). Slider spans **0.30–0.86**; default **0.50**
  (~450 of 7,626 pairs). A compact Natural Earth 110m land outline
  (`data/ne_110m_land.geojson`) is embedded, so no external map tiles.
- **Semantic map** ([plot_map.py](plot_map.py), [make_layouts.py](make_layouts.py))
  — cities placed by dimensionality reduction, so *distance itself* encodes
  dissimilarity; switchable between MDS / PCA / t-SNE / UMAP, each rotated onto
  real geography (Method step 8, layout alternatives).
- **Clustered similarity matrix** — the full 124×124 matrix, rows/columns
  seriated by hierarchical clustering, dendrogram + region-coloured names down
  the left edge.

The page ([build_combined.py](build_combined.py) → `output/similarity_maps.html`,
`docs/index.html`) is structured as **question → How it works (4 cards) →
Explore (the three views) → What to notice → Methodology → Related work →
References**, with anchor navigation. Hovering a city previews its top-5 neighbours on both maps; clicking
pins it and opens a side drawer ranking all 123 others. Ships the full
7,626-pair similarity array inline, so every list is computed live.

## Related work

Recovering a recognizable map from text-only co-occurrence is a robust,
long-established result. Louwerse and Zwaan (2009) recovered US-city coordinates
via LSA + MDS (linking it to Tobler's law; Tobler, 1970); Konkol et al. (2017) fit
word-embedding city vectors to real coordinates as a benchmark; Liétard et al.
(2021), and for LLMs Gurnee and Tegmark (2024) and Godey et al. (2024), found
hidden states linearly encode coordinates (improving with scale but staying
geographically unequal); Barenholtz (2026) showed plain word2vec/GloVe carry the
same signal, riding on lexical directions (country/climate words) — the map is
*inherited* from how places are described.

What this adds is small and specific: a transparent, interactive build with
fully disclosed token-resolution calls, an exhaustive triangle-inequality audit
of `1 − cos` (all 310,124 triples; a check of this dataset, not a general
result), and an alignment-free geo-fidelity metric compared *across
projections* rather than across embeddings — with a decomposition showing that
the layouts' advantage over the raw space lives almost entirely in
between-region structure (within regions the raw space ties the best layout,
and collapsing any layout to nine region points *raises* its score — a lift
that survives label-free controls: data-driven dendrogram clusters lift scores
the same way, k-means on true coordinates lifts them higher, and random
groupings of the same sizes crash them to ρ ≈ .03). It also
shows the gap the literature predicts: a *supervised* probe that regresses
coordinates recovers geography far better (R² ≈ .8, reported in a preprint;
Barenholtz, 2026) than these *unsupervised* layouts do (geo-fidelity
ρ ≈ .57–.67). Those two figures are different metrics on different scales
(variance-explained vs rank correlation), so read the gap as a direction, not
a subtraction — either way, the result is a map of *discourse* more than of
the Earth: a sharp map of the world's regions, a blurry map inside them.

## Method

1. **Embedding model.** GoogleNews-vectors-negative300: word2vec (skip-gram
   with negative sampling) trained on ~100B words of Google News text
   (circa 2013); 3M-token vocabulary, 300 dimensions, frequent multiword
   phrases merged into single tokens (`New_York`, `Buenos_Aires`). Downloaded
   from the [gensim-data release](https://github.com/RaRe-Technologies/gensim-data/releases/tag/word2vec-google-news-300)
   to `data/word2vec-google-news-300.bin.gz` (1.74 GB, not committed). Under
   the distributional hypothesis, cities mentioned in similar news contexts
   get similar vectors. No geography enters the similarity computation or the
   layout — it is used only for the final rigid orientation (step 9,
   orientation).
2. **City list.** 124 cities curated by hand (metro population roughly >1M plus
   global prominence), balanced across 9 regions. Region labels are only used
   to colour the plot; they play no role in the computation.
3. **Token resolution.** Per city, an ordered candidate list (explicit
   overrides, then the underscored display name and a diacritics-stripped
   variant). `extract_vectors.py` stream-parses the gzipped binary in one pass
   (no gensim, no 3.6 GB in RAM) and matches candidates byte-exactly against
   all 3M vocabulary entries; first present candidate wins. Absences were
   verified by full-vocabulary scans, and ambiguous tokens tested empirically
   (see notes below).
4. **Similarity.** Vectors L2-normalized; full 124×124 cosine-similarity
   matrix (7,626 unique pairs). Observed range −.06 (Houston–Lisbon) to .86
   (Sydney–Melbourne), mean .30.
5. **Dissimilarity: why `d = 1 − cos`.** Three monotone transforms were
   compared empirically with identical SMACOF runs ([dissim_study.py](dissim_study.py)):

   | transform | stress-1 | recall@10 | fit ρ (d ↔ 2-D) | layout Δ vs 1−cos |
   |---|---|---|---|---|
   | `1 − cos` | **.347** | **.515** | **.709** | — |
   | `√(2(1−cos))` (chord, metric) | .392 | .505 | .687 | .005 |
   | `arccos(cos)` (angle, metric) | .384 | .511 | .692 | .003 |

   The textbook objection — `1 − cos` is only a semi-metric — is nearly moot
   here: enumerating **all C(124,3) = 310,124 triples**, exactly **2** violate
   the triangle inequality, by a largest excess of .023 (negligible for SMACOF).
   `1 − cos` also fits its target best, preserves the global cosine ranking
   (Spearman ρ) and top-10 neighbourhoods best, and
   all three layouts are nearly identical anyway (Procrustes disparity ≤ .005).
   The chord would be the safer default for datasets with near-duplicates; here
   the simplest transform wins. (Being monotone in each other, all three would
   give an *identical* nonmetric MDS.)
6. **MDS.** Metric MDS via SMACOF (sklearn 1.9), precomputed dissimilarities,
   2 components, classical-MDS (Torgerson) init + stress-majorization
   iterations (max 3000, eps 1e-9) — deterministic. Minimizes raw stress
   Σ(d̂ᵢⱼ − dᵢⱼ)².
7. **Fit diagnostics.** Kruskal stress-1 = √(Σ(d̂ᵢⱼ−dᵢⱼ)²/Σdᵢⱼ²) = **.347**;
   Pearson r between input dissimilarities and 2-D distances **.71**
   (Spearman ρ .71). A heavily compressed fit — expected when flattening
   high-rank 300-d similarity structure into a plane. Cluster membership and
   broad groupings are trustworthy; exact adjacency and fine distance
   differences are not (recall@10 = .52 — read nearest neighbours from the
   similarity ranking, not the map).
8. **Layout alternatives + geographic fidelity.** Four layouts on the same
   vectors/cosine distance ([make_layouts.py](make_layouts.py)), each
   geo-aligned by the same rigid Procrustes step (step 9), switchable on the
   page: **PCA** (linear baseline, recall@10 .41), **MDS** (only method
   optimizing all pairwise distances; default), **t-SNE** and **UMAP**
   (nonlinear, local neighbourhoods; recall@10 .71 / .70). To compare them
   *as maps of the world*, score each by **geo-fidelity** — the alignment-free
   rank correlation between on-screen distances and real great-circle
   distances. Result:
   **t-SNE .64 ≈ UMAP .67 > PCA .60 > MDS .57 > raw 300-d .50** — the
   neighbourhood methods (t-SNE, UMAP) score higher than the global
   ones (PCA, MDS), which in turn beat the un-projected 300-d cosine distances.
   A decomposition ([robustness_study.py](robustness_study.py)) shows where
   that gain lives: 88% of pairs are between-region; *within* regions the raw
   space (.33) ties the best layout; and collapsing any layout to its nine
   region centroids **raises** its score (e.g. UMAP .67 → .72) — so the metric
   mostly rewards regional sorting, and two mechanisms (noise-shedding vs
   cluster quantization, the neighbourhood methods' exaggeration of
   between-cluster separation) are both consistent with the ordering. Only
   UMAP is seed-dependent (ρ .60–.68 over 12 seeds, mean .65); PCA,
   classical-init MDS (verified constant across 12 seeds) and PCA-init t-SNE
   are deterministic, so the t-SNE/UMAP gap sits within that seed noise —
   though SMACOF started from *random* inits instead spans ρ .50–.58
   ([compute_intervals.py](compute_intervals.py)). A 1,000-resample city-level
   bootstrap keeps each layout-minus-raw difference away from zero (95% CIs)
   but not the adjacent layout-vs-layout gaps.
9. **Orientation (geographic).** MDS solutions are unique up to rotation/
   reflection/translation, so the raw axes are meaningless. Rather than an
   arbitrary convention, the configuration is aligned to real geography by
   **orthogonal Procrustes** (`cities.CITY_LATLON`): the rotation + reflection
   best mapping the embedding onto each city's true (longitude, latitude), with
   the two geographic axes standardized so E–W and N–S weigh equally. It is a
   rigid transform — every pairwise distance and the stress are preserved
   exactly; only "which way is up" changes. Afterwards E–W correlates with
   longitude at r = .70 and N–S with latitude at only r = .17. **These axis
   correlations are measured after an alignment that itself uses the real
   coordinates**, so they describe residual correspondence, not unsupervised
   recovery — for an alignment-free measure, see geo-fidelity in step 8.
10. **Beyond word2vec.** Kept deliberately as the canonical teaching model
    with ready phrase tokens and instructive quirks. Cleaner alternatives:
    **Wikipedia2Vec** (entity vectors — solves name collisions like
    Santiago/Hyderabad outright), **fastText** (subword information),
    **GloVe** (global co-occurrence counts), modern **sentence/LLM
    embeddings** of city descriptions. Swapping the embedding changes step 1
    only; the rest of the pipeline is unchanged.
11. **Clustered similarity matrix.** The full 124×124 matrix rendered on the
    page with rows/columns reordered by **agglomerative hierarchical clustering**,
    **average linkage / UPGMA** — `scipy.cluster.hierarchy.linkage(squareform(1 −
    cos), method="average", optimal_ordering=True)`. No cluster count is imposed;
    **optimal leaf ordering** (Bar-Joseph et al., 2001) refines the leaf order,
    and a dendrogram + region-coloured names run down the left edge.

**Reproducibility.** Stochastic steps are seeded (seed 42). PCA is
deterministic; MDS uses a deterministic classical-MDS init + single SMACOF
restart; t-SNE is initialized from PCA rather than a random layout, which makes
it deterministic too (identical geo-fidelity on all 12 seeds tried). Only UMAP
genuinely varies with the seed (geo-fidelity ρ .60–.68). Hyperparameters are in
the scripts; versions are pinned
in [requirements.txt](requirements.txt) (scikit-learn 1.9.0, SciPy 1.17.1,
umap-learn 0.5.12). Supporting analyses ship as runnable scripts:
[dissim_study.py](dissim_study.py) (transform comparison + full triangle
enumeration), [make_layouts.py](make_layouts.py) (layouts + geo-fidelity).

## Vocabulary resolution notes

Verified against the full 3M-token vocabulary:

- `Mexico_City`, `New_York_City`, `New_Delhi`, `Ho_Chi_Minh_City` do **not**
  exist as tokens. New York → `New_York`, Delhi → `Delhi`,
  Ho Chi Minh City → `Saigon`; Mexico City uses the `mean(Mexico, City)`
  composition (`COMPOSE_FALLBACK` in cities.py). The all-caps dateline token
  `MEXICO_CITY` exists and ranks its neighbours more cleanly, but dateline-
  register cosines are uniformly depressed (max 0.44), which makes metric MDS
  exile the city to the periphery; the composition places it correctly beside
  Monterrey and Guadalajara.
- St Petersburg uses `Saint_Petersburg`: the more frequent `St._Petersburg`
  token is dominated by St. Petersburg, *Florida* (cos to Tampa .68 vs
  Moscow .60).
- Kyiv resolves to its own `Kyiv` token even in this 2013-era corpus.

## Run it

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt
curl -L -o data/word2vec-google-news-300.bin.gz \
  https://github.com/RaRe-Technologies/gensim-data/releases/download/word2vec-google-news-300/word2vec-google-news-300.gz
curl -L -o data/ne_110m_land.geojson \
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson
.venv/bin/python extract_vectors.py   # ~2 min: streams the 1.74 GB model once
.venv/bin/python run_mds.py
.venv/bin/python plot_map.py           # semantic (MDS) map
.venv/bin/python plot_geo_network.py   # geographic similarity network
.venv/bin/python make_layouts.py       # MDS/PCA/t-SNE/UMAP layouts + metrics
.venv/bin/python build_combined.py     # combined interactive page (docs/)
.venv/bin/python compute_intervals.py  # seed + MDS-init sensitivity sweeps
.venv/bin/python robustness_study.py   # decomposition, bootstrap, rotation scan
```

## References

- Barenholtz, E. (2026). *World properties without world models: Recovering
  spatial and temporal structure from co-occurrence statistics in static word
  embeddings*. arXiv. https://arxiv.org/abs/2603.04317
- Bar-Joseph, Z., Gifford, D. K., & Jaakkola, T. S. (2001). Fast optimal leaf
  ordering for hierarchical clustering. *Bioinformatics, 17*(Suppl. 1),
  S22–S29. https://doi.org/10.1093/bioinformatics/17.suppl_1.S22
- Godey, N., de la Clergerie, É., & Sagot, B. (2024). *On the scaling laws of
  geographical representation in language models*. arXiv.
  https://arxiv.org/abs/2402.19406
- Gurnee, W., & Tegmark, M. (2024). Language models represent space and time.
  In *International Conference on Learning Representations*.
  https://arxiv.org/abs/2310.02207
- Konkol, M., Brychcín, T., Nykl, M., & Hercig, T. (2017). Geographical
  evaluation of word embeddings. In *Proceedings of the Eighth International
  Joint Conference on Natural Language Processing (Volume 1: Long Papers)*
  (pp. 224–232).
  https://aclanthology.org/I17-1023/
- Liétard, B., Abdou, M., & Søgaard, A. (2021). Do language models know the way
  to Rome? In *Proceedings of the Fourth BlackboxNLP Workshop on Analyzing and
  Interpreting Neural Networks for NLP* (pp. 510–517).
  https://aclanthology.org/2021.blackboxnlp-1.40/
- Louwerse, M. M., & Zwaan, R. A. (2009). Language encodes geographical
  information. *Cognitive Science, 33*(1), 51–73.
  https://doi.org/10.1111/j.1551-6709.2008.01003.x
- Tobler, W. R. (1970). A computer movie simulating urban growth in the Detroit
  region. *Economic Geography, 46*(Suppl.), 234–240.
  https://doi.org/10.2307/143141
