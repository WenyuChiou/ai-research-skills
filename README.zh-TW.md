# AI Research Skills

這是一個給研究者使用的 AI skills 總目錄，整理 Zotero、Obsidian、NotebookLM、論文寫作、以及 Codex/Gemini delegation 相關 skills。

這個 repo 是 umbrella catalog，不複製各 skill 的本體。每個 skill 仍由原本的 canonical repo 維護，避免文件、測試和安裝方式分叉。

## 適合誰

如果你想用 AI assistant 做以下事情，這個 catalog 適合你：

- 整理 Zotero、Obsidian、NotebookLM 之間的研究資料。
- 不重讀所有 PDF 也能比較文獻。
- 壓縮研究專案 context，讓未來 AI session 少花 token。
- 準備 manuscript、claim-evidence audit、reviewer response。
- 把 coding 或長 context 工作交給 Codex 或 Gemini。

你不需要三個工具都用。任選兩個就有價值：

```text
Zotero + Obsidian
Obsidian + NotebookLM
Zotero + NotebookLM
```

三個都用時，可以形成完整研究工作流。

## 從這裡開始

| 你想做什麼 | 使用這個 skill | 下載 / 安裝 |
|---|---|---|
| 連接 Zotero、Obsidian、NotebookLM | [`research-hub`](https://github.com/WenyuChiou/research-hub) | `pip install research-hub-pipeline`，再執行 `research-hub install --platform claude-code` |
| 做 literature review 比較表 | [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | 透過 `research-hub install` 安裝 |
| 驗證 NotebookLM brief | [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | 透過 `research-hub install` 安裝 |
| 準備 manuscript 給 AI 寫作/修改 | [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) + [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | 安裝 `research-hub`，並 clone `academic-writing-skills` |
| 修改論文或回覆 reviewer | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | `git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills` |
| 清理或編輯 Zotero library | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | `git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills` |
| 委派大量 coding 工作 | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | `git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate` |
| 委派長 context 或中英文工作 | [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill) | `git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill` |

完整目錄見 [docs/skill-directory.md](docs/skill-directory.md)。Machine-readable catalog 見 [catalog/skills.yml](catalog/skills.yml)。

## Skill Families

| 類別 | Canonical repo | 用途 |
|---|---|---|
| Research workspace | [`research-hub`](https://github.com/WenyuChiou/research-hub) | 讓 AI 操作 Zotero、Obsidian、NotebookLM、clusters、dashboard 和本地研究 artifacts。 |
| Academic writing | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | manuscript revision、claim-evidence audit、reviewer response、figure-text consistency。 |
| Zotero operations | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | 深度 Zotero CRUD、collections、tags、batch metadata、library maintenance。 |
| Codex delegation | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | 讓 Claude 把 coding-heavy 工作交給 Codex CLI。 |
| Gemini delegation | [`gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill) | 讓 Claude 把長 context、多語言或中文重的工作交給 Gemini CLI。 |

## 建議安裝順序

1. 如果你用 Zotero、Obsidian、NotebookLM 任兩個，先裝 `research-hub`。
2. 如果你用 AI 寫論文或改稿，裝 `academic-writing-skills`。
3. 如果你需要深度整理 Zotero library，裝 `zotero-skills`。
4. 如果你同時使用多個 AI CLI，裝 `codex-delegate` 和 `gemini-delegate-skill`。

安裝指令見 [docs/install.md](docs/install.md)。

## 收錄內容

### Research workspace skills

來自 `research-hub`：

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md)
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md)
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md)
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md)
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md)

這些 skills 負責文獻工作流、Obsidian cluster notes、NotebookLM brief verification，以及 `.research/` / `.paper/` context files。

### Academic writing skill

來自 `academic-writing-skills`：

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md)

負責 manuscript structure、claim-evidence audit、reviewer response、journal format checks、figure-text consistency、pre-submission checks。

### Zotero and delegation skills

獨立 repo：

- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md)
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md)
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md)

這些不放進 `research-hub`，因為它們處理的是不同層次的工作。

## 邊界規則

- Zotero / Obsidian / NotebookLM workflow skills 放在 `research-hub`。
- 論文寫作和審稿回覆放在 `academic-writing-skills`。
- 深度 Zotero CRUD 放在 `zotero-skills`。
- AI CLI delegation 放在 `codex-delegate` 和 `gemini-delegate-skill`。
- 特定模型的 governance、coupling、audit traces 應放在各自模型 repo，不放在這個 umbrella catalog。

## 推廣文章角度

> 不要每次都叫 AI 重讀你的研究專案，給它 skills。

核心訊息：

- Zotero 管 references。
- Obsidian 管 notes 和 project memory。
- NotebookLM 做 source-grounded briefs。
- AI skills 把這些工作流接起來，減少重複讀 context。

見 [docs/public-post-outline.md](docs/public-post-outline.md)。

## 狀態

這個 catalog 刻意保持輕量。它指向已測試的 canonical repos，不變成 monorepo。

目前已驗證：

- `research-hub`：targeted skill tests passing。
- `academic-writing-skills`：integrity tests passing。

## License

MIT
