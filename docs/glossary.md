# Glossary

The catalog uses a handful of conventions that aren't standard in
general "AI tooling" space. Defining them once so the rest of the docs
can use them without explaining each time.

Languages: [English](glossary.md) | [繁中](glossary.zh-TW.md)

---

### Plugin

A Claude Code marketplace entry — one row in
`.claude-plugin/marketplace.json`. Five of them in this catalog:
`research-workspace`, `academic-writing-skills`, `zotero-skills`,
`codex-delegate`, `gemini-delegate`. A plugin can bundle one or more
skills.

### Skill

A single `SKILL.md` file with frontmatter (`name`, `description`) plus
optional `references/` and `evals/` directories. Claude Code's
auto-trigger reads the `description` and tries to match your phrasing to
the right skill. 15 skills total across the 5 plugins in this catalog.

### Bare name vs qualified name

In Claude Code's `Skill()` call:

- **Bare name** — just the skill name, e.g. `Skill(skill="zotero-skills")`.
  Claude resolves the first match by registration order.
- **Qualified name** — `<plugin>:<skill>` form, e.g.
  `Skill(skill="zotero-skills:zotero-skills")`. Use this when two
  plugins ship a skill with the same name (silent shadowing) and you
  need to be explicit about which one. See
  [`docs/verification.md` § Silent skill-name collision](verification.md#silent-skill-name-collision-found-zotero-skills)
  for the one known case.

### `.research/` convention

A directory pattern that `research-hub` skills write to and read from,
typically at the root of your research project. Files inside:

- `project_manifest.yml` — high-level project state (questions,
  methods, current phase)
- `design_brief.md` — output of `research-design-helper` after the
  Socratic-segment walkthrough
- `literature_matrix.md` — output of `literature-triage-matrix`
- `experiment_matrix.yml`, `data_dictionary.yml` — compressor outputs
  for replay across AI sessions
- `orientation_memo.md` — output of `research-project-orienter`,
  generated from the manifests above

The convention exists so AI sessions can pick up state from prior
runs without re-scanning the repo.

### `.paper/` convention

A directory pattern that `paper-memory-builder` writes and
`academic-writing-skills` reads, at the root of a manuscript draft.
Files inside:

- `claims.yml` — list of claims in the draft, each with id, status
  (`draft` / `supported` / `rejected` / `gap`), and `evidence_artifacts`
- `figures.yml` — figure data and key numbers
- `reviewer_comments.md` — raw reviewer comments (your input)
- `reviewer_responses.md` — point-by-point response skeleton
  (`academic-writing-skills` output)
- `revision_history.yml` — track-changes log between revision rounds

### Obsidian cluster

A subdirectory inside your Obsidian vault holding the papers for a
specific topic (typically one literature review or one grant), plus
the metadata that `research-hub` writes (cluster index, per-paper
note skeletons, ingestion logs). The cluster boundary is the unit
`research-hub auto` ingests at a time.

### NotebookLM brief

An auto-generated summary that NotebookLM produces from the sources
you uploaded to it. `notebooklm-brief-verifier` checks whether the
brief actually used all the sources or quietly dropped some
(observed failure mode — see `docs/verification.md` for the real-life
Kumar-only-brief example).

### `research-hub auto`

A pipeline command (not a skill) that ingests a topic end-to-end:
search → dedupe → fetch → Zotero items → Obsidian cluster → NotebookLM
upload → brief generation. Requires `pip install research-hub-pipeline`.
The skills layer above this CLI lets you orchestrate it from natural
language inside Claude Code.

### T1 / T2 / T3 verification tiers

How each skill's verification status is graded in `docs/verification.md`
and `catalog/skills.yml`. The authoritative definitions live in
[`docs/verification.md` § Verification tiers](verification.md#verification-tiers);
this glossary entry is a short pointer:

- **T1** — Functional smoke test: skill invoked with real input;
  output inspected for the documented behaviour.
- **T2** — Binary / SKILL.md sanity: external CLI version probe plus
  a one-shot end-to-end call.
- **T3** — SKILL.md inspection: frontmatter, structure, and supporting
  reference files checked.

For prompt-based skills, T3 is "not weaker" than T1 — they're
qualitatively different checks rather than a strict hierarchy. See
the verification doc for the full nuance.

Current mix (per `docs/verification.md` 2026-05-09 header): 13 at T1,
1 at T2 — the 14 skills audited on that date. `gap-to-topic` (the 15th,
added 2026-05-21) was verified separately; see its `verification_notes`
in `catalog/skills.yml`. Tier is independent of `verification_status`
(pass/caveat/fail/not_yet) — the two axes describe different things.

### Skill router / auto-trigger

Claude Code's mechanism for matching your natural-language phrasing to
the right SKILL.md based on the frontmatter `description` field. When
auto-trigger picks the wrong skill, you can name the skill explicitly
(*"Use `literature-triage-matrix` to compare these 5 papers"*) — that
bypasses the router.

### Marketplace cache vs `~/.claude/skills/`

Two different install paths land SKILL.md in two different places:

- **Marketplace install** (`claude plugin install …@ai-research-skills`)
  → `~/.claude/plugins/cache/ai-research-skills/<plugin>/<version>/skills/<skill>/`.
  Confirm with `claude plugin list`, NOT `ls ~/.claude/skills/`.
- **Manual git clone** (the legacy path documented in `docs/install.md`)
  → `~/.claude/skills/<name>/`.

Both work; they just land in different directories. The catalog's
canonical recommendation is the marketplace path.

### Phase numbers (`Stage 1 → Stage 8`)

A research-workflow staging used in `docs/pipeline.md` and the skill
list in the main README. Each skill's tag like *(Stages 3a, 4)*
locates it on that pipeline:

- **Stages 1-2** — Discovery + literature triage
- **Stage 3a** — Research-question sharpening
- **Stage 3b** — Project manifest / context compression
- **Stage 4** — Build the model (design + scaffold)
- **Stage 5** — Run, calibrate & validate
- **Stage 6** — Visualise & interpret results
- **Stage 7** — Manuscript memory + writing
- **Stage 8** — Submission / reviewer response

(Codex / Gemini delegation is *cross-cutting* — available at every
stage, not a single stage — see `docs/pipeline.md`.)

Open `docs/pipeline.md` for the diagram; the stage numbers in the
README skill list point at it.

---

If a term in the docs trips you and isn't defined here, open an
[issue](https://github.com/WenyuChiou/ai-research-skills/issues) — the
glossary lives here so it can grow.
