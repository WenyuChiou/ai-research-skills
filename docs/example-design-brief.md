---
project: "LLM agents for human behaviour in socio-hydrology"
last_updated: "2026-05-23"
stage: design
status: draft
source: "topic_dossier.gaps.yml#G2"
gap_verdict: "conditional-go — Open (medium confidence), partially-attempted on dead-end history"
placeholder_segments: [2, 3, 4]
---

# Design brief

> **What this example shows.** A `research-design-helper` (Stage 3a)
> output for a research idea that has already been vetted by a Stage 2
> `gap-to-topic` run (the chosen `conditional-go` candidate `G2` from
> the companion [`example-topic-dossier.gaps.yml`](example-topic-dossier.gaps.yml)).
> Three schema features visible here that a researcher consuming
> this brief should recognise:
>
> 1. **Provenance frontmatter** — `source` points back to the
>    upstream `.gaps.yml` and `gap_verdict` is a frozen snapshot of
>    the verdict + reason. Downstream tools (e.g. `research-context-compressor`
>    Stage 3b) copy `source` into the project manifest's
>    `provenance.from_gap` field so the manifest can trace back to
>    the dossier candidate without re-reading the dossier.
> 2. **§0 auto-pre-fill (v0.3.12+)** — Segments 1 (sharpened RQ) and
>    5 (risk register) were pre-filled by the skill's §0 step from
>    the chosen `gaps[].statement` and `open_questions[]`. The
>    Socratic dialog still ran for those segments, but the starting
>    points came from the dossier — saving the researcher from
>    re-articulating context the dossier already captured.
> 3. **`placeholder_segments` (v0.3.15+)** — Segments 2-4 in this
>    example were filled by AI-generated stub content (not real
>    Socratic answers from a human) to exercise the Stage 3b handoff
>    in testing. The frontmatter `placeholder_segments: [2, 3, 4]`
>    flags this so downstream tools refuse to gate real research on
>    a brief whose segments are non-empty but synthetic. When all
>    five segments come from genuine Socratic dialog, leave the list
>    empty (`[]`).

## 1. Research question

**Sharpened RQ** (one sentence, falsifiable):
*LLM agents conditioned on household demographics, prior water-use
observations, and local flood history can predict held-out household
flood-adaptation adoption decisions (binary: did the household adopt
a flood-protection measure within a 2-year window) at AUC > a
discrete-choice baseline trained on the same features, by ≥ 0.05
(p < 0.05, paired DeLong test).*

**Falsification condition** (what would you observe if FALSE):
The LLM-agent AUC fails to exceed the discrete-choice baseline by
≥ 0.05 on the held-out set, OR the difference is not significant
at p < 0.05. Either outcome falsifies "LLM agents add representational
value over conventional ABM in this domain."

**Smallest answerable version** (1-week prototype scope):
One region (single FEMA flood zone or equivalent administrative unit),
~100 households from a publicly-available adaptation survey,
GPT-class API with pinned model version, single LLM-agent prompt
template vs a logit baseline, 70/30 stratified train/test split.
Output: one AUC comparison + one paired DeLong test result.

## 2. Expected mechanism

_TEST-FIT-PLACEHOLDER (segments 2-4) — not from operator dialog._

**Causal chain**:
Household demographics + local flood history + social context →
LLM agent reads as natural-language prompt → LLM samples a posterior
over discrete actions consistent with the *"decision-making like a
stakeholder with this profile"* frame → action selected →
aggregated to household-level adoption rates across the population →
fed into the socio-hydrology coupling layer (e.g. CAT-style
hydrodynamic + ABM coupling) → projected basin-scale adoption /
adaptation outcomes.

**Most uncertain step**:
Whether the LLM "samples a posterior over actions" step actually
approximates how real households make adaptation decisions, or
whether it mimics the model's pre-training distribution of
plausible-sounding decisions. This is the exact construct-validity
risk Schück 2026 raises.

**First step you'd bet breaks**:
The LLM-agent → individual decision step. The LLM may produce
decisions that look reasonable to a human reader but don't match
the heterogeneity / boundedly-rational quirks of real household
decisions — passing a face-validity check while failing
predictive validation.

## 3. Identifiability check

_TEST-FIT-PLACEHOLDER — not from operator dialog._

**Discriminating condition** (what experiment / data / counterfactual
distinguishes RQ-true from RQ-false):
Held-out predictive test on real adaptation decisions: train both
LLM agents and the logit baseline on 70% of households; predict the
held-out 30%'s adoption decision; compare AUC on the held-out set.
RQ-true if LLM-agent AUC > baseline AUC + 0.05 with p < 0.05.

**Confounders to rule out**:
- The held-out 30% is not a representative subset → use stratified
  matched split on demographics + flood-zone.
- The LLM "sees" the answer indirectly through pre-training (dataset
  appears in the model's training corpus) → check dataset publication
  date vs LLM training cutoff; prefer datasets post-cutoff or local
  unpublished surveys.
- Demographic-only signal already captures most variance → run a
  demographics-only logit (no flood history, no social context) as
  a third baseline; LLM must beat THIS baseline too, not just the
  feature-rich one.
- LLM stochasticity dominates the small effect → fix temperature, run
  N=10 repeats per held-out household, average the predicted
  probability before scoring.

**Missing-data plan** (if current data can't discriminate, what's
the minimum extra data needed):
If no public dataset has (demographics, flood history, social context,
adoption decision) tuples at household level, primary collection via
targeted survey is required — minimum N ≈ 500 households for adequate
power, ethics approval ~3–4 months. Jiang 2026 (North China Plain)
has aggregate model data, not individual-level — verify before
relying. Backup candidate datasets to scope: FEMA HMA grant
applications, post-Harvey household surveys, post-Sandy resilience
panels.

## 4. Validation plan

_TEST-FIT-PLACEHOLDER — not from operator dialog._

**Success metric**:
Held-out predictive accuracy on the binary household-adoption decision:
**AUC + balanced accuracy**. Pre-registered threshold: *LLM-agent AUC
> baseline AUC + 0.05 AND p < 0.05 on a paired DeLong test on the
same held-out folds.*

**Baseline being beaten**:
1. **Discrete-choice logit** with the same features (demographics +
   flood history + spatial context) — the conventional socio-hydrology
   ABM baseline.
2. **Rule-based ABM** with hand-coded if-then rules drawn from prior
   socio-hydrology literature (e.g. Yang et al. flood-adaptation
   rules) — the "what we'd do without LLMs" baseline.
3. **Demographics-only logit** — to rule out the case where
   demographics alone capture most variance.

**Negative control** (a setup where you EXPECT the metric to NOT
improve, confirming the method isn't just noise):
*Profile-shuffled LLM agents*: same households, but randomly shuffle
the (demographics, history, social-context) tuples across households
before prompting the LLM. If shuffled-LLM AUC ≈ profile-LLM AUC, the
apparent improvement is from LLM general priors, NOT from real
household differentiation — falsifies the design. Pre-register
expectation: *shuffled-LLM AUC should approach demographics-only
baseline, NOT profile-LLM AUC.*

## 5. Risk register

| # | Risk | Early-warning signal | Mitigation |
|---|---|---|---|
| 1 | **Construct-validity risk** (pre-filled from `gaps[G2].feasibility` hint + Q3): LLM-generated behaviour looks plausible but doesn't faithfully represent real human water decisions — the exact risk Schück 2026 raises against this approach | Held-out validation: LLM agents cannot beat a discrete-choice or rule-based ABM baseline on real household-adaptation decisions | Bake the construct-validity test into the design from day 1 — predict held-out behaviour vs baseline before claiming the agents add value (this is §3 + §4 above) |
| 2 | **Recall risk** (pre-filled from Q1): The dossier's gap-still-open verdict is medium-confidence; Semantic Scholar was rate-limited during search | Full-recall re-run with `SEMANTIC_SCHOLAR_API_KEY` enabled surfaces an existing calibrated-LLM-agent-for-socio-hydrology paper | Re-run the gap-to-topic search before committing thesis-scale effort; if a paper exists, narrow the topic or pivot |
| 3 | **Novelty / out-distancing risk** (pre-filled from Q2 + borderline_reason B1): Batista 2025 is a close in-domain analogue (LLM sentiment for water governance). The design must show this work is more than a sentiment-style application | The pilot's validation result doesn't meaningfully out-distance Batista 2025's signal-quality benchmark | Frame the contribution as the *validated agent-based decision representation* (§4 validation result), not "LLM agents in water"; explicitly contrast in validation §4 |
| 4 | **Data-binding risk** (pre-filled from Q4 + feasibility): Behavioural-validation dataset is the binding feasibility constraint. No reusable observed-behaviour dataset = primary collection (ethics approval + ~6 months) dominates timeline | First-pass lit search for reusable household behaviour data turns up nothing reusable (e.g. Jiang 2026 NCP model lacks individual-level data) | Identify a reusable dataset BEFORE committing to thesis scope, OR plan a primary-collection schedule with ethics-approval timeline |
| 5 | **Reproducibility risk**: LLM outputs depend on an external API model that can change or be retired mid-project | An API model version-bump moves the agent behaviour outside its calibration band | Pin LLM model versions in the design; archive prompts + outputs; budget for a re-calibration pass if the API model is deprecated |

## Notes

- This brief is published as a catalog example to show the
  `research-design-helper` Stage 3a output shape. Segments 2–4 here
  are AI-generated stubs flagged by `placeholder_segments: [2, 3, 4]`
  in the frontmatter; in a real session a researcher would replace
  them through the skill's Socratic dialog before the brief is used
  to gate any research decision.
- Segment 1 (RQ) and Segment 5 (risks) are production-shaped output:
  segment 1 was pre-filled from the upstream `gaps[].statement` and
  then sharpened (the falsification condition and 1-week prototype
  scope come from dialog, not from the dossier); segment 5 was
  pre-filled from `open_questions[]` + the `feasibility:
  feasible-with-effort` hint and lightly extended with the
  reproducibility risk.
- Provenance back-pointer (`source: topic_dossier.gaps.yml#G2`) is
  set. If a future Stage 3a session reads this brief and detects a
  different chosen gap id, the skill's provenance-protection
  rule (v0.3.12+) asks the user before overwriting — preventing
  silent rewrite of design context across topic decisions.
