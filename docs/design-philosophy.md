# Design philosophy

This document is the design contract of `ai-research-skills` — what the
catalog promises to do, and what it deliberately does not.

The catalog is a curated index of [Claude Code](https://claude.ai/code)
plugins for researcher workflows. Each plugin's code lives in a
maintained source repo; this repo is the registry plus docs.

Languages: [English](design-philosophy.md) | [繁中](design-philosophy.zh-TW.md)

---

## What the catalog is

Five plugins that map to 15 SKILL.md files under `~/.claude/skills/`
after install:

| Plugin | Source repo | What's in it |
|---|---|---|
| `research-workspace` | [`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub) | 11 research-hub skills (literature triage, project memory, NotebookLM brief verification, paper summarisation, …) |
| `academic-writing-skills` | [`WenyuChiou/academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | Manuscript revision, banned-word audit, claim-evidence check, journal format, reviewer response |
| `zotero-skills` | [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | Full Zotero CRUD (local + Web API) |
| `codex-delegate` | [`WenyuChiou/codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | Claude → Codex CLI handoff for code-heavy work |
| `gemini-delegate` | [`WenyuChiou/gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill) | Claude → Gemini CLI handoff for long-context / CJK work |

---

## Design choices

1. **Curated, not auto-discovered.** Every plugin in the catalog is
   hand-picked for a specific researcher use case, and is used by the
   maintainer in active research projects.
2. **No pipeline orchestrator.** Skills are invoked individually by the
   researcher. The catalog does not chain them into a stage-1 →
   stage-2 pipeline.
   [`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills)
   is the reference point if you want orchestration.
3. **Opinionated subset, not exhaustive coverage.** Five plugins, 15
   skills — chosen because they close gaps the maintainer hit in real
   research, not because they cover everything an academic might want.
4. **Bilingual entry points.** README, install, verification, pipeline,
   skill-directory, and this design doc are all maintained in both
   English and Traditional Chinese. Internal reference files inside
   each skill are English-only by convention.
5. **Honest scope.** The README has a Limitations section; each plugin's
   source repo carries its own. The catalog was assembled and tested by
   one graduate-student researcher; it is not corpus-scale-validated,
   and the maintainer's domain bias (water resources, agent-based
   modeling) is acknowledged in writing rather than papered over.

---

## What the catalog machine-checks

CI runs on every push and PR to `main`. It runs `python -m pytest tests/ -q`,
`python scripts/check_marketplace_consistency.py`, and
`python scripts/check_catalog_schema.py`. Together these guard:

- `catalog/skills.yml` — every field shape against
  [`schema/skills.schema.json`](../schema/skills.schema.json) (JSON
  Schema Draft 2020-12): required fields per skill / family /
  top-level, URL pattern regexes, enum-restricted `verification_status`
  / `verification_tier`, ISO-date `verified_on` and `updated`, unknown
  fields rejected (`additionalProperties: false`).
- `.claude-plugin/marketplace.json` — well-formed schema, expected
  plugin order, every plugin has a source URL.
- Cross-document consistency — every catalog skill's `repo_url` maps to
  a plugin source URL; the `research-workspace` description's
  `<N> research-hub skills` count matches the actual catalog count;
  every `skill_url` is a real `/blob/<branch>/SKILL.md` shape.
- README content — researcher-facing audience phrases present (Zotero,
  Obsidian, NotebookLM mentioned by name); persona table present in
  both languages; canonical install command (`research-hub setup`)
  consistent across README + install docs + catalog YAML.
- Verification counts — 15 skills total with the documented status
  split (see [`docs/verification.md`](verification.md)).

A red CI run blocks merge. The full check list is in
[`tests/test_catalog.py`](../tests/test_catalog.py),
[`tests/test_catalog_schema.py`](../tests/test_catalog_schema.py),
[`scripts/check_marketplace_consistency.py`](../scripts/check_marketplace_consistency.py),
and [`scripts/check_catalog_schema.py`](../scripts/check_catalog_schema.py).

---

## What the catalog does NOT machine-check

- **SKILL.md content quality.** That's the source repo's
  responsibility. Each plugin's source repo carries its own tests.
- **Upstream URL liveness.** A network test would be flaky; manual
  review on PRs.
- **Cross-skill artifact contracts** — e.g. `paper-memory-builder`
  writes `.paper/claims.yml`, `academic-writing-skills` reads it.
  Both must agree on path/schema, but the catalog does not enforce
  it. See [CONTRIBUTING.md](../CONTRIBUTING.md) §2 for the manual
  coordination rule.
- **Behavioral correctness on real-world inputs.** Layer-3 acceptance
  (running each skill against a real manuscript) is the source repo's
  responsibility, not the catalog's.

---

## What's borrowed from related projects

[`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills)
("ARS") is the mature, comprehensive reference for academic skill
suites in Claude Code. Patterns adapted (shape, not scale) into this
catalog and its plugins:

- **Schema-driven validation** at the catalog layer —
  [`schema/skills.schema.json`](../schema/skills.schema.json) (JSON
  Schema Draft 2020-12) formalises the shape of `catalog/skills.yml`,
  enforced by [`scripts/check_catalog_schema.py`](../scripts/check_catalog_schema.py)
  in CI and by [`tests/test_catalog_schema.py`](../tests/test_catalog_schema.py)
  on every PR.
- **Honest provenance** — every comparison to another project (in this
  doc, in plugin READMEs, in CHANGELOG entries) is paired with a
  verifiable link to the source it cites.
- **Per-skill `Limitations` sections** — convention is to ship one per
  source repo's `README`, plus a catalog-wide one here.

Patterns deliberately **not** ported:

- Pipeline orchestrator stages — the catalog is a registry, not a runner.
- Opt-in feature flags (e.g. `<PROJECT>_*` env vars). Every check that
  ships, ships on.
- Declarative-only annotations that aren't runtime-enforced.

If you want pipeline orchestration with maximum coverage, ARS is the
right pick. If you want a curated subset that loads into Claude Code
one plugin at a time, this catalog is.

---

## Roadmap

The catalog has open work and acknowledged gaps. See open issues + PRs
for current progress. Items not yet promised by any version:

- Cross-model independent judge (Codex / Gemini as second opinion on
  skill behavioral evals).
- Corpus-scale FNR/FPR calibration of any plugin.
- Generalisation tested beyond the maintainer's domain (water
  resources, agent-based modeling).
- Translation of internal reference files (only top-level docs
  bilingual; convention).

---

This document is the catalog's design contract. If you find behaviour
that contradicts a claim above, open an issue.
