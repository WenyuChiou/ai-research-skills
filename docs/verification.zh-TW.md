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
