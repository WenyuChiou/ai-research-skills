# Full Research Pipeline

The 8 stages of a research project, with the skills that fit each one.
This is the comprehensive reference — most users get what they need
from the [README's persona table](../README.md#pick-your-starting-point)
and never need to read this.

繁中: [pipeline.zh-TW.md](pipeline.zh-TW.md)

```text
1. Discover lit  →  2. Organise & compare  →  3a. Frame  →  3b. Plan
        →  4. Build model  →  5. Run & validate (C&V)  →  6. Visualise
        →  7. Draft manuscript  →  8. Submit, respond, wrap up
```

Three skills don't belong to a specific stage — they're triggered by
*task character*, not pipeline position. See **Cross-cutting tools**
at the bottom.

## 1. Discover literature

> *"What has been done? What should I read?"*

Tools you probably use: **Zotero · NotebookLM · Obsidian** *(no native
OneNote skill — use Obsidian as the notes layer.)*

| Skill | What it does |
|---|---|
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | Search arXiv / Semantic Scholar / CrossRef / PubMed, ingest metadata, write paper notes into Obsidian. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) | Add, tag, deduplicate, and clean Zotero items beyond the research-hub pipeline. |

## 2. Organise & compare literature, find the gap

> *"Where is the research gap? Which 5 papers actually matter?"*

| Skill | What it does |
|---|---|
| [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | Compare papers by method, data, claim, limitation, and relevance — without rereading every PDF. |
| [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | Verify a NotebookLM brief against the source bundle. Catches missed sources, unsupported claims, and contradictions. |
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | Build the Obsidian cluster and the NotebookLM source bundle that feed the matrix. |
| [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) *(optional)* | Audit Zotero before comparison — find duplicate DOIs, orphan items, propose tag/collection cleanup. Read-only. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | Apply the cleanup the curator proposes — full CRUD on Zotero items. |

## 3a. Frame the problem

> *"Is my research question sharp enough to be falsifiable?"*

A Socratic dialog partner that asks structured questions to surface
what you'd otherwise leave implicit.

| Skill | What it does |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | Walks you through 5 segments — research question → expected mechanism → identifiability check → validation plan → risk register — and writes `.research/design_brief.md`. |

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

Re-read the `design_brief.md` produced in Stage 3a as your model spec,
then generate implementation scaffolding.

| Skill | What it does |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | Same skill as 3a — re-read `.research/design_brief.md` here when translating "what to model" into "how to model". |

For implementation scaffolding (test harness, plotting, batch edits)
and design review by long-context reading, use the **Cross-cutting
tools** (`codex-delegate`, `gemini-delegate`) below.

## 5. Run experiments, calibrate, and validate (C&V)

> *"Is the run reproducible, checkable, extensible? Can I save tokens
> across long sessions?"*

| Skill | What it does |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Token-saving manifests so each run-and-check session doesn't start from zero. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Cheap re-onboarding when you switch experiments or come back days later. |

For repeatable sweeps and post-fix verification, delegate via the
**Cross-cutting tools** below.

## 6. Visualise and interpret results

> *"What does the figure actually show? Does my caption match?"*

Tools: **matplotlib / plotly / your plotting stack of choice.**

| Skill | What it does |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) | Generate or refactor plotting scripts (consistent style across N figures, batch re-renders). |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) | Pair a figure with a draft caption / interpretation paragraph using long-context reading. |

## 7. Draft and revise the manuscript

> *"Does the prose match the figure? Does it fit the target journal?
> Does it sound human?"*

| Skill | What it does |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | Extract `.paper/claims.yml` and `.paper/figures.yml` so writing tools see the same numbers as the figures. |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) | Manuscript revision, claim-evidence audit, banned-word / humanize pass, figure-text consistency, journal-format check. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | Deep-edit bibliography entries when the writing skill flags references that need cleanup. |

For long-form bilingual rewrites or 繁中 / CJK drafts, use the
**Cross-cutting tool** `gemini-delegate` below.

## 8. Submit, respond to reviewers, wrap up

> *"Are my claims defensible? Is the reviewer response complete? Is the
> project state preserved for future me?"*

| Skill | What it does |
|---|---|
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) | Reviewer response tables, pre-submission checklist, journal-format audit, rebuttal letter. |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Freeze the project's final state so future AI sessions (or future you) can resume in seconds. |

## Cross-cutting tools — used at every stage

Three skills don't belong to a specific stage — they're triggered by
*task character*:

| Skill | Trigger | What it does |
|---|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) | Token-heavy mechanical work | Hand batch edits, scaffolding, refactors, test generation, plotting scripts to Codex CLI. |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) | Long-context reading or 繁中 / CJK output | Hand long-PDF synthesis, bilingual rewrites, second-opinion review to Gemini CLI. |
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | "Who should do this?" | Stage-agnostic, character-driven routing — produces a delegation plan + handoff prompts. |
