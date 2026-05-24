# Runtime Contract

這個 catalog 是 skill layer。真正可執行的研究流程在各 source repo，
尤其是 `research-hub`。

## 每一層負責什麼

| 層級 | 提供 | 不提供 |
|---|---|---|
| `ai-research-skills` catalog | Marketplace registry、安裝文件、canonical `SKILL.md` 連結 | Python CLI、Zotero API access、NotebookLM browser session、MCP server |
| `SKILL.md` 檔案 | 給 AI host 的可攜工作流程指令與輸出 contract | 保證 host 會自動觸發，或保證能存取外部工具 |
| `research-hub-pipeline` | `research-hub` CLI、MCP/REST server、Zotero/Obsidian/NotebookLM 自動化、dashboard | 整個 catalog 的 Claude Code marketplace 安裝 |

安裝這個 catalog 或複製 `SKILL.md`，不代表 Python runtime 已安裝。
`claude plugin list` 只驗證 Claude Code marketplace 狀態。

## Skill 類型

| 類型 | 範例 | Runtime 需求 |
|---|---|---|
| Prompt-only workflow skills | `gap-to-topic`、`research-design-helper`、`literature-triage-matrix`、`academic-writing-skills` | 任何能讀必要檔案並遵守輸出 contract 的 host |
| Workspace-file skills | `research-context-compressor`、`research-project-orienter`、`paper-memory-builder` | 能讀寫專案檔案，或由使用者手動提供 context |
| Runtime-backed research automation | `research-hub`、`paper-summarize`、部分 `notebooklm-brief-verifier`、Zotero-backed curation flows | `pip install research-hub-pipeline`，再加上需要的 Zotero、Obsidian、NotebookLM、LLM CLI、MCP 或 REST 設定 |
| Deep Zotero CRUD | `zotero-skills` | Zotero local/Web API credentials，且 host 能呼叫 API |
| Delegation skills | `codex-delegate`、`gemini-delegate`、`research-hub-multi-ai` | 目標 CLI 已安裝且在 `PATH`，或改用手動 handoff prompt |

## 文獻搜尋前的 Agent Preflight

Claude Code、Codex、Gemini CLI、Cursor、OpenClaw、Hermes 或 generic API
client 要跑文獻流程前，先確認 executable layer：

```bash
research-hub describe --json
research-hub doctor
research-hub auto "agent-based modeling" --max-papers 3 --no-nlm
```

如果找不到 `research-hub`：

```bash
pip install research-hub-pipeline
research-hub setup --persona researcher   # or: analyst | humanities | internal
```

如果 smoke test 因為沒有 relevance judge 而停下，請安裝/設定支援的
LLM CLI（`claude`、`codex`、`gemini`、`opencode`、`aichat`、`cursor`
或 custom adapter），或用 `--no-fit-check` 跑 smoke test，並明確記錄
這次略過了關聯性過濾。

Zotero/Obsidian 匯入流程確認能跑後，再加入 NotebookLM：

```bash
research-hub notebooklm login --auto-detect
research-hub notebooklm bundle --cluster <slug>
research-hub notebooklm upload --cluster <slug>
research-hub notebooklm generate --cluster <slug> --type brief
research-hub notebooklm download --cluster <slug>
```

## Host 相容性

- Claude Code 有 packaged marketplace 路徑與 `claude plugin list`。
- Codex、Cursor、Gemini、Windsurf、Hermes、OpenClaw 與 generic API
  clients 可以使用同一份 `SKILL.md` 指令，但每個 host 都要用自己的
  discovery 或 prompt smoke test 驗證。
- 需要真正工具執行時，MCP/REST-capable hosts 應優先使用
  `research-hub serve`，而不是只靠 prompt-only workflow。
- OpenClaw 透過 MCP / 手動 `SKILL.md` 載入在結構上相容，但本 catalog
  尚未宣稱 release-grade OpenClaw verification。
