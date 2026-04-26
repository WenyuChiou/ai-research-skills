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
engineers, librarians, and research support staff who run real research
projects with AI in the loop.

## Who This Is For

Use this collection if you want AI help with any of these:

- finding and organising papers across Zotero, Obsidian, and NotebookLM,
- comparing literature without rereading every PDF,
- compressing project context so future AI sessions are cheap,
- building, running, and validating models or experiments,
- preparing manuscripts, responding to reviewers, and submitting,
- delegating coding or long-context work to Codex or Gemini.

You do not need every tool. Any two of these pairings already unlocks
most of the workflow:

```text
Zotero + Obsidian
Obsidian + NotebookLM
Zotero + NotebookLM
```

## Research Pipeline — Pick Your Stage

AI skills are most useful when matched to the stage you are in. Find your
stage below, install the matching skill, and stop asking AI to reread your
project from scratch each time.

```text
1. Discover lit  →  2. Organise & compare  →  3a. Frame  →  3b. Plan
        →  4. Build model  →  5. Run & validate (C&V)  →  6. Visualise
        →  7. Draft manuscript  →  8. Submit, respond, wrap up
```

> Most skills below live in [`research-hub`](https://github.com/WenyuChiou/research-hub)
> or [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills).
> The "Lives in" line on each stage tells you which repo to clone.

## Cross-cutting Tools — Used at Every Stage

Three skills don't belong to a specific stage — they're triggered by *task
character*, not pipeline position:

| Skill | Trigger | What it does |
|---|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | Token-heavy mechanical work | Hand batch edits, scaffolding, refactors, test generation, plotting scripts to Codex CLI. Claude reviews; Codex types. |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | Long-context reading or 繁中 / CJK output | Hand long-PDF synthesis, bilingual rewrites, second-opinion review to Gemini CLI. |
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | "Who should do this?" | Stage-agnostic, character-driven routing — produces a delegation plan + handoff prompts. |

Use them at *any* stage. The stage tables below focus on stage-specific
skills and reference these three by name where they apply.

**Lives in:** standalone `codex-delegate` / `gemini-delegate-skill` ·
`research-hub` (multi-ai router).

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
| [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) *(optional)* | Audit Zotero before comparison — find duplicate DOIs, orphan items, propose tag/collection cleanup. Read-only. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) *(optional)* | Apply the cleanup the curator proposes — full CRUD on Zotero items. |

**Lives in:** `research-hub` (matrix, verifier, hub, curator) · standalone `zotero-skills`.

### 3a. Frame the problem (you do this)

> *"Is my research question sharp enough to be falsifiable?"*

AI doesn't replace this work — sharpening a vague interest into a research
question with identifiable mechanism, validation plan, and risk register
is the irreducibly creative part of research. The skill below acts as a
**Socratic dialog partner**, not a problem-framer.

| Skill | What it does |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | Walks you through 5 segments — research question sharpening → expected mechanism → identifiability check → validation plan → risk register — and writes `.research/design_brief.md`. Does NOT invent the question; helps you articulate it. |

**Lives in:** `research-hub`.

### 3b. Plan the project (capture the artifacts)

> *"What am I claiming, with what data, and what's my plan?"*

Once Stage 3a has shaped the question, these skills capture the plan as
machine-readable manifests so future AI sessions don't reread the whole repo.

| Skill | What it does |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Write `.research/project_manifest.yml`, `.research/experiment_matrix.yml`, `.research/data_dictionary.yml` so future AI sessions skip the rescan. Picks up `design_brief.md` from 3a if present. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Read those manifests and produce a fast orientation memo when you (or a new AI session) come back to the project. |

**Lives in:** `research-hub`.

### 4. Design and build the model

> *"What architecture, equations, agents, or prompts do I need?"*

Tools: **your repo + IDE.**

The creative part — choosing model class, parameters, identifiability
strategy — stays human. AI helps by reading back the `design_brief.md`
produced in Stage 3a and generating implementation scaffolding.

| Skill | What it does |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | Same skill as 3a — re-read `.research/design_brief.md` here when you're ready to translate "what to model" into "how to model". |

For implementation scaffolding (test harness, plotting, batch edits) and
design review by long-context reading, use the **Cross-cutting tools**
(`codex-delegate`, `gemini-delegate`) above.

**Lives in:** `research-hub`.

### 5. Run experiments, calibrate, and validate (C&V)

> *"Is the run reproducible, checkable, extensible? Can I save tokens
> across long sessions?"*

Tools: **your repo + multi-AI CLIs.**

| Skill | What it does |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Token-saving manifests so each new run-and-check session does not start from zero. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Cheap re-onboarding when you switch between experiments or come back days later. |

For repeatable sweeps, regression tests, and post-fix verification,
delegate token-heavy runs via the **Cross-cutting tools**
(`codex-delegate` for code-heavy work; `research-hub-multi-ai` to plan
the routing across Claude / Codex / Gemini).

**Lives in:** `research-hub`.

### 6. Visualise and interpret results

> *"What does the figure actually show? Does my caption match?"*

Tools: **matplotlib / plotly / your plotting stack of choice.**

No native skill yet. Visualisation work is typically direct interaction
with your plotting stack. When the work is mechanical (consistent style
across N figures, batch re-renders) or interpretive (caption /
narrative pairing for a figure), delegate via the **Cross-cutting
tools** above — `codex-delegate` for plotting scripts;
`gemini-delegate` for figure-caption pairing using long context.

### 7. Draft and revise the manuscript

> *"Does the prose match the figure? Does it fit the target journal? Does
> it sound human?"*

Tools: **Word · LaTeX · Markdown.**

| Skill | What it does |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | Extract `.paper/claims.yml` and `.paper/figures.yml` so writing tools see the same numbers as the figures. |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | Manuscript revision, claim-evidence audit, banned-word / humanize pass, figure-text consistency, journal-format check. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) *(optional)* | Deep-edit bibliography entries — fix citation metadata, add missing fields, attach PDFs — when the writing skill flags references that need cleanup. |

For long-form bilingual rewrites or 繁中 / CJK drafts, use the
**Cross-cutting tool** `gemini-delegate` above.

**Lives in:** `research-hub` (paper-memory-builder) · standalone `academic-writing-skills` · standalone `zotero-skills`.

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
**Thirteen skills total** — every one of them appears either in at least
one pipeline stage or in the Cross-cutting tools section above.

**From [`research-hub`](https://github.com/WenyuChiou/research-hub) (9 skills):**

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) — search, ingest, organise papers across Zotero / Obsidian / NotebookLM. *(Stages 1, 2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) — comparison matrix across method, data, claim, limitation. *(Stage 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) — verify NotebookLM briefs against source bundles. *(Stage 2)*
- [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) — audit Zotero library, find duplicates / orphans, propose cleanup (preview only). *(Stage 2)*
- [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) — Socratic dialog through research question → mechanism → identifiability → validation → risk. Writes `.research/design_brief.md`. *(Stages 3a, 4)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) — `.research/` manifests so future AI sessions skip the rescan. *(Stages 3b, 5, 8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) — fast orientation memo from those manifests. *(Stages 3b, 5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) — stage-agnostic, character-driven routing across Claude / Codex / Gemini. *(Cross-cutting)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) — `.paper/claims.yml` and `.paper/figures.yml` for manuscript work. *(Stage 7)*

**Standalone repos (4 skills):**

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) — manuscript revision, claim-evidence audit, banned-word / humanize, journal format, reviewer response. *(Stages 7, 8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) — full Zotero CRUD, batch metadata, library maintenance. *(Stages 1, 2, 7 — the apply layer beneath `zotero-library-curator`)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) — Claude → Codex CLI handoff for code-heavy work. *(Cross-cutting)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) — Claude → Gemini CLI handoff for long-context, multilingual, or CJK work. *(Cross-cutting)*

Stage with no native skill yet: **(6) visualisation** — the closest fits
are the cross-cutting `codex-delegate` (plotting scripts) and
`gemini-delegate` (figure-caption pairing). Contributions welcome.

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
