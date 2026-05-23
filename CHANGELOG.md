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

## [1.5.16] - 2026-05-23

### Changed

- **`research-workspace` plugin registry version `0.3.12` → `0.3.15`**
  (`.claude-plugin/marketplace.json`). Bundles three upstream
  `research-hub` releases:
  - **PR #97 (v0.3.12 → v0.3.13)** — SKILL.md prose tightenings from
    the v0.3.12 dogfood. `research-context-compressor` `## Outputs`
    section now shows an explicit `provenance.from_gap` example block
    (the wire was registered in the schema doc but the Output example
    didn't show it — F1). `research-design-helper` §0 explicitly
    forbids `_PRE-FILL_`-style annotations in the design_brief file
    content (chat message signals pre-fill, file content stays clean —
    F2).
  - **PR #98 (v0.3.13 → v0.3.14)** — `brief_to_docx.js` ships inside
    `skills/research-design-helper/scripts/` as the sister generator
    to `dossier_to_docx.js`. `design_brief.md` becomes shareable as a
    Word document for advisor / committee review — closes F4 from the
    v0.3.12 dogfood. Not part of the contracted Stage 3a output;
    downstream skills read the `.md`, the `.docx` is human-only.
  - **PR #99 (v0.3.14 → v0.3.15)** — codex review tightenings from
    the independent eval of the v0.3.12-v0.3.14 deliverables. C2:
    new multi-eligible `.gaps.yml` fixture exercises the §0
    "2+ candidates → ask the user" branch (was documented in
    SKILL.md, never run against a real multi-eligible fixture).
    C4: `design_brief.md` frontmatter gains optional
    `placeholder_segments: []` field so dogfood / test-fit content
    can be machine-flagged (downstream tools should refuse to gate
    research on a brief with non-empty list).

- **Codex C1 fix — `docs/examples.md` verdict-shape table.** The
  table previously claimed "each candidate gets one of three outcomes"
  but listed four rows, the fourth being `Not assessed`. Per the
  codex independent review: `Not assessed` is a *gate-cell status*
  inside the scorecard table (a gate skipped because an earlier gate
  failed), NOT a fourth candidate-level verdict. The table is now
  relabeled to make this distinction explicit: three rows for the
  three candidate verdicts (`Do not pursue` / `Worth pursuing
  conditionally` / `Worth pursuing`), and the `Not assessed` row is
  separated under a sub-heading explaining it applies to gate cells
  in the per-candidate scorecard, not the candidate-level verdict.

- **`catalog/skills.yml`** — `research-design-helper` +
  `research-context-compressor` `verification_notes` appended with
  the v0.3.13 / v0.3.14 / v0.3.15 descriptions (`gap-to-topic`
  unchanged — PRs #97–#99 made no changes to that skill itself; its
  notes still end at the v0.3.10 / v0.3.11 history). Both skills'
  `verification_status` stays `pass`.

`source.ref` unchanged (`master`). Skill count unchanged at 11.
Catalog metadata version `1.5.15` → `1.5.16`.

## [1.5.15] - 2026-05-23

### Added

- **`docs/example-topic-dossier.*` published** — six-file example
  deliverable for `gap-to-topic`, matching the existing
  `docs/example-literature-review-deliverable.*` pattern:
  `.md`, `.docx`, `.bib`, `.gaps.yml`, `.zh-TW.md`, `.zh-TW.docx`.
  Copied from the dogfood at
  `~/.claude/audits/dogfood_runs/2026-05-21-gap-to-topic-llm-abm-profiles/`
  (LLM applications in water resources — Candidate 2 conditional-go).
  `docs/examples.md` gains a corresponding section. Catalog users can
  now read what the `gap-to-topic` skill emits without installing.

### Changed

- **`research-workspace` plugin registry version `0.3.10` → `0.3.12`**
  (`.claude-plugin/marketplace.json`). Bundles two upstream
  `research-hub` releases:
  - **PR #95 (v0.3.10 → v0.3.11)** — schema reference for
    `topic_dossier.gaps.yml` refreshed to match what the skill
    actually emits since v0.3.6 (the `--screen` fit-check) and v0.3.9
    (the 7-section reflow): now documents top-level `run_type` /
    `recall` (with full `screen` sub-block) / `pipeline`, plus
    per-gap `open_confidence` / `dead_end_evidence` /
    `borderline_reason` / `verdict` / `verdict_reason`. New
    `downstream_consumer: research-design-helper` top-level key as a
    forward-compat hook. Companion: `gap-to-topic` made discoverable
    in research-hub's own `docs/ai-research-skills.md` (it was
    invisible there since the skill shipped at v0.3.10).
  - **PR #96 (v0.3.11 → v0.3.12)** — Stage 2 → 3a → 3b handoff
    wiring. `research-design-helper` now reads
    `.research/topic_dossier.gaps.yml` as new Input #2: when a recent
    `gap-to-topic` run is present, segment 1 (RQ) is pre-filled from
    the chosen `gaps[].statement` and segment 5 (risks) from
    `open_questions[]` + the specific concern hinted by
    `gaps[].feasibility`. Segments 2–4 (mechanism / identifiability
    / validation) are never pre-filled. Candidate selection is
    verdict-aware (filters `gaps[]` to
    `verdict in {conditional-go, go}`). `design_brief.md` frontmatter
    gains optional `source` (URI-fragment pointer to the chosen gap,
    e.g. `topic_dossier.gaps.yml#G2`) and `gap_verdict` (frozen
    snapshot of `verdict` + first 60 chars of `verdict_reason`) so
    provenance is recorded. Companion fix: `research-context-compressor`
    now reads `.research/design_brief.md` as Input #2 (matching the
    `pipeline.md` contract) and copies the `source` gap-id to the
    manifest's `provenance.from_gap` field (registered in
    `docs/research-workspace-manifest.md` upstream). First cross-skill
    handoff integration test ships at
    `tests/test_handoff_gap_to_topic_design_helper.py`.

- **Catalog drift fixed — `gap-to-topic` now visible in all
  narrative docs.** Since the skill shipped (research-hub PR #93 →
  catalog `1.5.14` via ai-research-skills PR #30), `README.md`
  "All 15 skills" details block claimed
  "11 skills" but only listed 10. `docs/pipeline.md` Stage 2 table
  omitted it. `docs/img/pipeline-overview-prompt.md` Stage 2 chip set
  + 11-skill enumeration omitted it. This PR adds `gap-to-topic` to:
  - `README.md` + `README.zh-TW.md` "All 15 skills" research-hub list
  - `docs/pipeline.md` + `.zh-TW.md` Stage 2 table (and updated Stage 3a
    row to reflect the v0.3.12 `.gaps.yml` handoff)
  - `docs/img/pipeline-overview-prompt.md` Stage 2 chip set + the
    canonical 11-skill enumeration in the regen pre-conditions
  - **Hand-off action (not gating this merge):** `docs/img/pipeline-overview.png`
    and `pipeline-overview.zh-TW.png` need manual regeneration via
    ChatGPT image-gen using the updated prompt. Until that ships, the
    image is one chip behind reality.

- **`catalog/skills.yml`** — `research-design-helper` and
  `research-context-compressor` `verification_notes` appended with the
  v0.3.12 handoff description. `gap-to-topic` `verification_notes`
  appended with the v0.3.11 schema refresh description. All three
  `verification_status` stay `pass`.

`source.ref` unchanged (`master`). Skill count unchanged at 11.
Catalog metadata version `1.5.14` → `1.5.15`.

## [1.5.14] - 2026-05-22

### Changed

- **`research-workspace` plugin registry version `0.3.9` → `0.3.10`**
  (`.claude-plugin/marketplace.json`). Mirrors upstream `research-hub`
  PR #93, which ships `dossier_to_docx.js` as a first-class artifact
  inside the `gap-to-topic` skill (`skills/gap-to-topic/scripts/`). The
  `.docx` is now a contracted deliverable, not an operator-local
  post-processing step: the script handles Markdown table-separator
  skipping (so `|---|---|` rows do not leak as literal "---" cells in
  Word), bilingual verdict-cell colour coding (light red "do not pursue"
  / "不予推進", light yellow conditional "worth pursuing … only if" /
  "值得推進 … 須其待決條件成立", light green unconditional, light grey
  "not assessed" / "未評估"), and en / zh-TW font auto-selection
  (Microsoft JhengHei when the filename matches `.zh|zh-|zh_|-tw|-cn`,
  Arial otherwise). Prereq: `npm install -g docx` (one-time global) or
  per-skill `npm install docx`. `source.ref` unchanged (`master`); skill
  count unchanged at 11. `gap-to-topic` `verification_notes` in
  `catalog/skills.yml` updated; `verification_status` stays `pass`.
  Catalog metadata version `1.5.13` → `1.5.14`.

## [1.5.13] - 2026-05-22

### Changed

- **`research-workspace` plugin registry version `0.3.8` → `0.3.9`**
  (`.claude-plugin/marketplace.json`). Mirrors upstream `research-hub`
  PR #92, which reflowed the `gap-to-topic` dossier as a 7-section
  research-grade decision memo: Executive Summary with per-candidate
  verdict cards → Candidate Definitions → per-candidate Decision Scorecards
  → Evidence Base → Gate-by-Gate Assessment (fixed five-field skeleton) →
  Risks & Upgrade/Kill Tests → Recommended Next Steps → reproducibility-log
  Appendix A → file-list Appendix B. `source.ref` unchanged (`master`);
  skill count unchanged at 11. `gap-to-topic` `verification_notes` in
  `catalog/skills.yml` updated; `verification_status` stays `pass`.
  Catalog metadata version `1.5.12` → `1.5.13`.

## [1.5.12] - 2026-05-22

### Changed

- **`research-workspace` plugin registry version `0.3.7` → `0.3.8`**
  (`.claude-plugin/marketplace.json`). Mirrors upstream `research-hub`
  PR #89, a section-by-section rework of the `gap-to-topic` dossier for
  researcher value: a 5-point Likert Decision scorecard, a "what it would
  contribute" claim and a minimum-validation sketch in Gate 2, design /
  scale / proposal-vs-dissertation feasibility in Gate 3, a
  conditional-recommendation framing in the decision section, and a
  method-note Appendix. `source.ref` unchanged (`master`); skill count
  unchanged at 11. `gap-to-topic` `verification_notes` in
  `catalog/skills.yml` updated; `verification_status` stays `pass`. Catalog
  metadata version `1.5.11` → `1.5.12`.

## [1.5.11] - 2026-05-22

### Changed

- **`research-workspace` plugin registry version `0.3.6` → `0.3.7`**
  (`.claude-plugin/marketplace.json`). Mirrors upstream `research-hub`
  PR #87, which reworked the `gap-to-topic` dossier to read as a plain
  summary report — the `G1`/`G2` machine codes dropped from the document
  (kept only in `.gaps.yml`), the Decision-scorecard glyphs replaced with
  plain words, the "no-go / go" verdict jargon replaced with plain phrasing,
  and an in-document "What's in this deliverable" index added. `source.ref`
  unchanged (`master`); skill count unchanged at 11. `gap-to-topic`
  `verification_notes` in `catalog/skills.yml` updated; `verification_status`
  stays `pass`. Catalog metadata version `1.5.10` → `1.5.11`.

## [1.5.10] - 2026-05-22

### Changed

- **`research-workspace` plugin registry version `0.3.5` → `0.3.6`**
  (`.claude-plugin/marketplace.json`). Mirrors upstream `research-hub`
  PR #86, which wired `gap-to-topic` §1 onto the new `search --screen`
  fit-check BM25 relevance gate (research-hub PR #84) — §1 step 1 now runs
  `search --adversarial --screen --json` and builds the matrix and `.bib`
  from the on-topic results only. `source.ref` unchanged (`master`); skill
  count unchanged at 11. `gap-to-topic` `verification_notes` in
  `catalog/skills.yml` updated; `verification_status` stays `pass`. Catalog
  metadata version `1.5.9` → `1.5.10`.

## [1.5.9] - 2026-05-22

### Changed

- **`research-workspace` plugin registry version `0.3.2` → `0.3.5`**
  (`.claude-plugin/marketplace.json`). Mirrors three upstream `research-hub`
  plugin bumps that iterated the `gap-to-topic` dossier for readability:
  reader-first layout (PR #78), scannability tables incl. a Decision
  scorecard (PR #80), and evidence-strength tags plus an upgrade/kill test
  from a Codex evaluation (PR #82). `source.ref` unchanged (`master`); skill
  count unchanged at 11. `gap-to-topic` `verification_notes` in
  `catalog/skills.yml` updated to record the dossier iteration; the skill's
  `verification_status` stays `pass`. Catalog metadata version
  `1.5.8` → `1.5.9`.

## [1.5.8] - 2026-05-22

### Changed

- **`research-workspace` plugin registry version `0.3.1` → `0.3.2`**
  (`.claude-plugin/marketplace.json`). Mirrors the upstream `research-hub`
  `.claude-plugin/plugin.json` bump (PR #76), which fixed a `gap-to-topic`
  §1 workflow gap — the SKILL.md named `literature-triage-matrix` as the
  default prior-art tool but no §1 step produced its matrix; §1 now has an
  explicit step that runs it. `source.ref` unchanged (`master`); skill
  count unchanged at 11. `gap-to-topic` `verification_notes` in
  `catalog/skills.yml` updated to record the fix and the end-to-end
  re-test on the corrected pipeline (topic: "LLM applications in water
  resources"). Catalog metadata version `1.5.7` → `1.5.8`.

## [1.5.7] - 2026-05-21

### Changed

- **`gap-to-topic` verification status `not_yet` → `pass`, tier `T3` → `T1`**
  (`catalog/skills.yml`). The skill was dogfood-verified end-to-end on
  2026-05-21: a run on the topic "LLM-generated agent profiles in
  agent-based models" produced a complete five-section `topic_dossier.md`
  plus `.bib` and `.gaps.yml` companions matching the dossier template.
  The run surfaced one Gate 1 bug — the `.bib` instruction relied on
  `cite`, which resolves only already-ingested Zotero items — fixed
  upstream in research-hub plugin v0.3.1. YAML-side verification counts
  are now 15 pass + 0 caveat + 0 not_yet (`test_catalog.py` updated).
- **`research-workspace` plugin registry version `0.3.0` → `0.3.1`**
  (`.claude-plugin/marketplace.json`). Mirrors the upstream `research-hub`
  `.claude-plugin/plugin.json` bump (PR #75) that fixed the `gap-to-topic`
  Gate 1 `.bib` instruction. `source.ref` unchanged (`master`); skill
  count unchanged at 11. Catalog metadata version `1.5.6` → `1.5.7`.

## [1.5.6] - 2026-05-21

### Changed

- **`research-workspace` plugin registry version `0.2.0` → `0.3.0`**
  (`.claude-plugin/marketplace.json`). Mirrors the upstream `research-hub`
  `.claude-plugin/plugin.json` bump — research-hub added an 11th packaged
  skill, `gap-to-topic` (a topic-decision dossier that runs a candidate
  research topic through a 3-gate go/no-go test). The registry entry now
  matches the upstream `0.3.0`, so a
  `claude plugin update research-workspace@ai-research-skills` pulls a
  fresh cache that includes the new skill. `source.ref` unchanged
  (`master`); the plugin description is updated 10 → 11 skills.

## [1.5.5] - 2026-05-21

### Added

- **`docs/example-literature-review-deliverable.md` (+ `.zh-TW.md`,
  `.docx`, `.zh-TW.docx`, `.bib`, `.gaps.yml`) — a full
  literature-review deliverable example.** The per-skill entries in
  `docs/examples.md` show output *fragments*; this new file shows the
  consolidated 9-section document the research-hub literature pipeline
  (`search` → `literature-triage-matrix` → `research-design-helper`)
  produces end to end — literature inventory, per-paper summaries,
  cross-paper
  synthesis, tagged research-gap analysis, recommended next step,
  references, and a provenance section. Doubles as a reusable
  section-contract template. Fully synthetic (6 fabricated papers,
  placeholder identifiers) per the catalog's no-real-artifacts policy.
  Markdown + Word, English + 繁中. Ships machine-readable companions
  too — a BibTeX `.bib` (references) and a `.gaps.yml` (structured
  research gaps + open questions). `docs/examples.md` and `.zh-TW.md`
  gain a "Putting it together" pointer section.

## [1.5.4] - 2026-05-21

### Changed

- **`academic-writing-skills` plugin registry version `0.1.0` → `0.2.0`**
  (`.claude-plugin/marketplace.json`). Mirrors the upstream
  `academic-writing-skills` `.claude-plugin/plugin.json` bump
  (Phase 8.1). A 2026-05-21 Phase 9 behavioral verification found the
  `§8 step 10` claim-gap cross-reference (added in the prior
  `academic-writing-skills` release) had shipped to that repo's `main`
  but not to user installs — the plugin cache directory is keyed on
  the version string, and the prior change never bumped it. The
  registry entry now matches the upstream `0.2.0` so a
  `claude plugin update academic-writing-skills@ai-research-skills`
  pulls a fresh cache. `source.ref` unchanged (`main`).

## [1.5.3] - 2026-05-21

### Changed

- **`research-workspace` plugin registry version `0.1.0` → `0.2.0`**
  (`.claude-plugin/marketplace.json`). Mirrors the upstream
  `research-hub` `.claude-plugin/plugin.json` bump (Phase 8 Wave 1).
  A 2026-05-20 dogfood test found fresh `claude plugin install` users
  were still served the pre-Phase-7 cached `0.1.0` skill bundle — the
  `paper-memory-builder` anti-leakage rule (Phase 7 Wave A) and the
  `zotero-skills` shadow removal (Wave C) had shipped to the
  `research-hub` `master` branch but not propagated to installs,
  because the plugin cache directory is keyed on this version string.
  The registry entry now matches the upstream `0.2.0` so a
  `claude plugin marketplace update` pulls a fresh cache. The plugin
  `source.ref` is unchanged (`master`); only the version label moves.

## [1.5.2] - 2026-05-20

### Added

- **Standalone-skills callout in `README.md` + `README.zh-TW.md`** at
  the top of the `## Install` section: explicit list of the 7 of 14
  skills that work immediately with only Claude Code (no Python /
  Zotero / Codex / Gemini CLI setup) — the 6 manifest / triage /
  design skills inside `research-workspace`
  (`literature-triage-matrix`, `research-design-helper`,
  `research-context-compressor`, `research-project-orienter`,
  `paper-memory-builder`, `research-hub-multi-ai`) plus
  `academic-writing-skills`. Closes the "如果其他人只有 Claude
  怎麼辦" question raised during the Phase 5.3.b verification dogfood.

## [1.5.1] - 2026-05-20

### Fixed

- **README badges rendered as literal markdown text instead of shield
  images.** The Phase 6 PR-2 (`v1.5.0`) "badge clutter" cleanup wrapped
  the three badges in `<sub>...</sub>` for smaller font, but per
  CommonMark / GFM rules a multi-line markdown block inside an HTML
  block tag (with no blank line separator) is not processed as
  markdown — so the three badges shipped as literal
  `[![License](...)](LICENSE)` text on GitHub's renderer. Replaced
  the markdown image syntax with equivalent pure-HTML
  `<a><img></a>` inside the same `<sub>` wrapper, on a single line.
  Now the badges render correctly as 3 small shields linking to
  `LICENSE` and `.research/hermes-compatibility-audit.md`. Same fix
  applied to `README.zh-TW.md`. No behavior change beyond the visual
  fix; the link targets are unchanged.

## [1.5.0] - 2026-05-20

### Added

The usability content that the Phase 6 agent-team analysis flagged as
the highest-impact missing pieces. PR-1 (`1.4.3`) shipped only bug
fixes; this minor release adds net-new docs.

- **`docs/verification.md` + `docs/verification.zh-TW.md` § 2026-05-20 Phase 6 post-merge re-verification on v1.5.0** — captures the install round-trip + 14-skill auto-trigger + three dogfood walks re-run against the v1.5.0 (`1b557fc`) HEAD. Phase A passes (5 / 5 ✔ enabled). Phase B strict count 10 / 14 (lenient 13 / 14, one routing overlap with `agent-collab-workspace:agent-task-splitter`, three conservative input-first responses). Phase C three ⚠ partial walks, all gaps roll into the existing Phase 2 hard-gated research-hub backlog. (Originally landed in PR #15 on top of `v1.5.0`; recorded here under the version it actually exercised.)

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

[Unreleased]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.5.6...HEAD
[1.5.6]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.5.5...v1.5.6
[1.5.5]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.5.4...v1.5.5
[1.5.4]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.5.3...v1.5.4
[1.5.3]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.5.2...v1.5.3
[1.5.2]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.5.1...v1.5.2
[1.5.1]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.3...v1.5.0
[1.4.3]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.2...v1.4.3
[1.4.2]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/WenyuChiou/ai-research-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/WenyuChiou/ai-research-skills/releases/tag/v1.0.0
