# Knowing When Not to Interpret: Uncertainty-Aware Agency in Caption-to-Video Translation of Modern Art

**Target venue:** NeurIPS 2026 — Creative AI Track (theme: *Agency*; deadline Aug 3, 2026 AoE — verify against the primary CfP)
**Status:** Experimental design (pre-implementation)
**See also:** `PAPER_DRAFT.md` — the complete NeurIPS-template-shaped write-up
(abstract through appendices, RQ-specific results sections, two full ablation
studies, all tables as auto-fill placeholders with a defined `{{token}}` protocol —
**start here**), `RELATED_WORK.md` (full annotated bibliography), and `IDEA.md` (how
the framing evolved across research passes). This file is the implementation-level
detail behind `PAPER_DRAFT.md`'s Method and Experimental Setup sections.

---

## 1. Framing

Uncertainty itself is not agency. Agency appears when uncertainty *determines what the
system is permitted to do*: confidently interpret, expose alternatives, defer, or ask
for guidance. This document lays out the experimental plan for studying uncertainty in
the caption-mediated translation of human artwork into AI-generated video, and for
using that uncertainty to regulate the system's creative authority.

Pipeline under study:

```
Human-created artwork I
        ↓
Human-written caption C
        ↓
Wan2.1 samples V₁, V₂, …, Vₖ  (Wan2.1 never sees I)
        ↓
Uncertainty estimation (interpretive, artwork-correspondence, semantic, temporal)
        ↓
Agency policy π(U): commit / diversify / abstain
```

The evaluator sees `I`; Wan2.1 does not. This asymmetry is what lets us treat
"correspondence to the hidden artwork" as a proxy ground truth rather than a
similarity metric between two arbitrary modalities.

---

## 2. Research questions and what each experiment must produce

| RQ | Question | Required output |
|----|----------|------------------|
| RQ1 | How uncertain are T2V models when translating descriptions of modern artwork into motion? | Distribution of $U_{\text{interpretive}}$, $U_{\text{semantic}}$ across the corpus |
| RQ2 | Does generation uncertainty predict disagreement with the hidden original artwork? | Correlation between caption-only uncertainty and $U_{\text{art}}$ / $F_{\text{art}}$ |
| RQ3 | Which artistic properties (subject, composition, color, style, affect) are most vulnerable to uncertainty? | Per-attribute $U_a$ ranking, breakdown by art movement/genre |
| RQ4 | Can uncertainty-aware generation better regulate AI creative agency than single-output generation? | Human preference / trust study comparing $\pi(U)$ policy vs. single-seed baseline |

---

## 3. Data

### 3.1 Artwork corpus
- Source: public-domain / CC-licensed modern-art collections (e.g. WikiArt subset,
  museum open-access APIs) to avoid copyright issues in a published benchmark.
- Target size: **300–500 artworks** for a full future study; **~150–200 artworks for
  the Aug 3 pilot** given the 7×A100/Wan2.1-14B compute budget (§10.2) — pick the
  exact number only after the generation-time benchmark in §10.2 comes back.
  Stratified across:
  - movement (e.g. Cubism, Abstract Expressionism, Surrealism, Pop Art, Impressionism)
  - dominant subject (figurative vs. abstract vs. landscape vs. still life)
  - implied dynamism (static composition vs. gesture/motion-suggestive brushwork)
- Stratification matters directly for RQ3 — need enough abstract/ambiguous pieces to
  populate the high-uncertainty regime and enough clear figurative pieces to populate
  the low-uncertainty regime.

### 3.2 Captions
- One human-written caption per artwork, collected under a fixed protocol (e.g.
  "describe what is depicted and how it might move, in 1–3 sentences, without naming
  the artist or artwork title" — title/artist leakage would let the model shortcut via
  memorized associations rather than genuine visual grounding).
- Optionally collect **2–3 independent captions per artwork** from different annotators
  for a subset (~50 artworks) to separately measure *caption-authoring* variance vs.
  *generation* variance — this matters for correctly attributing uncertainty to the
  T2V model rather than to caption ambiguity upstream.

### 3.3 Splits
- No train/test split needed (no fine-tuning in the core study) — full corpus used for
  evaluation. Reserve a fixed 15% "calibration" subset for fitting policy thresholds
  $\tau_1, \tau_2$ (Section 7), held out from the numbers reported for RQ1–RQ4.

---

## 4. Generation setup

- **Model:** Wan2.1 (T2V). Primary citation: Wang et al., "Wan: Open and Advanced
  Large-Scale Video Generative Models," arXiv:2503.20314 (2025). Fixed
  checkpoint/version pinned and recorded for reproducibility — VBench rank shifts
  with newer Wan releases, so record exactly which checkpoint was used at
  submission time.
- **Samples per caption:** $K = 8$ (budget-permitting; $K=4$ as a fallback if compute is
  constrained — report results at both $K$ to show sensitivity of $U_{\text{interpretive}}$
  to sample count).
- **Seeds:** independently sampled random seeds per generation, same decoding
  hyperparameters (guidance scale, steps, resolution, frame count $T$) held fixed across
  the whole corpus so that variation is attributable to stochasticity, not
  hyperparameter drift.
- **Frame count:** fix $T$ (e.g. 16 or 24 frames) uniformly; store all frames for
  temporal-uncertainty analysis, not just a pooled clip embedding.

---

## 5. Embedding models (feature extractors)

Two roles need to be filled and should **not** share a backbone, to avoid inflating
correlations by shared-encoder artifacts:

- $f_V$ (video embedding, for interpretive uncertainty): a video-native encoder such as
  ViCLIP (trained on InternVid, arXiv:2307.06942 — ViT-L with spatiotemporal attention,
  contrastive video-text pretraining) or InternVideo2 (arXiv:2403.15377, ~100M
  video-text pairs) — pooled clip-level embedding.
- $f_I$ (image embedding, for artwork correspondence + temporal uncertainty): a
  vision-language image encoder such as CLIP / SigLIP, applied to the artwork and to
  each generated frame, then averaged over $t$ per Eq. in §6.2, or applied per-frame for
  the temporal-drift curve (§6.4).
- Report results with **at least two different encoder families** for $f_V$ and $f_I$ as
  a robustness check — uncertainty numbers that flip sign or rank under a different
  backbone would undercut the paper's central claims.
- For auxiliary text-video alignment sanity checks (not the core uncertainty metrics,
  but useful for confirming the corpus isn't sitting in an unusually low-quality
  region of Wan2.1's behavior), consider VQAScore or ETVA over plain CLIPScore — both
  are more robust to compositional prompts than CLIPScore, and VBench's 16
  human-validated dimensions are worth spot-reporting alongside the custom metrics.
  See `RELATED_WORK.md` §5 for the full comparison.

---

## 6. Uncertainty estimation — implementation plan

### 6.1 Interpretive uncertainty

**Primary estimator — adopt Directional Concentration Uncertainty (DCU; Chattopadhyay
et al., arXiv:2602.13264, AISTATS 2026 workshop "Calibration for Modern AI"; see
`RELATED_WORK.md` §2).** Fit a von Mises–Fisher
distribution to the $K$ unit-norm video embeddings $z_k = f_V(V^{(k)})$ and read
uncertainty off the concentration parameter:
$$\bar R = \frac{1}{K}\left\| \sum_{k=1}^K z_k \right\|, \qquad
\hat\kappa \approx \frac{\bar R (d - \bar R^2)}{1 - \bar R^2}, \qquad
U_{\text{interpretive}} = \frac{1}{\hat\kappa}$$
where $d$ is the embedding dimension and the $\hat\kappa$ approximation is the
closed-form MLE estimate (Banerjee et al., 2005); solve
$A_d(\kappa)=I_{d/2}(\kappa)/I_{d/2-1}(\kappa) = \bar R$ numerically instead if higher
precision is needed. Large $\hat\kappa$ (tightly clustered generations) → low
uncertainty; small $\hat\kappa$ (dispersed generations) → high uncertainty.

**Ablation baseline — naive pairwise dissimilarity** (what earlier drafts of this
document used as the primary definition; keep only to show DCU is an improvement):
$$U_{\text{interpretive}}^{\text{pairwise}} = \frac{2}{K(K-1)} \sum_{a<b} \left[1-\cos(z_a,z_b)\right]$$

- Computed per caption, over the $K$ generations.
- Report corpus-level distribution (histogram), and break down by art movement /
  abstractness label.
- Report both estimators' correlation with each other and, separately, each one's
  correlation with $U_{\text{art}}$ (RQ2) — this is the evidence for "DCU is a better
  interpretive-uncertainty estimator than the naive pairwise average," which should be
  a small, explicit result in the paper, not just a methods-section footnote.

### 6.2 Artwork correspondence uncertainty
$$s_k = \frac{1}{T}\sum_{t=1}^{T}\cos\!\big(f_I(I), f_I(V_t^{(k)})\big), \qquad
U_{\text{art}} = \operatorname{Var}(s_1,\ldots,s_K), \qquad
F_{\text{art}} = \frac{1}{K}\sum_{k=1}^{K}s_k$$
- Report the joint $(F_{\text{art}}, U_{\text{art}})$ scatter per artwork — this is the
  key plot for RQ2, with quadrants labeled (consistently distant / consistently aligned
  / unstable) as in the framing above.

**Secondary estimator — externally-anchored directional concentration.** DCU (§6.1)
models dispersion of $\{z_k\}$ around their *own* mean direction; it has no
externally-anchored variant. As an extension beyond DCU (see `RELATED_WORK.md` §2 for
why this is a genuine contribution rather than a restatement), fit the concentration
of the $K$ video embeddings around the *artwork's* direction $f_I(I)$ instead of their
own mean — i.e. treat $f_I(I)$ as the fixed pole and estimate $\hat\kappa_{\text{art}}$
from the resultant length of $\{z_k\}$ measured relative to that pole. Report
$1/\hat\kappa_{\text{art}}$ alongside $U_{\text{art}} = \operatorname{Var}(s_1,\ldots,s_K)$
as a robustness check — they should be highly correlated if the variance-based measure
is capturing genuine directional instability rather than an artifact of using scalar
cosine similarity.

### 6.3 Semantic uncertainty (VLM-elicited)
- Use a VLM (e.g. GPT-4V-class or open equivalent, fixed and documented) to classify
  each generated video (and the source artwork, separately) along structured attributes:
  subject/object presence, dominant color, composition, emotion, artistic style, implied
  motion.
- For each attribute $a$, collect the VLM's categorical distribution $p_a(c)$ either by
  (i) sampling the VLM $M$ times per video with temperature and taking empirical
  frequencies, or (ii) reading log-prob-derived distributions if available; document
  which is used since it changes what $U_a$ actually measures.
$$U_a = -\sum_c p_a(c)\log p_a(c)$$
- Aggregate $U_a$ across the $K$ generations per caption (mean and max) and across the
  corpus, ranked to directly answer RQ3.
- Include an inter-rater check: for a 50-artwork subset, have 2 human annotators
  independently label the same attributes to validate that the VLM's attribute
  distributions correlate with genuine ambiguity rather than VLM noise.

### 6.4 Temporal uncertainty
$$U_{\text{temporal}} = \frac{1}{T}\sum_{t=1}^{T} d\big(f_I(I), f_I(V_t)\big)$$
- Plot $d(f_I(I), f_I(V_t))$ vs. frame index $t$, averaged over $K$ and over the corpus,
  with confidence bands — this produces the "alignment drifts over time" figure.
- Also compute per-artwork slope (linear fit of $d$ vs. $t$) as a scalar drift rate for
  correlating against $U_{\text{art}}$ and against art-movement stratification (RQ3-adjacent).

---

## 7. Agency policy

$$\pi(U) = \begin{cases}
\text{commit to one video}, & U < \tau_1\\
\text{show multiple interpretations}, & \tau_1 \le U < \tau_2\\
\text{abstain from fidelity claim}, & U \ge \tau_2
\end{cases}$$

- $U$ here is a caption-only, artwork-blind signal (interpretive + semantic
  uncertainty), since at deployment time the system does not have access to the hidden
  artwork — this is the whole point of RQ2.
- **Threshold calibration:** fit $\tau_1, \tau_2$ on the held-out 15% calibration
  subset by choosing operating points that best separate the three $U_{\text{art}}$
  regimes (low-mean/low-var, high-mean/low-var, high-variance) observed with oracle
  access; freeze thresholds before evaluating on the remaining 85%.
- **Theoretical grounding:** map the three branches onto MOSAAIC's Authority axis
  (Issak, Rezwana & Harteveld, ICCC 2025, arXiv:2505.11481) — commit = system holds
  full interpretive authority, diversify = authority is shared with the viewer, abstain
  = authority is ceded back to the human. The abstain branch is distinct from
  classical selective-prediction abstention (El-Yaniv & Wiener lineage; "Know Your
  Limits," TACL 2025) in that the system still generates output — it declines to
  *claim fidelity* to the artwork, rather than declining to answer at all. Watch for
  the over-abstention failure mode documented in that survey when tuning $\tau_2$. See
  `RELATED_WORK.md` §3–4.
- **Sensitivity analysis:** sweep $\tau_1,\tau_2$ and report how policy-decision rates
  (commit / diversify / abstain) and downstream human-judged appropriateness change —
  this shows the policy isn't cherry-picked to one threshold setting.

---

## 8. Comparison methods

| Method | Sees artwork `I`? | Behavior |
|---|---|---|
| Single-seed generation | No | Chooses one interpretation without uncertainty |
| Best-of-K oracle | Yes (selection only) | Selects the $V^{(k)}$ maximizing $s_k$; upper bound given text-only generation |
| Caption-only uncertainty | No | Estimates $U$ from captions/generations alone, no policy action |
| UQ-aware agency policy (ours) | No | Commits, diversifies, or abstains via $\pi(U)$ |
| Image-conditioned video baseline: Wan I2V, or **Every Painting Awakened** (arXiv:2503.23736) | Yes (generation input) | Upper reference: what's achievable when the model itself sees the artwork |

- Best-of-K oracle and the image-conditioned baseline both require `I`, so they are
  **not** deployable policies — they exist purely to bound the achievable
  correspondence ($F_{\text{art}}$) when artwork access is available, at generation time
  or at selection time respectively. The paper's actual contribution (the agency
  policy) is evaluated only against methods that share its text-only constraint.
- **Every Painting Awakened** ("Every Painting Awakened: A Training-free Framework for
  Painting-to-Animation Generation," arXiv:2503.23736) is the closest existing system
  to this task — training-free I2V animation of real paintings with fidelity
  preservation via dual-path video score distillation sampling. It always commits to a
  single output and has no uncertainty/agency layer, which is exactly the gap this
  paper targets. Check code availability before deciding whether to run it directly as
  this baseline row or cite it as the related system a from-scratch I2V baseline is
  modeled after. See `RELATED_WORK.md` §1 for details — verify against the actual
  paper (only the abstract was reachable from this session).

---

## 9. Evaluation protocol

### 9.1 Automatic metrics
- $U_{\text{interpretive}}$, $U_{\text{art}}$, $F_{\text{art}}$, $U_a$ (per attribute),
  $U_{\text{temporal}}$ — reported as corpus-level distributions and stratified by art
  movement/abstractness.
- Correlation analysis (Pearson + Spearman) between caption-only $U$ and oracle-only
  $U_{\text{art}}/F_{\text{art}}$ (RQ2).
- Calibration curve: does higher predicted $U$ actually track lower $F_{\text{art}}$ /
  higher $U_{\text{art}}$ monotonically? Report as a reliability diagram.

### 9.2 Human evaluation
- **Judged appropriateness of policy decisions.** For a sample of ~100 artworks per
  policy regime, show human raters (a) the artwork, (b) the caption, (c) the system's
  chosen action (single video / a set of $k'$ videos / an abstention message), and ask
  whether the action was appropriate given how well the generation(s) actually matched
  the artwork's intent. Compare rater agreement rates across: single-seed baseline vs.
  UQ-aware policy.
- **Trust/preference study.** Pairwise comparison: "system A always shows one video,
  system B sometimes says it isn't confident and shows options instead — which do you
  trust more as a faithful animation of this artwork?" This is the study that most
  directly supports the paper's normative claim in RQ4. Structure the questionnaire
  around the four validated dimensions of felt creative agency from Creativity
  Research Journal (2025), "Agency in Human-AI Collaboration for Image Generation and
  Creative Writing": creative self-efficacy, control over creative action, autonomy in
  the process, and ownership of the resulting artwork — rather than a single ad hoc
  trust score. See `RELATED_WORK.md` §4.
- Recruit ≥3 raters per item, report inter-rater agreement (Krippendorff's α or similar).

### 9.3 Ablations
- Remove each uncertainty component ($U_{\text{interpretive}}$-only,
  $U_{\text{semantic}}$-only, combined) from the policy trigger and measure the drop in
  human-judged appropriateness — isolates which uncertainty signal actually drives good
  agency decisions.
- Vary $K \in \{4, 8, 16\}$ to show how many samples are actually needed to estimate
  $U_{\text{interpretive}}$ stably (diminishing-returns curve), since $K$ directly
  drives compute cost.
- Swap $f_V$/$f_I$ backbones (Section 5) to test metric robustness.

---

## 10. Compute budget

### 10.1 Full-study target (unchanged, for a future non-workshop version)
- Generation: $|\text{corpus}| \times K$ videos = 500 × 8 = 4,000 Wan2.1 generations
  (plus calibration subset). Budget GPU-hours accordingly and pin exact resolution/step
  count, since that's the dominant cost driver.
- VLM attribute elicitation: 4,000 videos × ~6 attributes × $M$ samples (if using
  frequency-based $p_a(c)$) — consider caching / batching, and consider using a
  lower-cost open VLM for the bulk of the corpus with the paid VLM reserved for a
  validation subset.
- Embedding extraction ($f_V$, $f_I$ over all frames): cheap relative to generation,
  but still requires per-frame storage — budget disk accordingly (4,000 videos × ~16–24
  frames).

### 10.2 Pilot compute plan — 7× A100, Wan2.1 **14B**, Aug 3 deadline

**Step zero, before any corpus decision: benchmark real per-video generation time on
the actual hardware and settings.** Published Wan2.1 14B timings vary roughly
8–20 min/video on a single A100 depending on resolution (480p vs 720p), frame count
(5s clip ≈ 81 frames at 16fps), and diffusion step count — a 2.5x spread that alone
swings the feasible corpus size by hundreds of artworks. Generate 10 videos at the
exact settings intended for the full run and measure wall-clock time before
committing to anything below.

**GPU-hour math (provisional, replace with real numbers from the benchmark):**
- Budget ~2.5 days (60 hours) of the ~7-day window to the generation phase itself,
  leaving the rest for VLM elicitation, embedding extraction, calibration, ablations,
  a (necessarily small) human pass, and writing.
- 60 hours × 7 GPUs = 420 GPU-hours available for generation.
- At 8 min/video (optimistic): ~3,150 videos → **~395 artworks at K=8**.
- At 14 min/video (midpoint estimate): ~1,800 videos → **~225 artworks at K=8**.
- At 20 min/video (pessimistic): ~1,260 videos → **~157 artworks at K=8**.

**Working target until the benchmark comes back: ~150–200 artworks, K=8** — biased
toward the pessimistic end since 14B was chosen deliberately for quality and there's
no slack in the week to redo a botched estimate. If the benchmark comes in faster,
grow the corpus; if slower, drop $K$ to 4–6 before shrinking the corpus further (the
DCU/interpretive-uncertainty estimate degrades gracefully with smaller $K$, per the
§9.3 ablation; a too-small or non-stratified corpus breaks RQ3 and the calibration
split outright).

**Overlap generation with everything else that doesn't need it finished first:**
- Corpus curation + captioning (§3) has zero GPU dependency — do this today/tomorrow
  in parallel with the benchmark and the start of generation, not after it.
- Reserve one of the 7 A100s for VLM attribute elicitation (open VLM run locally) and
  embedding extraction, overlapped with the tail of the generation run on the other
  6, rather than sequenced after full generation completes.
- Embedding extraction itself is cheap (order minutes for a few thousand videos on one
  A100) — not a scheduling bottleneck.

**What almost certainly gets cut for Aug 3, and should be stated as such rather than
silently dropped:**
- The full §9.2 human evaluation (≥3 raters × ~100 items × 2 studies) is not
  achievable in this window. Realistic options: run a small informal pilot (2–3
  available raters, ~20–30 items) explicitly labeled as preliminary/pilot in the
  paper, or omit the human study for this submission and present RQ4 as a proposed
  and partially-instrumented but not-yet-run evaluation — consistent with the track's
  stated openness to "critical, speculative" and in-progress work.
- The $K \in \{4,8,16\}$ sweep (§9.3) likely narrows to $K=8$ only, with the sweep
  itself deferred — note this as a limitation rather than running a half-powered
  version of it.
- Backbone-robustness cross-checks (§5, §9.3) can likely still happen since embedding
  extraction is cheap — keep these if the generation phase doesn't overrun its 2.5-day
  budget.

---

## 11. Risks / things that could break the paper's claims

- **Caption ambiguity confound:** if $U_{\text{interpretive}}$ is mostly explained by
  caption vagueness rather than model behavior, the "model uncertainty" framing weakens.
  Mitigated by the multi-caption subset (§3.2) — regress out caption-level variance
  before attributing residual uncertainty to the model.
- **VLM-as-judge circularity:** using a VLM both to generate semantic uncertainty and
  (implicitly) to validate correspondence risks the two numbers being correlated by
  shared VLM biases rather than by genuine model uncertainty — mitigated by using CLIP/
  SigLIP embeddings (not VLM judgments) for $U_{\text{art}}$, and reserving the VLM
  strictly for the structured-attribute entropy computation.
- **Threshold overfitting:** freeze $\tau_1,\tau_2$ on the calibration split only; never
  tune on the evaluation split used for RQ1–RQ4 numbers.
- **Copyright:** confirm licensing of every artwork in the corpus before any public
  release; prefer public-domain/CC sources exclusively for the released benchmark.

---

## 12. Deliverables checklist

- [ ] Curated, license-clean artwork + caption corpus (with stratification metadata)
- [ ] Generation pipeline + all $K$ samples per caption, versioned/pinned Wan2.1 checkpoint
- [ ] Uncertainty computation code for all four metric families
- [ ] Calibrated agency policy ($\tau_1,\tau_2$) + ablations over $K$ and backbones
- [ ] Baseline implementations: single-seed, best-of-K oracle, image-conditioned baseline
- [ ] Human evaluation protocol, rater instructions, agreement statistics
- [ ] Figures: interpretive-uncertainty histogram, $(F_{\text{art}}, U_{\text{art}})$
      scatter, per-attribute $U_a$ ranking, temporal-drift curve, policy decision-rate
      sweep, human preference results
