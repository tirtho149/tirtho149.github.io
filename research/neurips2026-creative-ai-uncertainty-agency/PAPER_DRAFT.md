# Knowing When Not to Interpret: Uncertainty as a Boundary of Creative Agency in Text-to-Video Translation of Human Artwork

*Complete conceptual draft — no code, no results yet. Written so the actual submission
can be drafted directly from this document. Target: NeurIPS 2026 Creative AI Track
(theme: Agency), research-paper format, 2–6 pages excluding references, OpenReview,
deadline August 3, 2026 AoE. Companion documents: `RELATED_WORK.md` (full annotated
bibliography), `IDEA.md` (how the framing evolved across research passes),
`EXPERIMENTAL_SETUP.md` (implementation-level detail and the 7×A100 pilot compute
plan). Sections marked **[core]** are load-bearing for a 2–6 page paper; sections
marked **[if space permits]** are natural cuts for a shorter version.*

---

## Abstract *(~200 words, core)*

When a text-to-video model receives only a caption of a human artwork — never the
artwork itself — how much authority should it exercise over the interpretation it
produces? We study this question using Wan2.1 on a corpus of captioned modern
artworks, generating $K$ independent seeds per caption and measuring four kinds of
uncertainty: *interpretive* (disagreement across the model's own samples, estimated
via a von Mises–Fisher concentration statistic), *artwork-correspondence* (instability
relative to the hidden original, visible only to the evaluator, never to the model),
*semantic* (VLM-elicited entropy over structured artistic attributes), and *temporal*
(drift from the artwork's semantics over the course of a generated clip). We show that
caption-only, artwork-blind uncertainty predicts correspondence instability the model
itself never observes, and use this predictive signal to drive a three-way agency
policy — commit to one interpretation, expose several, or abstain from claiming
fidelity — that a conventional single-seed generator cannot express. Grounding this in
the co-creativity literature's Autonomy/Authority/Initiative framework, we argue, and
begin to test empirically, that regulating *when* a generative system commits to an
interpretation of a human-authored artwork is itself a mechanism of creative agency,
not a reliability feature bolted onto one.

---

## 1. Introduction *(core)*

**Opening move — lead with the venue's own question.** NeurIPS 2026's Creative AI
Track is themed *Agency*, and its call asks explicitly: "how does AI change where
creative agency begins, where it ends, and how it is recognized?" and "can an artwork
reveal agencies that are hidden inside technical systems?" This paper answers both
literally. We study a pipeline in which a text-to-video model translates a *caption*
of a human artwork into motion, never seeing the artwork itself — while the evaluator
does. The gap between what the model can see (a sentence) and what it is being asked
to reconstruct (a specific visual and emotional artifact) is exactly where the
question of "where agency begins and ends" becomes measurable rather than rhetorical:
the model's *un*certainty about a caption it cannot verify against ground truth is a
direct proxy for how much interpretive authority it is actually entitled to exercise.
A generative system that silently commits to one stochastic sample as *the* animation
of someone's painting is asserting an authority it has not earned when the underlying
interpretation is unstable. We argue the right response is not better generation, but
*regulated* generation: a policy that knows when to stop pretending it knows.

**Contributions:**
1. A four-part uncertainty decomposition for caption-mediated artwork-to-video
   translation — interpretive, artwork-correspondence, semantic, temporal — that
   separates *how much the model disagrees with itself* from *how much it happens to
   agree with a ground truth it never saw*.
2. An adoption and extension of Directional Concentration Uncertainty (DCU;
   Chattopadhyay et al., 2026) — previously demonstrated only on language-model QA and
   VQA outputs — as a principled, distribution-theoretic estimator for interpretive
   uncertainty in *generated video*, plus a novel externally-anchored variant for
   measuring correspondence uncertainty against a fixed reference the model cannot see.
3. A discrete, three-way agentic policy $\pi(U)$ — commit, diversify, abstain — that
   converts continuous uncertainty into a visible creative-authority decision,
   explicitly distinguished from classical selective-prediction abstention (which
   declines to *answer*) as declining to *claim fidelity* while still generating.
4. Grounding of this mechanism in an established co-creativity control framework
   (MOSAAIC's Autonomy/Authority/Initiative axes) and a human-evaluation design built
   on a validated instrument for felt creative agency, rather than an invented
   preference score.

---

## 2. Related Work *(core, condensed — full version in `RELATED_WORK.md`)*

**Painting-to-video generation.** "Every Painting Awakened" (2025) is the closest
existing system to our task: training-free image-to-video synthesis that animates
real paintings while preserving fidelity, via dual-path video score distillation. It
always commits to a single output and has no notion of uncertainty or graded
authority — precisely the layer this paper adds. Related but structurally different:
Eulerian cinemagraph synthesis (subtle looping motion from a still + text) and
AnimatePainter (reconstructing the *process* of painting rather than animating the
finished scene).

**Uncertainty in generative vision/video.** Diffusion-model UQ work (Franchi et al.,
2025; DECU; EMoE) decomposes or estimates uncertainty for text-to-*image* generation,
mostly in the aleatoric/epistemic sense rather than as a lever on system behavior. The
closest UQ-for-video precedent, C³ ("World Models That Know When They Don't Know,"
Princeton, 2025), trains dense subpatch-level calibrated confidence for
**robotic world models** (Bridge, DROID datasets), targeting physical-plausibility
hallucination in predicted frames — a different failure mode, a different modality of
uncertainty (spatial, within-frame), and a different domain (embodied control, not
human-artwork interpretation) from ours (cross-sample, artwork-semantic).

**Directional Concentration Uncertainty (DCU).** Chattopadhyay et al. (AISTATS 2026
workshop, "Calibration for Modern AI") introduce a von Mises–Fisher concentration
statistic over generated-output embeddings as a heuristic-free alternative to semantic
entropy, demonstrated on QA and VQA. Its own stated future direction — "integration
into UQ for multi-modal and agentic frameworks" — is precisely what this paper does:
we instantiate it on *generated video* embeddings (an unclaimed modality) and extend
it to an *externally-anchored* setting DCU's own single-distribution formulation
cannot express (dispersion around a fixed external reference — the hidden artwork —
rather than around the sample's own mean).

**Selective prediction / abstention.** The classical lineage (El-Yaniv & Wiener;
SelectiveNet; recent LLM abstention surveys) treats abstention as declining to
*answer*. Our third policy branch still generates a video; it declines to *assert
fidelity* to a specific artwork. This is a distinct notion of generative abstention
worth naming as such, not an application of the existing framework.

**Agency in co-creativity.** MOSAAIC (Issak et al., ICCC 2025) distills 172 papers
into three control dimensions — Autonomy, Authority, Initiative — giving us a citable
vocabulary: commit = the system holds full interpretive authority, diversify =
authority is shared with the viewer, abstain = authority is ceded back to the human.
A 2025 Creativity Research Journal study names four empirically-grounded dimensions of
*felt* agency in human-AI creative collaboration — self-efficacy, control, autonomy,
ownership — which structures our human-evaluation design (§4.3) rather than an ad hoc
trust question. Broader humanities/philosophy work on AI-art authorship (2025–26,
multiple venues, including a live Cambridge CFP on exactly this theme) situates the
paper's central claim within an active, contested, cross-disciplinary conversation the
Creative AI Track itself sits inside.

---

## 3. Method *(core)*

### 3.1 Setup

Given a human artwork $I$, a human-written caption $C$ describing it (without naming
artist or title, to prevent memorized-association shortcuts), and a fixed,
version-pinned Wan2.1 checkpoint, we generate $K$ independent videos
$\mathcal{V} = \{V^{(1)},\ldots,V^{(K)}\}$ from $C$ alone — the model never observes
$I$. The evaluator observes both $\mathcal{V}$ and $I$, which is what allows treating
correspondence-to-$I$ as a meaningful proxy signal rather than an arbitrary
cross-modal distance.

### 3.2 Four uncertainty signals

**Interpretive uncertainty** — how differently the model interprets its own caption.
Fit a von Mises–Fisher distribution to the unit-norm video embeddings
$z_k = f_V(V^{(k)})$ and read uncertainty off the fitted concentration:
$$\bar R = \tfrac1K\big\|\textstyle\sum_k z_k\big\|,\quad
\hat\kappa \approx \frac{\bar R(d-\bar R^2)}{1-\bar R^2},\quad
U_{\text{interpretive}} = 1/\hat\kappa.$$
This is DCU's estimator, adopted rather than reinvented; a naive pairwise-cosine
average is retained only as an ablation baseline to demonstrate the improvement.

**Artwork-correspondence uncertainty** — how unstable the model's outputs are
*relative to a ground truth it cannot see*. With $s_k = \tfrac1T\sum_t
\cos(f_I(I), f_I(V_t^{(k)}))$, report both the mean $F_{\text{art}} =
\tfrac1K\sum_k s_k$ (how close, on average) and $U_{\text{art}} =
\operatorname{Var}(s_1,\ldots,s_K)$ (how stable). These are conceptually
independent: low-mean/low-variance means consistently missing the mark, high-mean/
low-variance means reliable fidelity, high variance means the model is, in effect,
guessing differently each time. As an extension of DCU's own machinery, also fit a
directional concentration *around $f_I(I)$ as an external pole* rather than around the
sample mean, giving a principled alternative to the variance-based estimate — DCU has
no mechanism for an externally-anchored setting, so this is new.

**Semantic uncertainty** — a VLM elicits a categorical distribution over structured
artistic attributes (subject, dominant color, composition, emotion, style, implied
motion) for each generation; $U_a = -\sum_c p_a(c)\log p_a(c)$ per attribute. This is
a closed-set, cross-modal descendant of semantic entropy (Kuhn et al., 2023;
Farquhar et al., *Nature* 2024), which clusters open-set LLM text completions —
here we elicit a fixed schema directly instead of clustering free-form output.

**Temporal uncertainty** — whether alignment with the artwork degrades over the
clip: $U_{\text{temporal}} = \tfrac1T\sum_t d(f_I(I), f_I(V_t))$, plotted against
frame index to reveal whether generations start plausible and drift, or are unstable
throughout.

### 3.3 The agency policy

$$\pi(U) = \begin{cases}
\text{commit to one video}, & U < \tau_1\\
\text{show multiple interpretations}, & \tau_1 \le U < \tau_2\\
\text{abstain from a fidelity claim}, & U \ge \tau_2
\end{cases}$$

where $U$ is computed from the *caption-only, artwork-blind* signals
(interpretive + semantic) — the artwork is never available at policy-decision time,
mirroring real deployment. Thresholds $\tau_1,\tau_2$ are calibrated on a held-out
split by finding operating points that best separate the correspondence regimes
(consistently distant / consistently aligned / unstable) observed *only* on that
calibration split, where oracle access to $F_{\text{art}}, U_{\text{art}}$ is used
purely to fit the thresholds — never to inform the policy at evaluation time. Mapping
onto MOSAAIC's Authority axis: commit asserts full authority, diversify shares it,
abstain returns it to the viewer. This is deliberately distinct from
selective-classification abstention — the system still produces output; it declines a
*claim*, not an *answer* — and the classical over-abstention failure mode (reward
hacking toward excessive hedging) is an explicit risk to monitor when setting $\tau_2$.

---

## 4. Pilot Study *(core, scoped to the confirmed constraints)*

**Compute:** 7× A100 GPUs, Wan2.1 14B (quality prioritized over corpus breadth,
per the compute-budget analysis in `EXPERIMENTAL_SETUP.md` §10.2). Corpus target
~150–200 public-domain/CC-licensed artworks at $K=8$, sized from a required
first-step generation-time benchmark (published 14B timings range 8–20 min/video on
an A100, a 2.5× swing that determines corpus feasibility outright).

**Corpus:** stratified across art movement, dominant subject, and implied dynamism,
so the high- and low-uncertainty regimes are both populated (needed for RQ3).
Captions collected under a fixed protocol; a small multi-caption subset used to
separate caption-authoring variance from model-generation variance.

**Research questions and what the pilot must show:**
- **RQ1** (how uncertain are T2V translations of artwork captions?) — corpus-level
  distributions of $U_{\text{interpretive}}$ and $U_{\text{semantic}}$.
- **RQ2** (does artwork-blind uncertainty predict correspondence instability the
  model never observes?) — correlation between caption-only $U$ and oracle-only
  $U_{\text{art}}/F_{\text{art}}$; the calibration-curve result the whole policy
  depends on.
- **RQ3** (which artistic properties are most uncertainty-prone?) — per-attribute
  $U_a$ ranking, stratified by movement.
- **RQ4** (does the agency policy change felt creative agency, not just output
  quality?) — the RQ most constrained by the timeline: full multi-rater evaluation is
  not achievable in the pilot window, so this is either a small labeled-preliminary
  pass (~20–30 items, 2–3 raters, scored against the four validated agency
  dimensions) or explicitly presented as instrumented-but-not-yet-run, consistent
  with the track's stated openness to speculative/in-progress work.

**Comparisons:** single-seed generation (no uncertainty), best-of-$K$ oracle
(artwork-visible selection — upper bound on achievable fidelity via selection alone),
caption-only uncertainty without a policy action, the UQ-aware agency policy, and an
image-conditioned baseline (Wan I2V or, if code is available, Every Painting Awakened
directly) as the upper reference for what's achievable when the model *can* see the
artwork.

---

## 5. Positioning and Novelty *(core — this is the section a reviewer reads first)*

No existing work combines: (1) text-only, artwork-blind generation, (2) a
multi-family uncertainty decomposition evaluated jointly against a hidden ground
truth, (3) a discrete *behavioral* policy rather than a reported confidence number,
and (4) explicit grounding in the co-creativity agency/authority literature with a
felt-agency human study. Each nearby paper covers a strict subset, and — after this
research pass — every domain boundary is confirmed rather than assumed: Every
Painting Awakened covers the application domain but not uncertainty or agency; C³
covers calibrated video uncertainty but for robotic world models, not creative
interpretation; DCU covers principled representational uncertainty but for
language-model/VQA outputs, not generated video, and names "agentic frameworks" as
future work without building one; MOSAAIC and the Creativity Research Journal paper
cover agency but not generative uncertainty at all. This paper is the connective
tissue between all four clusters.

---

## 6. Limitations and Risks *(core, keep short in the actual submission)*

- **Caption-ambiguity confound:** interpretive uncertainty may partly reflect caption
  vagueness rather than genuine model behavior; the multi-caption subset is a partial
  mitigation, not a full solution at pilot scale.
- **VLM-as-judge circularity:** semantic uncertainty and any VLM-based validation
  share a potential bias source; correspondence uncertainty is kept on CLIP/SigLIP
  embeddings specifically to avoid this.
- **Threshold overfitting / over-abstention:** $\tau_1,\tau_2$ calibrated on a
  held-out split only; the abstention literature's over-abstention failure mode
  applies directly and is not yet stress-tested at pilot scale.
- **Pilot scope:** ~150–200 artworks and a small or deferred human study, versus the
  300–500-artwork, full-human-study design this idea calls for at full scale — stated
  explicitly as future work, not hidden.
- **Copyright:** artwork corpus restricted to public-domain/CC sources throughout.

---

## 7. Conclusion *(core)*

Uncertainty is not agency. Agency is what a system does *because of* uncertainty —
whether it commits, diversifies, or steps back. By making that decision explicit and
measurable in a domain where a human artist's original intent is genuinely
unavailable to the model, this paper turns "how does AI change where creative agency
begins and ends" from the track's framing question into an experiment.

---

## References *(compiled from `RELATED_WORK.md`; format for final submission)*

- Chattopadhyay, Kennedy, Munikoti, Sarkar, Pazdernik. "Directional Concentration
  Uncertainty: A representational approach to uncertainty quantification for
  generative models." AISTATS 2026 Workshop, arXiv:2602.13264.
- [Princeton] "World Models That Know When They Don't Know: Controllable Video
  Generation with Calibrated Uncertainty." arXiv:2512.05927.
- "Every Painting Awakened: A Training-free Framework for Painting-to-Animation
  Generation." arXiv:2503.23736.
- "AnimatePainter: A Self-Supervised Rendering Framework for Reconstructing Painting
  Process." arXiv:2503.17029.
- "Text-Guided Synthesis of Eulerian Cinemagraphs." arXiv:2307.03190.
- Farquhar, Kossen, Kuhn, Gal. "Detecting hallucinations in large language models
  using semantic entropy." *Nature* 630, 625–630 (2024).
- Franchi et al. "Generative Uncertainty in Diffusion Models." UAI 2025,
  arXiv:2502.20946.
- "Shedding/Casting Light on Large Generative Networks: Estimating Epistemic
  Uncertainty in Diffusion Models" (DECU). arXiv:2406.18580.
- "EMoE: Training-Free Expert Disagreement for Uncertainty-Aware Text-to-Image
  Diffusion." arXiv:2505.13273.
- "Diverse Video Generation with Determinantal Point Process-Guided Policy
  Optimization." arXiv:2511.20647.
- El-Yaniv & Wiener. Foundational selective-classification risk-coverage tradeoff
  (2010).
- "Know When to Abstain: Optimal Selective Classification with Likelihood Ratios."
  arXiv:2505.15008.
- "Know Your Limits: A Survey of Abstention in Large Language Models." *TACL* (2025).
- "The Art of Refusal: A Survey of Abstention in Large Language Models."
  arXiv:2407.18418.
- Issak, Rezwana, Harteveld. "MOSAAIC: Managing Optimization towards Shared
  Autonomy, Authority, and Initiative in Co-creation." ICCC 2025, arXiv:2505.11481.
- "Agency in Human-AI Collaboration for Image Generation and Creative Writing:
  Preliminary Insights from Think-Aloud Protocols." *Creativity Research Journal*
  (2025).
- "A User-centered Framework for Human-AI Co-creativity." CHI 2024.
- Wang et al. (Wan Team). "Wan: Open and Advanced Large-Scale Video Generative
  Models." arXiv:2503.20314.
- "InternVid: A Large-scale Video-Text Dataset..." (ViCLIP). arXiv:2307.06942.
- "InternVideo2: Scaling Foundation Models for Multimodal Video Understanding."
  arXiv:2403.15377.
- VBench, VQAScore, ETVA — video/text-video alignment evaluation metrics (see
  `RELATED_WORK.md` §5 for full citations).

*Supplementary/optional citations for intro framing (use 1–2 sentences' worth, not
more): agency/authorship discourse in AI art (ScienceDirect 2025/26, AI and Ethics
2025, Frontiers in Psychology 2026) — see `RELATED_WORK.md` §4 for full list.*

---

## What is NOT yet done (be honest about this in any actual submission)

- No code has been written; no generations have been produced; no numbers in this
  document are results — everything above is the fully-specified plan and framing.
- The required generation-time benchmark (`EXPERIMENTAL_SETUP.md` §10.2) has not been
  run, so the exact pilot corpus size is still provisional.
- Several cited papers (Every Painting Awakened, C³, DCU) are characterized from
  abstracts/summaries reconstructed via search, not full-text verification, except
  where the user directly supplied the primary text (DCU's abstract only).
- The NeurIPS 2026 Creative AI CfP dates/format are as reported by search results and
  the official NeurIPS X account, not independently fetched from
  `neurips.cc/Conferences/2026/CallForCreativeAI` (blocked from this session).
