# Contributing

This is the public catalog index for `ai-research-skills`. Skills
themselves live in 5 upstream repos. The split affects how you
contribute, depending on what you want to change.

## Where the change belongs

| Change | Where to PR |
|---|---|
| SKILL.md content (descriptions, references, examples, prerequisite checks) | The upstream skill source repo |
| `references/<skill>/*.md` reference files | The upstream skill source repo |
| Catalog README, install table, persona table, pipeline doc | This repo (`ai-research-skills`) |
| Skill metadata (name, purpose, use_when, outputs, verification status) | `catalog/skills.yml` in this repo |
| Marketplace config (plugin entries, refs, source URLs) | `.claude-plugin/marketplace.json` in this repo |

Upstream source repos:

- [`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub) — 9 skills (research-workspace plugin)
- [`WenyuChiou/academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) — manuscript writing
- [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) — Zotero CRUD
- [`WenyuChiou/codex-delegate`](https://github.com/WenyuChiou/codex-delegate) — Codex CLI handoff
- [`WenyuChiou/gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill) — Gemini CLI handoff

## Interop rules — read before renaming anything

The catalog and the upstream repos share a thin contract: marketplace
auto-discovery expects `skills/<plugin-name>/SKILL.md`, and several
skills compose by reading each other's output files (`.research/*.yml`,
`.paper/*.yml`). Renames break that contract silently if not
coordinated.

### 1. Source directory renames need a coord issue first

If you want to rename a skill's source directory (e.g. `skills/foo/` →
`skills/bar/`), open an issue in **this repo** describing the rename,
the upstream PR, and the catalog files that must update in lockstep.
Don't merge the upstream rename until the catalog PR is ready.

The marketplace's auto-discovery is path-sensitive. A silent upstream
rename will:
- Break `claude plugin install <plugin>@ai-research-skills` for new
  users (the marketplace still expects the old path).
- 404 every link to `skill_url` in `catalog/skills.yml` and the 6 docs
  that reference SKILL.md URLs (README.md, README.zh-TW.md,
  docs/pipeline.md, docs/pipeline.zh-TW.md,
  docs/researcher-workflow-checklist.md, docs/skill-directory.md).
- Strand any cross-skill artifact contract that hardcodes the rename
  in references (e.g. `paper-memory-builder` writes
  `.paper/claims.yml`; `academic-writing-skills` reads it — both need
  to agree on the path).

### 2. Skill output contract changes need a coord issue too

These cross-skill artifact paths are part of the contract:

| Producer | Path | Consumer |
|---|---|---|
| `research-design-helper` | `.research/design_brief.md` | `research-context-compressor` |
| `research-context-compressor` | `.research/project_manifest.yml`, `experiment_matrix.yml`, `data_dictionary.yml` | `research-project-orienter` |
| `paper-memory-builder` | `.paper/claims.yml`, `.paper/figures.yml` | `academic-writing-skills` |

If you change a producer's output schema or path, update the
consumer's SKILL.md in the same coordination round. Tests in this
repo don't currently catch artifact-contract breakage; manual review
is the only gate.

### 3. Plugin name in marketplace ↔ source repo plugin.json must match

`.claude-plugin/marketplace.json` references each plugin by name
(e.g. `gemini-delegate`). The upstream
`<repo>/.claude-plugin/plugin.json` must declare the same `name`.
A mismatch causes `claude plugin install` to fail at validation.

The plugin name is **not** required to match the repo name. Example:
the repo `gemini-delegate-skill` ships a plugin named `gemini-delegate`.

### 4. Default branch ↔ marketplace.json `ref` must match

If you change a source repo's default branch (e.g. `master` →
`main`), update the corresponding `source.ref` in
`.claude-plugin/marketplace.json` here.

## Local development

```bash
git clone https://github.com/WenyuChiou/ai-research-skills
cd ai-research-skills
python -m pytest tests/ -q   # 11 tests, < 1s
```

Tests guard:
- Catalog YAML structure (required families, fields, URLs).
- README phrase invariants (Zotero/Obsidian/NotebookLM mentioned;
  persona starting points present; bilingual parity).
- Marketplace JSON structure (5 plugins, expected names, source
  fields).
- `research-hub setup` documented as the canonical install command.
- 13 skills total with the documented verification status counts
  (12 pass + 1 caveat).

What tests do **not** guard (manual review needed):
- Upstream SKILL.md URLs being live (network test would be flaky).
- Upstream `skills/<plugin>/SKILL.md` paths actually existing.
- Cross-skill artifact contract (e.g. `.paper/claims.yml` schema).

## Adding a new skill

1. Add the skill to its upstream repo at `skills/<name>/SKILL.md`.
   For a new repo, also add `.claude-plugin/plugin.json`.
2. PR this repo:
   - Add the skill to `catalog/skills.yml` (under the right family).
   - If it's a new plugin (new source repo), add it to
     `.claude-plugin/marketplace.json`.
   - Reference the SKILL.md URL from
     `docs/skill-directory.md`,
     `docs/researcher-workflow-checklist.md`, and the relevant
     stage in `docs/pipeline.md` + `docs/pipeline.zh-TW.md`.
   - Update the README's How-to-use example phrases if the skill
     trigger phrasing is non-obvious.
3. Run `python -m pytest tests/` — must pass.
4. Test end-to-end:
   `claude plugin marketplace remove ai-research-skills`
   `claude plugin marketplace add WenyuChiou/ai-research-skills`
   `claude plugin install <new-plugin>@ai-research-skills`
   `claude plugin list` should show the new plugin as `✔ enabled`.

## Removing or deprecating a skill

Same coordination as renames: issue here first, upstream removal
after, catalog PR with the skill removed from `skills.yml` +
`marketplace.json` + the doc references in lockstep.

## For maintainers: GitHub repo settings

The repo's discoverability comes from two settings that aren't in git
and have to be set via the GitHub API or UI:

### Description + topics (set via `gh` CLI, version-controlled here)

```bash
gh api -X PATCH repos/WenyuChiou/ai-research-skills \
  -f description="13 Claude Code skills for common research tasks — literature triage, research design, project context, manuscript writing, and multi-AI delegation. 5-plugin marketplace, install in one command."

gh api -X PUT repos/WenyuChiou/ai-research-skills/topics \
  -f 'names[]=claude-code' -f 'names[]=claude-skills' \
  -f 'names[]=research' -f 'names[]=academic-writing' \
  -f 'names[]=zotero' -f 'names[]=obsidian' -f 'names[]=notebooklm' \
  -f 'names[]=literature-review' -f 'names[]=ai-skills' \
  -f 'names[]=marketplace'
```

Re-run if the description or topics need to change. Verify with:

```bash
gh repo view WenyuChiou/ai-research-skills --json description,repositoryTopics
```

### Social preview image (manual UI step — no API)

The image at `docs/img/social-preview.png` is the intended preview
for Twitter / Threads / LinkedIn / Slack shares. GitHub does not
expose an API for setting it; upload manually:

1. GitHub → repo Settings → General → Social preview.
2. Click "Edit" → upload `docs/img/social-preview.png`.
3. Save.

Re-upload only if the source image changes.
