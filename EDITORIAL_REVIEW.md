# Editorial Review Package — city-similarity-map

Simulated journal peer review (academic-paper-reviewer skill, `full` mode).

- **Manuscript**: "Could language reconstruct a map of the world?" — interactive explorable
  explanation (docs/index.html) + methods documentation (README.md)
- **Venue class**: statistics / data-science education (JSDSE / JOSE / Distill-style)
- **Review date**: 2026-07-21 · **Round**: 1
- **Panel**: Editor-in-Chief, R1 Methodology, R2 Domain, R3 Perspective, Devil's Advocate —
  five independent seats, no cross-referencing; reviewers read-only.

---

## Editor-in-Chief

**Identity**: Editor of an international journal of statistics and data-science education (JSDSE/JOSE-class), with a background in statistics education, open educational resources, and interactive scientific communication.

**Review focus**: Venue fit and originality of the submission as a teaching resource; significance to instructors, students, and self-learners; coherence of the piece as a publishable educational artifact; and whether the framing question ("Could language reconstruct a map of the world?") is honestly answered. Statistical methodology depth and literature completeness are left to the specialist reviewers.

**Recommendation**: **Minor Revision** · Confidence 4/5

**Scores (0–100)**: originality 72 · rigor 82 · evidence 85 · coherence 88 · writing 84

### Summary

This is an unusually honest and well-crafted explorable explanation of a classic result: that distributional word vectors partially encode geography. The framing question is answered in the first line ("Short answer: partly, yes") and, rarely for the genre, the piece keeps that calibration throughout — the Related work section states plainly that "the central finding is not new, and Konkol et al. (2017) established it more rigorously," and every headline number I spot-checked against the shipped data (cosine range, mean, and the three worked geo-fidelity pairs) reproduces exactly. The pedagogical ladder (context → 300-number vector → cosine angle → MDS) is coherent, and the interface is designed to teach skepticism about dimensionality-reduction maps rather than merely display one — the pinned drawer deliberately exposes "the projection's compromises." As a Distill-style essay this is close to publishable as-is. What keeps it from acceptance at a teaching-materials venue in its current form is the missing instructional apparatus: no stated audience or learning objectives, no instructor guidance or suggested activities, and no evidence of use with learners. Secondarily, the register oscillates between general-reader warmth and expert-density methodology, and the one genuinely novel empirical claim (all four projections beat the raw 300-d geo-fidelity) is advertised somewhat beyond what a single embedding and one hand-curated 124-city sample can license. These are fixable within a minor revision, and I would expect the revised piece to be a strong addition to the venue.

### Strengths

**S1: The framing question is answered honestly, and the honesty is sustained**

The hero opens "Short answer: partly, yes" and immediately qualifies: "news events, ambiguous names and shared institutions bend the map in revealing ways." Related work states "What this page adds is small and specific... The central finding is not new, and Konkol et al. (2017) established it more rigorously." Methodology step 9 flags that the E–W/N–S axis correlations "are measured after an alignment that itself uses the real coordinates, so they describe residual correspondence rather than prove unsupervised recovery." This is exactly the epistemic modeling a teaching venue should reward; most submissions in this genre oversell.

**S2: A coherent pedagogical ladder with a genuinely elegant foreshadowing move**

The four "How it works" cards build cleanly (context → "a name becomes 300 numbers" with the actual vector stripes → cosine angle → "MDS: a map from distances alone"). Card 3's caveat is the standout: "the gap you see between Melbourne and New York (≈ 41°) is not their real angle... three 300-d arrows simply cannot be flattened onto a plane without distorting some angle. That is the very compression MDS negotiates across all 124 cities in card 4." Introducing the projection-distortion problem inside the toy example, before the real map, is first-rate instructional design.

**S3: The interactivity teaches critical reading rather than decorating**

One cutoff slider and one selection drive all three linked views; the drawer ranks all 123 neighbours from the true 300-d cosines, and the Methodology says why: "The hover overlay shows each city's true 300-d nearest neighbours precisely so the projection's compromises stay visible." The layout switcher plus per-layout notes ("the gaps between clusters are largely artefacts of the optimizer, so do not read them as distances") turn the page into a working lesson on not over-reading DR maps — a learning outcome of real value to the readership.

**S4: Statistical candour unusual for an explorable**

Stress-1 = .347 is reported against Kruskal's rule of thumb and called "a heavily compressed fit"; the UMAP whisker is explicitly "the observed min–max range... (not a confidence interval)"; the neighbourhood > global > raw ordering is downgraded to "a strong tendency, not a law" because at its narrowest it holds "by only .004." The worked Madrid/Barcelona/Lisbon/Tokyo pairs make the geo-fidelity metric concrete, and all three cosines match the shipped vectors to three decimals.

**S5: Reproducibility appropriate to an educational artifact**

Pinned versions (scikit-learn 1.9.0, SciPy 1.17.1, umap-learn 0.5.12), deterministic initializations documented per method, a runnable step-by-step "Run it" recipe, and supporting analyses shipped as scripts (dissim_study.py, make_layouts.py). I independently verified the 124 cities, 7,626 pairs, and the −.06/.86/.30 similarity statistics from data/city_vectors.npy and data/city_index.csv.

### Weaknesses

**W1: No instructional apparatus: audience, learning objectives, and instructor guidance are absent** — *Major*

- **Problem**: Neither the page nor the README states who the resource is for, what a learner should be able to do afterwards, or how an instructor would deploy it. There are no suggested activities, discussion prompts, or assessment ideas, and no evidence of use with actual learners (even informal classroom piloting or user feedback).
- **Why it matters**: For a JSDSE/JOSE-class venue this is the difference between a portfolio essay and an adoptable open educational resource. Reviewers and adopting instructors need learning goals to evaluate whether the design succeeds, and the venue's readership is instructors first.
- **Suggestion**: Add a short "Using this in teaching" section (page and README): 3–5 explicit learning objectives (e.g., interpret cosine similarity; explain why DR maps distort; distinguish supervised probes from unsupervised layouts), 2–3 concrete activities (predict-before-reveal with the slider; have students audit a token-resolution choice; swap the city list), and any evidence of use. This is prose work only; no re-analysis is required.

**W2: Uneven audience calibration between the explanatory front and the methodology back** — *Major*

- **Problem**: The piece courts a general reader ("a name becomes 300 numbers", the Firth quote) but Methodology steps 5–9 run at specialist density in continuous prose: SMACOF with Torgerson initialization, semi-metric triangle audits, "Procrustes disparity ≤ .005", closed-form SVD solutions. Step 8 in particular is a single ~250-word paragraph carrying four algorithms, a baseline argument, and a seed analysis.
- **Why it matters**: The students the introduction successfully recruits are the readers most likely to disengage mid-Methodology; the experts who want that density will go to the scripts anyway. The venue's self-learner audience needs a graded path.
- **Suggestion**: Tier the methodology: keep one plain-language sentence per step in the main flow and move derivation-level detail into the page's existing <details> disclosure pattern (already used elsewhere). Breaking step 8 into "the four algorithms" and "the baseline result" sub-items would help most.

**W3: The headline novel claim is stated more generally than one sample and one embedding can support** — *Major*

- **Problem**: Contribution (1) — "all four 2-D layouts reproduce geography better than the raw 300-d cosine distances" — rests on a single embedding (GoogleNews 2013) and a single hand-curated sample that the authors themselves describe as "deliberately balanced across 9 regions rather than ranked by population." That curation plausibly shapes both the .50 raw baseline and the projection ordering; nothing on the page tests whether the result survives a different city sample or model.
- **Why it matters**: This is the one finding the piece advertises as not found in the literature; if it is an artifact of the curated sample, the teaching narrative built on it ("projection concentrates geography by shedding noise") would need re-hedging. Deep methodology is Reviewer 1's remit, but the scope of an advertised contribution is an editorial matter.
- **Suggestion**: Either add one robustness paragraph (e.g., re-run make_layouts.py on a strict top-N-by-population list, or on GloVe) or narrow the claim's wording to "on this curated sample and embedding" wherever contribution (1) is stated (Related work, What to notice, Methodology step 8).

**W4: Archival self-containment is undercut by CDN dependencies** — *Minor*

- **Problem**: The page loads Google Fonts and KaTeX 0.16 from external CDNs (head links to fonts.googleapis.com and cdn.jsdelivr.net) while elsewhere advertising self-containment ("A compact Natural Earth 110m land outline... is embedded, so no external map tiles").
- **Why it matters**: Published teaching materials are used offline, behind school firewalls, and must remain intact for archival; a CDN outage or URL rot degrades typography and all typeset formulae. The page does carry HTML fallbacks inside the math spans, which mitigates but does not resolve this.
- **Suggestion**: Bundle the two fonts and KaTeX (or accept system serif + the existing HTML math fallbacks and drop the CDN links). State the self-containment guarantee once, accurately.

**W5: README duplicates the page's Methodology in parallel prose, inviting drift** — *Minor*

- **Problem**: README "Method" steps 1–11 restate the page's Methodology in different wording with the same numbers. The two are currently consistent (I cross-checked the geo-fidelity ordering, seed range, and triangle audit), but every future edit must now be made twice; the README also carries page-only detail (e.g., the slider's 0.30–0.86 span) that will silently stale if the UI changes.
- **Why it matters**: For an accepted artifact, the repo documentation is part of the publication; divergence between the two would be a correctness defect discovered by readers.
- **Suggestion**: Make the README the reproduction-focused document (pipeline, run instructions, data provenance) and link to the page as the canonical methods narrative, or generate both from one source.

### Questions for the author
1. Who is the primary intended audience — introductory data-science students, NLP students, or general readers — and what should they be able to do after working through the page? Would you commit to explicit learning objectives and a short instructor-guidance section?
2. Has the page been used with real learners in any setting (course, workshop, informal testing), and if so what did you observe or change as a result?
3. Does the "every projection beats the raw 300-d baseline" ordering survive a different city sample (e.g., strict top-124 by population, which you note would look very different) or a second embedding such as GloVe — and if untested, would you narrow the claim's wording accordingly?
4. For archival publication, are you willing to bundle the fonts and KaTeX so the page is fully self-contained offline, as the map data already is?

### Minor issues
- No visible license, date, or version on the page footer (the repo has a LICENSE file); an accepted OER should surface its license and a suggested citation on the artifact itself.
- The footer offers no "how to cite this page" entry — worth adding alongside the GitHub link for a venue publication.
- Methodology "Software" says labels were "pre-computed offline with matplotlib 3.11 and adjustText 1.4" — these two packages are absent from the README's reproducibility narrative; add them to the pinned-versions sentence for completeness.
- The per-layout E–W/N–S axis correlations (e.g., PCA r = .80/.10, t-SNE .90/.40) appear only in the page's layout-switcher stats and not in the README's method summary; harmless, but one more drift surface between the two documents.
- On viewports under 640px all map labels are hidden except the selected city's; the small-screen reading experience of the two maps deserves one sentence of guidance (e.g., "on phones, search or tap to label").
- The Barenholtz (2026) R² ≈ .8 comparison is properly hedged as "different metrics on different scales... a direction, not a subtraction" — good; I leave verification of that preprint's details to the literature reviewer.

---

## Peer Reviewer 1 (Methodology)

**Identity**: Quantitative methodologist specializing in embedding evaluation and dimensionality reduction (MDS/t-SNE/UMAP practice, uncertainty reporting, rank-based evaluation metrics).

**Review focus**: Research-design rigor of the submission: whether geo-fidelity is a sound and sufficient metric; whether the seed/determinism analysis and its min–max whisker are correct; whether the triangle-inequality audit and Procrustes-circularity disclosures are handled properly; whether the headline "projections beat raw space" claim is metric-robust; and reproducibility of the shipped scripts. I re-ran the fast analyses on the shipped small arrays (data/city_vectors.npy, output/layouts.json, output/intervals.json) to verify numbers and to probe the central claim.

**Recommendation**: **Minor Revision** · Confidence 4/5

**Scores (0–100)**: originality 66 · rigor 63 · evidence 72 · coherence 85 · writing 88

### Summary

This is an unusually honest and well-documented explorable explanation. Every headline number I checked reproduces exactly from the shipped artifacts: raw-space geo-fidelity .503, layouts .574/.599/.644/.671 (recomputed from output/layouts.json), the 12-seed UMAP range .603–.675, t-SNE invariant at .644, Stress-1 .347, and recall@10 .41/.52/.71/.70. The disclosure practices — Procrustes circularity flagged as "descriptive only", the UMAP whisker explicitly labeled min–max "not a confidence interval", determinism claims verified per method — exceed the norm for teaching material and for much published work. However, the central novel claim (contribution 1, "every 2-D layout reproduces real geography better than the raw 300-d distances") is metric- and scale-dependent in ways the page does not acknowledge: under geographic neighbour recall@10 the raw space (.594) beats MDS (.452) and PCA (.362), and restricted to within-region pairs the raw space matches or beats all four layouts (.332 vs .225–.332). The projections' win lives almost entirely in coarse between-region structure. Additionally, layout differences carry no sampling uncertainty over the 124-city list (a bootstrap shows PCA−MDS and UMAP−t-SNE intervals crossing zero), and the repo's own seed sweep (intervals.json) shows random-init MDS spanning .496–.578 — dipping below the raw baseline — a sensitivity the page never surfaces. All fixes are qualifications and surfacing of existing analyses; no new machinery is needed.

### Strengths

**S1: Procrustes circularity is disclosed and quarantined correctly**

Methodology step 9 states the axis correlations are "measured after an alignment that itself uses the real coordinates, so they describe residual correspondence rather than prove unsupervised recovery — for that, see the alignment-free geo-fidelity metric". The design is also correct in substance: run_mds.py applies a genuinely rigid rotation (no scaling) to the MDS solution, Stress-1 is computed before alignment, and geo-fidelity is rank-based and thus provably alignment-invariant, exactly as the page claims ("the Procrustes alignment — which merely rotates the finished map — leaves it unchanged"). This separation of a disclosed-circular descriptive statistic from an alignment-free evaluative one is textbook-correct and rarely done this cleanly.

**S2: Seed/determinism analysis is accurate and honestly reported**

The claims "PCA and classical-init MDS have no random step, and t-SNE, initialized from PCA … was .644 on all 12 seeds tried" and "UMAP … min of .60 and a max of .68 (mean .65, SD .02)" match output/intervals.json exactly (t-SNE min=max=.644, sd 0.0; UMAP .603–.675, mean .649, sd .021). The whisker is explicitly labeled "min–max over 12 seeds … (not a confidence interval)", and the narrowest-margin caveat ("UMAP's worst seed .603 vs PCA's .599 … only .004 … a strong tendency, not a law") is verifiably correct. Reporting the shown run's position within the seed distribution (.67 "sits near its top") is a detail most authors omit.

**S3: Verification culture: exhaustive audit instead of assumption, with a common-reference transform study**

The semi-metric objection to 1−cos is checked by enumerating "all C(124,3) = 310,124 triples" (dissim_study.py implements this directly), finding 2 violations, max excess .023. The transform comparison uses common reference criteria (recall@10 against the cosine ranking; Spearman against 1−cos) alongside per-target stress, and honestly reports the deflationary conclusion that "the three layouts are nearly identical anyway (Procrustes disparity ≤ .005)" — i.e., the choice barely matters. The monotone-transform footnote ("all three would give an identical nonmetric MDS") is exactly right.

**S4: Reproducibility is near-complete and the numbers actually reproduce**

Versions are pinned (requirements.txt: scikit-learn 1.9.0, SciPy 1.17.1, umap-learn 0.5.12), seeds fixed, and every analysis ships as a runnable script. I independently recomputed geo-fidelity for all four layouts from output/layouts.json plus data/city_vectors.npy and matched the page to three decimals. The determinism claims are architecturally grounded (init="classical_mds" with n_init=1 in run_mds.py; init="pca" for t-SNE in make_layouts.py), not asserted.

**S5: Correct refusal to over-compare incommensurable figures**

The Related-work section resists a tempting but invalid comparison: the supervised probe's R² ≈ .8 vs geo-fidelity ρ ≈ .57–.67 are "different metrics on different scales (variance-explained vs rank correlation), so read them as a direction, not a subtraction". Similarly, Stress-1 = .347 is contextualized with Kruskal's benchmarks and translated into concrete usage guidance ("exact nearest neighbours should be taken from the pinned similarity ranking, not from which dot looks closest").

### Weaknesses

**W1: The headline "projections beat raw space" claim is metric- and scale-dependent, and stated without that qualification** — *Major*

- **Problem**: "What to notice" asserts "Every 2-D layout reproduces real geography better than the raw 300-d cosine distances" — unconditionally. Geo-fidelity is a single global rank correlation over all 7,626 pairs, 88% of which are between-region. Probing alternatives on the shipped data: under geographic neighbour recall@10 (fraction of each city's 10 geographically nearest cities among its 10 nearest in the given space), raw 300-d scores .594, beating MDS (.452) and PCA (.362), with only t-SNE (.606) and UMAP (.612) marginally ahead. Restricted to the 933 within-region pairs, Spearman geo-fidelity is raw .332 vs MDS .232, PCA .225, t-SNE .332, UMAP .280 — the raw space ties or wins. The projections' advantage is entirely coarse, between-region structure (raw .351 vs layouts .442–.563).
- **Why it matters**: This is contribution claim (1), the paper's most interesting empirical point. As phrased it invites the incorrect reading that projection adds geographic information at every scale; in fact compression trades fine-grained geographic fidelity for a cleaner coarse arrangement. The page's own mechanism paragraph ("a projection … drops the rest") is consistent with the scale-resolved picture, but the claim outruns it. Note the tension with the page's own caveat that for t-SNE/UMAP "distances between clusters stop being comparable" — the winning metric is dominated by precisely those pairs.
- **Suggestion**: Qualify the claim as holding for the global rank-correlation metric (it is robust across Spearman and Pearson — I verified Pearson raw .515 < all layouts — so say so), and add one sentence or a small table showing the within-region/neighbour-recall reversal. This strengthens rather than weakens the story: the projections concentrate coarse geography while sacrificing fine geography, which is exactly the compression narrative the page teaches.

**W2: No sampling uncertainty over the 124-city list; "the deterministic part of the order never moves" conflates determinism with stability** — *Major*

- **Problem**: The gf-lead text says "The deterministic part of the order never moves: raw .50 < MDS .57 < PCA .60 < t-SNE .64". "Never moves" is true only across random seeds. The 124 cities are themselves a curated sample; a city-level bootstrap (300 resamples, recomputed on the shipped layouts) gives PCA−MDS mean +.026, 95% CI [−.010, +.062] and UMAP−t-SNE +.026, CI [−.035, +.076] — both crossing zero — while MDS−raw (+.070, CI [+.034, +.106]) and t-SNE−MDS (+.070, CI [+.023, +.120]) are solid. So the tier claim (neighbourhood > global > raw) is supported, but the full four-way ordering is not distinguishable from city-sampling noise at adjacent steps.
- **Why it matters**: The page is careful about seed noise (correctly calling t-SNE vs UMAP "effectively tied") but silent about the other, larger uncertainty source. A reader is licensed to conclude "PCA beats MDS at reconstructing geography" as a stable fact; on this evidence it is a point estimate whose sign is not settled. For a venue teaching data-science practice, modeling only one of two noise sources is the kind of lesson-by-omission worth fixing.
- **Suggestion**: Run a city-level bootstrap (a ~15-line addition to compute_intervals.py; it needs only layouts.json and coordinates) and either add intervals to the bar chart or soften the text to claim only the tier ordering, explicitly noting that adjacent differences (MDS vs PCA, t-SNE vs UMAP) are within sampling noise of the city list.

**W3: The repo's own MDS seed sweep contradicts its docstring and surfaces an un-disclosed init sensitivity** — *Major*

- **Problem**: compute_intervals.py's docstring claims it refits "under N random seeds at the *shown* hyperparameters" and that "classical-init MDS (SMACOF) is effectively deterministic, but we still sweep its random_state to confirm". The code does neither for MDS: it calls MDS(..., random_state=s, n_init=1) with no init argument — under the installed scikit-learn 1.9 that is random initialization (default max_iter 300, eps 1e-6, vs the pipeline's classical init, 3000, 1e-9), plus the deprecated dissimilarity="precomputed" API. The result, shipped in output/intervals.json, is anything but deterministic: MDS geo-fidelity spans .496–.578 (SD .024), and its minimum falls below the raw baseline of .503 — a random-init MDS run can violate "every projection beats the raw space". Neither the page nor the README mentions this.
- **Why it matters**: The page's determinism claim for the shown classical-init configuration remains true (I verified the architecture in run_mds.py), but the sweep as written does not "confirm" it — it tests a different estimator and quietly demonstrates that the all-four-beat-raw result is contingent on the initialization choice. Since classical init lands near the top of the random-init range (.578 max vs .57 shown), a skeptic could ask whether the MDS bar benefits from a favorable init. Leaving the contradicting artifact in the repo undiscussed is the sort of loose end reviewers of the interactive-explainer genre should not find.
- **Suggestion**: Fix compute_intervals.py to sweep the shown configuration (init="classical_mds" — which should then show zero variance — and the current MDS API), or keep the random-init sweep but describe it accurately and cite it on the page as an init-sensitivity analysis: "random-init MDS spans ρ .50–.58 over 12 seeds; the deterministic classical init used here lands at .57". Either resolves the contradiction; the second is more informative.

**W4: Hyperparameter sensitivity is unexamined while seed sensitivity is meticulous** — *Minor*

- **Problem**: The neighbourhood-vs-global ordering rests on one hyperparameter setting per method: t-SNE perplexity 20, UMAP n_neighbors 15 / min_dist 0.3 (Methodology step 8). Both parameters directly control the local/global trade-off that the paper's central comparison is about — large perplexity or n_neighbors pushes these methods toward global-structure behavior, and geo-fidelity is a global metric. No sweep is reported.
- **Why it matters**: The generalization from "t-SNE at perplexity 20 and UMAP at n_neighbors 15 beat MDS/PCA" to "the neighbourhood methods (t-SNE, UMAP) recover geography better than the global ones" (README step 8, page step 8, What-to-notice) is a claim about method families supported at a single point of a parameter space known to matter for exactly this contrast. The asymmetry is conspicuous next to the care spent on seeds: a reader learns to check the cheap robustness axis but not the influential one.
- **Suggestion**: Add a small sweep (perplexity ∈ {5, 20, 50}; n_neighbors ∈ {5, 15, 50}) to compute_intervals.py — the fits take seconds at n=124 — and report whether the tier ordering survives; otherwise soften the family-level claim to the tested settings.

**W5: Small documentation/description inaccuracies: undocumented seed script, non-rigid "rigid" alignment, unverifiable rotation-ceiling figure** — *Minor*

- **Problem**: (a) compute_intervals.py, the source of the whisker figure and the 12-seed claims, appears in neither the README pipeline table (steps 1–7), the "Run it" block, nor the "Supporting analyses ship as runnable scripts" list. (b) Page step 8 says "All four share the same rigid Procrustes (rotation/reflection) alignment" and README step 8 says "each geo-aligned by the same rigid Procrustes step (step 9)", but make_layouts.py's align_to_geo rescales PCA/t-SNE/UMAP to unit RMS before rotating — a similarity transform, not rigid, and not the same code path as MDS (aligned scale-free in run_mds.py). All reported metrics are scale-invariant, so no number is wrong, but the description is. (c) The claim "even the single best rotation cannot lift the MDS layout's latitude past r ≈ .21" corresponds to no shipped script.
- **Why it matters**: For a submission whose selling point is a transparent, fully runnable pipeline, the one analysis a skeptical reader most wants to re-run (the seed sweep) is the one that is undocumented; and "rigid" is load-bearing vocabulary in step 9's argument that alignment "preserves every pairwise distance and the stress exactly" — a claim that is strictly true only for the MDS path.
- **Suggestion**: Add compute_intervals.py to the README pipeline table and Run-it block; reword step 8 to "scaled to common size and rigidly rotated" (noting the reported metrics are scale-invariant); either ship the rotation-scan behind the r ≈ .21 figure or drop the number.

### Questions for the author
1. Restricted to within-region pairs, raw 300-d geo-fidelity (.332) ties or beats all four layouts (.225–.332), and raw geographic neighbour recall@10 (.594) beats MDS (.452) and PCA (.362). Do you agree contribution (1) should be qualified as a claim about coarse, between-region structure under a global rank metric, and will you add a scale-resolved statement?
2. compute_intervals.py sweeps MDS under random initialization with default iteration settings, while its docstring claims classical init "at the shown hyperparameters"; the shipped intervals.json shows random-init MDS spanning .496–.578, below the raw baseline at its minimum. Was this discrepancy known, and how will you surface the init sensitivity on the page?
3. Have you checked whether the neighbourhood > global > raw ordering survives varying t-SNE perplexity and UMAP n_neighbors/min_dist, given both parameters directly tune the local/global trade-off the comparison is about?
4. What analysis produced the "single best rotation cannot lift latitude past r ≈ .21" figure in step 9 and t-SNE's N–S r = .40 comparison — is there a script, and can it ship with the repo?

### Minor issues
- Stress-1 values across the three transforms (step 5 table: .347/.392/.384) are each computed against a different target, so they are not commensurable as a selection criterion; the common-reference columns (recall@10, fit ρ) carry the argument — consider noting this in the table caption.
- The triangle-inequality audit is presented as contribution (2), but SMACOF does not require metric inputs at all (stress majorization accepts arbitrary symmetric dissimilarities), and violations of 1−cos require cos_ij + cos_jk − cos_ik > 1, which is a priori near-impossible with max cos .86; the audit is a nice pedagogical verification, not a load-bearing result — the framing slightly overplays it.
- The 7,626 pairwise observations entering geo-fidelity are Mantel-type non-independent (124 cities generate them); the page correctly reports no p-values, but a one-line teaching note would preempt readers from attaching naive significance to ρ values or differences.
- t-SNE "identical geo-fidelity on all 12 seeds" rests on values rounded to 3 decimals in compute_intervals.py's stats(); "identical to three decimals" would be the precisely supported claim.
- make_layouts.py still calls the raw-space figure the "geo-fidelity ceiling" in comments and printout, while the page correctly reframes it as a baseline that every layout beats — align the code vocabulary with the page.
- UMAP whisker endpoints .603/.675 are reported as ".60 to .68"; the .675→.68 rounding is defensible but the SVG aria-label and text could state three decimals once for exactness.
- compute_intervals.py's MDS call uses the deprecated dissimilarity="precomputed" parameter under the pinned scikit-learn 1.9, while run_mds.py uses the current metric="precomputed" API — harmonize before the deprecation lands.

---

## Peer Reviewer 2 (Domain)

**Identity**: Computational linguist working on geographic and world knowledge in distributional semantics; my reference line runs from Louwerse and Zwaan (2009) through Konkol et al. (2017) to Gurnee and Tegmark (2024) and the recent LLM-probing literature.

**Review focus**: Literature coverage and positioning: whether the Related-work sections of the page and README are fair, complete and accurate; whether the three claimed contributions (across-projection comparison with projections-beat-raw, exhaustive semi-metric audit, dateline-token artefact) are genuinely absent from prior work and correctly sized; and whether Konkol et al. (2017) is characterized accurately. I do not review statistics mechanics or venue fit.

**Recommendation**: **Minor Revision** · Confidence 4/5

**Scores (0–100)**: originality 70 · rigor 84 · evidence 82 · coherence 87 · writing 90

### Summary

This submission positions itself with unusual honesty for the genre. The Related-work section correctly traces the lineage from Louwerse and Zwaan (2009) through Recchia and Louwerse (2014), Louwerse and Benesh (2012, Middle-earth), Konkol et al. (2017), Liétard et al. (2021), Gurnee and Tegmark (2024), Godey et al. (2024) and Barenholtz (2026), and states plainly that "The central finding is not new, and Konkol et al. (2017) established it more rigorously." The characterization of Konkol et al. — 16 embedding models, a spherical 3-D regression target, kilometre errors, cross-validation — is accurate, and mapping their ambiguous-name failure mode (Kobe, Bismarck) onto this page's Lisbon/St Petersburg/Santiago cases is exactly the right use of precedent. The three claimed contributions are hedged appropriately ("three minor empirical points I did not find in that literature") and plausibly novel at that modest size. Two things need fixing: the claim that regional inequality in LLM probes "echoes this map's weak north–south axis" conflates representation inequality with what the authors' own Methodology says is a projection artefact (and the region list should be re-verified against the cited papers); and three adjacent strands are missing — the word2vec country–capital analogy result, the spatialization/cognitive-cartography literature that directly tested the distance-as-similarity reading the page relies on, and static-embedding attribute-probing precedents between Louwerse and Konkol. These are repairable in minor revision.

### Strengths

**S1: Honest, correctly-sized contribution claims**

The page states "What this page adds is small and specific. The central finding is not new, and Konkol et al. (2017) established it more rigorously," and the README mirrors this ("What this adds is small and specific"). Each of the three claims is scoped as a "minor empirical point" hedged with "I did not find in that literature" — the exhaustive triangle audit (310,124 triples, 2 violations) and the MEXICO_CITY dateline artefact are indeed the kind of dataset-specific observations that prior work would not have published, so presenting them as minor documentation rather than discoveries is exactly the right sizing.

**S2: Accurate and generous characterization of the closest precedent**

Konkol et al. (2017) is described as fitting "city vectors from 16 embedding models to real coordinates as a benchmark — with a more rigorous setup (a spherical 3-D target, error reported in kilometres, noise-robustness and cross-validation)," which matches the paper, and crediting the precedent as "more rigorous" is rare candour. Aligning their ambiguous-name failure mode ("their Kobe → the basketball player, Bismarck → the chancellor; here Lisbon, St Petersburg, Santiago") is a genuinely insightful use of prior work: it shows the same error mechanism reproducing across a decade and two methodologies.

**S3: Complete and current core lineage, with the supervised–unsupervised gap handled responsibly**

The chain LSA-era (Louwerse & Zwaan 2009; Recchia & Louwerse 2014; Louwerse & Benesh 2012) → static embeddings (Konkol 2017; Barenholtz 2026) → LLM probing (Liétard 2021; Gurnee & Tegmark 2024; Godey 2024) covers every landmark I would demand, including a 2026 preprint. The comparison of Barenholtz's supervised R² ≈ .8 with the page's unsupervised ρ ≈ .57–.67 is explicitly defused: "different metrics on different scales (variance-explained vs rank correlation), so read them as a direction, not a subtraction" — the right way to cite an incommensurable number.

**S4: Positioning is protected against the circularity objection**

Because the page separates the alignment-free geo-fidelity metric from the post-Procrustes axis correlations ("measured after an alignment that itself uses the real coordinates, so they describe residual correspondence rather than prove unsupervised recovery"), the across-projections comparison in contribution (1) rests on a metric that genuinely never sees geography — a prerequisite for claiming it as a finding relative to prior work.

### Weaknesses

**W1: The "echo" between LLM regional inequality and the weak north–south axis is a category confusion** — *Major*

- **Problem**: Related work states the LLM signal is "geographically unequal, worst for Oceania, South Asia and South America — an asymmetry that echoes this map's weak north–south axis." But Methodology step 9 explicitly says the weak N–S recovery (r = .17) is "a statement about this projection, not a claim that the 300-d space contains none — t-SNE, for one, reaches north–south r = .40." Regional probe-error inequality in Gurnee & Tegmark and Godey et al. is a property of the representation and training data; the weak N–S axis here is, by the authors' own account, largely an MDS artefact. The two are not the same phenomenon, and the region list itself should be re-verified — my recollection is that Africa is among the worst-served regions in both papers, and it is conspicuously absent from the list given.
- **Why it matters**: This is the one place where the otherwise scrupulous positioning overclaims a connection to the literature; a domain reader will catch both the conflation and any misstated region ranking, undermining trust in an otherwise accurate section.
- **Suggestion**: Either delete the "echoes" clause or rephrase to what is defensible, e.g. "a reminder that geographic signal in embeddings is unevenly distributed — as this map's own weak north–south recovery under MDS also shows in a different way." Re-check the "worst for" region list against the actual tables in Gurnee & Tegmark (2024) and Godey et al. (2024) and attribute the inequality finding per-paper.

**W2: Three adjacent literature strands are missing** — *Major*

- **Problem**: (a) The country–capital analogy result (Mikolov, Yih & Zweig, 2013, NAACL) — the single most famous demonstration that word2vec encodes geographic relations — is absent, even though the page is a teaching resource built on exactly that model. (b) The spatialization / cognitive-cartography literature (e.g., Skupin & Fabrikant, 2003; Fabrikant, Montello and colleagues' experiments on whether viewers actually read distance-as-similarity in point-display spatializations, framed by them as a "first law of cognitive geography") is uncited, despite the page's central framing being Tobler's law and "distance itself encodes dissimilarity." (c) Between Louwerse (2009) and Konkol (2017) sits static-embedding attribute-probing work (e.g., Gupta, Boleda, Baroni & Padó, 2015, EMNLP, decoding referential attributes of cities and countries from distributional vectors), a direct precedent for the supervised-probe side of the comparison the page draws with Barenholtz.
- **Why it matters**: For a venue publishing open educational resources, (a) is the most teachable single citation available and its absence is striking; (b) is the literature that validates the page's core visual metaphor and its Tobler framing; (c) affects the accuracy of the implied history in which supervised probing of static embeddings jumps from Konkol to Barenholtz.
- **Suggestion**: Add one sentence and citation for each: the analogy result in the "How it works" cards or Related work; a spatialization citation where the semantic-map callout promises "the closer two cities sit, the more similar their vectors"; and Gupta et al. (2015) alongside Konkol in the supervised-precedent sentence.

**W3: Contribution (1)'s novelty is checked only against the geographic-embeddings literature, not the DR-evaluation literature** — *Minor*

- **Problem**: The claim that layouts were "compared across projections rather than across embeddings" and that "all four 2-D layouts reproduce geography better than the raw 300-d cosine distances" is hedged only against "that literature" (the geography line). Comparing projection methods on preservation of external structure is home turf for the dimensionality-reduction evaluation literature (projection quality-metric surveys, neighbourhood-preservation and denoising analyses), which is not engaged; the projections-beat-raw effect is a cousin of known results on DR shedding off-manifold variance and mitigating high-dimensional distance concentration.
- **Why it matters**: The claim as scoped survives, but a reader from the visualization/DR community could reasonably say the mechanism is anticipated; one sentence of engagement would make the claim robust to that audience and keep the novelty statement precise (the geo-fidelity instance is new; the denoising mechanism is not).
- **Suggestion**: Keep the claim but add a hedging clause and one citation to a DR quality-metrics survey (e.g., Espadoto et al., or Lee & Verleysen on quality criteria), positioning the geographic instantiation — not the noise-shedding mechanism — as the new part.

**W4: The gloss on Recchia & Louwerse (2014) does not match that paper's headline contribution** — *Minor*

- **Problem**: The page writes "the effect is robust across corpora and parameters (Recchia & Louwerse, 2014)", but the cited paper — "Grounding the ungrounded: Estimating locations of unknown place names from linguistic associations and grounded representations" — is primarily about inferring locations of unseen place names by association with known ones, not a parametric robustness study of the MDS-recovery effect.
- **Why it matters**: A citation whose gloss mismatches its content is exactly what domain reviewers audit, and it also undersells that paper's actual, relevant contribution (extension to unseen place names).
- **Suggestion**: Either re-gloss accurately ("and even extends to estimating locations of unseen place names from their linguistic associations") or attach the robustness claim to the correct source in the Louwerse line and cite it specifically.

**W5: README Related work is an inconsistent subset of the page's** — *Minor*

- **Problem**: The README's Related-work paragraph omits Recchia & Louwerse (2014) and Louwerse & Benesh (2012), both cited on the page, and its clause "Liétard et al. (2021), and for LLMs Gurnee and Tegmark (2024) and Godey et al. (2024), found hidden states linearly encode coordinates (improving with scale...)" attributes the scale-dependence finding to a list that includes the 2021 probe.
- **Why it matters**: The README is the citable methods document for the repository; readers who see only it get a thinner and slightly misattributed history than the page presents.
- **Suggestion**: Mirror the page's related-work list in the README (one added sentence suffices) and split the Liétard clause so scale-dependence is attributed only to the 2024 papers.

### Questions for the author
1. Are the Kobe (basketball player) and Bismarck (chancellor) examples taken directly from Konkol et al. (2017)'s error analysis, or reconstructed from memory? Please confirm against the paper, since this vignette carries the precedent-alignment argument.
2. Please re-verify the "worst for Oceania, South Asia and South America" region list against the results tables of Gurnee & Tegmark (2024) and Godey et al. (2024) — is Africa's absence from that list supported by the papers?
3. For contribution (1), did you search the DR-evaluation literature (projection quality metrics, denoising/neighbourhood-preservation studies) in addition to the geographic-embeddings line before asserting the across-projections comparison was not found?
4. The dateline-token artefact (contribution 3) is presented as undocumented; did you check practitioner-facing sources (gensim documentation and issue trackers, GoogleNews-vocabulary analyses) where all-caps token quirks of this model circulate, so the claim can be scoped as "not in the peer-reviewed literature"?

### Minor issues
- Page, Related work: "probed early by Liétard et al. (2021)" is accurate but uninformative; one clause on what they found (weak-but-present geographic encoding in masked LMs) would make the 2021→2024 arc read as progress rather than name-dropping.
- Louwerse & Zwaan (2009) is glossed on the page as "applied MDS to newspaper-text similarities" and in the README as "via LSA + MDS"; harmonize the two glosses so the method description is identical in both documents.
- Barenholtz (2026) is an arXiv preprint doing heavy load-bearing work in the supervised-vs-unsupervised comparison; consider flagging its preprint status in the running text (not just the reference list).
- Firth (1957) is cited only in the hero card and Harris (1954) only in Methodology; mentioning the two together once as the twin roots of the distributional hypothesis would serve the teaching audience.
- README Related work omits the Tobler in-text framing the page uses so effectively; the README mentions Tobler only parenthetically inside the Louwerse sentence.

---

## Peer Reviewer 3 (Perspective)

**Identity**: Cartographer and geovisualization/information-visualization researcher with an interest in visual statistics education; I review interactive explorable explanations for cartographic soundness, encoding design, accessibility, and pedagogical effectiveness.

**Review focus**: Cross-disciplinary evaluation of the submission's visualization and cartographic choices (equirectangular network map, the 9-region colour+shape scheme, label/leader design, clustered matrix, geo-fidelity bar chart, hero teaser), its accessibility for colour-vision-deficient, screen-reader and mobile users, and the pedagogical effectiveness of the three linked views and the Sydney/Melbourne/New York through-line. I inspected both files fully and exercised the live page (desktop/mobile, light/dark, layout switching, pinning, matrix hover).

**Recommendation**: **Minor Revision** · Confidence 4/5

**Scores (0–100)**: originality 68 · rigor 78 · evidence 86 · coherence 88 · writing 90

### Summary

This is an unusually well-crafted explorable explanation. The pedagogical architecture is exemplary: the four "How it works" cards carry one concrete trio (Sydney/Melbourne/New York) from raw context sentences through real 300-d vector stripes, real measured angles, and an honest to-scale trilateration, and card 3's caveat ("the gap you see... is not their real angle") pre-teaches the central epistemic lesson of the whole page. The three linked views with shared cutoff and selection are genuinely coordinated, the geo-fidelity bar chart is a model of honest statistical graphics (full 0–1 axis, dashed measured baseline, min–max whisker explicitly labelled "not a confidence interval"), and the concrete Madrid/Barcelona/Lisbon pair cards make an abstract rank correlation tangible. Disclosure of limitations (Stress-1 .347, "read neighbours from the ranking, not the map", post-alignment axis correlations "descriptive only") is exceptional for the genre, and the MEXICO_CITY dateline artefact is a superb data-provenance lesson. The weaknesses sit squarely in my remit: the region encoding assigns the same triangle marker to Europe and Oceania, breaking the shape redundancy exactly where the amber/brown colour pair is weakest for colour-vision-deficient readers; the equirectangular network draws straight, non-wrapping segments so trans-Pacific links (Auckland–Vancouver, cos .44) render the long way around the Earth; screen-reader semantics are internally contradictory (focusable markers inside role="img" SVGs, a canvas matrix with no non-visual alternative); and small light-mode caption text measures 3.8:1 contrast. All are localized and fixable. Minor revision.

### Strengths

**S1: A model pedagogical through-line built from real data**

The four cards reuse one real trio end-to-end: card 1's swap-a-city news sentences ("storms lashed Sydney/Melbourne"), card 2's actual 300-d vectors as heat stripes ("Melbourne's stripes match Sydney's far more often than New York's do — that shared pattern is the similarity"), card 3's arrows "drawn at its real, measured angle to Sydney", and card 4's exact trilateration "distances ∝ 1 − cos". Nothing is a cartoon; every number on screen is the real measurement. Card 3's ex-note ("the gap you see between Melbourne and New York (≈41°) is not their real angle... cos .26, θ ≈ 75°") is the best single teaching move on the page — it makes the projection's dishonesty visible before the reader ever meets MDS.

**S2: Honest, well-designed statistical graphics**

The geo-fidelity bar chart uses the full 0–1 correlation scale, an outlined (not filled) bar for the raw 300-d baseline, a dashed reference line, and in-chart annotations ("UMAP whisker = min–max over 12 seeds · others deterministic"); the prose explicitly warns the whisker is "not a confidence interval" and that the narrowest margin is ".004... a strong tendency, not a law". The link-count minichart discloses its log scale and marks "default 0.50 → 454". This is Tufte-grade restraint rare in interactive explainers.

**S3: Genuinely coordinated multiple views with disclosed reading rules**

One cutoff slider and one selection drive both maps and the drawer; the callouts state each view's positional semantics crisply ("Here position is real geography..." vs "Here position is similarity itself..."), and the Tobler framing ("mostly the law wins, and the exceptions are the interesting part") gives the geographic network an actual question to answer rather than decoration. The instruction to "read exact neighbours from the pinned ranking, not the pixels" correctly subordinates the layout to the data.

**S4: Data-provenance lessons of real instructional value**

The MEXICO_CITY dateline-register artefact ("dateline tokens keep company with other datelines, so their cosines run uniformly low"), the St Petersburg Florida collision (cos to Tampa .68 vs Moscow .60), and Lisbon's Treaty-of-Lisbon drift teach students that embedding geometry inherits corpus register and sense-collision — exactly the provenance scepticism data-science courses struggle to convey. The README's vocabulary-resolution notes make these reproducible claims, not anecdotes.

**S5: Real, partial accessibility effort**

The page is not accessibility-naive: prefers-reduced-motion is honoured, focus-visible outlines are styled, the layout switcher is a proper roving-tabindex radiogroup with arrow-key support, region chips carry aria-pressed, markers are Tab-focusable with Enter-to-pin, Escape closes the drawer, and both charts and the SVG figures carry substantive aria-labels (the gfchart's label narrates the entire result). This is a foundation worth finishing (see weaknesses), not a retrofit.

### Weaknesses

**W1: Europe and Oceania share the same map marker, and colour-only fallbacks undermine the redundant encoding** — *Major*

- **Problem**: In the REGION table both "Europe" and "Oceania" map to m: "tri" (upward triangle), distinguished only by amber #eda100 vs brown #8a5a2b — one of the least reliable hue pairs under deuteranomaly. Elsewhere the shape redundancy disappears entirely: the hero map draws colour-only circles for all 124 cities, and the clustered matrix encodes region with a 6px colour swatch and coloured name only.
- **Why it matters**: The nine-colour-plus-shape scheme is the page's main categorical encoding, and it is advertised implicitly as CVD-safe by being doubly encoded. A colour-blind reader comparing the semantic map's Oceania outliers to the European cluster — one of the page's own talking points ("Sydney & Melbourne... the tightest pair") — gets identical glyphs. ~4–8% of male readers are affected; for a teaching resource the audience is large.
- **Suggestion**: Give Oceania a unique marker (e.g., a star or ring; "pent" is already taken but a hexagon is free), and add shape glyphs to the hero map or state that it is decorative. For the matrix, prefix row names with the region glyph (the glyph() helper already exists) rather than relying on name colour alone.

**W2: Straight, non-wrapping edges on the equirectangular map misrepresent trans-Pacific proximity** — *Major*

- **Problem**: Edges are drawn as straight pixel segments in plate-carrée space with no antimeridian wrapping and no great-circle arcs. I verified from data/city_vectors.npy that Auckland–Vancouver = cos .442, Tokyo–Los Angeles = .374, Sydney–Los Angeles = .336 — all visible once the slider drops below ~.44 toward its .30 minimum, and each renders as a line spanning nearly the full map width (Auckland lon 174.8 → Vancouver −123.1 drawn across ~298° of longitude instead of ~62° across the Pacific).
- **Why it matters**: The callout explicitly asks readers to test Tobler's law — near things should be more related — using this picture. A Pacific-neighbour pair drawn as the longest line on the map visually inverts the very relationship the figure exists to display, and at high latitudes plate carrée already exaggerates E–W separations (e.g., Stockholm–Moscow). This is the one place the page's cartography actively fights its pedagogy.
- **Suggestion**: Split edges at the antimeridian (duplicate the segment exiting one edge and re-entering the other), or draw great-circle arcs (a 10-point interpolation is ~15 lines of JS). At minimum, add a sentence to Methodology step 10 acknowledging that link geometry is schematic and trans-Pacific links draw the long way round.

**W3: Screen-reader semantics are internally contradictory; the matrix has no non-visual pathway** — *Major*

- **Problem**: Both interactive SVGs are labelled role="img" ("World map of cities connected by semantic similarity") yet contain 124 tabindex="0" <path> markers each — ARIA treats descendants of role="img" as presentational, so assistive technology may announce a focus stop with no accessible context; the markers' aria-label is the bare city name with no role, no region, and no way to reach the tooltip content (no aria-describedby, no live region; the link-count readout also never announces changes). The 124×124 canvas matrix exposes only a single aria-label and is hover/click-only — no keyboard access at all — and the CSS still ships styles for a data table and <details> (".tblwrap", table.data, summary) that no longer exist in the markup, suggesting a tabular fallback was removed.
- **Why it matters**: For a venue publishing open educational resources, WCAG-level access is a review criterion, not polish. As shipped, a screen-reader user can read the excellent prose but cannot answer the page's central invitation ("select any city to light up its neighbours... and rank them in the side panel"), and a keyboard user must Tab through up to 248 markers with no skip link to pass the charts.
- **Suggestion**: Replace role="img" with role="group" on the two interactive SVGs (keep it on the static hero and gfchart), give markers role="button" and richer labels ("Dubai, Middle East & North Africa"), make the drawer a focus target when opened and announce it (aria-live="polite" on the drawer header or readout), and restore a visually-hidden or <details> ranked-list/table fallback for the matrix.

**W4: The layout switcher teleports; object constancy is lost exactly where it teaches most** — *Minor*

- **Problem**: applyLayout() rewrites viewBox and every transform attribute synchronously, so switching MDS → t-SNE is an instantaneous jump; the invitation "Switch the semantic map between MDS, PCA, t-SNE and UMAP to feel the difference" depends on the reader visually tracking cities between layouts, which a hard cut prevents. In dense t-SNE clusters (East Asia, Gulf) the pre-computed labels also collide at reading size.
- **Why it matters**: Animated transitions between projection layouts are the canonical device (Distill's t-SNE article, TensorFlow Embedding Projector) precisely because motion preserves object identity and lets learners see what each algorithm does to neighbourhoods — the page's own stated learning goal for this control. Without it, only pinned spotlights bridge the views.
- **Suggestion**: Interpolate marker/edge positions over ~600ms on layout change (positions are already in a common pixel space via PROJ; a requestAnimationFrame lerp suffices, and the existing prefers-reduced-motion rule can disable it). Consider per-layout label pruning where overlap exceeds a threshold.

**W5: Mobile interaction falls below usable target sizes and the bottom drawer occludes the evidence** — *Minor*

- **Problem**: At 375px width the geographic map renders ~340px wide, making markers roughly 3–4 css-px across (viewBox 1000/1080 units, marker radii 3.7 and 6) — far below the ~24px WCAG 2.5.8 / 44px HIG touch-target guidance — while all city labels are display:none under 640px; the pinned drawer then covers up to 46vh, hiding much of the map whose spotlight it describes. The full-ranking spotlight also draws all 123 lines (dashed down to opacity .05) on both charts, adding hairball noise on small screens.
- **Why it matters**: The lead instruction is "hover, tap or Tab to it"; on phones — likely the majority of casual readers for a shared teaching page — tapping a specific city is a lottery, and the search box becomes the only practical selector without being framed as such.
- **Suggestion**: Add an invisible enlarged hit area (transparent circle r≈12 viewBox units) around each marker, promote the search field / "Try:" buttons as the primary mobile pathway, cap spotlight lines to the top-N below-cutoff neighbours, and let the drawer start half-height with a drag handle.

### Questions for the author
1. Will you wrap edges at the antimeridian or draw great-circle arcs on the geographic network? At the slider minimum (.30) pairs like Auckland–Vancouver (cos .44) currently draw across ~298° of longitude — have you counted how many rendered edges cross the ±180° meridian?
2. Is the Europe/Oceania shared triangle marker deliberate (e.g., to keep shapes simple), and if so, what is the intended disambiguation for colour-vision-deficient readers on the semantic map and in the hero teaser?
3. What is the intended screen-reader experience for the two interactive SVGs (currently role="img" with focusable children) and the canvas matrix? The orphaned .tblwrap/table.data/details CSS suggests a tabular fallback once existed — was it removed intentionally?
4. Have you observed learners or a class using the page? In particular, do readers discover that the layout switcher's instant jump loses track of individual cities, and do mobile users find the search box once tapping markers fails?

### Minor issues
- Light-mode --ink-3 (#7f7a72 on #f3f1ea) measures 3.77:1, below WCAG AA 4.5:1 for the 10–12px mono captions, stats lines, legend and heromap captions that use it (dark mode passes at 5.15:1); darkening it one step would clear AA.
- Dead CSS remains for removed components: .tblwrap, table.data, details/summary rules, and summary:focus-visible have no corresponding markup in docs/index.html.
- The page depends on Google Fonts and the KaTeX CDN; offline or CSP-restricted classroom use degrades (font fallbacks are fine, and the .math plain-text fallback is well handled — a note in the README's Run it section would suffice, or self-host).
- Matrix row labels render at 6px with 15-character truncation ("Ho Chi Minh Ci…"); consider 7px rows or full-name tooltips on the label gutter, and the 40px dendrogram gutter is too shallow to read merge heights — either widen it or describe it as ordinal only.
- The geographic network has no city labels at any cutoff (labels exist only on the semantic map and six on the hero), so static screenshots of the network — likely reuse by instructors — are unreadable; consider labelling the ~10 highest-degree hubs.
- The link-count readout ("454 links · strongest 6.0% of 7,626 pairs") never announces changes to assistive tech; aria-live="polite" on the .readout would fix it.
- The similarity heatmap's alpha-ramp legend swatches are hard-coded rgba over the page background; they track the canvas correctly in both themes, but a labelled continuous ramp with tick values (−.06, 0, .5, .86) would be more precise than four discrete chips.
- Hero-map dots are colour-only circles (no region shapes) — acceptable as decoration, but a one-word caption change ("coloured by region" → also naming the encoding used later) or shared glyphs would keep the encoding consistent from the first figure.

---

## Devil's Advocate Review

*The submission is unusually honest for the genre: it discloses the Procrustes circularity, labels the E-W/N-S correlations "descriptive only", distinguishes a min-max seed range from a confidence interval, self-rates its contributions as "small and specific", and ships a fully deterministic, reproducible pipeline whose numbers replicate exactly (I recomputed the raw-space baseline at .503 and Dubai's top-10 from the shipped arrays before running any counterfactual). As pedagogy — the four "How it works" cards, the three linked views, the worked geo-fidelity pair examples — it is genuinely excellent.*

### Strongest Counter-Argument

The page asks whether language can reconstruct a map and answers "partly, yes" on the strength of one number, geo-fidelity rho .57-.67. But that statistic cannot tell a map from a gazetteer. Recompute it from the authors' own shipped artifacts: collapse every city onto its region's centroid within each shipped layout — destroying all within-region geometry, leaving nine points — and geo-fidelity rises, not falls (MDS .574 to .706, PCA .599 to .705, t-SNE .644 to .681, UMAP .671 to .720). Do it with no hand labels at all, cutting the page's own average-linkage dendrogram at nine clusters, and t-SNE still improves (.644 to .670). The metric is 88% between-region pairs (6,693 of 7,626); within regions the layouts' correlation with geography is only .22-.33. So the flagship finding (1) — every projection beats the raw space — reduces to the textbook fact that t-SNE and UMAP exaggerate cluster separation, which the page itself concedes makes their between-cluster distances "stop being comparable"; yet those very distances constitute the metric that crowns them. The "denoising" explanation is a just-so story: "cluster quantization" explains the same ordering with fewer assumptions and survives the collapse test, which denoising does not. What the embedding demonstrably encodes is which region's discourse a city belongs to — a categorical fact — not geometry. Second, the sample is 124 world-famous cities hand-balanced across nine regions, a design that manufactures the very block structure the metric rewards, and token resolution was adjudicated against geographic ground truth (St Petersburg, Mexico City), contradicting "no geographic information enters at any point". Third, where the question is genuinely about information content, the right instrument — supervised probing — already exists and answers it better. The honest title would be: word2vec sorts famous cities into regional discourse communities; 2-D cluster plots make that sorting look like a map.

### CRITICAL (2)

**C1. [data-conclusion mismatch / metric construct validity (core-thesis challenge)]**

The headline metric cannot distinguish 'reconstructs a map' from 'recovers a categorical region label'. Empirically, a degenerate 9-point layout (each city moved to its region's centroid within the shipped layout coordinates) scores HIGHER geo-fidelity than every full 124-city layout (MDS .574->.706, PCA .599->.705, t-SNE .644->.681, UMAP .671->.720), and an entirely unsupervised variant (collapsing to k=9 clusters from the page's own average-linkage dendrogram, no region labels used) matches or beats the layouts (t-SNE .644->.670). Within-region geo-fidelity of the layouts is only .22-.33, and 6,693 of 7,626 pairs (88%) are between-region. Therefore geo-fidelity rho .57-.67 evidences regional co-membership, not map geometry — the within-region 'map' detail the page displays actually LOWERS its own score. The thesis 'Short answer: partly, yes' and contribution (1) both rest on a metric that a gazetteer would ace.

- *Location*: Semantic map section, 'How geographic is each layout? Each map is scored by geo-fidelity — the Spearman rank correlation, computed over all 7,626 city pairs'; 'What to notice' item 'The projections beat the raw space'; Related work, contribution '(1) The map is compared across projections... all four 2-D layouts reproduce geography better than the raw 300-d cosine distances'; README 'Related work' and Method step 8.
- *Field-norm boundary*: The dimensionality-reduction evaluation literature separates local from global structure preservation precisely because single aggregate distance-rank statistics are dominated by coarse cluster structure — e.g., the co-ranking / rank-based quality framework (Lee & Verleysen 2009, 'Quality assessment of dimensionality reduction: Rank-based criteria', Neurocomputing 72). But severity here does not rest on the norm: it rests on the reviewer-run collapse counterfactual computed from the submission's own shipped artifacts.
- *Evidence-crossing rationale*: Crosses the critical bar as a data-conclusion mismatch verified computationally, not rhetorically: I first replicated the canonical raw baseline (.503, exact) from data/city_vectors.npy + cities.CITY_LATLON, then ran the collapse test on output/layouts.json. A metric that improves when all fine-grained map structure is deleted cannot support the claim that fine-grained map structure was recovered; this undermines the hero answer, 'What to notice' item 6, and contribution (1) simultaneously.

**C2. [logic-chain break (internal contradiction) / confirmation bias in the 'denoising' explanation]**

The page concedes that for t-SNE and UMAP 'distances between clusters stop being comparable' (its stated price for recall@10 .71/.70), yet it crowns exactly these methods best 'on the geography question' using a metric composed 88% of between-cluster pairs — and then explains the result with an unfalsified 'denoising/concentration' narrative ('the projection... concentrates the geography that is, by shedding noise'). The rival explanation — t-SNE/UMAP exaggerate cluster separation and shrink within-cluster spread, mechanically aligning distance ranks with a region-dominated target — is never considered, although it predicts the observed ordering (neighbourhood > global > raw) equally well AND survives the collapse test that falsifies the denoising story (if projections concentrated geographic GEOMETRY, deleting within-region geometry should hurt the score; it helps).

- *Location*: Methodology, 'Alternative layouts (the switcher)': 'at the price that distances between clusters stop being comparable' followed in the same item by 'On the geography question... every 2-D layout beats that baseline'; Semantic map section, paragraph 'Why should squeezing 300 dimensions into 2 make the map more geographic, not less?'.
- *Field-norm boundary*: That t-SNE inter-cluster distances are not meaningful is an externally checkable norm: Wattenberg, Viégas & Johnson (2016), 'How to Use t-SNE Effectively', Distill (distill.pub/2016/misread-tsne) — 'distances between clusters might not mean anything'; UMAP's documentation carries the same caution.
- *Evidence-crossing rationale*: Critical because the contradiction is internal to the submission's own text — the same Methodology item declares between-cluster distances unreliable and then relies on them — and because the page presents the denoising mechanism with causal confidence ('the reason is that...') while its only support is the very result it purports to explain. The alternative mechanism is not hypothetical: it is quantified above (collapse raises every layout's score).

### MAJOR (5)

**M1. [premise contradiction / circularity in token resolution]**

Methodology step 1 asserts 'no geographic information enters the similarity computation at any point', but token resolution was adjudicated against geographic ground truth: St Petersburg's token was chosen because the commoner token 'is dominated by St. Petersburg, Florida (cos to Tampa .68 vs Moscow .60)'; MEXICO_CITY was 'tested and rejected' because it 'push[es] the city to the map's edge' while the composition 'places it correctly beside Monterrey and Guadalajara' (README) — 'correctly' is defined by real geography. Ho Chi Minh City -> Saigon was picked for having 'the right meaning'. The disclosed selection criterion for ambiguous cases is geographic plausibility of the outcome, so the headline geo-fidelity numbers are conditional on geography-informed curation. The categorical 'at any point' claim is false as stated; a fix is to weaken it to 'no coordinates enter the algorithms; analyst token choices in ~4 disclosed cases were validated against known geography' and, ideally, report geo-fidelity under the naive first-candidate resolver as a robustness row.

- *Location*: Methodology step 1 ('no geographic information enters the similarity computation at any point') vs step 3 bullets (Mexico City, St Petersburg, Ho Chi Minh City); README 'Vocabulary resolution notes' ('the composition places it correctly beside Monterrey and Guadalajara').
- *Field-norm boundary*: Standard preregistration/leakage norms: outcome-dependent analytic choices ('garden of forking paths', Gelman & Loken 2014, American Scientist) must be reported as such and the claim of no-leakage qualified.
- *Evidence-crossing rationale*: Major rather than critical because the affected cases are few, fully disclosed, and quantitatively bounded — but the contradiction is verbatim between two adjacent methodology items, and the unqualified 'at any point' is precisely the sentence a reader will quote.

**M2. [overgeneralization / sampling design manufactures the result]**

The title question 'Could language reconstruct a map of the world?' is answered from one embedding, one English news corpus frozen in 2013, and 124 hand-picked globally salient cities deliberately 'balanced across 9 regions rather than ranked by population' — a curation the page justifies aesthetically ('the map would lose most of the regions a general reader recognizes'). Region balancing constructs strong, evenly-sized continental blocks, which is exactly the structure the geo-fidelity metric rewards (see critical finding 1) and which t-SNE/UMAP amplify. The page's own cited literature (Konkol et al. 2017; Godey et al. 2024) shows the effect degrades sharply for less famous names and under-covered regions, so the sample sits precisely where the effect is strongest. No robustness check on an alternative sample (top-N by population, random cities, single-region subset) is reported. Fix: report geo-fidelity for at least one non-curated sample, or scope the thesis to 'world-famous cities in Anglophone news discourse'.

- *Location*: Header ('Could language reconstruct a map of the world?... Short answer: partly, yes'); Methodology step 2 ('deliberately balanced across 9 regions... a strict top-N by population would be dominated by Chinese and South-Asian metros'); README 'City list'.
- *Field-norm boundary*: External-validity convention that convenience samples selected partly for expected outcome legibility cannot ground population-level claims (standard treatment in Shadish, Cook & Campbell 2002, Experimental and Quasi-Experimental Designs, ch. 3 on construct and external validity).
- *Evidence-crossing rationale*: The confound is not speculative: region counts (Europe 24, North America 21 vs Oceania 5, verified from data/city_index.csv) show the balancing, and the critical-finding decomposition shows the metric is driven by exactly the between-region structure the balancing guarantees.

**M3. [cherry-picking / unoperationalized superlative with unverified causal gloss]**

'What to notice' states London 'is the European city that leans hardest towards the United States — a hub both news spheres share'. No operationalization is given, and the claim is fragile: by mean cosine to the North American cities, London (.31) edges Madrid (.30) and Stockholm (.29) by a hair; by maximum cosine to any North American city, Madrid and Paris (.49) beat London (.48). The attached causal story (shared news hub) is asserted, not shown — no evidence excludes the alternative that the 'London' token blends London, Ontario and financial-register 'City of London' usage. The same pattern of confident post-hoc narrative without corpus evidence recurs: Lisbon's offset attributed specifically to 'the Treaty of Lisbon' and Dubai's reach to 'trade and labour-migration links', with no nearest-word-neighbour or context analysis shown for either. Fix: state the operationalization, report the margin, and downgrade causal glosses to hypotheses (or show the vocabulary neighbours that support them).

- *Location*: 'What to notice', items 'The transatlantic hinge', 'Where the corpus bends the map', 'A city with a wide footprint'; README summary paragraph ('London sits between the US and Europe, Lisbon is pulled away from Iberia by Treaty-of-Lisbon coverage').
- *Field-norm boundary*: Severity rests on reviewer computation from data/city_vectors.npy (margins above), not on a field norm; where a norm is wanted, Konkol et al. (2017) — the page's own closest precedent — demonstrates that token-collision explanations must be tested, not narrated.
- *Evidence-crossing rationale*: A .01 margin under one plausible operationalization, reversed under another, cannot support a bolded superlative in the section titled 'A few things the map gets right'; the untested causal attributions are the page's only interpretive payload for its showcase anomalies.

**M4. [cherry-picked failure modes (confirmation bias in 'What to notice')]**

'What to notice' promises 'a few things the map gets right, and a few it gets wrong', but every showcased 'wrong' is a charming single-city anecdote with a tidy story (Lisbon/Treaty, St Petersburg/Florida). The two systematic failures the page's own numbers document — the default MDS view recovers almost no north-south structure (r = .17, 'even the single best rotation cannot lift... past r ≈ .21'), and within-region geometry is weak everywhere (recall that exact adjacency 'should be taken from the pinned similarity ranking, not from which dot looks closest') — never appear in the section a casual reader will actually read. The result is a curated impression that errors are quirky and local while the map is globally sound, when the quantitative picture is closer to the reverse: regions are sound, geometry is quirky. Fix: add one 'What to notice' item on the missing north-south axis and/or the weak within-region fidelity.

- *Location*: 'What to notice' (all six items) vs Methodology step 9 ('the MDS map recovers little north-south structure') and step 7 ('exact nearest neighbours should be taken from the pinned similarity ranking').
- *Field-norm boundary*: Severity rests on the internal asymmetry between the summary section and the submission's own methodology numbers; no external norm required.
- *Evidence-crossing rationale*: The information exists in the submission but is stratified by reader effort: confirmations and cute anomalies surface in the headline section, systematic weaknesses only in methodology fine print — the structural signature of confirmation bias even when nothing stated is false.

**M5. [question-instrument mismatch (alternative paths)]**

If the question is the title's — could language reconstruct a map? — the appropriate instrument is one that reads out the information content of the vectors (supervised probe, as in Konkol et al. 2017 and Barenholtz 2026, reported R² ≈ .8), not the behaviour of generic unsupervised 2-D projections. The page knows this ('a supervised probe... recovers geography far better') and correctly warns the two numbers are incommensurable, yet keeps the unsupervised layouts as the headline evidence and the probe as a caveat. Consequently the page's central quantitative result, contribution (1), is a statement about projection algorithms (which ones sharpen clusters), not about language — while the title, hero, and 'Short answer: partly, yes' claim the latter. The defense of retaining word2vec ('canonical teaching model... instructive quirks') justifies the embedding choice pedagogically but does not justify answering an information-content question with a projection-aesthetics measurement. Fix: either add a simple supervised readout on these same 124 vectors (a ridge regression to lat/lon with LOO-CV is a few lines and would directly answer the title), or reframe the title/hero to the question actually answered.

- *Location*: Header ('Could language reconstruct a map of the world?'); Related work, final paragraph ('read the gap as a direction, not a subtraction'); Methodology step 12 'Beyond word2vec'; README 'Related work'.
- *Field-norm boundary*: The probing literature the page itself cites (Konkol et al. 2017; Gurnee & Tegmark 2024) treats supervised regression to coordinates as the standard instrument for the information-content question — checkable in those papers' methods.
- *Evidence-crossing rationale*: Not merely a preference: the mismatch is what makes critical finding 1 possible, because an unsupervised layout scored by pairwise rank correlation is exactly the instrument that cannot separate map from gazetteer, whereas a supervised readout would.

### MINOR (7)

**M1. [conceptual overstatement]**

The denoising argument asserts geography 'is intrinsically two-dimensional (cities sit on a surface), so a 2-D layout is exactly the right shape to hold it' — but cities sit on a sphere, whose great-circle metric is not embeddable in the plane; no flat 2-D layout can represent global great-circle distances even in principle (Konkol et al. used a spherical 3-D target for exactly this reason, as the page's own Related work notes).

- *Location*: Semantic map section, paragraph 'Why should squeezing 300 dimensions into 2...'; echoed in Methodology step 8.

**M2. [misapplied benchmark]**

Kruskal's stress rule of thumb ('<.025 excellent, <.05 good, >.20 poor') was derived for nonmetric MDS stress and is cautioned against as an absolute benchmark by the page's own cited authority (Borg & Groenen 2005 discuss its unreliability across n and error models); applying it to a metric-SMACOF Stress-1 of .347 is loose, even though the qualitative 'heavily compressed' verdict is right.

- *Location*: Methodology step 7, 'By Kruskal's rule of thumb (<.025 excellent, <.05 good, >.20 poor)'.

**M3. [sourcing]**

The R² ≈ .8 supervised anchor — load-bearing for the page's closing 'map of discourse more than of the Earth' framing — rests on a single unreviewed 2026 arXiv preprint (Barenholtz), cited four times across page and README with no hedge about its review status.

- *Location*: Related work final paragraph; README 'Related work'; References, 'ref-barenholtz'.

**M4. [selective narration]**

Dubai's 'top ten reaches into Southeast Asia (Singapore, Kuala Lumpur) and South Asia (Karachi, Mumbai)' is accurate but omits Amman (#7) and Hyderabad (#9) from the recitation — Hyderabad being an acknowledged collision token sits awkwardly in the trade-and-migration story; the verified top-10 is Abu Dhabi, Jeddah, Doha, Riyadh, Singapore, Kuala Lumpur, Amman, Karachi, Hyderabad, Mumbai.

- *Location*: 'What to notice', item 'A city with a wide footprint'.

**M5. [untested causal gloss]**

'Australian cities are nearly interchangeable in world news' explains the Sydney-Melbourne cos .86 by a corpus property no one measured; with only 5 Oceania cities in the sample, 'tightest pair in the whole matrix' is also partly a sampling statement.

- *Location*: 'What to notice', first item.

**M6. [so-what of contribution (2)]**

The exhaustive triangle-inequality audit is, by the page's own adjacent numbers, consequence-free: the three transforms yield near-identical layouts (Procrustes disparity <= .005) and 'a nonmetric MDS would not distinguish them at all'; the 2-in-310,124 result is specific to these 124 curated vectors and licenses no general conclusion about 1 - cos. Fine as classroom rigor; overpitched as an empirical contribution 'rather than assumed'.

- *Location*: Related work, contribution '(2)'; Methodology step 5; README Method step 5.

**M7. [rhetorical framing]**

'Short answer: partly, yes' delivers the bolded verdict before any definition of what 'partly' means; given that the honest referent is 'region-level structure, weak within-region geometry, little latitude in the default view', the hero primes a stronger reading than the methodology supports.

- *Location*: Header, subtitle paragraph.

### Ignored alternative explanations
1. Cluster quantization, not denoising: t-SNE/UMAP exaggerate between-cluster separation and shrink within-cluster spread, mechanically aligning distance ranks with a region-dominated target; verified by the collapse test (region-collapsing every layout raises its geo-fidelity: MDS .574->.706, PCA .599->.705, t-SNE .644->.681, UMAP .671->.720; unsupervised k=9 collapse of t-SNE .644->.670).
2. Sampling artifact: the hand-balanced 9-region city list manufactures evenly sized continental blocks; on a population-ranked or random sample the projections-beat-raw ordering and the .57-.67 range could shrink or invert.
3. Categorical co-membership, not spatial gradient: shared country/league/institution co-mention predicts the cosine structure without any distance decay; the Tobler's-law framing may be decorative (within-region geo-fidelity of the raw space is only .33, and both within- and between-region correlations, .33/.35, sit far below the aggregate .503 — the aggregate is largely the two-tier near/far contrast).
4. Dimensionality matching: great-circle distance among 124 clustered cities is itself generated by a low-dimensional clustered structure, so any variance-shrinking 2-D projection of clustered data tends to gain rank correlation with it — a geometric artifact independent of 'geography surviving projection'.
5. London-as-hinge could be token polysemy (London, Ontario; financial-register 'City of London') rather than shared transatlantic news spheres; the margin over Madrid is .01 and reverses under max-cosine.
6. Lisbon's Iberian offset could reflect generally lower or differently-registered news salience of Portugal in an Anglophone corpus rather than Treaty-of-Lisbon coverage specifically; no context or neighbour-word evidence is offered for the Treaty mechanism.

### Missing stakeholder perspectives
- Non-Anglophone readers and non-English corpora (the 'language' of the title is one language's news register)
- Residents of under-sampled regions (Sub-Saharan Africa 12 and Oceania 5 of 124 cities)
- Populations of ambiguous-name cities conflated by the token (Santiago, Hyderabad)
- Small and global-south cities excluded by the >1M-plus-prominence filter
- Colour-vision-deficient learners relying on the region colour encoding
- Educators who would adopt the page (no learning-outcome evidence for the explorable format)

### Unexamined premise

That a pairwise distance-rank correlation between an unsupervised 2-D scatter and great-circle distances operationalizes 'reconstructing a map' at all. The entire argument assumes map-ness equals aggregate geometric agreement, but everything the page measures is equally consistent with a discrete regional taxonomy plus noise — and the page deploys no instrument capable of telling a map from a gazetteer (the collapse counterfactual shows its chosen instrument prefers the gazetteer).

### Observations (non-defects)
- All reviewer counterfactuals were computed read-only from shipped artifacts: /Users/ivan/projects/map_similarity_claude/data/city_vectors.npy, data/city_index.csv, output/layouts.json, and cities.CITY_LATLON, using the project venv; the canonical raw baseline replicated at .503 exactly and Dubai's top-10 matched the page verbatim before any adversarial test was run, so the collapse-test numbers should be treated as verified, not speculative.
- Reference ceiling for categorical knowledge: placing each city at its region's true geographic centroid (9 points, zero language input beyond the label) scores geo-fidelity .885, and a purely semantic version (each city assigned its region's mean word2vec vector) scores .815 — both far above the best layout's .67, quantifying how much headroom mere region identity commands under this metric.
- The page partially anticipates the strongest critique — it concedes t-SNE/UMAP inter-cluster distances 'stop being comparable', flags the Procrustes circularity, and hedges the denoising story with 'plausibly' in Related work — but the hedges never propagate to the hero, 'What to notice', or the contribution claims, which is where readers will form their beliefs.
- The MEXICO_CITY dateline-token artefact (contribution 3) is the submission's most defensible novel claim: concrete, checkable, and independent of the metric problems above; a devil's advocate has little purchase on it.
- If the author adds a single robustness figure — geo-fidelity of each layout after region collapse, alongside a supervised lat/lon readout on the same 124 vectors — the critical findings above would be either absorbed into the page's narrative or refuted; the fix is cheap relative to the damage the current framing invites.

---

## Editorial Decision Letter

**Decision: MAJOR REVISION** (re-review required)

Dear author,

Five independent reviewers have assessed your submission. All four scoring reviewers
recommend Minor Revision, with dimension scores averaging ≈80/100 (originality ≈69,
rigor ≈77, evidence ≈81, coherence ≈87, writing ≈88) and confidence 4/5 across the
board — on the numbers alone this would be a Minor Revision. The Devil's Advocate,
however, raised two CRITICAL findings that the editor has independently verified
against your own shipped artifacts, and by editorial policy a verified CRITICAL
precludes acceptance in the current form. Because both findings target the framing of
the central empirical claim rather than peripheral matters, the decision is Major
Revision. The required work is bounded — reframing, one robustness analysis, and
disclosure fixes; no new machinery — and the panel is unanimous that the revised piece
is likely to be a strong publication.

**What the panel agreed on (consensus).**
1. *The honesty and craft are exceptional for the genre* (all five seats). The
   Procrustes circularity disclosure, the min–max-not-a-CI whisker, the "not new,
   Konkol et al. established it more rigorously" positioning, and the card-3
   flattening caveat were singled out repeatedly. Every number spot-checked by any
   reviewer reproduced exactly.
2. *The flagship claim over-reaches its instrument* (DA CRITICAL 1–2; R1 W1, W2;
   EiC W3; R2 W3). Geo-fidelity is a single global rank correlation over pairs that
   are 88% between-region. Editor-verified counterfactual: collapsing every city to
   its region centroid — destroying all within-region geometry — RAISES geo-fidelity
   for every layout (MDS .574→.706, PCA .599→.705, t-SNE .644→.681, UMAP .671→.720).
   The metric therefore cannot distinguish "reconstructs a map" from "recovers a
   regional taxonomy", and the projections-beat-raw ordering is at least as
   parsimoniously explained by cluster quantization (t-SNE/UMAP exaggerating
   between-cluster separation — which the page itself warns about) as by the page's
   "denoising" story. R1 independently found the same weakness from the other side:
   under geographic neighbour recall and within-region correlation the raw space
   matches or beats the layouts.
3. *Instructional apparatus is missing for this venue* (EiC W1; R3 Q4; DA
   stakeholders): no stated audience, learning objectives, activities, or evidence
   of use.
4. *Small real bugs in the analysis periphery* (R1 W3): compute_intervals.py sweeps
   MDS under RANDOM initialization (sklearn's current default) while its docstring
   claims the shown classical-init configuration — the shipped intervals.json
   .496–.578 range is an init-sensitivity result, not a seed-stability confirmation;
   and the r ≈ .21 rotation-ceiling figure has no shipped script.

**Where the panel disagreed (arbitration).** The four scoring seats read the page's
extensive hedging as sufficient qualification; the Devil's Advocate showed the hedges
do not propagate to the hero ("Short answer: partly, yes"), "What to notice" ("Every
2-D layout reproduces real geography better…"), or the contribution claims. The
editor sides with the Devil's Advocate on scope: the qualifications exist but the
headline statements do not carry them, and the collapse counterfactual is decisive
that the current interpretation outruns the instrument. The DA's remaining challenges
(sample curation, token-resolution circularity vs the "no geographic information
enters" sentence, cherry-picked vignettes) were each grounded in computation or the
page's own text and are folded into the roadmap below.

**Specially flagged (iron rule): Devil's Advocate CRITICAL findings** —
(C1) geo-fidelity cannot distinguish map from gazetteer (region-collapse test, editor-
verified); (C2) internal contradiction: t-SNE/UMAP are crowned "most geographic" by a
metric composed 88% of exactly the between-cluster distances the page says "stop
being comparable" for those methods. Both must be substantively addressed — by
analysis and reframing, not wording alone — before re-review.

## Revision Roadmap (prioritized)

**REQUIRED — must be addressed for re-review**

R1. **Reframe contribution (1) and add the decomposition analysis** [DA C1, C2; R1 W1;
    EiC W3]. Qualify "every 2-D layout reproduces real geography better than the raw
    300-d distances" as a global-rank-correlation result dominated by between-region
    structure. Add a small robustness figure/paragraph: region-collapsed geo-fidelity
    per layout (the numbers above), within-region geo-fidelity (~.22–.33), and
    geographic neighbour recall — presenting "cluster quantization" as the parsimonious
    alternative alongside the (already hedged) denoising story. Propagate the
    qualification to the hero, "What to notice", Related work, and README.
R2. **Say what "partly, yes" means at first use** [DA M7, C-thread; EiC S1]: strong
    region-level structure; weak within-region geometry; little latitude recovery in
    the default view.
R3. **Resolve the "no geographic information enters" contradiction** [DA M1]: token
    resolution was adjudicated against geographic ground truth (St Petersburg, Mexico
    City); reword step 1 to disclose the adjudication criteria honestly.
R4. **Fix compute_intervals.py** [R1 W3]: sweep the shown classical-init configuration
    (or keep the random-init sweep and describe it accurately as init-sensitivity,
    citing it on the page); add the script to the README pipeline table; ship or drop
    the r ≈ .21 rotation-scan.
R5. **Add instructional apparatus** [EiC W1]: audience, 3–5 learning objectives, 2–3
    classroom activities, any evidence of use.
R6. **Accessibility/cartography majors** [R3 W1–W3]: unique Oceania marker + glyphs
    (or declared-decorative status) on the hero; antimeridian wrapping or a schematic-
    geometry disclosure for trans-Pacific links; role="group" + focus semantics for
    interactive SVGs and a non-visual pathway for the matrix.

**STRONGLY RECOMMENDED**

S1. City-level bootstrap for layout differences, or soften "never moves" to the tier
    level [R1 W2].
S2. Literature: add Mikolov et al. (2013 NAACL) country–capital analogies; a
    spatialization/cognitive-cartography citation at the distance-as-similarity
    promise; Gupta et al. (2015) beside Konkol; a DR-quality-metrics survey citation;
    fix the "echoes this map's weak north–south axis" category confusion; re-gloss
    Recchia & Louwerse (2014) [R2 W1–W4].
S3. Tier the Methodology prose (plain-language sentence per step; details in
    disclosures) [EiC W2].
S4. Hedge the Barenholtz (2026) preprint status; balance "What to notice" with the two
    systematic failures (N–S weakness, neighbour distortion); reweigh or
    operationalize the London-hinge and Dubai vignettes [DA M3, M4, minors].

**SUGGESTED**

G1. Bundle fonts/KaTeX for archival self-containment or state the guarantee accurately
    [EiC W4]. G2. Single-source the README/page methods [EiC W5]. G3. Hyperparameter
    sweep (perplexity, n_neighbors) [R1 W4]. G4. Animated layout transitions +
    mobile hit targets [R3 W4–W5]. G5. Kruskal rule-of-thumb wording [DA minor 2].

*Panel provenance: all five seats ran on the same model family (Fable); correlated-
error caveat applies. The editor independently re-verified the decision-critical
counterfactual (region collapse) and the compute_intervals.py init discrepancy before
issuing this decision.*
