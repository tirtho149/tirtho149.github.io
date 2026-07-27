# Refined Idea (post-literature-review)

*Written after a literature pass — see `RELATED_WORK.md` for the full annotated
bibliography this draws on. Every claim below traces to a specific citation there.*

## Fit to the actual call

The NeurIPS 2026 Creative AI Track's theme is **Agency**, and its own example
questions are "how does AI change where creative agency begins, where it ends, and
how it is recognized?" and "can an artwork reveal agencies that are hidden inside
technical systems?" Our $\pi(U)$ policy is a direct, measurable instantiation of the
first question, and the whole caption-mediated pipeline (the artwork is hidden from
Wan2.1 but visible to the evaluator) is a literal instantiation of the second — the
"hidden agency" is the uncertainty structure inside Wan2.1 that only becomes visible
once you compare its blind guesses against the artwork it never saw. **Lead the
abstract/intro with this**, don't bury it.

## Sharpened title

**Knowing When Not to Interpret: Uncertainty as a Boundary of Creative Agency in
Text-to-Video Translation of Human Artwork**

(Keeps the original "Knowing When Not to Interpret" hook, folds in "boundary of
agency" from the earlier framing, and swaps "caption-to-video" for the clearer
"text-to-video translation" — matches how the venue and the T2V literature phrase it.)

## One-paragraph pitch (for the abstract)

When a text-to-video model receives only a caption of a human artwork — never the
artwork itself — how much authority should it exercise over the interpretation it
produces? We study this question with Wan2.1 on a corpus of captioned modern
artworks, generating $K$ seeds per caption and measuring four distinct kinds of
uncertainty: *interpretive* (disagreement across the model's own samples),
*artwork-correspondence* (instability relative to the hidden original, visible only
to the evaluator), *semantic* (VLM-elicited entropy over structured artistic
attributes), and *temporal* (drift from the artwork over the course of a generated
clip). We show that caption-only, artwork-blind uncertainty predicts
artwork-correspondence instability that the model itself never gets to see
(RQ2), and we use this predictive signal to drive a three-way agency policy —
commit, diversify, or abstain from a fidelity claim — that a single-seed generator
cannot express. Grounding this in the co-creativity literature's Autonomy/Authority/
Initiative framework (MOSAAIC), we argue and empirically test, via a human study
structured around validated dimensions of felt creative agency (self-efficacy,
control, autonomy, ownership), that regulating *when* a system commits to an
interpretation is itself a creative-agency mechanism, not merely a reliability
feature bolted onto one.

## What changed from the first draft, and why

1. **Abstention is reframed as "abstention-from-a-claim," not "abstention-from-an-
   answer."** The selective-prediction/abstention literature (El-Yaniv & Wiener
   lineage, the TACL "Know Your Limits" survey, "Know When to Abstain" 2025) is all
   about declining to answer a query. Our third policy branch still generates a
   video — it just declines to assert that the video is a faithful reading of a
   specific human artwork. That's a distinct, arguably more interesting, notion of
   abstention for generative/creative systems, and it's a contribution back to that
   literature, not just a borrowed technique. State this explicitly early in the
   paper.
2. **"Agency" gets an actual theoretical anchor.** MOSAAIC's Autonomy/Authority/
   Initiative decomposition (ICCC 2025, from a 172-paper systematic review) gives a
   citable vocabulary: map commit → system holds full authority, diversify → shared
   authority, abstain → authority ceded to the human. Without this the "agency" claim
   risks reading as a rhetorical flourish over an uncertainty-thresholding system;
   with it, the paper is legibly contributing to an existing HCI framework.
3. **The human study has a validated instrument to borrow instead of inventing one.**
   The Creativity Research Journal (2025) think-aloud paper on agency in human-AI
   image/writing collaboration names four dimensions — self-efficacy, control,
   autonomy, ownership. Structure the RQ4 trust/preference study (§9.2 of
   `EXPERIMENTAL_SETUP.md`) around these four constructs instead of a generic "which
   do you trust more" question. This is both more rigorous and more clearly
   Creative-AI-track-appropriate than an ML-style preference score.
4. **A real, closely-related competing system exists and must be addressed head-on:**
   "Every Painting Awakened" (arXiv:2503.23736) already does training-free
   painting→video with fidelity preservation — but it's I2V (sees the artwork) and
   always commits to one output. That's precisely the counterfactual our paper needs:
   it shows what "maximum achievable single-shot fidelity" looks like when the model
   *can* see the artwork, which is a stronger, citable version of our "Best-of-K
   oracle" / "image-conditioned baseline" rows than a homebrew baseline would be.
   Recommend either (a) citing it as related work and building our own
   image-conditioned baseline in the same spirit, or (b) if code is available,
   running it directly as the image-conditioned baseline — check the project page's
   code release status before deciding.
5. **The uncertainty metric itself has closer precedent than "we invented four
   metrics" — and it's now been confirmed, not just reconstructed from search
   snippets.** The user pulled the actual DCU abstract directly from arXiv
   (arXiv:2602.13264, AISTATS 2026 workshop): DCU's own reported experiments are on
   **language model** outputs; "generalizes well to more complex tasks in multi-modal
   domains" and "integration into UQ for multi-modal and agentic frameworks" are
   explicitly framed as the paper's discussion of *wider potential*, not something
   they built. That's a clean opening: instantiating DCU-style von Mises–Fisher
   concentration for **video** embeddings, and extending it to an
   **externally-anchored** setting (artwork correspondence, which single-distribution
   DCU has no mechanism for), is genuinely unclaimed ground — say so explicitly, and
   quote DCU's own "agentic frameworks" line when motivating $\pi(U)$, since that's
   precisely the follow-up direction its authors point at without taking. Separately,
   $U_a$ (the VLM-attribute-entropy metric) remains a direct cross-modal descendant of
   semantic entropy (Farquhar et al., *Nature* 2024) — closed-set VLM attribute
   elicitation instead of open-set LLM completion clustering — and
   $U_{\text{interpretive}}$/DCU together are best described as *aleatoric*
   uncertainty in Franchi et al.'s (UAI 2025) aleatoric/epistemic decomposition;
   we're deliberately not estimating epistemic uncertainty (which would need multiple
   independently trained Wan checkpoints). State this decomposition choice explicitly
   — it preempts an obvious reviewer question.
6. **A genuinely new empirical question falls out of the DPP-diversity paper**
   (arXiv:2511.20647): does the "diversify" branch actually need genuinely
   diversity-optimized sampling (DPP-guided) instead of plain multi-seed sampling to
   be useful to a human viewer? This can be a secondary contribution/ablation rather
   than just related work — worth adding as an explicit ablation in
   `EXPERIMENTAL_SETUP.md` §9.3.
7. **World Models That Know When They Don't Know** (arXiv:2512.05927) is the one
   paper that could pre-empt the "uncertainty-calibrated video generation" framing —
   need the full text to confirm its application domain (reads as
   robotics/planning/world-model, not creative/artistic, from the abstract snippet
   alone). **This is the single highest-priority thing to verify before writing the
   related-work section** — if it turns out to already do a creative/artistic version
   of this, the novelty claim needs to shift toward the agency-policy and
   abstention-from-a-claim framing rather than the calibrated-uncertainty framing.

## Updated research questions (unchanged in substance, sharpened in language)

- **RQ1** — unchanged.
- **RQ2** — unchanged; this is the calibration claim, methodologically parallel to
  "World Models That Know When They Don't Know," so use a reliability-diagram-style
  analysis to make the comparison legible to reviewers who know that paper.
- **RQ3** — unchanged.
- **RQ4**, reframed: *Does an uncertainty-aware agency policy change not just
  output-selection quality but humans' felt creative agency/ownership over the
  resulting artwork, relative to a single-seed system that always commits?* — now
  answerable with a validated instrument rather than an ad hoc question (see point 3
  above).

## Immediate action items before drafting

0. **Get full text of DCU (Chattopadhyay et al., arXiv:2602.13264 — confirmed AISTATS
   2026 "Calibration for Modern AI" workshop paper, not ICML) and switch
   $U_{\text{interpretive}}$ to it.** This was the most consequential finding of the
   second research pass: our original pairwise-cosine formula for
   $U_{\text{interpretive}}$ is a weaker, ad hoc version of a real, more principled
   method (von Mises–Fisher concentration parameter $\kappa$) that already exists and
   already reports matching/exceeding semantic-entropy calibration. Being a workshop
   paper rather than a fully-reviewed main-track result is good news for us: it means
   applying and properly validating DCU in a new modality (video) and extending it to
   an externally-anchored setting (artwork correspondence) is legitimately open,
   publishable ground rather than a scooped result. `EXPERIMENTAL_SETUP.md`
   §6.1 has been updated to make DCU the primary estimator and the old formula an
   ablation baseline. Confirmed via the verbatim abstract (pulled directly from
   arXiv by the user): DCU's own experiments are language-model-only; multi-modal and
   agentic integration are named as future potential, not demonstrated — so the
   video-domain instantiation is not narrowed novelty after all. Remaining before
   drafting: confirm the exact estimator details and whether they release code (still
   only recoverable as method-level summary, not full derivation, from this session).
1. **Get full text of "Every Painting Awakened" and "World Models That Know When They
   Don't Know."** Both are load-bearing for the novelty argument and were only
   available as abstracts in this pass (arXiv was unreachable from this session's
   network — fetch these from a machine with normal internet access, or ask a
   collaborator).
2. Decide whether "Every Painting Awakened" becomes a literally-run baseline (needs
   code availability check) or a cited comparison point.
3. Pull the exact NeurIPS 2026 Creative AI submission format/page-limit requirements
   directly from `neurips.cc/Conferences/2026/CallForCreativeAI` (also unreachable
   here) before drafting — the track has historically accepted non-standard formats
   (videos, "critical, speculative, poetic, performative" work per this year's call),
   which may mean the expected paper shape is not a standard 8-page NeurIPS main-track
   submission.
4. **Read the timeline warning at the bottom of this document before doing anything
   else.**

---

## Timeline reality check

Per the search results, the NeurIPS 2026 Creative AI Track deadline is **August 3,
2026, AoE** — still unverified against the primary source
(`neurips.cc/Conferences/2026/CallForCreativeAI`, unreachable from this session).
**Decision made:** attempting the Aug 3 submission, using 7× A100 GPUs running Wan2.1
**14B** (quality prioritized over corpus breadth). Full plan, GPU-hour math, and what
gets cut for this timeline are in `EXPERIMENTAL_SETUP.md` §10.2 — summary:

- **Corpus:** ~150–200 artworks (pending the required first-step generation-time
  benchmark; could range from ~155 to ~395 depending on real per-video timing), K=8,
  vs. the 300–500 full-study target.
- **Human evaluation (RQ4):** the full multi-rater study is not achievable in this
  window. Either a small labeled-preliminary pilot (~20–30 items, 2–3 raters) or
  omit it for this submission and present RQ4 as instrumented-but-not-yet-run,
  leaning on the track's explicit openness to speculative/in-progress work.
- **Ablations:** the $K\in\{4,8,16\}$ sweep likely narrows to $K=8$ only; backbone
  cross-checks (cheap, embedding-only) likely still fit.
- **Sequencing:** corpus curation/captioning has no GPU dependency — start it today,
  in parallel with the mandatory generation-time benchmark, not after it.
- **300–500 artworks + full human study remain the target for a subsequent full
  paper** (NeurIPS 2027 or a journal/main-track venue) — the Aug 3 submission is the
  pilot/position version of this work, not the final word on it.
