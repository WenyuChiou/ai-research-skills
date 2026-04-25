# Repo Map

This document explains where each skill should live.

## Canonical Repos

| Repo | Owns | Should not own |
|---|---|---|
| `research-hub` | Zotero/Obsidian/NotebookLM workflows, `.research/`, workspace memory, literature matrices, NotebookLM verification | Manuscript prose editing, deep Zotero CRUD, model governance |
| `academic-writing-skills` | Manuscript writing, reviewer response, claim-evidence audit, journal compliance, figure-text consistency | Zotero workflows, NotebookLM upload, coding delegation |
| `zotero-skills` | Deep Zotero item operations, tags, collections, metadata cleanup | Obsidian/NotebookLM pipeline logic |
| `codex-delegate` | Claude-to-Codex delegation for coding-heavy work | Research-domain workflow logic |
| `gemini-delegate-skill` | Claude-to-Gemini delegation for long-context or multilingual work | Research-domain workflow logic |
| Model repos | Domain-specific experiments, governance, coupling contracts, audit traces | General research workspace or writing skills |

## Why Not A Monorepo?

Duplicating skill bodies in this umbrella repo would create stale copies.
Instead:

- canonical repos own implementation and tests,
- this repo owns discovery and positioning,
- public posts link here first, then users install the specific repo they need.

## Packaging Rule

If a new skill is mainly about:

- research workspace state -> `research-hub`,
- manuscript writing -> `academic-writing-skills`,
- Zotero CRUD -> `zotero-skills`,
- AI CLI handoff -> delegation repo,
- domain simulation or coupling -> the model repo.

