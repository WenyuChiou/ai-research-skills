# Changelog

All notable changes to the `ai-research-skills` catalog (the registry
+ docs repo at `WenyuChiou/ai-research-skills`). The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning
follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Scope.** This CHANGELOG covers the catalog itself — `marketplace.json`,
> `catalog/skills.yml`, this repo's docs, tests, and scripts. Each
> plugin's source repo keeps its own changelog for SKILL.md content,
> reference files, and per-plugin behaviour. Upstream changes are
> picked up automatically because `marketplace.json` currently uses
> `ref: <default-branch>` for every plugin (pinning is on the roadmap,
> see [`docs/design-philosophy.md`](docs/design-philosophy.md)).

## [Unreleased]

## [1.4.0] - 2026-05-19

### Added

- `schema/skills.schema.json` — JSON Schema (Draft 2020-12) formalising
  the shape of `catalog/skills.yml`. Every field, every URL pattern,
  every enum is now machine-checked.
- `scripts/check_catalog_schema.py` — CI-runnable validator that loads
  the YAML, validates against the schema, and prints JSON-pointer-style
  error paths on failure.
- `tests/test_catalog_schema.py` — 14 pytest cases: 1 positive (live
  catalog validates), 1 meta (schema itself is valid Draft 2020-12),
  12 negative (ad-hoc mutations are correctly rejected — guards the
  schema from being silently weakened).
- `CHANGELOG.md` (this file) — reconstructed from PR history.
- `.github/workflows/test.yml` — installs `jsonschema` and runs
  `python scripts/check_catalog_schema.py` as a CI step alongside the
  existing pytest + consistency check.

### Changed

- `.claude-plugin/marketplace.json` `metadata.version`: `1.3.0 → 1.4.0`.
- `docs/design-philosophy.md` + `.zh-TW.md` — "JSON schema for
  catalog/skills.yml is on the roadmap" moved from the Roadmap section
  into the **What the catalog machine-checks** list, now that it ships.

## [1.3.0] - 2026-05-19

### Removed

- `audit-first-skills` sibling plugin (PR
  [#9](https://github.com/WenyuChiou/ai-research-skills/pull/9)).
  Was briefly registered in `1.2.0` earlier the same day; the scope
  was a misread — the sibling repo (`WenyuChiou/audit-first-skills`)
  was deleted and the catalog reverted to 5 plugins.
- `docs/why-not-ARS.md`, `docs/audit-first-design.md` — both specific
  to the deleted sibling.
- `docs/demo-walkthrough.md` + `.zh-TW.md` — out of scope for the
  curated-catalog framing; `docs/pipeline.md` + `docs/skill-directory.md`
  are the user-facing entry points.
- `templates/test_skill_integrity.template.py` — no consumer remains
  after the sibling deletion.

### Added

- `docs/design-philosophy.md` + `.zh-TW.md` — bilingual honest design
  contract: what the catalog is, what it machine-checks, what it does
  not, what's borrowed from ARS (shape, not scale), Roadmap.
- `README.md` + `README.zh-TW.md`: `## Limitations` / `## 限制`
  sections with concrete honest scope statements (one researcher;
  water-resources / ABM domain bias; no CI-asserted install round-trip).

### Fixed

- `.claude-plugin/README.md` `research-workspace` skill count `9 → 10`
  (the `paper-summarize` skill was missing from the enumeration; a
  pre-existing off-by-one surfaced by the cleanup pass).

## [1.2.0] - 2026-05-19  *(reverted same day in 1.3.0)*

### Added

- `audit-first-skills` sibling plugin registered via PR
  [#8](https://github.com/WenyuChiou/ai-research-skills/pull/8). A
  5-skill bundle (verify-references, senior-author-review,
  abstract-writer, scientific-writing, skill-lint) sourced from
  `WenyuChiou/audit-first-skills`.

> ⚠️ **Reverted in 1.3.0 (same day, ~2h later).** The user's intent
> was to mature `ai-research-skills` itself, not spin off a sibling
> repo. If you installed during the ~2-hour window the sibling was
> registered, run `claude plugin update` to refresh.

## [1.1.0] - 2026-05-09

### Added

- `scripts/check_marketplace_consistency.py` — CI script that verifies
  `catalog/skills.yml` and `.claude-plugin/marketplace.json` agree on
  plugin order, repo URLs, and skill counts.
- `.github/workflows/test.yml` — CI runs `pytest tests/ -q` and the
  new consistency script on every push / PR to `main`.

### Changed

- `codex-delegate` verification tier `T2 → T1` after upstream PR
  [`WenyuChiou/codex-delegate#1`](https://github.com/WenyuChiou/codex-delegate/pull/1)
  documented the `-m gpt-5.4` workaround + stdin-close requirement.
- `paper-summarize` verification tier `T2 → T1` after upstream PR
  [`WenyuChiou/research-hub#31`](https://github.com/WenyuChiou/research-hub/pull/31)
  surfaced the existing 23-test end-to-end suite in the skill's own
  Verification section.
- `research-hub-multi-ai` role repositioned (still T1) as the **router**
  in a router/leaves architecture via upstream PR
  [`WenyuChiou/research-hub#30`](https://github.com/WenyuChiou/research-hub/pull/30);
  triggers only when ≥2 delegates are needed in the same round.

## [1.0.0] - 2026-04-26

### Added

- Initial public Claude Code plugin marketplace at
  `WenyuChiou/ai-research-skills` with 5 plugins:
  - `research-workspace` — 10 skills auto-discovered from
    `WenyuChiou/research-hub`.
  - `academic-writing-skills`.
  - `zotero-skills`.
  - `codex-delegate`.
  - `gemini-delegate` (source: `WenyuChiou/gemini-delegate-skill`).
- 14 SKILL.md files across the 5 plugins.
- `catalog/skills.yml` — machine-readable catalog.
- Bilingual entry-point docs: `README.md` + `README.zh-TW.md`,
  `docs/install.md` + `.zh-TW.md`, `docs/verification.md` + `.zh-TW.md`,
  `docs/pipeline.md` + `.zh-TW.md`, `docs/researcher-workflow-checklist.md`
  + `.zh-TW.md`, `docs/skill-directory.md` + `.zh-TW.md`.
- `scripts/install-all.sh` + `install-all.ps1` batch installers.
- `tests/test_catalog.py` — structural pytest covering catalog YAML,
  marketplace JSON, README phrase invariants, persona table, verification
  counts.
- `.claude-plugin/marketplace.json` — Claude Code marketplace registry.
- `CONTRIBUTING.md` — coordination rules for source-dir renames,
  skill-output contracts, marketplace ↔ source repo plugin-name
  matching, default-branch ↔ marketplace `ref` matching.
- `LICENSE` — MIT.

[Unreleased]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/WenyuChiou/ai-research-skills/releases/tag/v1.0.0
