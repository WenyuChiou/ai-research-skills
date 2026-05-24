# 安裝指引

這個 repo 是一份可攜的 `SKILL.md` catalog。Claude Code marketplace 是
最快的 packaged install path；Codex CLI、Cursor、Gemini CLI、Hermes、
OpenClaw、Windsurf 或通用 API client 也可以載入同一批 `SKILL.md`。
英文版：[install.md](install.md)。

前置條件：至少有一個能讀 Markdown context 的 AI host。Claude Code
使用者可以透過 marketplace 安裝並保留自動觸發；其他 host 則需要明確
指定要載入哪一份 `SKILL.md`。

> **第一次來？** Claude Code / Python / Zotero 都還沒 work 的話，
> 先看 [**setup-guide.zh-TW.md**](setup-guide.zh-TW.md) —— 從 runtime
> 到 plugin 到 Zotero local API 整個 end-to-end 帶你跑，每步有驗證
> 指令。這頁假設你 prereq 都 work，專注在「哪個 plugin 對應哪個 workflow」。

完整 skill 列表跟連結：[skill-directory.zh-TW.md](skill-directory.zh-TW.md)。
可攜 `SKILL.md` 指令與可執行 runtime 需求的分界，請看
[runtime-contract.zh-TW.md](runtime-contract.zh-TW.md)。

## 先選安裝路徑

| 使用情境 | 建議路徑 | 驗證方式 |
|---|---|---|
| Claude Code | `claude plugin marketplace add` + `claude plugin install` | `claude plugin list` |
| Claude Code 加 literature pipeline 自動化 | Marketplace install 加 `pip install research-hub-pipeline` 與 `research-hub setup` | `claude plugin list` 加 `research-hub auto ... --no-nlm` smoke test |
| Codex CLI / Cursor / Windsurf | Clone canonical skill repo，將 `SKILL.md` 放入 host 的 skills / rules 目錄，或 inline 到 prompt | Host 自己的 discovery 檢查，或明確 prompt smoke test |
| Gemini CLI / 通用 API client | 把 `SKILL.md` inline 成 prompt 或 system context | Prompt smoke test |
| Hermes | `hermes skills install <raw-SKILL.md-url>` | `hermes skills list`；本 repo 目前只有 `literature-triage-matrix` 在 Hermes 0.13.0 驗證 |
| OpenClaw | 在 OpenClaw 支援時，使用 `~/.openclaw/skills/<skill>/SKILL.md` 這類 directory 形狀 | 手動檢查 host discovery；本 repo 尚未 release-grade verified |

## 路徑 A — Claude Code marketplace（推薦）

主 README 跟 [README.zh-TW.md](../README.zh-TW.md) 已經把通用分流講完。
Claude Code 最短路徑是：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
claude plugin list
```

### Windows cmd.exe

如果把多行指令一次貼到 `cmd.exe`，有時只會執行第一行。請逐行執行，
或使用下面這個單行版：

```cmd
claude plugin marketplace add WenyuChiou/ai-research-skills && claude plugin marketplace update ai-research-skills && claude plugin install research-workspace@ai-research-skills --scope user && claude plugin list
```

`claude plugin list` 只驗證 Claude Code marketplace 狀態；它不能代表
Codex、Cursor、Hermes、OpenClaw 或通用 API client 已經載入 `SKILL.md`。

## 路徑 B — research-hub Python CLI（要 literature pipeline 自動化時加）

使用 Zotero、Obsidian、NotebookLM 或這 3 個任一兩個的組合時用：

```bash
pip install research-hub-pipeline
research-hub setup --persona researcher
research-hub doctor
research-hub auto "agent-based modeling" --max-papers 3 --no-nlm
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
/ Gemini 的話，若你安裝的 `research-hub-pipeline` 版本支援這些 platform
adapter，安裝完之後再指定平台：

```bash
research-hub install --platform cursor
research-hub install --platform codex
research-hub install --platform gemini
```

OpenClaw 與 generic API client 目前請使用
[在 Claude Code 之外用這些 skills](#在-claude-code-之外用這些-skills)
的 raw `SKILL.md` 路徑；本 repo 尚未加入 release-grade OpenClaw 驗證。

在 Claude Code 預設路徑下，裝完之後 11 個 skill 出現在
`~/.claude/skills/` 底下：`research-hub`、`research-design-helper`、
`research-context-compressor`、`research-project-orienter`、
`research-hub-multi-ai`、`literature-triage-matrix`、
`paper-memory-builder`、`paper-summarize`、`notebooklm-brief-verifier`、
`zotero-library-curator`、`gap-to-topic`。

*註*: 這條 Python-CLI 路徑(`research-hub setup`)**會**把 skill 展到
`~/.claude/skills/` 底下。Claude Code marketplace 路徑(`claude plugin
install …@ai-research-skills`)**不會** —— 那些 skill 住在
`~/.claude/plugins/cache/…` 底下。兩條路徑都能用,只是 SKILL.md 落點不同。
端到端紀錄看 [verification.md](verification.md) §2026-05-20。

NotebookLM 的瀏覽器自動化（如果 setup 時答 yes 就會幫你裝；跳過的話
個別在這裡裝）：

```bash
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login --auto-detect
```

不靠 NotebookLM 先做煙霧測試：

```bash
research-hub auto "agent-based modeling" --max-papers 3 --no-nlm
```

在要求任何 AI host 跑文獻搜尋前，先做 runtime preflight：
`research-hub describe --json`、`research-hub doctor`，再跑上面的
小型 `auto ... --no-nlm` smoke test。安裝這個 catalog 或複製
`SKILL.md`，不等於已安裝 Python CLI。

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
claude plugin install research-workspace@ai-research-skills        # 11 skills
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

`claude plugin install` 那條路徑只有 Claude Code 認得。可攜層是每個
skill 的 `SKILL.md`，加上它引用的 `references/`、`scripts/` 與 workflow
contracts。非 Claude host 通常沒有 Claude Code 的 auto-trigger，所以要在
prompt 裡明確說要用哪個 skill，或放進該 host 自己的 skills / rules 目錄。

### 1. 拿原始檔

```bash
git clone https://github.com/WenyuChiou/research-hub
git clone https://github.com/WenyuChiou/academic-writing-skills
git clone https://github.com/WenyuChiou/zotero-skills
git clone https://github.com/WenyuChiou/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill
```

每個 repo 的 `SKILL.md` 都在 `skills/<skill-name>/` 底下。`research-hub`
有 11 份 skill；其他 4 個 repo 各 1 份。

### 2. 各 host 載入方式

| Host | 怎麼載入 `SKILL.md` | 本 repo 狀態 |
|---|---|---|
| **Codex CLI** | 如果你的 Codex 版本支援 skills directory，就放進 Codex skills 目錄；否則把 `SKILL.md` inline 到 `codex exec` 或 task prompt。 | 結構上可攜；不是 marketplace install。 |
| **Cursor / Windsurf** | 把 `SKILL.md` 放進 `.cursor/rules/`、`~/.cursor/skills/`，或目前 editor 支援的 rules / skills 位置。 | 結構上可攜；用 editor discovery 驗證。 |
| **Gemini CLI** | 把 `SKILL.md` inline 進 prompt，例如 `gemini -p`。 | 結構上可攜；沒有 auto-trigger。 |
| **Hermes Agent** | `hermes skills install <github-raw-url-to-SKILL.md>`。 | `literature-triage-matrix` 已在 Hermes 0.13.0 skill-load 驗證；inference loop 尚未測。 |
| **OpenClaw** | 在你的 OpenClaw 安裝支援 `SKILL.md` skills 時，用 `~/.openclaw/skills/<skill>/SKILL.md` 這類目錄。 | 結構上相容；本 repo 尚未 release-grade verified。 |
| **通用 API client** | 把 `SKILL.md` 當 system / developer prompt context，需要時附上引用的 `references/`。 | 可攜 prompt contract。 |

### 3. 實際呼叫範例

`<repo>` 換成你 clone 下來的絕對路徑。

**Codex CLI** —— 對 5 篇 paper 跑 `literature-triage-matrix`：

```bash
codex exec --sandbox workspace-write -C "$(pwd)" \
  "$(cat <repo>/skills/literature-triage-matrix/SKILL.md)

  現在對 ./papers/ 5 篇做 9 欄比較表，輸出寫到
  .research/literature_matrix.md。"
```

**Gemini CLI** —— 對一段草稿跑 `academic-writing-skills` banned-word audit：

```bash
gemini -p "$(cat <repo>/skills/academic-writing-skills/SKILL.md)

audit 這段有沒有 banned word 跟 overclaim:
$(cat draft_paragraph.md)"
```

**Cursor / Windsurf** —— 把 skill 放進專案 rules：

```bash
mkdir -p .cursor/rules
cp <repo>/skills/literature-triage-matrix/SKILL.md \
   .cursor/rules/literature-triage-matrix.md
```

**OpenClaw** —— 手動 directory 形狀，等待 release-grade verification：

```bash
mkdir -p ~/.openclaw/skills/literature-triage-matrix
cp <repo>/skills/literature-triage-matrix/SKILL.md \
   ~/.openclaw/skills/literature-triage-matrix/SKILL.md
```

### 4. 哪些 skill 在 Claude Code 之外比較合理

- 純 workflow skill 最適合跨 AI 使用，例如 `literature-triage-matrix`、
  `gap-to-topic`、`research-design-helper`、`research-context-compressor`、
  `research-project-orienter`、`paper-memory-builder`。它們定義的是
  instructions 與 output contract，不依賴 Claude 特定機制。
- `academic-writing-skills` 只要 host 能讀 manuscript 與 `.paper/`
  context 就能用。
- `notebooklm-brief-verifier` 的 manual fallback 模式任何 host 都能跑。
- `zotero-skills` 需要 AI host 能呼叫 Zotero local 或 Web API；
  `SKILL.md` 本身只是 routing contract。
- `research-hub` 與 `research-hub-multi-ai` 不論哪個 AI 讀取 skill，
  都要先讓 `research-hub-pipeline` Python CLI 在 PATH 上。
- `codex-delegate` / `gemini-delegate` 主要適合 Claude Code 對外
  delegation；如果你已經在 Codex 或 Gemini 裡，通常直接用目標 skill 即可。
