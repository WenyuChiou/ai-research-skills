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

每個既有階段的 AI-for-science 輸入、輸出、品質證據與研究者決策，見
[科學研究生命週期與品質關卡](scientific-lifecycle.zh-TW.md)。

## 1. 找文獻

> *「這個題目別人做過什麼？我該讀什麼？」*

先用 **Codex 或 Claude Code** 當前實際提供的搜尋、deep-research、閱讀、
引文工具與相關 skills。不要假設兩個 host 都有所有能力；記錄本輪已使用、
可用但未測、或在此環境不可用的項目。遵循上游的
[research protocol](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/references/research-protocol.md)
與 [source-claim audit guidance](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/references/source-claim-audit.md)，
不在 catalog 另建一套搜尋引擎。

**Research Hub 本身是可選的。** 原生 AI Skills 的搜尋與原文閱讀，不需要安裝或設定
Research Hub，可直接使用 host 實際可用的工具。共用 protocol 連結是研究指引，
不表示必須執行 Hub。使用者選擇 Hub 時，再依需要使用它提供的整理、持久儲存、
workflow／整合路線。只檢查所選動作需要的設定與存取，不把 Hub CLI 設定、整合
帳號、API key 或 login 變成原生路線的必要前提；host 工具仍依其實際可用且已授權
的能力執行。

### 確認本輪需求與搜尋路線

用自然語言接收主題、目標篇數與閱讀深度。沿用已提供的偏好，只問真正缺少且
影響結果的選項。例如「約 12 篇，先看摘要，再精讀兩篇核心文獻」已同時交代
篇數與深度，不要重問，也不要求填表。需要篇數但尚未指定時，可提議一輪
**10–20 篇相關且不重複的論文**，按問題與可得證據調整。這不是配額，也不是
預設 30 篇；不要用低相關文獻、重複版本或無法取得的論文湊數。交代不足與未
涵蓋需求；較少但有用的集合也可能是合適結果。

把問題拆成概念、關鍵字、同義詞、縮寫與相鄰術語，嘗試多條適合的搜尋路線及
查詢變體，再做向後與向前 citation chasing。記錄真正使用的路線、結果與失敗；
單次查詢不代表廣泛涵蓋。逐篇說明角色：**classic** 提供奠基背景、**core**
直接服務目前問題、**nearest** 是最接近的主題比較、**methodological** 提供
方法或資料貢獻、**contrary** 挑戰目前主張。角色可以重疊；年代、被引次數或
只有方法相似，都不會自動使論文成為核心或最近前作。

### 分開篇數與閱讀證據

原始命中數與不同 works 的 **discovered**、**screened**、**included**、
**reading-depth counts**、**core count** 要分開記錄。Preprint、期刊版與修訂版
在 work 層級去重，但保留版本身分、互連與實際閱讀的版本，不把版本算成額外
篇數；同一沿革若確實包含不同研究，要交代理由。未限定 public-fulltext-only 的
一般發現輪次，納入可記錄相關性而與全文可得性分開；重要的 pending/background
作品仍可保留納入，但須揭露存取限制。
選為 core 不代表已讀。
`not-read`、`abstract-only`、`selected-sections`、`full-text` 描述實際閱讀，
不是檔案可得性或儲存狀態。每份摘要與重要 claim 都須對應來源／版本與真正
讀過的章節；未核對前，不跨版本搬用支持證據。

當使用者選擇 public-fulltext-only（僅公開全文）範圍時，正式納入須同時符合
已評估的學術相關性，以及已實際取得且核驗為所選 work/version 的合法公開完整
正文。此條件適用於正式 included count、交付清單，以及選用目的地的歸檔／
NotebookLM 清單。Landing／abstract-only、非公開、登入／付費牆、blocked 或缺少
正文的回應都不能當正式論文。重要者另列未納入／背景線索，不計入正式篇數、
不湊數。取得全文仍可能只讀了部分章節，須如實標示閱讀層級／章節；可得性不
證明全文已讀或學術相關。

交接需保留搜尋需求／查詢與實際觀察結果、來源身分與版本／日期、實際閱讀
層級與 claim locator、最接近或相反的研究，以及 `not-read`／`unknown`。
依賴全文 claim 前須讀相關方法與結果；abstract-only 摘要、搜尋命中、填好的
locator 或結構檢查都不等於原文驗證。作者自行維護的 query ledger 與留存的
工具呼叫 receipt 要分開；不要只為補造歷史 receipt 而要求重跑搜尋。

### 歸檔或進入 NotebookLM 前先驗證全文資格

歸檔／NotebookLM 須有**合法公開可取得的完整正文**，並核對實際 PDF 或實質
正文符合目標 work/version。檢查回應與可讀內容／頁面；只有 `.pdf` 網址、
HTTP 200、MIME 標籤或 PDF 檔頭都不充分。登入頁、摘要／landing page、付費牆
與錯誤回應不是論文全文。重要但無法取得的作品保留為 pending/background，
記錄存取限制與下一個安全路線，不丟棄、不標成全文已讀，也不當全文上傳。
不得繞過存取限制；已驗證有完整正文，仍不代表每個章節都已讀過。

**Zotero · NotebookLM · Obsidian 都是可選整合**，不是這輪找文獻的前提。
只有需要且已獲授權時，才使用設定好的儲存／自動化；不要為文獻研究額外
要求帳號或設定步驟。某個 executor 沒有 Hub CLI，不代表產品沒有該能力；
可攜／手動交接也不等於已執行 Hub pipeline。

由使用者選擇目的地，包括不用或稍後再存。每個指定的目的地／動作各留獨立
receipt，包含來源／版本、目的地身分，以及已確認成功、失敗、未知或跳過的
結果。本 catalog 提供指引，不實作這些 provider 能力。**已儲存不等於語義上
已完成**；檔案或上傳 receipt 不會完成閱讀、相關性判斷或 claim 驗證。技術性
pending 不會自動變成人才能決定的問題：在既有授權內繼續安全、有界的診斷／
修補，沒有安全路線時保留 blocker。只有真正的範圍／科學選擇、存取許可、
資源承諾或另需寫入授權時才問研究者；不暗中安裝工具或要求選用帳號。

| Skill | 用途 |
|---|---|
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) | 按共用 protocol 使用可用的原生搜尋與原文閱讀；需要時才用已設定的 arXiv / Semantic Scholar / CrossRef / PubMed 搜尋與獲授權的匯入／儲存。 |
| [`paper-summarize`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-summarize/SKILL.md) *（可選）* | 匯入後補寫逐篇 abstract-only 摘要；不讀 PDF，也不驗證論文全文 claim。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *（可選）* | 需要且另行獲授權時，才做 Zotero 加項、tag、去重、清理。 |

## 2. 整理、比較文獻、找出 research gap

> *「研究 gap 在哪裡？哪 5 篇是真的關鍵？」*

| Skill | 用途 |
|---|---|
| [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) | 不重讀每一篇 PDF，就能依 method、data、claim、limitation、relevance 比較。 |
| [`gap-to-topic`](https://github.com/WenyuChiou/research-hub/blob/master/skills/gap-to-topic/SKILL.md) | 3-gate go/no-go 決策備忘錄 — 對候選論文/提案主題評估「缺口開不開？有貢獻嗎？可不可行？」。v0.3.12+ 起把 `.gaps.yml` 接給 Stage 3a。 |
| [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) | 把 NotebookLM 的 brief 對回原始 source bundle，抓出漏掉的 source、沒根據的 claim、互相矛盾的描述。 |
| [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) | 建立要餵進 matrix 的 Obsidian cluster 與 NotebookLM source bundle。 |
| [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) *(optional)* | 比較前先 audit Zotero——找出重複 DOI、orphan items、提出 tag/collection 整理計畫。**Read-only**。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | 真的執行 curator 提出來的整理動作——對 Zotero items 完整 CRUD。 |

## 3a. 框問題

> *「我的研究問題夠不夠 sharp？可不可以證偽？」*

一個 Socratic 對話夥伴，用結構化的提問逼你把原本含糊的東西講清楚。

| Skill | 用途 |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | 引導你走過 5 段：研究問題 sharpen → expected mechanism → identifiability check → validation plan → risk register，產出 `.research/design_brief.md`。**v0.3.12+**：若 `.research/topic_dossier.gaps.yml` 存在（前一輪 `gap-to-topic` 跑出來的），自動 pre-fill 段 1 (RQ) 與段 5 (risks)，verdict-aware 挑 candidate。 |

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

重新讀 3a 的 `design_brief.md` 作為研究設計意圖，先與研究者建立
專案的實作規格，再產生 scaffolding；design helper 不會發明 model architecture。

| Skill | 用途 |
|---|---|
| [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) | 跟 3a 同一個 skill——準備把「要建什麼模型」翻成「怎麼建」時，重新讀 `.research/design_brief.md` 對照。 |

實作 scaffolding（test harness、繪圖、batch edits）請用下方
**Cross-cutting tools** 的 `codex-delegate` 與 `antigravity-delegate`。
大型 reference codebase 的 design review、長 context 判斷留在 primary model。

## 5. 執行實驗、校正與驗證 (C&V)

> *「跑出來的東西可重現、可檢查、可擴充嗎？跨長 session 能不能省 token？」*

| Skill | 用途 |
|---|---|
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 用 manifest 省 token，每次跑/檢查的 session 不必從零開始。 |
| [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) | 切換實驗、或休息幾天回來時，用便宜的方式重新進入狀況。 |

反覆執行的 sweep、regression test、修完 bug 的 verification 這類
token 重的工作，請用下方 **Cross-cutting tools**——`codex-delegate`
做 code-heavy 的執行；`antigravity-delegate` 只處理有邊界、非誠實性關鍵的
機械性工作；`research-hub-multi-ai` 規劃 Codex / Antigravity leaves 的分工。

## 6. 視覺化與結果解讀

> *「這張圖到底在說什麼？我的 caption 寫對了嗎？」*

常用工具：**matplotlib / plotly 或你慣用的繪圖工具。**

| Skill | 用途 |
|---|---|
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) | 產生或重構繪圖腳本（多張圖統一風格、批次重畫）。 |
| [`antigravity-delegate`](https://github.com/WenyuChiou/antigravity-delegate/blob/master/skills/antigravity-delegate/SKILL.md) | 在 Claude 監督下處理有邊界、非誠實性關鍵的繪圖清理或 fixture 維護。 |

## 7. 論文撰寫與修改

> *「文字描述跟圖一致嗎？符合目標期刊嗎？讀起來像人寫的嗎？」*

| Skill | 用途 |
|---|---|
| [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) | 抽出 `.paper/claims.yml` 與 `.paper/figures.yml`，讓寫作工具看到的數字跟圖完全一致。 |
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) | Extended outline、逐段與逐節撰寫、evidence alignment、術語、重複、流暢度、跨檔案 revision 與 release checks。 |
| [`paper-review`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/paper-review/SKILL.md) | 通用科學審查，會按需選用 psychometrics／SEM、AI／LLM、水資源／CNHS、洪水／hydrodynamics 或混合 modules。 |
| [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) *(optional)* | 寫作 skill 標出來的引文 metadata 有問題時，深度編輯 Zotero entry——修 citation 欄位、補缺、附 PDF。 |

長段重寫、中英／CJK 草稿、文字風格與審查判斷留在 primary model。

## 8. 投稿、回覆審查、收尾

> *「我的 claim 站得住嗎？reviewer response 完整嗎？專案狀態有沒有為下
> 一個人（或半年後的自己）保留好？」*

| Skill | 用途 |
|---|---|
| [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) | 跨檔案同步、submission package 檢查與 blocking release readiness。 |
| [`paper-review`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/paper-review/SKILL.md) | 依 round 校準的 top-to-bottom review 與 prior-comment regression checks；只有明確要求時才套用 Ethan-style。 |
| [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) | 把專案最終狀態凍結進 `.research/` manifests，讓未來 AI session（或未來的你）幾秒就能回到狀況。 |

## Cross-cutting tools——每個階段都會用到

有 3 個 skills 不屬於特定階段——它們的觸發條件是 **task 性質**：

| Skill | 觸發 | 用途 |
|---|---|---|
| [`research-workflow-orchestrator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-workflow-orchestrator/SKILL.md) | 可續接多階段 workflow | 協調既有階段、provenance 與明確 human decision gates。 |
| [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) | token 重的機械性工作 | 把 batch edits、scaffolding、refactor、test 生成、繪圖腳本交給 Codex CLI。 |
| [`antigravity-delegate`](https://github.com/WenyuChiou/antigravity-delegate/blob/master/skills/antigravity-delegate/SKILL.md) | 有邊界、非誠實性關鍵的機械性工作 | 在 Claude 監督下把範圍明確的機械性 edits 交給 Antigravity CLI。 |
| [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) | 「這件事該交給誰？」 | Stage-agnostic routing，在 Codex 與 Antigravity leaves 之間產出分工計畫與交接 prompt。 |
