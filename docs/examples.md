# What the skills actually produce

Real deliverable shapes so you can decide whether each skill fits your
workflow *before* installing it. All examples below use **synthetic
data** — no real maintainer artifacts.

Languages: [English](examples.md) | [繁中](examples.zh-TW.md)

> The samples are illustrative. Your inputs and prompts will produce
> output of the same *shape* but different content; row counts, tone,
> and verdict mix vary with the source material.

---

## `literature-triage-matrix` — 5 papers, 9 columns

**Input**: A folder of 5 papers (PDFs, Obsidian notes, or Zotero
collection items) + the prompt *"compare these 5 papers by method,
data, claims, limitations."*

**Output** — written to `.research/literature_matrix.md`:

| Citation | Year | Type | Method | Data | Central claim | Domain | Limitation | Relevance |
|---|---|---|---|---|---|---|---|---|
| Chen 2022 | 2022 | empirical | finite-difference flood model, 30 m grid | Hurricane Harvey, 5-day window | Coastal subsidence amplifies surge inundation by 12-18% | Coastal hydrology | Single event; no recurrence-interval sweep | High — direct method match |
| Patel 2023 | 2023 | tooling | open-source ABM platform (`pyabm`) | Synthetic 1000-agent runs | Decentralised insurance pricing converges in <20 ticks under heterogeneous risk | Insurance ABM | No empirical calibration | Medium — pipeline reference |
| Ortiz-Lim 2024 | 2024 | conceptual | Argument-mining + risk taxonomy | 47 IPCC AR6 chapters | "Compound risk" is operationalised inconsistently across WG2 vs WG3 | Climate risk taxonomy | No code; no replication artifact | Low — adjacent framing |
| Kumar 2026 | 2026 | empirical | LLM-as-agent, 6-round multi-issue bargaining | 1200 simulated dyads | Theory-of-mind prompting raises Pareto-efficiency by 9 pp | Multi-agent LLM | Single LLM provider; no human baseline | High — recent + reproducible |
| Wang 2026 | 2026 | empirical | Streaming-platform telemetry + agent-based replay | 4.3M user-streamer interactions | Triadic feedback loop between viewer-streamer-platform reproduces engagement skew | Social ABM | Platform-specific; not pre-registered | Medium — methodological transfer |

**Sanity grid** that the skill auto-emits below the matrix:

```
Method × Domain   coastal  insurance  taxonomy  multi-agent  social-abm
  empirical          1         0          0          1           1
  tooling            0         1          0          0           0
  conceptual         0         0          1          0           0
```

When the grid shows a row/column with only one paper, you can ask the
skill to find more in that cell before writing the lit-review section.

---

## `academic-writing-skills` — banned-word audit + reviewer response

### Banned-word audit (input = a single paragraph)

**Input**: *"The proposed framework leverages a novel deep-learning
pipeline to comprehensively delve into the multifaceted challenges of
flood resilience, robustly demonstrating that our approach is
significantly better than baselines."*

**Output** — line-by-line audit table:

| Span | Banned term | Why flagged | Suggested replacement |
|---|---|---|---|
| "leverages a novel" | `leverages`, `novel` (GenAI filler × 2) | Empty intensifiers; "novel" rarely survives peer review unedited | "uses" / drop "novel" |
| "comprehensively delve" | `delve` | `delve` is on the high-confidence GenAI-fingerprint list (banned_words.md §A) | "examine" / "study" |
| "multifaceted challenges" | `multifaceted` | Empty modifier; specify what makes the challenge multidimensional or drop | "challenges across X, Y, Z dimensions of …" |
| "robustly demonstrating" | `robustly` (without a robustness check cited) | Overclaim absent supporting analysis | drop adverb; state the test that earns the word |
| "significantly better" (no *p*-value / effect size) | `significantly` (vernacular vs statistical) | Reviewer pattern: 1 in 4 reviewers will flag | "outperforms baselines by *X%* (CI [a, b])" |

**Summary verdict**: 5 issues / 1 paragraph. Recommend revision before
submission.

### Reviewer-response table (input = `.paper/reviewer_comments.md`)

**Input** — a `.paper/reviewer_comments.md` with 6 comments numbered R2.1-R2.6.

**Output** — `.paper/reviewer_responses.md` skeleton:

| Comment | Anchor (manuscript span) | Author response (student tone) | Manuscript change | Evidence cited |
|---|---|---|---|---|
| R2.1 — *"Figure 3 axis ordering is unconventional."* | §4.2 Fig. 3 caption | Fixed. Reordered axes to median-asc, retained outlier band. | Fig. 3 panels (b, c) regenerated. | `figures/fig3_v2.pdf` |
| R2.2 — *"Where does the 12% number come from?"* | §3.1 last paragraph | The 12% is the mean of bootstrap distributions (n=10000), now reported with 95% CI. | Added "Mean 12% (95% CI 9-15%)" to §3.1. | `.paper/figures.yml` row C3 |
| R2.3 — *"Why not cite Smith 2019?"* | §1.3 background | Added. Smith 2019 frames the FFE/EH distinction we use; relevant. | Citation added at §1.3; reference list updated. | Smith 2019 *J. Hydrol.* 575:122-138 |
| R2.4 — *"Discussion overclaims the policy lesson."* | §6 last paragraph | Agreed. Softened "proves" → "is consistent with" and added domain caveat. | §6 rewritten; 1 sentence on transferability scope. | — |
| R2.5 — *"Section 5 is repetitive."* | §5.1, §5.4 | Removed §5.4 (duplicated §5.1's mechanism); merged surviving content into §5.1. | §5 cut from 4 subsections to 3. | — |
| R2.6 — *"Where is the code?"* | (missing) | Public Zenodo DOI added to acknowledgements + footnote. | Added Zenodo DOI + repo URL to acknowledgements. | DOI 10.5281/zenodo.xxxxxxx |

Tone, banned-word audit, and concession-threshold rules from
`reviewer_response_workflow.md` are applied during generation.

---

## `zotero-library-curator` — preview-only audit report

**Input**: An 800-item Zotero library + prompt *"audit my library for
duplicates, orphan tags, and bloat."*

**Output** — written in conversation (no library writes):

```
Library audit — 2024-03-15  (synthetic — not a real maintainer run)

Items inspected:       814
Read-only?             yes (no changes applied)

Findings:
  ▸ Duplicate DOIs:          11   (3 high-confidence pairs shown below)
  ▸ Orphan-tag items:        42   (items with no tags in any collection)
  ▸ Near-duplicate tags:     27   (case-only or trailing-whitespace variants)
  ▸ Sparse tags (≤2 items):  398  (81% of total tag vocabulary)
  ▸ Cluster bloat (>200):    1    ("methodology" — 247 items, consider sub-splits)

High-confidence duplicate pairs:
  1. doi:10.1029/2018wr023456
     - keep: Chen, Y. (2018) — "Flood model intercomparison" — has full text
     - merge: Chen, Y. (2018) — same DOI, no attachment, manual entry
  2. doi:10.1038/s41586-020-2649-2
     - keep: Wei, K. (2020) — has annotations + tags
     - merge: K. Wei (2020) — duplicate author-format entry
  3. doi:10.1175/jhm-d-19-0157.1
     - keep: full citation w/ collection assignments
     - merge: bare title-only entry

Suggested next action:
  Hand the high-confidence pairs to `zotero-skills` (the CRUD plugin):
    "merge the 3 duplicate DOIs identified by the curator audit"
  Curator does NOT write; zotero-skills DOES. Back up the library first.
```

The curator only emits this report; the actual merge / delete happens
in `zotero-skills` after you confirm.

---

## `paper-summarize` — Key Findings markdown block per paper

**Input**: An Obsidian cluster of 5 ingested papers whose per-paper
notes still have TODO skeletons (created by `research-hub auto`).

**Output** — for each paper, one markdown block written into both the
Obsidian note AND the matching Zotero child note (atomically rolled back
if the Zotero write fails):

```markdown
## Key Findings

- Decentralised insurance pricing under heterogeneous risk converges
  in <20 ticks across all 36 parameter combinations the authors
  swept. The convergence is robust to asymmetric information but
  brittle when more than 30% of agents underreport risk class
  (convergence time grows super-linearly).
- The pricing mechanism's stability depends on the *number* of
  insurers, not their market share — a 5-insurer 80/20 market and a
  5-insurer 20/20/20/20/20 market both converge in the same horizon.

## Methodology

- Agent-based simulation in `pyabm` (Patel's open-source platform).
- 1000 agents per run; 36 parameter combinations (3 risk-class
  distributions × 4 information regimes × 3 market structures).
- Outcome metric: time-to-equilibrium plus a Lyapunov-style stability
  index defined in §3.2.

## Relevance

- Method match: directly relevant to a reader's own coupled ABM
  project — substitute your active project name and section reference.
- Use-case: pricing-mechanism robustness check (or analogous
  mechanism-stability check) under whichever risk-misperception
  scenario you're modelling.
- Skip if: not working on insurance / pricing mechanisms; this paper
  is upstream tooling, not a substantive ABM claim about social
  outcomes.
```

The block lands at the existing `## Key Findings` / `## Methodology` /
`## Relevance` headings (it replaces TODO skeletons, doesn't append).

---

## `gap-to-topic` — 3-gate decision dossier for a candidate topic

**Input**: A candidate thesis or proposal topic (Socratically articulated
in §0) — e.g. *"LLM agents for human behaviour in socio-hydrology"* — plus
the broader area to search (*"LLM applications in water resources"*).

**Output bundle** — 4 files written to `.research/`, plus a matching
`topic_dossier.docx` emitted via `scripts/dossier_to_docx.js`:

| File | What it is |
|---|---|
| `topic_dossier.md` / `.docx` | 7-section + 2-appendix research-grade decision memo: Executive Summary with per-candidate verdict cards → Definitions → Decision Scorecards (3 gates × Likert) → Evidence Base → Gate-by-Gate Assessment → Risks & Kill Tests → Recommended Next Steps → reproducibility-log Appendix A → file-list Appendix B |
| `topic_dossier.bib` | BibTeX reference list — every cited paper with a resolvable DOI / arXiv ID |
| `topic_dossier.gaps.yml` | Machine-readable structured export — per-gap `verdict` / `verdict_reason` / `feasibility` / `dead_end_status` plus `open_questions[]`. Read by `research-design-helper` v0.3.12+ for Stage 3a handoff |
| `literature_matrix.md` | Paper-by-paper comparison table (method / claim / evidence type / limitation / relevance) — built by `literature-triage-matrix` as §1 step 2 |

**Verdict shape** — each candidate gets one of three outcomes:

| Verdict | Meaning | Color in `.docx` |
|---|---|---|
| **Do not pursue — as stated** | At least one gate fails (occupied / not a contribution / not feasible). Salvage path optional. | Light red |
| **Worth pursuing — only if its open conditions hold** | All three gates clear at neutral or better, but conditional on operational follow-ups (e.g. dataset identification, validation pilot). | Light yellow |
| **Worth pursuing** | All three gates clear unconditionally. | Light green |
| **Not assessed** | Gate skipped because an earlier gate already failed. | Light grey |

A complete bilingual example, copied from a real dogfood run (LLM
applications in water resources, two candidates evaluated, one
`do-not-pursue` + one `conditional-go`), ships in this repo as:

- [`example-topic-dossier.md`](example-topic-dossier.md) / [`.docx`](example-topic-dossier.docx)
- [`example-topic-dossier.bib`](example-topic-dossier.bib)
- [`example-topic-dossier.gaps.yml`](example-topic-dossier.gaps.yml)
- [`example-topic-dossier.zh-TW.md`](example-topic-dossier.zh-TW.md) / [`.zh-TW.docx`](example-topic-dossier.zh-TW.docx)

The `.docx` files render with bilingual verdict colour coding
(`gen_docx.js` regex matches both English `"do not pursue"` and zh-TW
`"不予推進"`) and en / zh-TW font auto-selection (Microsoft JhengHei
when the filename matches `.zh|zh-|zh_|-tw|-cn`, Arial otherwise).

---

## Putting it together — a full literature-review deliverable

The per-skill samples above are fragments. Run the research-hub literature
pipeline end to end — `search` → `literature-triage-matrix` →
`research-design-helper` — and those fragments add up to one consolidated
document: a **literature-review deliverable** — all nine sections, from a
TL;DR and literature inventory through per-paper summaries, a cross-paper
synthesis, a tagged research-gap analysis, open questions, a recommended
next step, references, and a provenance section.

A complete synthetic example — the full 9-section shape, ready to reuse as a
template — is at
[`example-literature-review-deliverable.md`](example-literature-review-deliverable.md)
([繁中](example-literature-review-deliverable.zh-TW.md)).

---

## What these examples do NOT show

- **Real time-to-complete numbers** — see `README.md` § "Time + cost
  expectations" for realistic ranges. Output length scales with input;
  a 5-paper triage matrix typically completes in 1-3 minutes of
  conversation; a 6-comment reviewer response in 3-8 minutes.
- **Errors and edge cases** — every skill has a `## Limitations`
  section in its own SKILL.md. When a skill cannot find the input it
  expects (no `.paper/`, no Zotero connection, no source bundle), it
  prints a clear "missing prereq" message rather than hallucinating
  output.
- **Real research data** — the matrix, banned-word audit, library
  report, and Key Findings above are synthetic. Real results from the
  maintainer's workflow are not published in this catalog (per the
  `## Limitations` policy of "no real maintainer artifacts").

Open an [issue](https://github.com/WenyuChiou/ai-research-skills/issues)
if a skill produces output meaningfully different from the shape shown
here — that's a real bug worth reporting.
