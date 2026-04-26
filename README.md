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

Skills are Markdown instruction files (`SKILL.md`) under
`~/.claude/skills/`. Claude Code reads them automatically when your
request matches a skill's trigger description.

Each step below is **additive** — stop after any step and use what
you've installed. Every code block has GitHub's copy button in the top
right.

### Step 1 — Marketplace plugin (start here)

Run in a terminal, not inside the interactive `/plugin` UI:

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills --scope user
```

**You can use:** `literature-triage-matrix`, `research-design-helper`,
`research-context-compressor`, `research-project-orienter`,
`paper-memory-builder`, plus `notebooklm-brief-verifier` (Manual
fallback mode). That's 6 of 13 skills, ready immediately.

### Step 2 — Manuscript work

```bash
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

**+ `academic-writing-skills`** — banned-word audit, claim-evidence
check, journal format, reviewer response.

### Step 3 — Zotero

First, in Zotero desktop ([download](https://www.zotero.org/download/)):
Edit → Settings → Advanced → check **"Allow other applications on
this computer to communicate with Zotero"**. (Web API key alternative:
see [zotero-skills README](https://github.com/WenyuChiou/zotero-skills#readme).)

```bash
claude plugin install zotero-skills@ai-research-skills --scope user
```

**+ `zotero-skills`** (full CRUD) and **`zotero-library-curator`**
(audit + cleanup proposals — already in step 1's bundle, this step
turns it from preview-only into "can apply changes").

### Step 4 — Multi-CLI delegation

First install the CLI binaries (instructions in upstream READMEs):
[Codex CLI](https://github.com/WenyuChiou/codex-delegate#readme) ·
[Gemini CLI](https://github.com/WenyuChiou/gemini-delegate-skill#readme).

```bash
claude plugin install codex-delegate@ai-research-skills --scope user
claude plugin install gemini-delegate@ai-research-skills --scope user
```

**+ `codex-delegate`** (hand token-heavy code to Codex CLI),
**+ `gemini-delegate`** (long-context / CJK output via Gemini CLI).

### Step 5 — Literature pipeline automation

```bash
pip install research-hub-pipeline
research-hub setup
```

`research-hub setup` runs an interactive onboarding that asks which
of Zotero / Obsidian / NotebookLM you want to wire up. No flags or
choices to memorise upfront.

**+ `research-hub`** (paper search, ingest, NotebookLM upload),
**`research-hub-multi-ai`** (delegation orchestration). Also installs
steps 1-2's skills if you skipped them.

### Verify

```bash
claude plugin list
ls ~/.claude/skills/
```

**Other notes:**

- `(no content)` from `/plugin marketplace info` is not an error —
  `info` is not a supported subcommand on Claude Code 2.1.119.
- The interactive `/plugin install` UI can fall back to SSH and fail
  without a GitHub SSH key; the terminal `claude plugin install ...`
  uses HTTPS.
- All 5 plugins (research-workspace + the 4 standalones) install via
  `claude plugin install` from this catalog's marketplace. Background
  on the marketplace schema and per-plugin coverage:
  [.claude-plugin/README.md](.claude-plugin/README.md).

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
> **Don't see your goal?** See [docs/pipeline.md](docs/pipeline.md)
> for the full 8-stage breakdown — find your stage and the matching
> skill.

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

### One workflow note

`research-project-orienter` reads `.research/` manifests if they
exist (fast), otherwise falls back to scanning `README.md` + `docs/`
(slower). For repeat orientation, run `research-context-compressor`
first to produce the manifests.

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
