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
   metrics."** $U_a$ is a direct cross-modal descendant of semantic entropy
   (Farquhar et al., *Nature* 2024) — closed-set VLM attribute elicitation instead of
   open-set LLM completion clustering. $U_{\text{interpretive}}$ is best described as
   *aleatoric* uncertainty in Franchi et al.'s (UAI 2025) aleatoric/epistemic
   decomposition — we're deliberately not estimating epistemic uncertainty (which
   would need multiple independently trained Wan checkpoints, and we don't have or
   need those). State this decomposition choice explicitly; it preempts an obvious
   reviewer question.
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

## Timeline reality check — read this first

Per the search results, the NeurIPS 2026 Creative AI Track deadline is **August 3,
2026, AoE**. Today is **July 27, 2026**. That is **7 days out** — this needs to be
verified immediately against the primary source
(`neurips.cc/Conferences/2026/CallForCreativeAI`, unreachable from this session) since
it changes everything about what's achievable:

- The full experimental plan in `EXPERIMENTAL_SETUP.md` (300–500 artworks, K=8 Wan2.1
  generations each ≈ 4,000 videos, VLM attribute elicitation over all of them, a
  calibrated policy, and a multi-rater human study) is **not** a one-week undertaking
  even with unlimited compute — the human-eval design and rater recruitment alone
  typically takes longer than that.
- If August 3 is the real deadline and this is meant for that submission, the
  realistic options are (a) submit a much smaller **pilot/position paper** — e.g.
  20–30 artworks, K=4, no human study, framed as "preliminary findings + proposed
  agency policy," leaning on the track's explicit openness to "critical, speculative"
  work rather than a full empirical study, or (b) target the **NeurIPS 2027** Creative
  AI call instead and use the next ~12 months to run the full study properly.
- This is a scope/timeline decision only you can make — flagging it rather than
  silently picking one.
