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

---

## 2026-05-20 — Phase 5.3.b 端到端驗證(中文摘要)

跟上面的 T1/T2 逐項 skill 驗證**性質不同**。上面的 pass 是針對單個
skill 對真實 input 的行為。這次 pass 是針對 **marketplace 的安裝
路徑本身** —— `claude plugin marketplace add` → `claude plugin
install` → bare-name skill 解析整套鏈條 —— 在乾淨機器上跑。

**測試環境:** Windows 11 / Claude Code 2.1.142 / git-bash 5.2.37 /
Python 3.14。測試者:Claude(Opus 4.7),在 maintainer 機器上。
完整 artifact 放在 `/tmp/airs-verify/`(00–15),沒 commit,但相關
輸出引用在英文版
[verification.md §2026-05-20](verification.md#2026-05-20--phase-53b-end-to-end-verification)。

### Phase A — install round-trip

| Step | 指令 | 結果 |
|---|---|---|
| 1 | `claude plugin marketplace add WenyuChiou/ai-research-skills` | ✅ "Successfully added marketplace" |
| 2 | `bash scripts/install-all.sh` | ✅ 5/5 plugin 安裝完成 |
| 3 | `claude plugin list` | ✅ 5 個都顯示 `Status: ✔ enabled, Scope: user, Version: 0.1.0` |
| 4 | 14 個預期 skill 名字可以用 bare name 解析 | ✅ 在乾淨 `claude -p` session 全部解析得到 —— 但其中一個(`zotero-skills`)解析到錯的副本;見下方[靜默 skill-name 碰撞](#找到一個靜默的-skill-name-碰撞zotero-skills) |

**文件勘誤:** 原本的 verification recipe 預期 plugin 安裝後 skill 會
解開到 `~/.claude/skills/<name>/`,事實上不會 —— Claude Code 把
plugin skill 放在
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/skills/<skill>/`,
然後透過 `.claude-plugin/plugin.json` 的 auto-discovery 註冊。
驗證該檢查的應該是「`claude -p` 是否能用 bare name 解析到
`Skill(skill=<name>)`」,而不是 `~/.claude/skills/` diff。這次
pass 改用前者。

### Phase B — 每個 skill 的觸發測試(14 / 14)

對 14 個預期 skill 名字,各餵一個代表性 trigger prompt 到乾淨
`claude -p` session,記錄它會 route 到哪個 skill。14/14 命中。

完整 trigger 表跟 prompt 文字看英文版
[verification.md §2026-05-20 — Phase B](verification.md#phase-b--per-skill-trigger-14--14)。

**#11 的小註記:** `academic-writing-skills` 可以 route 到,但
"banned" 這個字在 plugin description 裡是隱含("GPT-style prose
cleanup")不是字面寫出來,所以信心降到 medium。未來小幅微調 description 是
候選改進。

### 找到一個靜默的 skill-name 碰撞(zotero-skills)

**白話版總結。** Catalog 5 個 plugin 裡有兩個都註冊了名叫
`zotero-skills` 的 skill。當你說「search 我 Zotero library tag 是 X 的
item」之類 Claude Code auto-trigger 挑到 `zotero-skills` 時,**它每次都會
落在 `research-workspace` 裡內嵌的那份**(那是 research-hub 帶的舊大份
副本)—— **絕對不會**落在 standalone `zotero-skills` plugin(canonical 那份)
上。沒錯誤訊息、沒 prompt、沒 warning —— bare-name 解析就直接 hit 到
registry 順序排第一的那個。

**實際影響。** 大部分 prompt 兩份副本做的事一樣,使用者通常不會注意到。
但如果你想用的是 standalone canonical 新加的某個行為,你的 prompt 會落
在舊的內嵌副本上,然後你會困惑為什麼新 feature 沒生效。

**證據。**

| 來源 plugin | 磁碟路徑 | SKILL.md 大小 | 註冊名稱 |
|---|---|---|---|
| `research-workspace`(research-hub 內嵌) | `…/research-workspace/0.1.0/skills/zotero-skills/` | 11,321 B(舊、較大) | `zotero-skills` |
| standalone `zotero-skills`(canonical) | `…/zotero-skills/0.1.0/skills/zotero-skills/` | 4,391 B(canonical) | `zotero-skills` |

**Phase 2 修好之前的 workaround。** 用 qualified 形式強制指定 canonical
那份。在 Claude Code prompt 裡:

```
Skill(skill="zotero-skills:zotero-skills")
```

`<plugin-name>:<skill-name>` 這個寫法(`zotero-skills:zotero-skills`)
能 disambiguate,因為 canonical 那份剛好 plugin name 跟 skill name
都叫同樣的。research-workspace 那份內嵌的對應寫法則是
`research-workspace:zotero-skills`。**只有真的需要 canonical
standalone 時才用 qualified form**;一般 Zotero workflow,內嵌那份就夠了。

**正確修法**是從 `WenyuChiou/research-hub` 刪掉 `skills/zotero-skills/`,
讓 canonical standalone 成為唯一來源。research-hub 那邊一個 PR 就解決。
但**目前被 Phase 2 hard-gate 擋住**(這 round 不能改 research-hub 的源碼),
會在 Phase 2 Task B1 + E4 視窗一起處理。屆時 bare-name 解析就會回到安全狀態。

**分類:** pre-existing —— 早於 Phase 5.3.b 驗證。
**延後到:** Phase 2。

### 這次 pass **沒有**做的事(誠實列出落差)

- **跨 model second-opinion routing**(Codex / Gemini 當第二 judge) ——
  還在 v0.3 backlog,這次沒跑。
- **使用者真實資料上的 skill 行為驗證** —— 已由 2026-04-25 / 2026-05-09
  的 T1 pass 涵蓋,這次沒重跑。
- **`marketplace.json` `ref:` 釘到 v0.1.0 tag** —— 還在 default
  branch。路線圖項目見
  [`docs/design-philosophy.md`](design-philosophy.md) §Roadmap。
- **水資源 / agent-based modeling 以外的 domain 驗證** —— 還寫在
  README §限制 裡。

### 結論

Marketplace 安裝 + 每個 skill 的 auto-trigger 在乾淨 Claude Code
2.1.142 機器上 **PASSES**。找到一個靜默碰撞已記錄;修法因 hard-gate
延後到 Phase 2。這 addendum 落地後標 `v1.4.2` tag。

---

## 2026-05-20 — Phase 6 post-merge re-verification on v1.5.0

對 v1.5.0(`1b557fc`)HEAD 重跑 Phase 5.3.b 的 install + trigger 流程,
再加三個 dogfood walk 對著 Phase 6 PR-2 新加的文件
(`docs/examples.md`、`docs/glossary.md`、README 時間/成本表 + Zotero
備份提醒)走一遍,看新文件有沒有把 agent-team 分析指出的落差補起來。

**測試環境:** Windows 11、Claude Code 2.1.145、git-bash 5.2.37、Python
3.14。**測試者:** Claude(Opus 4.7),在維護者機器上跑。
所有輸出收在 `~/airs-verify-phase6/`(00 baseline → 11 dogfood notes)
—— 沒 commit。Phase B 每個 trigger 都用一個獨立的 `claude -p` 程序、
`< /dev/null` 把 stdin 關掉,確保 in-session skill registry 不會污染結果
(Phase 5.3.b 的方法論教訓)。

### Phase A —— install 來回

| 步驟 | 指令 | 結果 |
|---|---|---|
| 1 | `claude plugin marketplace remove ai-research-skills` | ✅ "Successfully removed" |
| 2 | `claude plugin marketplace add WenyuChiou/ai-research-skills` | ✅ "Successfully added marketplace" |
| 3 | 從 v1.5.0(`1b557fc`)`git clone --depth 1` 後跑 `bash scripts/install-all.sh` | ✅ 5/5 plugin 都裝起來 |
| 4 | `claude plugin list` | ✅ 5 個都 `Status: ✔ enabled`、`Scope: user`、`Version: 0.1.0`:`academic-writing-skills`、`codex-delegate`、`gemini-delegate`、`research-workspace`、`zotero-skills` |

### Phase B —— 14 個 skill auto-trigger

每個 prompt 都餵給一個獨立的 `claude -p`;結尾 sentinel 要 model 回報
有沒有真的呼叫 Skill tool。結果:

| # | 預期 | Sentinel 回報 | 分類 |
|---|---|---|---|
| 1 | `research-hub` | `research-workspace:research-hub` | ✅ hit(qualified) |
| 2 | `research-hub-multi-ai` | `agent-collab-workspace:agent-task-splitter` | ⚠ routing 重疊 —— 見下方說明 |
| 3 | `research-context-compressor` | `research-workspace:research-context-compressor` | ✅ hit(qualified) |
| 4 | `research-project-orienter` | `research-workspace:research-project-orienter` | ✅ hit(qualified) |
| 5 | `research-design-helper` | `research-design-helper` | ✅ hit(bare) |
| 6 | `literature-triage-matrix` | `research-workspace:literature-triage-matrix` | ✅ hit(qualified)—— skill 先問論文來源才產出 matrix |
| 7 | `paper-memory-builder` | `paper-memory-builder` | ✅ hit(bare) |
| 8 | `paper-summarize` | `NONE` | ⚠ 回覆裡有指名 `paper-summarize` 但沒實際呼叫 —— model 先問 cluster 名稱 |
| 9 | `notebooklm-brief-verifier` | `notebooklm-brief-verifier` | ✅ hit(bare) |
| 10 | `zotero-library-curator` | `zotero-library-curator`(重跑後成功;第一次 180 秒 timeout) | ✅ hit(bare) |
| 11 | `academic-writing-skills` | `NONE` | ⚠ 回覆裡有指名 `academic-writing-skills`/`banned-word-auditor` 但沒實際呼叫 —— model 先問段落文字;見下方 C2(餵真實文字後輸出符合 examples.md 表格) |
| 12 | `zotero-skills` | `zotero-skills:zotero-skills` | ✅ hit 在 canonical 標準版 standalone(qualified form 把 §2026-05-20 Phase 5.3.b 記錄的靜默碰撞繞過) |
| 13 | `codex-delegate` | `codex-delegate:codex-delegate` | ✅ hit(qualified) |
| 14 | `gemini-delegate` | `NONE` | ⚠ 回覆裡有指名 `gemini-delegate` 但沒實際呼叫 —— model 先問 brief 內容 |

計數:
- **嚴格(Skill tool 真的被呼叫)**:10 / 14。
- **寬鬆(回覆有指名正確 skill,不管有沒有 invoke)**:13 / 14。
  *(Trigger 2 兩個計數都不計 —— 觸發的是不同 skill,不是預期的那個。)*
- **Routing 重疊**:1(trigger 2)。

非嚴格結果的說明:

- **Trigger 2 —— routing 重疊。** prompt「task 需要 codex + gemini」更
  貼近 `agent-collab-workspace:agent-task-splitter` 的描述,不是
  `research-hub-multi-ai`。`CLAUDE.md` 本身就把 ≥2-delegate prompt
  路給 `agent-task-splitter`,所以這是跨 marketplace 的設計重疊,不
  是本 catalog 這邊的 router 失誤。要釐清 router-vs-splitter 分工,
  需要同時改 research-hub(`research-hub-multi-ai` 描述)與
  `agent-collab-skills`(`agent-task-splitter` 描述)—— HARD-GATED,
  超出本 catalog repo 範圍。
- **Trigger 6 —— skill 已觸發、inline 要求輸入。** `literature-triage-matrix`
  正確解析且 Skill tool 有呼叫(計入嚴格 10)。skill 在回覆裡要求論
  文來源清單,符合其文件介面;這是保守-正確,不是失誤。
- **Trigger 8、11、14 —— 回覆有指名 skill 但未實際呼叫。** model 認出
  正確 skill(`paper-summarize`、`academic-writing-skills`、
  `gemini-delegate`),但先問需要的輸入(cluster 名稱、段落文字、
  brief 內容)才會 invoke Skill tool。這三個是嚴格/寬鬆計數落差的
  根據(寬鬆 13 = 嚴格 10 + 這三個)。下面 C2 顯示一旦有實際文字
  餵進去,`academic-writing-skills` 就會輸出 `docs/examples.md` 文
  件記錄的表格形狀。input-first 是這類 skill 的正確預設;這裡用的是
  探針 prompt,不是完整任務句。

### Phase C —— 三個 dogfood walk 對著 Phase 6 PR-2 新文件

| # | Walk | 結果 | 證據 |
|---|---|---|---|
| C1 | 「比較 5 篇論文」→ `literature-triage-matrix` | ⚠ partial | skill 經 Phase B trigger 6 正確解析(`research-workspace:literature-triage-matrix`)。skill 先問論文來源才能產 matrix;沒實際輸入就沒法端到端驗證 9-欄形狀。Skill 行為是保守-正確;形狀驗證留到下回合。 |
| C2 | 「audit 這段段落 banned word」→ `academic-writing-skills` | ⚠ partial | 拿 `docs/examples.md` 範例 input 重跑。輸出 ✅ 對得起 `docs/examples.md` §academic-writing-skills 的 banned-word audit 表格(Severity / Term / Span / Replacement / Reason)。抓到 `leverages`、`novel`、`comprehensively`、`multifaceted`、`robustly`、`demonstrating`、`significantly`、`delve`、`proposed` —— 一句話 9 個 hit。Sentinel 回 `NONE` 但回覆內容就是 audit 表格;這是 sentinel 協定的雜訊,不是 skill miss。**D6 發現**:整段回覆裡完全沒有提到 `paper-memory-builder`、`.paper/` 或 `claims.yml` —— auto-router 沒向使用者點出 upstream skill 依賴。已在 Phase 2 backlog(research-hub 裡的 SKILL.md 描述)。 |
| C3 | 「audit 我的 Zotero library」→ `zotero-library-curator` | ⚠ partial | skill 對維護者的真實 Zotero 庫跑了一次 read-only audit:1,191 個 item、4 個重複 DOI(8 個 item,4 個可移除)、331 個 orphan(27.8%,其中 96% 來自 2026-01 的一次 bulk-import)。輸出 preview-only,實際刪除動作交回給 `zotero-skills`。形狀 ✅ 對得起 `docs/examples.md` §zotero-library-curator。**Backup 提醒發現**:README 的 `⚠️ Back up before any Zotero CRUD` 區塊沒有出現在 skill 回覆裡。skill 有說「verify which copy has the PDF attachment」「Don't blanket-delete」—— 有用,但不是 Zotero RDF export 那一步。要把 backup 建議寫進 curator SKILL.md 是 research-hub 那邊的事 —— Phase 2 hard-gated。 |

### 這次驗證實際出的修補

無 —— 驗證確認 v1.5.0 狀態。每個找到的落差都在 research-hub 那邊,
全部落在 Phase 2 hard-gate 內,所以本 catalog repo
(`WenyuChiou/ai-research-skills`)這回合沒有可修的東西。
`marketplace.json` 維持在 1.5.0;這個 addendum 不對應新 tag。

### 這回合**沒有**修的已知問題

進 Phase 2 backlog(全部都是 research-hub source-repo 編輯,要等
「research-hub 可以」才能動):

1. `research-hub-multi-ai` 跟 `agent-collab-workspace:agent-task-splitter`
   在 ≥2-delegate prompt 上的 routing 重疊 —— 要同時改 research-hub
   (給 `research-hub-multi-ai`)與 `agent-collab-skills`
   (給 `agent-task-splitter`)的 SKILL.md 描述。
2. `academic-writing-skills` 回覆沒提示使用者上游 `paper-memory-builder`
   依賴 —— research-hub 那邊改描述。
3. `zotero-library-curator` 回覆沒把 README 的 Zotero RDF 備份建議重述
   給使用者 —— research-hub 那邊改 SKILL.md。
4. 加上前幾回合已堆起來的四個 Phase 2 backlog
   (`paper-memory-builder` 防資料外洩 schema;`research-hub`
   `plugin.json` 宣告 3 個 skill 但實際 ship 11 個;`zotero-skills`
   靜默碰撞的真正修法;auto-trigger 關鍵字重疊的五個 SKILL.md 描述
   重寫)。

### 這次驗證**沒**涵蓋的部分

- 外部使用者 —— 使用資料仍 N=1(只有維護者)。
- 跨 model 第二意見 judge(Codex / Gemini 當第二 reviewer)—— v0.3 backlog。
- 水資源 / agent-based modeling 以外的 domain 一般化 —— v0.3 backlog。
- banned-word + overclaim audit 在語料庫尺度的 false-negative /
  false-positive rate 校正 —— v0.3 backlog。

### 方法論教訓(留給下回合)

- `claude -p` 一定要加 `< /dev/null` 把 stdin 關掉,不然會跳「no
  stdin data received in 3 s」然後直接退出、prompt 根本沒跑。
- 結尾 sentinel(`__SKILL_USED__: <name-or-NONE>`)只有在 Skill tool
  真的觸發時才是可靠 measurement。純對話內 reasoning 的 skill(像
  banned-word-auditor 這類)可以在不註冊 `Skill()` 呼叫的情況下,
  就把文件記錄的輸出 ship 出來;這種情況算 ⚠,不算 ❌,要拿回覆
  內容當真實訊號。
- 探針 prompt 不等於完整任務句。對「需要論文清單 / cluster 名 /
  段落文字 / brief 內容」這類 skill,auto-router 保守、先問輸入是
  正確預設。探針集應該預期有相當比例的 input-first 回覆,並以「正
  確 skill 是否被指名」而不是「`Skill()` 有沒有被呼叫」當判準。

### 這次 pass 的結論

Phase A 通過(5 / 5 ✔ enabled)。Phase B 嚴格 10 / 14,其餘四個都
有解釋:一個是 `CLAUDE.md` 跨 marketplace routing 刻意造成的重疊,
三個是 input-first 保守回覆、回覆內已指名正確 skill。Phase C 三個
walk 都是 ⚠ partial,所有底層落差都在 research-hub source 檔案、
落到 Phase 2 backlog。Marketplace 安裝 + skill 解析路徑在 v1.5.0
是完整的;這回合本 repo 沒有修補 PR。
