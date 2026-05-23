# AI Research Skills

> 一套包含 15 個 Claude Code skills 的組合包，專為完整研究工作流程而設計——
> 從文獻探討 → 研究設計 → 實作 → 執行 → 論文撰寫 → 投稿，
> 並內建跨 AI 協作代理功能。

語言：[English](README.md) | [繁中](README.zh-TW.md) ·
[Pipeline](docs/pipeline.md) ·
[範例](docs/examples.md) ·
[詞彙表](docs/glossary.md)

**這是什麼。** 這是一套包含五個 Claude Code plugins（總共 15 個 skills）的組合，專為在研究流程中深度使用 AI 的研究人員設計——包括研究生、博士生、博士後及研究支援人員。這些 Skills 是符合 [agentskills.io](https://agentskills.io) 規範的 Markdown 檔案；它們會根據您在 Claude Code 中的語句自動觸發，並且也能載入到 Codex CLI / Gemini CLI / Cursor / Windsurf / Hermes 中（詳見 [§6 相容性 (Compatibility)](#6-相容性-compatibility)）。

<sub><a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a> <a href=".research/hermes-compatibility-audit.md"><img alt="agentskills.io spec compliant" src="https://img.shields.io/badge/agentskills.io-spec_compliant-2DA89C"></a> <a href=".research/hermes-compatibility-audit.md"><img alt="Hermes 0.13.0 skill-load verified" src="https://img.shields.io/badge/Hermes_0.13.0-skill--load_verified-2DA89C"></a></sub>

> 📚 本項目為 [agentic AI 學習路線圖](https://github.com/WenyuChiou/awesome-agentic-ai-zh) 的一部分
> ——收錄於 §13–14 (研究工作流程)。

---

## 1. 安裝 (Install) — 取得這套 skills

**懶人包 — 30 秒搞定：**

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
```

兩個指令。這樣您就安裝了 11 個 `research-hub` skills — 其中 6 個
(`literature-triage-matrix`, `research-design-helper`,
`research-context-compressor`, `research-project-orienter`,
`paper-memory-builder`, `research-hub-multi-ai`)
是純推理型，可以立即使用。另外 5 個則需與外部工具（Zotero /
NotebookLM / `research-hub-pipeline` Python CLI）搭配，需要進行個別設定。

> **正在 Claude / ChatGPT 中閱讀？** 將整個 §1 貼給您的 AI 助理，然後說：*"幫我安裝全部 5 個 plugins 並驗證。"*
> 下方的指令是自給自足的 — AI 助理可以一步步執行，無需額外查詢。

**漸進式安裝 — 每一步完成後，已安裝的功能即可使用：**

```bash
# 1. Marketplace + 11 個 research-hub skills (6 個純推理型，可立即使用)
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills

# 2. 論文寫作 — claim-evidence audit, banned-word, reviewer response
claude plugin install academic-writing-skills@ai-research-skills

# 3. Zotero CRUD (請先在 Zotero 桌面版啟用 local API — 見 docs/setup-guide.md §C)
claude plugin install zotero-skills@ai-research-skills

# 4. 多 CLI 代理 (請先安裝 codex / gemini CLI 執行檔)
claude plugin install codex-delegate@ai-research-skills
claude plugin install gemini-delegate@ai-research-skills

# 5. 文獻 pipeline 自動化 (research-hub skills 背後的 Python CLI)
pip install research-hub-pipeline
research-hub setup
```

一次安裝全部 5 個 plugins：

```bash
bash scripts/install-all.sh        # macOS / Linux / git-bash
pwsh scripts/install-all.ps1       # Windows PowerShell
```

**驗證：**

```bash
claude plugin list
# 預期輸出：5 個 plugins，名稱皆以 @ai-research-skills 結尾，且狀態為 ✔ enabled。
```

從 Marketplace 安裝的 plugins **不會** 被解壓縮到 `~/.claude/skills/`
— 它們位於
`~/.claude/plugins/cache/ai-research-skills/<plugin>/<version>/skills/<name>/`
路徑下，Claude Code 透過每個 plugin 的
`.claude-plugin/plugin.json` 檔案來發現它們。僅用 `ls ~/.claude/skills/`
**無法** 確認 Marketplace 是否安裝成功 — 請使用 `claude plugin list`。

各 plugin 的詳細資訊：[docs/install.md](docs/install.md) ·
若尚未設定 Python / Zotero / Git？請從
[docs/setup-guide.md](docs/setup-guide.md) 開始。

<details>
<summary><b>我想 clone 這個 repo</b> (貢獻者 / 除錯用)</summary>

```bash
git clone https://github.com/WenyuChiou/ai-research-skills.git
cd ai-research-skills
```

這個 catalog 是一個 **註冊中心 (registry)**，不是一個 monorepo。每個
plugin 的原始碼都放在各自的 repo 中：

- `github.com/WenyuChiou/research-hub` — 11 個 `research-workspace` skills
- `github.com/WenyuChiou/academic-writing-skills` — 1 個 skill
- `github.com/WenyuChiou/zotero-skills` — 1 個 skill
- `github.com/WenyuChiou/codex-delegate` — 1 個 skill
- `github.com/WenyuChiou/gemini-delegate-skill` — 1 個 skill

如果您想修改某個 plugin，請 clone **其** 原始碼 repo，而不是這個
catalog。本 catalog 只維護 `marketplace.json`、文件、圖片資源以及
catalog 層級的 `CHANGELOG.md`。

</details>

---

## 2. 為什麼存在這個 catalog (Why this catalog exists)

您可能已經很熟悉 AI 在研究上的痛點。以下五點是這個 catalog
真正能解決的問題——不僅僅是紙上談兵。

### P1 — "我每次跟 AI 開新對話都要重講一次"

您打開一個新的 Claude / ChatGPT 對話，想繼續昨天的工作，但模型對您的研究問題、已完成的實驗、基準模型，或是上週找到的 gap 一無所知。您花了前十分鐘重新輸入所有內容。明天，又得再來一次。

### P2 — "AI 會自信地給我不存在的論文"

模型寫出 *"如 Chen 等人 (2024) 所證明的…"* — 但這篇論文根本不存在。您這次抓到了（這次）。在回覆審稿人意見時，一個幻覺引文就足以讓您的稿件被直接拒絕。

### P3 — "我讀了 50 篇論文，還是不知道哪個 gap 值得做成一篇學位論文"

有三個問題需要結構化的答案：(1) 這個 gap 真的還存在嗎？ (2) 填補這個 gap 是真正的貢獻，還是只是現有工作的排列組合？ (3) 我有足夠的時間完成它嗎？那些只產生一段「研究缺口摘要」的工具，根本沒有回答任何一個問題。

### P4 — "AI 寫出來的論文一看就是 AI 寫的"

*"此外"、"值得注意的是"*，充滿閃爍其詞、沒有明確主張的句子。審稿人（以及資深共同作者）看兩段就聞到那股味道，然後您的稿件在他們待辦事項列表中的優先級就下降了。

### P5 — "在 Claude / Codex / Gemini 之間切換，每次切換都像失憶"

您用 Claude 設計 prompt，交給 Codex 建立程式碼骨架，再切換到 Gemini 進行長文脈的論文綜合。每一次切換都要花五分鐘重新說明背景。跨 AI 的交接正是時間真正消失的地方。

---

### 三個設計原則，應用於 15 個 skills

這個 catalog 圍繞三個有力的核心理念構建，而不只是一張功能清單：

| 原則 | 功能 | 解決的痛點 |
|---|---|---|
| **1. Manifests** (`.research/`, `.paper/`) | 研究狀態儲存在受版本控制的 YAML / Markdown 檔案中。新的 AI 對話 session 會讀取 manifest 並自行了解背景 — 您不必再重覆解釋。 | P1, P5 |
| **2. 帶有 anti-leakage 規則的 Schemas** | 每個跨 skill 的產出物都有一個 YAML schema。一個 `evidence_artifacts` 為空的 claim **會被強制** 標記為 `status: gap` 並附上 `gap_reason` — 絕不會是 `supported`。一個 `verdict: do-not-pursue` 的候選主題會與 `worth-pursuing` 的主題在結構上被分開。下游工具會拒絕傳遞過度自信的輸出。 | P2, P3, P4 |
| **3. Character-driven routing (依任務性質分流)** | 機械性的批量工作 → Codex。長文脈 / 中日韓語 → Gemini。判斷 / 治理 → Claude。路由工具 (`research-hub-multi-ai`) 會寫一個協調檔案，讓每個代理只讀取自己的任務簡報，而非上層的完整文脈。 | P5 |

下方八階段的 pipeline 就是將這三個原則應用於真實研究工作流程的成果。

![15 個 AI skills 對應到 8 個研究工作流程階段，並有可於各階段使用的跨領域工具 (codex-delegate, gemini-delegate, research-hub-multi-ai)](docs/img/pipeline-overview.zh-TW.png)

---

## 3. The pipeline — 每個階段為下一階段交付什麼

從 *"我應該讀讀關於 X 的資料"* 到 *"稿件已送出"* 的八個階段。每個階段的輸出就是下一階段的輸入 — 交接是機械式的，而非憑感覺。

| # | 階段 | Skill(s) | 輸出 → 下一階段 |
|---|---|---|---|
| 1 | **找文獻** | `research-hub`, `paper-summarize` | `.bib` + 每篇論文的重點筆記 → 階段 2 |
| 2 | **整理比較、找 gap** | `gap-to-topic`, `literature-triage-matrix`, `notebooklm-brief-verifier`, `zotero-library-curator` | `topic_dossier.gaps.yml` (包含 `verdict`, `verdict_reason`) → 階段 3a |
| 3a | **框問題** | `research-design-helper` | `design_brief.md` (frontmatter `source: gaps.yml#G2`, `gap_verdict`) → 階段 3b + 階段 4 |
| 3b | **寫計畫** | `research-context-compressor`, `research-project-orienter` | `project_manifest.yml` (`provenance.from_gap`) → 階段 4–8 |
| 4 | **設計與建模** | *cookbook* — `codex-delegate` 用於 ≥5 個檔案的骨架，Claude 直接用於 ≤4 個檔案或判斷性工作 | 您專案 repo 中的程式碼 (見 [cookbook](docs/example-design-to-build.md)) → 階段 5 |
| 5 | **執行、校正、驗證** | `research-context-compressor`, `research-project-orienter` | `.research/` run manifests 讓未來的 AI sessions 省去重新掃描 → 階段 6 |
| 6 | **視覺化與結果解讀** | `codex-delegate`, `gemini-delegate` | 圖表 + 分析腳本 → 階段 7 |
| 7 | **論文撰寫與修改** | `paper-memory-builder`, `academic-writing-skills` | `.paper/claims.yml` (包含 `status` enum + anti-leakage) → 階段 8 |
| 8 | **投稿、回覆審查、收尾** | `academic-writing-skills`, `research-context-compressor` | reviewer-response.md, 帶有版本標籤的 manifests → 完成 |

跨 skills 的交接 (階段 2 → 3a → 3b → 8; 階段 7 → 8) 是以 **YAML schemas** 文件化的，而非自由文本。下游 skill 可以拒絕處理格式錯誤的交接——當 schema 違規可能傳播時（例如，`status: gap` 的 claims 沒有 `gap_reason` 會在階段 7 被拒絕），它確實會這麼做。

**跨領域 (所有階段):** `codex-delegate`, `gemini-delegate`, `research-hub-multi-ai`。這三者位於 pipeline 旁側，而非在 pipeline 上 — 任何階段都可以透過它們來處理機械性 / 長文脈 / 多 AI 的工作。

完整的流程敘述 + 各階段工具表：[docs/pipeline.md](docs/pipeline.md)。

---

## 4. 使用方法 (Use it)

### 找到你的起點

如果你不想讀完整 pipeline,可以直接從目標切入:

| 你目前的目標 | 你會用到的 skills |
|---|---|
| **找文獻、比較文獻** | `research-hub` + `literature-triage-matrix` |
| **寫論文 / 改稿** | `paper-memory-builder` + `academic-writing-skills` |
| **管理研究專案** | `research-design-helper` + `research-context-compressor` + `zotero-library-curator` |

> **協助別人用 AI 做研究** (圖書館員 / RA / 指導老師)?
> 不需要安裝 — 把這份 README + [docs/install.md](docs/install.md) 給他們即可。

完整 pipeline 敘述:[docs/pipeline.zh-TW.md](docs/pipeline.zh-TW.md)。

### 或者,直接描述你想做的事

用自然的語言描述您想做的事 — Claude Code 會將您的語句與對應的 skill 進行匹配。您不需要記住 skill 的名稱。

| 當您說… | 觸發的 Skill |
|---|---|
| "比較這 5 篇論文的方法、數據、限制" | `literature-triage-matrix` |
| "這個 gap 是否值得做成一篇學位論文？帶我走過三個檢核關卡" | `gap-to-topic` |
| "在我開始寫程式前，帶我走一遍我的研究設計" | `research-design-helper` |
| "審核這段文字，檢查是否有禁用詞和過度宣稱" | `academic-writing-skills` |

完整的觸發對照表 (15 列)：[docs/skill-directory.md](docs/skill-directory.md)。
如果自動觸發選錯了 skill，可以直接指名：
*"用 `literature-triage-matrix` 比較這 5 篇論文。"*

### 全部 15 個 skills

<details>
<summary><b>來自 <code>research-hub</code> (11 個 skills)</b> — 一次安裝，全部擁有</summary>

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md) — 在 Zotero / Obsidian / NotebookLM 之間搜尋、匯入、整理論文。*(階段 1, 2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) — 根據方法、數據、主張、限制建立比較矩陣。*(階段 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) — 驗證 NotebookLM 的簡報是否與原始資料包一致。*(階段 2)*
- [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md) — 審核 Zotero，提出清理建議 (若無 `zotero-skills` 則僅為預覽)。*(階段 2)*
- [`gap-to-topic`](https://github.com/WenyuChiou/research-hub/blob/master/skills/gap-to-topic/SKILL.md) — 為候選的學位/研究提案主題提供三關式（開放性？貢獻度？可行性？）的 go/no-go 決策檔案。產出 `.gaps.yml` 以便在階段 3a 交接給 `research-design-helper`。*(階段 2)*
- [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md) — 透過 Socratic dialog 引導完成 RQ → 機制 → 可識別性 → 驗證 → 風險評估。讀取 `.gaps.yml` 以預填第 1 和 5 部分；階段 4 的 [cookbook](docs/example-design-to-build.md) 會重用其產出的 `design_brief.md`。*(階段 3a, 4)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) — 產生 `.research/` manifests，讓未來的 AI sessions 省去重新掃描的步驟。*(階段 3b, 5, 8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) — 從那些 manifests 快速生成專案導覽備忘錄。*(階段 3b, 5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) — 根據任務性質在 Claude / Codex / Gemini 之間進行 character-driven routing。*(跨領域)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) — 產生 `.paper/claims.yml` + `.paper/figures.yml` (包含狀態列舉、anti-leakage 規則、檔案哨兵)。*(階段 7)*
- [`paper-summarize`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-summarize/SKILL.md) — 在 `research-hub auto` 執行後，將每篇論文的重點發現 / 方法 / 關聯性，同時填入 Obsidian 和 Zotero 的子筆記中。*(階段 1)*

</details>

<details>
<summary><b>獨立 repos (4 個 plugins)</b> — 每個 plugin 需單獨安裝</summary>

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md) — 稿件修訂、claim-evidence 審核 (與 `.paper/claims.yml` schema 對應)、禁用詞/語氣潤飾、期刊格式、審稿人回覆。*(階段 7, 8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md) — 完整的 Zotero CRUD、批次處理 metadata、文獻庫維護。*(階段 1, 2, 7)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md) — 從 Claude → Codex CLI 的交接，處理程式碼密集 / 機械性工作。*(跨領域, 也用於階段 4, 6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md) — 從 Claude → Gemini CLI 的交接，處理長文脈、多語言或中日韓語工作。*(跨領域, 也用於階段 6, 7)*

</details>

### 時間 + 成本預期

根據 session 中實際使用的粗略估計 — 請根據您的輸入大小進行調整：

| 任務 | 一般所需時間 | 對話輪次 | 備註 |
|---|---|---|---|
| 比較 5 篇論文 (`literature-triage-matrix`) | 1–3 分鐘 | 1–2 | 與論文數量成正比；20 篇約 5 分鐘 |
| 3 關卡 gap 決策 (`gap-to-topic`) | 5–15 分鐘 | 3–6 | 取決於候選主題數量及文獻回溯深度 |
| 審核一段文字的禁用詞 (`academic-writing-skills`) | <1 分鐘 | 1 | 與稿件總長度無關 |
| 回覆審稿人意見 (6 則) (`academic-writing-skills`) | 3–8 分鐘 | 3–5 | 取決於意見深度及所需修改幅度 |
| 審核 800 條的 Zotero 文獻庫 (`zotero-library-curator`) | 2–4 分鐘 | 1 | 唯讀；標籤多樣性比文獻庫大小影響更大 |
| 為每個叢集摘要 5 篇論文 (`paper-summarize`) | 4–10 分鐘 | 1 | 每篇論文一次 LLM call；失敗時會針對單篇論文進行回滾 |

這些是 **維護者觀察到的範圍**，並非基準測試數據。您的 LLM 供應商、網路、文獻庫狀態以及 prompt 的寫法都會影響實際時間。

### ⚠ 在進行任何 CRUD 操作前，請備份 Zotero

`zotero-library-curator` 是唯讀的 — 它只會產出預覽報告。
`zotero-skills` *可以* 寫入（合併重複項、刪除項目、重組收藏）。**在讓任何 AI 修改您的文獻庫之前，務必先匯出 Zotero 備份**：Zotero → File → "Export Library…" → Zotero RDF。這些 skills 不會自動為您執行此操作。

---

## 5. 查看每個 skill 的產出 (See what each skill produces)

每個發布的 skill 在 [`docs/examples.md`](docs/examples.md) 中至少有一個實作範例檔案：

- 文獻回顧的交付成果 (階段 1–2)
- 包含三關卡決策的主題檔案 (階段 2)
- 追溯至主題檔案來源的設計簡報 (階段 3a)
- 帶有 `provenance.from_gap` 的專案 manifest (階段 3b)
- **階段 4 cookbook** — 兩種路徑 (Claude-direct 用於 ≤4 個檔案；`codex-delegate` 用於 ≥5 個檔案的骨架)
- 帶有 `status: gap` 模式 + 圖表哨兵的 Paper-memory `claims.yml` + `figures.yml` (階段 7)
- 完整的文獻回顧 pipeline 輸出 (所有部分組合而成)

您可以根據上述階段選擇，或從頭到尾閱讀 [`docs/examples.md`](docs/examples.md)。

---

## 6. 相容性 (Compatibility)

這 15 個 SKILL.md 檔案均遵循 [agentskills.io](https://agentskills.io) 開放規格 — 約 35 個 agent runtime 都使用相同的格式。

| 項目 | 狀態 |
|---|---|
| 15 個 SKILL.md 通過最低規格要求 (`name` + `description`, ≤500 行) | ✅ 15/15 spec-verified |
| 在 agentskills.io hosts 之間可零編輯移植 | ✅ 11/14 |
| 需要進行外觀性 `<skill-root>` 路徑編輯 (已完成) | 3/14 |
| 在 NousResearch/hermes-agent 0.13.0 上通過端到端安裝驗證 | ✅ `literature-triage-matrix` — 安全掃描 SAFE, 註冊為 `enabled` |
| 在 Hermes 上進行推論循環 | ⚠ 未測試 (受身份驗證限制；超出範圍) |
| 其他 34 個 agentskills.io hosts | 未個別測試 |

`n/14` 的可移植性數據反映了 2026-05-10 的審核結果，當時 catalog 只有 14 個 skills；`gap-to-topic`（於 2026-05-21 新增，成為第 15 個）尚未進行可移植性審核。

校準審核 + 實驗記錄：
[`.research/hermes-compatibility-audit.md`](.research/hermes-compatibility-audit.md)。

若要在 Codex CLI / Gemini CLI / Cursor / Windsurf 或任何通用 API 客戶端上載入 SKILL.md，請參閱
[docs/install.md → 在 Claude Code 之外使用這些 skills](docs/install.md#using-these-skills-outside-claude-code)。

---

## 7. 限制 (Limitations)

- 由一位研究生研究員組裝和測試；未經大規模語料庫驗證。
- 領域偏向水資源和代理人基模擬；未在社會科學、機器學習或臨床寫作領域進行驗證。
- 在真實世界輸入下的行為正確性是原始碼 repo 的責任，而非本 catalog 的責任。
- 上游 URL 的存活狀態未經機器檢查；在 PR 時手動驗證。
- CI 不斷言 `claude plugin install` 的往返過程；marketplace registry 經過結構性檢查，但實際的安裝 + 觸發路徑由維護者在版本發布之間進行驗證（關於涵蓋範圍的詳細資訊，請參見 [docs/verification.md](docs/verification.md)）。
- `zotero-skills` 同時由兩個 plugins 提供（`research-workspace` 嵌入了一個較舊的版本，同時還有一個獨立的、標準的 `zotero-skills` plugin）。直接以名稱調用 `Skill(skill="zotero-skills")` 會靜默解析到 `research-workspace` 中嵌入的副本。要使用標準的獨立版本，需使用 plugin 限定的形式 `Skill(skill="zotero-skills:zotero-skills")`。重現步驟和延後修復的說明請見 [docs/verification.md §2026-05-20](docs/verification.md#2026-05-20--phase-53b-end-to-end-verification)。

完整的設計合約 — 包括哪些是機器檢查的，哪些不是 — 請參閱 [docs/design-philosophy.md](docs/design-philosophy.md)。

---

## 授權 (License)

MIT. 每個 skill 都在其標準 repo 中維護 — 本 catalog 是一個索引，而非 monorepo。歡迎透過 issue 或 PR 進行貢獻。
新 skill 的提案 → 若與工作流程整合，請至 `research-hub`；若為深度、單一目的的 CRUD，請建立獨立 repo。
