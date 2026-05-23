# AI Research Skills

> A catalog of 15 Claude Code skills for the full research workflow —
> literature → research design → build → run → manuscript → submit,
> with cross-AI delegation built in.

Languages: [English](README.md) | [繁中](README.zh-TW.md) ·
[Pipeline](docs/pipeline.md) ·
[Examples](docs/examples.md) ·
[Glossary](docs/glossary.md)

**What this is.** Five Claude Code plugins (15 skills total) for
researchers running real projects with AI in the loop — graduate students,
PhDs, postdocs, and research support staff. Skills are
[agentskills.io](https://agentskills.io)-compliant Markdown files;
they auto-trigger inside Claude Code from your phrasing, and load
into Codex CLI / Gemini CLI / Cursor / Windsurf / Hermes too (see
[§6 Compatibility](#6-compatibility)).

<sub><a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a> <a href=".research/hermes-compatibility-audit.md"><img alt="agentskills.io spec compliant" src="https://img.shields.io/badge/agentskills.io-spec_compliant-2DA89C"></a> <a href=".research/hermes-compatibility-audit.md"><img alt="Hermes 0.13.0 skill-load verified" src="https://img.shields.io/badge/Hermes_0.13.0-skill--load_verified-2DA89C"></a></sub>

> 📚 Part of the [agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
> — featured in §13–14 (research workflows).

---

## 1. Install — get the skills

**TL;DR — 30 seconds:**

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
```

Two commands. You now have 11 `research-hub` skills installed — 6 of
them (`literature-triage-matrix`, `research-design-helper`,
`research-context-compressor`, `research-project-orienter`,
`paper-memory-builder`, `research-hub-multi-ai`) work immediately
because they're pure-reasoning. The other 5 wrap external tools
(Zotero / NotebookLM / the `research-hub-pipeline` Python CLI) and
need per-tool setup.

> **Reading this in Claude / ChatGPT?** Paste this whole §1 into your
> assistant and ask *"Install all 5 plugins for me and verify."* The
> commands below are self-contained — an AI assistant can run them
> step by step without external lookups.

**Additive install — stop after any step and use what you have:**

```bash
# 1. Marketplace + 11 research-hub skills (6 immediately usable, pure reasoning)
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills

# 2. Manuscript work — claim-evidence audit, banned-word, reviewer response
claude plugin install academic-writing-skills@ai-research-skills

# 3. Zotero CRUD (enable local API in Zotero desktop first — docs/setup-guide.md §C)
claude plugin install zotero-skills@ai-research-skills

# 4. Multi-CLI delegation (install codex / gemini CLI binaries first)
claude plugin install codex-delegate@ai-research-skills
claude plugin install gemini-delegate@ai-research-skills

# 5. Literature pipeline automation (Python CLI behind research-hub skills)
pip install research-hub-pipeline
research-hub setup
```

Batch all 5 plugins in one go:

```bash
bash scripts/install-all.sh        # macOS / Linux / git-bash
pwsh scripts/install-all.ps1       # Windows PowerShell
```

**Verify:**

```bash
claude plugin list
# expected: 5 plugins, each ending in @ai-research-skills, each ✔ enabled.
```

Marketplace-installed plugins do **not** extract into `~/.claude/skills/`
— they live under
`~/.claude/plugins/cache/ai-research-skills/<plugin>/<version>/skills/<name>/`
and Claude Code discovers them via each plugin's
`.claude-plugin/plugin.json`. A bare `ls ~/.claude/skills/` does *not*
confirm a successful marketplace install — use `claude plugin list`.

Full per-plugin breakdown: [docs/install.md](docs/install.md) ·
Python / Zotero / Git not set up yet? Start with
[docs/setup-guide.md](docs/setup-guide.md).

<details>
<summary><b>I'd rather clone the repo</b> (contributors / debugging)</summary>

```bash
git clone https://github.com/WenyuChiou/ai-research-skills.git
cd ai-research-skills
```

This catalog is the **registry**, not a monorepo. Each plugin's source
code lives in its own repo:

- `github.com/WenyuChiou/research-hub` — 11 `research-workspace` skills
- `github.com/WenyuChiou/academic-writing-skills` — 1 skill
- `github.com/WenyuChiou/zotero-skills` — 1 skill
- `github.com/WenyuChiou/codex-delegate` — 1 skill
- `github.com/WenyuChiou/gemini-delegate-skill` — 1 skill

If you're hacking on a plugin, clone **its** source repo, not this
catalog. This catalog only maintains `marketplace.json`, docs, image
assets, and the catalog-side `CHANGELOG.md`.

</details>

---

## 2. Why this catalog exists

You probably know the AI-for-research pain points already. The five
below are the ones this catalog actually fixes — not the ones it
gestures at.

### P1 — "I keep re-explaining context to every new AI session"

You open a new Claude / ChatGPT session to continue yesterday's work,
and the model knows nothing about your research question, the
experiments you've already finished, your baselines, or the gap you
closed last week. You spend the first ten minutes re-typing all of it.
Tomorrow, again.

### P2 — "AI confidently cites papers that don't exist"

The model writes *"as Chen et al. (2024) demonstrated…"* — the paper
is not real. You catch it (this time). In a reviewer response, a
hallucinated citation is a desk-reject.

### P3 — "I've read 50 papers and still can't tell which gap is worth a thesis"

Three questions need structured answers: *(1) is the gap actually
still open? (2) is closing it a real contribution or a permutation of
existing work? (3) can I close it in the time I have?* Tools that
produce a one-paragraph "research gap summary" don't answer any of
them.

### P4 — "AI-written prose smells like AI"

*"Furthermore", "It is noteworthy that"*, hedged sentences with no
committed claim. Reviewers (and senior co-authors) catch the smell in
two paragraphs, and the manuscript drops in their priority list.

### P5 — "Switching Claude / Codex / Gemini wipes my state"

You design the prompt with Claude, hand it to Codex to scaffold the
code, switch to Gemini for the long-context paper synthesis. Each
switch costs five minutes of re-onboarding. The cross-AI handoff is
where real time disappears.

---

### Three design principles, applied across 15 skills

The catalog is arranged around three load-bearing ideas, not a feature
list:

| Principle | What it does | Solves |
|---|---|---|
| **1. Manifests** (`.research/`, `.paper/`) | Research state lives in checked-in YAML / Markdown files. A new AI session reads the manifest and re-onboards itself — you don't re-explain context. | P1, P5 |
| **2. Schemas with anti-leakage rules** | Every cross-skill artifact has a YAML schema. A claim with empty `evidence_artifacts` is **forced** to carry `status: gap` + a `gap_reason` — never `supported`. A topic candidate with `verdict: do-not-pursue` is structurally separated from `worth-pursuing` ones. Downstream tools refuse to ship overconfident output. | P2, P3, P4 |
| **3. Character-driven routing** | Mechanical bulk → Codex. Long-context / CJK → Gemini. Judgment / governance → Claude. The router (`research-hub-multi-ai`) writes a coordination file so each delegate reads its own brief, not the parent context. | P5 |

The 8-stage pipeline below is these three principles applied to a
real research workflow.

![15 AI skills mapped to 8 research workflow stages, with cross-cutting tools (codex-delegate, gemini-delegate, research-hub-multi-ai) usable at every stage](docs/img/pipeline-overview.png)

---

## 3. The pipeline — what each stage delivers to the next

Eight stages from *"I should read about X"* to *"the manuscript
shipped"*. Each stage's output is the next stage's input — the
handoff is mechanical, not vibes.

| # | Stage | Skill(s) | Output → next stage |
|---|---|---|---|
| 1 | **Discover literature** | `research-hub`, `paper-summarize` | `.bib` + per-paper Key Findings notes → Stage 2 |
| 2 | **Find the gap** | `gap-to-topic`, `literature-triage-matrix`, `notebooklm-brief-verifier`, `zotero-library-curator` | `topic_dossier.gaps.yml` (with `verdict`, `verdict_reason`) → Stage 3a |
| 3a | **Frame the RQ** | `research-design-helper` | `design_brief.md` (frontmatter `source: gaps.yml#G2`, `gap_verdict`) → Stage 3b + Stage 4 |
| 3b | **Plan the project** | `research-context-compressor`, `research-project-orienter` | `project_manifest.yml` (`provenance.from_gap`) → Stages 4–8 |
| 4 | **Build the model** | *cookbook* — `codex-delegate` for ≥5-file scaffold, Claude direct for ≤4-file or judgment work | code in your project repo (see [cookbook](docs/example-design-to-build.md)) → Stage 5 |
| 5 | **Run & validate** | `research-context-compressor`, `research-project-orienter` | `.research/` run manifests so future AI sessions skip the rescan → Stage 6 |
| 6 | **Visualise & interpret** | `codex-delegate`, `gemini-delegate` | figures + analysis scripts → Stage 7 |
| 7 | **Draft the manuscript** | `paper-memory-builder`, `academic-writing-skills` | `.paper/claims.yml` (with `status` enum + anti-leakage) → Stage 8 |
| 8 | **Submit + respond** | `academic-writing-skills`, `research-context-compressor` | reviewer-response.md, version-tagged manifests → done |

The cross-skill handoffs (Stage 2 → 3a → 3b → 8; Stage 7 → 8) are
documented as **YAML schemas**, not free text. A downstream skill can
refuse to process a malformed handoff — and does, when the schema
violation would otherwise propagate (e.g. `status: gap` claims with no
`gap_reason` are rejected at Stage 7).

**Cross-cutting (every stage):** `codex-delegate`, `gemini-delegate`,
`research-hub-multi-ai`. These three sit beside the pipeline, not on
it — any stage routes mechanical / long-context / multi-AI work
through them.

Full narrative + per-stage tool tables: [docs/pipeline.md](docs/pipeline.md).

---

## 4. Use it

### Pick by goal

If you'd rather not read the full pipeline above, jump in by your
immediate goal:

| Your immediate goal | Skills you'll use |
|---|---|
| **Find & compare literature** | `research-hub` + `literature-triage-matrix` |
| **Write or revise a paper** | `paper-memory-builder` + `academic-writing-skills` |
| **Manage a research project** | `research-design-helper` + `research-context-compressor` + `zotero-library-curator` |

> **Helping others adopt AI for research** (librarian / RA / advisor)?
> No install needed — share this README plus [docs/install.md](docs/install.md).

### Or, just describe what you want

Describe what you want in plain language — Claude Code matches your
phrasing to a skill. You don't need to remember skill names.

| When you say… | Skill that activates |
|---|---|
| "Compare these 5 papers by method, data, limitations" | `literature-triage-matrix` |
| "Is this gap worth a thesis? Walk me through the three gates" | `gap-to-topic` |
| "Walk me through my research design before I start coding" | `research-design-helper` |
| "Audit this paragraph for banned words and overclaim" | `academic-writing-skills` |

Full trigger map (15 rows): [docs/skill-directory.md](docs/skill-directory.md).
If auto-trigger picks the wrong skill, name it explicitly:
*"Use `literature-triage-matrix` to compare these 5 papers."*

### All 15 skills

<details>
<summary><b>From <code>research-hub</code> (11 skills)</b> — one install gets all</summary>

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) — search, ingest, organise papers across Zotero / Obsidian / NotebookLM. *(Stages 1, 2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) — comparison matrix across method, data, claim, limitation. *(Stage 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) — verify NotebookLM briefs against source bundles. *(Stage 2)*
- [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) — audit Zotero, propose cleanup (preview-only without `zotero-skills`). *(Stage 2)*
- [`gap-to-topic`](https://github.com/WenyuChiou/research-hub/blob/master/skills/gap-to-topic/SKILL.md) — 3-gate go/no-go decision dossier for a candidate thesis/proposal topic (open? a contribution? feasible?). Emits `.gaps.yml` for `research-design-helper` Stage 3a handoff. *(Stage 2)*
- [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) — Socratic dialog through RQ → mechanism → identifiability → validation → risk. Reads `.gaps.yml` to pre-fill segments 1 + 5; Stage 4 [cookbook](docs/example-design-to-build.md) reuses the produced `design_brief.md`. *(Stages 3a, 4)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) — `.research/` manifests so future AI sessions skip the rescan. *(Stages 3b, 5, 8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) — fast orientation memo from those manifests. *(Stages 3b, 5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) — character-driven routing across Claude / Codex / Gemini. *(Cross-cutting)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) — `.paper/claims.yml` + `.paper/figures.yml` (status enum, anti-leakage rule, file sentinels). *(Stage 7)*
- [`paper-summarize`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-summarize/SKILL.md) — fill per-paper Key Findings / Methodology / Relevance in both Obsidian and Zotero child notes after `research-hub auto`. *(Stage 1)*

</details>

<details>
<summary><b>Standalone repos (4 plugins)</b> — one plugin install each</summary>

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) — manuscript revision, claim-evidence audit (schema-aware against `.paper/claims.yml`), banned-word / humanize, journal format, reviewer response. *(Stages 7, 8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) — full Zotero CRUD, batch metadata, library maintenance. *(Stages 1, 2, 7)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) — Claude → Codex CLI handoff for code-heavy / mechanical work. *(Cross-cutting, also Stages 4, 6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) — Claude → Gemini CLI handoff for long-context, multilingual, or CJK work. *(Cross-cutting, also Stages 6, 7)*

</details>

### Time + cost expectations

Rough envelope from in-session use — adjust to your input size:

| Task | Typical wall time | Conversation turns | Notes |
|---|---|---|---|
| Compare 5 papers (`literature-triage-matrix`) | 1–3 min | 1–2 | Linear in paper count; 20 papers ≈ 5 min |
| 3-gate gap decision (`gap-to-topic`) | 5–15 min | 3–6 | Scales with candidate count + literature-recall depth |
| Banned-word audit on 1 paragraph (`academic-writing-skills`) | <1 min | 1 | Independent of manuscript size |
| Reviewer response (6 comments) (`academic-writing-skills`) | 3–8 min | 3–5 | Scales with comment depth + revision required |
| Audit 800-item Zotero library (`zotero-library-curator`) | 2–4 min | 1 | Read-only; library size matters less than tag diversity |
| Summarize 5 papers per cluster (`paper-summarize`) | 4–10 min | 1 | One LLM call per paper; rolls back per-paper on failure |

These are **maintainer-observed ranges**, not benchmark numbers. Your
LLM provider, network, library state, and prompt phrasing all affect
the actual time.

### ⚠ Back up Zotero before any CRUD

`zotero-library-curator` is read-only — it emits a preview report.
`zotero-skills` *can* write (merge duplicates, delete items, rebind
collections). **Always export a Zotero backup before letting any AI
modify your library**: Zotero → File → "Export Library…" → Zotero RDF.
The skills will not do this for you.

---

## 5. See what each skill produces

Every shipping skill has at least one worked-example file in
[`docs/examples.md`](docs/examples.md):

- Literature-review deliverables (Stages 1–2)
- Topic dossier with the 3-gate decision (Stage 2)
- Design brief with provenance to the dossier (Stage 3a)
- Project manifest with `provenance.from_gap` (Stage 3b)
- **Stage 4 cookbook** — two paths (Claude-direct for ≤4 files;
  `codex-delegate` for ≥5-file scaffold)
- Paper-memory `claims.yml` + `figures.yml` with the `status: gap`
  pattern + figure sentinels (Stage 7)
- Full literature-review pipeline output (everything composed)

Pick by stage above, or read [`docs/examples.md`](docs/examples.md) end
to end.

---

## 6. Compatibility

The 15 SKILL.md files conform to the
[agentskills.io](https://agentskills.io) open spec — the same format used
by ~35 agent runtimes.

| What | Status |
|---|---|
| 15 SKILL.md pass strict-minimum spec (`name` + `description`, ≤500 lines) | ✅ 15/15 spec-verified |
| Zero-edit portable across agentskills.io hosts | ✅ 11/14 |
| Needed cosmetic `<skill-root>` path edits (since landed) | 3/14 |
| End-to-end install verified on NousResearch/hermes-agent 0.13.0 | ✅ `literature-triage-matrix` — security scan SAFE, registered `enabled` |
| Inference loop on Hermes | ⚠ not tested (auth-gated; out of scope) |
| Other 34 listed agentskills.io hosts | not individually tested |

The `n/14` portability rows reflect the audit run 2026-05-10, when the
catalog had 14 skills; `gap-to-topic` (added 2026-05-21, the 15th) is
not yet portability-audited.

Calibrated audit + experiment transcripts:
[`.research/hermes-compatibility-audit.md`](.research/hermes-compatibility-audit.md).

For loading SKILL.md on Codex CLI / Gemini CLI / Cursor / Windsurf or
any generic-API client, see
[docs/install.md → Using these skills outside Claude Code](docs/install.md#using-these-skills-outside-claude-code).

---

## 7. Limitations

- Assembled and tested by one graduate-student researcher; not
  corpus-scale-validated.
- Domain bias toward water resources and agent-based modeling; not
  validated for social sciences, ML, or clinical writing.
- Behavioral correctness on real-world inputs is the source repo's
  responsibility, not this catalog's.
- Upstream URL liveness is not machine-checked; verified manually on PRs.
- No `claude plugin install` round-trip is asserted by CI; the
  marketplace registry is checked structurally, the actual install +
  trigger path is verified by the maintainer between releases (see
  [docs/verification.md](docs/verification.md) for what is and isn't
  covered).
- `zotero-skills` is shipped by two plugins simultaneously
  (`research-workspace` embeds an older copy alongside the canonical
  standalone `zotero-skills` plugin). A bare-name invocation of
  `Skill(skill="zotero-skills")` resolves silently to the
  `research-workspace` embedded copy. To reach the canonical
  standalone, use the plugin-qualified form
  `Skill(skill="zotero-skills:zotero-skills")`. See
  [docs/verification.md §2026-05-20](docs/verification.md#2026-05-20--phase-53b-end-to-end-verification)
  for the reproduction and the deferred fix.

The full design contract — including what is and is not machine-checked
— is in [docs/design-philosophy.md](docs/design-philosophy.md).

---

## License

MIT. Each skill is maintained in its canonical repo — this catalog is
the index, not a monorepo. Contributions welcome via issue or PR.
New-skill proposals → either `research-hub` (workflow integration) or
a standalone repo (deep, single-purpose CRUD).
