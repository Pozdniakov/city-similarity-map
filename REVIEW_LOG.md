# Review & revision log — city-similarity-map

Running log of reviewer findings and fixes. Newest phases at the bottom.

## Phase 0 — user feedback + attached novelty review (this round)

Editorial / content:
- [x] Novelty framing reworked: dropped "demonstration, not a discovery" and
      "faithful, transparent replication"; RELATED WORK rewritten as an actual
      literature review + modest, specific "what this adds".
- [x] Reproducibility paragraph: dropped seed prose and "it's all in the repo";
      kept tools + versions, added repo link.
- [x] Removed "a teaching demo by".
- [x] orthogonal Procrustes: added gloss + Schönemann (1966) reference + link.
- [x] Edge-count-vs-cutoff list → inline SVG chart.
- [x] Removed the self-describing "step-by-step build; token resolution; geo-fidelity" list.

Substantive (from the novelty review):
- [x] geo-fidelity CEILING computed: raw 300-d cosine distance vs great-circle
      Spearman rho = 0.503. ALL four 2-D layouts (.57-.67) exceed it — the
      reductions concentrate geography (denoising). Added to methodology + RELATED WORK.
- [x] Ranking robustness: t-SNE spans ~.63-.73 (perplexity/seed), UMAP ~.51-.67.
      Exact t-SNE/UMAP order is NOT stable — reframed as "neighbourhood >= linear >= raw".
- New refs: Konkol 2017 (already), Recchia & Louwerse 2014, Louwerse & Benesh 2012,
  Schönemann 1966 (Procrustes).

Layout:
- [ ] Desktop + mobile pass (user reports it opens badly on both).

## Phase 1+ — multi-agent reviewer loop (below)

## Round 1 (workflow wf_99f9cea5) — citations lens (only lens that completed)
- [x] MED: orphan ref Liétard 2021 — added in-text cite in Related-work LLM sentence.
- [x] MED: refs out of order (Kruskal before Konkol) — swapped so Ko < Kr.
- [x] LOW: McInnes cited two ways — JS UMAP note now 'McInnes et al., 2018' to match.
- [x] LOW: combined (Kruskal 1964; Borg & Groenen 2005) both linked #ref-kruskal — split anchors.
- facts/grammar/clarity/consistency lenses FAILED (stalls/API) — re-running lighter.

## Round 1b (wf_89fa9fd9) — facts+consistency CLEAN; grammar 6, clarity 4 (all fixed)
Grammar: cosines run/pushed tense; coloring->colouring; Firth curly->straight quotes;
artifact->artefact; fully-documented->fully documented; ambiguous "it is used"->"each name is used".
Clarity: card 4 wrongly lumped PCA with t-SNE/UMAP (fixed, split out); "What to notice"
UMAP>MDS overclaim reframed to "projections beat raw .50 ceiling, ordering seed-dependent";
Louwerse/Barenholtz duplication in methodology item 1 compressed to a pointer;
Procrustes glossed + step-9 ref on first use in item 8.

## Round 2 (grammar+consistency CLEAN; 1 fact, 4 citations, 3 clarity — all fixed)
Facts:
- [x] Dubai "What to notice" bullet was wrong (claimed Karachi/Mumbai "just behind",
      Doha over Jeddah). Verified true ranks: Abu Dhabi .79, Jeddah .57, Doha .57,
      Riyadh .53, Singapore .49, KL .48, Amman .48, Karachi(8) .44, Mumbai(10) .43.
      Rewritten to match ("Gulf city first… top ten reaches into SE/South Asia").
Citations (APA form):
- [x] (Bar-Joseph, Gifford, & Jaakkola, 2001) -> (Bar-Joseph et al., 2001).
- [x] (Bojanowski, Grave, Joulin, & Mikolov, 2017) -> (Bojanowski et al., 2017).
- [x] (Pennington, Socher, & Manning, 2014) -> (Pennington et al., 2014).
- [x] (Kruskal, 1964; Borg & Groenen, 2005) -> alphabetical (Borg & Groenen; Kruskal).
Clarity / consistency:
- [x] "ceiling" mislabel — layouts EXCEED the raw score, so it is a baseline/floor,
      not a ceiling. Renamed all four occurrences (chart label, aria-label,
      "What to notice", Related work) "ceiling" -> "baseline".
- [x] UMAP JS METHOD_NOTE said "best of the four / lands closest" — contradicts the
      seed-dependent framing. Softened to "in the configuration shown… ρ = .67,
      though the t-SNE/UMAP ordering is seed-dependent".
- [x] Methodology item 8 "every 2-D layout beats that ceiling" reworded with
      "which you might expect to be the best a 2-D map could hope to match".

## Geo-fidelity emphasis (user: "про geo-fidelity нужно подробнее + акцентировать
## результат разных layouts где меньше где больше")
- [x] Added a horizontal dot-plot SVG (.gfchart): raw 300-d .50 (hollow, on dashed
      baseline) then MDS .57, PCA .60, t-SNE .64, UMAP .67 — ascending gradient.
- [x] Added .gf-lead paragraph spelling out where the signal is lowest (MDS, barely
      above raw) and highest (UMAP), with the neighbourhood > linear > raw reading
      and the seed ranges. viewBox widened 344->372 so the "geo-fidelity ρ .70"
      axis title is not clipped. Verified desktop + mobile, no h-scroll, no console errors.
