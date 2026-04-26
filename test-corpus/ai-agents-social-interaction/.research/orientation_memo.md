# Orientation memo — produced by research-project-orienter

Generated 2026-04-25 by reading only the files in `.research/`. Total
inputs: `project_manifest.yml`, `experiment_matrix.yml`,
`data_dictionary.yml`, `run_log.md`, `open_questions.md`. Source code,
the README, the catalog YAML, and the test corpus were **not** opened —
the orientation comes entirely from the manifests.

---

## Project orientation: ai-research-skills

**Research question**: How should a researcher discover, install, and
combine AI skills across the full research lifecycle (literature →
planning → modelling → execution → visualization → writing →
submission), and which existing skills are verified to work in practice
on a real researcher's stack?

**Stage**: writing · **Last updated**: 2026-04-25

**Datasets** (4):
- `skills.yml` — 11 skills × 4 families with verification metadata, at
  `catalog/skills.yml`.
- `search-results.json` — 8 raw papers from `research-hub search`, used
  to seed the test corpus.
- `literature_matrix.md` — 9-column comparison over the 5-paper test
  corpus, at `.research/literature_matrix.md`.
- `per-paper test corpus` — 5 markdown files (frontmatter + abstract +
  extractable claims) at `test-corpus/ai-agents-social-interaction/papers/`.

**Experiments** (11 verification runs, by status):
- pass (T1): `research-hub`, `zotero-skills`, `literature-triage-matrix`,
  `research-context-compressor`
- pending (T1): `research-project-orienter`, `paper-memory-builder`,
  `academic-writing-skills`, `research-hub-multi-ai`,
  `notebooklm-brief-verifier`
- pass (T2): `gemini-delegate`
- caveat (T2): `codex-delegate` — default model `gpt-5.5` too new for
  installed `codex-cli 0.121.0`; works with `-m gpt-5.4`.

**Main entrypoints**:
- `README.md` — primary public-facing index, restructured around 8-stage
  research pipeline.
- `README.zh-TW.md` — Traditional Chinese mirror.
- `docs/researcher-workflow-checklist.md` — checklist by tool combination.
- `docs/skill-directory.md` — full per-skill directory.
- `docs/install.md` — install commands for each canonical repo.
- `catalog/skills.yml` — machine-readable source of truth.
- `docs/verification.md` — first verification report.
- `test-corpus/ai-agents-social-interaction/` — reproducible test inputs.

**Recent decisions** (0): no `.research/decisions.md` yet.

**Open questions** (4):
- Is `.research/` itself in scope for this umbrella repo, or should it
  stay only in downstream research projects?
- How should `catalog/skills.yml` versioning evolve? `verified_on`/
  `verification_status`/`verification_tier` fields were added without
  bumping `version: 2`.
- Should `README.bilingual.md` track the new pipeline structure?
- No `CONTRIBUTING.md` yet — external contributors lack guidance on how
  to add a skill or which verification standard to meet before merging.

**Evidence artifacts**:
- `docs/verification.md` — supports the verification status of each of
  the 11 catalogued skills.
- `.research/literature_matrix.md` — supports the literature-triage-matrix
  T1 pass.
- `.research/project_manifest.yml`, `.research/experiment_matrix.yml`,
  `.research/data_dictionary.yml` — supports the
  research-context-compressor T1 pass.
- `test-corpus/ai-agents-social-interaction/search-results.json` —
  supports reproducibility of the corpus selection.

**Suggested next action**: Stage is `writing`. The pending experiments
(`research-project-orienter`, `paper-memory-builder`,
`academic-writing-skills`, `research-hub-multi-ai`,
`notebooklm-brief-verifier`) need to be executed and their outputs
recorded in `docs/verification.md`. The codex-delegate caveat should be
either fixed (upgrade codex-cli or pin `gpt-5.4` in `~/.codex/config.toml`)
or accepted as documented.

---

## Token-saving check

Outside-`.research/` files read during orientation: **0**. Pure
manifest-driven. The 7 prompt-based skills can now be invoked against
this memo (paste it back as context) instead of re-reading the catalog
repo.
