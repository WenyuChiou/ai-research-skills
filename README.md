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

## Skill Families

| Family | Canonical repo | Use when |
|---|---|---|
| Research workspace | `research-hub` | You want AI to operate Zotero, Obsidian, NotebookLM, clusters, dashboards, and local research artifacts. |
| Academic writing | `academic-writing-skills` | You want manuscript revision, claim-evidence audits, reviewer response, and figure-text consistency. |
| Zotero operations | `zotero-skills` | You need deeper Zotero CRUD, collections, tags, batch metadata, or library maintenance. |
| Codex delegation | `codex-delegate` | Claude should hand code-heavy work to Codex CLI. |
| Gemini delegation | `gemini-delegate-skill` | Claude should hand long-context, multilingual, or CJK-heavy work to Gemini CLI. |

Full machine-readable catalog: [catalog/skills.yml](catalog/skills.yml).

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

- `knowledge-base`
- `research-hub-multi-ai`
- `research-context-compressor`
- `research-project-orienter`
- `literature-triage-matrix`
- `paper-memory-builder`
- `notebooklm-brief-verifier`

These skills cover literature workflow, Obsidian cluster notes, NotebookLM
brief verification, and `.research/` / `.paper/` context files.

### Academic writing skill

From `academic-writing-skills`:

- `academic-writing-skills`

This skill covers manuscript structure, claim-evidence audits, reviewer
response, journal format checks, figure-text consistency, and pre-submission
checks.

### Zotero and delegation skills

From standalone repos:

- `zotero-skills`
- `codex-delegate`
- `gemini-delegate-skill`

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

