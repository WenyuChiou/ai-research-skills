# Skill 實際產出什麼

真實 deliverable 形狀,讓你在裝之前就能判斷每個 skill 適不適合你的工作流。
下面所有範例都用**合成資料** —— 沒有 maintainer 的真實 artifact。

語言:[English](examples.md) | [繁中](examples.zh-TW.md)

> 範例是示意。實際 input 跟 prompt 會產出**同樣形狀**但內容不同的 output;
> 行數、語氣、verdict 比例隨 source material 變。

---

## `literature-triage-matrix` — 5 篇 paper、9 欄

**Input**:5 篇 paper 的資料夾(PDF、Obsidian 筆記、或 Zotero collection)
加 prompt *「比較這 5 篇論文的 method、data、claims、limitations」*。

**Output** —— 寫到 `.research/literature_matrix.md`:

| Citation | Year | Type | Method | Data | Central claim | Domain | Limitation | Relevance |
|---|---|---|---|---|---|---|---|---|
| Chen 2022 | 2022 | empirical | finite-difference flood model、30 m grid | Hurricane Harvey、5 天視窗 | 海岸地層下陷放大 surge 淹水 12-18% | Coastal hydrology | 單一事件;沒做 recurrence-interval sweep | High — method 直接 match |
| Patel 2023 | 2023 | tooling | 開源 ABM platform(`pyabm`) | 合成 1000-agent runs | 異質風險下分散式保險定價在 <20 ticks 收斂 | Insurance ABM | 沒做 empirical 校準 | Medium — pipeline 參考 |
| Ortiz-Lim 2024 | 2024 | conceptual | Argument-mining + 風險分類 | 47 章 IPCC AR6 | 「Compound risk」在 WG2 vs WG3 之間 operationalise 不一致 | Climate risk taxonomy | 沒 code;沒 replication artifact | Low — 框架性鄰近 |
| Kumar 2026 | 2026 | empirical | LLM-as-agent、6-round multi-issue bargaining | 1200 模擬 dyad | Theory-of-mind prompting 把 Pareto efficiency 提高 9 pp | Multi-agent LLM | 單一 LLM provider;沒 human baseline | High — 近期 + 可重現 |
| Wang 2026 | 2026 | empirical | Streaming-platform telemetry + agent-based replay | 4.3M user-streamer 互動 | 觀眾-streamer-平台 triadic feedback loop 重現 engagement skew | Social ABM | 平台特定;沒 pre-register | Medium — 方法論可遷移 |

**Sanity grid**(skill 自動在表下方 emit):

```
Method × Domain   coastal  insurance  taxonomy  multi-agent  social-abm
  empirical          1         0          0          1           1
  tooling            0         1          0          0           0
  conceptual         0         0          1          0           0
```

某 row/column 只有一篇 paper 時,可以再 ask skill 找更多填進該 cell 才開始寫 lit-review。

---

## `academic-writing-skills` — banned-word audit + reviewer response

### Banned-word audit(input = 一段文字)

**Input**: *「The proposed framework leverages a novel deep-learning pipeline to
comprehensively delve into the multifaceted challenges of flood resilience,
robustly demonstrating that our approach is significantly better than baselines.」*

**Output** —— 逐行 audit:

| Span | Banned term | 為什麼 flag | 建議替換 |
|---|---|---|---|
| "leverages a novel" | `leverages`、`novel`(GenAI filler ×2) | 空 intensifier;peer review 通常會被刪掉 | 「uses」/ 拿掉 "novel" |
| "comprehensively delve" | `delve` | `delve` 在 high-confidence GenAI-fingerprint list (banned_words.md §A) | 「examine」/「study」 |
| "multifaceted challenges" | `multifaceted` | 空修飾語;說清楚哪幾個 dimension 或刪掉 | 「challenges across X, Y, Z dimensions of …」 |
| "robustly demonstrating" | `robustly`(沒對應 robustness check) | 沒分析支撐就 overclaim | 拿掉 adverb;改寫成 "robust" 動詞所對應的 test |
| "significantly better"(沒 *p*-value / effect size) | `significantly`(口語 vs 統計) | Reviewer pattern:1/4 reviewer 會 flag | 「outperforms baselines by *X%* (CI [a, b])」 |

**Summary verdict**:5 issues / 1 paragraph。建議投稿前修。

### Reviewer-response 表(input = `.paper/reviewer_comments.md`)

**Input** —— `.paper/reviewer_comments.md` 6 條意見 R2.1-R2.6。

**Output** —— `.paper/reviewer_responses.md` 骨架:

| Comment | Anchor(原文段落) | 作者回覆(student tone) | 稿件改動 | 引用證據 |
|---|---|---|---|---|
| R2.1 — *「Figure 3 軸序不常見。」* | §4.2 Fig. 3 caption | Fixed。改成 median-asc、保留 outlier band。 | Fig. 3 panels (b, c) 重產。 | `figures/fig3_v2.pdf` |
| R2.2 — *「12% 這個數字從哪來?」* | §3.1 末段 | 12% 是 bootstrap 分佈平均(n=10000),現在改報 95% CI。 | §3.1 加「Mean 12% (95% CI 9-15%)」。 | `.paper/figures.yml` row C3 |
| R2.3 — *「為什麼沒引 Smith 2019?」* | §1.3 background | Added。Smith 2019 框架了我們用的 FFE/EH 區分,相關。 | §1.3 加 citation;reference 列表更新。 | Smith 2019 *J. Hydrol.* 575:122-138 |
| R2.4 — *「Discussion 對 policy 過度推論。」* | §6 末段 | 同意。「proves」改「is consistent with」,加 domain caveat。 | §6 重寫;1 句 transferability scope。 | — |
| R2.5 — *「Section 5 重複。」* | §5.1、§5.4 | 把 §5.4 刪掉(重複 §5.1 的 mechanism);倖存內容併進 §5.1。 | §5 從 4 子節縮成 3。 | — |
| R2.6 — *「程式碼在哪?」* | (沒寫) | 在 acknowledgements 加 Zenodo DOI + 註腳。 | acknowledgements 加 Zenodo DOI + repo URL。 | DOI 10.5281/zenodo.xxxxxxx |

語氣、banned-word audit、concession-threshold 規則來自 `reviewer_response_workflow.md`。

---

## `zotero-library-curator` — preview-only audit 報告

**Input**:800 條的 Zotero library 加 prompt *「audit 我的 library 找重複、
orphan tag、bloat」*。

**Output** —— 在對話裡(不會寫進 library):

```
Library audit — 2024-03-15  (合成範例 —— 非 maintainer 真實執行)

Items inspected:       814
Read-only?             yes (no changes applied)

Findings:
  ▸ Duplicate DOIs:          11   (3 high-confidence 對,下方列出)
  ▸ Orphan-tag items:        42   (任何 collection 都沒 tag 的 item)
  ▸ Near-duplicate tags:     27   (大小寫或尾隨空白變體)
  ▸ Sparse tags (≤2 items):  398  (佔 tag 詞彙 81%)
  ▸ Cluster bloat (>200):    1    ("methodology" — 247 items, 建議拆子分類)

High-confidence 重複對:
  1. doi:10.1029/2018wr023456
     - keep: Chen, Y. (2018) — "Flood model intercomparison" — 有全文
     - merge: Chen, Y. (2018) — 同 DOI、無附件、手動鍵入
  2. doi:10.1038/s41586-020-2649-2
     - keep: Wei, K. (2020) — 有 annotation + tag
     - merge: K. Wei (2020) — 作者格式重複條目
  3. doi:10.1175/jhm-d-19-0157.1
     - keep: 完整 citation + collection
     - merge: 只有 title 的空條目

建議下一步:
  把 3 對 high-confidence 交給 `zotero-skills`(CRUD plugin):
    「按 curator audit 找出的 3 個重複 DOI 做 merge」
  Curator **不寫**;zotero-skills 才寫。動之前先備份 library。
```

Curator 只 emit 這份報告;實際 merge / delete 在你確認後由 `zotero-skills` 動。

---

## `paper-summarize` — 每篇 paper 一個 Key Findings markdown block

**Input**:Obsidian cluster 裡 5 篇 paper、每篇 per-paper note 還是 TODO 骨架
(`research-hub auto` 剛跑完的狀態)。

**Output** —— 每篇 paper 一塊 markdown,同時寫進 Obsidian note **跟** 對應的
Zotero child note(Zotero 寫失敗會 atomic rollback):

```markdown
## Key Findings

- 異質風險下分散式保險定價在 36 個 parameter combination 全部 <20 ticks
  收斂。收斂對 asymmetric information 穩,但對 >30% agent 低報風險級別
  脆弱(收斂時間 super-linearly 拉長)。
- 定價機制的 stability 取決於**保險公司數量**、不是市佔率 —— 5 家
  80/20 跟 5 家 20/20/20/20/20 的市場收斂時間一樣。

## Methodology

- ABM 模擬用 `pyabm`(Patel 的開源平台)。
- 每個 run 1000 agent;36 個 parameter combination(3 種風險級別分佈
  × 4 種資訊regime × 3 種市場結構)。
- Outcome metric:time-to-equilibrium 加 §3.2 定義的 Lyapunov-style
  stability index。

## Relevance

- Method match:直接對應**你**自己的 coupled ABM 專案 —— 換成你目前
  研究的專案名稱跟段落引用。
- Use case:你正在 model 的 risk-misperception scenario(或類似的
  機制穩定性檢查)所需的定價機制 robustness check。
- 略過如果:沒在做 insurance / pricing mechanism;這是 upstream
  tooling,不是 ABM 在 social outcome 上的實質 claim。
```

Block 落在現有的 `## Key Findings` / `## Methodology` / `## Relevance`
標題下(取代 TODO 骨架,不會 append)。

---

## `gap-to-topic` — 候選主題的 3-gate 決策檔

**輸入**: 一個候選的論文或提案主題 (在 §0 中透過 Socratic 式方法闡明) — 例如「用於社會水文學中人類行為的 LLM 代理人」— 加上要搜索的更廣泛領域 (「LLM 在水資源中的應用」)。

**輸出包** — 寫入 `.research/` 的 4 個檔案，加上透過 `scripts/dossier_to_docx.js` 產生的相應 `topic_dossier.docx`:

| 檔案 | 內容 |
|---|---|
| `topic_dossier.md` / `.docx` | 7 節 + 2 附錄的研究級決策備忘錄：包含每個候選者結論卡的執行摘要 → 定義 → 決策 Scorecards (3 gates × Likert) → 證據基礎 → 逐 Gate 評估 → 風險與終止測試 → 建議後續步驟 → 可重複性日誌附錄 A → 檔案列表附錄 B |
| `topic_dossier.bib` | BibTeX 參考文獻列表 — 每篇被引用的論文都有可解析的 DOI / arXiv ID |
| `topic_dossier.gaps.yml` | 機器可讀的結構化匯出 — 每個 gap 的 `verdict` / `verdict_reason` / `feasibility` / `dead_end_status` 加上 `open_questions[]`。由 `research-design-helper` v0.3.12+ 讀取以進行 Stage 3a 交接 |
| `literature_matrix.md` | 逐篇論文比較表 (方法 / 論點 / 證據類型 / 限制 / 相關性) — 由 `literature-triage-matrix` 在 §1 步驟 2 建立 |

**候選者層級的結論** — 每個候選者只會得到三種結果之一：

| 結論 | 意義 | `.docx` 中的顏色 |
|---|---|---|
| **Do not pursue — as stated** | 至少有一個 gate 未通過 (已被佔據 / 不構成貢獻 / 不可行)。可選的補救路徑。 | Light red |
| **Worth pursuing — only if its open conditions hold** | 所有三個 gate 都達到中立或更佳，但取決於後續的操作性跟進 (例如，資料集識別、驗證性試點)。 | Light yellow |
| **Worth pursuing** | 所有三個 gate 都無條件通過。 | Light green |

**Gate-cell 狀態** — 在每個候選者的 scorecard 內部，單獨的 gate cell 也可以帶有 "skipped" 狀態，當同一候選者中較早的 gate 失敗時 (剩餘的 gate 會被短路)：

| 狀態 | 意義 | `.docx` 中的顏色 |
|---|---|---|
| `Not assessed` | Gate 被跳過，因為同一個 scorecard 中較早的 gate 已經失敗。適用於 **scorecard 表格內的 cell**，而非候選者層級的結論。 | Light grey |

一個完整的雙語範例，複製自一個真實的 dogfood 執行 (LLM 在水資源中的應用，評估了兩個候選者，一個 `do-not-pursue` + 一個 `conditional-go`)，作為以下檔案包含在此 repo 中：

- [`example-topic-dossier.md`](example-topic-dossier.md) / [`.docx`](example-topic-dossier.docx)
- [`example-topic-dossier.bib`](example-topic-dossier.bib)
- [`example-topic-dossier.gaps.yml`](example-topic-dossier.gaps.yml)
- [`example-topic-dossier.zh-TW.md`](example-topic-dossier.zh-TW.md) / [`.zh-TW.docx`](example-topic-dossier.zh-TW.docx)

`.docx` 檔案以雙語結論顏色編碼呈現 (`gen_docx.js` 的 regex 同時匹配英文的 `"do not pursue"` 和繁體中文的 `"不予推進"`) 並自動選擇 en / zh-TW 字體 (當檔名匹配 `.zh|zh-|zh_|-tw|-cn` 時為微軟正黑體，否則為 Arial)。

---

## `research-design-helper` — Stage 3a 設計簡報

**輸入**: 一個研究想法，通常是先前 `gap-to-topic` dossier 執行中的 `conditional-go` 候選者 (下方有配套範例)。此 skill 會引導研究人員完成五個 Socratic 式環節，並將結果寫入 `.research/design_brief.md`。

**輸出包** — 一個帶有 YAML frontmatter 的 Markdown 檔案：

| 章節 | 捕捉的內容 |
|---|---|
| Frontmatter (`source`, `gap_verdict`, `placeholder_segments`) | 指向上游 `gap-to-topic` 候選者的來源紀錄 (v0.3.12+ wire)；標示任何由非 Socratic 式佔位符內容填寫的環節的機器標記列表 (v0.3.15+) |
| §1 研究問題 | 用一個可證偽的句子來精煉 RQ + 證偽條件 + 最小可行的一週原型範圍 |
| §2 預期 mechanism | 具有明確「最不確定步驟」+「你賭會先壞掉的第一步」註釋的因果鏈 |
| §3 Identifiability 檢查 | 區分條件、要排除的 confounders、遺失資料計畫 |
| §4 驗證計畫 | 成功指標、要超越的 baseline、negative control |
| §5 風險紀錄 | 3–5 個已命名的風險，每個都有 early-warning signal + mitigation |

一個完整的範例，從 Stage 2 dossier 預先填寫，並展示了來源紀錄 wire + 佔位符環節的慣例，作為以下檔案包含在此 repo 中：

- [`example-design-brief.md`](example-design-brief.md)

簡報的 frontmatter `source: topic_dossier.gaps.yml#G2` 指回了開啟 Stage 2 → 3a wire 的 [`example-topic-dossier.gaps.yml`](example-topic-dossier.gaps.yml) 的候選者 2。

---

## `research-context-compressor` — Stage 3b 專案 manifest

**輸入**: 一個研究 repository，可選擇性地包含來自 Stage 3a `research-design-helper` 會話的 `.research/design_brief.md`。此 skill 會掃描 repo 並寫入 `.research/project_manifest.yml` 作為一個機器可讀的定向檔案，未來的 AI 會話將讀取此檔案而不是重新掃描 repo。

**輸出**: 一個 YAML 檔案，其 schema 特性在範例中可見：

| 欄位 | 備註 |
|---|---|
| `project_name`, `research_area`, `research_question`, `current_stage`, `last_updated` | 必填的核心欄位 |
| `provenance.from_gap` | 從上游 design_brief frontmatter 的 `source` 欄位逐字複製 (v0.3.12+ wire)；讓 project-orienter 能夠將 manifest 追溯回 dossier 候選者 |
| 可選的描述性欄位 (`tools`, `datasets`, `entrypoints`, 等) | 從 repo 掃描輸入 (README, `pyproject.toml`, `scripts/`, `data/`) 填入；當誠實地未知而不是捏造時，為空列表 |

一個展示了來源紀錄 wire (manifest 將 `source` 從 brief 複製到 `provenance.from_gap`) 的完整範例，作為以下檔案提供：

- [`example-project-manifest.yml`](example-project-manifest.yml)

manifest 的 `research_question` 逐字鏡像了 [`example-design-brief.md`](example-design-brief.md) §1 中精煉的 RQ — brief 是權威；manifest 鏡像它。

---

## `paper-memory-builder` — Stage 7 論文 memory

**輸入**: 一個手稿檔案 (`.docx`, `.tex`, `.md`) 加上可選的圖表目錄和用於上下文的 `.research/` manifest。此 skill 將論文層級的 claim 和圖表清單提取到 `.paper/{claims.yml, figures.yml, revision_history.yml}`，這樣下游的 `academic-writing-skills` skill 就可以運行 claim-evidence audit、banned-word 檢查和審稿人回應工作，而無需每次都重新閱讀手稿。

**輸出包** — 兩個 YAML 檔案加上一個僅供附加的歷史日誌：

| 檔案 | 承載的內容 |
|---|---|
| `claims.yml` | 每個論文層級的 claim，包含 `evidence_artifacts`, `figure_or_table`, `status`, `risk`, `sentence_in_manuscript`。強制執行 anti-leakage 規則：`evidence_artifacts` 為空的 claim 帶有 `status: gap` + 一個非空的 `gap_reason`。 |
| `figures.yml` | 圖表清單，包含 `file`, `panels`, `key_numbers`, `supports_claims` 交叉引用。`file:` 接受 sentinel 值，如 `embedded-in-manuscript` (v0.3.16+)，用於沒有可分離圖表來源檔案的基於 Word 的工作流程。 |
| `revision_history.yml` | 僅供附加的 audit trail，記錄每個修訂回合中哪些 claim 被新增 / 更改 / 刪除。 |

一個圍繞 Kizilkaya et al. 2025 (*"Toward HydroLLM"*) 建立的摘要層級範例 — 交叉連結到 [`example-topic-dossier.bib`](example-topic-dossier.bib) 條目 — 作為以下檔案提供：

- [`example-paper-memory-claims.yml`](example-paper-memory-claims.yml)
- [`example-paper-memory-figures.yml`](example-paper-memory-figures.yml)

The claims 檔案展示了 `gap` 狀態 + `gap_reason` 模式 (claim C5 — 摘要本身無法支持的範圍限制)。figures 檔案展示了 `embedded-in-manuscript` sentinel。

一個針對完整的 Kizilkaya 2025 手稿 (不僅是摘要) 的真實 `paper-memory-builder` 執行，會將這些摘要層級的 claim 替換為更細粒度的 Methods / Results claim，並用來自 `figures/` 目錄的具體路徑填充 `figures[].file`。

---

## Stage 4 — 從設計簡報到鷹架程式碼 (cookbook, 兩條路徑)

**輸入**: 來自 Stage 3a 的 [`example-design-brief.md`](example-design-brief.md)。 **輸出**: 在*你的*專案 repo 中的一組 prompt 檔案、腳本、分析模組和測試工具的鷹架 — 而不是一個具有固定 schema 的 YAML manifest。因為輸出是程式碼，Stage 4 刻意地**不是一個專門的 skill**；交接是操作者的膠水，並由一份 cookbook 來記錄。

該 cookbook 提供了[兩條路徑](example-design-to-build.md) — 根據鷹架的大小和工作的機械化程度來選擇：

| 路徑 | 時機 | 工具 |
|---|---|---|
| **A — Claude-direct** | ≤ 4 個檔案 或 重度依賴判斷 (架構、函式庫選擇、prompt-shape 迭代) | Claude 的 `Write` / `Edit` |
| **B — `codex-delegate`** | ≥ 5 個檔案 且 模式穩定 (測試骨架、baseline 變體、腳本化佈局) | `codex-delegate` skill；Codex 執行，Claude 審查 diff |

兩條路徑都從同一個 brief 開始，並產生結構相似的鷹架。決策在於 token 成本落在何處 — 對於單一檔案的情況，請參閱 `codex-delegate` 的「~1× (別費事)」anti-pattern。cookbook 記錄了每條路徑的**確切驗收指令** (例如 `python -m py_compile $(git ls-files '*.py')`, `grep -c "design_brief" ...`)，因此鷹架對 brief 的可追溯性是可機械驗證的。

一個混合的鷹架 (機械化檔案 + 依賴判斷的檔案) 會被拆分到兩條路徑；兩者在 commit 之前都會經過相同的 `code-reviewer` 檢查。

請參閱 [`example-design-to-build.md`](example-design-to-build.md) 以獲得完整的 cookbook，包括 codex brief 模板、包裝器調用、審查清單和 anti-patterns 表格。

---

## 把它組起來 —— 一份完整的文獻回顧交付品

上面的逐 skill 範例是片段。把 research-hub 文獻管線端到端跑一次 —— `search`
→ `literature-triage-matrix` → `research-design-helper` —— 這些片段就加總成
一份整合文件:一份 **文獻回顧
交付品** —— 完整九節,從 TL;DR、文獻清單,到逐篇摘要、跨論文綜合、附標記的
研究缺口分析、開放問題、建議下一步、參考文獻,以及來源說明。

一份完整的合成範例 —— 完整 9 節外形、可直接重用為範本 —— 位於
[`example-literature-review-deliverable.zh-TW.md`](example-literature-review-deliverable.zh-TW.md)
([English](example-literature-review-deliverable.md))。

---

## 上面範例**沒**展示的

- **真實 time-to-complete 數字** —— 看 `README.md` § 「Time + cost
  expectations」 拿到合理範圍。Output 長度跟 input 線性相關;5-paper
  triage matrix 通常 1-3 分鐘對話完成;6-comment reviewer response
  3-8 分鐘。
- **錯誤跟 edge case** —— 每個 skill 都有自己的 `## Limitations`。
  Skill 找不到預期 input 時(沒 `.paper/`、沒 Zotero 連線、沒 source
  bundle)會印清楚的「missing prereq」訊息、不會幻覺輸出。
- **真實研究資料** —— 上面的 matrix、banned-word audit、library
  report、Key Findings 都是合成的。Maintainer 真實 workflow 產出不會
  公布在這個 catalog(依 `## Limitations` 「no real maintainer
  artifacts」政策)。

Skill 產出跟上面形狀差很多時,開
[issue](https://github.com/WenyuChiou/ai-research-skills/issues) ——
那是真 bug,值得 report。
