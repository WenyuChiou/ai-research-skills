# 安裝指引

這個 repo 是個 catalog，skill 本身在各自的 canonical repo。
英文版：[install.md](install.md)。

前置條件：[Claude Code](https://claude.ai/code)（或 Codex CLI /
Cursor / Gemini CLI）。所有 catalog 收錄的 skill 都在 AI 對話內啟動。

> **第一次來？** Claude Code / Python / Zotero 都還沒 work 的話，
> 先看 [**setup-guide.zh-TW.md**](setup-guide.zh-TW.md) —— 從 runtime
> 到 plugin 到 Zotero local API 整個 end-to-end 帶你跑，每步有驗證
> 指令。這頁假設你 prereq 都 work，專注在「哪個 plugin 對應哪個 workflow」。

完整 skill 列表跟連結：[skill-directory.zh-TW.md](skill-directory.zh-TW.md)。

## 路徑 A — Claude Code marketplace（推薦）

主 README 跟 [README.zh-TW.md](../README.zh-TW.md) 已經把 5 個 plugin 的
marketplace 安裝路徑講完了。最短的是:

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
bash scripts/install-all.sh        # 或 pwsh scripts/install-all.ps1
```

裝好之後 5 個 plugin 全部到位、總共 14 個 skill。Step 5(research-hub
CLI)跟 step 3-4(Zotero / Codex / Gemini 外部 binary)的前置設定看
README。

## 路徑 B — research-hub Python CLI（要 literature pipeline 自動化時加）

使用 Zotero、Obsidian、NotebookLM 或這 3 個任一兩個的組合時用：

```bash
pip install research-hub-pipeline
research-hub setup
```

`setup` 是一個互動式指令，會問你要連哪些 service（Zotero default
collection、NotebookLM login 等），順便裝範例資料。是
**idempotent** ——隨時重跑，更新 skill 或換 persona。

Persona 速查表（互動式 setup 會問你；要事先指定也可以
`--persona <X>`）：

| Persona | Stack | 適用情況 |
|---|---|---|
| `researcher` | Zotero + Obsidian + NotebookLM | 想要全套 workflow |
| `analyst` | Obsidian + NotebookLM only（無 Zotero）| 不用 Zotero |
| `humanities` | Zotero + 質性預設 | 做 interpretive / archival 研究、不寫 code repo |
| `internal` | 純 catalog 閱讀、不裝 | 推薦給別人用、自己不安裝 |

**其他 AI host：** `setup` 會自動偵測 Claude Code；用 Cursor / Codex
/ Gemini 的話，安裝完之後再指定平台：

```bash
research-hub install --platform cursor
research-hub install --platform codex
research-hub install --platform gemini
```

裝完之後 10 個 skill 出現在 `~/.claude/skills/` 底下：`research-hub`、
`research-design-helper`、`research-context-compressor`、
`research-project-orienter`、`research-hub-multi-ai`、
`literature-triage-matrix`、`paper-memory-builder`、`paper-summarize`、
`notebooklm-brief-verifier`、`zotero-library-curator`。

*註*: 這條 Python-CLI 路徑(`research-hub setup`)**會**把 skill 展到
`~/.claude/skills/` 底下。Claude Code marketplace 路徑(`claude plugin
install …@ai-research-skills`)**不會** —— 那些 skill 住在
`~/.claude/plugins/cache/…` 底下。兩條路徑都能用,只是 SKILL.md 落點不同。
端到端紀錄看 [verification.md](verification.md) §2026-05-20。

NotebookLM 的瀏覽器自動化（如果 setup 時答 yes 就會幫你裝；跳過的話
個別在這裡裝）：

```bash
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

不靠 NotebookLM 先做煙霧測試：

```bash
research-hub auto "agent-based modeling" --no-nlm
```

### 之前只跑了 `install` 沒跑 `setup`？

```bash
# 舊指令：research-hub install --platform claude-code
# 還能跑，但只寫 SKILL.md 檔案（不會做 persona、Zotero default、
# NotebookLM login）。任何時間重跑 setup 補完整 onboarding：
research-hub setup
```

### 從 research-hub-pipeline ≤ 0.45 升級

舊版本會裝一個叫 `knowledge-base/` 的 skill。canonical 名字從 v0.46
開始就是 `research-hub/`(同樣的 workflow)。新裝不會再寫
`knowledge-base/`,但之前裝的可能還留著舊目錄。

如果 `~/.claude/skills/knowledge-base/` 跟 `~/.claude/skills/research-hub/`
同時存在,舊 alias 可能讓 skill router 重複觸發。
`get_bundled_skill_path("knowledge-base")` 這個 alias 在 `v0.45–0.69`
會印 `DeprecationWarning`、`v0.70+` 已經拿掉 alias。安全移除舊目錄:

```bash
rm -rf ~/.claude/skills/knowledge-base
```

## 各 plugin 直接安裝指令（不想跑 helper script 的話）

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills        # 10 skills
claude plugin install academic-writing-skills@ai-research-skills   # +1
claude plugin install zotero-skills@ai-research-skills             # +1
claude plugin install codex-delegate@ai-research-skills            # +1
claude plugin install gemini-delegate@ai-research-skills           # +1
```

## 建議最小組合

大部分研究者：

```text
research-workspace
academic-writing-skills
```

如果有大量 Zotero library 要管，再加 `zotero-skills`。如果跟 Codex
或 Gemini 配合用，再加 delegation skill。

---

## 在 Claude Code 之外用這些 skills

`claude plugin install` 那條路徑只有 Claude Code 認得。SKILL.md 本身
就是 Markdown，可以給 Codex CLI、Gemini CLI、Cursor、Windsurf、Hermes
或任何吃 context file 的 AI assistant 用。代價是失去 Claude Code 的
auto-trigger（你描述需求它會自己挑對的 skill）——在其他 host 上你要
明確指出要用哪個 SKILL.md。

### 1. 拿原始檔

```bash
git clone https://github.com/WenyuChiou/research-hub
git clone https://github.com/WenyuChiou/academic-writing-skills
git clone https://github.com/WenyuChiou/zotero-skills
git clone https://github.com/WenyuChiou/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill
```

每個 repo 的 SKILL.md（連同 `references/`）都在
`skills/<plugin-name>/` 底下。research-hub 有 10 份；其他 4 個各 1 份。

### 2. 各 host 載入方式

| Host | 怎麼載入 SKILL.md |
|---|---|
| **Codex CLI** | `codex exec --full-auto -C /repo "$(cat path/to/SKILL.md)\n\n現在做 X..."`，或寫一份 `.ai/codex_task.md` 開頭塞 SKILL.md 內容 |
| **Gemini CLI** | `--system-prompt-file path/to/SKILL.md`，或放進 project context |
| **Cursor / Windsurf** | 把 SKILL.md（或內容）丟到 `.cursor/rules/` 或對應 rules 目錄 |
| **Hermes Agent** | `hermes skills install <github-raw-url-to-SKILL.md>`——`literature-triage-matrix` 已在 Hermes 0.13.0 端對端驗證過；見 [`.research/hermes-compatibility-audit.md`](../.research/hermes-compatibility-audit.md) |
| **通用 API** | 把 SKILL.md 當 system prompt 用 |
| **其他 AI** | 把 SKILL.md 相關段落貼進你的 prompt |

### 3. 哪些 skill 在 Claude Code 之外比較合理

- 5 個純推理 skill（`literature-triage-matrix`、
  `research-design-helper`、`research-context-compressor`、
  `research-project-orienter`、`paper-memory-builder`）任何 AI 都能
  跑——它們講的是 workflow + 輸出格式，不依賴 Claude 特定機制。
- `academic-writing-skills` 任何 AI 能讀檔（`.paper/`、`journal_format.md`）就行。
- `notebooklm-brief-verifier` 的 Manual fallback 模式哪都能跑。
- `zotero-skills` 任何 AI 能呼叫 Zotero local / Web API 就能用——它
  主要是 API routing reference，不是 Claude 特性。
- `codex-delegate` / `gemini-delegate` 是 **Claude 對外 delegate**
  時用的；如果你直接用 Codex 或 Gemini，這兩個幫助比較小。
- `research-hub` 跟 `research-hub-multi-ai` 不論用哪個 AI 都要先
  `pip install research-hub-pipeline`。
