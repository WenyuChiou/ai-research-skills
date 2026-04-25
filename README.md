# AI Research Skills

A researcher-facing index of practical AI skills, organised the way a
researcher actually works — from finding the first paper to wrapping up the
final submission.

Languages: [English](README.md) | [繁中](README.zh-TW.md) | [Bilingual / 中英文對照](README.bilingual.md)

This repo is an umbrella catalog. The skills themselves live in their own
repositories so updates, tests, and install instructions stay in one place:

- [`research-hub`](https://github.com/WenyuChiou/research-hub) — Zotero, Obsidian, NotebookLM, `.research/`, `.paper/`.
- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) — manuscript revision, claim audits, reviewer response.
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) — deep Zotero CRUD.
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) — hand coding work to Codex CLI.
- [`gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill) — hand long-context or bilingual work to Gemini CLI.

Target readers: graduate students, PhD researchers, postdocs, research
engineers, and anyone who runs a real research project with AI in the loop.

## Who This Is For

Use this collection if you want AI help with any of these:

- finding and organising papers across Zotero, Obsidian, and NotebookLM,
- comparing literature without rereading every PDF,
- compressing project context so future AI sessions are cheap,
- building, running, and validating models or experiments,
- preparing manuscripts, responding to reviewers, and submitting,
- delegating coding or long-context work to Codex or Gemini.

You do not need every tool. Any two of `Zotero + Obsidian + NotebookLM`
already unlocks most of the workflow.

## Research Pipeline — Pick Your Stage

AI skills are most useful when matched to the stage you are in. Find your
stage below, install the matching skill, and stop asking AI to reread your
project from scratch each time.

```text
1. Discover lit  →  2. Organise & compare  →  3. Frame & plan  →  4. Build model
        →  5. Run & validate (C&V)  →  6. Visualise  →  7. Draft manuscript
        →  8. Submit, respond, wrap up
```

> Most skills below live in [`research-hub`](https://github.com/WenyuChiou/research-hub)
> or [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills).
> The "Lives in" line on each stage tells you which repo to clone.

### 1. Discover literature

> *"What has been done? What should I read?"*

Tools you probably use: **Zotero · NotebookLM · Obsidian** *(no native
OneNote skill — use Obsidian as the notes layer.)*

| Skill | What it does |
|---|---|
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | Search arXiv / Semantic Scholar / CrossRef / PubMed, ingest metadata, write paper notes into Obsidian. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) | Add, tag, deduplicate, and clean Zotero items beyond the research-hub pipeline. |

**Lives in:** `research-hub` (search/ingest) · standalone `zotero-skills`.

### 2. Organise & compare literature, find the gap

> *"Where is the research gap? Which 5 papers actually matter?"*

Tools: **Zotero collections · Obsidian clusters · NotebookLM briefs.**

| Skill | What it does |
|---|---|
| [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | Compare papers by method, data, claim, limitation, and relevance — without rereading every PDF. |
| [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | Verify a NotebookLM brief against the source bundle. Catches missed sources, unsupported claims, and contradictions. |
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | Build the Obsidian cluster and the NotebookLM source bundle that feed the matrix. |

**Lives in:** `research-hub` (all three).

### 3. Frame the problem, plan the project

> *"What am I claiming, with what data, and what's my plan?"*

Tools: **Obsidian project notes · `.research/` manifests in your repo.**

| Skill | What it does |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Write `.research/project_manifest.yml`, `.research/experiment_matrix.yml`, `.research/data_dictionary.yml` so future AI sessions skip the rescan. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Read those manifests and produce a fast orientation memo when you (or a new AI session) come back to the project. |

**Lives in:** `research-hub`.

### 4. Design and build the model

> *"What architecture, equations, agents, or prompts do I need?"*

Tools: **your repo + IDE.**

There is no model-design-specific skill in this catalog yet. Closest match:

| Skill | What it does |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | Hand scaffolding, batch edits, boilerplate, and many-file refactors to Codex CLI. Claude reviews; Codex types. |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | Use Gemini's long context for design reviews, second opinions, and reading large reference codebases. |

**Lives in:** standalone `codex-delegate` and `gemini-delegate-skill` repos.

### 5. Run experiments, calibrate, and validate (C&V)

> *"Is the run reproducible, checkable, extensible? Can I save tokens
> across long sessions? Can I share work across multiple AIs?"*

Tools: **your repo + multi-AI CLIs (Claude, Codex, Gemini).**

| Skill | What it does |
|---|---|
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | Decide what stays in Claude vs. what goes to Codex (code-heavy) vs. Gemini (long context, bilingual). Plan the handoff. |
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | Repeatable Codex runs for sweeps, regression tests, and post-fix verification. |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Token-saving manifests so each new run-and-check session does not start from zero. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Cheap re-onboarding when you switch between experiments or come back days later. |

**Lives in:** `research-hub` (multi-ai, compressor, orienter) · standalone `codex-delegate`.

### 6. Visualise and interpret results

> *"What does the figure actually show? Does my caption match?"*

Tools: **matplotlib / plotly / your plotting stack of choice.**

There is no visualisation-specific skill in this catalog yet. Closest match:

| Skill | What it does |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | Generate or refactor plotting scripts (consistent style across N figures, batch re-renders). |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | Pair a figure with a draft caption / interpretation paragraph using long-context reading. |

**Lives in:** standalone `codex-delegate` and `gemini-delegate-skill`.

### 7. Draft and revise the manuscript

> *"Does the prose match the figure? Does it fit the target journal? Does
> it sound human?"*

Tools: **Word · LaTeX · Markdown.**

| Skill | What it does |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | Extract `.paper/claims.yml` and `.paper/figures.yml` so writing tools see the same numbers as the figures. |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | Manuscript revision, claim-evidence audit, banned-word / humanize pass, figure-text consistency, journal-format check. |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | Long-form rewrites, bilingual or CJK drafts, second-opinion review on prose. |

**Lives in:** `research-hub` (paper-memory-builder) · standalone `academic-writing-skills` · standalone `gemini-delegate-skill`.

### 8. Submit, respond to reviewers, wrap up

> *"Are my claims defensible? Is the reviewer response complete? Is the
> project state preserved for the next person — or for future me?"*

Tools: **journal portal · your repo.**

| Skill | What it does |
|---|---|
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | Reviewer response tables, pre-submission checklist, journal-format audit, rebuttal letter. |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Freeze the project's final state into `.research/` manifests so future AI sessions (or future you) can resume in seconds. |

**Lives in:** standalone `academic-writing-skills` · `research-hub`.

## All Skills in This Catalog

The full set of skills referenced above, grouped by their canonical repo.
Eleven skills total — every one of them appears in at least one stage of
the pipeline.

**From [`research-hub`](https://github.com/WenyuChiou/research-hub) (7 skills):**

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) — search, ingest, organise papers across Zotero / Obsidian / NotebookLM. *(Stages 1, 2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) — comparison matrix across method, data, claim, limitation. *(Stage 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) — verify NotebookLM briefs against source bundles. *(Stage 2)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) — `.research/` manifests so future AI sessions skip the rescan. *(Stages 3, 5, 8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) — fast orientation memo from those manifests. *(Stages 3, 5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) — split work across Claude / Codex / Gemini, plan handoffs. *(Stage 5)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) — `.paper/claims.yml` and `.paper/figures.yml` for manuscript work. *(Stage 7)*

**Standalone repos (4 skills):**

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) — manuscript revision, claim-evidence audit, banned-word / humanize, journal format, reviewer response. *(Stages 7, 8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) — deep Zotero CRUD, batch metadata, library maintenance. *(Stage 1)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) — Claude → Codex CLI handoff for code-heavy work. *(Stages 4, 5, 6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) — Claude → Gemini CLI handoff for long-context, multilingual, or CJK work. *(Stages 4, 6, 7)*

Stages with no native skill yet: **(4) model design** and **(6) visualization**
— the closest fits today are `codex-delegate` and `gemini-delegate`.
Contributions for either gap are welcome.

## Quick Reference — By Tool Combination

If you already know your stack, use this lookup instead of the pipeline.

| If you want to... | Use this skill | Install |
|---|---|---|
| Connect Zotero, Obsidian, and/or NotebookLM | [`research-hub`](https://github.com/WenyuChiou/research-hub) | `pip install research-hub-pipeline` then `research-hub install --platform claude-code` |
| Compare papers in a literature review | [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | via `research-hub install` |
| Verify a NotebookLM brief | [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | via `research-hub install` |
| Prepare a manuscript for AI writing | [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) + [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | install `research-hub` and clone `academic-writing-skills` |
| Revise a paper or respond to reviewers | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | `git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills` |
| Clean or edit a Zotero library | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | `git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills` |
| Delegate coding-heavy work | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | `git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate` |
| Delegate long-context or bilingual work | [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill) | `git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill` |

For the researcher-facing checklist, see
[docs/researcher-workflow-checklist.md](docs/researcher-workflow-checklist.md).
Full directory: [docs/skill-directory.md](docs/skill-directory.md).
Machine-readable catalog: [catalog/skills.yml](catalog/skills.yml).

## Skill Families & Boundary Rules

| Family | Canonical repo | Owns |
|---|---|---|
| Research workspace | [`research-hub`](https://github.com/WenyuChiou/research-hub) | Zotero / Obsidian / NotebookLM workflow, `.research/` and `.paper/` handoff files. |
| Academic writing | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | Manuscript revision, claim-evidence audit, reviewer response, figure-text consistency, journal compliance. |
| Zotero operations | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | Deep Zotero CRUD, batch metadata, library maintenance. |
| Codex delegation | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | Claude → Codex CLI handoff for code-heavy work. |
| Gemini delegation | [`gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill) | Claude → Gemini CLI handoff for long-context, multilingual, or CJK work. |

Domain-specific simulation governance, model coupling, and audit traces
belong in the relevant model repository, not here.

## Recommended Install Order

1. Install `research-hub` if you use any two of Zotero, Obsidian, NotebookLM.
2. Install `academic-writing-skills` if you write or revise papers with AI.
3. Add `zotero-skills` if you need deep Zotero library operations.
4. Add `codex-delegate` and `gemini-delegate-skill` if you use multiple AI CLIs.

Commands: [docs/install.md](docs/install.md).

## Status

The catalog is intentionally lightweight. It points to tested canonical
repos rather than becoming a monorepo.

Currently verified:

- `research-hub`: targeted skill tests passing.
- `academic-writing-skills`: integrity tests passing.

## License

MIT
