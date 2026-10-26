# Full Research Pipeline

The 8 stages of a research project, with the skills that fit each one.
This is the comprehensive reference — most users get what they need
from the [README's Pick-by-goal table](../README.md#pick-by-goal)
and never need to read this.

繁中: [pipeline.zh-TW.md](pipeline.zh-TW.md)

```text
1. Discover lit  →  2. Organise & compare  →  3a. Frame  →  3b. Plan
        →  4. Build model  →  5. Run & validate (C&V)  →  6. Visualise
        →  7. Draft manuscript  →  8. Submit, respond, wrap up
```

Four skills don't belong to a specific stage — they're triggered by
*task character*, not pipeline position. See **Cross-cutting tools**
at the bottom.

For end-to-end AI-for-science inputs, outputs, quality evidence, and researcher
decisions at each existing stage, see [scientific lifecycle and quality gates](scientific-lifecycle.md).

## 1. Discover literature

> *"What has been done? What should I read?"*

Start with the search, deep-research, reading, citation and relevant skills
actually available in **Codex or Claude Code**. Do not assume that either host
exposes every capability: record what was used, available but untested, or
unavailable here. Follow the canonical [research protocol](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/references/research-protocol.md)
and [source-claim audit guidance](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/references/source-claim-audit.md),
not a second catalog-owned search engine.

**Research Hub itself is optional.** Native AI Skills discovery and source
reading can use the host's available tools without installing or configuring
Research Hub. Shared protocol references are instructions, not a requirement
to run Hub. If the user chooses Hub, it offers an optional route for
organization, persistence and selected workflow/integration operations.
Check only the setup and access needed for those selected operations;
do not add mandatory Hub CLI setup, integration accounts, API keys or logins
to the native route. Host tool access still depends on the host's actual
authorized capabilities.

### Agree the round and search routes

Take the topic, target count and reading depth in natural language. Reuse
preferences already supplied; ask only about missing choices that matter. For
example, "about 12 papers, abstracts first, then read two core papers closely"
already supplies both count and depth. Do not repeat those intake questions or
require a form. When a count is needed but unspecified, propose a need-based
round of **10–20 relevant distinct papers**, adjusted to the question and
available evidence. This is not a quota or a 30-paper default: do not pad weak
matches, duplicate versions or inaccessible papers to reach a number. Report
shortfalls and uncovered needs; a smaller useful set may be the right outcome.

Decompose the question into concepts, keywords, synonyms, abbreviations and
adjacent terminology. Try multiple relevant search routes and query variants,
then backward and forward citation chasing. Record routes actually used and
their results or failures; a single query is not evidence of broad coverage.
Explain each relevant role: **classic** for foundational context, **core** for
the present question, **nearest** for the closest topical comparator,
**methodological** for a method/data contribution, and **contrary** for evidence
that challenges the working claim. Roles may overlap; age, citation count or
method similarity alone does not make a paper core or nearest.

### Keep counts and reading evidence separate

Report raw hits separately from distinct works **discovered**, works
**screened**, works **included**, **reading-depth counts**, and the **core
count**. Deduplicate preprint/journal/revision versions at work level while
preserving version identities, links and the exact version read. Do not count
versions as extra papers; if genuinely distinct studies share a lineage,
explain the distinction. Inclusion records relevance, not full-body access:
important pending/background works may remain included with access limits
visible. A core selection is not a claim that it was read.
Reading levels such as `not-read`, `abstract-only`, `selected-sections` and
`full-text` describe actual reading, not file availability or storage status.
Bind every summary and consequential claim to that source/version and the
sections actually read; do not transfer support across versions unchecked.

The handoff records search needs/queries and their observed results, source
identity and version/date, actual reading level and claim locators, closest or
contrary work, and remaining `not-read` / `unknown` items. Read the relevant
methods/results before relying on a full-text claim; an abstract-only summary,
search hit, filled locator or structural check is not source-level verification.
Distinguish an author-maintained query ledger from retained invocation receipts;
do not rerun a search merely to manufacture a missing historical receipt.

### Check full-body eligibility before archiving or NotebookLM

Archive/NotebookLM eligibility requires a **lawfully publicly accessible full
body**, with the actual PDF or substantive body validated for the intended
work/version. Inspect the response and readable content/pages; a `.pdf` URL,
HTTP 200, MIME label or PDF signature alone is insufficient. A login page,
abstract/landing page, paywall or error payload is not the paper's full body.
Keep important inaccessible works as pending/background with the access limit
and next safe route recorded; do not discard them, label them fully read, or
upload them as full text. Do not bypass access restrictions. Having a validated
full body still does not establish that every section was read.

**Zotero · NotebookLM · Obsidian are optional integrations**, not prerequisites
for this discovery pass. Use configured storage/automation only when needed and
authorized; do not add accounts or setup steps just to conduct the literature
review. Missing Hub CLI access in one executor does not establish a missing
product capability. A portable/manual handoff is not an executed Hub pipeline.

Let the user choose destinations, including none or later. Keep a separate
receipt for each requested destination/action: source/version, destination
identity, and confirmed success, failure, unknown or skipped outcome. This
catalog specifies guidance; it does not implement those provider capabilities.
**Saved does not mean semantically completed.** A file or upload receipt does
not finish reading, relevance assessment or claim verification. Technical
pending work is not automatically a human-only decision: continue safe bounded
diagnosis/remediation within existing authorization, retaining the blocker when
no safe route remains. Ask the researcher only for a genuine scope/scientific
choice, access permission, resource commitment or separately required write
authorization; do not silently install tools or require optional accounts.

| Skill | What it does |
|---|---|
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) | Use available native discovery and source reading under the shared protocol; optionally use configured arXiv / Semantic Scholar / CrossRef / PubMed search and authorized ingest/storage. |
| [`paper-summarize`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-summarize/SKILL.md) *(optional)* | Fill abstract-only per-paper notes after ingest; does not read PDFs or verify the paper's full-text claims. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | Add, tag, deduplicate, and clean Zotero items when those separately authorized library operations are needed. |

## 2. Organise & compare literature, find the gap

> *"Where is the research gap? Which 5 papers actually matter?"*

| Skill | What it does |
|---|---|
| [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | Compare papers by method, data, claim, limitation, and relevance — without rereading every PDF. |
| [`gap-to-topic`](https://github.com/WenyuChiou/research-hub/blob/master/skills/gap-to-topic/SKILL.md) | 3-gate go/no-go decision dossier for a candidate thesis/proposal topic (open? a contribution? feasible?). Hands `.gaps.yml` to Stage 3a (v0.3.12+). |
| [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | Verify a NotebookLM brief against the source bundle. Catches missed sources, unsupported claims, and contradictions. |
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) | Build the Obsidian cluster and the NotebookLM source bundle that feed the matrix. |
| [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) *(optional)* | Audit Zotero before comparison — find duplicate DOIs, orphan items, propose tag/collection cleanup. Read-only. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | Apply the cleanup the curator proposes — full CRUD on Zotero items. |

## 3a. Frame the problem

> *"Is my research question sharp enough to be falsifiable?"*

A Socratic dialog partner that asks structured questions to surface
what you'd otherwise leave implicit.

| Skill | What it does |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | Walks you through 5 segments — research question → expected mechanism → identifiability check → validation plan → risk register — and writes `.research/design_brief.md`. **v0.3.12+**: auto-pre-fills segments 1 (RQ) and 5 (risks) from `.research/topic_dossier.gaps.yml` if a recent `gap-to-topic` run is present (verdict-aware candidate selection). |

## 3b. Plan the project (capture the artifacts)

> *"What am I claiming, with what data, and what's my plan?"*

Once 3a has shaped the question, these skills capture the plan as
machine-readable manifests so future AI sessions don't reread the whole
repo.

| Skill | What it does |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Write `.research/project_manifest.yml`, `experiment_matrix.yml`, `data_dictionary.yml`. Picks up `design_brief.md` from 3a if present. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Read those manifests and produce a fast orientation memo when you (or a new AI session) come back to the project. |

## 4. Design and build the model

> *"What architecture, equations, agents, or prompts do I need?"*

Re-read `design_brief.md` from Stage 3a as design intent. Develop the
project-specific implementation specification with the researcher before
generating scaffolding; the design helper does not invent model architecture.

| Skill | What it does |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | Same skill as 3a — re-read `.research/design_brief.md` here when translating "what to model" into "how to model". |

For implementation scaffolding (test harness, plotting, batch edits),
use the **Cross-cutting tools** (`codex-delegate`, `antigravity-delegate`)
below. Long-context design review stays with the primary model. If a
single round of work needs both delegates (e.g. Codex writes the test
harness *and* Antigravity performs bounded fixture maintenance), route through the
[`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)
router first — it writes `.coord/multi_ai_plan.md` and the leaves read
their per-task brief.

## 5. Run experiments, calibrate, and validate (C&V)

> *"Is the run reproducible, checkable, extensible? Can I save tokens
> across long sessions?"*

| Skill | What it does |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Token-saving manifests so each run-and-check session doesn't start from zero. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Cheap re-onboarding when you switch experiments or come back days later. |

For repeatable sweeps and post-fix verification, delegate via the
**Cross-cutting tools** below. Multi-delegate rounds in this stage
(e.g. one Codex run for the sweep, a parallel Codex run for the post-
fix verification) go through the
[`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)
router first.

## 6. Visualise and interpret results

> *"What does the figure actually show? Does my caption match?"*

Tools: **matplotlib / plotly / your plotting stack of choice.**

| Skill | What it does |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) | Generate or refactor plotting scripts (consistent style across N figures, batch re-renders). |
| [`antigravity-delegate`](https://github.com/WenyuChiou/antigravity-delegate/blob/master/skills/antigravity-delegate/SKILL.md) | Handle bounded non-honesty-critical mechanical plotting cleanups or fixture maintenance under Claude supervision. |

Captioning, interpretation, and figure-to-claim honesty checks stay with
the primary model. When a figure pass needs both delegates same round
(e.g. Codex re-renders N figures and Antigravity applies bounded
mechanical fixture edits), use the
[`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)
router so the plan and per-task briefs stay in sync.

## 7. Draft and revise the manuscript

> *"Does the prose match the figure? Does it fit the target journal?
> Does it sound human?"*

| Skill | What it does |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | Extract `.paper/claims.yml` and `.paper/figures.yml` so writing tools see the same numbers as the figures. |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) | Extended outlines, paragraph and section drafting, evidence alignment, terminology, repetition, flow, cross-artifact revision, and release checks. |
| [`paper-review`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/paper-review/SKILL.md) | General scientific review that progressively selects the applicable psychometrics/SEM, AI/LLM, water/CNHS, flood/hydrodynamics, or hybrid modules. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | Deep-edit bibliography entries when the writing skill flags references that need cleanup. |

Long-form bilingual rewrites, 繁中 / CJK drafts, and review judgments stay
with the primary model.

## 8. Submit, respond to reviewers, wrap up

> *"Are my claims defensible? Is the reviewer response complete? Is the
> project state preserved for future me?"*

| Skill | What it does |
|---|---|
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) | Cross-file synchronization, submission-package checks, and blocking release readiness. |
| [`paper-review`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/paper-review/SKILL.md) | Round-calibrated top-to-bottom review and prior-comment regression checks; Ethan-style activates only when explicitly requested. |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Freeze the project's final state so future AI sessions (or future you) can resume in seconds. |

## Cross-cutting tools — used at every stage

Four skills don't belong to a specific stage — they're triggered by
*task character*:

| Skill | Trigger | What it does |
|---|---|---|
| [`research-workflow-orchestrator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-workflow-orchestrator/SKILL.md) | Resumable multi-stage workflow | Coordinate existing stages, provenance and explicit human decision gates. |
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) | Token-heavy mechanical work | Hand batch edits, scaffolding, refactors, test generation, plotting scripts to Codex CLI. |
| [`antigravity-delegate`](https://github.com/WenyuChiou/antigravity-delegate/blob/master/skills/antigravity-delegate/SKILL.md) | Bounded non-honesty-critical mechanical work | Hand tightly scoped mechanical edits to Antigravity CLI under Claude supervision. |
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | "Who should do this?" | Stage-agnostic routing across Codex and Antigravity leaves — produces a delegation plan + handoff prompts. |
