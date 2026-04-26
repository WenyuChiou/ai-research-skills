# Claude Code Plugin Marketplace

This directory makes the [`ai-research-skills`](https://github.com/WenyuChiou/ai-research-skills)
catalog installable as a Claude Code plugin marketplace.

## Quick install

```text
/plugin marketplace add WenyuChiou/ai-research-skills
/plugin install research-workspace@ai-research-skills
/plugin list
```

Use `/plugin marketplace list` to confirm the marketplace is configured.
On Claude Code 2.1.119, `/plugin marketplace info ai-research-skills`
can return `(no content)` even when the marketplace validates and plugins
install correctly; treat install/list as the supported verification path.

## Plugin shipped

Currently the marketplace ships **one plugin** that installs cleanly
under Claude Code's auto-discovery rules:

| Plugin | Source repo | Skills bundled |
|---|---|---|
| `research-workspace` | `WenyuChiou/research-hub` | 9 skills auto-discovered from `skills/<name>/SKILL.md` (research-hub, literature-triage-matrix, notebooklm-brief-verifier, zotero-library-curator, research-design-helper, research-context-compressor, research-project-orienter, research-hub-multi-ai, paper-memory-builder) |

### Coverage of those 9 skills without the Python CLI

The marketplace install ships only the SKILL.md instruction files.
Python CLI commands (`research-hub auto`, `research-hub search`,
NotebookLM browser automation) come from
`pip install research-hub-pipeline`, **not** from the marketplace.

| Without the CLI | Coverage |
|---|---|
| `literature-triage-matrix`, `research-design-helper`, `research-context-compressor`, `research-project-orienter`, `paper-memory-builder` | **Full** — pure Claude reasoning + writes markdown / YAML files |
| `notebooklm-brief-verifier` | **Manual fallback** works (your downloaded brief + a plain source list); CLI-managed mode (auto-fetched source bundle) needs the CLI |
| `zotero-library-curator` | **Read-only audit / proposal** works; applying cleanup is delegated to `zotero-skills` (Zotero local API), independent of the research-hub CLI |
| `research-hub`, `research-hub-multi-ai` | **Describes the workflow but cannot execute** — these skills are wrappers around the CLI |

If you only want the lightweight "help me think about this" cases
(compare papers, sharpen a research question, write a project
manifest, build paper memory), the marketplace install alone is
enough. If you want literature pipeline automation, NotebookLM upload,
or multi-AI orchestration, install `pip install research-hub-pipeline`
on top — see [docs/install.md](../docs/install.md) Path B.

When a CLI-required skill is invoked without the CLI present, the
skill prints a `pip install research-hub-pipeline` hint instead of
silently failing.

## Why only one plugin?

The catalog also references 4 **standalone** skill repos
(`academic-writing-skills`, `zotero-skills`, `codex-delegate`,
`gemini-delegate-skill`). Each of those repos keeps its `SKILL.md` at
the repo root, not under `skills/<name>/`. The marketplace plugin
schema's documented workaround for that layout —
`"skills": ["./"]` — is currently rejected by Claude Code's parser
when paired with a `github` source. As a result, those 4 plugins are
**not** in the marketplace yet; the catalog README directs users to
install them via `git clone` (Path B) until the upstream issue is
resolved.

Two ways the 4 standalone plugins could ship via this marketplace
later:

1. **Add `plugin.json`** declaring `{"skills": ["./"]}` to each of the
   4 source repos. Claude Code would then read that manifest after
   cloning and find SKILL.md correctly.
2. **Upstream fix in Claude Code** so `"skills": ["./"]` is accepted
   for `github`-source plugins (matches the documented spec).

Tracked as a follow-up; this marketplace will grow back to 5 plugins
once one of those paths lands.

## Marketplace install vs. `pip install research-hub-pipeline`

| You want… | Use this path |
|---|---|
| Just the SKILL.md instructions (skills auto-trigger inside Claude Code) | `/plugin marketplace add` above — lighter, no Python env |
| The full research-hub workflow with CLI commands (`research-hub auto`, `research-hub search`, NotebookLM upload automation, etc.) | `pip install research-hub-pipeline` then `research-hub setup --persona <X>` (see [docs/install.md](../docs/install.md)) |

Both paths install the same 9 SKILL.md files under
`~/.claude/skills/` — the difference is whether you also get the
Python CLI.

## Schema reference

This marketplace follows the [Claude Code plugin marketplace schema](https://code.claude.com/docs/en/plugin-marketplaces).
The `research-workspace` plugin uses a remote `github` source, so
installing pulls SKILL.md files directly from
`WenyuChiou/research-hub` — no skill content lives in this catalog
repo.

## Updating the marketplace

When `WenyuChiou/research-hub` updates its skills, no change is needed
here — Claude Code refetches the latest commit on `/plugin marketplace
update` (the marketplace tracks the source repo's default branch).

To change which plugins are exposed, edit `marketplace.json`. The
repo's `tests/test_catalog.py` guards the file's basic structure
(parses, has at least one plugin, every plugin has `name` + `source`).
