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

### Added

- **`docs/verification.md` + `docs/verification.zh-TW.md` § 2026-05-20 Phase 6 post-merge re-verification on v1.5.0** — captures the install round-trip + 14-skill auto-trigger + three dogfood walks re-run against the v1.5.0 (`1b557fc`) HEAD. Phase A passes (5 / 5 ✔ enabled). Phase B strict count 10 / 14 (lenient 13 / 14, one routing overlap with `agent-collab-workspace:agent-task-splitter`, three conservative input-first responses). Phase C three ⚠ partial walks, all gaps roll into the existing Phase 2 hard-gated research-hub backlog. No fix-PRs shipped against this repo this round; `marketplace.json` stays at 1.5.0 and no new tag is associated with the addendum.

## [1.5.0] - 2026-05-20

### Added

The usability content that the Phase 6 agent-team analysis flagged as
the highest-impact missing pieces. PR-1 (`1.4.3`) shipped only bug
fixes; this minor release adds net-new docs.

- **`docs/examples.md`** + **`docs/examples.zh-TW.md`** — synthetic
  deliverable samples for the 4 most-common skills
  (`literature-triage-matrix`: 5-paper × 9-column matrix;
  `academic-writing-skills`: banned-word audit table + reviewer-response
  table; `zotero-library-curator`: preview-only audit report; 
  `paper-summarize`: per-paper Key Findings / Methodology / Relevance
  markdown block). Closes the dogfood-report finding that fresh users
  install on faith without ever seeing what each skill produces.
- **`docs/glossary.md`** + **`docs/glossary.zh-TW.md`** — defines the
  catalog-specific terms used across the docs (plugin vs skill, bare
  name vs qualified name, `.research/` and `.paper/` conventions,
  Obsidian cluster, NotebookLM brief, `research-hub auto`, T1/T2/T3
  verification tiers, skill router, marketplace cache vs
  `~/.claude/skills/`, stage 1–8 phase numbers used in the skill list).
  Closes the dogfood-report finding that 4 of those terms were used
  without definition.
- **README.md + README.zh-TW.md — "Time + cost expectations" table**:
  maintainer-observed wall-time + conversation-turn ranges for the 5
  most common tasks (compare 5 papers, banned-word audit, reviewer
  response, Zotero audit, summarize 5 papers). Closes the dogfood
  finding that the docs gave no time/cost signal.
- **README.md + README.zh-TW.md — Zotero backup callout**: explicit
  "⚠️ Back up before any Zotero CRUD" block before any path that lets
  `zotero-skills` write. Closes the dogfood finding that 800-item
  library cleanup had no backup warning.
- **README.md + README.zh-TW.md — cross-links**: new top-of-page links
  to `docs/examples` and `docs/glossary`; new pointer to
  `docs/pipeline.md` + `docs/glossary.md`'s "Phase numbers" section
  from the All-14-skills section, so the dangling `*(Stages X, Y)*`
  tags now resolve.
- **`docs/install.md` + `docs/install.zh-TW.md` "Worked invocation
  examples"**: concrete recipes for `codex exec`, `gemini`, and Cursor
  rules-dir layout. Closes the per-host F3 gap (mechanism table was
  present in 1.4.x but no concrete invocation snippets).

### Changed

- **`docs/verification.md` + `docs/verification.zh-TW.md` — zotero-skills
  shadow collision workaround section rewritten** in plain language
  with a concrete `Skill(skill="zotero-skills:zotero-skills")` worked
  example and a clear explanation of when to use the qualified form
  vs the bare form. The 1.4.x version was honest but used too much
  jargon — fresh users could not act on it. (Underlying collision
  remains; the real fix is still Phase 2-gated.)
- **README.md + README.zh-TW.md — badge placement**: the 3 compatibility
  badges (MIT, agentskills.io, Hermes verified) moved from above the
  tagline into a `<sub>` block below the language selector. The
  promotional-feel-at-the-top issue flagged by the dogfood report;
  badges still verifiable, just less prominent.

### Out of scope for this release (Phase 2 hard-gated, unchanged)

- SKILL.md `description` rewrites in `WenyuChiou/research-hub` for
  auto-trigger keyword overlap (research-hub, paper-memory-builder,
  research-design-helper, notebooklm-brief-verifier,
  zotero-library-curator).
- Delete `research-hub/skills/zotero-skills/` to resolve the bare-name
  shadow collision at the source.
- Align `research-hub/.claude-plugin/plugin.json` to declare all 10
  shipped skills.
- v0.3 backlog: cross-model independent judge, corpus-scale FNR/FPR
  calibration, domain generalisation beyond water-resources / ABM.

## [1.4.3] - 2026-05-20

### Fixed

Stale-fact + install-path-consistency sweep driven by the Phase 6 agent-team
analysis (Explore + code-reviewer + fresh-user dogfood). All findings of the
"would actually break a new user's experience" class — no new content,
no schema changes. The matching usability *additions* ship in [1.5.0].

- **Verify-step bug across 4 user-entry-point docs** (6 distinct
  occurrences total): `README.md`, `README.zh-TW.md`,
  `docs/setup-guide.md` (3 locations: Phase B1, B-extra, C3),
  `docs/setup-guide.zh-TW.md` (same 3 locations) all instructed
  `ls ~/.claude/skills/<name>` after `claude plugin install`, but
  marketplace plugins do **not** extract there — they live under
  `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/skills/<name>/`.
  A new user running the prior verify command saw an empty directory
  and concluded the install failed. Replaced every occurrence with
  `claude plugin list` + an inline explanation. (The Phase 5.3.b
  addendum had documented this correctly in `docs/verification.md` but
  the fix never propagated to the user-entry-point docs.)
- `CONTRIBUTING.md`: `# 11 tests, < 1s` → `# 25 tests, < 1s` (test count
  was stale since the schema layer landed in 1.4.0).
- `CONTRIBUTING.md`: research-hub upstream description "9 skills" →
  "10 skills" (every other doc in the repo had already said 10;
  CONTRIBUTING.md was the lone holdout).
- `docs/skill-directory.zh-TW.md`: added the `paper-summarize` row that
  was present in the EN counterpart but missing in zh-TW, so 繁中 readers
  could not discover the skill from the directory.
- `docs/install.md` + `docs/install.zh-TW.md`: "9 skills under
  `~/.claude/skills/`" → "10 skills"; updated the enumeration to include
  `paper-summarize`.
- `docs/install.md` + `docs/install.zh-TW.md`: rewrote the
  `knowledge-base` deprecation note from "slated for removal in
  research-hub-pipeline v0.70" (future tense) to a past-tense
  observation that v0.70+ has dropped the alias — the prior wording was
  stale relative to current research-hub releases.
- `docs/install.md` §2–§5: relabeled the canonical install path for
  each of `academic-writing-skills` / `zotero-skills` / `codex-delegate`
  / `gemini-delegate` to `claude plugin install …@ai-research-skills`,
  collapsed the bare `git clone … ~/.claude/skills/<name>` blocks into
  `<details>` "Legacy alternative" sections. README and `install.md`
  now agree on which install path is canonical.
- `docs/setup-guide.md` + `docs/setup-guide.zh-TW.md` (Phase D verify):
  expected version `0.7x or higher` → `0.45.0 or higher` to match the
  baseline documented in `docs/verification.md`.
- `docs/setup-guide.md` + `docs/setup-guide.zh-TW.md` (Phase E3):
  added Node.js 18+ prerequisite before the `npm install -g` commands
  (Python-only environments hit `npm: command not found` with no
  diagnostic path); fixed the Codex CLI link from
  `WenyuChiou/codex-delegate#readme` (the skill wrapper) to
  `github.com/openai/codex` (the actual upstream CLI), same for the
  Gemini CLI link.

### Out of scope for this release

These came up in the Phase 6 analysis but cannot ship in 1.4.3 because
they require changes to the `WenyuChiou/research-hub` source repo,
which is Phase-2 hard-gated:

- SKILL.md `description` rewrites for `research-hub`, `paper-memory-builder`,
  `research-design-helper`, `notebooklm-brief-verifier`, `zotero-library-curator`
  to improve auto-trigger keyword overlap.
- Removing the embedded `research-hub/skills/zotero-skills/` copy to
  resolve the bare-name shadow collision documented in `docs/verification.md`
  §2026-05-20.
- Aligning `research-hub/.claude-plugin/plugin.json` to declare all 10
  shipped skills (currently declares 3).

## [1.4.2] - 2026-05-20

### Added

- [`docs/verification.md`](docs/verification.md) +
  [`docs/verification.zh-TW.md`](docs/verification.zh-TW.md) — Phase
  5.3.b end-to-end addendum: real `claude plugin marketplace add` →
  `install-all.sh` → bare-name skill resolution chain exercised on a
  clean Claude Code 2.1.142 machine. All 14 expected skill names
  resolve; trigger-routing prompts hit 14/14 (one resolution lands on
  the wrong copy of `zotero-skills` — see collision note in the
  addendum). Provides the first documented evidence for the
  "no install round-trip is asserted by CI" gap that the README
  Limitations section called out. CI still does not assert this path
  — only manual evidence now exists.
- [`README.md`](README.md) + [`README.zh-TW.md`](README.zh-TW.md)
  Limitations — documented the silent `zotero-skills` name collision
  (`research-workspace` embeds an old copy that shadows the canonical
  standalone via bare-name invocation), with the
  `Skill(skill="zotero-skills:zotero-skills")` workaround for users
  who need the canonical standalone variant. Upstream fix is deferred
  to Phase 2 (research-hub source edit).

### Changed

- `.claude-plugin/marketplace.json` — `research-workspace`
  description now enumerates all 10 listed research-hub skills (the
  previous text listed 9 items for a stated count of 10 — the
  `project orientation` item for `research-project-orienter` was
  missing). No behavioural change; documentation polish to match the
  stated count.
- `.claude-plugin/marketplace.json` `metadata.version`: `1.4.1 → 1.4.2`.

## [1.4.1] - 2026-05-20

### Removed

- `docs/public-post-outline.md` — was launch-marketing material, no
  longer needed after the marketplace shipped.
- `docs/repo-map.md` + `docs/repo-map.zh-TW.md` — content duplicated
  by `CONTRIBUTING.md` §"Where the change belongs" and
  `docs/skill-directory.md`.

### Changed

- `docs/index.html` — removed the "Repo map" link card.

## Upstream ecosystem notes

> This section is **not** part of any catalog release. It records
> changes that landed in plugin source repos during the catalog's
> Phase 5.3.a audit window (2026-05-20) so future readers can trace
> when the maturity floor moved.

- [`WenyuChiou/academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills)
  — added `CHANGELOG.md`, `.github/workflows/test.yml` (first CI),
  and fixed a latent test path bug (silent since the 2026-04-26
  marketplace migration). Tagged
  [`v0.1.0`](https://github.com/WenyuChiou/academic-writing-skills/releases/tag/v0.1.0).
- [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills)
  — added MIT `LICENSE` (was previously legally ambiguous despite
  README's `## License: MIT` declaration); added `CHANGELOG.md`;
  tagged
  [`v0.1.0`](https://github.com/WenyuChiou/zotero-skills/releases/tag/v0.1.0).
- [`WenyuChiou/codex-delegate`](https://github.com/WenyuChiou/codex-delegate)
  — added `CHANGELOG.md`; tagged
  [`v0.1.0`](https://github.com/WenyuChiou/codex-delegate/releases/tag/v0.1.0).
- [`WenyuChiou/gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill)
  — added `CHANGELOG.md`; tagged
  [`v0.1.0`](https://github.com/WenyuChiou/gemini-delegate-skill/releases/tag/v0.1.0).

Pinning `marketplace.json` plugin `ref` to `v0.1.0` is deferred — see
`docs/design-philosophy.md` §Roadmap.

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

[Unreleased]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.5.0...HEAD
[1.5.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.3...v1.5.0
[1.4.3]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.2...v1.4.3
[1.4.2]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/WenyuChiou/ai-research-skills/releases/tag/v1.0.0
