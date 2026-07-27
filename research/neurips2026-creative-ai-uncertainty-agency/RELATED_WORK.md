# Related Work & Baseline Landscape

Compiled via web search (July 2026). Direct full-text fetch of arxiv.org, neurips.cc,
huggingface.co, semanticscholar.org, openreview.net, and paperswithcode.com was
**blocked by this session's egress policy** (proxy CONNECT denied with 403 on all of
them). Everything below is reconstructed from search-result snippets/abstracts, not
verified full text — **re-verify every claim against the primary PDF before citing in
the paper**, especially method details for "Every Painting Awakened" and the World
Models uncertainty paper, where only abstract-level detail was recoverable.

---

## 0. The venue itself just handed us the framing

The official call (confirmed via search snippet of the NeurIPS Conference account and
`aiweekly.co`'s coverage):

> "In its fourth year, NeurIPS 2026 Creative AI Track invites research papers and
> artworks that explore emerging applications, methods, and critiques of artificial
> intelligence and machine learning in art, design, and creative practice. Focusing on
> the theme of **Agency**, this year's track asks: how agency emerges, is exercised, is
> negotiated, and is contested through creative practice with AI. Agency may belong to
> an artist, a collaborator, a model, an audience, a platform, a community, or even a
> larger social and technical system, and may be asserted, delegated, shared, resisted,
> constrained, or redistributed."

Example questions explicitly listed as welcome:
- "How does AI change where creative agency begins, where it ends, and how it is
  recognized?"
- "Can an artwork reveal agencies that are hidden inside technical systems?"

**This is a near-exact match to our π(U) framing.** The policy — commit / diversify /
abstain — is a concrete, measurable answer to "where does the model's creative agency
begin and end," and the abstain branch is literally the system declining to assert
authority. Worth quoting/paraphrasing the call in the paper's intro to make the fit
explicit to reviewers who are scoring for thematic relevance.

**Dates (from search snippet):** submissions open June 30, 2026; deadline **August 3,
2026, AoE**; decisions ~September 18; camera-ready ~October 23. Verify these directly
at `neurips.cc/Conferences/2026/CallForCreativeAI` once fetchable — this is exactly the
kind of date that's worth confirming firsthand before committing to it.

---

## 1. Directly competing / closest prior systems (same task: paintings → motion)

### Every Painting Awakened: A Training-free Framework for Painting-to-Animation Generation
arXiv:2503.23736 (Mar 2025). Project page: painting-animation.github.io/animation
- **This is the closest existing system to our application domain** — it is literally
  "animate a real painting into video," which is our task minus the uncertainty/agency
  layer.
- Per the abstract snippet: training-free, image-to-video (**sees the painting
  directly**, unlike our text-only Wan2.1 setup), uses a pretrained image-refinement
  model to produce a synthetic proxy image from painting + prompt, then dual-path video
  score distillation sampling over both the real painting and the synthetic proxy to
  get two initial video latents, merged for the final generation. Reports improved
  text alignment while preserving painting fidelity, evaluated against unspecified I2V
  baselines (need full text for the exact metric/baseline list).
- **Positioning:** this paper optimizes for a single best output under artwork access.
  It has no notion of uncertainty, no multiple-interpretation exposure, no abstention —
  it always commits. That's exactly the gap our paper targets. It's the natural
  candidate for our **"Image-conditioned video baseline"** row (Section 8 of
  `EXPERIMENTAL_SETUP.md`), and/or the paper we most need to cite in the intro as "here
  is what fidelity-maximizing painting animation looks like without an agency layer."

### AnimatePainter: A Self-Supervised Rendering Framework for Reconstructing Painting Process
arXiv:2503.17029 (Mar 2025)
- Different task — reconstructs the *stroke-by-stroke painting process*, not motion
  implied by the finished scene. Cite as adjacent/related but not a baseline.

### Text-Guided Synthesis of Eulerian Cinemagraphs
arXiv:2307.03190
- Generates subtle looping motion from a still image + text (cinemagraph synthesis,
  not full video). Useful prior art for "motion from a static artwork + text," and a
  precedent for the idea that not all pixels/regions of a static image should be
  animated with equal confidence — could be cited when motivating
  $U_{\text{temporal}}$ region- or object-level extensions.

---

## 2. Uncertainty quantification in generative image/video models

### ⭐ Directional Concentration Uncertainty (DCU) — adopt this for $U_{\text{interpretive}}$
Chattopadhyay, Kennedy, Munikoti, Sarkar, Pazdernik (Pacific Northwest National
Laboratory). "Directional Concentration Uncertainty: A representational approach to
uncertainty quantification for generative models." arXiv:2602.13264 (Feb 2026).
**Venue, confirmed:** AISTATS 2026 workshop *"Towards Trustworthy Predictions: Theory
and Applications of Calibration for Modern AI"* (held May 5, 2026, Tangier, Morocco;
workshop site: calibration-workshop.github.io; OpenReview venue id
`aistats.org/AISTATS/2026/Workshop/Calibration_for_Modern_AI`) — a **workshop paper**,
not a full ICML submission as an earlier search pass had suggested. This matters:
workshop papers are shorter, typically less exhaustively evaluated, and often
non-archival, which means (a) treat the reported results as promising-but-preliminary
rather than a settled benchmark result, and (b) there is more open room for a full
paper to properly extend and validate DCU in a new modality/domain than there would be
if this were already a mature, fully-reviewed main-track result.

**Verbatim abstract (confirmed by the user directly against arxiv.org, since this
session cannot fetch arxiv.org itself):**

> In the critical task of making generative models trustworthy and robust, methods for
> Uncertainty Quantification (UQ) have begun to show encouraging potential. However,
> many of these methods rely on rigid heuristics that fail to generalize across tasks
> and modalities. Here, we propose a novel framework for UQ that is highly flexible
> and approaches or surpasses the performance of prior heuristic methods. We introduce
> *Directional Concentration Uncertainty* (DCU), a novel statistical procedure for
> quantifying the concentration of embeddings based on the von Mises-Fisher (vMF)
> distribution. Our method captures uncertainty by measuring the geometric dispersion
> of multiple generated outputs **from a language model** using continuous embeddings
> of the generated outputs without any task specific heuristics. In our experiments,
> we show that DCU matches or exceeds calibration levels of prior works like semantic
> entropy (Kuhn et al., 2023) and also generalizes well to more complex tasks in
> multi-modal domains. We present a framework for the wider potential of DCU and its
> implications for integration into UQ for multi-modal and agentic frameworks.

**This sharpens the novelty argument.** The paper's own demonstrated experiments are
on **language model** outputs. "Generalizes well to more complex tasks in multi-modal
domains" and "implications for integration into UQ for multi-modal and agentic
frameworks" are stated as the paper's discussion of *wider potential* — i.e. DCU's
authors are pointing at exactly the direction we'd be taking it (multi-modal, agentic),
not claiming to have already done it for video generation or tied it to an agency
policy. Two consequences:
1. **Applying DCU-style concentration UQ to video embeddings (our
   $U_{\text{interpretive}}$) is a genuinely open extension, not a re-run of their
   experiments** — worth stating plainly in the paper: "DCU was demonstrated on
   language model outputs; we are (to our knowledge) the first to instantiate it for
   video generation and to extend it to an externally-anchored correspondence setting."
2. **The "agentic frameworks" line is a gift for framing.** DCU's own authors name
   integration into agentic frameworks as future work they see as valuable but didn't
   do. Our $\pi(U)$ policy is precisely that — a UQ-driven agentic decision layer. Cite
   DCU's abstract directly when motivating $\pi(U)$: this paper is explicit that
   turning a concentration-based uncertainty score into agentic behavior is exactly
   where this line of work is headed, and we're the ones doing it, in a creative
   (artwork-to-video) rather than general-agent setting.

- **This is the paper to check, and the current draft of `EXPERIMENTAL_SETUP.md`
  §6.1 reinvents a weaker version of it.** DCU fits a **von Mises–Fisher (vMF)
  distribution** to the unit-norm embeddings of $K$ generated outputs (continuous
  embeddings, no task-specific heuristics) and reads uncertainty off the fitted
  **concentration parameter $\kappa$**: large $\kappa$ = tightly clustered samples =
  low uncertainty; small $\kappa$ = dispersed samples = high uncertainty. Estimation
  is via the standard vMF MLE, matching the mean resultant length $\bar R$ to
  $A_d(\kappa) = I_{d/2}(\kappa)/I_{d/2-1}(\kappa)$ (ratio of modified Bessel
  functions), solvable numerically or via the closed-form Banerjee et al. (2005)
  approximation $\hat\kappa \approx \bar R (d-\bar R^2)/(1-\bar R^2)$. Reported (on
  language-model outputs) to match or exceed the calibration of semantic entropy
  (Kuhn et al., 2023), with no modality-specific heuristics required by construction —
  see the verbatim abstract below for exactly what is demonstrated vs. proposed as
  future direction.
- **Why this matters for us:** our current $U_{\text{interpretive}}$
  ($\frac{2}{K(K-1)}\sum_{a<b}[1-\cos(z_a,z_b)]$, §6.1) is a crude moment of exactly
  the same underlying object DCU models properly — the dispersion of $K$ unit-norm
  embeddings on a hypersphere. Pairwise-average cosine distance only captures
  second-order structure and has no statistical interpretation; $\kappa$ is a proper
  sufficient statistic of a well-defined directional distribution, with known
  estimation theory and (per their results) demonstrated calibration against a
  hallucination-detection ground truth. **Recommendation: replace the naive pairwise
  formula with DCU's $\hat\kappa$-based estimator as the primary
  $U_{\text{interpretive}}$ definition**, and keep the pairwise-cosine version only
  as an ablation baseline to show DCU is an improvement, not just a different choice.
- **A further extension DCU doesn't cover, and we should propose as our own
  contribution:** DCU characterizes dispersion of a sample set around its own mean
  direction. It does **not** address the artwork-correspondence signal
  ($U_{\text{art}}$, §6.2), which needs the *direction from a fixed external
  reference* (the hidden artwork embedding $f_I(I)$), not from the sample mean. A
  natural extension is a **directional-concentration analog for correspondence**:
  fit a vMF (or a von Mises–Fisher regression / directional residual) to the $K$
  video embeddings around the *artwork's* direction rather than their own mean, and
  read off both the mean cosine similarity to $I$ (≈ our $F_{\text{art}}$) and a
  concentration parameter around that external anchor (≈ a principled replacement
  for $\operatorname{Var}(s_1,\ldots,s_K)$). This is a genuine, citable extension of
  DCU rather than a restatement of it — worth framing explicitly as such in the
  paper: *"we adopt DCU for interpretive uncertainty and extend its directional-
  concentration machinery to externally-anchored correspondence uncertainty, which
  DCU's single-distribution setting does not cover."*
- **Novelty implication:** since DCU already exists as a general, modality-agnostic
  representational UQ method, our contribution is **not** "a new way to measure
  embedding dispersion" — it's (a) adopting DCU properly instead of the ad hoc
  formula, (b) extending it to the externally-anchored correspondence case, and (c)
  everything downstream of the uncertainty numbers: the semantic/temporal signals,
  the artwork-blind vs. artwork-visible asymmetry, and above all the agency policy
  $\pi(U)$ that acts on the resulting uncertainty. Say this explicitly in the paper
  to preempt a reviewer citing DCU against us.
- **Caveat:** only abstract/method-level detail was recoverable via search (arXiv
  itself is blocked from this session, as with everything else in this document) —
  confirm the exact estimator, the multi-modal experiments they actually ran (does
  "multi-modal" include vision, or is it multiple *text* modalities/tasks?), and
  whether they release code, before committing to adopting it wholesale.

### Semantic entropy (the method our $U_a$ is descended from)
Farquhar, Kossen, Kuhn, Gal. "Detecting hallucinations in large language models using
semantic entropy." *Nature* 630, 625–630 (2024).
- Origin of "entropy computed over meaning-clusters, not token sequences" for LLMs:
  sample completions, cluster by semantic equivalence, compute entropy over cluster
  membership.
- **Our $U_a$ (Section 6.3 of the experimental setup) is a cross-modal adaptation**:
  instead of clustering free-text LLM completions, we use a VLM to *directly elicit* a
  categorical distribution over a fixed attribute schema (subject, color, composition,
  emotion, style, motion) for each generated video, and take entropy over that. This is
  a meaningfully different design (closed-set attribute elicitation vs. open-set
  clustering) and should be framed explicitly as such — it's simpler and more
  interpretable but assumes the attribute schema is expressive enough, which is a
  limitation worth stating.

### Generative Uncertainty in Diffusion Models
Franchi et al., UAI 2025. arXiv:2502.20946.
- Decomposes diffusion-model uncertainty into aleatoric (irreducible, data-generating)
  and epistemic (model/parameter, from limited training data) components.
- **Relevant distinction for us:** our $U_{\text{interpretive}}$ is closer to their
  *aleatoric* notion (variability across seeds under one fixed, frozen Wan2.1) — we are
  not estimating epistemic/parameter uncertainty (would require ensembles of
  differently-trained Wan checkpoints, which we don't have). Worth one sentence in
  related work clarifying we measure stochastic/interpretive variance, not model
  uncertainty in the classical Bayesian sense — reviewers who know this literature will
  ask.

### DECU (Diffusion Ensembles for Capturing Uncertainty)
Berry et al., "Shedding/Casting Light on Large Generative Networks: Estimating
Epistemic Uncertainty in Diffusion Models." arXiv:2406.18580.
- Ensemble-based epistemic UQ for diffusion models via Pairwise-Distance Estimators.
  Different problem (epistemic, needs ensembles) but same broad area — cite as related
  technique, note we deliberately avoid needing multiple trained checkpoints.

### EMoE: Training-Free Expert Disagreement for Uncertainty-Aware Text-to-Image Diffusion
arXiv:2505.13273 (2025)
- **Methodologically close to us**: training-free UQ via disagreement, no retraining
  needed. Currently text-to-image only. Worth checking full text for whether their
  disagreement signal could substitute or complement our
  $U_{\text{interpretive}}$/$U_{\text{semantic}}$ computation, and citing as the T2I
  analog of what we're doing for T2V.

### World Models That Know When They Don't Know — Controllable Video Generation with Calibrated Uncertainty
arXiv:2512.05927 (2025)
- **Closest existing paper combining "uncertainty" + "video generation" + a form of
  behavior change** ("calibrated uncertainty" implies the system's confidence estimate
  is validated against outcomes, which is exactly what our RQ2/calibration-curve
  analysis in §9.1 of the experimental setup should emulate methodologically).
- Framed as a "world model" / controllable-generation paper, which reads as a
  robotics/planning/decision-making context rather than a creative/artistic one —
  **need full text to confirm**, but if so, this is the single most important paper to
  cite as "uncertainty-calibrated video generation has been studied for control; we are
  the first (to our knowledge) to study it for creative interpretive authority over
  human artwork." That contrast is a strong novelty sentence if the domain split holds
  up after reading the actual paper.

### Diverse Video Generation with Determinantal Point Process-Guided Policy Optimization
arXiv:2511.20647 (2025)
- Treats diversity as an explicit RL/policy-optimization objective (DPP-based) rather
  than relying on incidental seed variation. **Actionable for us**: for the "expose
  multiple interpretations" branch of $\pi(U)$, naive random-seed sampling may not give
  maximally distinct interpretations. Worth an ablation: does DPP-guided sampling
  produce a *better* (more separable, more genuinely alternative) set of $k'$ videos
  than plain multi-seed sampling for the same $U$ budget? This could become a real
  secondary contribution rather than just a citation.

---

## 3. Selective prediction / abstention (grounds the three-way policy)

- El-Yaniv & Wiener (2010) — foundational risk-coverage tradeoff for selective
  classification.
- Geifman & El-Yaniv (2017) and the SelectiveNet line — deep networks with a learned
  rejection head; Deep Gamblers / Self-Adaptive Training — reject-class training.
- "Know When to Abstain: Optimal Selective Classification with Likelihood Ratios,"
  arXiv:2505.15008 (2025) — Neyman–Pearson-optimal selection functions, unifying prior
  post-hoc baselines.
- "Know Your Limits: A Survey of Abstention in Large Language Models," *TACL* (2025,
  MIT Press) — comprehensive taxonomy of *why*/*when*/*how* models should abstain,
  including the over-abstention failure mode (reward hacking toward excessive "I don't
  know").
- "The Art of Refusal: A Survey of Abstention in Large Language Models," arXiv:2407.18418.

**Positioning:** all of this literature is classification/QA-flavored — "abstain" means
"don't answer." Our third policy arm is the *generative* analog: "don't claim fidelity
to a specific human artwork," which is a materially different notion of abstention
(the system still produces output, just declines to assert it's a faithful
interpretation). This distinction — **abstention-from-a-claim vs. abstention-from-an-
answer** — is worth making explicit; it's a genuine conceptual contribution back to the
abstention literature, not just an application of it. Also flag the over-abstention
risk from the TACL survey directly in our limitations/threshold-calibration section
(§7 of the experimental setup) since it applies just as much to $\tau_1,\tau_2$
miscalibration.

---

## 4. Agency / co-creativity framing (HCI side — this is what makes the paper "Creative AI" and not just "ML")

### MOSAAIC: Managing Optimization towards Shared Autonomy, Authority, and Initiative in Co-creation
Issak, Rezwana, Harteveld. ICCC 2025. arXiv:2505.11481.
- Systematic review of 172 co-creativity papers, distilled into three control
  dimensions: **Autonomy, Authority, Initiative**.
- **This should be our theoretical anchor for "agency."** Map $\pi(U)$ explicitly onto
  their *Authority* axis: commit = system unilaterally exercises full interpretive
  authority; diversify = authority is shared (system proposes, human selects/weighs);
  abstain = authority is ceded back to the human entirely. This gives the paper a
  citable, established vocabulary for the agency claim instead of inventing one from
  scratch — reviewers in this track will likely know MOSAAIC or the co-creativity
  literature it's drawn from.

### Agency in Human-AI Collaboration for Image Generation and Creative Writing: Preliminary Insights from Think-Aloud Protocols
*Creativity Research Journal* (Dec 2025).
- Empirically identifies four dimensions of felt agency in human-AI creative
  collaboration: **creative self-efficacy, control over creative action, autonomy in
  the process, ownership of the product**.
- **Directly usable for the human-evaluation design (§9.2).** Instead of an ad hoc
  "trust" question, structure the trust/preference study around these four validated
  dimensions — e.g., does seeing the system abstain/diversify change the *human's*
  felt ownership over the final animated artwork, versus a single-seed system that
  silently commits? This turns our human study from a one-off preference check into
  something that speaks to an established construct.

### A User-centered Framework for Human-AI Co-creativity
CHI 2024 (dl.acm.org/doi/fullHtml/10.1145/3613905.3650929).
- General co-creativity/agency-and-control framework; secondary citation alongside
  MOSAAIC.

---

## 5. Evaluation metrics / embedding backbones (implementation choices for §5–6 of the experimental setup)

| Candidate | Role | Note |
|---|---|---|
| ViCLIP (InternVid, arXiv:2307.06942) | $f_V$ video embedding | ViT-L + spatiotemporal attention, contrastive video-text pretraining |
| InternVideo2 (arXiv:2403.15377) | $f_V$ alternative backbone | ~100M video-text pairs; use for the cross-backbone robustness check in §5/§9.3 |
| CLIP / SigLIP | $f_I$ image embedding | Standard choice for artwork-frame correspondence |
| CLIPScore | Auxiliary text-video alignment metric | Known weakness: unreliable on compositional prompts — don't rely on it alone |
| VQAScore (Lin et al.) | Alternative alignment metric | VQA-based, more robust to compositionality than CLIPScore |
| ETVA | Alternative alignment metric | Fine-grained question-generation-based text-video alignment |
| VBench | Auxiliary video-quality benchmark | 16 human-validated dimensions (subject consistency, temporal flickering, motion smoothness, etc.) — worth reporting a few dimensions alongside our custom metrics so reviewers can sanity-check generation quality isn't confounding the uncertainty numbers |
| Wan-Bench | Backbone's own benchmark | Dynamic quality / image quality / instruction-following — useful for confirming our corpus isn't hitting unusually low-quality generation regions of Wan2.1's behavior |

---

## 6. Wan2.1 backbone — correct citation

Wang et al. (Wan Team, Alibaba), "Wan: Open and Advanced Large-Scale Video Generative
Models," arXiv:2503.20314 (2025). Diffusion-transformer backbone, novel VAE, 14B and
1.3B variants, T2V and I2V modes, reported #1 on VBench at the time of release. This is
the correct primary citation for "Wan2.1" (the arXiv report title is just "Wan"; the
open-sourced checkpoints are versioned 2.1). Pin the exact checkpoint/commit hash used,
per §4 of the experimental setup — VBench rank will keep moving as newer Wan versions
ship, and reviewers may ask why an older checkpoint was used if a newer one existed at
submission time.

---

## 7. Gaps this leaves genuinely open (i.e., what's actually novel)

After this pass, nothing found combines all four of:
1. text-only (caption-mediated, artwork-blind) generation,
2. multi-family uncertainty estimation (interpretive + artwork-correspondence +
   semantic + temporal) evaluated jointly,
3. a discrete *behavioral* policy (commit/diversify/abstain) rather than just a
   reported confidence score, and
4. explicit grounding in the co-creativity "agency/authority" literature with a human
   study measuring felt agency, not just output quality.

The closest single papers each cover a subset: Every Painting Awakened covers the
domain (paintings→video) but not uncertainty or agency; World Models That Know When
They Don't Know covers calibrated video uncertainty but (apparently) not the creative/
agency framing or the abstain-from-a-claim distinction; MOSAAIC and the Creativity
Research Journal paper cover agency but not generative uncertainty. The paper's
contribution is the connective tissue between these three clusters — that's the pitch.
