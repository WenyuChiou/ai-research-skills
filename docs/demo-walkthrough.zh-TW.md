# Demo Walkthrough — 5 個 skill 在真實小型 corpus 上協同運作

這份 walkthrough 示範實際把 catalog 裡的 skill 用在一個真實研究任務時會發生什麼事。下面提到的每個產出都已存在本 repo 的 [`test-corpus/ai-agents-social-interaction/`](../test-corpus/ai-agents-social-interaction/) — 沒有任何假設、沒有任何為了文件重跑的東西。

Corpus：5 篇 AI agents + 社會互動主題的真實論文，於 2026-04-25 由 `research-hub search` 抓取。主題涵蓋 VR-embodied agents、LLM 在 poker 中的 theory-of-mind、多 agent 學習、多 agent 實驗工具、直播對齊。

英文 README：[../README.md](../README.md)。本 zh-TW walkthrough 與英文版段落同步；artifact 檔案本身仍多為英文。

## 安裝（一次性）

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
bash scripts/install-all.sh        # 或 pwsh scripts/install-all.ps1
```

裝完之後 6 個 plugin 都會載入(14 個核心 skill + audit-first-skills 的 5 個 skill)。本 walkthrough 用到其中三個會需要額外設定:

- `research-hub`（論文搜尋）需要 `pip install research-hub-pipeline` + `research-hub setup`。詳見 [install.md](install.md)。
- `notebooklm-brief-verifier` 的手動模式不需設定；Managed 模式需要 research-hub CLI。
- 本 walkthrough 用到的另外 2 個（`literature-triage-matrix`、`paper-memory-builder`）是純推理 skill — 安裝完就能用。

## Step 1 — 發現論文（`research-hub`）

```text
使用者: 找 AI agents 與社會互動相關的論文，方法與領域要散開、約 5 篇。
```

Claude 觸發 `research-hub` skill，它會呼叫 `research-hub search "AI agents social interaction" --limit 8 --rank-by smart`。選出的 5 篇論文與完整搜尋 JSON 在：

- **[`test-corpus/.../search-results.json`](../test-corpus/ai-agents-social-interaction/search-results.json)** — Semantic Scholar / arXiv / OpenAlex 的原始搜尋回應。
- **[`test-corpus/.../papers/`](../test-corpus/ai-agents-social-interaction/papers/)** — 一篇論文一個 Markdown note，含 metadata + abstract。

這一步示範什麼：skill 選出 5 篇橫跨 3 種方法（實證實驗、框架、概念）與 5 個領域（VR / 健康、poker / ToM、教育、HCI 基礎建設、直播對齊）的論文 — 這個 spread 就是 test corpus README 自己宣告的可證偽主張。

## Step 2 — Triage 與比較（`literature-triage-matrix`）

```text
使用者: 比較這 5 篇論文的方法、資料、主張、限制。
```

Claude 觸發 `literature-triage-matrix` 並讀取 5 篇論文 note。產出：

- **[`test-corpus/.../.research/literature_matrix.md`](../test-corpus/ai-agents-social-interaction/.research/literature_matrix.md)** — 跨 `Method`、`Data`、`Central claim`、`Limitation`、`Relevance to RQ` 的比較表。

這一步示範什麼：你拿到的不是 5 個一篇一個的通用摘要，而是一張能凸顯 gap 的表（例如「5 篇都研究 agent，只有 #4 instrument 多 agent 實驗；#5 是框架沒有實證」）。這張矩陣就是下一步的輸入。

## Step 3 — 驗證 NotebookLM brief（`notebooklm-brief-verifier`）

```text
使用者: 我把這 5 篇上傳到 NotebookLM 拿到一份 brief，幫我對照原始 source bundle 驗證。
```

這個 skill 有兩種模式：
- **Managed**：`research-hub` 已上傳 bundle 並有追蹤。
- **Manual fallback**：你把下載的 brief + 一份 plain source list 貼進來。給只裝 marketplace plugin（沒有 `research-hub` CLI）的使用者用。

Manual fallback 的產物在另一份平行 test corpus：

- **[`test-corpus/manual-fallback-fresh-user/`](../test-corpus/manual-fallback-fresh-user/)** — `brief.txt`（NotebookLM 原始輸出）、`sources.md`（source list）、`brief-verify-manual-fallback.md`（驗證輸出：漏掉的 source、未支撐的主張、矛盾、建議的 follow-up prompt）。

這一步示範什麼：典型的 NotebookLM brief 會悄悄漏掉 1–2 個 source、含 1–3 個未支撐的主張。Verifier 會明確標出來。同一個 skill、兩種輸入模式、一致的輸出結構。

## Step 4 — 銳化研究問題（`research-design-helper`）

```text
使用者: 帶我走過研究設計。RQ：LLM agent 的 theory-of-mind 行為會隨社會 context 改變嗎？
```

Claude 觸發 `research-design-helper`，這是一個 5 段式 Socratic 對話（RQ → 預期機制 → 可識別性檢查 → 驗證計畫 → 風險清單）。產出：

- **[`test-corpus/.../.research/design_brief.md`](../test-corpus/ai-agents-social-interaction/.research/design_brief.md)** — 一份 Markdown 檔案，5 段針對這個 RQ 都填好。

這一步示範什麼：在寫 code 之前先得到一個可證偽的設計。這份 brief 接著會變成 project-context-compressor（下一步）與 model-design 步驟的輸入。

## Step 5 — 壓縮專案 context（`research-context-compressor`）

```text
使用者: 把這個專案的 context 壓縮起來，讓未來的 AI session 不必再重讀所有東西。
```

Claude 觸發 `research-context-compressor` 並寫出：

- **[`test-corpus/.../.research/project_manifest.yml`](../test-corpus/ai-agents-social-interaction/.research/project_manifest.yml)** — 研究問題、資料集、目前階段、關鍵入口點。
- （視情況也會寫 `.research/experiment_matrix.yml` 與 `.research/data_dictionary.yml`，給已開跑實驗的專案。）

這一步示範什麼：未來的 Claude session 幾秒就把 manifest 載入，不必爬 20 多個檔案。對接手專案的人類協作者也是同樣效果。

## Step 6 — 建構 paper 記憶（`paper-memory-builder`）

```text
使用者: 我有一份稿件草稿。改稿前先建好 paper memory。
```

Claude 對稿件檔案觸發 `paper-memory-builder`。產出：

- **[`test-corpus/.../.paper/lim-2025/claims.yml`](../test-corpus/ai-agents-social-interaction/.paper/lim-2025/claims.yml)** — 每一個 paper-level claim，含證據指針與狀態。
- **[`test-corpus/.../.paper/lim-2025/figures.yml`](../test-corpus/ai-agents-social-interaction/.paper/lim-2025/figures.yml)** — 每張圖的關鍵數字以及它支撐哪個 claim。
- （實際走過 revision 之後還會有 `revision_history.yml` — append-only 的稽核軌跡。詳見 [revision_history schema 參考](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/references/revision_history_schema.md)。）

這一步示範什麼：寫作 skill 不再每次稽核都重讀稿件。`claims.yml` 是共用的記憶層。

## Step 7 — 稿件稽核 + 修訂（`academic-writing-skills`）

```text
使用者: 幫這段做 banned words、主張-證據支撐、圖文一致性的稽核。
```

Claude 把段落 + Step 6 產出的 `.paper/claims.yml` 與 `.paper/figures.yml` 一起餵給 `academic-writing-skills`。這個 skill 會：

1. 載入 `references/banned_words.md`（禁用的 GPT 式 / 過度宣稱片語）。
2. 載入 `references/claim_evidence_audit.md`。
3. 把每一個數字主張對 `claims.yml` 與 `figures.yml` 交叉檢查。
4. 回報：含禁用詞的行、沒有證據的 claim、與 `figures.yml` 不符的圖示參照。

這個 skill 的 reference 檔案（實際的稽核邏輯）住在 [`academic-writing-skills/skills/academic-writing-skills/references/`](https://github.com/WenyuChiou/academic-writing-skills/tree/main/skills/academic-writing-skills/references)。對真實稿件工作的驗證在 [verification.md](verification.md)（中文版：[verification.zh-TW.md](verification.zh-TW.md)）。

這一步示範什麼：`paper-memory-builder → academic-writing-skills` 這條鏈讓稽核變成增量式。每次重大改稿跑一次 paper-memory-builder；稽核則是 per-paragraph 或 per-session。

## 整體要傳達什麼

- **每個 skill 的輸出都是下一個 skill 的輸入。** 這條鏈是真的（這就是同一份 `.paper/claims.yml` 同時出現在 paper-memory-builder 的輸出規格與 academic-writing-skills 的輸入規格的原因）。
- **Skill 不必由使用者自己接線。** Claude Code 的 auto-trigger 從你的措辭挑出對的 skill，你不必手動選。
- **Artifact 跨 session 持續存在。** `.research/` 與 `.paper/` 目錄是耐久的記憶層。新的 Claude session 讀 `project_manifest.yml` + `claims.yml` 後幾秒鐘就上手。

## 這份 walkthrough 沒有涵蓋的

- `zotero-skills` / `zotero-library-curator` — 需要真實 Zotero 庫；test corpus 上沒有。
- `research-hub-multi-ai` — 是把任務在 Claude / Codex / Gemini 之間 routing 的 router skill；不會在 corpus 裡產生單一 artifact。
- `codex-delegate` / `gemini-delegate` — 用於下游 coding 或長 context 寫作，不在文獻 triage 路徑上。
- 真實 reviewer-response 迴圈搭配 `revision_history.yml` — schema 定義在 research-hub 的 `paper-memory-builder/references/revision_history_schema.md`；端到端真實改稿迴圈會放在後續的 walkthrough。
