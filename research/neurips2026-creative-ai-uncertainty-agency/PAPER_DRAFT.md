# Knowing When Not to Interpret: Uncertainty as a Boundary of Creative Agency in Text-to-Video Translation of Human Artwork

**Track:** NeurIPS 2026 Creative AI Track (theme: *Agency*) — Research Paper, 2–6 pages excluding references, OpenReview, deadline August 3, 2026 AoE.
**Format note:** structured to follow the standard NeurIPS paper template's section
order and required components (abstract, numbered sections, a Limitations section,
a Broader Impact/Ethics statement, and a NeurIPS-style paper checklist appendix), laid
out in Markdown since that's the working format — port directly into the official
`.tex` template (`neurips_2026.sty`) for the actual OpenReview submission. **Whether
the Creative AI Track requires double-blind anonymization was not confirmed** in
research for this document (see `RELATED_WORK.md` §0) — the author block below is a
placeholder pending that check.

**Authors:** *[REDACTED FOR REVIEW — confirm track anonymization policy before
submission]*

---

## How to auto-fill this document

Every quantitative cell in every table below is a placeholder token
`{{section.key}}`. The convention: run the experiment named in the "Source" line
directly under each table, write its output into a results file (e.g.
`results.json`) using the same dotted keys, then substitute — by hand or with a
one-off find/replace script — every `{{...}}` token for the matching value. No
numbers in this document are real; nothing below should be read as a result. A
consolidated punch-list of every placeholder and its source experiment is in
**Appendix C**.

---

## Abstract

When a text-to-video model receives only a caption of a human artwork — never the
artwork itself — how much authority should it exercise over the interpretation it
produces? We study this question using Wan2.1 on a corpus of {{corpus.n_artworks}}
captioned modern artworks, generating $K={{corpus.k}}$ independent seeds per caption
and measuring four kinds of uncertainty: *interpretive* (disagreement across the
model's own samples, estimated via a von Mises–Fisher concentration statistic),
*artwork-correspondence* (instability relative to the hidden original, visible only
to the evaluator), *semantic* (VLM-elicited entropy over structured artistic
attributes), and *temporal* (drift from the artwork's semantics over a generated
clip). We find that caption-only, artwork-blind uncertainty
{{abstract.rq2_headline_finding}} the model's correspondence instability to a hidden
ground truth it never observes ($r={{abstract.rq2_r}}$), and we use this predictive
signal to drive a three-way agency policy — commit, diversify, or abstain from a
fidelity claim — that a single-seed generator cannot express. The policy
{{abstract.rq4_headline_finding}} relative to a single-seed baseline, both in
automatic correspondence to the hidden artwork and in a pilot human study of felt
creative agency (self-efficacy, control, autonomy, ownership). We argue that
regulating *when* a system commits to an interpretation of human-authored artwork is
itself a mechanism of creative agency, not a reliability feature bolted onto one.

---

## 1. Introduction

**The venue's own question, answered literally.** NeurIPS 2026's Creative AI Track is
themed *Agency*; its call asks how AI changes "where creative agency begins, where it
ends, and how it is recognized," and whether "an artwork [can] reveal agencies that
are hidden inside technical systems." This paper studies a pipeline in which a
text-to-video model translates a *caption* of a human artwork into motion, never
seeing the artwork itself, while the evaluator does. The gap between what the model
can see (a sentence) and what it is being asked to reconstruct (a specific visual and
emotional artifact) is where "where does agency begin and end" becomes measurable: the
model's uncertainty about a caption it cannot verify against ground truth is a direct
proxy for how much interpretive authority it is entitled to exercise. A system that
silently commits to one stochastic sample as *the* animation of someone's painting
asserts authority it has not earned when the underlying interpretation is unstable.
We argue the right response is not better generation, but *regulated* generation — a
policy that knows when to stop pretending it knows.

**Contributions.**
1. A four-part uncertainty decomposition for caption-mediated artwork-to-video
   translation — interpretive, artwork-correspondence, semantic, temporal — separating
   *how much the model disagrees with itself* from *how much it happens to agree with
   a ground truth it never saw*.
2. An adoption and extension of Directional Concentration Uncertainty (DCU;
   Chattopadhyay et al., 2026) — previously demonstrated only on language-model QA and
   VQA outputs — as an estimator for interpretive uncertainty in *generated video*,
   plus a novel externally-anchored variant for correspondence uncertainty against a
   reference the model never sees, which DCU's own single-distribution formulation
   cannot express.
3. A discrete three-way agentic policy $\pi(U)$ — commit, diversify, abstain —
   converting continuous uncertainty into a visible creative-authority decision,
   distinguished from classical selective-prediction abstention (declining to
   *answer*) as declining to *claim fidelity* while still generating.
4. Grounding in an established co-creativity control framework (MOSAAIC's
   Autonomy/Authority/Initiative axes) and a human-evaluation design built on a
   validated instrument for felt creative agency.
5. Four research questions (§5) with automatic and human evaluation, plus two ablation
   studies (§6) isolating which design choices actually matter.

---

## 2. Related Work

**Painting-to-video generation.** "Every Painting Awakened" (arXiv:2503.23736, 2025)
is the closest existing system to our task: training-free image-to-video synthesis
that animates real paintings while preserving fidelity, via dual-path video score
distillation. It always commits to a single output with no notion of uncertainty or
graded authority — the gap this paper fills. Related but structurally different:
Eulerian cinemagraph synthesis (arXiv:2307.03190) and AnimatePainter
(arXiv:2503.17029, reconstructs the painting *process*, not the finished scene's
motion).

**Uncertainty in generative vision/video.** Diffusion-model UQ work (Franchi et al.,
UAI 2025; DECU, arXiv:2406.18580; EMoE, arXiv:2505.13273) targets text-to-*image*
generation, mostly aleatoric/epistemic estimation rather than a lever on system
behavior. The closest UQ-for-video precedent, C³ ("World Models That Know When They
Don't Know," arXiv:2512.05927, Princeton), trains dense subpatch-level calibrated
confidence for **robotic world models** (Bridge, DROID datasets) — physical-
plausibility hallucination in predicted frames, spatially localized within a frame.
Different failure mode, different granularity, different domain from ours
(cross-sample, artwork-semantic, not physical).

**Directional Concentration Uncertainty (DCU).** Chattopadhyay et al. (AISTATS 2026
workshop, arXiv:2602.13264) introduce a von Mises–Fisher concentration statistic over
generated-output embeddings as a heuristic-free alternative to semantic entropy,
demonstrated on QA and VQA (image+text input, text output). Its own stated future
direction — "integration into UQ for multi-modal and agentic frameworks" — is what
this paper does: instantiating it on generated-*video* output embeddings (unclaimed)
and extending it to an externally-anchored setting DCU cannot express.

**Selective prediction / abstention.** The classical lineage (El-Yaniv & Wiener;
SelectiveNet-era work; "Know Your Limits," *TACL* 2025) treats abstention as declining
to *answer*. Our third policy branch still generates a video; it declines to *assert
fidelity*. This is a distinct notion of generative abstention.

**Agency in co-creativity.** MOSAAIC (Issak et al., ICCC 2025, arXiv:2505.11481)
distills 172 papers into Autonomy/Authority/Initiative — commit = full interpretive
authority, diversify = shared authority, abstain = authority ceded to the human. A
2025 *Creativity Research Journal* study names four empirically-grounded dimensions of
felt agency — self-efficacy, control, autonomy, ownership — structuring our
human-evaluation design (§4.5) rather than an ad hoc trust question.

*(Full annotated bibliography with all details: `RELATED_WORK.md`.)*

---

## 3. Method

### 3.1 Problem setup

Given human artwork $I$, a human-written caption $C$ (no artist/title, to prevent
memorized-association shortcuts), and a fixed, version-pinned Wan2.1 checkpoint, we
generate $K$ independent videos $\mathcal V=\{V^{(1)},\dots,V^{(K)}\}$ from $C$ alone —
the model never observes $I$. The evaluator observes both $\mathcal V$ and $I$.

### 3.2 Four uncertainty signals

**Interpretive uncertainty** (DCU-based). Fit a von Mises–Fisher distribution to unit-
norm video embeddings $z_k=f_V(V^{(k)})$:
$$\bar R=\tfrac1K\big\|\textstyle\sum_k z_k\big\|,\quad
\hat\kappa\approx\frac{\bar R(d-\bar R^2)}{1-\bar R^2},\quad
U_{\text{interpretive}}=1/\hat\kappa.$$
A naive pairwise-cosine average ($U^{\text{pairwise}}_{\text{interpretive}} =
\frac{2}{K(K-1)}\sum_{a<b}[1-\cos(z_a,z_b)]$) is kept only as **Ablation A** (§6.1).

**Artwork-correspondence uncertainty.** With $s_k=\tfrac1T\sum_t\cos(f_I(I),
f_I(V_t^{(k)}))$: $F_{\text{art}}=\tfrac1K\sum_k s_k$ (mean fidelity),
$U_{\text{art}}=\operatorname{Var}(s_1,\dots,s_K)$ (stability). Also fit a directional
concentration around $f_I(I)$ as an *external* pole (rather than the sample mean) —
an extension DCU's single-distribution formulation has no mechanism for.

**Semantic uncertainty.** A VLM elicits $p_a(c)$ over structured attributes $a$
(subject, dominant color, composition, emotion, style, implied motion) per
generation; $U_a=-\sum_c p_a(c)\log p_a(c)$ — a closed-set, cross-modal descendant of
semantic entropy (Farquhar et al., *Nature* 2024).

**Temporal uncertainty.** $U_{\text{temporal}}=\tfrac1T\sum_t d(f_I(I),f_I(V_t))$,
plotted against frame index to reveal drift vs. stable misalignment.

### 3.3 The agency policy

$$\pi(U)=\begin{cases}\text{commit}, & U<\tau_1\\
\text{diversify}, & \tau_1\le U<\tau_2\\
\text{abstain from a fidelity claim}, & U\ge\tau_2\end{cases}$$

$U$ is computed **only** from caption-only, artwork-blind signals (interpretive +
semantic) — mirroring real deployment, where the artwork is never available at
decision time. $\tau_1,\tau_2$ are calibrated on a held-out split using oracle
$F_{\text{art}}/U_{\text{art}}$ *only to fit the thresholds*, never at evaluation
time. Mapped to MOSAAIC: commit asserts full authority, diversify shares it, abstain
returns it. Distinct from selective-classification abstention (system still
generates; declines a *claim*, not an *answer*); watch for over-abstention when
tuning $\tau_2$ (**Ablation B**, §6.2, targets exactly this).

---

## 4. Experimental Setup

*(Full implementation-level detail: `EXPERIMENTAL_SETUP.md`. Condensed here for
self-containedness.)*

**4.1 Corpus.** {{corpus.n_artworks}} public-domain/CC-licensed modern artworks,
stratified by movement, dominant subject, and implied dynamism, so both
high- and low-uncertainty regimes are populated (needed for RQ3). One human caption
per artwork under a fixed protocol; a small multi-caption subset (~50 artworks, 2–3
captions each) separates caption-authoring variance from generation variance. A 15%
calibration split is held out for fitting $\tau_1,\tau_2$ and never used in the
reported RQ1–RQ4 numbers.

**4.2 Generation.** Wan2.1 **14B**, fixed checkpoint (record commit/version hash),
$K={{corpus.k}}$ seeds/caption, fixed decoding hyperparameters (resolution, steps,
frame count $T$) across the whole corpus. Compute: 7× A100, sized from a required
first-step generation-time benchmark (published 14B timings span 8–20 min/video —
confirm before committing to final corpus size; see `EXPERIMENTAL_SETUP.md` §10.2).

**4.3 Embedding backbones.** $f_V$: ViCLIP (arXiv:2307.06942) or InternVideo2
(arXiv:2403.15377). $f_I$: CLIP/SigLIP. Report both an $f_V$ and an $f_I$ swap as a
robustness check — not a full ablation section, but included in RQ1/RQ2 tables as a
secondary column where feasible.

**4.4 Baselines.** Single-seed generation (no uncertainty); best-of-$K$ oracle
(artwork-visible selection — upper bound via selection alone); caption-only
uncertainty without a policy action; the UQ-aware agency policy (ours);
image-conditioned baseline (Wan I2V, or Every Painting Awakened directly if code is
available).

**4.5 Evaluation.** Automatic: correlation/calibration analysis (RQ2), per-attribute
ranking (RQ3), policy-branch correspondence stratification (RQ4a). Human: pilot pass
(~20–30 items, 2–3 raters given the timeline — see `EXPERIMENTAL_SETUP.md` §10.2)
scored on the four felt-agency dimensions (RQ4b), inter-rater agreement via
Krippendorff's α.

---

## 5. Results

*Each subsection is one research question. Every table is a placeholder — see
"How to auto-fill this document" above and Appendix C.*

### 5.1 RQ1 — How uncertain are text-to-video translations of artwork captions, and does it vary by signal type?

**Table 1. Corpus-level uncertainty summary.**

| Metric | Mean | Std | Median | IQR |
|---|---|---|---|---|
| $U_{\text{interpretive}}$ (DCU) | {{rq1.u_interp_dcu.mean}} | {{rq1.u_interp_dcu.std}} | {{rq1.u_interp_dcu.median}} | {{rq1.u_interp_dcu.iqr}} |
| $U_{\text{interpretive}}$ (pairwise, ref. only) | {{rq1.u_interp_pairwise.mean}} | {{rq1.u_interp_pairwise.std}} | {{rq1.u_interp_pairwise.median}} | {{rq1.u_interp_pairwise.iqr}} |
| $U_{\text{semantic}}$ (mean over 6 attributes) | {{rq1.u_semantic.mean}} | {{rq1.u_semantic.std}} | {{rq1.u_semantic.median}} | {{rq1.u_semantic.iqr}} |
| $U_{\text{temporal}}$ | {{rq1.u_temporal.mean}} | {{rq1.u_temporal.std}} | {{rq1.u_temporal.median}} | {{rq1.u_temporal.iqr}} |

> **Source (not yet run):** generate $K=8$ Wan2.1-14B samples per caption over the
> full pilot corpus (§4.1–4.2); compute all four metrics per Method §3.2; aggregate
> corpus-wide. Depends on: corpus finalized, generation-time benchmark complete.

**Table 2. Uncertainty stratified by art movement.**

| Movement | N | Mean $U_{\text{interpretive}}$ | Mean $U_{\text{semantic}}$ |
|---|---|---|---|
| {{rq1.strat.m1.name}} | {{rq1.strat.m1.n}} | {{rq1.strat.m1.u_interp}} | {{rq1.strat.m1.u_semantic}} |
| {{rq1.strat.m2.name}} | {{rq1.strat.m2.n}} | {{rq1.strat.m2.u_interp}} | {{rq1.strat.m2.u_semantic}} |
| {{rq1.strat.m3.name}} | {{rq1.strat.m3.n}} | {{rq1.strat.m3.u_interp}} | {{rq1.strat.m3.u_semantic}} |
| *(repeat per stratum in §4.1)* | | | |

> **Source (not yet run):** same generations as Table 1, grouped by the movement
> label assigned during corpus curation (§4.1).

**Figure 1 [PLACEHOLDER].** Histogram of $U_{\text{interpretive}}$ (DCU) across the
corpus, overlaid with the pairwise-cosine ablation distribution. *Source: same run as
Table 1; plot both estimators' densities on one axis.*

---

### 5.2 RQ2 — Does caption-only, artwork-blind uncertainty predict the model's (unobserved) disagreement with the hidden original artwork?

**Table 3. Correlation between caption-only uncertainty and oracle-only correspondence signals.**

| Predictor | Target | Pearson $r$ | Spearman $\rho$ | $p$ |
|---|---|---|---|---|
| $U_{\text{interpretive}}$ (DCU) | $U_{\text{art}}$ | {{rq2.interp_vs_uart.pearson}} | {{rq2.interp_vs_uart.spearman}} | {{rq2.interp_vs_uart.p}} |
| $U_{\text{interpretive}}$ (DCU) | $F_{\text{art}}$ | {{rq2.interp_vs_fart.pearson}} | {{rq2.interp_vs_fart.spearman}} | {{rq2.interp_vs_fart.p}} |
| $U_{\text{semantic}}$ | $U_{\text{art}}$ | {{rq2.sem_vs_uart.pearson}} | {{rq2.sem_vs_uart.spearman}} | {{rq2.sem_vs_uart.p}} |
| Combined ($U_{\text{interpretive}}+U_{\text{semantic}}$) | $U_{\text{art}}$ | {{rq2.combined_vs_uart.pearson}} | {{rq2.combined_vs_uart.spearman}} | {{rq2.combined_vs_uart.p}} |

> **Source (not yet run):** compute both caption-only signals and both oracle-only
> signals per artwork (needs $I$, evaluator-side only, per Method §3.1); correlate
> across the corpus (calibration split excluded, per §4.1). This is the load-bearing
> result for the whole paper — everything in §5.4/RQ4 depends on this correlation
> being real and directionally correct (higher $U$ → lower $F_{\text{art}}$ / higher
> $U_{\text{art}}$).

**Figure 2 [PLACEHOLDER].** $(F_{\text{art}}, U_{\text{art}})$ scatter, one point per
artwork, quadrants labeled (consistently distant / consistently aligned / unstable).
*Source: same computation as Table 3.*

**Figure 3 [PLACEHOLDER].** Reliability diagram: predicted caption-only uncertainty
(binned) vs. observed oracle-only correspondence instability. *Source: same
computation as Table 3, binned and calibration-curve-plotted.*

---

### 5.3 RQ3 — Which artistic properties are most vulnerable to uncertainty in caption-to-video translation?

**Table 4. Per-attribute semantic uncertainty ranking.**

| Rank | Attribute | Mean $U_a$ | Std | N artworks in top decile |
|---|---|---|---|---|
| 1 | {{rq3.rank1.attribute}} | {{rq3.rank1.mean}} | {{rq3.rank1.std}} | {{rq3.rank1.top_decile_n}} |
| 2 | {{rq3.rank2.attribute}} | {{rq3.rank2.mean}} | {{rq3.rank2.std}} | {{rq3.rank2.top_decile_n}} |
| 3 | {{rq3.rank3.attribute}} | {{rq3.rank3.mean}} | {{rq3.rank3.std}} | {{rq3.rank3.top_decile_n}} |
| 4 | {{rq3.rank4.attribute}} | {{rq3.rank4.mean}} | {{rq3.rank4.std}} | {{rq3.rank4.top_decile_n}} |
| 5 | {{rq3.rank5.attribute}} | {{rq3.rank5.mean}} | {{rq3.rank5.std}} | {{rq3.rank5.top_decile_n}} |
| 6 | {{rq3.rank6.attribute}} | {{rq3.rank6.mean}} | {{rq3.rank6.std}} | {{rq3.rank6.top_decile_n}} |

*(Rows correspond to the six attributes in Method §3.2: subject, dominant color,
composition, emotion, style, implied motion — ranked, not fixed to this order.)*

> **Source (not yet run):** VLM attribute elicitation over all $K\times N$
> generations (§4.1–4.2); compute $U_a$ per attribute per Method §3.2; rank by
> corpus-mean. Requires the inter-rater validation subset (50 artworks, 2 human
> annotators) to confirm VLM attribute distributions track genuine ambiguity, not VLM
> noise — report that agreement rate alongside this table.

**Table 4b. Attribute uncertainty × art movement interaction (if space permits).**

| Movement | Most uncertain attribute | Least uncertain attribute |
|---|---|---|
| {{rq3.interaction.m1.movement}} | {{rq3.interaction.m1.most}} | {{rq3.interaction.m1.least}} |
| {{rq3.interaction.m2.movement}} | {{rq3.interaction.m2.most}} | {{rq3.interaction.m2.least}} |

> **Source (not yet run):** same as Table 4, grouped by movement label.

---

### 5.4 RQ4 — Does the agency policy improve correspondence to the hidden artwork, and does it increase humans' felt creative agency?

**Table 5a. Automatic: policy-branch validity against oracle correspondence.**

| Policy branch | N (%) | Mean $F_{\text{art}}$ | Mean $U_{\text{art}}$ | Best-of-$K$ oracle $F_{\text{art}}$ | Single-seed baseline $F_{\text{art}}$ |
|---|---|---|---|---|---|
| Commit | {{rq4a.commit.n_pct}} | {{rq4a.commit.f_art}} | {{rq4a.commit.u_art}} | {{rq4a.commit.oracle_f_art}} | {{rq4a.commit.single_seed_f_art}} |
| Diversify | {{rq4a.diversify.n_pct}} | {{rq4a.diversify.f_art}} | {{rq4a.diversify.u_art}} | {{rq4a.diversify.oracle_f_art}} | {{rq4a.diversify.single_seed_f_art}} |
| Abstain | {{rq4a.abstain.n_pct}} | {{rq4a.abstain.f_art}} | {{rq4a.abstain.u_art}} | {{rq4a.abstain.oracle_f_art}} | {{rq4a.abstain.single_seed_f_art}} |

> **Source (not yet run):** apply the calibrated policy (§3.3) to the evaluation
> split; for each branch, report the oracle-only correspondence stats of the
> artworks that landed in it. A working policy should show: Commit branch ≈
> single-seed baseline quality (policy correctly identified "safe" cases); Diversify
> and Abstain branches show markedly worse single-seed $F_{\text{art}}$ than Commit
> (policy correctly identified "risky" cases the single-seed baseline would have
> mishandled).

**Table 5b. Human: felt creative agency, single-seed baseline vs. UQ-aware policy (pilot, small N).**

| Dimension (1–7 Likert) | Single-seed baseline (mean) | UQ-aware policy (mean) | Δ | $p$ |
|---|---|---|---|---|
| Creative self-efficacy | {{rq4b.self_efficacy.baseline}} | {{rq4b.self_efficacy.policy}} | {{rq4b.self_efficacy.delta}} | {{rq4b.self_efficacy.p}} |
| Control over creative action | {{rq4b.control.baseline}} | {{rq4b.control.policy}} | {{rq4b.control.delta}} | {{rq4b.control.p}} |
| Autonomy in the process | {{rq4b.autonomy.baseline}} | {{rq4b.autonomy.policy}} | {{rq4b.autonomy.delta}} | {{rq4b.autonomy.p}} |
| Ownership of the resulting artwork | {{rq4b.ownership.baseline}} | {{rq4b.ownership.policy}} | {{rq4b.ownership.delta}} | {{rq4b.ownership.p}} |
| Inter-rater agreement (Krippendorff's α) | {{rq4b.agreement.alpha}} | — | — | — |

> **Source (not yet run):** small pilot human study (~20–30 items, 2–3 raters given
> the Aug 3 timeline — see `EXPERIMENTAL_SETUP.md` §10.2), instrument = the four
> Creativity Research Journal (2025) dimensions, questionnaire structured per §4.5.
> **If this cannot be run before submission, replace this table with a stated
> instrument + protocol and mark RQ4b "instrumented, not yet run" rather than
> omitting it** — consistent with the track's stated openness to in-progress work.

---

## 6. Ablation Studies

### 6.1 Ablation A — Is DCU actually better than the naive pairwise-cosine estimator it replaces?

**Motivation.** §3.2 adopts DCU's von Mises–Fisher concentration estimator as the
primary $U_{\text{interpretive}}$ definition on the claim that it is more principled
than averaging pairwise cosine distances. This ablation tests that claim directly
rather than asserting it.

**Table 6. Estimator comparison.**

| Estimator | Corr. with $U_{\text{art}}$ (Pearson) | Corr. with $U_{\text{art}}$ (Spearman) | Corr. with VLM semantic-entropy cross-check | Relative compute cost |
|---|---|---|---|---|
| DCU ($\hat\kappa$-based, ours) | {{abA.dcu.pearson}} | {{abA.dcu.spearman}} | {{abA.dcu.vs_semantic}} | {{abA.dcu.cost}} |
| Naive pairwise-cosine | {{abA.pairwise.pearson}} | {{abA.pairwise.spearman}} | {{abA.pairwise.vs_semantic}} | {{abA.pairwise.cost}} |

> **Source (not yet run):** reuses the RQ2 correlation computation (Table 3) with
> $U_{\text{interpretive}}$ swapped for each estimator; compute cost measured as
> wall-clock time to compute the statistic given the same $K$ embeddings (should be
> near-identical — the comparison is about correlation quality, not speed). A
> supporting result, not the paper's headline — DCU should show a measurably higher
> correlation with the oracle-only correspondence signal than the pairwise baseline;
> if it does not, the paper needs to say so plainly and either keep the pairwise
> version as primary or explain the discrepancy.

---

### 6.2 Ablation B — Which uncertainty signal actually drives good agency decisions?

**Motivation.** $\pi(U)$ (§3.3) combines interpretive and semantic uncertainty into a
single trigger. This ablation isolates each component's individual contribution to
decision quality, and checks for the over-abstention failure mode flagged in the
abstention literature (§2).

**Table 7. Policy-trigger ablation.**

| Policy trigger signal | Decision appropriateness (human-judged, % appropriate) | Over-abstention rate | Under-commitment rate (false "commit") |
|---|---|---|---|
| Interpretive-only | {{abB.interp_only.appropriateness}} | {{abB.interp_only.over_abstain}} | {{abB.interp_only.under_commit}} |
| Semantic-only | {{abB.semantic_only.appropriateness}} | {{abB.semantic_only.over_abstain}} | {{abB.semantic_only.under_commit}} |
| Combined (ours) | {{abB.combined.appropriateness}} | {{abB.combined.over_abstain}} | {{abB.combined.under_commit}} |
| Random threshold (noise control) | {{abB.random.appropriateness}} | {{abB.random.over_abstain}} | {{abB.random.under_commit}} |

> **Source (not yet run):** recalibrate $\tau_1,\tau_2$ separately for each trigger
> variant on the same calibration split (§4.1); apply each variant's policy to the
> same evaluation artworks used in Table 5a; "appropriateness" and the two error
> rates are judged the same way as §4.5's human protocol, reusing the RQ4b rater
> pool if feasible within the timeline, otherwise a smaller dedicated pass. "Random
> threshold" control: thresholds fit on shuffled/permuted uncertainty labels, to
> confirm the combined signal outperforms chance, not just any threshold.

---

## 7. Discussion and Positioning

No existing work combines: (1) text-only, artwork-blind generation, (2) a
multi-family uncertainty decomposition evaluated jointly against a hidden ground
truth, (3) a discrete *behavioral* policy rather than a reported confidence number,
and (4) explicit grounding in the co-creativity agency/authority literature with a
felt-agency human study. Every Painting Awakened covers the application domain but
not uncertainty or agency; C³ covers calibrated video uncertainty but for robotic
world models; DCU covers principled representational uncertainty but for
language-model/VQA outputs and names "agentic frameworks" as future work without
building one; MOSAAIC and the Creativity Research Journal instrument cover agency but
not generative uncertainty. This paper is the connective tissue between all four
clusters — see `RELATED_WORK.md` §7 for the full gap analysis.

---

## 8. Limitations

- **Pilot scale.** {{corpus.n_artworks}} artworks and a small-or-deferred human study
  (§4.5, §5.4 RQ4b), against the 300–500-artwork, full-human-study design this idea
  calls for at full scale (see `IDEA.md`) — stated explicitly, not hidden.
- **Caption-ambiguity confound.** Interpretive uncertainty may partly reflect caption
  vagueness rather than model behavior; the multi-caption subset (§4.1) is a partial
  mitigation, untested at pilot scale.
- **VLM-as-judge circularity.** Semantic uncertainty (§3.2) and any VLM-based
  validation share a potential bias source; $U_{\text{art}}$ deliberately stays on
  CLIP/SigLIP embeddings, never VLM judgments, to avoid this.
- **Threshold overfitting / over-abstention.** $\tau_1,\tau_2$ calibrated on a
  held-out split only; the classical over-abstention failure mode applies directly
  and Ablation B (§6.2) is the paper's only direct check on it.
- **Single backbone family per role by default.** $f_V$/$f_I$ robustness swaps (§4.3)
  are secondary checks, not a full ablation, given the timeline.

---

## 9. Broader Impact and Ethics Statement

This work studies when a generative system should decline to assert fidelity to a
specific human artist's work — a mechanism intended to *reduce* overclaiming by AI
systems about human creative intent, not to automate artistic interpretation at
scale. Risks: (1) an uncertainty-aware system could still be deployed to generate
unauthorized derivative animations of copyrighted artwork even when it "honestly"
abstains from a fidelity claim — abstention is not consent, and this paper does not
address artist consent or attribution; (2) the corpus is restricted to public-domain/
CC-licensed artworks specifically to avoid contributing to this risk in the released
benchmark itself (§4.1); (3) the human study (§5.4 RQ4b) involves human raters — 
standard informed-consent and IRB/ethics-review practice applies and is not yet
confirmed for this pilot's timeline; flag this explicitly before running it.

---

## 10. Conclusion

Uncertainty is not agency. Agency is what a system does *because of* uncertainty —
whether it commits, diversifies, or steps back. By making that decision explicit and
measurable in a domain where a human artist's original intent is genuinely
unavailable to the model, this paper turns "how does AI change where creative agency
begins and ends" from the track's framing question into an experiment.

---

## References

- Chattopadhyay, Kennedy, Munikoti, Sarkar, Pazdernik. "Directional Concentration
  Uncertainty..." AISTATS 2026 Workshop, arXiv:2602.13264.
- [Princeton] "World Models That Know When They Don't Know: Controllable Video
  Generation with Calibrated Uncertainty." arXiv:2512.05927.
- "Every Painting Awakened: A Training-free Framework for Painting-to-Animation
  Generation." arXiv:2503.23736.
- "AnimatePainter: A Self-Supervised Rendering Framework..." arXiv:2503.17029.
- "Text-Guided Synthesis of Eulerian Cinemagraphs." arXiv:2307.03190.
- Farquhar, Kossen, Kuhn, Gal. "Detecting hallucinations in large language models
  using semantic entropy." *Nature* 630, 625–630 (2024).
- Franchi et al. "Generative Uncertainty in Diffusion Models." UAI 2025,
  arXiv:2502.20946.
- "Shedding/Casting Light on Large Generative Networks..." (DECU). arXiv:2406.18580.
- "EMoE: Training-Free Expert Disagreement..." arXiv:2505.13273.
- "Diverse Video Generation with Determinantal Point Process-Guided Policy
  Optimization." arXiv:2511.20647.
- El-Yaniv & Wiener. Foundational selective-classification risk-coverage tradeoff
  (2010).
- "Know When to Abstain: Optimal Selective Classification with Likelihood Ratios."
  arXiv:2505.15008.
- "Know Your Limits: A Survey of Abstention in Large Language Models." *TACL* (2025).
- "The Art of Refusal: A Survey of Abstention in Large Language Models."
  arXiv:2407.18418.
- Issak, Rezwana, Harteveld. "MOSAAIC..." ICCC 2025, arXiv:2505.11481.
- "Agency in Human-AI Collaboration for Image Generation and Creative Writing..."
  *Creativity Research Journal* (2025).
- "A User-centered Framework for Human-AI Co-creativity." CHI 2024.
- Wang et al. (Wan Team). "Wan: Open and Advanced Large-Scale Video Generative
  Models." arXiv:2503.20314.
- "InternVid..." (ViCLIP). arXiv:2307.06942.
- "InternVideo2..." arXiv:2403.15377.
- VBench, VQAScore, ETVA — see `RELATED_WORK.md` §5 for full citations.
- Supplementary agency/authorship discourse citations: `RELATED_WORK.md` §4.

---

## Appendix A — NeurIPS-style paper checklist (draft, unconfirmed against the Creative AI Track's actual required checklist)

| # | Question | Answer | Justification |
|---|---|---|---|
| 1 | Do the main claims match the abstract/intro? | {{checklist.q1.answer}} | {{checklist.q1.justification}} |
| 2 | Are limitations discussed? | {{checklist.q2.answer}} | Yes — §8 |
| 3 | Are assumptions/theory (if any) stated? | {{checklist.q3.answer}} | vMF/DCU assumptions in §3.2 |
| 4 | Are experiments reproducible (code, data, seeds)? | {{checklist.q4.answer}} | {{checklist.q4.justification}} — no code released yet |
| 5 | Is the corpus's license/copyright status stated? | {{checklist.q5.answer}} | Yes — §4.1, §9 |
| 6 | Are human subjects protections addressed? | {{checklist.q6.answer}} | §9 — flagged as unresolved for the pilot |
| 7 | Is compute/resource usage disclosed? | {{checklist.q7.answer}} | `EXPERIMENTAL_SETUP.md` §10.2 |

> **Note:** confirm the Creative AI Track's actual checklist requirements — this may
> differ from the NeurIPS main-track checklist. Not yet verified (arXiv/neurips.cc
> unreachable from the research session that produced this document).

## Appendix B — Reproducibility and Compute

Full detail: `EXPERIMENTAL_SETUP.md` (corpus protocol §3, generation setup §4,
embedding backbones §5, all four metric formulas §6, policy calibration §7,
baselines §8, evaluation protocol §9, compute budget and 7×A100/Wan2.1-14B pilot
sizing §10, risks §11, deliverables checklist §12).

## Appendix C — Master experiment checklist (every placeholder, one place)

| Placeholder group | Experiment required | Depends on | Status |
|---|---|---|---|
| `{{corpus.*}}` | Finalize corpus size/stratification after the generation-time benchmark | 7×A100 timing test (§4.2) | Not started |
| `{{rq1.*}}`, Fig. 1 | Generate $K=8$/caption over full corpus; compute all 4 uncertainty metrics; aggregate + stratify | Corpus finalized | Not started |
| `{{rq2.*}}`, Fig. 2, Fig. 3 | Correlate caption-only vs. oracle-only signals across corpus | RQ1 generations | Not started |
| `{{rq3.*}}` | VLM attribute elicitation over all generations + inter-rater validation (50-artwork subset, 2 annotators) | RQ1 generations | Not started |
| `{{rq4a.*}}` | Calibrate $\tau_1,\tau_2$ on 15% split; apply policy to eval split; stratify oracle stats by branch | RQ2 correlations (for calibration) | Not started |
| `{{rq4b.*}}` | Pilot human study (~20–30 items, 2–3 raters), four-dimension instrument, informed consent | Policy applied (RQ4a), rater recruitment | Not started — timeline-constrained, may ship as "instrumented, not run" |
| `{{abA.*}}` (Table 6) | Recompute RQ2 correlation with pairwise-cosine estimator swapped in; compare | RQ2 pipeline | Not started |
| `{{abB.*}}` (Table 7) | Recalibrate policy per trigger-signal variant + random control; re-run human appropriateness judgment | RQ4a/b pipelines | Not started |
| `{{checklist.*}}` | Fill once the actual Creative AI Track checklist requirements are confirmed | Track policy confirmation | Not started |

**Nothing in this document has been executed.** This file is the complete write-up of
the idea, method, and evaluation plan — not a report of results.
