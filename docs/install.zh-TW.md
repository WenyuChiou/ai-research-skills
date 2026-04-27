# 安裝指引

這個 repo 是個 catalog，skill 本身在各自的 canonical repo。
英文版：[install.md](install.md)。

前置條件：[Claude Code](https://claude.ai/code)（或 Codex CLI /
Cursor / Gemini CLI）。所有 catalog 收錄的 skill 都在 AI 對話內啟動。

完整 skill 列表跟連結：[skill-directory.zh-TW.md](skill-directory.zh-TW.md)。

## 路徑 A — Claude Code marketplace（推薦）

主 README 跟 [README.zh-TW.md](../README.zh-TW.md) 已經把 5 個 plugin 的
marketplace 安裝路徑講完了。最短的是：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
bash scripts/install-all.sh        # 或 pwsh scripts/install-all.ps1
```

裝好之後 5 個 plugin 共 13 個 skill 全部到位。Step 5（research-hub
CLI）跟 step 3-4（Zotero / Codex / Gemini 外部 binary）的前置設定看
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

裝完之後 9 個 skill 出現在 `~/.claude/skills/` 底下：`research-hub`、
`research-design-helper`、`research-context-compressor`、
`research-project-orienter`、`research-hub-multi-ai`、
`literature-triage-matrix`、`paper-memory-builder`、
`notebooklm-brief-verifier`、`zotero-library-curator`。

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

舊版本會裝一個叫 `knowledge-base/` 的 skill。現在的正式名稱是
`research-hub/`（同樣的 workflow）。新裝不會再寫 `knowledge-base/`，
但你之前裝的可能還留著舊目錄。

如果 `~/.claude/skills/knowledge-base/` 跟
`~/.claude/skills/research-hub/` 同時存在，舊 alias 可能讓 skill
router 重複觸發。可以安全移除：

```bash
rm -rf ~/.claude/skills/knowledge-base
```

舊版 code 還在引用 `get_bundled_skill_path("knowledge-base")` 這個版本
還能跑，但會印 `DeprecationWarning`；alias 預計在
research-hub-pipeline v0.70 移除。

## 各 plugin 直接安裝指令（不想跑 helper script 的話）

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills        # 9 skills
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
