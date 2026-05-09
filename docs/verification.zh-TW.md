# Skill 驗證報告（zh-TW 摘要）

**最近一次跑：** 2026-05-09（delegate 清理 pass；接續 2026-04-25 T1 升級 pass）
**測試環境：** Windows 11、Python 3.14、`research-hub-pipeline` 0.45.0、`codex-cli` 0.121.0、`gemini` 0.38.2。
**測試者：** Claude（Opus 4.7），對使用者真實工作區（`knowledge-base` 1100+ 篇論文、活躍 Zotero 庫、現役 NotebookLM session）執行。

完整逐項命令、預期、實際輸出與證據路徑見英文版 [verification.md](verification.md)。本檔提供中文使用者的快速摘要與本次 pass 變更紀錄。

[`catalog/skills.yml`](../catalog/skills.yml) 的 `verified_on` 欄位是機器可讀的真實來源。

## 本次 pass 變更

2026-04-25 那次 pass 把 6 個純推理 skill 從 T3 升到 **T1**：建好真實 5 篇論文 test corpus（AI agents + 社會互動主題，由 `research-hub search` 抓取），逐個 skill 端到端跑過。所有產出 commit 在 `test-corpus/ai-agents-social-interaction/`。

2026-05-09 這次 pass 清掉剩下兩個非 T1 項目：

- **codex-delegate**：caveat ⚠ → ✓ pass（T2 → T1）。先前 `gpt-5.5` model mismatch 的 caveat 已由上游 PR [WenyuChiou/codex-delegate#1](https://github.com/WenyuChiou/codex-delegate/pull/1) 在 skill 自己的 SKILL.md 解掉：新增 Model Selection（`-m gpt-5.4` 與 `~/.codex/config.toml` override）、Non-Interactive Shell Note（`< /dev/null` 要求）、Quota Fallback（`.fallback_claude` sentinel）、Multi-Agent Coordination（leaf 角色）、Five Workflow Patterns 五段；同時 `references/patterns.md` 提供可貼上的 prompt 模板。
- **paper-summarize**：T2 thin → T1。上游 PR [WenyuChiou/research-hub#31](https://github.com/WenyuChiou/research-hub/pull/31) 把 skill 既有的 23 個端到端測試（stub LLM、真實 Obsidian 寫入、Zotero rollback 不變式）寫進 SKILL.md 的 `## Verification` 區塊。先前的 T2 評等是文件落差，不是覆蓋率落差 — 測試套件其實已端到端覆蓋。
- **research-hub-multi-ai**：保留 T1，但角色重新定位。上游 PR [WenyuChiou/research-hub#30](https://github.com/WenyuChiou/research-hub/pull/30) 把它定位為 router / leaves 架構中的 router；現在只有「同一回合需要 ≥2 個 delegate」才會觸發，並寫出 `.coord/multi_ai_plan.md`。先前 9 步 routing 計畫的產物 `test-corpus/ai-agents-social-interaction/.research/multi-ai-routing-decision.md` 仍是 router 化前的有效歷史 artifact，保留。

## 驗證等級

- **T1 — 功能 smoke test。** 用真實輸入啟動 skill；檢查輸出。能抓到「CLI 跑不起來」與「指令語法跟文件 drift」。
- **T2 — Binary / SKILL.md 健康檢查。** 外部 CLI 版本探測 + 一次端到端呼叫。給「價值在外部 CLI」的 delegate skill 用。
- **T3 — SKILL.md 內部審查。** Frontmatter、結構、reference 檔案檢查。給純推理 skill 用 — 這類 skill 的 runtime 是 Claude 自己的對話 context，沒法獨立「跑」，但內部一致性與支援 tooling 仍可驗。

T3 不代表較弱，只是反映純推理 skill 性質不同。對這類 skill 最強的證據，是 catalogued 行為符合使用者實際在做的事（例如 `banned_words.md` 真的含有使用者自己 `CLAUDE.md` 描述的詞）。

## 14 個 skill 總覽（簡表）

| # | Skill | Tier | 狀態 | 證據摘要（詳見英文） |
|---|---|---|---|---|
| 1 | `research-hub` | T1 | ✓ pass | doctor 全綠 + 真實 search 回傳 3 筆結果；test corpus 全套 ingest |
| 2 | `literature-triage-matrix` | T1 | ✓ pass | `literature_matrix.md`（5 篇 × 9 欄比較表） |
| 3 | `notebooklm-brief-verifier` | T1 | ✓ pass（雙模式） | research-hub-managed 與 manual fallback 同樣抓到 1/5 source coverage 的真實 NLM 缺漏 |
| 4 | `research-context-compressor` | T1 | ✓ pass | `.research/{project_manifest,experiment_matrix,data_dictionary}.yml` 都 parse 過 |
| 5 | `research-project-orienter` | T1 | ✓ pass | `orientation_memo.md`（讀 0 個 `.research/` 外的檔案） |
| 6 | `research-hub-multi-ai` | T1 | ✓ pass | router 化前 9 步 routing 計畫 + 本次重新定位為 ≥2 delegate router |
| 7 | `paper-memory-builder` | T1 | ✓ pass | `claims.yml` 5 個 claim 抽出；`figures.yml` 空（誠實的 abstract-only run） |
| 8 | `paper-summarize` | T1 | ✓ pass | 23 個端到端測試（stub LLM + 真 Obsidian + Zotero rollback），已寫進 skill SKILL.md |
| 9 | `academic-writing-skills` | T1 | ✓ pass | banned-word 稽核找到 `leveraging`、`crucial`、`highlight`（符合 `banned_words.md`） |
| 10 | `zotero-skills` | T1 | ✓ pass | local API 回傳 `我的文獻庫` 真實 collection；test corpus ingest 走過 |
| 11 | `codex-delegate` | T1 | ✓ pass | `gpt-5.5` caveat 已解；wrappers 預設 `-m gpt-5.4`；leaf 角色寫進 SKILL.md |
| 12 | `gemini-delegate` | T2 | ✓ pass | `gemini -p "Say only PING"` 回傳 `PING` |
| 13 | `research-design-helper` | T1 | ✓ pass | `design_brief.md` 5 段都填好，含 Cliff's δ 等具體可證偽條件 |
| 14 | `zotero-library-curator` | T1 | ✓ pass | 抓出真實 vault 的 10 個重複 DOI、44 對 case-only 重複 tag、435 個 sparse tag |

**統計：** 14 ✓ pass · 0 ⚠ caveat · 0 ✗ fail · 0 not_yet · **14 個 skill 中 13 個達到 T1**，剩下 1 個（gemini-delegate）保持 T2 — 對「價值在外部 CLI」的 delegate skill 來說，T2 就是合適的等級。

## 進一步資訊

- **完整逐項命令、預期、實際輸出與分支判斷：** [verification.md](verification.md)（英文）
- **未結 follow-up：** [verification.md#open-follow-ups](verification.md#open-follow-ups)（英文）
- **整體 pipeline 與 stage 對應：** [pipeline.md](pipeline.md) 或 [pipeline.zh-TW.md](pipeline.zh-TW.md)
- **Skill catalog 機器可讀來源：** [`catalog/skills.yml`](../catalog/skills.yml)
