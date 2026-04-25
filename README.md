# AI Research Skills

A curated index of practical AI skills for researchers who use AI assistants
with Zotero, Obsidian, NotebookLM, manuscript drafts, and coding agents.

This repo is an umbrella catalog. It does not duplicate the skill bodies from
the source repositories. Each skill remains maintained in its canonical repo so
updates, tests, and installation instructions stay in one place.

## Who This Is For

Use this collection if you are a researcher who wants AI help with:

- organizing papers across Zotero, Obsidian, and NotebookLM,
- comparing literature without rereading every PDF,
- compressing project context for future AI sessions,
- preparing manuscripts for AI-assisted writing and reviewer response,
- delegating coding or long-context work to Codex or Gemini.

You do not need all tools. The most useful entry point is any two of:

```text
Zotero + Obsidian
Obsidian + NotebookLM
Zotero + NotebookLM
```

Using all three unlocks the full loop.

## Start Here

| If you want to... | Use this skill | Download / install |
|---|---|---|
| Connect Zotero, Obsidian, and/or NotebookLM | [`research-hub`](https://github.com/WenyuChiou/research-hub) | `pip install research-hub-pipeline` then `research-hub install --platform claude-code` |
| Compare papers in a literature review | [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | Installed through `research-hub install` |
| Verify a NotebookLM brief | [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | Installed through `research-hub install` |
| Prepare a manuscript for AI writing | [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) + [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | Install `research-hub` and clone `academic-writing-skills` |
| Revise a paper or respond to reviewers | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | `git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills` |
| Clean or edit Zotero library items | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | `git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills` |
| Delegate coding-heavy work | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | `git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate` |
| Delegate long-context or bilingual work | [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill) | `git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill` |

For a researcher-facing checklist, start with
[docs/researcher-workflow-checklist.md](docs/researcher-workflow-checklist.md).
Full directory: [docs/skill-directory.md](docs/skill-directory.md). Machine-readable catalog: [catalog/skills.yml](catalog/skills.yml).

## Skill Families

| Family | Canonical repo | Use when |
|---|---|---|
| Research workspace | [`research-hub`](https://github.com/WenyuChiou/research-hub) | You want AI to operate Zotero, Obsidian, NotebookLM, clusters, dashboards, and local research artifacts. |
| Academic writing | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | You want manuscript revision, claim-evidence audits, reviewer response, and figure-text consistency. |
| Zotero operations | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | You need deeper Zotero CRUD, collections, tags, batch metadata, or library maintenance. |
| Codex delegation | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | Claude should hand code-heavy work to Codex CLI. |
| Gemini delegation | [`gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill) | Claude should hand long-context, multilingual, or CJK-heavy work to Gemini CLI. |

## Recommended Install Order

1. Install `research-hub` if your workflow uses any two of Zotero, Obsidian,
   and NotebookLM.
2. Install `academic-writing-skills` if you write or revise papers with AI.
3. Install `zotero-skills` only if you need deep Zotero library operations.
4. Install `codex-delegate` and `gemini-delegate-skill` if you use multiple AI
   CLIs and want clean handoffs.

See [docs/install.md](docs/install.md) for commands.

## Public Skill Set

### Research workspace skills

From `research-hub`:

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md)
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md)
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md)
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md)
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md)

These skills cover literature workflow, Obsidian cluster notes, NotebookLM
brief verification, and `.research/` / `.paper/` context files.

### Academic writing skill

From [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills):

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md)

This skill covers manuscript structure, claim-evidence audits, reviewer
response, journal format checks, figure-text consistency, and pre-submission
checks.

### Zotero and delegation skills

From standalone repos:

- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md)
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md)
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md)

These are intentionally separate from `research-hub` because they solve
different layers of the workflow.

## Boundary Rules

- Put Zotero / Obsidian / NotebookLM workflow skills in `research-hub`.
- Put manuscript writing and reviewer response in `academic-writing-skills`.
- Put deep Zotero CRUD in `zotero-skills`.
- Put AI CLI delegation in `codex-delegate` and `gemini-delegate-skill`.
- Put domain-specific simulation governance, model coupling, and audit traces
  in the relevant model repository, not in this umbrella catalog.

## Suggested Article Angle

> Stop asking AI to reread your research project. Give it skills.

The practical message:

- Zotero stores references.
- Obsidian stores notes and project memory.
- NotebookLM creates source-grounded briefs.
- AI skills connect the workflow and reduce repeated context loading.

See [docs/public-post-outline.md](docs/public-post-outline.md).

## Status

This catalog is intentionally lightweight. It points to tested canonical repos
rather than becoming a monorepo.

Current verified repos:

- `research-hub`: targeted skill tests passing.
- `academic-writing-skills`: integrity tests passing.

## License

MIT
