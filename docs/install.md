# Install Guide

This repo is a catalog. Install skills from their canonical repositories.

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

For NotebookLM browser automation:

```bash
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

First smoke test without NotebookLM:

```bash
research-hub auto "agent-based modeling" --no-nlm
```

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
