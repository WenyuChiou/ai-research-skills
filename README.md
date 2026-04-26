# AI Research Skills

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

> **Researcher-led, AI-assisted.**
>
> 13 skills organized by an actual research workflow.

A researcher-facing catalog of 13 AI skills covering the full research
workflow — from finding the first paper to submitting the final
manuscript.

Languages: [English](README.md) | [繁中](README.zh-TW.md)

![13 AI skills mapped to the 8-stage research workflow, with cross-cutting tools (codex-delegate, gemini-delegate, research-hub-multi-ai) usable at every stage](docs/img/pipeline-overview.png)

**What you get:** 13 skills covering the full research workflow.
9 ship via one install (`research-hub-pipeline`); 4 are standalone
clones. Per-skill testing details:
[docs/verification.md](docs/verification.md).

**Who this is for:** graduate students, PhD researchers, postdocs,
research engineers, librarians, and research support staff who run real
research projects with AI in the loop.

---

## Install

Prerequisite: Claude Code (https://claude.ai/code).

> **How skills actually work:** each skill is a Markdown instruction
> file (`SKILL.md`) installed under `~/.claude/skills/`. AI hosts that
> support skills (Claude Code, Cursor with the Claude Code extension,
> etc.) automatically read and apply them when your request matches
> the skill's trigger description. Skills are not CLI tools or Python
> packages — they're prompt scaffolding the host loads on your behalf.

### Path A — Claude Code marketplace (one command, 9 skills)

```text
/plugin marketplace add WenyuChiou/ai-research-skills
/plugin install research-workspace@ai-research-skills
```

Verify with:

```text
/plugin marketplace list
/plugin list
```

Claude Code 2.1.119 does not expose a reliable `marketplace info`
command; `(no content)` from `/plugin marketplace info
ai-research-skills` does not mean the marketplace is empty. The
install command above is the source-of-truth check.

This installs the **9 research-hub skills** (literature search,
comparison, planning manifests, design dialog, multi-AI routing,
NotebookLM brief verification, paper-memory builder, Zotero curator).

> **Path A ships SKILL.md only — no Python CLI.** Coverage of the 9
> skills:
>
> - **5 skills work fully without the CLI** (pure Claude reasoning +
>   file writes): `literature-triage-matrix`, `research-design-helper`,
>   `research-context-compressor`, `research-project-orienter`,
>   `paper-memory-builder`.
> - **1 skill works in fallback mode**: `notebooklm-brief-verifier` —
>   the Manual fallback uses your downloaded brief + a plain source
>   list, [verified end-to-end](test-corpus/manual-fallback-fresh-user/brief-verify-manual-fallback.md)
>   to match the CLI-managed mode.
> - **3 skills need `pip install research-hub-pipeline` for full
>   function**: `research-hub` (paper search / ingest / NotebookLM
>   upload automation), `research-hub-multi-ai` (delegation
>   orchestration), `zotero-library-curator` (Zotero auth + CRUD via
>   `zotero-skills`).
>
> Each affected skill prints a `pip install research-hub-pipeline` hint
> if you call it without the CLI present, so you won't be stuck
> guessing — most users start with Path A and add the CLI from
> **Path B** below only when a skill asks.

For the 4 standalone skills (academic-writing-skills, zotero-skills,
codex-delegate, gemini-delegate), use **Path B** below — each is a
single `git clone` because the marketplace plugin spec doesn't yet
support their root-level SKILL.md layout.

### Path B — `pip install` + `git clone` (full platform with CLI)

Pick this if you want the **research-hub Python CLI** (`research-hub
auto`, `research-hub search`, NotebookLM browser automation, etc.) on
top of the SKILL.md files, **or** if you want the 4 standalone skills.

```bash
# 1. research-hub — installs 9 skills + onboards your persona in one go
pip install research-hub-pipeline
research-hub setup --persona researcher   # or: analyst | humanities | internal

# 2. academic-writing-skills — for any manuscript work
git clone https://github.com/WenyuChiou/academic-writing-skills \
  ~/.claude/skills/academic-writing-skills
```

Add as needed:

```bash
# Heavy Zotero CRUD (deeper than research-hub bundles)
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills

# Multi-CLI workflows (Claude + Codex + Gemini)
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill

# Optional NotebookLM browser automation (handled by `setup` if you
# answer yes when prompted; install separately here if you skipped it)
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

> **Path A vs Path B:** Path A is one command, ships only the 9
> research-hub SKILL.md files (no Python env). Path B adds the
> research-hub CLI plus the 4 standalone skills. Most users pick A
> first and add Path B repos later if they need them.

Full install guide: [docs/install.md](docs/install.md). Marketplace
internals: [.claude-plugin/README.md](.claude-plugin/README.md).
Upgrading from research-hub-pipeline ≤ 0.45? See the upgrade note in
the install guide.

---

## How to use

After install, skills auto-trigger inside Claude Code when your
phrasing matches a skill's description. **You don't have to remember
skill names** — describe what you want and Claude Code picks the right
skill.

### Example phrases → skills they activate

| When you say... | Skill that activates |
|---|---|
| "Compare these 5 papers by method, data, and limitations" | `literature-triage-matrix` |
| "Audit my Zotero library for duplicates and orphan tags" | `zotero-library-curator` |
| "Walk me through my research design before I start coding" | `research-design-helper` |
| "Verify this NotebookLM brief against the source bundle" | `notebooklm-brief-verifier` |
| "Build a paper memory layer from my manuscript draft" | `paper-memory-builder` |
| "Audit my paragraph for banned words and overclaim" | `academic-writing-skills` |
| "Compress this project context for future AI sessions" | `research-context-compressor` |
| "Orient me — what is this repo about?" | `research-project-orienter` |
| "This task is code-heavy — delegate to Codex" | `codex-delegate` |
| "Translate this brief into 繁中 with long context" | `gemini-delegate` |

### When skills don't auto-trigger

If Claude Code doesn't pick the right skill, name it explicitly:

> "Use `literature-triage-matrix` to compare these 5 papers."

---

## Pick Your Starting Point

If you'd rather pick a skill subset by goal instead of using everything,
match your immediate goal below.

| Your immediate goal | Skills you'll use |
|---|---|
| **Find & compare literature** | `research-hub` + `literature-triage-matrix` |
| **Write or revise a paper** | `paper-memory-builder` + `academic-writing-skills` |
| **Manage a research project / Zotero library** | `research-design-helper` + `research-context-compressor` + `zotero-library-curator` |

> **Helping others adopt AI for research** (librarian / RA / advisor)?
> No install needed — read [docs/install.md](docs/install.md) and
> [docs/verification.md](docs/verification.md) and recommend.
>
> **Don't see your goal?** The full pipeline below covers 8 stages of
> research; find your stage and the matching skill.

---

<details>
<summary><h2>Full Research Pipeline (click to expand)</h2></summary>

The 8 stages of a research project, with the skills that fit each one.
This is the comprehensive reference — most users will pick from the
persona table above and never need to read this.

```text
1. Discover lit  →  2. Organise & compare  →  3a. Frame  →  3b. Plan
        →  4. Build model  →  5. Run & validate (C&V)  →  6. Visualise
        →  7. Draft manuscript  →  8. Submit, respond, wrap up
```

Three skills don't belong to a specific stage — they're triggered by
*task character*, not pipeline position. See **Cross-cutting tools**
below.

### 1. Discover literature

> *"What has been done? What should I read?"*

Tools you probably use: **Zotero · NotebookLM · Obsidian** *(no native
OneNote skill — use Obsidian as the notes layer.)*

| Skill | What it does |
|---|---|
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | Search arXiv / Semantic Scholar / CrossRef / PubMed, ingest metadata, write paper notes into Obsidian. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) | Add, tag, deduplicate, and clean Zotero items beyond the research-hub pipeline. |

### 2. Organise & compare literature, find the gap

> *"Where is the research gap? Which 5 papers actually matter?"*

| Skill | What it does |
|---|---|
| [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | Compare papers by method, data, claim, limitation, and relevance — without rereading every PDF. |
| [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | Verify a NotebookLM brief against the source bundle. Catches missed sources, unsupported claims, and contradictions. |
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | Build the Obsidian cluster and the NotebookLM source bundle that feed the matrix. |
| [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) *(optional)* | Audit Zotero before comparison — find duplicate DOIs, orphan items, propose tag/collection cleanup. Read-only. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) *(optional)* | Apply the cleanup the curator proposes — full CRUD on Zotero items. |

### 3a. Frame the problem

> *"Is my research question sharp enough to be falsifiable?"*

A Socratic dialog partner that asks structured questions to surface
what you'd otherwise leave implicit.

| Skill | What it does |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | Walks you through 5 segments — research question → expected mechanism → identifiability check → validation plan → risk register — and writes `.research/design_brief.md`. |

### 3b. Plan the project (capture the artifacts)

> *"What am I claiming, with what data, and what's my plan?"*

Once 3a has shaped the question, these skills capture the plan as
machine-readable manifests so future AI sessions don't reread the whole
repo.

| Skill | What it does |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Write `.research/project_manifest.yml`, `experiment_matrix.yml`, `data_dictionary.yml`. Picks up `design_brief.md` from 3a if present. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Read those manifests and produce a fast orientation memo when you (or a new AI session) come back to the project. |

### 4. Design and build the model

> *"What architecture, equations, agents, or prompts do I need?"*

Re-read the `design_brief.md` produced in Stage 3a as your model spec,
then generate implementation scaffolding.

| Skill | What it does |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | Same skill as 3a — re-read `.research/design_brief.md` here when translating "what to model" into "how to model". |

For implementation scaffolding (test harness, plotting, batch edits)
and design review by long-context reading, use the **Cross-cutting
tools** (`codex-delegate`, `gemini-delegate`) below.

### 5. Run experiments, calibrate, and validate (C&V)

> *"Is the run reproducible, checkable, extensible? Can I save tokens
> across long sessions?"*

| Skill | What it does |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Token-saving manifests so each run-and-check session doesn't start from zero. |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | Cheap re-onboarding when you switch experiments or come back days later. |

For repeatable sweeps and post-fix verification, delegate via the
**Cross-cutting tools** below.

### 6. Visualise and interpret results

> *"What does the figure actually show? Does my caption match?"*

Tools: **matplotlib / plotly / your plotting stack of choice.**

| Skill | What it does |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | Generate or refactor plotting scripts (consistent style across N figures, batch re-renders). |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | Pair a figure with a draft caption / interpretation paragraph using long-context reading. |

### 7. Draft and revise the manuscript

> *"Does the prose match the figure? Does it fit the target journal?
> Does it sound human?"*

| Skill | What it does |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | Extract `.paper/claims.yml` and `.paper/figures.yml` so writing tools see the same numbers as the figures. |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | Manuscript revision, claim-evidence audit, banned-word / humanize pass, figure-text consistency, journal-format check. |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) *(optional)* | Deep-edit bibliography entries when the writing skill flags references that need cleanup. |

For long-form bilingual rewrites or 繁中 / CJK drafts, use the
**Cross-cutting tool** `gemini-delegate` below.

### 8. Submit, respond to reviewers, wrap up

> *"Are my claims defensible? Is the reviewer response complete? Is the
> project state preserved for future me?"*

| Skill | What it does |
|---|---|
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | Reviewer response tables, pre-submission checklist, journal-format audit, rebuttal letter. |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | Freeze the project's final state so future AI sessions (or future you) can resume in seconds. |

</details>

---

## Cross-cutting Tools — Used at Every Stage

Three skills don't belong to a specific stage — they're triggered by
*task character*:

| Skill | Trigger | What it does |
|---|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | Token-heavy mechanical work | Hand batch edits, scaffolding, refactors, test generation, plotting scripts to Codex CLI. |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | Long-context reading or 繁中 / CJK output | Hand long-PDF synthesis, bilingual rewrites, second-opinion review to Gemini CLI. |
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | "Who should do this?" | Stage-agnostic, character-driven routing — produces a delegation plan + handoff prompts. |

---

## All 13 Skills

<details>
<summary><b>From <code>research-hub</code> (9 skills)</b> — one install gets all of them</summary>

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) — search, ingest, organise papers across Zotero / Obsidian / NotebookLM. *(Stages 1, 2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) — comparison matrix across method, data, claim, limitation. *(Stage 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) — verify NotebookLM briefs against source bundles. *(Stage 2)*
- [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) — audit Zotero, propose cleanup (preview only). *(Stage 2)*
- [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) — Socratic dialog through RQ → mechanism → identifiability → validation → risk. *(Stages 3a, 4)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) — `.research/` manifests so future AI sessions skip the rescan. *(Stages 3b, 5, 8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) — fast orientation memo from those manifests. *(Stages 3b, 5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) — stage-agnostic, character-driven routing across Claude / Codex / Gemini. *(Cross-cutting)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) — `.paper/claims.yml` and `.paper/figures.yml` for manuscript work. *(Stage 7)*

</details>

<details>
<summary><b>Standalone repos (4 skills)</b> — git clone individually</summary>

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) — manuscript revision, claim-evidence audit, banned-word / humanize, journal format, reviewer response. *(Stages 7, 8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) — full Zotero CRUD, batch metadata, library maintenance. *(Stages 1, 2, 7)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) — Claude → Codex CLI handoff for code-heavy work. *(Cross-cutting, also Stage 6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) — Claude → Gemini CLI handoff for long-context, multilingual, or CJK work. *(Cross-cutting, also Stages 6, 7)*

</details>

### Standalone use notes

**All 13 skills are usable directly after install** — no skill depends
on another skill, and none require a research-hub workspace beyond
what `research-hub setup --persona <X>` configures for you.

The 1 skill below has a *workflow chain* worth knowing — not a
dependency, just an order:

- **`research-project-orienter`** — reads `.research/` manifests for
  speed. If none exist yet, the skill falls back to scanning
  `README.md` + `docs/` (slower); for repeat orientation, run
  `research-context-compressor` first to produce the manifests.

The other 12 skills work **directly** with their natural inputs:

- 5 need only Claude Code + your own files: `research-design-helper`,
  `research-hub-multi-ai`, `research-context-compressor`,
  `paper-memory-builder`, `academic-writing-skills`.
- 4 need one external service you'd already have: `zotero-skills` /
  `zotero-library-curator` (Zotero local API), `codex-delegate`
  (Codex CLI binary), `gemini-delegate` (Gemini CLI binary).
- 3 work either with or without research-hub-managed inputs:
  - `literature-triage-matrix` — paste any paper list (titles + DOIs)
    in chat (per SKILL.md mode #0).
  - `notebooklm-brief-verifier` — accepts manually-downloaded brief +
    plain source list (per SKILL.md Manual fallback mode, v0.68.2).
    [Verified end-to-end](test-corpus/manual-fallback-fresh-user/brief-verify-manual-fallback.md)
    against a fresh-user setup; produces identical results to the
    research-hub-managed mode.
  - `research-hub` (knowledge-base) — pick `analyst` persona for
    Obsidian + NotebookLM only (no Zotero), or `humanities` for
    Zotero + qualitative defaults.

---

## Testing

Per-skill testing matrix and reproducible test-corpus artifacts:
[docs/verification.md](docs/verification.md).

---

## Status & License

Lightweight catalog. Each skill is maintained in its canonical repo —
this catalog is the index, not a monorepo.

License: MIT. Contributions welcome — open an issue or PR. New skill
proposals should target either `research-hub` (workflow integration)
or a standalone repo (deep, single-purpose CRUD).
