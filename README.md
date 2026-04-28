# AI Research Skills

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

> 14 Claude Code skills for common research tasks — literature
> triage, research design, project context, manuscript writing, and
> multi-AI delegation.

Languages: [English](README.md) | [繁中](README.zh-TW.md)

![14 AI skills mapped to research workflow stages, with cross-cutting tools (codex-delegate, gemini-delegate, research-hub-multi-ai) usable at every stage](docs/img/pipeline-overview.png)

**What you get:** 5 plugins shipped via one Claude Code marketplace,
exposing 14 skills total. Per-skill testing details:
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
claude plugin install research-workspace@ai-research-skills
```

**You can use immediately** (pure Claude reasoning + file writes, no
external setup): `literature-triage-matrix`, `research-design-helper`,
`research-context-compressor`, `research-project-orienter`,
`paper-memory-builder`, plus `notebooklm-brief-verifier` (Manual
fallback mode). 6 of 14 skills.

> Step 1 also installs `research-hub`, `research-hub-multi-ai`, and
> the apply-cleanup half of `zotero-library-curator`. When invoked
> without the `research-hub` Python CLI on PATH they print a
> `pip install research-hub-pipeline` hint instead of fabricating
> output — see Step 5 to enable them fully.

> **Want all 5 plugins in one go?** After step 1 + steps 2-4 below,
> you can also batch them with the helper script:
>
> ```bash
> bash scripts/install-all.sh                # macOS / Linux / git-bash
> pwsh scripts/install-all.ps1               # Windows PowerShell
> ```
>
> The script does the same `claude plugin install` calls below, just
> in a loop. External prereqs (Zotero local API, Codex / Gemini CLI
> binaries) still need the manual setup described in steps 3 and 4.

### Step 2 — Manuscript work

```bash
claude plugin install academic-writing-skills@ai-research-skills
```

**+ `academic-writing-skills`** — banned-word audit, claim-evidence
check, journal format, reviewer response.

### Step 3 — Zotero

First, in Zotero desktop ([download](https://www.zotero.org/download/)):
Edit → Settings → Advanced → check **"Allow other applications on
this computer to communicate with Zotero"**. (Web API key alternative:
see [zotero-skills README](https://github.com/WenyuChiou/zotero-skills#readme).)

```bash
claude plugin install zotero-skills@ai-research-skills
```

**+ `zotero-skills`** (full CRUD) and **`zotero-library-curator`**
(audit + cleanup proposals — already in step 1's bundle, this step
turns it from preview-only into "can apply changes").

### Step 4 — Multi-CLI delegation

First install the CLI binaries (instructions in upstream READMEs):
[Codex CLI](https://github.com/WenyuChiou/codex-delegate#readme) ·
[Gemini CLI](https://github.com/WenyuChiou/gemini-delegate-skill#readme).

```bash
claude plugin install codex-delegate@ai-research-skills
claude plugin install gemini-delegate@ai-research-skills
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

## Using these skills outside Claude Code

The `claude plugin install` path is Claude Code-specific. Each
SKILL.md is plain Markdown, so you can use these skills with Codex
CLI, Gemini CLI, Cursor, Windsurf, or any AI assistant that accepts
context files. You lose Claude Code's auto-trigger (the
description-matching that picks the right skill from your phrasing) —
on other hosts, point the AI at the specific `SKILL.md` you want.

### 1. Get the source

```bash
git clone https://github.com/WenyuChiou/research-hub
git clone https://github.com/WenyuChiou/academic-writing-skills
git clone https://github.com/WenyuChiou/zotero-skills
git clone https://github.com/WenyuChiou/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill
```

Each repo's SKILL.md (and its `references/`) live under
`skills/<plugin-name>/`. For research-hub that's 10 SKILL.md files;
the other 4 repos have 1 each.

### 2. Load per host

| Host | How to load SKILL.md |
|---|---|
| **Codex CLI** | `codex exec --full-auto -C /repo "$(cat path/to/SKILL.md)\n\nNow do X..."`, or write a `.ai/codex_task.md` that starts with the SKILL.md contents and references the workflow you want |
| **Gemini CLI** | Pass via `--system-prompt-file path/to/SKILL.md`, or include in project context |
| **Cursor / Windsurf** | Copy SKILL.md (or its contents) into `.cursor/rules/` or the editor's rules directory |
| **Generic API client** | Use SKILL.md as the system prompt |
| **Any other AI** | Paste the relevant section of SKILL.md into your prompt |

### 3. Notes on which skills make sense outside Claude Code

- The 5 pure-reasoning skills (`literature-triage-matrix`,
  `research-design-helper`, `research-context-compressor`,
  `research-project-orienter`, `paper-memory-builder`) work on any
  AI — they describe a workflow + output format, not a Claude-specific
  trigger.
- `academic-writing-skills` works on any AI that can read files
  (`.paper/`, journal_format.md).
- `notebooklm-brief-verifier` Manual fallback works anywhere.
- `zotero-skills` works on any AI that can call the Zotero local /
  Web API (it's mostly an API-routing reference, not a Claude
  feature).
- `codex-delegate` / `gemini-delegate` are most useful **from
  Claude** delegating outward; if you're already using Codex or
  Gemini directly, these don't add much.
- `research-hub` and `research-hub-multi-ai` need the
  `research-hub-pipeline` Python CLI on PATH regardless of which
  AI calls them.

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
| "Build a point-by-point response to these reviewer comments" | `academic-writing-skills` |
| "Audit my figure captions for figure-text consistency" | `academic-writing-skills` |
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
| **Find & compare literature** | [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) + [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) |
| **Write or revise a paper** | [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) + [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) |
| **Manage a research project / Zotero library** | [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) + [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) + [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) |

> **Helping others adopt AI for research** (librarian / RA / advisor)?
> No install needed — read [docs/install.md](docs/install.md) and
> [docs/verification.md](docs/verification.md) and recommend.
>
> **Don't see your goal?** See [docs/pipeline.md](docs/pipeline.md)
> for the full 8-stage breakdown — find your stage and the matching
> skill.
>
> **Want to see what using these skills together looks like end-to-end?**
> [docs/demo-walkthrough.md](docs/demo-walkthrough.md) walks 7 skills
> through a real 5-paper test corpus and links every artifact each
> skill produced.

---

## All 14 Skills

<details>
<summary><b>From <code>research-hub</code> (10 skills)</b> — one install gets all of them</summary>

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) — search, ingest, organise papers across Zotero / Obsidian / NotebookLM. *(Stages 1, 2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) — comparison matrix across method, data, claim, limitation. *(Stage 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) — verify NotebookLM briefs against source bundles. *(Stage 2)*
- [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) — audit Zotero, propose cleanup (preview only). *(Stage 2)*
- [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) — Socratic dialog through RQ → mechanism → identifiability → validation → risk. *(Stages 3a, 4)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) — `.research/` manifests so future AI sessions skip the rescan. *(Stages 3b, 5, 8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) — fast orientation memo from those manifests. *(Stages 3b, 5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) — stage-agnostic, character-driven routing across Claude / Codex / Gemini. *(Cross-cutting)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) — `.paper/claims.yml` and `.paper/figures.yml` for manuscript work. *(Stage 7)*
- [`paper-summarize`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-summarize/SKILL.md) — fill per-paper Key Findings / Methodology / Relevance in both Obsidian markdown and Zotero child notes after `research-hub auto`. *(Stage 2)*

</details>

<details>
<summary><b>Standalone repos (4 skills)</b> — git clone individually</summary>

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) — manuscript revision, claim-evidence audit, banned-word / humanize, journal format, reviewer response. *(Stages 7, 8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) — full Zotero CRUD, batch metadata, library maintenance. *(Stages 1, 2, 7)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) — Claude → Codex CLI handoff for code-heavy work. *(Cross-cutting, also Stage 6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) — Claude → Gemini CLI handoff for long-context, multilingual, or CJK work. *(Cross-cutting, also Stages 6, 7)*

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
