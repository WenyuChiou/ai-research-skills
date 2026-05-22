# 詞彙表

Catalog 用幾個「AI 工具」一般領域不會有的慣例。在這定義一次,其他文件就
不用每次解釋。

語言:[English](glossary.md) | [繁中](glossary.zh-TW.md)

---

### Plugin(plugin)

Claude Code marketplace 的一筆 entry —— `.claude-plugin/marketplace.json`
裡的一列。Catalog 有 5 個:`research-workspace`、`academic-writing-skills`、
`zotero-skills`、`codex-delegate`、`gemini-delegate`。一個 plugin 可以包一個
或多個 skill。

### Skill

一支 `SKILL.md` 加 frontmatter(`name`、`description`)加可選的
`references/`、`evals/` 資料夾。Claude Code 的 auto-trigger 讀 `description`、
嘗試把你說的話 match 到對的 skill。Catalog 5 個 plugin 共 15 個 skill。

### Bare name(裸名)vs qualified name(限定名)

Claude Code 的 `Skill()` call 裡:

- **Bare name** —— 只給 skill 名字,例如 `Skill(skill="zotero-skills")`。
  Claude 按註冊順序解析第一個 match。
- **Qualified name** —— `<plugin>:<skill>` 形式,例如
  `Skill(skill="zotero-skills:zotero-skills")`。兩個 plugin 都 ship 同名
  skill(silent shadowing)時用,明說選哪一個。目前已知一個 case 看
  [`docs/verification.md` § 找到一個靜默的 skill-name 碰撞](verification.md#找到一個靜默的-skill-name-碰撞zotero-skills)。

### `.research/` 慣例

`research-hub` 系列 skill 讀寫的目錄,通常在研究專案 root。裡面:

- `project_manifest.yml` —— 專案層級狀態(問題、方法、階段)
- `design_brief.md` —— `research-design-helper` Socratic 段落跑完的產出
- `literature_matrix.md` —— `literature-triage-matrix` 的產出
- `experiment_matrix.yml`、`data_dictionary.yml` —— compressor 給未來 AI
  session replay 用的 output
- `orientation_memo.md` —— `research-project-orienter` 從上面 manifest
  產出的摘要

慣例的目的是讓 AI session 可以從上次中斷的狀態接起來,不用每次都重掃 repo。

### `.paper/` 慣例

`paper-memory-builder` 寫、`academic-writing-skills` 讀的目錄,在 manuscript
草稿 root。裡面:

- `claims.yml` —— 草稿裡每個 claim,有 id、status(`draft` / `supported`
  / `rejected` / `gap`)、`evidence_artifacts`
- `figures.yml` —— 圖表資料跟關鍵數字
- `reviewer_comments.md` —— reviewer 原始意見(你的 input)
- `reviewer_responses.md` —— point-by-point response 骨架
  (`academic-writing-skills` 的 output)
- `revision_history.yml` —— 不同 revision 輪之間 track changes

### Obsidian cluster

Obsidian vault 裡某個主題的子目錄(通常一篇 lit review 或一份 grant),
加上 `research-hub` 寫的 metadata(cluster index、per-paper note 骨架、
ingestion log)。Cluster 邊界就是 `research-hub auto` 一次 ingest 的單位。

### NotebookLM brief

NotebookLM 自動產出的 source summary。`notebooklm-brief-verifier` 檢查
brief 是真用了所有 source、還是偷偷漏掉某些(實際觀察到的 failure mode ——
看 `docs/verification.md` 裡 Kumar-only-brief 那個真實例子)。

### `research-hub auto`

一個 pipeline 指令(不是 skill),端到端 ingest 一個主題:search → dedupe
→ fetch → Zotero items → Obsidian cluster → NotebookLM upload → brief
generation。需要 `pip install research-hub-pipeline`。上面那層 skill 讓你
從 Claude Code 自然語言觸發這條 CLI。

### T1 / T2 / T3 verification tier(驗證等級)

每個 skill 在 `docs/verification.md` 跟 `catalog/skills.yml` 的驗證 grade。
權威定義在
[`docs/verification.md` § Verification tiers](verification.md#verification-tiers);
這份 glossary 條目只是短指針:

- **T1** —— Functional smoke test:用真實 input 呼叫 skill、檢查 output
  有沒有文件宣稱的行為。
- **T2** —— Binary / SKILL.md sanity:外部 CLI 版本探測加上一次端到端呼叫。
- **T3** —— SKILL.md 檢查:frontmatter、結構、參考檔。

對 prompt-based skill 而言,T3 不是「比 T1 弱」—— 是「不同的 check」,
不是嚴格層級。完整 nuance 看 verification 文件。

目前比例(看 `docs/verification.md` 2026-05-09 header):13 個 T1、1 個 T2。
Tier 跟 `verification_status`(pass/caveat/fail/not_yet)是兩個獨立 axis ——
兩個維度描述不同的事。

### Skill router / auto-trigger

Claude Code 把你的自然語言對應到 SKILL.md 的機制 —— 看 frontmatter
`description` 欄。Auto-trigger 挑錯 skill 時,可以明說 skill 名字
(*「用 `literature-triage-matrix` 比較這 5 篇」*)bypass router。

### Marketplace cache vs `~/.claude/skills/`

兩條 install 路徑、SKILL.md 落在兩個不同位置:

- **Marketplace install**(`claude plugin install …@ai-research-skills`)
  → `~/.claude/plugins/cache/ai-research-skills/<plugin>/<version>/skills/<skill>/`。
  用 `claude plugin list` 確認,**不是** `ls ~/.claude/skills/`。
- **Manual git clone**(`docs/install.md` 裡的 legacy 路徑)
  → `~/.claude/skills/<name>/`。

兩條都能用,只是落點不同。Catalog 的 canonical 推薦是 marketplace 路徑。

### Phase 數字(`Stage 1 → Stage 8`)

`docs/pipeline.md` 跟主 README skill 清單裡用的研究 workflow 階段。
每個 skill 標記像 *(Stages 3a, 4)* 是它在這 pipeline 上的位置:

- **Stages 1-2** —— Discovery + 文獻 triage
- **Stage 3a** —— 研究問題收斂
- **Stage 3b** —— 專案 manifest / context 壓縮
- **Stage 4** —— Design 對話
- **Stage 5** —— 實作(orient + replay context)
- **Stage 6** —— 跨切 delegation(Codex / Gemini handoff)
- **Stage 7** —— Manuscript memory + 寫作
- **Stage 8** —— 投稿 / reviewer response

完整圖看 `docs/pipeline.md`;README skill 列表的 stage 數字都指這。

---

文件裡的詞讓你卡住、又沒在這定義過,開
[issue](https://github.com/WenyuChiou/ai-research-skills/issues) ——
glossary 就是在這長大的。
