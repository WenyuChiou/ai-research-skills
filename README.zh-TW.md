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

## 找到你的起點

對到你眼前的目標。一個指令裝完，其他等你需要再說。

| 你眼前的目標 | 你會用到的 skills | 一行 install | 時間 |
|---|---|---|---|
| **找文獻、比較文獻** | `research-hub` + `literature-triage-matrix` | `research-hub setup --persona researcher` | ~10 分鐘 |
| **寫論文 / 改稿** | `paper-memory-builder` + `academic-writing-skills` | 上面那行 + `git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills` | ~15 分鐘 |
| **管理研究專案 / Zotero library** | `research-design-helper` + `research-context-compressor` + `zotero-library-curator` | `research-hub setup --persona researcher` | ~20 分鐘 |

> **協助別人用 AI 做研究**（圖書館員 / RA / 指導者）？不用裝——讀
> [docs/install.md](docs/install.md) 與 [docs/verification.md](docs/verification.md)
> 然後推薦就好。
>
> **沒對到你的目標？** 下方完整 pipeline 列出 8 個研究階段，找到你的
> 階段就裝對應的 skill。

---

<details>
<summary><h2>完整研究 pipeline（點開展開）</h2></summary>

研究專案的 8 個階段，配上每個階段適用的 skill。這是完整版 reference——
大部分使用者用上面的「找到你的起點」就夠了，不必讀這段。

```text
1. 找文獻  →  2. 整理比較、找 gap  →  3a. 框問題  →  3b. 寫計畫
        →  4. 設計與建模  →  5. 執行、校正、驗證 (C&V)  →  6. 視覺化
        →  7. 撰寫論文  →  8. 投稿、回覆審查、收尾
```

有 3 個 skills 不屬於特定階段——它們的觸發條件是 **task 性質**，不是
pipeline 位置。見下方 **Cross-cutting tools**。

### 1. 找文獻

> *「這個題目別人做過什麼？我該讀什麼？」*

常用工具：**Zotero · NotebookLM · Obsidian** *（目前沒有 OneNote 對應的
skill，請以 Obsidian 作為筆記層。）*

| Skill | 用途 |
|---|---|
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | 在 arXiv / Semantic Scholar / CrossRef / PubMed 搜尋論文，匯入 metadata，自動寫成 Obsidian 筆記。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) | research-hub pipeline 不夠時，做更深的 Zotero 加項、tag、去重、清理。 |

### 2. 整理、比較文獻、找出 research gap

> *「研究 gap 在哪裡？哪 5 篇是真的關鍵？」*

| Skill | 用途 |
|---|---|
| [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | 不重讀每一篇 PDF，就能依 method、data、claim、limitation、relevance 比較。 |
| [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | 把 NotebookLM 的 brief 對回原始 source bundle，抓出漏掉的 source、沒根據的 claim、互相矛盾的描述。 |
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) | 建立要餵進 matrix 的 Obsidian cluster 與 NotebookLM source bundle。 |
| [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) *(optional)* | 比較前先 audit Zotero——找出重複 DOI、orphan items、提出 tag/collection 整理計畫。**Read-only**。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) *(optional)* | 真的執行 curator 提出來的整理動作——對 Zotero items 完整 CRUD。 |

### 3a. 框問題

> *「我的研究問題夠不夠 sharp？可不可以證偽？」*

一個 Socratic 對話夥伴，用結構化的提問逼你把原本含糊的東西講清楚。

| Skill | 用途 |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | 引導你走過 5 段：研究問題 sharpen → expected mechanism → identifiability check → validation plan → risk register，產出 `.research/design_brief.md`。 |

### 3b. 寫計畫 artifact（讓 AI 幫你記住）

> *「我的 claim 是什麼？用什麼資料？接下來的計畫是什麼？」*

3a 把問題框定後，下面這些 skill 把計畫存成 machine-readable manifest，
之後的 AI session 不需要重讀整個 repo。

| Skill | 用途 |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 寫出 `.research/project_manifest.yml`、`experiment_matrix.yml`、`data_dictionary.yml`。如果 3a 已經產出 `design_brief.md` 也會一起收進來。 |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | 讀那些 manifest，幫你（或新的 AI session）快速產生 orientation 摘要。 |

### 4. 設計與建立模型

> *「我需要什麼架構、什麼方程式、什麼 agents、什麼 prompt？」*

把 3a 產出的 `design_brief.md` 讀回來當 model spec，再產生
implementation scaffolding。

| Skill | 用途 |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | 跟 3a 同一個 skill——準備把「要建什麼模型」翻成「怎麼建」時，重新讀 `.research/design_brief.md` 對照。 |

實作 scaffolding（test harness、繪圖、batch edits）和大型 reference
codebase 的 design review，請用下方 **Cross-cutting tools** 的
`codex-delegate` 與 `gemini-delegate`。

### 5. 執行實驗、校正與驗證 (C&V)

> *「跑出來的東西可重現、可檢查、可擴充嗎？跨長 session 能不能省 token？」*

| Skill | 用途 |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 用 manifest 省 token，每次跑/檢查的 session 不必從零開始。 |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | 切換實驗、或休息幾天回來時，用便宜的方式重新進入狀況。 |

反覆執行的 sweep、regression test、修完 bug 的 verification 這類
token 重的工作，請用下方 **Cross-cutting tools**——`codex-delegate`
做 code-heavy 的執行；`research-hub-multi-ai` 規劃 Claude / Codex /
Gemini 之間的分工。

### 6. 視覺化與結果解讀

> *「這張圖到底在說什麼？我的 caption 寫對了嗎？」*

常用工具：**matplotlib / plotly 或你慣用的繪圖工具。**

| Skill | 用途 |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | 產生或重構繪圖腳本（多張圖統一風格、批次重畫）。 |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | 利用長 context，讓圖與草稿 caption / 解讀段落配在一起。 |

### 7. 論文撰寫與修改

> *「文字描述跟圖一致嗎？符合目標期刊嗎？讀起來像人寫的嗎？」*

| Skill | 用途 |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | 抽出 `.paper/claims.yml` 與 `.paper/figures.yml`，讓寫作工具看到的數字跟圖完全一致。 |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | 論文修改、claim-evidence audit、banned-word／humanize、figure-text 一致性、journal format 檢查。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) *(optional)* | 寫作 skill 標出來的引文 metadata 有問題時，深度編輯 Zotero entry——修 citation 欄位、補缺、附 PDF。 |

長段重寫、中英／CJK 草稿、文字風格的第二意見，請用下方 **Cross-cutting
tools** 的 `gemini-delegate`。

### 8. 投稿、回覆審查、收尾

> *「我的 claim 站得住嗎？reviewer response 完整嗎？專案狀態有沒有為下
> 一個人（或半年後的自己）保留好？」*

| Skill | 用途 |
|---|---|
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | Reviewer response 表、pre-submission checklist、journal format 審查、rebuttal letter。 |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 把專案最終狀態凍結進 `.research/` manifests，讓未來 AI session（或未來的你）幾秒就能回到狀況。 |

</details>

---

## Cross-cutting Tools——每個階段都會用到

有 3 個 skills 不屬於特定階段——它們的觸發條件是 **task 性質**：

| Skill | 觸發 | 用途 |
|---|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) | token 重的機械性工作 | 把 batch edits、scaffolding、refactor、test 生成、繪圖腳本交給 Codex CLI。 |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) | 長 context 閱讀或繁中／CJK 輸出 | 把長 PDF 摘要、雙語改寫、第二意見 review 交給 Gemini CLI。 |
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | 「這件事該交給誰？」 | Stage-agnostic、按 task 性質做 routing——產出分工計畫與交接 prompt。 |

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

### Standalone 使用說明

**13 個 skill 全部裝完就能直接用**——沒有 skill 依賴另一個 skill，也
沒有任何 skill 需要超出 `research-hub setup --persona <X>` 已經幫你
設好的 research-hub workspace。

下面這 1 個有 *workflow 順序*——不是依賴，只是建議的執行順序：

- **`research-project-orienter`**——讀 `.research/` manifest 比較快。
  如果還沒有，skill 會 fallback 去 scan `README.md` + `docs/`（比較
  慢）；想要重複用 orientation 的話，先跑 `research-context-compressor`
  產出 manifest。

其他 12 個 skill 都是**直接**用自然輸入：

- 5 個只需要 Claude Code + 你自己的檔案：`research-design-helper`、
  `research-hub-multi-ai`、`research-context-compressor`、
  `paper-memory-builder`、`academic-writing-skills`。
- 4 個需要一個你本來就會有的外部服務：`zotero-skills` /
  `zotero-library-curator`（Zotero local API）、`codex-delegate`
  （Codex CLI binary）、`gemini-delegate`（Gemini CLI binary）。
- 3 個有 research-hub-managed / 手動雙模式：
  - `literature-triage-matrix`——任何論文 list 貼進 chat 即可（per
    SKILL.md mode #0）。
  - `notebooklm-brief-verifier`——接受手動下載的 brief + 純文字 source
    list（per SKILL.md Manual fallback mode，v0.68.2）。
    [已用 fresh-user setup 端到端驗證](test-corpus/manual-fallback-fresh-user/brief-verify-manual-fallback.md)，
    跟 research-hub-managed mode 產出**完全相同**的結果。
  - `research-hub`（knowledge-base）——選 `analyst` persona 是 Obsidian
    + NotebookLM only（無 Zotero）；選 `humanities` 是 Zotero +
    qualitative-friendly defaults。

---

## 安裝

前置條件：Claude Code（https://claude.ai/code）。

> **Skills 實際上怎麼運作：** 每個 skill 是一份 Markdown 指令檔
> （`SKILL.md`），安裝在 `~/.claude/skills/` 下。支援 skills 的 AI host
> （Claude Code、有 Claude Code extension 的 Cursor 等）在你的請求符合
> 該 skill 的 trigger description 時，會自動讀進來並套用。Skills 不是
> CLI 工具、不是 Python package——它們是 host 替你載入的 prompt
> scaffolding。

### 路徑 A — Claude Code marketplace（大多數使用者推薦這條）

兩個指令。不用 Python env、不用一個一個 `git clone`。Skills 在來源 repo
push 新 commit 時會自動更新。

```text
/plugin marketplace add WenyuChiou/ai-research-skills
/plugin install research-workspace@ai-research-skills
```

Catalog 共 5 個 plugins，按需求挑：

| Plugin | 內容 |
|---|---|
| `research-workspace` | 9 個 skills：文獻搜尋 + 比較 + 計畫 + 多 AI routing |
| `academic-writing-skills` | 論文修改、claim audit、reviewer response |
| `zotero-skills` | 比 research-hub 更深的 Zotero CRUD |
| `codex-delegate` | Claude → Codex CLI 委派 |
| `gemini-delegate` | Claude → Gemini CLI 委派 |

Marketplace 內部說明：[.claude-plugin/README.md](.claude-plugin/README.md)。

### 路徑 B — `pip install` + `git clone`（完整平台、含 CLI）

如果除了 SKILL.md 之外還想要 **research-hub Python CLI**（`research-hub
auto`、`research-hub search`、NotebookLM 瀏覽器自動化等），用這條：

```bash
# 1. research-hub——一個指令裝 9 個 skills + onboarding 你的 persona
pip install research-hub-pipeline
research-hub setup --persona researcher   # 或：analyst | humanities | internal

# 2. academic-writing-skills——任何 manuscript 工作都會用到
git clone https://github.com/WenyuChiou/academic-writing-skills \
  ~/.claude/skills/academic-writing-skills
```

需要時再加：

```bash
# 深度 Zotero CRUD（research-hub 不夠用時）
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills

# 多 CLI workflow（Claude + Codex + Gemini）
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill

# 選裝：NotebookLM 瀏覽器自動化（如果 setup 時答 yes 就會幫你裝；
# 跳過的話可以個別在這裡裝）
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

> **路徑 A vs 路徑 B：** A 只裝 SKILL.md（輕量、不用 Python env）。B
> 多了 research-hub CLI（搜尋／匯入／NotebookLM 自動化／dashboard）。
> 你大部分時間在 Claude Code 對話裡 → 選 A；你會 script research-hub
> 指令 → 選 B。

完整安裝指南：[docs/install.md](docs/install.md)。從
research-hub-pipeline ≤ 0.45 升級的話，請參考該檔案的 upgrade note。

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
