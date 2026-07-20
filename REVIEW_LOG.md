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

## Round 3 (wf_691b965d, 4 lenses) — 2 HIGH, 5 MED, 4 LOW; all fixed
Most findings landed in the just-added geo-fidelity prose. Fixes:
Clarity/consistency (the important ones):
- [x] HIGH: gf-lead "UMAP the most" read as a fixed leaderboard but the seed ranges
      it cites (t-SNE .63-.73, UMAP .51-.67) make t-SNE typically >= UMAP. Rewrote:
      t-SNE/UMAP "effectively tied", UMAP leads only in the seed shown; across seeds
      t-SNE generally matches or beats UMAP (which can dip below PCA).
- [x] HIGH: tier label "linear" + "(MDS, PCA) fit all pairwise distances" was wrong
      (MDS isn't linear; PCA doesn't fit all pairwise dists — contradicts item 8).
      Relabelled the middle tier "global"; MDS = fits every pairwise distance, PCA =
      linear variance projection. "neighbourhood >= linear >= raw" ->
      "neighbourhood >= global >= raw" in BOTH gf-lead and methodology item 8.
- [x] MED: "baseline" overloaded — PCA was "the classical linear baseline" while
      "baseline" elsewhere = the raw .50 floor. PCA note -> "classical linear benchmark".
- [x] MED: seed caveat scoped only to t-SNE/UMAP gap, but UMAP .51 dips below PCA/MDS
      — noted the tier itself can swap; used >= consistently (dropped the stray ">").
- [x] MED: MDS N-S "cannot lift latitude past r ~ .21 ... this 2-D layout" read as a
      universal ceiling but t-SNE gets N-S r=.40. Scoped to "the MDS layout/map" and
      added "t-SNE, for one, reaches north-south r = .40".
- [x] LOW: "concentrates ... by shedding noise dimensions" overclaimed as a law for
      all layouts. Softened to "a plausible reason ... the gain is not guaranteed".
Grammar:
- [x] MED: British spelling — "toward" x3 -> "towards" (Lisbon x2, London x1).
- [x] LOW: "most so the neighbourhood methods" (broken) reworded in item 8.
Citations:
- [x] MED: narrative cites "Louwerse & Zwaan (2009)" and "Gurnee & Tegmark (2024)"
      -> "and" (APA uses & only inside parentheticals).
- [x] LOW: "Konkol et al. established..." (new paragraph) -> added year (2017).
- [~] LOW: "J. R. Firth (1957)" initials — KEPT: it is an epigraph attribution,
      where initials are conventional/acceptable (reviewer conceded this).
Facts:
- [x] LOW: gf-chart dots were ~3px off the tick scale (plotted at true unrounded
      rho). Snapped all dots to x = 119.6 + (rho-.50)*911 so each dot sits exactly
      on its labelled value; moved the dashed baseline onto the .50 gridline and
      dropped the now-redundant solid .50 gridline.

## Round 4 (wf_5f43e777) — CONVERGED: facts/citations/grammar all clean
Only 1 LOW consistency nit: Related-work "reductions concentrate the geographic signal
by discarding noise" stated as fact while the geo-fidelity sections now hedge it.
- [x] Hedged to "plausibly because the reductions shed noise directions and concentrate
      what geographic signal remains".

## User revision round 2 (design + content requests)
- [x] geo-fidelity now EXPLAINED on the page: added a definition paragraph (Spearman rank
      correlation over all 7,626 pairs, on-screen vs great-circle distance; rho=1 exact,
      rho=0 none; Procrustes-invariant) + why raw is only rho~.50 ("a moderate correlation …
      word2vec encodes much more than geography"). Trimmed the duplicate m-legend clause.
- [x] Moved "How geographic is each layout?" (definition + dot-plot + interpretation) BELOW
      the semantic map (was above). Rationale: show the map, then analyse it.
- [x] Related work: removed selective author-name bolding (Louwerse&Zwaan, Konkol) -> none
      bold, consistent.
- [x] Software: added every version (Python 3.11, NumPy 2.4, pandas 3.0, scikit-learn 1.9.0,
      umap-learn 0.5.12, SciPy 1.17.1, matplotlib 3.11, adjustText 1.4, KaTeX 0.16); clarified
      vectors are parsed from the GoogleNews binary by a custom NumPy parser (no gensim);
      explained Natural Earth 110m; named the viz tools (hand-written SVG/canvas + KaTeX).
- [x] Section headings enlarged (group-h 13->17px, teal top rule; sect-h 12->14px; References
      given the group-h treatment) for clearer visual separation of parts.
- [x] Similarity matrix shrunk (cells 8->6px wide, 7px rows, 6.5px names) so it fits desktop
      with NO horizontal scroll (canvas 868px < 882px client).
- [x] Overall column narrowed (wrap 1120->940px) so figures sit closer to the text measure
      (charts ~868 vs text 746, was ~1080). Verified no page h-scroll desktop or mobile.
- [x] Card fixes: angle diagram (card 3) label overlap fixed ("angles from Sydney" caption
      moved to its own line, viewBox 132->148); added spacing under the visuals on cards 2,3,4
      (ex-card padding-bottom 10->16, diagram margin ->12/12, heatcap margin-bottom 10).

## Round 5 (wf_981265c5) — facts+citations clean; 2 copy fixes in the new text
- [x] MED: Software para "the two maps, the network, ..." double-counted the network
      (the network IS one of the two maps). Dropped "the network,".
- [x] LOW: gf-chart aria-label said "raw .50 ... all above the raw baseline" (raw IS
      the baseline). Reworded to "raw 300-d baseline .50; ... every 2-D projection
      above the raw baseline".
Loop converged: facts/citations/grammar clean across two consecutive rounds bar these
two self-introduced nits, now fixed.

## User revision round 3 (design + methodology deep-dive)
Data: ran compute_intervals.py — 12-seed sweep. Corrected the seed story:
  raw .503 · PCA .599 (det.) · MDS .57 (classical init, det.) · t-SNE .644 (PCA-init,
  DETERMINISTIC, sd=0) · UMAP .60–.68 mean .65 sd .02 (shown seed .671). Earlier
  hand-stated ranges (t-SNE .63–.73, UMAP .51–.67, "dip below PCA") were WRONG — removed.
- [x] Figures still too wide: narrowed wrap 940→800; figures now 742 ≈ text 746 (aligned).
      Matrix cells 6→5px to fit (canvas 734 < 742 client), no desktop h-scroll.
- [x] Card 2 spacing: mini-row 12px, #vrows 8/6, heatcap 8/16 margins.
- [x] Removed "(fit: Stress-1 = .347)" from card 4.
- [x] Close-×/slider overlap: root cause was the slider growing full-width (under the
      fixed right panel) once the readout wrapped. Capped .slider flex 1 1 180px,
      max 320px → slider stays left, clears the panel at every desktop width (verified).
- [x] Map labels too far: tightened adjustText (force_pull .4→.9, less repulsion) and
      regenerated layouts — max label displacement now 3.2% of map width (was larger);
      leader-line threshold retuned (24→21) so the ~30 displaced labels get a connector
      (was 108 at threshold 14), opacity .42→.6, width .5→.6.
- [x] Baseline clarity: state it is MEASURED (ρ = .503, hence ≈ .50), not theoretical.
      Rebuilt the dot-plot as a 0-to-1 bar chart (correlation scale) with a UMAP-only
      seed-range whisker; axis "Spearman ρ (0 = no relation, 1 = perfect)".
- [x] Why a projection beats raw: added a full explanation (word2vec distance mixes
      geography with non-geographic variation across 300 axes; a 2-D projection drops
      the noise directions and geography — a large, intrinsically 2-D slice — survives).
- [x] Rewrote the confusing "tendency… tied… dip below PCA" paragraph with the corrected,
      clean story (ordering stable; only UMAP stochastic; t-SNE .64 / UMAP .67 within noise).
      Updated the same numbers in methodology item 8, the "What to notice" finding, and the
      UMAP JS method-note.
- [x] Illustrated geo-fidelity with three real pairs (Madrid–Barcelona 505 km/cos .73 agree;
      Tokyo–Lisbon 11,140 km/cos .23 agree; Lisbon–Madrid 503 km/cos .49 disagree).

## User revision round 4 (matrix squares + label the spread measure)
- [x] Matrix cells square again: CW=RH=6 (were 5x7 non-square). To keep square cells
      readable AND avoid desktop h-scroll, the matrix panel now BREAKS OUT of the 800px
      text column: .cmpanel width min(890px, 100vw-24), centred on the viewport
      (never wider than it). Canvas 858x753, square 6px cells; verified no page h-scroll
      desktop or mobile, no internal scroll on desktop.
- [x] Spread measure labelled explicitly. Chart: added a legend line "UMAP whisker =
      min–max over 12 seeds · others deterministic" + aria-label update. Text: states
      it is the observed min–max range (min .60, max .68, mean .65, SD .02), NOT a
      confidence interval.
- [x] Explained why t-SNE has no whisker: it is deterministic (PCA-init t-SNE gave .644
      on all 12 seeds; PCA and classical-init MDS have no random step). Only UMAP is
      stochastic here.

## Academic peer-review panel — Round 1 (Opus + Sonnet + Haiku, independent, parallel)
wf_e1b23162. All three: submission rigorous; every checkable statistic matches the data.
- [x] HIGH (Sonnet, truth): card-3 angle diagram (#angdemo) drew each arrow at its
      angle to Sydney, so the VISIBLE Melbourne–New York angle was just the difference
      (~41 deg, cos .76) — but the real Mel–NY cosine is .264 (74.7 deg), the LEAST
      similar pair. The diagram inverted the ranking it teaches. Verified from data.
      Fix (kept the Sydney-anchored construction, which is pedagogically correct):
      reworded the lead-in to "each arrow at its real, measured angle to Sydney", and
      added an .ex-note caveat giving the true Mel–NY value (cos .26, ~75 deg) and
      framing the visible gap as a flattening artefact — an honest preview of the MDS
      compression theme.
- [x] MED/LOW (Opus + Sonnet, statistics): Kruskal Stress-1 bands mis-stated
      "(<.05 excellent, >.20 poor)". Kruskal's five-band scale: .025 excellent, .05 good,
      .10 fair, .20 poor. Fixed to "(<.025 excellent, <.05 good, >.20 poor)".
- [x] LOW (Opus, notation): dissimilarity-study table header "Spearman r" -> "Spearman ρ"
      (bare italic r reads as Pearson; ρ used everywhere else).
- [x] LOW (Opus, grammar): "initialised" (lone -ise outlier) -> "initialized". The page
      convention is Oxford British (-ize + -our: colour, neighbour, optimizes, recognizes),
      so -ize is correct and consistent.
- [~] REJECTED (Haiku, grammar): flagged recognizes/prioritize/prioritizes as "American".
      Not applied — the page is consistently Oxford -ize (only "surprising" is -ise, which
      has no -ize form). Changing them would BREAK consistency. Haiku misread the convention.

## User revision round 5 (matrix must fit within the page, not break out)
- [x] Dropped the viewport breakout. Instead widened the page frame: wrap 800 -> 920,
      and capped the reading column (.wrap > *:not(.matrix)) at the text measure (746),
      centred. The matrix section (.sect.matrix) alone takes the fuller 880 width so the
      square 6x6 canvas (858) sits WITHIN the page (never past its edge), centred and
      aligned with the reading column. Verified: all block centres align on the page
      centre; no page h-scroll desktop or mobile; matrix does not internally scroll on
      desktop. Matrix heading + callout kept at reading width.

## Academic peer-review panel — Round 2 (Opus + Sonnet + Haiku)
wf_26339401. Haiku: clean. Two findings:
- [x] HIGH (Sonnet, truth): Card 1 described word2vec's objective as "predict each word
      from the words around it" = CBOW, contradicting the Methodology's own (correct)
      "skip-gram with negative sampling". GoogleNews-vectors-negative300 are skip-gram
      (word -> context). Fixed Card 1 to "predict the words that appear around each word
      (the skip-gram objective)".
- [x] LOW (Opus, statistics): Related-work compared a supervised probe's R² ≈ .8 against
      the unsupervised layouts' ρ ≈ .5–.7 as "far better" — different metrics/scales
      (variance-explained vs rank correlation). Added an explicit note that they are
      different metrics ("a direction, not a subtraction"); attributed R² to Barenholtz (2026).

## Academic peer-review panel — Round 3 (Opus + Sonnet + Haiku) — CONVERGED
wf_3c75f5fa. All three reviewers returned EMPTY findings.
  Opus: "no genuine defects found."
  Sonnet: "sound as-is."
  Haiku: "No defects detected."
Loop complete: three independent models, three rounds; each earlier round caught a real
issue (R1 misleading angle diagram + Kruskal bands; R2 skip-gram/CBOW error), and the
final round is unanimously clean.

## Layout improvements (rec #1 + #2 from the design critique)
- [x] #1 Hero teaser map: added a static faint world map (#heromap) in the header showing
      all 124 cities at their real coordinates, colour-coded by region, with 6 anchor labels
      (Sydney, New York, London, Tokyo, Cairo, Buenos Aires). Reuses the geographic map's
      projection + Natural Earth land. The whole banner links to #explore ("explore the maps ↓").
      Gives the page an immediate visual hook instead of a text-only opening.
- [x] #2 Left-margin section rail (.railnav): fixed, vertically-centred nav in the desktop
      whitespace (How it works / Explore / What to notice / Methodology / Related work /
      References), with a scroll-spy that highlights the section in view (getBoundingClientRect
      vs a 35%-viewport line). Shown only >=1161px (where the margin has room); below that the
      inline hero anchor-nav is used instead (the two no longer double up). Verified: rail clears
      the reading column, scrollspy tracks correctly, no page h-scroll at desktop/tablet/mobile,
      no console errors, theme-aware.

## Academic peer-review panel — Round 4 (Opus + Sonnet + Haiku) — after hero + rail
wf_2c129996. Haiku: clean. Two LOW findings, both fixed:
- [x] LOW (Opus, clarity): the dissimilarity-transform table's "Spearman ρ" column
      (.709 for 1-cos MDS = the dissimilarity<->2-D-distance fit) shares the label
      "Spearman ρ" with the headline geo-fidelity metric (.57 for MDS), which could be
      misread as a contradictory geo-fidelity value. Renamed the column header to
      "fit ρ (d <-> 2-D)".
- [x] LOW (Sonnet, statistics): "SD .02" was non-italic; APA italicises SD/M/N/r.
      Wrapped it: "<i>SD</i> .02" (matches the page's italic r, M elsewhere).
The hero teaser map and section rail added no content issues.

## Academic peer-review panel — Round 5 (Opus + Sonnet + Haiku)
wf_8a0101df. Haiku: clean. Two LOW findings, both fixed:
- [x] LOW (Opus, truth): Software section still called the geo-fidelity figure a
      "dot-plot" — stale after it was redesigned into a bar chart. Changed to "bar chart".
- [x] LOW (Sonnet, citations): References list had Bar-Joseph (2001) before
      Barenholtz (2026); APA letter-by-letter (hyphen ignored) puts "Bare..." before
      "Barj...". Swapped the two entries.

## Academic peer-review panel — Round 6 (Opus + Sonnet + Haiku)
wf_758393b7. Opus clean, Haiku clean. One MED finding, fixed:
- [x] MED (Sonnet, statistics): the static link-count minichart had baked-in numbers
      (3403 @ 0.30, 451 @ 0.50, 10 @ 0.80) that had drifted from the live slider counter,
      which reads DATA.sims and shows 454 @ 0.50, 3413 @ 0.30. Root-fix: the minichart is
      now GENERATED at build time (build_combined.make_minichart) from the same sims the
      slider uses, so its polyline, marker, labels and aria-label can never drift again.
      Verified live counter (454) == chart label (454) at the default cutoff.

## Academic peer-review panel — Round 7 (DEGRADED) + README validation
wf_906eee7f: Haiku ran and returned CLEAN; Opus and Sonnet both FAILED with
"You've hit your weekly limit (resets 10pm Europe/Berlin)" — so the full 3-model
panel cannot run again until the weekly limit resets.

User reported a separate read-only validation (per README) that surfaced real defects
in README.md — a file the page-only panel never reviewed. All fixed:
- [x] HIGH: "UMAP/t-SNE take the seed" (Reproducibility) was misleading — t-SNE is
      deterministic under PCA init; only UMAP varies. Rewritten: PCA, classical-init MDS
      and PCA-init t-SNE deterministic; only UMAP seed-dependent (ρ .60–.68).
- [x] MED: hard order "UMAP .67 > t-SNE .64 > ..." with no seed caveat -> reordered to
      "t-SNE .64 ≈ UMAP .67 > PCA .60 > MDS .57 > raw .50" + the determinism/seed note.
- [x] MED: American spellings amid British — color->colour, neighbors->neighbours,
      toward->towards.
- [x] MED: six citations with no References section -> added a References section
      (8 entries, APA, alphabetical) pulled from the vetted page reference list.
- [x] Also: dropped "demonstration, not a discovery" (a framing the user disliked, still
      in the README) and reframed Related work as lit review + "what this adds"; flagged
      the R²-vs-ρ comparison as different metrics; table header "Spearman r" -> "fit ρ
      (d ↔ 2-D)"; corrected the Dubai claim and the page-structure line.
