# Skill 目錄

實用 index——從你已經在用的工具組合開始，再裝對應的 skill。
英文版：[skill-directory.md](skill-directory.md)。

按工具組合 / 寫稿 / AI assistant 找對應 skill 的 checklist：
[researcher-workflow-checklist.zh-TW.md](researcher-workflow-checklist.zh-TW.md)。

## 按你的工具組合挑

| 你用 | 從這個開始 | 安裝 |
|---|---|---|
| Zotero + Obsidian | `research-hub` | `claude plugin install research-workspace@ai-research-skills`，然後 `pip install research-hub-pipeline` + `research-hub setup` |
| Obsidian + NotebookLM | `research-hub` | 同上，setup 時選 `analyst` persona |
| Zotero + NotebookLM | `research-hub` | 同上，setup 時選 `researcher` persona |
| 人文 / 質性研究（Zotero、不寫 code） | `research-hub` | 同上，setup 時選 `humanities` persona |
| 寫論文 | `academic-writing-skills` | `claude plugin install academic-writing-skills@ai-research-skills` |
| 大型 Zotero library 整理 | `zotero-skills` | `claude plugin install zotero-skills@ai-research-skills` |
| Code-heavy AI handoff | `codex-delegate` | `claude plugin install codex-delegate@ai-research-skills` |
| 長 context / 雙語 handoff | `gemini-delegate` | `claude plugin install gemini-delegate@ai-research-skills` |

## 完整 skill 清單

### research-hub plugin（research-workspace）

Repo：[research-hub](https://github.com/WenyuChiou/research-hub)

安裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
# 想要 CLI（pipeline 自動化）：
pip install research-hub-pipeline
research-hub setup
```

`setup` 是互動式——自動偵測 Claude Code、會問你 Zotero default
collection（`analyst` 略過）、會問你要不要登入 NotebookLM。

選用的 NotebookLM 自動化（也可以在 setup 時答 yes）：

```bash
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

| Skill | 何時用 | SKILL.md |
|---|---|---|
| `research-hub` | 想讓 AI 找論文、ingest source、操作 Zotero/Obsidian/NotebookLM、開 dashboard、維護 vault。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) |
| `research-hub-multi-ai` | 想把 research-hub 工作分給 Claude / Codex / Gemini / 其他 assistant 做（cross-cutting routing）。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) |
| `research-design-helper` | 想用 5 段 Socratic 對話 sharpen 研究問題（RQ → mechanism → identifiability → validation → risks），產出 `.research/design_brief.md`。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) |
| `research-context-compressor` | 想產出 `.research/` manifest，未來 AI session 就不必重掃整個 repo。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) |
| `research-project-orienter` | repo 已經有 `.research/` manifest，想快速產 orientation 摘要。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) |
| `literature-triage-matrix` | 想對 Zotero collection、Obsidian cluster 或手動論文清單做緊湊比較表。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) |
| `paper-memory-builder` | 想在寫稿 / 修稿前產出 `.paper/claims.yml` 跟 `.paper/figures.yml`。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) |
| `notebooklm-brief-verifier` | 下載了 NotebookLM brief，想 verify source 涵蓋、未根據的 claim、矛盾敘述。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) |
| `zotero-library-curator` | 想 audit Zotero library——找重複 DOI、orphan item、提整理計畫。Read-only；寫操作丟給 `zotero-skills`。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) |

### academic-writing-skills

Repo：[academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills)

安裝：

```bash
claude plugin install academic-writing-skills@ai-research-skills
```

| Skill | 何時用 | SKILL.md |
|---|---|---|
| `academic-writing-skills` | 需要 manuscript 重寫、claim-evidence audit、reviewer response、journal format 檢查、figure-text 一致性、submission 前審查。 | [SKILL.md](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) |

### zotero-skills

Repo：[zotero-skills](https://github.com/WenyuChiou/zotero-skills)

安裝：

```bash
claude plugin install zotero-skills@ai-research-skills
```

| Skill | 何時用 | SKILL.md |
|---|---|---|
| `zotero-skills` | 需要對 Zotero 做完整 CRUD：search、add、update、delete、collection、tag、note、PDF attachment。 | [SKILL.md](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) |

### AI delegation skills

Repo：[codex-delegate](https://github.com/WenyuChiou/codex-delegate)、
[gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill)

安裝：

```bash
claude plugin install codex-delegate@ai-research-skills
claude plugin install gemini-delegate@ai-research-skills
```

| Skill | 何時用 | SKILL.md |
|---|---|---|
| `codex-delegate` | Coding 工作 token 重、機械性、跨多檔案，Claude 督導、Codex 實際執行。 | [SKILL.md](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) |
| `gemini-delegate` | 工作是長 context、synthesis-heavy、雙語 / CJK 重，或需要 second-opinion review。 | [SKILL.md](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) |

## 快速建議

- 新研究 workspace：先裝 `research-hub`（research-workspace plugin）。
- 寫論文：裝 `academic-writing-skills`。
- 整理 Zotero：裝 `zotero-skills`。
- 多 AI CLI 並用：裝 `codex-delegate` 跟 / 或 `gemini-delegate`。
- 想推給合作者：先送他這份目錄，再指出他需要哪個 skill。
