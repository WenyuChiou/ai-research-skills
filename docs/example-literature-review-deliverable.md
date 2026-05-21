# Example — Literature Review Deliverable

> **SYNTHETIC EXAMPLE.** Every paper, author, identifier, and number below
> is **fabricated** to illustrate the *shape* of a research-hub
> literature-review deliverable. Nothing here refers to a real publication.
> In a real run, all citations are real and resolvable. — No real maintainer
> artifacts (per the catalog's [`## Limitations`](../README.md) policy).
>
> Languages: [English](example-literature-review-deliverable.md) | [繁中](example-literature-review-deliverable.zh-TW.md)

This is the consolidated end-to-end output of the research-hub literature
pipeline (`search` → `literature-triage-matrix` → `research-design-helper`)
— the single document those skills add up to.

> **Template note:** this file is BOTH a worked example AND the reusable
> section contract. Each `>` italic note states what the section must
> contain. To reuse: keep the section structure and the italic contracts,
> replace the synthetic content with your own corpus.

| Field | Value |
|---|---|
| Topic | Do LLMs reproduce human-style cognitive biases on classic cognitive-science paradigms? |
| Scope | Anchoring / framing / persona effects; model scale, prompt detail, and applied-domain risk |
| Corpus | 6 papers — abstracts only, not full-text (synthetic) |
| Compiled | 2026-01-15 (synthetic date) |
| Pipeline | research-hub: `search` → `literature-triage-matrix` → `research-design-helper` |
| Evidence grade | Screening-grade triage — **NOT a systematic review** |

---

## 1. TL;DR

> *3–6 bullets: the headline findings, the main disagreement, the sharpest
> gap. A reader who stops here should still know what to do next.*

- **Cognitive biases appear broadly in current LLMs.** A 40-model benchmark
  (Banerjee et al. 2025) reports bias-consistent responses in 22–61% of
  items across 12 bias categories; anchoring specifically is confirmed
  independently (Reyes & Okafor 2024).
- **Mitigation is the central disagreement.** Reyes & Okafor (2024) find
  simple prompt-based fixes cut anchoring by only ~10%; Achebe et al. (2024)
  report a structured self-audit prompt removes most of the effect. The two
  use different tasks and metrics, so they cannot yet be ranked.
- **Biases reach applied settings** — Voss & Hartman (2025) show cognitive
  biases can be exploited as a black-box manipulation surface in LLM
  recommenders.
- **Sharpest gap [G1]:** no study reports a standardized *free-response*
  effect size for anchoring — the corpus speaks only in rates and percentages.
- **Corpus caveat:** 6 papers, abstracts only — a first-pass triage that
  scopes a study, not settled evidence.

---

## 2. Literature inventory

> *One row per source. Minimum columns: ID, citation, year, evidence type
> (empirical / conceptual), relevance grade with a one-line reason.*

| ID | Citation | Year | Type | Relevance |
|---|---|---|---|---|
| S1 | Reyes & Okafor — *Anchoring Effects in Instruction-Tuned Language Models* | 2024 | Empirical | **High** — direct anchoring evidence + negative result on simple mitigation |
| S2 | Lindqvist et al. — *Cognitive Bias Risk in LLM Decision Support: A Position Paper* | 2024 | Conceptual / position | **Medium** — risk framing; not an empirical anchor |
| S3 | Banerjee et al. — *BiasGrid: A 40-Model Benchmark of Cognitive Bias Prevalence* | 2025 | Empirical + benchmark | **High** — broadest controlled evaluation in the corpus |
| S4 | Sato & Pellegrini — *Persona Conditioning and Bias Susceptibility in LLMs* | 2025 | Empirical | **Medium** — adds a persona-moderator angle |
| S5 | Achebe et al. — *Self-Audit Prompting Reduces Anchoring in Generative Models* | 2024 | Empirical + framework | **High** — proposes a mitigation that works where simple prompts fail |
| S6 | Voss & Hartman — *Cognitive Bias as an Adversarial Surface in LLM Recommenders* | 2025 | Empirical (applied) | **Medium-High** — biases as a manipulation vector in a deployed setting |

---

## 3. Per-paper summary

> *For each source: research question · method · sample · key findings
> (quantified ONLY where the source quantifies) · author-acknowledged
> limitation · how to use it. Never invent numbers the abstract does not
> give — write "not specified in abstract" instead.*

### S1 — Reyes & Okafor 2024 — Anchoring Effects in Instruction-Tuned Language Models
- **Question / method:** Does anchoring appear in instruction-tuned LLMs, and
  do prompt-based fixes remove it? Numeric-estimation tasks with seeded
  anchors; four prompt-based mitigation strategies compared.
- **Sample:** 8 instruction-tuned models; 1,800 estimation prompts.
- **Findings:** Anchoring is robust; the four prompt-based mitigations reduce
  the effect by only ~10% on average.
- **Limitation:** Numeric-estimation tasks only; no free-response generation.
- **Use as:** §"anchoring-specific evidence"; cite for "simple debiasing fails".

### S2 — Lindqvist et al. 2024 — Cognitive Bias Risk in LLM Decision Support: A Position Paper
- **Question / method:** What cognitive-bias risks face LLM decision-support
  deployments? Conceptual synthesis; no measurement.
- **Sample:** None.
- **Findings:** Identifies five bias families as deployment risks; proposes a
  mitigation research agenda.
- **Limitation:** No empirical evaluation — agenda-setting, not evidence.
- **Use as:** Introduction §"why this matters"; motivation only.

### S3 — Banerjee et al. 2025 — BiasGrid: A 40-Model Benchmark of Cognitive Bias Prevalence
- **Question / method:** How prevalent are cognitive biases across many LLMs,
  and how does model size affect them? Multiple-choice benchmark; 12 bias
  categories; controlled prompt variation.
- **Sample:** 40 models × 600 items = 24,000 evaluations.
- **Findings:** Bias-consistent responses in 22–61% of items across the 12
  categories; models >70B reduce bias in roughly one-third of cases;
  detailed prompts help most biases but worsen confirmation framing.
- **Limitation:** Multiple-choice format; free-response behaviour untested.
- **Use as:** Methods §"evaluation framework"; Results §"prevalence numbers".

### S4 — Sato & Pellegrini 2025 — Persona Conditioning and Bias Susceptibility in LLMs
- **Question / method:** Do assigned personas change bias susceptibility?
  Persona-conditioned evaluation across model architectures.
- **Sample:** Not specified in abstract.
- **Findings:** Analytical personas lower bias susceptibility; "expert"
  personas raise overconfidence bias.
- **Limitation:** The operationalization of "persona" is opaque.
- **Use as:** Discussion §"moderators of bias"; counterpoint on variability.

### S5 — Achebe et al. 2024 — Self-Audit Prompting Reduces Anchoring in Generative Models
- **Question / method:** Can a structured self-audit prompt mitigate
  anchoring? Proposes a two-pass "self-audit" prompt; compares to baselines.
- **Sample:** Not specified in abstract.
- **Findings:** Self-audit prompting removes most of the anchoring effect on
  the tested task family — where simple Chain-of-Thought did not.
- **Limitation:** Tested on a single task family.
- **Use as:** Methods §"mitigation frameworks"; direct counterpoint to S1.

### S6 — Voss & Hartman 2025 — Cognitive Bias as an Adversarial Surface in LLM Recommenders
- **Question / method:** Can cognitive biases be exploited to manipulate LLM
  recommenders? Black-box manipulation of item descriptions using bias
  principles.
- **Sample:** One recommender setup; multiple model scales.
- **Findings:** "Social proof" framing reliably boosts an item's
  recommendation rank; the manipulation is hard to detect.
- **Limitation:** One recommender setup; no mitigation evaluated.
- **Use as:** §"applied risk / biases as an attack surface".

---

## 4. Cross-paper synthesis

> *What the corpus agrees on, where it disagrees (name the papers), and how
> to reconcile. Flag low-evidence sources explicitly. Do not smooth over a
> disagreement — surface it.*

- **Convergence — biases are broadly present.** S1 and S3 independently
  confirm that cognitive biases (anchoring in particular) appear across many
  models. The *existence* of the phenomenon is the corpus's most defensible
  claim.
- **Central disagreement — does mitigation work?** S1 reports simple
  prompt-based fixes cut anchoring by only ~10%; S5 reports a structured
  self-audit prompt removes most of it. They use different tasks and metrics,
  so the disagreement cannot be resolved from abstracts — it is itself a gap
  ([G5]).
- **Applied risk** is an emerging theme — S6 reframes cognitive bias as an
  exploitable manipulation surface, not only a fairness concern.
- **Moderators** — S4 adds that an assigned persona shifts susceptibility,
  which complicates any single "prevalence" number.
- **Low-evidence flag:** S2 is a position paper with no measurement — use it
  for motivation, never as an evidence anchor.

---

## 5. Research gaps

> *Each gap = (a) a one-sentence statement, (b) the evidence that it IS a gap
> — which papers fail to cover it, (c) what would close it. Gaps tagged
> `[G-n]`. A gap that maps to a planned study carries the claim ID from
> `.paper/claims.yml`.*

| Gap | Statement | Why it is a gap (evidence) | What would close it |
|---|---|---|---|
| **[G1]** | No standardized free-response effect size for LLM anchoring. *(→ claims.yml C6, status: gap)* | S1 uses numeric-estimation tasks; S3 uses multiple-choice; neither reports a free-response effect size. | A free-response anchoring pilot reporting a standardized effect size. |
| **[G2]** | The anchor effect's dependence on anchor plausibility is untested. *(→ claims.yml C5, status: gap)* | No corpus paper grades anchor plausibility; all use fixed anchors. | A graded-anchor pilot testing a monotonic dose-response. |
| **[G3]** | Cross-paper results are not comparable — each study uses its own benchmark. | S1, S3, and S5 each use a different task set and metric; no shared benchmark exists. | A shared public benchmark with a common severity metric. |
| **[G4]** | Multiple-choice → free-response generalization is unverified. | S3's prevalence numbers are all multiple-choice; open-ended behaviour is untested. | A free-response replication of a benchmark subset. |
| **[G5]** | Bias-mitigation efficacy has no head-to-head evaluation. | S1 (simple prompts fail) and S5 (self-audit works) are not comparable across their differing setups. | A controlled bake-off of mitigation methods on one benchmark. |
| **[G6]** | Persona / moderator effects rest on an opaque operationalization. | Only S4 conditions on persona, and its definition of "persona" is not specified. | A full-text read of S4 plus an independent persona-conditioning replication. |

---

## 6. Open questions

> *Unresolved questions the corpus cannot answer that affect how the gaps
> should be prioritized. Distinct from gaps: a gap is closable by a defined
> study; an open question may need a judgment call or more reading.*

- **Q1:** Do S1's estimation tasks and S3's 600 benchmark items share any
  scenarios? If not, their apparent agreement on prevalence is two
  non-overlapping samples agreeing by construction.
- **Q2:** Should a pilot be powered for S3's full range (22–61%) or its high
  end? The choice changes the required sample size; a power analysis is
  outstanding.

---

## 7. Recommended next step

> *The single highest-leverage study the gap analysis points to, stated
> concretely enough to start. One paragraph + a scope line.*

The gap analysis points most directly at **[G1] + [G5]**: run a free-response
anchoring pilot that also serves as a mitigation bake-off. On a single pinned
model snapshot, compare a control prompt, the simple Chain-of-Thought fix
(S1's class), and the self-audit prompt (S5's method) on the same
free-response task — for example, 200 prompts × 3 anchor levels per
condition. Report a standardized effect size between anchor conditions for
each mitigation, so the S1↔S5 disagreement is resolved on a common metric.
Include an anchor-absent control to rule out training-data priors. Full
design, confounders, and risk register: `.research/design_brief.md`.

*Scope line:* 1-week prototype; one model snapshot; one task family; persona
moderators ([G6]) and the shared-benchmark effort ([G3]) are out of scope for
the prototype.

---

## 8. References

> *Full, resolvable references — arXiv ID / DOI + URL at minimum, ordered by
> ID. In a real deliverable these identifiers are real and resolve; the
> placeholder IDs below mark this as a synthetic example.*

- **[S1]** Reyes, A., & Okafor, N. (2024). *Anchoring Effects in
  Instruction-Tuned Language Models.* arXiv:XXXX.XXXXX (synthetic).
- **[S2]** Lindqvist, M., Park, J., & Mensah, K. (2024). *Cognitive Bias
  Risk in LLM Decision Support: A Position Paper.* arXiv:XXXX.XXXXX (synthetic).
- **[S3]** Banerjee, R., Cho, S., & Whitfield, T. (2025). *BiasGrid: A
  40-Model Benchmark of Cognitive Bias Prevalence.* arXiv:XXXX.XXXXX (synthetic).
- **[S4]** Sato, Y., & Pellegrini, L. (2025). *Persona Conditioning and Bias
  Susceptibility in LLMs.* arXiv:XXXX.XXXXX (synthetic).
- **[S5]** Achebe, C., Romano, D., & Idris, F. (2024). *Self-Audit Prompting
  Reduces Anchoring in Generative Models.* arXiv:XXXX.XXXXX (synthetic).
- **[S6]** Voss, E., & Hartman, G. (2025). *Cognitive Bias as an Adversarial
  Surface in LLM Recommenders.* arXiv:XXXX.XXXXX (synthetic).

---

## 9. Provenance & limitations

> *How this deliverable was produced + honest caveats. A literature-review
> deliverable without this section is not trustworthy — every reader needs
> to know the evidence grade before acting on it.*

- **This is a synthetic example.** All six papers, their authors, their
  identifiers, and every number are fabricated to illustrate the *structure*
  of a research-hub literature-review deliverable. None refer to a real
  publication. A real run produces this same shape with real, resolvable
  sources.
- **Produced by:** the research-hub literature pipeline — `search` (corpus
  discovery) → `literature-triage-matrix` (§2–§4) → `research-design-helper`
  (§5–§7). Raw search output is archived alongside a real deliverable.
  `paper-memory-builder` is not a literature-review step — it runs on a
  user's own manuscript draft; the `.paper/claims.yml` claim IDs in §5 come
  from such a draft, not from the corpus.
- **Companion files (machine-readable):** every deliverable ships with
  `<name>.bib` — a BibTeX export of §8 References — and `<name>.gaps.yml`
  — a structured export of §5 research gaps + §6 open questions (each gap
  carries `statement / evidence / closes_via / linked_claim / status`).
  For this example: `example-literature-review-deliverable.bib` and
  `example-literature-review-deliverable.gaps.yml`.
- **Corpus limitation:** in a real run the corpus is read **abstract-only**
  unless full-text is fetched; quantified findings are transcribed from
  abstracts, and "not specified in abstract" is used wherever the abstract
  is silent.
- **Not a systematic review:** this is a screening-grade triage, not a
  reproducible database query with formal inclusion/exclusion criteria.
  Recall is unknown — relevant work may be missing.
- **Claim-status linkage:** claims in `.paper/claims.yml` carry a `status`
  field; `status: gap` claims (here C5 and C6) have empty `evidence_artifacts`
  and map to research gaps ([G2] and [G1] respectively).
- **To upgrade a real deliverable:** re-run `search` with varied query
  phrasings and merge; read the high-relevance papers in full; run the power
  analysis flagged in Q2.
