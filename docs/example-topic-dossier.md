# Topic Decision Dossier — LLM applications in water resources

## 1. Executive Decision Summary

| Field | Value |
|---|---|
| Area | Applications of large language models in water resources |
| Compiled | 2026-05-22 |
| Verdict grade | Screening-grade — assembles evidence; does NOT decide worth |
| Search confidence | Medium — Semantic Scholar was unavailable during the run |

Two candidate topics were evaluated for applying large language models to
water resources.

| Candidate 1 | LLM-driven water resources management |
|---|---|
| **Verdict** | Do not pursue — as stated |
| **Reason** | A hydrology-specific LLM benchmark (HydroLLM, Kizilkaya et al. 2025) and a bibliometric analysis of LLMs in hydrology (Sajja et al. 2025) both exist — a field with a benchmark and a review is established, not an opening. |

| Candidate 2 | LLM agents for human behaviour in socio-hydrology |
|---|---|
| **Verdict** | Worth pursuing — only if its open conditions hold |
| **Reason** | No paper builds calibrated LLM agents for socio-hydrology, but Schück (2026) is a peer-reviewed paper that explicitly cautions against using LLMs for human data in human-water research — the project's validation design must answer that caution. |

**Key uncertainty.** Recall confidence is only medium — Semantic Scholar
was rate-limited during the run, so a missed paper for Candidate 2 is
possible until the search is re-run with that backend enabled.

## 2. Candidate Definitions

**Candidate 1 — LLM-driven water resources management.** Using LLMs and
LLM agents for water resources management and decision support:
hydrological forecasting, reservoir and river operations, monitoring, and
planning. *Why it could be a gap:* No one has tried this — applying LLMs,
a recent capability, broadly across water-resources management.

**Candidate 2 — LLM agents for human behaviour in socio-hydrology.** Using
LLM agents to represent how individual stakeholders and households make
water decisions inside a coupled human–water (socio-hydrology) model, with
those agents calibrated and checked against observed water-use and
adaptation behaviour. *Why it could be a gap:* No one has tried this — no
calibrated LLM agents exist for stakeholder behaviour in a
socio-hydrology model.

## 3. Decision Scorecards

**Candidate 1 — LLM-driven water resources management**

| Gate | Score | Rationale |
|---|---|---|
| Gate 1 — Gap still open | 1/5 strongly disagree | Occupied: a benchmark, a review and a bibliometric study exist |
| Gate 2 — Real contribution | Not assessed | Failed Gate 1 |
| Gate 3 — Feasible | Not assessed | Failed Gate 1 |
| **Verdict** | **Do not pursue — as stated** | Broad field is firmly established |

**Candidate 2 — LLM agents for human behaviour in socio-hydrology**

| Gate | Score | Rationale |
|---|---|---|
| Gate 1 — Gap still open | 3/5 neutral | Open, but the search was only medium-confidence |
| Gate 2 — Real contribution | 3/5 neutral | Borderline — the contribution depends on the validation design |
| Gate 3 — Feasible | 3/5 neutral | Feasible with effort — the behavioural dataset is the binding constraint |
| **Verdict** | **Worth pursuing — only if its open conditions hold** | All three gates clear at neutral; conditional on the checks in §6 |

## 4. Evidence Base

**Search funnel.**

| Stage | Count |
|---|---|
| Retrieved (6 adversarial query phrasings) | 435 unique papers |
| Returned for relevance screening | 25 |
| Kept on-topic by the relevance gate | 25 |
| Selected into the prior-art corpus | 13 |

**Prior-art classification of the 13-paper corpus.**

| By evidence type | By candidate |
|---|---|
| 6 primary studies, 2 reviews, 1 survey, 1 perspective, 1 caution paper, 2 close analogues | 9 bear on Candidate 1, 4 on Candidate 2 |

**Closest prior work.**

- **Candidate 1:** the field is broadly worked. Key items: a
  hydrology-specific LLM benchmark dataset (Kizilkaya et al. 2025,
  *HydroLLM* — primary study); a bibliometric analysis of LLMs in
  hydrology (Sajja et al. 2025 — review); a systematic review of AI in
  water regulation (Wang et al. 2026 — review); LLMs fine-tuned for
  environmental problems (Zhang et al. 2025 — primary study); and
  conversational water-quality LLM agents (Ravindran et al. 2025 —
  primary study). A benchmark together with a bibliometric study is a
  clear field-maturity signal — the occupancy signal is solid.
- **Candidate 2:** no paper builds calibrated LLM agents for
  socio-hydrology. The closest in-domain work is Batista et al. 2025
  (close analogue — an LLM that models *sentiment* for water governance,
  not agent-based decision modelling). Schück (2026) is the dominant
  caution paper. Braga et al. 2025 and Khaki et al. 2025 are out-of-domain
  LLM human-behaviour analogues. The direct evidence is thin — which is
  what keeps the gap open.

## 5. Gate-by-Gate Assessment

### Gate 1 — Gap still open

- **Score.** Candidate 1: 1/5 (strongly disagree). Candidate 2: 3/5
  (neutral).
- **Evidence.** For Candidate 1, the field has a benchmark, a systematic
  review, a bibliometric analysis, and primary fine-tuning and
  conversational-agent studies — the broad gap is firmly taken. For
  Candidate 2, no paper does the calibrated-LLM-agent-for-socio-hydrology
  task; only one close in-domain analogue (Batista 2025, sentiment) and a
  caution paper (Schück 2026) bear on the slice.
- **Interpretation.** Candidate 1 is occupied; pursuing it as stated would
  produce work the field already has. Candidate 2 reads as open, but the
  medium-confidence search means the verdict is tentative.
- **Risk.** Semantic Scholar was rate-limited during the run, so a missed
  paper for Candidate 2 remains possible. "Absent from this corpus" is
  not proof of "open".
- **Action needed.** Re-run the search with a Semantic Scholar API key
  enabled before relying on Candidate 2's openness.

### Gate 2 — Real contribution

- **Score.** Candidate 1: not assessed (failed Gate 1). Candidate 2: 3/5
  (neutral).
- **Evidence.** No abandoned attempt was found. Schück (2026) is a
  peer-reviewed perspective that engages the exact premise as a standing
  caution. Batista (2025) is the closest in-domain prior work using an
  LLM on a human signal for water governance, but it is sentiment
  analysis, not agent-based decision modelling.
- **Interpretation.** What Candidate 2 would contribute is a **validated
  method for representing household water-adaptation decisions with LLM
  agents** — agents whose choices are calibrated to, and tested against,
  observed adaptation behaviour, usable as the behavioural layer of a
  socio-hydrology model. The contribution is the validated behavioural
  representation, not "LLM agents in water". Novelty is borderline; the
  validation requirement is what could lift the work from an extension
  to a new capability.
- **Risk.** **Construct validity** — whether LLM-generated behaviour
  faithfully represents real human water decisions, or merely looks
  plausible. This is precisely the risk Schück raises.
- **Action needed.** A minimum validation sketch the proposal must
  satisfy: behaviour target = observed household adaptation decisions
  (e.g. whether a household adopted a flood-protection measure or changed
  water use under scarcity); baseline = a conventional discrete-choice
  model or a rule-based ABM agent; held-out test = predict decisions on a
  held-out household set the LLM agents were not tuned on; main failure
  mode the study must survive = plausible-sounding but
  population-unrepresentative behaviour.

### Gate 3 — Feasible

- **Score.** Candidate 1: not assessed (failed Gate 1). Candidate 2: 3/5
  (neutral).
- **Evidence.** Household water-use and adaptation behaviour data are
  partly public; hydrological data are largely public; LLM API access is
  available at a metered cost. Baseline models (discrete-choice /
  rule-based ABM) are standard. Household behaviour data carries privacy
  and consent constraints — a targeted survey needs ethics approval.
  Reproducibility is a concern: LLM outputs depend on an external API
  model. A thesis-sized project fits one region, a few hundred
  households' behaviour data, one socio-hydrology coupling, and roughly
  12–18 months of work; LLM API cost is modest (low hundreds of USD).
- **Interpretation.** The **binding constraint** is the
  behavioural-validation dataset. Proposal-feasible now — the design can
  be fully articulated. Dissertation-feasible conditional on the dataset:
  if a reusable behaviour dataset exists, a full dissertation is
  realistic; if primary collection is required, the project is still
  feasible but a data-collection phase will dominate the first year.
- **Risk.** Privacy and consent constraints on household-behaviour data,
  plus reproducibility — LLM agent outputs depend on an external API
  model that can change or be retired.
- **Action needed.** Identify a reusable observed-behaviour dataset (one
  lead worth checking first: Jiang et al. 2026 build socio-hydrological
  models of the North China Plain with policy scenarios). Failing that,
  plan a primary-collection schedule with ethics approval that fits the
  project timeline. Pin LLM model versions and archive prompts and
  outputs for reproducibility.

## 6. Risks and Upgrade / Kill Tests

**Named risks.**

- **Construct-validity risk** — whether LLM-generated behaviour faithfully
  represents real human water decisions, or only looks plausible; this is
  the risk Schück (2026) raises against the very approach Candidate 2
  takes.
- **Dataset-constraint risk** — the behavioural-validation dataset is the
  binding feasibility constraint for Candidate 2; if no reusable dataset
  is found, primary collection dominates the timeline.
- **Novelty risk** — Candidate 2 sits at the borderline between a new
  capability and an extension; Batista 2025 is a weaker realised form
  (LLM sentiment for water governance) that the project must out-distance.
- **Reproducibility risk** — LLM outputs depend on an external API model;
  the design must pin model versions and archive prompts and outputs so
  the work can be re-run when the API model changes or is retired.

**Upgrade / kill test — Candidate 2: LLM agents for human behaviour in
socio-hydrology.** Worth pursuing once **all** of these hold:

1. A full-recall search re-run with Semantic Scholar enabled returns no
   paper that already builds calibrated LLM agents for socio-hydrology.
2. A pilot produces a held-out validation result in which the LLM agents
   predict observed household-adaptation decisions at least as well as a
   discrete-choice or rule-based ABM baseline on the same held-out set.
3. A reusable observed-behaviour dataset is identified, or a
   primary-collection schedule with ethics approval that fits the project
   timeline is in hand.

Not worth pursuing if the re-run surfaces such a paper, **or** the pilot
shows the agents cannot beat a trivial baseline or cannot be calibrated,
**or** no behavioural dataset is obtainable within scope.

**Salvage path — Candidate 1: LLM-driven water resources management.**
The broad form is closed, but a specific under-served sub-problem may not
be — for example a particular water-management task the existing
benchmark and review literature does not cover. Recovering it needs a
fresh, narrower search aimed at that sub-problem, not the broad area.

## 7. Recommended Next Steps

The broad "LLM-driven water resources management" topic should not be
pursued in its current form. The field is firmly established — a
benchmark, a systematic review, and a bibliometric analysis all exist —
and committing to the broad framing would not yield a defensible
contribution. If a specific water-management sub-problem under-served by
the existing literature is of interest, the next move there is a fresh,
narrower search aimed at that sub-problem.

The narrower "LLM agents for human behaviour in socio-hydrology" topic
remains conditionally promising. Before commitment, three actions are
required: re-run the literature search with Semantic Scholar enabled to
confirm the gap; read Schück (2026) and design the validation around its
construct-validity caution — at minimum a held-out comparison against a
discrete-choice or rule-based ABM baseline on real household-adaptation
decisions; and either identify a reusable behavioural dataset or plan a
primary-collection schedule with ethics approval that fits the project
timeline.

---

## Appendix A. Search and Screening Protocol

| Field | Value |
|---|---|
| Search date | 2026-05-22 |
| Databases searched | crossref, OpenAlex, arXiv. Semantic Scholar was rate-limited (HTTP 429) and contributed nothing this run. |
| Query families | Six adversarial phrasings of "LLM applications in water resources / management / hydrology", generated by `search --adversarial` |
| Number retrieved | 435 unique papers (after backend-level deduplication) |
| Deduplication rule | DOI-based primary, arXiv ID fallback; near-duplicate titles consolidated |
| Inclusion criteria | Papers genuinely about LLMs applied to water resources, *or* close behavioural analogues bearing on Candidate 2 (LLM agents simulating human decisions). 13 entered the prior-art corpus. |
| Exclusion criteria | Tangential AI-in-water papers not about LLMs; duplicates; out-of-domain LLM work without a behavioural-analogue role |
| Screening process | Automated relevance gate (BM25 fit-check, `search --screen`) returned 25 on-topic of the top-screened set; agent judgement selected 13 for the corpus and assigned the evidence-type tags |
| Known limitations | Semantic Scholar unavailable; some 2026 conference abstracts have empty crossref records; corpus is skewed to 2024–2026 (expected for an LLM-applications topic) |
| Recall confidence | Medium. For a tighter verdict, re-run the search with `SEMANTIC_SCHOLAR_API_KEY` set. |

## Appendix B. Deliverable File List

| File | What it is | What it gives you |
|---|---|---|
| `topic_dossier.md` / `.docx` | This document — the topic-decision memo | The verdict on each candidate and the evidence behind it |
| `topic_dossier.bib` | The reference list, as BibTeX | Every cited paper with a resolvable DOI — lets you verify "open" yourself |
| `literature_matrix.md` | The paper-by-paper comparison table | How each retrieved paper compares — method, claim, evidence type, limitation |
| `topic_dossier.gaps.yml` | Machine-readable export | Structured data for a downstream tool or a later pass; not needed for reading |

```
en/
├── topic_dossier.md / .docx
├── topic_dossier.bib
├── literature_matrix.md
└── topic_dossier.gaps.yml
```

A Traditional Chinese mirror of this deliverable is in the sibling
`zh-TW/` folder.
