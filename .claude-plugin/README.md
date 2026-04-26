# Claude Code Plugin Marketplace

This directory makes the [`ai-research-skills`](https://github.com/WenyuChiou/ai-research-skills)
catalog installable as a Claude Code plugin marketplace.

## Quick install

```text
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin marketplace list
claude plugin install research-workspace@ai-research-skills
claude plugin list
```

Expected checks:

- `claude plugin marketplace list` should include `ai-research-skills`.
- `claude plugin list` should include `research-workspace@ai-research-skills`.

For shell-level diagnostics, use:

```powershell
claude plugin list --available --json
```

Do not use `/plugin marketplace info ai-research-skills` as a
verification step on Claude Code 2.1.119; `marketplace info` is not a
supported marketplace subcommand in that version.

Also prefer the terminal `claude plugin install ...` command over the
interactive `/plugin install` UI on Claude Code 2.1.119. The
interactive path can try SSH (`git@github.com`) for GitHub sources and
fail on machines without a configured GitHub SSH key.

## Plugins shipped

The marketplace ships **5 plugins** — one bundle (`research-workspace`)
that auto-discovers 9 skills from a `skills/<name>/SKILL.md` layout,
plus 4 standalone single-skill plugins whose SKILL.md sits at the repo
root and is exposed via a `.claude-plugin/plugin.json` declaring
`"skills": ["./"]`.

| Plugin | Source repo | Skills it ships |
|---|---|---|
| `research-workspace` | `WenyuChiou/research-hub` | 9 skills auto-discovered from `skills/<name>/SKILL.md`: research-hub, literature-triage-matrix, notebooklm-brief-verifier, zotero-library-curator, research-design-helper, research-context-compressor, research-project-orienter, research-hub-multi-ai, paper-memory-builder |
| `academic-writing-skills` | `WenyuChiou/academic-writing-skills` | Single skill: manuscript revision, banned-word audit, claim-evidence check, journal format, reviewer response |
| `zotero-skills` | `WenyuChiou/zotero-skills` | Single skill: full Zotero CRUD (local + Web API) |
| `codex-delegate` | `WenyuChiou/codex-delegate` | Single skill: hand token-heavy mechanical work to Codex CLI |
| `gemini-delegate` | `WenyuChiou/gemini-delegate-skill` | Single skill: hand long-context / CJK output to Gemini CLI |

### What each plugin gets you out of the box

- **`research-workspace`** — 5 of its 9 skills work fully without any
  extra setup (`literature-triage-matrix`, `research-design-helper`,
  `research-context-compressor`, `research-project-orienter`,
  `paper-memory-builder`). 1 works in fallback mode
  (`notebooklm-brief-verifier`). 3 are CLI wrappers and need
  `pip install research-hub-pipeline` to actually run; without it they
  print a setup hint instead of hallucinating output.
- **`academic-writing-skills`** — works fully on its own.
- **`zotero-skills`** + **`zotero-library-curator`** (in
  `research-workspace`) — need Zotero connectivity (local API on port
  23119, or Web API key).
- **`codex-delegate`** / **`gemini-delegate`** — need their respective
  CLI binaries installed; see each source repo's README.

## Marketplace install vs. `pip install research-hub-pipeline`

| You want… | Use this path |
|---|---|
| Just the SKILL.md instructions (skills auto-trigger inside Claude Code) | `claude plugin marketplace add` above — lighter, no Python env |
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
