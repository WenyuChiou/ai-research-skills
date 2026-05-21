# AI Research Skills

> 14 Claude Code skills for research workflows — literature triage, research
> design, project context, manuscript writing, multi-AI delegation.

Languages: [English](README.md) | [繁中](README.zh-TW.md) ·
[See what each skill produces →](docs/examples.md) ·
[Glossary](docs/glossary.md)

<sub><a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a> <a href=".research/hermes-compatibility-audit.md"><img alt="agentskills.io spec compliant" src="https://img.shields.io/badge/agentskills.io-spec_compliant-2DA89C"></a> <a href=".research/hermes-compatibility-audit.md"><img alt="Hermes 0.13.0 skill-load verified" src="https://img.shields.io/badge/Hermes_0.13.0-skill--load_verified-2DA89C"></a></sub>

![14 AI skills mapped to research workflow stages, with cross-cutting tools (codex-delegate, gemini-delegate, research-hub-multi-ai) usable at every stage](docs/img/pipeline-overview.png)

---

## What is this

5 plugins in one Claude Code marketplace, 14 skills total. Built for
graduate students, PhDs, postdocs, and research support staff running real
research projects with AI in the loop.

Skills are [agentskills.io](https://agentskills.io)-compliant Markdown files
— they auto-trigger inside Claude Code from your phrasing, and also load
into Codex CLI / Gemini CLI / Cursor / Windsurf / Hermes (see
[Compatibility](#compatibility)).

> 📚 Part of the [agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
> — featured in §13-14 (research workflows).

---

## Install

Prerequisite: [Claude Code](https://claude.ai/code). If you don't have
Python / Zotero / Git working yet, start with
[**docs/setup-guide.md**](docs/setup-guide.md).

**If you only have Claude Code** (no Python / Zotero / Codex / Gemini
CLI), 7 of the 14 skills are pure-reasoning and work immediately
after Step 1 + Step 2 below: 6 `research-workspace` skills —
`literature-triage-matrix`, `research-design-helper`,
`research-context-compressor`, `research-project-orienter`,
`paper-memory-builder`, `research-hub-multi-ai` (routing guidance is
useful even though the Codex / Gemini handoffs it prescribes won't
execute without those CLIs) — plus `academic-writing-skills`. The
other 7 skills wrap external tools (Zotero local API, NotebookLM,
the `research-hub-pipeline` Python CLI, Codex CLI, Gemini CLI) and
need their per-tool setup. Full breakdown:
[docs/install.md](docs/install.md).

Each step is **additive** — stop after any step and use what you've
installed.

```bash
# 1. Marketplace + 10 research-hub skills (6 are immediately usable, pure reasoning)
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills

# 2. Manuscript work
claude plugin install academic-writing-skills@ai-research-skills

# 3. Zotero (enable local API in Zotero desktop first — see docs/setup-guide.md §C)
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

External prereqs (Zotero local API, Codex / Gemini CLI binaries) still
need their manual steps. Full per-plugin breakdown:
[docs/install.md](docs/install.md).

**Verify**:

```bash
claude plugin list
# expected: 5 plugins, each ending in @ai-research-skills, each marked ✔ enabled.
```

Marketplace-installed plugins do **not** extract into `~/.claude/skills/`
— they live under `~/.claude/plugins/cache/ai-research-skills/<plugin>/<version>/skills/<name>/`
and are discovered by Claude Code via each plugin's `.claude-plugin/plugin.json`.
A bare `ls ~/.claude/skills/` does not confirm a successful marketplace
install. Use `claude plugin list` for that. (See
[docs/verification.md](docs/verification.md) §2026-05-20 for the
end-to-end install + skill-trigger verification record.)

---

## How to use

Describe what you want in plain language — Claude Code matches your
phrasing to a skill. You don't need to remember skill names.

| When you say... | Skill that activates |
|---|---|
| "Compare these 5 papers by method, data, limitations" | `literature-triage-matrix` |
| "Audit my Zotero library for duplicates and orphan tags" | `zotero-library-curator` |
| "Walk me through my research design before I start coding" | `research-design-helper` |
| "Verify this NotebookLM brief against the source bundle" | `notebooklm-brief-verifier` |
| "Audit this paragraph for banned words and overclaim" | `academic-writing-skills` |
| "Build a point-by-point reviewer response" | `academic-writing-skills` |
| "Compress this project context for future AI sessions" | `research-context-compressor` |
| "This task is code-heavy — delegate to Codex" | `codex-delegate` |
| "Translate this brief into 繁中 with long context" | `gemini-delegate` |

If auto-trigger picks the wrong skill, name it explicitly:
*"Use `literature-triage-matrix` to compare these 5 papers."*

### Pick by goal

| Your immediate goal | Skills you'll use |
|---|---|
| **Find & compare literature** | `research-hub` + `literature-triage-matrix` |
| **Write or revise a paper** | `paper-memory-builder` + `academic-writing-skills` |
| **Manage a research project** | `research-design-helper` + `research-context-compressor` + `zotero-library-curator` |

> **Helping others adopt AI for research** (librarian / RA / advisor)?
> No install needed — share this README plus [docs/install.md](docs/install.md).

Full mapping: [docs/skill-directory.md](docs/skill-directory.md) ·
Pipeline-stage view: [docs/pipeline.md](docs/pipeline.md) ·
Deliverable samples: [docs/examples.md](docs/examples.md).

### Time + cost expectations

Rough envelope from in-session use — adjust to your input size:

| Task | Typical wall time | Conversation turns | Notes |
|---|---|---|---|
| Compare 5 papers (`literature-triage-matrix`) | 1–3 min | 1–2 | Linear in paper count; 20 papers ≈ 5 min |
| Banned-word audit on 1 paragraph (`academic-writing-skills`) | <1 min | 1 | Independent of manuscript size |
| Reviewer response (6 comments) (`academic-writing-skills`) | 3–8 min | 3–5 | Scales with comment depth + revision required |
| Audit 800-item Zotero library (`zotero-library-curator`) | 2–4 min | 1 | Read-only; library size matters less than tag diversity |
| Summarize 5 papers per cluster (`paper-summarize`) | 4–10 min | 1 | One LLM call per paper; rolls back per-paper on failure |

These are **maintainer-observed ranges**, not benchmark numbers. Your
LLM provider, network, library state, and prompt phrasing all affect
the actual time. Bring a cup of coffee.

### ⚠️ Back up before any Zotero CRUD

`zotero-library-curator` is read-only — it emits a preview report.
`zotero-skills` *can* write (merge duplicates, delete items, rebind
collections). **Always export a Zotero backup before letting any AI
modify your library**: Zotero → File → "Export Library…" → Zotero RDF.
The skills will not do this for you.

---

## Compatibility

The 14 SKILL.md files conform to the
[agentskills.io](https://agentskills.io) open spec — the same format used
by ~35 agent runtimes.

| What | Status |
|---|---|
| 14 SKILL.md pass strict-minimum spec (`name` + `description`, ≤500 lines) | ✅ 14/14 verified |
| Zero-edit portable across agentskills.io hosts | ✅ 11/14 |
| Needed cosmetic `<skill-root>` path edits (since landed) | 3/14 |
| End-to-end install verified on NousResearch/hermes-agent 0.13.0 | ✅ `literature-triage-matrix` — security scan SAFE, registered `enabled` |
| Inference loop on Hermes | ⚠ not tested (auth-gated; out of scope) |
| Other 34 listed agentskills.io hosts | not individually tested |

Calibrated audit + experiment transcripts:
[`.research/hermes-compatibility-audit.md`](.research/hermes-compatibility-audit.md).

For loading SKILL.md on Codex CLI / Gemini CLI / Cursor / Windsurf or any
generic-API client, see
[docs/install.md → Using these skills outside Claude Code](docs/install.md#using-these-skills-outside-claude-code).

---

## All 14 skills

> `*(Stages X, Y)*` tags below refer to research-workflow stages 1–8 —
> see [`docs/pipeline.md`](docs/pipeline.md) for the diagram and
> [`docs/glossary.md`](docs/glossary.md) §Phase numbers for the
> stage-by-stage breakdown.

<details>
<summary><b>From <code>research-hub</code> (10 skills)</b> — one install gets all</summary>

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) — search, ingest, organise papers across Zotero / Obsidian / NotebookLM. *(Stages 1, 2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) — comparison matrix across method, data, claim, limitation. *(Stage 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) — verify NotebookLM briefs against source bundles. *(Stage 2)*
- [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) — audit Zotero, propose cleanup (preview-only without `zotero-skills`). *(Stage 2)*
- [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) — Socratic dialog through RQ → mechanism → identifiability → validation → risk. *(Stages 3a, 4)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) — `.research/` manifests so future AI sessions skip the rescan. *(Stages 3b, 5, 8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) — fast orientation memo from those manifests. *(Stages 3b, 5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) — character-driven routing across Claude / Codex / Gemini. *(Cross-cutting)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) — `.paper/claims.yml` and `.paper/figures.yml` for manuscript work. *(Stage 7)*
- [`paper-summarize`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-summarize/SKILL.md) — fill per-paper Key Findings / Methodology / Relevance in both Obsidian and Zotero child notes after `research-hub auto`. *(Stage 2)*

</details>

<details>
<summary><b>Standalone repos (4 plugins)</b> — one plugin install each</summary>

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) — manuscript revision, claim-evidence audit, banned-word / humanize, journal format, reviewer response. *(Stages 7, 8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) — full Zotero CRUD, batch metadata, library maintenance. *(Stages 1, 2, 7)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) — Claude → Codex CLI handoff for code-heavy work. *(Cross-cutting, also Stage 6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) — Claude → Gemini CLI handoff for long-context, multilingual, or CJK work. *(Cross-cutting, also Stages 6, 7)*

</details>

Per-skill testing matrix + reproducible test-corpus artifacts:
[docs/verification.md](docs/verification.md).

---

## Limitations

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

MIT. Each skill is maintained in its canonical repo — this catalog is the
index, not a monorepo. Contributions welcome via issue or PR. New-skill
proposals → either `research-hub` (workflow integration) or a standalone
repo (deep, single-purpose CRUD).
