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

### What you can use after each step

Pick the rows you need. Each row is **additive** — you can stop at
any row and use what you've installed.

| Step | Command | What you can use after this step |
|---|---|---|
| **1. Marketplace plugin** *(start here)* | `claude plugin marketplace add WenyuChiou/ai-research-skills`<br>`claude plugin marketplace list`<br>`claude plugin install research-workspace@ai-research-skills --scope user`<br>`claude plugin list` | **5 skills ready immediately** (Claude reasoning + file writes only): `literature-triage-matrix`, `research-design-helper`, `research-context-compressor`, `research-project-orienter`, `paper-memory-builder`. **+ 1 in fallback mode**: `notebooklm-brief-verifier` (your downloaded brief + plain source list — [verified](test-corpus/manual-fallback-fresh-user/brief-verify-manual-fallback.md)). |
| **2. + Manuscript work** | `git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills` | **+ 1 skill**: `academic-writing-skills` (banned-word audit, claim-evidence check, journal format, reviewer response). |
| **3. + Zotero** | Set up Zotero local API or Web key, then:<br>`git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills` | **+ 2 skills**: `zotero-skills` (full CRUD), `zotero-library-curator` (audit + cleanup proposals). |
| **4. + Multi-CLI delegation** | Install Codex / Gemini CLI binaries, then:<br>`git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate`<br>`git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill` | **+ 2 skills**: `codex-delegate` (token-heavy code work), `gemini-delegate` (long-context, CJK output). |
| **5. + Literature pipeline automation** | `pip install research-hub-pipeline`<br>`research-hub setup --persona researcher`<br>*(persona = `researcher` &#124; `analyst` &#124; `humanities` &#124; `internal`)* | **+ 2 skills**: `research-hub` (paper search, ingest, NotebookLM upload), `research-hub-multi-ai` (delegation orchestration). Step 5 also re-installs steps 1-2's skills if you skipped them. |

After step 1 alone, **6 of 13 skills are useful right away** (5 fully
+ 1 fallback). Steps 2-5 are additions you make only when you hit
that need. Skills that need a CLI / service print a setup hint
instead of failing silently.

### Notes

- Run the step 1 commands from your terminal, not from inside the
  interactive `/plugin` UI. On Claude Code 2.1.119, the interactive
  `/plugin install` path can try SSH (`git@github.com`) and fail if no
  SSH key is configured; the terminal `claude plugin install ...`
  command uses the supported CLI path and has been verified.
- Verify step 1 with `claude plugin marketplace list` first, then
  `claude plugin list`. The marketplace list should include
  `ai-research-skills`; the plugin list should include
  `research-workspace@ai-research-skills`.
- For shell-level diagnostics, use
  `claude plugin list --available --json`.
- Do not use `/plugin marketplace info ai-research-skills` as a
  verification step on Claude Code 2.1.119; `marketplace info` is not a
  supported marketplace subcommand in that version.
- Step 1 ships SKILL.md only — no Python env. Step 5 adds the
  `research-hub` Python CLI on top.
- The 4 standalone repos (steps 2-4) currently install via `git
  clone` rather than the marketplace because their `SKILL.md` lives
  at the repo root; this is a Claude Code marketplace schema
  limitation, tracked at
  [.claude-plugin/README.md](.claude-plugin/README.md).
- Full install detail (troubleshooting, upgrade notes, persona
  comparison): [docs/install.md](docs/install.md).

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
