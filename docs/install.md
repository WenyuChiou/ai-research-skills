# Install Guide

This repo is a catalog. Install skills from their canonical repositories.

Prerequisite: [Claude Code](https://claude.ai/code) (or Codex CLI / Cursor /
Gemini CLI). All catalogued skills activate inside an AI conversation.

For a complete inventory with direct skill links, see
[skill-directory.md](skill-directory.md).

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
Gemini hosts, point install at the right platform afterward:

```bash
research-hub install --platform cursor
research-hub install --platform codex
research-hub install --platform gemini
```

A fresh setup writes 9 skills under `~/.claude/skills/`: `research-hub`,
`research-design-helper`, `research-context-compressor`,
`research-project-orienter`, `research-hub-multi-ai`,
`literature-triage-matrix`, `paper-memory-builder`,
`notebooklm-brief-verifier`, `zotero-library-curator`.

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

Older versions installed a skill named `knowledge-base/`. The current
canonical name is `research-hub/` (same workflow). Fresh installs no
longer write `knowledge-base/`, but a previous install of yours may have
left the old directory behind.

If `~/.claude/skills/knowledge-base/` exists *and* `~/.claude/skills/research-hub/`
exists, the legacy alias may double-trigger the skill router. Safe to
remove:

```bash
rm -rf ~/.claude/skills/knowledge-base
```

Calling code that still references `get_bundled_skill_path("knowledge-base")`
keeps working in this version but emits a `DeprecationWarning`; the alias is
slated for removal in research-hub-pipeline v0.70.

## 2. academic-writing-skills

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills
```

Project-level install:

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills <project>/.claude/skills/academic-writing-skills
```

## 3. zotero-skills

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```

Use this only if you need deep Zotero operations beyond research-hub's pipeline
integration.

## 4. codex-delegate

```bash
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
```

## 5. gemini-delegate-skill

```bash
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill
```

## Suggested Minimal Set

For most researchers:

```text
research-hub
academic-writing-skills
```

Add `zotero-skills` if you maintain a large Zotero library. Add delegation
skills if you actively use Codex or Gemini alongside Claude.
