# Claude Code Plugin Marketplace

This directory makes the [`ai-research-skills`](https://github.com/WenyuChiou/ai-research-skills)
catalog installable as a Claude Code plugin marketplace. Users can register
the marketplace and install plugins (skill bundles) without cloning each
canonical repo manually.

## Quick install

```text
/plugin marketplace add WenyuChiou/ai-research-skills
/plugin install <plugin-name>@ai-research-skills
```

## Plugins

5 plugins, one per canonical source repo:

| Plugin | Source repo | Skills bundled | Use when |
|---|---|---|---|
| `research-workspace` | `WenyuChiou/research-hub` | 9: research-hub, literature-triage-matrix, notebooklm-brief-verifier, zotero-library-curator, research-design-helper, research-context-compressor, research-project-orienter, research-hub-multi-ai, paper-memory-builder | Most users — full literature → planning → modelling stack |
| `academic-writing-skills` | `WenyuChiou/academic-writing-skills` | 1: manuscript revision, claim audit, reviewer response, journal format | Anyone writing or revising a paper |
| `zotero-skills` | `WenyuChiou/zotero-skills` | 1: deep Zotero CRUD, batch metadata, library maintenance | Heavy Zotero users beyond `zotero-library-curator` |
| `codex-delegate` | `WenyuChiou/codex-delegate` | 1: Claude → Codex CLI handoff for code-heavy work | Multi-CLI users with Codex installed |
| `gemini-delegate` | `WenyuChiou/gemini-delegate-skill` | 1: Claude → Gemini CLI handoff for long-context, CJK, bilingual | Multi-CLI users with Gemini installed |

## Marketplace install vs. `pip install research-hub-pipeline`

Two install paths, for different needs:

| You want… | Use this path |
|---|---|
| Just the SKILL.md instructions (skills auto-trigger inside Claude Code) | **`/plugin marketplace add`** above — lighter, no Python env |
| The full research-hub workflow with CLI commands (`research-hub auto`, `research-hub search`, NotebookLM upload automation, etc.) | `pip install research-hub-pipeline` then `research-hub setup --persona <X>` (see [docs/install.md](../docs/install.md)) |

**The two paths are not mutually exclusive.** If you already ran
`research-hub setup`, the skills are already on disk and the marketplace
install would add the same content from a different source. Most users
pick one or the other based on whether they want the Python CLI.

## Schema reference

This marketplace follows the [Claude Code plugin marketplace schema](https://code.claude.com/docs/en/plugin-marketplaces).
Each plugin uses a remote `github` source, so installing pulls SKILL.md
files directly from each canonical repo (not from this catalog repo).

## Updating the marketplace

When a canonical source repo updates its skills, no change is needed
here — Claude Code refetches the latest commit on `/plugin marketplace
update` (the marketplace tracks each repo's `main` / `master` branch by
default).

To change which plugins or sources are exposed, edit
`marketplace.json`. The repo's `tests/test_catalog.py` guards the file's
basic structure (parses, ≥ 1 plugin, every plugin has `name` + `source`).
