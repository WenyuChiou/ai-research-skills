# Skill Directory

This page is the practical index. Start with the tool combination you already
use, then install the skill that matches your workflow.

For a checklist organized around Zotero, Obsidian, NotebookLM, manuscript work,
and AI assistants, see
[researcher-workflow-checklist.md](researcher-workflow-checklist.md).

## Choose By Tool Combination

| You use | Start with | Install |
|---|---|---|
| Zotero + Obsidian | `research-hub` | `pip install research-hub-pipeline` then `research-hub install --platform claude-code` |
| Obsidian + NotebookLM | `research-hub` | `pip install "research-hub-pipeline[playwright]"` then `research-hub install --platform claude-code` |
| Zotero + NotebookLM | `research-hub` | `pip install "research-hub-pipeline[playwright]"` then `research-hub install --platform claude-code` |
| Manuscript drafts | `academic-writing-skills` | `git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills` |
| Large Zotero library cleanup | `zotero-skills` | `git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills` |
| Coding-heavy AI handoff | `codex-delegate` | `git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate` |
| Long-context or bilingual handoff | `gemini-delegate` | `git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill` |

## Complete Skill Inventory

### research-hub

Repo: [research-hub](https://github.com/WenyuChiou/research-hub)

Install:

```bash
pip install research-hub-pipeline
research-hub install --platform claude-code
```

Optional NotebookLM automation:

```bash
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

| Skill | Use when | Direct skill link |
|---|---|---|
| `research-hub` | You want the AI to find papers, ingest sources, operate Zotero/Obsidian/NotebookLM, open dashboards, or maintain a vault. | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) |
| `research-hub-multi-ai` | You want Claude, Codex, Gemini, or another assistant to split research-hub work cleanly (cross-cutting routing). | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) |
| `research-design-helper` | You want to sharpen a research question through 5 Socratic segments (RQ → mechanism → identifiability → validation → risks) and produce `.research/design_brief.md`. | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) |
| `research-context-compressor` | You want to create `.research/` manifests so future AI sessions do not rescan the whole repo. | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) |
| `research-project-orienter` | The project already has `.research/` manifests and you want a fast orientation memo. | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) |
| `literature-triage-matrix` | You want a compact comparison table across a Zotero collection, Obsidian cluster, or manual paper list. | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) |
| `paper-memory-builder` | You want `.paper/claims.yml` and `.paper/figures.yml` before manuscript writing or revision. | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) |
| `notebooklm-brief-verifier` | You downloaded a NotebookLM brief and want to verify source coverage, unsupported claims, or contradictions. | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) |
| `zotero-library-curator` | You want to audit a Zotero library — find duplicate DOIs, orphan items, propose tag/collection cleanup. Read-only; defers writes to `zotero-skills`. | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) |

### academic-writing-skills

Repo: [academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills)

Install:

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills
```

| Skill | Use when | Direct skill link |
|---|---|---|
| `academic-writing-skills` | You need manuscript rewriting, claim-evidence audits, reviewer response, journal format checks, figure-text consistency, or pre-submission checks. | [SKILL.md](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) |

### zotero-skills

Repo: [zotero-skills](https://github.com/WenyuChiou/zotero-skills)

Install:

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```

| Skill | Use when | Direct skill link |
|---|---|---|
| `zotero-skills` | You need full Zotero CRUD: search, add, update, delete, collections, tags, notes, or PDF attachments. | [SKILL.md](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) |

### AI delegation skills

Repos: [codex-delegate](https://github.com/WenyuChiou/codex-delegate),
[gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill)

Install:

```bash
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill
```

| Skill | Use when | Direct skill link |
|---|---|---|
| `codex-delegate` | Coding work is repetitive, implementation-heavy, or spans many files, and Claude should supervise while Codex executes. | [SKILL.md](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) |
| `gemini-delegate` | Work is long-context, synthesis-heavy, bilingual/CJK-heavy, or needs a second-opinion review. | [SKILL.md](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) |

## Quick Recommendations

- New research workspace: install `research-hub`.
- Writing a paper: install `academic-writing-skills`.
- Cleaning Zotero: install `zotero-skills`.
- Using multiple AI CLIs: install `codex-delegate` and/or `gemini-delegate`.
- Publishing a workflow to collaborators: send this directory first, then point
  them to the exact skill repo they need.
