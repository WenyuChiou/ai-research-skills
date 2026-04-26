# AI Research Skills

> **不要每次都叫 AI 重讀你的研究專案。給它 skills。**

研究者導向的 **13 個 verified AI skills** 目錄——涵蓋從找第一篇論文到投稿
最後一份手稿的完整研究 workflow。

語言：[English](README.md) | [繁中](README.zh-TW.md)

![研究 pipeline 示意圖即將推出——13 個 skills 對應 8 個研究階段](docs/img/pipeline-overview.png)
*（圖片佔位中——完整 pipeline 示意圖即將推出。在此之前，請參考下方
**完整研究 pipeline** 段落。）*

**你會拿到什麼：** 13 個 skills，其中 11 個已對真實研究環境（1100+ 篇
Zotero、live NotebookLM、真實 manuscript audit）做完端到端驗證。9 個
透過一次安裝就到位（`research-hub-pipeline`）；4 個是獨立 clone。

**適合誰：** 研究生、博士生、博士後、研究人員、研究工程師、圖書館員，
以及在實際研究流程中把 AI 拉進來的研究支援人員。

---

## 5 分鐘上手

想在讀完整份 README 之前先感受一下這個目錄能做什麼？

**情境：** *「找 10 篇我研究主題的論文，產出一張可以拿來寫文獻回顧的
比較表」*

```bash
# 1. 安裝核心（一個指令就裝 9 個 skills）
pip install research-hub-pipeline
research-hub install --platform claude-code

# 2. 找並匯入 10 篇論文（第一次先跳過 NotebookLM）
python -m research_hub auto "你的研究主題" --max-papers 10 --no-nlm

# 3. 在 Claude Code 裡請它做比較表：
#    「Use literature-triage-matrix to compare the 10 papers
#     in cluster <research-hub 剛印出來的 slug>」
```

**會拿到什麼：** `.research/literature_matrix.md`，9 個欄位——citation、
question、method、data、claim、evidence type、limitation、relevance、
這篇論文該放在你 manuscript 的哪裡。**可重現的範例輸出：**
[test-corpus/.../literature_matrix.md](test-corpus/ai-agents-social-interaction/.research/literature_matrix.md)
（用 5 篇 AI agent 與 social interaction 主題的論文真的跑過）。

---

## 找到你的起點

對到下面其中一行就好。裝那 2 個 skill。其他等你需要再說。

| 你是... | 你的問題 | 從這 2 個 skills 開始 | 多久能拿到第一個結果 |
|---|---|---|---|
| **碩一 / 博一新生** | 「我這個題目別人做過什麼？我該讀什麼？」 | [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) + [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | ~10 分鐘 |
| **正在寫論文** | 「我的文字跟圖一致嗎？讀起來像人寫的嗎？」 | [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) + [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) | ~15 分鐘 |
| **跑實驗 / 建模型** | 「怎麼把 RQ 框得更 sharp？怎麼省 token 把專案狀態存下來？」 | [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) + [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | ~20 分鐘 |
| **整理 Zotero library** | 「我的 library 裡有哪些重複論文 / 缺 tag / 殘留 cluster？」 | [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) + [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) | ~5 分鐘 |
| **協助別人用 AI 做研究** *（圖書館員 / RA / 指導者）* | 「我該推薦給我的 team 用什麼？這東西真的能用嗎？」 | 整個目錄 + [docs/install.md](docs/install.md) + [docs/verification.md](docs/verification.md) | （read-only） |

> **你不在上面任何一行？** 下方的完整 pipeline 列出 8 個研究階段，找到
> 你的階段，裝對應的 skill。

---

## 完整研究 pipeline

研究專案的 8 個階段，配上每個階段適用的 skill。這是完整版——如果覺得密
度太高，可以先用上面的「找到你的起點」。

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

13 個 skill 中有 11 個不需要完整的 Zotero + Obsidian + NotebookLM
stack。下面 2 個有依賴鏈，**裝之前**值得先了解：

- **`research-project-orienter`**——需要 `.research/` manifest。如果還
  沒有，skill 會 fallback 去 scan `README.md` + `docs/`（一次性、比較
  慢）；想要重複用 orientation 的話，先跑
  `research-context-compressor` 產出 manifest。
- **`research-hub`**（knowledge-base）——這個就是**平台本體**。最輕量
  的入口是 `research-hub setup --persona analyst`（Obsidian + NotebookLM
  only，無 Zotero）或 `--persona humanities`（Zotero，但用 qualitative
  研究友善的 defaults）。

原本還有 3 個 skill（`literature-triage-matrix`、`research-context-compressor`、
`notebooklm-brief-verifier`）需要額外的 standalone caveat，但
research-hub-pipeline ≥ 0.68.2 已經把 standalone / 手動輸入的路徑直接
寫進各自的 SKILL.md 裡（triage 的 manual paper list、compressor 的 3 分支
input 結構含人文範例、verifier 的 Manual fallback mode）。安裝完直接讀
SKILL.md 就好——這邊不再列額外 caveat。

其餘 8 個 skill（`research-design-helper`、`research-hub-multi-ai`、
`paper-memory-builder`、`zotero-library-curator`、`academic-writing-skills`、
`zotero-skills`、`codex-delegate`、`gemini-delegate`）用各自的自然輸入就
能 standalone 跑（一份 paper draft、一個 Zotero 連線、一個 CLI binary，
等等）——不需要 research-hub workspace。

---

## 安裝

最低限度的有用組合：

```bash
# 1. research-hub——一個指令裝 9 個 skills
pip install research-hub-pipeline
research-hub install --platform claude-code

# 2. academic-writing-skills——任何 manuscript 工作都會用到
git clone https://github.com/WenyuChiou/academic-writing-skills \
  ~/.claude/skills/academic-writing-skills
```

對大多數研究者這樣就夠了。需要時再加：

```bash
# 深度 Zotero CRUD（research-hub 不夠用時）
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills

# 多 CLI workflow（Claude + Codex + Gemini）
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill

# 選裝：NotebookLM 瀏覽器自動化
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

完整安裝指南：[docs/install.md](docs/install.md)。從
research-hub-pipeline ≤ 0.45 升級的話，請參考該檔案的 upgrade note。

---

## 已驗證

這不是「相信我能用」型的 catalog。每個 skill 都對真實研究環境跑過、
證據 commit 進這個 repo：

- **13 個裡 11 個** 通過 **T1**（用真實輸入跑出真實輸出的功能性 smoke test）。
- **1 個 T2 caveat**（`codex-delegate`：有 workaround，文件記錄了）。
- **1 個 T2 pass**（`gemini-delegate`）。
- **0 個失敗**、**0 個未驗證**。

測試 corpus：5 篇 AI agent 與 social interaction 主題的論文（真實
arXiv / Elsevier metadata），單一 `research-hub search` 指令可重現。
完整 per-skill 報告：[docs/verification.md](docs/verification.md)。

---

## 狀態與授權

輕量 catalog。每個 skill 由各自的 canonical repo 維護——這個 catalog
是索引，不是 monorepo。

授權：MIT。歡迎 contribution——open issue 或 PR。新 skill 提案請鎖定
`research-hub`（workflow 整合）或一個獨立 repo（單一目的、深度的
CRUD）。
