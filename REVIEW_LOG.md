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

## README verification (Haiku-only; Opus/Sonnet weekly-limited)
wf_806dbe0b. One MED, fixed:
- [x] MED: "Tobler's law" mentioned without an in-text cite while Tobler (1970) is in
      References -> "(linking it to Tobler's law; Tobler, 1970)".
All numbers, spelling, reference formatting and grammar otherwise verified correct.

## Fable review panel — Round 1 (fable:page FAILED session limit; readme + cross-file ran)
wf_446adb64. Page lens hit a session limit; README and cross-file lenses completed.
All findings verified by hand before applying (the cross-file agent ran without the
safety classifier). 1 MED + 6 LOW, all fixed:
- [x] MED (cross-file, truth): README pipeline table row 6 said "MDS + UMAP + t-SNE",
      omitting PCA — contradicting the README's own step 9, the intro, and the page's
      four-way switcher (make_layouts.py does compute PCA). -> "MDS + PCA + t-SNE + UMAP".
- [x] LOW x2 (grammar): README "recognisable" -> "recognizable", "initialised" ->
      "initialized" (Oxford -ize convention).
- [x] LOW (clarity): thousands separator "7 626" (space, x2) -> "7,626" to match the
      rest of the README and the page.
- [x] LOW (clarity): "(step 9)" in Three linked views reads against the 7-row pipeline
      table -> "(Method, step 9)".
- [x] LOW (citations): page's Louwerse & Benesh (2012) entry linked PubMed; replaced
      with the DOI (10.1111/cogs.12000 — verified via Crossref: exact title/authors/
      volume/pages match).
- [x] LOW (clarity/validity): built page duplicated <meta charset>, <meta viewport>
      and <title> inside <body> (template fragment + build head). build_combined.py now
      strips the fragment's head lines for the standalone build (the artifact copy keeps
      them — the artifact platform reads the <title>). Standalone now has exactly one of
      each; page verified rendering with no console errors.

## Fable review panel — Round 2 (page + readme + cross-file; all three lenses ran)
wf_f9f79483. README: CLEAN. Page: 2 MED + 1 LOW. Cross-file: 3 LOW. All fixed:
- [x] MED (page, truth): "17 embedding models" for Konkol et al. (2017) was WRONG.
      Verified against the published PDF itself (fetched aclanthology I17-1023,
      extracted Table 1): exactly 16 embedding models (GloVe 6B x4, 42B, 840B,
      LexVec x2, MetaEmbeddings, SkipGram x3, FastText, WoRel, LSA, PPMI-SVD) plus
      2 random baselines. The "17" came from the user-supplied lit review; primary
      source wins. -> "16 embedding models".
- [x] MED (page, clarity): "cutoff slider and city search drive all three views at
      once" + "light up ... in all of them" + "light it up in all three views"
      overstated — the matrix ignores the slider/search/selection (verified in code:
      applyThreshold and select() never touch the canvas; the slider label itself
      says "both maps"). Reworded all three to "both maps" (+ note the matrix always
      shows every pair).
- [x] LOW (page): stale comments "Paris / London / Lagos" and "first five real
      numbers of Paris" -> Sydney / Melbourne / New York, Sydney.
- [x] LOW (cross-file, stats): supervised-probe sentence used loose "rho ~ .5-.7"
      vs the measured .57-.67 stated earlier on the page and in the README -> .57-.67.
- [x] LOW (cross-file): README numeric step cross-refs now carry names
      ("step 8, orientation"; "Method step 9, layout alternatives") since page/README
      step numbering differs.
- [x] LOW (cross-file, voice): "all 12 seeds we tried" -> "all 12 seeds tried"
      (single-author page; only "we").

## Fable review panel — Round 3 (all three lenses ran; the earlier "round 3" was a
## full session-limit failure and does not count)
wf_b41d79c9. 2 MED + 5 LOW, all fixed:
- [x] MED (page, statistics): "The order is the same every time ... holds in every
      run" overstated — UMAP's worst seed (.603) sits .004 above PCA (.599), invisible
      at 2 decimals and far inside UMAP's seed SD (.021). Rewrote: deterministic part
      never moves (raw < MDS < PCA < t-SNE); UMAP usually on top; ordering held in all
      12 runs but at its narrowest by .004 — "a strong tendency, not a law".
- [x] MED (cross-file, truth): README "Cluster membership and adjacency are
      trustworthy" contradicted the page (recall@10 .52; "read neighbours from the
      ranking"). -> "broad groupings trustworthy; exact adjacency and fine distances
      not (recall@10 = .52 ...)".
- [x] LOW (page): Kyiv item's "standard English form after 2014" was misleading ->
      "displaced 'Kiev' ... (most news style guides switched around 2019)".
- [x] LOW (page): Oceania shared --c1 blue with North America — indistinguishable on
      the colour-only hero map (8 colours for 9 regions). Added a ninth colour --c9
      (brown #8a5a2b light / #c08b4d dark) in all four palette blocks; hero now shows
      9 distinct fills (verified: 5 Oceania dots on --c9).
- [x] LOW (cross-file): page's "2013 news overwhelmingly used Saigon" unsupported ->
      "still common in news and historical coverage".
- [x] LOW (cross-file): README Method steps renumbered to match the page (Layout
      alternatives = 8, Orientation = 9) with both cross-references updated.
- [x] LOW (readme): decimal style unified to APA no-leading-zero for statistics
      (.347/.515/.709 table, fit stats, cosine range/mean, Tampa/Moscow cosines);
      slider cutoffs keep the UI's 0.xx form.

## Fable review panel — Round 4 (all three lenses ran)
wf_194b27fb. NO HIGH/MED remaining — 7 LOW copy-edit items (one duplicated across
two reviewers), all fixed:
- [x] LOW (page, grammar): lone serial comma "hover, tap, or Tab" -> "hover, tap or
      Tab" (page-wide no-serial-comma style).
- [x] LOW (page, clarity): "the same asymmetry as this map's weak north-south axis"
      overstated the equivalence with the LLM-probing papers' regional inequality ->
      "an asymmetry that echoes ...".
- [x] LOW x2 (readme + cross-file, duplicate): Run-it comment "# MDS/UMAP/t-SNE
      layouts" omitted PCA -> "# MDS/PCA/t-SNE/UMAP layouts + metrics".
- [x] LOW (readme, citations): two truncated proceedings titles completed in BOTH
      files: IJCNLP + "(Volume 1: Long Papers)"; BlackboxNLP + "on Analyzing and
      Interpreting Neural Networks for NLP" (titles per aclanthology).
- [x] LOW (readme, statistics): "preserves the cosine ranking best" qualified to
      "the global cosine ranking (Spearman ρ) and top-10 neighbourhoods best"
      (dissim_study also computes recall@5, where the transforms edge ahead within
      noise).
- [x] LOW (cross-file): pipeline table "both views" (stale, pre-matrix) -> "all three
      views".

## Fable review panel — Round 5 (all three lenses ran) — CONVERGED
wf_da18d899. All three reviewers returned EMPTY findings:
  page:      "The page is clean ... verified exactly ... reported honestly."
  readme:    "The README is clean ... no genuine defects found."
  cross-file: "The page and README are mutually consistent and clean."
Fable loop complete: R1 (1 MED + 6 LOW) -> R2 (2 MED + 5 LOW) -> R3 (2 MED + 5 LOW)
-> R4 (7 LOW) -> R5 (clean x3). Combined with the earlier Opus+Sonnet+Haiku loop
(also converged), the page and README have now passed two independent multi-round
multi-model review loops.

## Major-Revision implementation (panel roadmap: REQUIRED + RECOMMENDED, per Ivan's
## approval; R5 teaching apparatus deliberately skipped — page stays an essay)
New analysis: robustness_study.py -> output/robustness.json (all numbers verified):
  between-region share .878; within-region geo-fidelity raw .33 = t-SNE .33 > UMAP .28
  > MDS .23 = PCA .23; region-collapse RAISES every layout (MDS .574->.706, PCA
  .599->.705, t-SNE .644->.681, UMAP .671->.720); geographic neighbour recall@10 raw
  .59 vs MDS .45 / PCA .36 / t-SNE .61 / UMAP .61; 1000-resample city bootstrap:
  all layout-minus-raw CIs exclude 0 (PCA-raw [.04,.15]), all adjacent layout CIs
  include 0; rotation scan MDS max lat-r .209, t-SNE .407.
- [x] R1 (DA C1/C2): geo-fidelity DECOMPOSITION added to the page — new table (full /
      within-region / region-collapsed / neighbour recall) + rewritten mechanism
      paragraph presenting denoising AND cluster quantization; verdict propagated to
      hero ("partly has a precise shape... sharp map of regions, blurry inside"),
      What-to-notice, Related work, README.
- [x] R2: hero now defines "partly" (regional structure strong, within-region blurry,
      N-S weaker than E-W).
- [x] R3: "no geographic information enters" contradiction resolved — Methodology
      step 1 now discloses that token resolution was adjudicated with geographic
      ground truth (a blind pipeline would put St Petersburg in Florida).
- [x] R4: compute_intervals.py fixed — classical-init MDS seed sweep (constant .572
      x12, determinism now VERIFIED) + separate honest random-init sensitivity sweep
      (.496-.578); r~=.21 latitude ceiling now backed by a shipped rotation scan;
      both scripts added to README pipeline + Run-it.
- [x] R6 (R3-reviewer W1-W3): Oceania got a unique HEXAGON marker; hero draws region
      SHAPES (colour+shape redundant from the first figure); geo-map edges and
      spotlight lines now wrap at the antimeridian (154 ambient + e.g. 36 of
      Auckland's 123 spot lines draw the short way across the Pacific); interactive
      SVGs role="group", markers role="button" with "City, Region" labels; matrix
      rows get shape glyphs (Path2D) + canvas aria points to the accessible
      search/drawer pathway; drawer head aria-live="polite".
- [x] S1: city-bootstrap caveat added ("advantage over raw survives, podium positions
      do not").
- [x] S2: added verified refs Mikolov-Yih-Zweig 2013 (N13-1090), Montello et al. 2003
      (COSIT, DOI), Gupta et al. 2015 (D15-1002), Espadoto et al. 2021 (TVCG DOI);
      Mikolov 2013 cites disambiguated APA-style (Mikolov, Sutskever, et al.);
      "echoes N-S axis" category confusion fixed; Recchia & Louwerse re-glossed;
      unverified "worst for Oceania/South Asia/South America" list dropped.
- [x] S3 (light): step-8 stability machinery moved into a <details> disclosure.
- [x] S4: Barenholtz marked "preprint"; two systematic failures (N-S weakness,
      adjacency distortion) added as an explicit What-to-notice item; London hinge
      operationalized (.31 vs .30, "among the closest, not a podium"); Dubai top-10
      now includes Amman + flagged-ambiguous Hyderabad; Sydney-Melbourne gloss hedged.
Verified: build OK; 9 region colours + shapes on hero; decomposition table exact;
154 wrapped edges; Auckland spotlight wraps (36/123); no dead cite anchors; roles
correct; no console errors; no h-scroll desktop/mobile.
NOT pushed — awaiting Ivan's approval per ask-before-final-edits.

## Centroid-critique deep-dive (Ivan: "они же очень artificial? насколько эта критика
## вообще имеет место?")
Three controls added to robustness_study.py (shipped in output/robustness.json):
- LABEL-FREE: cutting the page's own average-linkage dendrogram (built from 1-cos
  alone) into 9 data-driven clusters reproduces the lift for MDS .574->.688,
  PCA .599->.659, t-SNE .644->.670; UMAP essentially flat (.671->.665). The effect
  does NOT depend on the hand-drawn region labels.
- GEOMETRIC: k-means (k=9) on the true coordinates lifts higher still (up to
  UMAP .742) — the metric essentially measures region-scale geographic recovery.
- PLACEBO: collapsing by RANDOM partitions of the same sizes crashes every score to
  rho ~= .03 (20 reps, range tight) — collapsing per se earns nothing; only
  geographically meaningful grouping does.
VERDICT: the DA's core point stands (the aggregate metric is dominated by
between-region structure and prefers a 9-point regional diagram to the full map),
but the "gazetteer" framing overstates: the collapsed points sit where each layout
itself put the regions, i.e. the between-region arrangement is genuinely recovered
geography at continental scale. Page updated: new controls paragraph ("Aren't nine
hand-drawn regions an artificial yardstick?"), README mirrored.
Also per Ivan: the page's dual identity (teaching demonstration AND small standalone
investigation) now stated explicitly in Related work + README intro; EiC's
teaching-apparatus request remains open as a deliberate positioning choice.

## Raw-space collapse added (Ivan: "почему region-collapsed не делается для raw?")
No principled reason — an omission. Added collapse_raw_by(): assign each city its
region's MEAN 300-d vector, cosine distances between means, geo-fidelity. Results
(robustness.json): region-collapsed raw = .815 — the highest of all (collapsed
layouts .68-.72); dendrogram-cut raw .711; k-means-coords raw .825; random .024.
Reading: the embedding's regional core is RICHER than what any 2-D layout retains —
nine region-mean vectors track great-circle distance at rho=.82 with no projection.
Table "—" replaced with .82; controls paragraph + README updated.

## Re-review round 1 (partial: recommended lens ran; required + fresh-eyes hit session
## limit, relaunching)
rr:recommended verified S1-S4 + A1-A2 against files and shipped artifacts:
S1/S3/S4/A1/A2 Addressed, S2 Partially. Residuals triaged (classifier was unavailable
for this agent, so every claim re-verified by hand):
- [x] REAL: step-8 details bootstrap CIs had drifted — my collapse-controls insertion
      consumed shared RNG state before the bootstrap, shifting resamples. Root fix:
      dedicated RNG streams per analysis (RNG_BOOT=42, RNG_RAND=43) so section order
      can never move another section's numbers; rerun reproduces the page's CIs
      exactly ([-.02,.08], [-.05,.10], [.04,.15]).
- [x] REAL: ".40 vs .41" — What-to-notice failures item said t-SNE "manages .40" while
      step 9's rotation scan says .41 (canonical .407). -> .41.
- [x] REAL (follow-on): placebo means with the dedicated stream are .01-.03; page
      wording made rerun-proof: "noise level (rho ~= 0, means .01-.03 over 20 draws)".
- [~] REJECTED: claimed leftover "(Mikolov et al., 2013)" in Software section — the
      built page has only disambiguated forms (2x Sutskever, 1x Yih); verified by grep.

## Re-review complete (all three lenses) — verification matrix
REQUIRED:  R1 Addressed / R2 Addressed / R3 Addressed / R4 Addressed /
           R5 Deliberately declined (dual positioning stated; venue-fit question
           stays open by design) / R6 Addressed.
RECOMMENDED: S1 / S3 / S4 / A1 / A2 Addressed; S2 Partially -> now fully.
Fresh-eyes found 3 MED + 1 LOW in the revised material, all fixed:
- [x] MED citations: "(Mikolov et al., 2013)" in the Software section WAS ambiguous
      after all — the cite is split across a line break, which my single-line grep
      missed. My earlier "REJECTED" note was WRONG; the reviewer was right. Fixed to
      (Mikolov, Sutskever, et al., 2013); built page now has 3x Sutskever + 1x Yih.
      CORRECTION to the previous log entry.
- [x] MED statistics: README said dendrogram clusters "lift scores the same way" —
      false for UMAP (flat, .671->.665). Mirrored the page's honest scoping.
- [x] MED truth: README step 1 lacked the ground-truth-adjudication qualification the
      page carries (R3) — added ("...and, as ground truth, in adjudicating ambiguous
      token choices (step 3): a fully blind pipeline would have put St Petersburg in
      Florida").
- [x] LOW grammar: README parenthetical broken by the raw-collapse edit (sentence
      break inside "(...)", stranded ")") — restructured.
Noted, no action: keyboard access is Tab-through-124-markers (future accessibility
pass); k-means raw .825 -> ".83" (consistent half-up rounding); MDS recall@10 .52
(half-up of .515 per layouts.json).
NEW EDITORIAL DECISION: ACCEPT (with the R5 venue-fit question recorded as open by
deliberate positioning). All round-1 CRITICAL and MAJOR findings verified closed by
analysis and reframing; revision additions (centroid controls, raw-collapse .82)
verified against shipped artifacts.
