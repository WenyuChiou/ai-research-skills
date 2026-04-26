# Install Guide

This repo is a catalog. Install skills from their canonical repositories.

For a complete inventory with direct skill links, see
[skill-directory.md](skill-directory.md).

## 1. research-hub

Use this if your workflow includes Zotero, Obsidian, NotebookLM, or any useful
two-tool subset.

```bash
pip install research-hub-pipeline
research-hub install --platform claude-code
research-hub install --platform cursor
research-hub install --platform codex
research-hub install --platform gemini
```

A fresh install writes 9 skills under `~/.claude/skills/`: `research-hub`,
`research-design-helper`, `research-context-compressor`,
`research-project-orienter`, `research-hub-multi-ai`,
`literature-triage-matrix`, `paper-memory-builder`,
`notebooklm-brief-verifier`, `zotero-library-curator`.

For NotebookLM browser automation:

```bash
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

First smoke test without NotebookLM:

```bash
research-hub auto "agent-based modeling" --no-nlm
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
