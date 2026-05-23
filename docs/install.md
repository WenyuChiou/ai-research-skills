# Install Guide

This repo is a portable `SKILL.md` catalog. Claude Code marketplace is the
fastest packaged install path, but the same `SKILL.md` files can also be
loaded by Codex CLI, Cursor, Gemini CLI, Hermes, OpenClaw, Windsurf, or a
generic API client.

Prerequisite: at least one AI host that can read Markdown context. Claude
Code users get marketplace install and auto-triggering; other hosts need to
point the model at the relevant `SKILL.md` explicitly.

> **New here?** If you don't have Claude Code, Python, or Zotero
> working yet, start with [**setup-guide.md**](setup-guide.md) — it
> walks through runtimes + plugins + Zotero local API end-to-end with
> verification commands at every step. This page assumes those prereqs
> are working and focuses on which plugin to install for which
> workflow.

For a complete inventory with direct skill links, see
[skill-directory.md](skill-directory.md).

## Choose an install path

| If you use... | Use this path | Verify with... |
|---|---|---|
| Claude Code | `claude plugin marketplace add` + `claude plugin install` | `claude plugin list` |
| Claude Code plus literature-pipeline automation | Marketplace install plus `pip install research-hub-pipeline` and `research-hub setup` | `claude plugin list` and a `research-hub auto ... --no-nlm` smoke test |
| Codex CLI / Cursor / Windsurf | Clone the canonical skill repo and load `SKILL.md` into the host's skills/rules directory, or inline it into the prompt | The host's own skill/rules discovery, or an explicit prompt smoke test |
| Gemini CLI / generic API client | Inline `SKILL.md` as prompt or system context | A prompt smoke test |
| Hermes | `hermes skills install <raw-SKILL.md-url>` | `hermes skills list`; only `literature-triage-matrix` is verified here on Hermes 0.13.0 |
| OpenClaw | Use a `SKILL.md` directory shape such as `~/.openclaw/skills/<skill>/SKILL.md` when your OpenClaw install supports it | Manual host discovery; this repo has not done release-grade OpenClaw verification yet |

### Claude Code marketplace fastest path

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
claude plugin list
```

### Windows cmd.exe

If you paste a multi-line block into `cmd.exe`, it may execute only the
first line. Run the commands one at a time, or use this single-line form:

```cmd
claude plugin marketplace add WenyuChiou/ai-research-skills && claude plugin marketplace update ai-research-skills && claude plugin install research-workspace@ai-research-skills --scope user && claude plugin list
```

`claude plugin list` verifies only Claude Code marketplace state. It does
not verify whether Codex, Cursor, Hermes, OpenClaw, or a generic API client
has loaded the `SKILL.md` files.

## 1. research-hub

Use this if your workflow includes Zotero, Obsidian, NotebookLM, or any useful
two-tool subset.

**Recommended (fresh install):**

```bash
pip install research-hub-pipeline
research-hub setup --persona researcher   # or: analyst | humanities | internal
```

`setup` is one interactive command that runs `init` + `install`, prompts for
the Zotero default collection (skipped on `analyst`), prompts for NotebookLM
login (skipped if you say no), and installs sample data. It is **idempotent**
— re-run any time to change persona or refresh skills.

Persona quick guide:

| Persona | Stack | Pick this if you... |
|---|---|---|
| `researcher` | Zotero + Obsidian + NotebookLM | want the full workflow |
| `analyst` | Obsidian + NotebookLM only (no Zotero) | don't use Zotero |
| `humanities` | Zotero + qualitative-friendly defaults | do interpretive / archival work, no code repo |
| `internal` | catalog reader, no install | help others adopt this stack |

**For other AI hosts:** `setup` auto-detects Claude Code; for Cursor / Codex /
Gemini hosts, point install at the right platform afterward when your
installed `research-hub-pipeline` version supports those platform adapters:

```bash
research-hub install --platform cursor
research-hub install --platform codex
research-hub install --platform gemini
```

OpenClaw and generic API clients should use the raw `SKILL.md` loading
path in [Using these skills outside Claude Code](#using-these-skills-outside-claude-code)
until this repo adds release-grade OpenClaw verification.

On the Claude Code default path, a fresh setup writes 11 skills under
`~/.claude/skills/`: `research-hub`, `research-design-helper`,
`research-context-compressor`, `research-project-orienter`,
`research-hub-multi-ai`, `literature-triage-matrix`,
`paper-memory-builder`, `paper-summarize`, `notebooklm-brief-verifier`,
`zotero-library-curator`, `gap-to-topic`.

*Note*: this Python-CLI path (`research-hub setup`) DOES extract skills
into `~/.claude/skills/`. The Claude Code marketplace path
(`claude plugin install …@ai-research-skills`) does NOT — those skills
live under `~/.claude/plugins/cache/…`. Both paths work; they just
land the SKILL.md files in different directories. See
[verification.md](verification.md) §2026-05-20 for the round-trip detail.

For NotebookLM browser automation (also handled by `setup` if you answer
yes when prompted):

```bash
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

First smoke test without NotebookLM:

```bash
research-hub auto "agent-based modeling" --no-nlm
```

### Already ran the bare `install` command?

```bash
# Was: research-hub install --platform claude-code
# This still works but only writes SKILL.md files (no persona, no Zotero
# default, no NotebookLM login). Re-run setup any time to onboard properly:
research-hub setup --persona researcher
```

### Upgrading from research-hub-pipeline ≤ 0.45

Older versions installed a skill named `knowledge-base/`. The canonical
name has been `research-hub/` since v0.46. Fresh installs no longer
write `knowledge-base/`, but a previous install may have left the old
directory behind.

If `~/.claude/skills/knowledge-base/` and `~/.claude/skills/research-hub/`
both exist, the legacy alias may double-trigger the skill router. The
`get_bundled_skill_path("knowledge-base")` alias emitted a
`DeprecationWarning` in `v0.45–0.69` and was removed in `v0.70+`. Safe
to remove the stale directory:

```bash
rm -rf ~/.claude/skills/knowledge-base
```

## 2. academic-writing-skills

**Canonical path** (Claude Code marketplace):

```bash
claude plugin install academic-writing-skills@ai-research-skills
```

<details>
<summary>Legacy alternative: manual <code>git clone</code> / raw <code>SKILL.md</code> checkout</summary>

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills
```

Project-level:

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills <project>/.claude/skills/academic-writing-skills
```

Use the manual path only when you need the SKILL.md outside Claude
Code (Codex CLI, Cursor, Hermes, etc.) — see *Using these skills
outside Claude Code* below.
</details>

## 3. zotero-skills

**Canonical path** (Claude Code marketplace):

```bash
claude plugin install zotero-skills@ai-research-skills
```

Use this only if you need deep Zotero operations beyond research-hub's
pipeline integration. **Note**: the `research-workspace` plugin
currently ships an embedded copy of `zotero-skills` from research-hub
that takes precedence by bare name — see `docs/verification.md`
§2026-05-20 for the workaround until the upstream collision is resolved.

<details>
<summary>Legacy alternative: manual <code>git clone</code></summary>

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```
</details>

## 4. codex-delegate

**Canonical path** (Claude Code marketplace):

```bash
claude plugin install codex-delegate@ai-research-skills
```

<details>
<summary>Legacy alternative: manual <code>git clone</code></summary>

```bash
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
```
</details>

## 5. gemini-delegate

**Canonical path** (Claude Code marketplace):

```bash
claude plugin install gemini-delegate@ai-research-skills
```

**Note**: the source repo is named `gemini-delegate-skill` but the
plugin name (and `Skill()` invocation name) is `gemini-delegate`. This
asymmetry is intentional — see [`CONTRIBUTING.md`](../CONTRIBUTING.md) §3.

<details>
<summary>Legacy alternative: manual <code>git clone</code></summary>

```bash
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate
```
</details>

## Suggested Minimal Set

For most researchers:

```text
research-workspace
academic-writing-skills
```

Add `zotero-skills` if you maintain a large Zotero library. Add delegation
skills if you actively use Codex or Gemini alongside Claude.

---

## Using these skills outside Claude Code

The `claude plugin install` path is Claude Code-specific. The portable
layer is each skill's `SKILL.md` plus any bundled `references/`, `scripts/`,
and workflow contracts. On non-Claude hosts you usually lose Claude Code's
auto-triggering, so name the skill explicitly in the prompt or put it in the
host's own skills/rules directory.

### 1. Get the source

```bash
git clone https://github.com/WenyuChiou/research-hub
git clone https://github.com/WenyuChiou/academic-writing-skills
git clone https://github.com/WenyuChiou/zotero-skills
git clone https://github.com/WenyuChiou/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill
```

Each repo's `SKILL.md` files live under `skills/<skill-name>/`. For
`research-hub`, that includes 11 skills; the other four repos have one
skill each.

### 2. Load per host

| Host | How to load `SKILL.md` | Status in this repo |
|---|---|---|
| **Codex CLI** | Put skills under a Codex skills directory when your Codex install supports it, or inline `SKILL.md` into `codex exec` / a task prompt. | Structurally portable; not marketplace-installed. |
| **Cursor / Windsurf** | Copy `SKILL.md` into `.cursor/rules/`, `~/.cursor/skills/`, or the editor's current rules/skills location. | Structurally portable; use editor-side discovery to verify. |
| **Gemini CLI** | Inline `SKILL.md` as prompt context, for example with `gemini -p`. | Structurally portable; no auto-trigger. |
| **Hermes Agent** | `hermes skills install <github-raw-url-to-SKILL.md>`. | `literature-triage-matrix` skill-load verified on Hermes 0.13.0; inference loop not tested. |
| **OpenClaw** | Use a directory such as `~/.openclaw/skills/<skill>/SKILL.md` when your OpenClaw install supports `SKILL.md`-style skills. | Structurally compatible target; not release-grade verified here. |
| **Generic API client** | Use `SKILL.md` as system/developer prompt context and include any referenced `references/` files needed for the task. | Portable prompt contract. |

### 3. Worked invocation examples

Replace `<repo>` with the absolute path to the cloned source repo.

**Codex CLI** — run `literature-triage-matrix` against five papers:

```bash
codex exec --sandbox workspace-write -C "$(pwd)" \
  "$(cat <repo>/skills/literature-triage-matrix/SKILL.md)

  Now produce a 9-column comparison matrix for the 5 papers in
  ./papers/. Write the output to .research/literature_matrix.md."
```

**Gemini CLI** — run an `academic-writing-skills` banned-word audit:

```bash
gemini -p "$(cat <repo>/skills/academic-writing-skills/SKILL.md)

Audit this paragraph for banned words and overclaim:
$(cat draft_paragraph.md)"
```

**Cursor / Windsurf** — copy a skill into project rules:

```bash
mkdir -p .cursor/rules
cp <repo>/skills/literature-triage-matrix/SKILL.md \
   .cursor/rules/literature-triage-matrix.md
```

**OpenClaw** — manual directory shape, pending release-grade verification:

```bash
mkdir -p ~/.openclaw/skills/literature-triage-matrix
cp <repo>/skills/literature-triage-matrix/SKILL.md \
   ~/.openclaw/skills/literature-triage-matrix/SKILL.md
```

### 4. Which skills make sense outside Claude Code

- Pure workflow skills such as `literature-triage-matrix`,
  `gap-to-topic`, `research-design-helper`, `research-context-compressor`,
  `research-project-orienter`, and `paper-memory-builder` work best across
  AI hosts because they define instructions and output contracts.
- `academic-writing-skills` works on any host that can read the manuscript
  and `.paper/` context.
- `notebooklm-brief-verifier` works anywhere in manual-fallback mode.
- `zotero-skills` needs an AI host that can call Zotero local or Web API
  tools; the `SKILL.md` itself is only the routing contract.
- `research-hub` and `research-hub-multi-ai` need the
  `research-hub-pipeline` Python CLI on PATH regardless of which AI host
  reads the skill.
- `codex-delegate` and `gemini-delegate` are most useful from Claude Code
  delegating outward; if you are already inside Codex or Gemini, use the
  target skill directly.
