# Researcher Workflow Checklist

Use this checklist if you work like many researchers: papers live in Zotero,
notes live in Obsidian, source-grounded summaries come from NotebookLM, and
manuscript work happens in Word, LaTeX, or Markdown.

## Quick Tool Checklist

Check what you use now:

- [ ] Zotero for references, PDFs, tags, and collections.
- [ ] Obsidian for Markdown notes, project memory, and cluster dashboards.
- [ ] NotebookLM for source-grounded briefs, audio, mind maps, or Q&A.
- [ ] Word, LaTeX, or Markdown for manuscript drafts.
- [ ] Claude, Codex, or Gemini for AI-assisted research work.

Then install the matching skills below.

## If You Use Zotero + Obsidian

Install:

```bash
pip install research-hub-pipeline
research-hub install --platform claude-code
```

Use these skills:

- [research-hub](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md): find papers, ingest metadata, write Obsidian paper notes, maintain clusters.
- [literature-triage-matrix](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md): compare papers by method, data, claim, limitation, and relevance.
- [research-context-compressor](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md): create `.research/` manifests so AI sessions do not rescan the whole project.
- [research-project-orienter](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md): read `.research/` manifests and produce a fast orientation memo.

Add if needed:

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```

- [zotero-skills](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md): deep Zotero CRUD, batch cleanup, tags, collections, item edits, and PDF attachments.

## If You Use Obsidian + NotebookLM

Install:

```bash
pip install "research-hub-pipeline[playwright]"
research-hub install --platform claude-code
research-hub notebooklm login
```

Use these skills:

- [research-hub](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md): import local PDFs, DOCX, Markdown, TXT, and URLs into an Obsidian-backed workspace.
- [notebooklm-brief-verifier](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md): verify downloaded NotebookLM briefs against the source bundle.
- [literature-triage-matrix](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md): convert notes and briefs into a comparison matrix.

Use this workflow:

```text
local files -> research-hub import-folder -> Obsidian notes
Obsidian cluster -> NotebookLM bundle/upload/generate/download
downloaded brief -> notebooklm-brief-verifier
verified sources -> literature-triage-matrix
```

## If You Use Zotero + NotebookLM

Install:

```bash
pip install "research-hub-pipeline[playwright]"
research-hub install --platform claude-code
research-hub notebooklm login
```

Use these skills:

- [research-hub](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md): select papers from Zotero, create source bundles, upload to NotebookLM, and download outputs.
- [notebooklm-brief-verifier](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md): catch missed sources, unsupported claims, and contradictions.
- [zotero-skills](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md): use only when you need item-level Zotero edits beyond the research-hub workflow.

## If You Use All Three: Zotero + Obsidian + NotebookLM

Install `research-hub` first:

```bash
pip install "research-hub-pipeline[playwright]"
research-hub install --platform claude-code
research-hub notebooklm login
```

Core skills:

- [research-hub](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md): full loop from search to ingest to organize to NotebookLM.
- [literature-triage-matrix](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md): literature comparison table.
- [notebooklm-brief-verifier](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md): NotebookLM output verification.
- [research-context-compressor](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md): project memory for future AI sessions.
- [research-project-orienter](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md): fast project orientation.

Typical loop:

```text
discover papers -> Zotero collection
Zotero collection -> Obsidian paper notes
Obsidian cluster -> NotebookLM source bundle
NotebookLM brief -> verifier
verified sources -> literature matrix
literature matrix -> manuscript claims
```

## If You Are Writing A Paper

Install:

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills
```

Use these skills:

- [paper-memory-builder](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md): extract `.paper/claims.yml` and `.paper/figures.yml`.
- [academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md): revise manuscript prose, audit claim evidence, respond to reviewers, check figures and journal format.

Recommended manuscript workflow:

```text
manuscript + figures -> paper-memory-builder
.paper/claims.yml + .paper/figures.yml -> academic-writing-skills
revised manuscript -> reviewer response / submission checklist
```

## If You Use Multiple AI Assistants

Install one or both:

```bash
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill
```

Use these skills:

- [codex-delegate](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md): coding-heavy, repetitive, or many-file implementation work.
- [gemini-delegate](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md): long-context reading, bilingual or CJK writing, source synthesis, and second-opinion reviews.
- [research-hub-multi-ai](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md): decide how Claude, Codex, and Gemini should share research-hub work.

## Minimal Recommendations

- [ ] Most researchers: install `research-hub` and `academic-writing-skills`.
- [ ] Heavy Zotero users: add `zotero-skills`.
- [ ] Heavy coding users: add `codex-delegate`.
- [ ] Long-context or bilingual users: add `gemini-delegate`.
- [ ] NotebookLM users: always use `notebooklm-brief-verifier` before trusting a brief.
