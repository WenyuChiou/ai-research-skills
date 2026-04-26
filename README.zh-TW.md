# AI Research Skills

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

> **研究者主導，AI 輔助。**
>
> 13 個 skills，依照實際研究 workflow 組織。

研究者導向的 13 個 AI skills 目錄——涵蓋從找第一篇論文到投稿最後一份
手稿的完整研究 workflow。

語言：[English](README.md) | [繁中](README.zh-TW.md)

![13 個 AI skills 對應 8 個研究階段，附 cross-cutting tools（codex-delegate、gemini-delegate、research-hub-multi-ai）每階段都可用](docs/img/pipeline-overview.zh-TW.png)

**你會拿到什麼：** 13 個 skills，涵蓋整個研究 workflow。9 個透過一次
安裝（`research-hub-pipeline`）就到位；4 個是獨立 clone。Per-skill
testing 細節見 [docs/verification.md](docs/verification.md)。

**適合誰：** 研究生、博士生、博士後、研究人員、研究工程師、圖書館員，
以及在實際研究流程中把 AI 拉進來的研究支援人員。

---

## 安裝

前置條件：Claude Code（https://claude.ai/code）。

Skills 是放在 `~/.claude/skills/` 底下的 Markdown 指令檔
（`SKILL.md`）。Claude Code 看到請求符合 skill 的描述就自動讀進來。

下面每一步是**累加的**——做到哪裡停都可以，已裝的就能用。每個 code
block 右上角會出現 GitHub 的複製按鈕。

### Step 1 — Marketplace plugin（從這裡開始）

請在 terminal 執行，不要在互動式 `/plugin` UI 裡跑：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills --scope user
```

**可以用的 skill：** `literature-triage-matrix`、`research-design-helper`、
`research-context-compressor`、`research-project-orienter`、
`paper-memory-builder`，加上 `notebooklm-brief-verifier`（Manual fallback 模式）。
13 個裡先得到 6 個，立刻可用。

### Step 2 — 寫論文

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills
```

**+ `academic-writing-skills`**——banned-word audit、claim-evidence
檢查、journal format、reviewer response。

### Step 3 — Zotero

先在 Zotero desktop（[下載](https://www.zotero.org/download/)）：Edit →
Settings → Advanced → 勾 **「Allow other applications on this computer
to communicate with Zotero」**。（Web API key 替代方案：看
[zotero-skills README](https://github.com/WenyuChiou/zotero-skills#readme)。）

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```

**+ `zotero-skills`**（完整 CRUD）和 **`zotero-library-curator`**
（audit + cleanup 提案；本身在第 1 步已經有，這步把它從 preview-only
變成「能真的執行修改」）。

### Step 4 — 多 CLI delegation

先裝 CLI binary（安裝指引在上游 README）：[Codex CLI](https://github.com/WenyuChiou/codex-delegate#readme)、
[Gemini CLI](https://github.com/WenyuChiou/gemini-delegate-skill#readme)。

```bash
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill
```

**+ `codex-delegate`**（把 token-heavy 的 code 工作交給 Codex CLI）、
**+ `gemini-delegate`**（長 context / CJK 輸出走 Gemini CLI）。

### Step 5 — 文獻 pipeline 自動化

```bash
pip install research-hub-pipeline
research-hub setup --persona researcher
```

Persona 選項：`researcher` / `analyst` / `humanities` / `internal`
——對應差異看 [docs/install.md](docs/install.md)。

**+ `research-hub`**（論文搜尋、ingest、NotebookLM 上傳）、
**`research-hub-multi-ai`**（delegation orchestration）。也會把第 1-2
步如果你跳過的補裝。

### 驗證

```bash
claude plugin list
ls ~/.claude/skills/
```

**其他注意：**

- `/plugin marketplace info` 顯示 `(no content)` 不是錯誤——`info`
  在 Claude Code 2.1.119 不是支援的 subcommand。
- 互動式 `/plugin install` 有時會改走 SSH，本機沒有 GitHub SSH key
  就會失敗；terminal 的 `claude plugin install ...` 走 HTTPS，沒有
  這個問題。
- 第 2-4 步用 `git clone`（不是 marketplace），因為這 4 個 repo 的
  `SKILL.md` 在 repo 根目錄，現行 Claude Code marketplace schema
  不接受這個 layout。詳情見
  [.claude-plugin/README.md](.claude-plugin/README.md)。

---

## 怎麼用

裝完之後，skills 會在你 Claude Code 的請求符合 skill 的描述時**自動觸發**。
**你不用記 skill 名字**——描述你想做什麼，Claude Code 會挑對的 skill。

### 範例：你怎麼說 → 哪個 skill 會啟動

| 你說... | 啟動的 skill |
|---|---|
| 「比較這 5 篇論文的 method、data、limitations」 | `literature-triage-matrix` |
| 「audit 我的 Zotero library 找重複跟 orphan tags」 | `zotero-library-curator` |
| 「在我開始 coding 之前先帶我走過研究 design」 | `research-design-helper` |
| 「驗證這份 NotebookLM brief 對應 source bundle」 | `notebooklm-brief-verifier` |
| 「從 manuscript draft 建一份 paper memory」 | `paper-memory-builder` |
| 「audit 我這段文字有沒有 banned words 跟 overclaim」 | `academic-writing-skills` |
| 「壓縮這個 project context 給未來 AI session 用」 | `research-context-compressor` |
| 「Orient 一下——這個 repo 在做什麼？」 | `research-project-orienter` |
| 「這個 task 是 code-heavy——交給 Codex」 | `codex-delegate` |
| 「把這份 brief 翻成繁中、需要長 context」 | `gemini-delegate` |

### Skill 沒自動觸發怎麼辦

如果 Claude Code 沒挑到對的 skill，明說 skill 名字：

> 「Use `literature-triage-matrix` to compare these 5 papers.」

---

## 找到你的起點

如果你想按目標挑 skill subset 而不是裝全部，對到你眼前的目標就好。

| 你眼前的目標 | 你會用到的 skills |
|---|---|
| **找文獻、比較文獻** | `research-hub` + `literature-triage-matrix` |
| **寫論文 / 改稿** | `paper-memory-builder` + `academic-writing-skills` |
| **管理研究專案 / Zotero library** | `research-design-helper` + `research-context-compressor` + `zotero-library-curator` |

> **協助別人用 AI 做研究**（圖書館員 / RA / 指導者）？不用裝——讀
> [docs/install.md](docs/install.md) 與 [docs/verification.md](docs/verification.md)
> 然後推薦就好。
>
> **沒對到你的目標？** 完整 8 階段研究 pipeline 在
> [docs/pipeline.zh-TW.md](docs/pipeline.zh-TW.md)，找到你的階段就裝
> 對應的 skill。

---

## 全部 13 個 Skills

<details>
<summary><b>來自 <code>research-hub</code>（9 個）</b>——一次安裝全部到位</summary>

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md)：在 Zotero / Obsidian / NotebookLM 之間搜尋、匯入、整理論文。*(階段 1、2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)：依 method、data、claim、limitation 做比較表。*(階段 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md)：把 NotebookLM brief 對回 source bundle 做驗證。*(階段 2)*
- [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md)：audit Zotero library，提整理計畫（preview only）。*(階段 2)*
- [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md)：Socratic 對話走過 RQ → mechanism → identifiability → validation → risk。*(階段 3a、4)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md)：用 `.research/` manifest 讓未來 AI session 不必重新掃 repo。*(階段 3b、5、8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md)：讀那些 manifest，快速產生 orientation 摘要。*(階段 3b、5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)：stage-agnostic、按 task 性質做 Claude / Codex / Gemini routing。*(Cross-cutting)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md)：產出 `.paper/claims.yml` 與 `.paper/figures.yml` 給寫作流程用。*(階段 7)*

</details>

<details>
<summary><b>獨立 repos（4 個）</b>——個別 git clone</summary>

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md)：manuscript 修改、claim-evidence audit、banned-word／humanize、journal format、reviewer response。*(階段 7、8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md)：完整 Zotero CRUD、batch metadata、library maintenance。*(階段 1、2、7)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md)：把程式重的工作從 Claude 交給 Codex CLI。*(Cross-cutting，也用於階段 6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md)：把長 context、多語、CJK 工作從 Claude 交給 Gemini CLI。*(Cross-cutting，也用於階段 6、7)*

</details>

### 一個 workflow 順序提醒

`research-project-orienter` 讀 `.research/` manifest 比較快；沒有的話
會 fallback scan `README.md` + `docs/`（比較慢）。要重複用 orientation
的話，先跑 `research-context-compressor` 產出 manifest。

---

## Testing

Per-skill testing 矩陣與可重現的 test-corpus 證據：
[docs/verification.md](docs/verification.md)。

---

## 狀態與授權

輕量 catalog。每個 skill 由各自的 canonical repo 維護——這個 catalog
是索引，不是 monorepo。

授權：MIT。歡迎 contribution——open issue 或 PR。新 skill 提案請鎖定
`research-hub`（workflow 整合）或一個獨立 repo（單一目的、深度的
CRUD）。
