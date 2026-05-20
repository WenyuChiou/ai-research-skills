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
