# AI Research Skills

一個面向研究者的 AI skills 總目錄，依照「研究者實際的工作流程」排列——
從找第一篇文獻，一路到最後投稿與收尾。

語言版本：[English](README.md) | [繁中](README.zh-TW.md) | [Bilingual / 中英文對照](README.bilingual.md)

這個 repo 是 umbrella catalog，本身不放 skill 內容；每個 skill 在自己的
repo 維護，方便文件、測試、安裝指令集中管理：

- [`research-hub`](https://github.com/WenyuChiou/research-hub)：Zotero、Obsidian、NotebookLM、`.research/`、`.paper/`。
- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills)：論文修改、claim 審查、reviewer response。
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills)：深度 Zotero CRUD。
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate)：把寫程式的工作交給 Codex CLI。
- [`gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill)：把長 context / 中英文工作交給 Gemini CLI。

目標讀者：研究生、博士生、博士後、研究人員、研究工程師，以及任何在實際
研究流程中把 AI 拉進來一起工作的人。

## 適合誰

如果你想用 AI 處理以下任一件事，這個 catalog 適合你：

- 在 Zotero、Obsidian、NotebookLM 之間找文獻、整理文獻；
- 不重讀所有 PDF 也能比較文獻；
- 壓縮研究專案 context，讓未來 AI session 少花 token；
- 設計、執行、驗證模型或實驗；
- 寫論文、回覆 reviewer、準備投稿；
- 把 coding 或長 context 工作交給 Codex 或 Gemini。

不需要三個工具都用。`Zotero + Obsidian + NotebookLM` 任挑兩個，就已經
足以開始整個流程。

## Research Pipeline——找到你目前所在的階段

AI skills 真正派上用場的時機，是「對到正確的研究階段」。對到階段、裝對
skill，未來的 AI session 就不必每次重讀整個專案。

```text
1. 找文獻  →  2. 整理比較、找 gap  →  3. 框問題、做計畫  →  4. 設計與建模
        →  5. 執行、校正、驗證 (C&V)  →  6. 視覺化  →  7. 撰寫論文
        →  8. 投稿、回覆審查、收尾
```

> 大多數 skills 都住在 [`research-hub`](https://github.com/WenyuChiou/research-hub)
> 或 [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills)，
> 每個階段下方的「Lives in」會告訴你該 clone 哪個 repo。

### 1. 找文獻 (Discover literature)

> *「這個題目別人做過什麼？我該讀什麼？」*

常用工具：**Zotero · NotebookLM · Obsidian** *（目前沒有 OneNote 對應的
skill，請以 Obsidian 作為筆記層。）*

| Skill | 用途 |
|---|---|
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | 在 arXiv / Semantic Scholar / CrossRef / PubMed 搜尋論文，匯入 metadata，自動寫成 Obsidian 筆記。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) | research-hub pipeline 不夠時，做更深的 Zotero 加項、tag、去重、清理。 |

**Lives in：** `research-hub`（搜尋／匯入）· 獨立 repo `zotero-skills`。

### 2. 整理、比較文獻、找出 research gap

> *「研究 gap 在哪裡？哪 5 篇是真的關鍵？」*

常用工具：**Zotero collections · Obsidian clusters · NotebookLM briefs。**

| Skill | 用途 |
|---|---|
| [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | 不重讀每一篇 PDF，就能依 method、data、claim、limitation、relevance 比較。 |
| [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | 把 NotebookLM 的 brief 對回原始 source bundle，抓出漏掉的 source、沒根據的 claim、互相矛盾的描述。 |
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | 建立要餵進 matrix 的 Obsidian cluster 與 NotebookLM source bundle。 |

**Lives in：** `research-hub`（三個都是）。

### 3. 框定問題、做研究計畫

> *「我的 claim 是什麼？用什麼資料？接下來的計畫是什麼？」*

常用工具：**Obsidian project notes · 專案 repo 裡的 `.research/` manifests。**

| Skill | 用途 |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 寫出 `.research/project_manifest.yml`、`.research/experiment_matrix.yml`、`.research/data_dictionary.yml`，未來 AI session 不必重新掃整個 repo。 |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | 讀那些 manifests，幫你（或新的 AI session）快速產生 orientation 摘要。 |

**Lives in：** `research-hub`。

### 4. 設計與建立模型

> *「我需要什麼架構、什麼方程式、什麼 agents、什麼 prompt？」*

常用工具：**自己的 repo + IDE。**

目前 catalog 中沒有專門的 model design skill。最接近的選擇：

| Skill | 用途 |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | 把 scaffolding、batch edits、boilerplate、跨檔案 refactor 交給 Codex CLI；Claude 負責 review。 |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | 利用 Gemini 的長 context 做 design review、第二意見、讀大型參考 codebase。 |

**Lives in：** 獨立 repo `codex-delegate` 與 `gemini-delegate-skill`。

### 5. 執行實驗、校正與驗證 (C&V)

> *「跑出來的東西可重現、可檢查、可擴充嗎？跨長 session 能不能省 token？
> 能不能讓多個 AI 一起分工？」*

常用工具：**自己的 repo + 多個 AI CLI（Claude、Codex、Gemini）。**

| Skill | 用途 |
|---|---|
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | 決定哪些工作留在 Claude、哪些丟給 Codex（程式重）、哪些丟給 Gemini（長 context、中文），並規劃交接 prompt。 |
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | 反覆執行的 Codex 任務：sweep、regression test、修完 bug 的 verification。 |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 用 manifest 省 token，每次跑/檢查的 session 不必從零開始。 |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | 切換實驗、或休息幾天回來時，用便宜的方式重新進入狀況。 |

**Lives in：** `research-hub`（multi-ai、compressor、orienter）· 獨立 `codex-delegate`。

### 6. 視覺化與結果解讀

> *「這張圖到底在說什麼？我的 caption 寫對了嗎？」*

常用工具：**matplotlib / plotly 或你慣用的繪圖工具。**

目前 catalog 中沒有專門的視覺化 skill。最接近的選擇：

| Skill | 用途 |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | 產生或重構繪圖腳本（多張圖統一風格、批次重畫）。 |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | 利用長 context，讓圖與草稿 caption / 解讀段落配在一起。 |

**Lives in：** 獨立 repo `codex-delegate` 與 `gemini-delegate-skill`。

### 7. 論文撰寫與修改

> *「文字描述跟圖一致嗎？符合目標期刊嗎？讀起來像人寫的嗎？」*

常用工具：**Word · LaTeX · Markdown。**

| Skill | 用途 |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | 抽出 `.paper/claims.yml` 與 `.paper/figures.yml`，讓寫作工具看到的數字跟圖完全一致。 |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | 論文修改、claim-evidence audit、banned-word／humanize、figure-text 一致性、journal format 檢查。 |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | 長段重寫、中英文／CJK 草稿、文字風格的第二意見。 |

**Lives in：** `research-hub`（paper-memory-builder）· 獨立 `academic-writing-skills` · 獨立 `gemini-delegate-skill`。

### 8. 投稿、回覆審查、收尾

> *「我的 claim 站得住嗎？reviewer response 完整嗎？專案狀態有沒有為下
> 一個人（或半年後的自己）保留好？」*

常用工具：**期刊投稿系統 · 自己的 repo。**

| Skill | 用途 |
|---|---|
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | Reviewer response 表、pre-submission checklist、journal format 審查、rebuttal letter。 |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 把專案最終狀態凍結進 `.research/` manifests，讓未來 AI session（或未來的你）幾秒就能回到狀況。 |

**Lives in：** 獨立 `academic-writing-skills` · `research-hub`。

## 目前 Catalog 收錄的所有 Skills

下面列出本 catalog 引用的所有 skills，依照所在的 canonical repo 分類。
共 **11 個 skills**，每一個都至少對應到上方 pipeline 的一個階段。

**來自 [`research-hub`](https://github.com/WenyuChiou/research-hub)（7 個）：**

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md)：在 Zotero / Obsidian / NotebookLM 之間搜尋、匯入、整理論文。*(階段 1、2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)：依 method、data、claim、limitation 做比較表。*(階段 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md)：把 NotebookLM brief 對回 source bundle 做驗證。*(階段 2)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md)：用 `.research/` manifest 讓未來 AI session 不必重新掃 repo。*(階段 3、5、8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md)：讀那些 manifest，快速產生 orientation 摘要。*(階段 3、5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)：規劃 Claude / Codex / Gemini 之間的工作分配與交接。*(階段 5)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md)：產出 `.paper/claims.yml` 與 `.paper/figures.yml` 給寫作流程用。*(階段 7)*

**獨立 repo（4 個）：**

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md)：manuscript 修改、claim-evidence audit、banned-word／humanize、journal format、reviewer response。*(階段 7、8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md)：深度 Zotero CRUD、batch metadata、library maintenance。*(階段 1)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md)：把程式重的工作從 Claude 交給 Codex CLI。*(階段 4、5、6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md)：把長 context、多語、CJK 工作從 Claude 交給 Gemini CLI。*(階段 4、6、7)*

目前還沒有原生 skill 的階段：**(4) 模型設計** 與 **(6) 視覺化**——
最接近的替代方案是 `codex-delegate` 與 `gemini-delegate`，歡迎 contribution。

## 快速查找——按工具組合

如果你已經知道自己用什麼工具，可以直接看這張表：

| 你想做什麼 | 使用這個 skill | 安裝 |
|---|---|---|
| 連接 Zotero、Obsidian、NotebookLM | [`research-hub`](https://github.com/WenyuChiou/research-hub) | `pip install research-hub-pipeline`，再執行 `research-hub install --platform claude-code` |
| 做文獻比較表 | [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | 透過 `research-hub install` |
| 驗證 NotebookLM brief | [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | 透過 `research-hub install` |
| 準備 manuscript 給 AI 寫作／修改 | [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) + [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | 安裝 `research-hub`，並 clone `academic-writing-skills` |
| 修改論文或回覆 reviewer | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | `git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills` |
| 清理或編輯 Zotero library | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | `git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills` |
| 委派大量 coding 工作 | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | `git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate` |
| 委派長 context 或中英文工作 | [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill) | `git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill` |

研究者工作流清單見
[docs/researcher-workflow-checklist.md](docs/researcher-workflow-checklist.md)。
完整目錄見 [docs/skill-directory.md](docs/skill-directory.md)。
Machine-readable catalog 見 [catalog/skills.yml](catalog/skills.yml)。

## Skill Families 與邊界規則

| 類別 | Canonical repo | 負責範圍 |
|---|---|---|
| Research workspace | [`research-hub`](https://github.com/WenyuChiou/research-hub) | Zotero / Obsidian / NotebookLM workflow，`.research/` 與 `.paper/` 交接檔。 |
| Academic writing | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | manuscript 修改、claim-evidence audit、reviewer response、figure-text 一致性、期刊規範。 |
| Zotero operations | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | 深度 Zotero CRUD、batch metadata、library maintenance。 |
| Codex delegation | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | Claude → Codex CLI 的程式重工作交接。 |
| Gemini delegation | [`gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill) | Claude → Gemini CLI 的長 context、多語、CJK 工作交接。 |

特定模型的 governance、coupling、audit traces 應放在各自模型 repo，
不放在這個 umbrella catalog。

## 建議安裝順序

1. 用 Zotero / Obsidian / NotebookLM 任兩個 → 先裝 `research-hub`。
2. 要寫論文或改稿 → 裝 `academic-writing-skills`。
3. 需要深度整理 Zotero library → 加裝 `zotero-skills`。
4. 同時用多個 AI CLI → 加裝 `codex-delegate` 與 `gemini-delegate-skill`。

完整指令見 [docs/install.md](docs/install.md)。

## 狀態

這個 catalog 刻意保持輕量，指向已測試的 canonical repos，不變成 monorepo。

目前已驗證：

- `research-hub`：targeted skill tests passing。
- `academic-writing-skills`：integrity tests passing。

## License

MIT
