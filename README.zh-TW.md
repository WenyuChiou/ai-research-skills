# AI Research Skills

> 14 個 Claude Code skills、覆蓋常見研究任務——文獻整理、研究 design、
> 專案 context、論文撰寫、多 AI delegation。

語言：[English](README.md) | [繁中](README.zh-TW.md) ·
[看每個 skill 實際產出什麼 →](docs/examples.zh-TW.md) ·
[詞彙表](docs/glossary.zh-TW.md)

<sub>
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![agentskills.io spec](https://img.shields.io/badge/agentskills.io-spec_compliant-2DA89C)](.research/hermes-compatibility-audit.md)
[![Hermes verified](https://img.shields.io/badge/Hermes_0.13.0-skill--load_verified-2DA89C)](.research/hermes-compatibility-audit.md)
</sub>

![14 個 AI skills 對應研究 workflow 階段，附 cross-cutting tools（codex-delegate、gemini-delegate、research-hub-multi-ai）每階段都可用](docs/img/pipeline-overview.zh-TW.png)

---

## 這是什麼

1 個 Claude Code marketplace、5 個 plugin、共 14 個 skill。
給研究生、博士生、博士後、研究人員、研究工程師、研究支援人員用——
真實研究流程裡把 AI 拉進來、不是 demo。

Skills 是 [agentskills.io](https://agentskills.io) 規格的 Markdown 檔——
在 Claude Code 內依你的描述自動觸發，也能載入 Codex CLI / Gemini CLI /
Cursor / Windsurf / Hermes（見 [Compatibility](#compatibility)）。

> 📚 [agentic AI 學習地圖](https://github.com/WenyuChiou/awesome-agentic-ai-zh) 的一部分
> ——在 §13-14（研究 workflow）介紹這個 marketplace。

---

## 安裝

前置：[Claude Code](https://claude.ai/code)。
Python / Zotero / Git 還沒裝起來的話，從
[**docs/setup-guide.zh-TW.md**](docs/setup-guide.zh-TW.md) 開始。

每一步**累加**——做到哪裡停都可以、已裝的就能用。

```bash
# 1. Marketplace + 10 支 research-hub skills（其中 6 支不用外部設定立刻能用）
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills

# 2. 論文撰寫
claude plugin install academic-writing-skills@ai-research-skills

# 3. Zotero（先在 Zotero desktop 開 local API——見 docs/setup-guide.zh-TW.md §C）
claude plugin install zotero-skills@ai-research-skills

# 4. 多 CLI delegation（先裝 codex / gemini CLI binary）
claude plugin install codex-delegate@ai-research-skills
claude plugin install gemini-delegate@ai-research-skills

# 5. 文獻 pipeline 自動化（research-hub skill 背後的 Python CLI）
pip install research-hub-pipeline
research-hub setup
```

一次裝 5 個 plugin:

```bash
bash scripts/install-all.sh        # macOS / Linux / git-bash
pwsh scripts/install-all.ps1       # Windows PowerShell
```

外部前置（Zotero local API、Codex / Gemini CLI binary）還是要照各步驟
手動處理。Per-plugin 完整說明：
[docs/install.zh-TW.md](docs/install.zh-TW.md)。

**驗證**：

```bash
claude plugin list
# 預期:5 個 plugin、每個以 @ai-research-skills 結尾、每個都標 ✔ enabled。
```

Marketplace 裝的 plugin **不會**展開到 `~/.claude/skills/` —— 它們住在
`~/.claude/plugins/cache/ai-research-skills/<plugin>/<version>/skills/<name>/`,
由 Claude Code 透過每個 plugin 的 `.claude-plugin/plugin.json` 發現。
直接 `ls ~/.claude/skills/` **不能**確認 marketplace 安裝成功;用
`claude plugin list` 才對。(端到端的安裝 + skill 觸發驗證紀錄看
[docs/verification.md](docs/verification.md) §2026-05-20。)

---

## 怎麼用

用自然語言講你要做什麼——Claude Code 會自動 match 到對的 skill。
你**不用記 skill 名字**。

| 你說... | 啟動的 skill |
|---|---|
| 「比較這 5 篇論文的 method、data、limitations」 | `literature-triage-matrix` |
| 「audit 我 Zotero library 找重複跟 orphan tags」 | `zotero-library-curator` |
| 「在我開始 coding 之前先帶我走過研究 design」 | `research-design-helper` |
| 「驗證這份 NotebookLM brief 對應 source bundle」 | `notebooklm-brief-verifier` |
| 「audit 我這段文字有沒有 banned words 跟 overclaim」 | `academic-writing-skills` |
| 「依照這些 reviewer 意見產出 point-by-point 回覆」 | `academic-writing-skills` |
| 「壓縮這個 project context 給未來 AI session 用」 | `research-context-compressor` |
| 「這個 task 是 code-heavy——交給 Codex」 | `codex-delegate` |
| 「把這份 brief 翻成繁中、需要長 context」 | `gemini-delegate` |

Auto-trigger 沒挑到對的 skill 時、明說 skill 名字：
*「用 `literature-triage-matrix` 比較這 5 篇論文。」*

### 找到你的起點

| 你眼前的目標 | 你會用到的 skills |
|---|---|
| **找文獻、比較文獻** | `research-hub` + `literature-triage-matrix` |
| **寫論文 / 改稿** | `paper-memory-builder` + `academic-writing-skills` |
| **管理研究專案 / Zotero library** | `research-design-helper` + `research-context-compressor` + `zotero-library-curator` |

> **協助別人用 AI 做研究**（圖書館員 / RA / 指導者）？不用裝——
> 把這份 README 跟 [docs/install.zh-TW.md](docs/install.zh-TW.md) 轉給對方就好。

完整對應表：[docs/skill-directory.zh-TW.md](docs/skill-directory.zh-TW.md) ·
按研究 pipeline 階段看：[docs/pipeline.zh-TW.md](docs/pipeline.zh-TW.md) ·
Skill 產出範例：[docs/examples.zh-TW.md](docs/examples.zh-TW.md)。

### 時間與成本預估

Maintainer 在 session 裡實際觀察到的範圍 —— 視你的 input 大小調整:

| Task | 典型時間 | 對話輪數 | 註記 |
|---|---|---|---|
| 比較 5 篇 paper(`literature-triage-matrix`)| 1–3 分鐘 | 1–2 | 對 paper 數線性;20 篇 ≈ 5 分鐘 |
| 1 段文字 banned-word audit(`academic-writing-skills`)| <1 分鐘 | 1 | 跟 manuscript 整體大小無關 |
| Reviewer response 6 條意見(`academic-writing-skills`)| 3–8 分鐘 | 3–5 | 隨意見深度跟需要改稿幅度增加 |
| Audit 800 條 Zotero library(`zotero-library-curator`)| 2–4 分鐘 | 1 | Read-only;tag diversity 影響大過 library size |
| 5 篇 paper summarize(`paper-summarize`)| 4–10 分鐘 | 1 | 每篇 paper 一次 LLM call;失敗會 per-paper rollback |

這些是 **maintainer 觀察範圍**、不是 benchmark。LLM provider、網路、
library 狀態、prompt 寫法都會影響實際時間。先泡杯咖啡。

### ⚠️ 動 Zotero CRUD 前先備份

`zotero-library-curator` 是 read-only —— 它只 emit preview 報告。
`zotero-skills` **會**寫(merge 重複、刪 item、改 collection 歸屬)。**讓
任何 AI 動你 library 之前一定先 export 備份**:Zotero → File →
「Export Library…」→ Zotero RDF。Skill 不會自動幫你做這件事。

---

## Compatibility

這 14 支 SKILL.md 符合 [agentskills.io](https://agentskills.io) open
spec——~35 個採用該規格的 agent runtime 用的同一套格式。

| 項目 | 狀態 |
|---|---|
| 14 支 SKILL.md 通過 strict-minimum spec（`name` + `description`、≤500 行）| ✅ 14/14 驗證 |
| 跨 agentskills.io host 零修改可移植 | ✅ 11/14 |
| 需要 cosmetic `<skill-root>` example-path 修改（已 landed） | 3/14 |
| 在 NousResearch/hermes-agent 0.13.0 端對端安裝驗證 | ✅ `literature-triage-matrix` —— 安全掃描 SAFE、`enabled` 註冊 |
| Hermes 上跑 inference loop | ⚠ 未測（卡 auth gate、超出範圍）|
| 其他 34 個 agentskills.io host | 未個別測試 |

Calibrated 審計 + 實驗 transcript：
[`.research/hermes-compatibility-audit.md`](.research/hermes-compatibility-audit.md)。

要在 Codex CLI / Gemini CLI / Cursor / Windsurf 或通用 API client 載入
SKILL.md，看
[docs/install.zh-TW.md → 在 Claude Code 之外用這些 skills](docs/install.zh-TW.md#在-claude-code-之外用這些-skills)。

---

## 全部 14 個 Skills

> 下方 `*(階段 X、Y)*` 對應研究 workflow 1-8 階段 ——
> 圖跟階段對應看 [`docs/pipeline.zh-TW.md`](docs/pipeline.zh-TW.md)
> 跟 [`docs/glossary.zh-TW.md`](docs/glossary.zh-TW.md) § Phase 數字。

<details>
<summary><b>來自 <code>research-hub</code>（10 個）</b>——一次安裝全部到位</summary>

- [`research-hub`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md)：Zotero / Obsidian / NotebookLM 之間搜尋、匯入、整理論文。*(階段 1、2)*
- [`literature-triage-matrix`](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)：依 method、data、claim、limitation 做比較表。*(階段 2)*
- [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md)：NotebookLM brief 對回 source bundle 做驗證。*(階段 2)*
- [`zotero-library-curator`](https://github.com/WenyuChiou/research-hub/blob/master/skills/zotero-library-curator/SKILL.md)：audit Zotero library，提整理計畫（preview only、沒有 `zotero-skills`）。*(階段 2)*
- [`research-design-helper`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md)：Socratic 對話走過 RQ → mechanism → identifiability → validation → risk。*(階段 3a、4)*
- [`research-context-compressor`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md)：`.research/` manifest 讓未來 AI session 不必重新掃 repo。*(階段 3b、5、8)*
- [`research-project-orienter`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md)：讀那些 manifest、快速產生 orientation 摘要。*(階段 3b、5)*
- [`research-hub-multi-ai`](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)：按 task 性質做 Claude / Codex / Gemini routing。*(Cross-cutting)*
- [`paper-memory-builder`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md)：產出 `.paper/claims.yml` 與 `.paper/figures.yml` 給寫作流程用。*(階段 7)*
- [`paper-summarize`](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-summarize/SKILL.md)：`research-hub auto` 跑完後、把每篇論文 Key Findings / Methodology / Relevance 同時寫到 Obsidian 跟 Zotero child note。*(階段 2)*

</details>

<details>
<summary><b>獨立 repos（4 個）</b>——一個 plugin 一個 install</summary>

- [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md)：manuscript 修改、claim-evidence audit、banned-word / humanize、journal format、reviewer response。*(階段 7、8)*
- [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md)：完整 Zotero CRUD、batch metadata、library maintenance。*(階段 1、2、7)*
- [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md)：把程式重的工作從 Claude 交給 Codex CLI。*(Cross-cutting，也用於階段 6)*
- [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md)：把長 context、多語、CJK 工作從 Claude 交給 Gemini CLI。*(Cross-cutting，也用於階段 6、7)*

</details>

Per-skill testing 矩陣與可重現的 test-corpus 證據：
[docs/verification.zh-TW.md](docs/verification.zh-TW.md)（中文摘要）或
[docs/verification.md](docs/verification.md)（英文完整逐項）。

---

## 限制

- 由一位研究生組裝、測試;沒做過 corpus 規模驗證。
- 領域偏向水資源、agent-based modeling;社會科學、ML、臨床寫作未驗證。
- 真實世界輸入的行為正確性是 source repo 的責任,不是 catalog 的。
- 上游 URL 是否還活著沒有 CI 自動檢查;PR 時人工 review。
- CI 沒有 assert `claude plugin install` 整套 round-trip——marketplace
  registry 是結構性檢查,實際安裝跟觸發路徑由 maintainer 在 release
  之間人工驗證(看 [docs/verification.md](docs/verification.md)
  哪些有覆蓋、哪些沒有)。
- `zotero-skills` 同時被兩個 plugin 提供:`research-workspace` 裡
  夾帶了舊版本,另一個是 canonical 的 standalone `zotero-skills`
  plugin。直接呼叫 `Skill(skill="zotero-skills")`(bare name)會
  靜默 resolve 到 `research-workspace` 裡的舊副本。要打到 canonical
  standalone 必須用 plugin-qualified 形式
  `Skill(skill="zotero-skills:zotero-skills")`。重現步驟跟延後修
  紀錄在
  [docs/verification.md §2026-05-20](docs/verification.md#2026-05-20--phase-53b-end-to-end-verification)。

完整設計契約——包含哪些東西用機器檢查、哪些不檢查——在
[docs/design-philosophy.zh-TW.md](docs/design-philosophy.zh-TW.md)。

---

## 授權

MIT。每個 skill 由各自的 canonical repo 維護——這個 catalog 是索引、
不是 monorepo。歡迎 contribution——open issue 或 PR。新 skill 提案
請鎖定 `research-hub`（workflow 整合）或一個獨立 repo（單一目的、深度
CRUD）。
