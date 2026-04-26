# 完整研究 pipeline

研究專案的 8 個階段，配上每個階段適用的 skill。這是完整版 reference——
大部分使用者用 [README 的「找到你的起點」](../README.zh-TW.md#找到你的起點)
就夠了，不必讀這段。

English: [pipeline.md](pipeline.md)

```text
1. 找文獻  →  2. 整理比較、找 gap  →  3a. 框問題  →  3b. 寫計畫
        →  4. 設計與建模  →  5. 執行、校正、驗證 (C&V)  →  6. 視覺化
        →  7. 撰寫論文  →  8. 投稿、回覆審查、收尾
```

有 3 個 skills 不屬於特定階段——它們的觸發條件是 **task 性質**，不是
pipeline 位置。見最下方的 **Cross-cutting tools**。

## 1. 找文獻

> *「這個題目別人做過什麼？我該讀什麼？」*

常用工具：**Zotero · NotebookLM · Obsidian** *（目前沒有 OneNote 對應的
skill，請以 Obsidian 作為筆記層。）*

| Skill | 用途 |
|---|---|
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) | 在 arXiv / Semantic Scholar / CrossRef / PubMed 搜尋論文，匯入 metadata，自動寫成 Obsidian 筆記。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) | research-hub pipeline 不夠時，做更深的 Zotero 加項、tag、去重、清理。 |

## 2. 整理、比較文獻、找出 research gap

> *「研究 gap 在哪裡？哪 5 篇是真的關鍵？」*

| Skill | 用途 |
|---|---|
| [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | 不重讀每一篇 PDF，就能依 method、data、claim、limitation、relevance 比較。 |
| [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | 把 NotebookLM 的 brief 對回原始 source bundle，抓出漏掉的 source、沒根據的 claim、互相矛盾的描述。 |
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) | 建立要餵進 matrix 的 Obsidian cluster 與 NotebookLM source bundle。 |
| [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) *(optional)* | 比較前先 audit Zotero——找出重複 DOI、orphan items、提出 tag/collection 整理計畫。**Read-only**。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | 真的執行 curator 提出來的整理動作——對 Zotero items 完整 CRUD。 |

## 3a. 框問題

> *「我的研究問題夠不夠 sharp？可不可以證偽？」*

一個 Socratic 對話夥伴，用結構化的提問逼你把原本含糊的東西講清楚。

| Skill | 用途 |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | 引導你走過 5 段：研究問題 sharpen → expected mechanism → identifiability check → validation plan → risk register，產出 `.research/design_brief.md`。 |

## 3b. 寫計畫 artifact（讓 AI 幫你記住）

> *「我的 claim 是什麼？用什麼資料？接下來的計畫是什麼？」*

3a 把問題框定後，下面這些 skill 把計畫存成 machine-readable manifest，
之後的 AI session 不需要重讀整個 repo。

| Skill | 用途 |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 寫出 `.research/project_manifest.yml`、`experiment_matrix.yml`、`data_dictionary.yml`。如果 3a 已經產出 `design_brief.md` 也會一起收進來。 |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | 讀那些 manifest，幫你（或新的 AI session）快速產生 orientation 摘要。 |

## 4. 設計與建立模型

> *「我需要什麼架構、什麼方程式、什麼 agents、什麼 prompt？」*

把 3a 產出的 `design_brief.md` 讀回來當 model spec，再產生
implementation scaffolding。

| Skill | 用途 |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | 跟 3a 同一個 skill——準備把「要建什麼模型」翻成「怎麼建」時，重新讀 `.research/design_brief.md` 對照。 |

實作 scaffolding（test harness、繪圖、batch edits）和大型 reference
codebase 的 design review，請用下方 **Cross-cutting tools** 的
`codex-delegate` 與 `gemini-delegate`。

## 5. 執行實驗、校正與驗證 (C&V)

> *「跑出來的東西可重現、可檢查、可擴充嗎？跨長 session 能不能省 token？」*

| Skill | 用途 |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 用 manifest 省 token，每次跑/檢查的 session 不必從零開始。 |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | 切換實驗、或休息幾天回來時，用便宜的方式重新進入狀況。 |

反覆執行的 sweep、regression test、修完 bug 的 verification 這類
token 重的工作，請用下方 **Cross-cutting tools**——`codex-delegate`
做 code-heavy 的執行；`research-hub-multi-ai` 規劃 Claude / Codex /
Gemini 之間的分工。

## 6. 視覺化與結果解讀

> *「這張圖到底在說什麼？我的 caption 寫對了嗎？」*

常用工具：**matplotlib / plotly 或你慣用的繪圖工具。**

| Skill | 用途 |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) | 產生或重構繪圖腳本（多張圖統一風格、批次重畫）。 |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) | 利用長 context，讓圖與草稿 caption / 解讀段落配在一起。 |

## 7. 論文撰寫與修改

> *「文字描述跟圖一致嗎？符合目標期刊嗎？讀起來像人寫的嗎？」*

| Skill | 用途 |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | 抽出 `.paper/claims.yml` 與 `.paper/figures.yml`，讓寫作工具看到的數字跟圖完全一致。 |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) | 論文修改、claim-evidence audit、banned-word／humanize、figure-text 一致性、journal format 檢查。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | 寫作 skill 標出來的引文 metadata 有問題時，深度編輯 Zotero entry——修 citation 欄位、補缺、附 PDF。 |

長段重寫、中英／CJK 草稿、文字風格的第二意見，請用下方 **Cross-cutting
tools** 的 `gemini-delegate`。

## 8. 投稿、回覆審查、收尾

> *「我的 claim 站得住嗎？reviewer response 完整嗎？專案狀態有沒有為下
> 一個人（或半年後的自己）保留好？」*

| Skill | 用途 |
|---|---|
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) | Reviewer response 表、pre-submission checklist、journal format 審查、rebuttal letter。 |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 把專案最終狀態凍結進 `.research/` manifests，讓未來 AI session（或未來的你）幾秒就能回到狀況。 |

## Cross-cutting tools——每個階段都會用到

有 3 個 skills 不屬於特定階段——它們的觸發條件是 **task 性質**：

| Skill | 觸發 | 用途 |
|---|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) | token 重的機械性工作 | 把 batch edits、scaffolding、refactor、test 生成、繪圖腳本交給 Codex CLI。 |
| [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) | 長 context 閱讀或繁中／CJK 輸出 | 把長 PDF 摘要、雙語改寫、第二意見 review 交給 Gemini CLI。 |
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | 「這件事該交給誰？」 | Stage-agnostic、按 task 性質做 routing——產出分工計畫與交接 prompt。 |
