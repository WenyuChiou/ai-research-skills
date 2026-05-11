# 安裝指引 — 從零到可以用

語言：[English](setup-guide.md) | [繁中](setup-guide.zh-TW.md)

這份文件帶你從「什麼都沒裝」走到「能叫 Claude 幫我整理 paper、會跑」。
如果你 Claude Code / Python / Zotero 都已經 work，跳到
[install.zh-TW.md](install.zh-TW.md) 就好（那篇只講 plugin install）。

**時間預算：**

- Phase A + B 單獨跑（~20 分鐘）→ 裝好 14 支裡的 10 支；research-workspace plugin 裡 6 支純 reasoning 立刻能用，不需要 Zotero。
- Phase A + B + C（~40 分鐘）→ 12 支 wired with Zotero 連接（B-extra 加 academic-writing-skills 拿到第 12 支）。
- Phase A + B + C + D（~60 分鐘）→ research-hub Python pipeline 接上 13 支；codex / gemini delegate 等 Phase E3。

任何一個 phase 收手都可以、用裝好的就行。

**約定**：每個步驟結尾有 `# verify` 區塊，跑那行命令確認沒爆才往下走。
跑失敗的話看 [Phase F — 故障排除](#phase-f--故障排除)。

---

## Phase A — Foundation（裝 runtime）

需要 3 個 CLI 工具：**Claude Code**、**Python 3.10+**、**Git**。
如果你 terminal 裡打 `python` 跟 `git` 已經有反應，A2 / A3 可以跳過。

### A1. 安裝 Claude Code

1. 瀏覽器打開 https://claude.ai/code
2. 下載對應作業系統的安裝檔（Windows `.msi` / macOS `.dmg` / Linux 看頁面）。
3. 預設選項裝起來。
4. **開新的** terminal 視窗（舊的看不到新 PATH）。

```bash
# verify
claude --version
# 預期：claude-code/<version>（任何版本字串都可以）
```

如果 `claude: command not found`，看 [F1](#f1-claude-command-not-found)。

### A2. 安裝 Python 3.10 以上

1. 瀏覽器打開 https://www.python.org/downloads/
2. 下載最新 Python 3.x。
3. **Windows 限定**：安裝第一個畫面要勾 **"Add python.exe to PATH"** 再按 Install。
   這個 checkbox 是 #1 安裝失敗原因。
4. macOS / Linux：預設即可。

```bash
# verify
python --version
# 預期：Python 3.10.x 或更新（3.10、3.11、3.12 都行）

pip --version
# 預期：pip 23.x 或更新
```

macOS / Linux 上指令可能是 `python3` 跟 `pip3`，兩種都行，下面其餘步驟相應替換。

### A3. 安裝 Git

1. 瀏覽器打開 https://git-scm.com/downloads
2. 預設選項裝起來。
3. Windows 上的安裝檔叫 **Git for Windows**，會順便裝 git-bash（Claude Code 在 Windows 內部會用）。

```bash
# verify
git --version
# 預期：git version 2.40.x 或更新
```

### Phase A checkpoint

3 個指令都印得出版本 → 可以進 Phase B。

---

## Phase B — 第一批 plugin（裝完馬上能用）

裝起來會給你 6 支純 reasoning skill，不需要 Zotero、不需要 Python pipeline、不需要 API key。
手動丟一份 paper list 給 Claude 做 triage、寫 outline、驗證 NotebookLM brief 都已經能做。

### B1. 加 marketplace

開 terminal（**不要**在 Claude 對話裡用 `/plugin` UI — 那會 fallback 到 SSH 容易爆）：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
```

```bash
# verify
claude plugin marketplace list
# 預期：列表裡看得到 "ai-research-skills"
```

### B2. 安裝 research-workspace plugin

```bash
claude plugin install research-workspace@ai-research-skills
```

```bash
# verify
ls ~/.claude/skills/
# 預期：10 個資料夾 — literature-triage-matrix、
# research-hub、research-design-helper、paper-memory-builder、
# paper-summarize、notebooklm-brief-verifier、
# research-context-compressor、research-project-orienter、
# research-hub-multi-ai、zotero-library-curator
```

### B3. Smoke test：3 篇 paper 出表

打開 Claude Code 在任何資料夾、貼這段：

```
幫我把下面 3 篇 paper 做一個 literature triage matrix:
- "Memory enables ToM-like behaviour in LLM poker agents", arXiv:2604.04157
- "Multi-agent LLM social learning", arXiv:2604.02677
- "Triadic Loop alignment framework", arXiv:2604.18850
```

```bash
# verify
ls .research/
# 預期：有一個 literature_matrix.md
cat .research/literature_matrix.md | head
# 預期：9 欄 markdown 表格（Citation / Question / Method / 等等）
```

Claude 回「我沒有這個 skill」或沒生表 → 看 [F2](#f2-claude-沒-trigger-skill)。

### Phase B checkpoint

14 支裡的 10 支裝好（research-workspace plugin），有 working literature matrix、不需要任何外部設定。
research-workspace 裡 6 支純 reasoning skill 立刻可用；剩下 4 支（research-hub、research-hub-multi-ai、
zotero-library-curator 的 apply mode、完整的 literature-triage-matrix 含 paper search）要 Phase C / D / E。
要寫 / 修稿就接 Phase B-extra；只要文獻整理就跳 Phase C。

### B-extra. academic-writing-skills（選擇性，~1 分鐘）

要寫 / 修 manuscript 的話加這支：

```bash
claude plugin install academic-writing-skills@ai-research-skills
```

```bash
# verify
ls ~/.claude/skills/academic-writing-skills/
# 預期：有 SKILL.md 加 references/
```

裝完是第 11 支 — banned-word audit、claim-evidence check、journal format、reviewer response。
只要做 lit triage / lit review 就跳過。

---

## Phase C — Zotero 連接（選擇性）

加完之後 Zotero CRUD 跟 audit cleanup 都會 work。沒做 Phase C 的話，
`zotero-library-curator` 只能做 preview（可以**提議**清理但不能**執行**）。

### C1. 安裝 Zotero 桌面版

1. 瀏覽器打開 https://www.zotero.org/download/
2. 下載 **Zotero**（不是 Zotero Connector — 那是瀏覽器擴充、不一樣的東西）。預設選項裝起來。
3. 啟動 Zotero、登入（免費帳號也可）。Sync 會在背景跑、不用等。

### C2. 開 Local API

Zotero 桌面版裡：

1. **Edit → Settings**（Windows / Linux）或 **Zotero → Settings**（macOS）。
2. 左側 sidebar 點 **Advanced**。
3. 勾 **"Allow other applications on this computer to communicate with Zotero"**。
4. 關掉 Settings 視窗（**不用**重啟 Zotero）。

```bash
# verify（Zotero 必須開著）
curl http://localhost:23119/api/users/0
# 預期：一個 JSON、有 "userID" 欄位
```

`Connection refused` → 看 [F3](#f3-zotero-local-api-port-23119-連不到)。

**替代方案：Web API key。** 跑不了 Zotero 桌面版（無頭 server、共用實驗室機器）的話，
可以改用 Zotero web API — 看 [zotero-skills README](https://github.com/WenyuChiou/zotero-skills#readme) 的 API key 路徑。
這份文件其餘部分假設用 local API。

### C3. 安裝 zotero-skills plugin

```bash
claude plugin install zotero-skills@ai-research-skills
```

```bash
# verify
ls ~/.claude/skills/zotero-skills/
# 預期：有 SKILL.md 跟 references/（如果有的話）
```

### C4. 測 Zotero 連接

Claude Code 裡問：

```
列出我 Zotero library 最近的 5 個 item。
```

Claude 應該呼叫 Zotero local API、回真的 title。
如果回「我不能存取 Zotero」或空結果 → 看 [F4](#f4-zotero-skill-找不到-item)。

### Phase C checkpoint

14 支裡 12 支 wired up（research-workspace 10 支 + Phase B-extra 的 academic-writing-skills + zotero-skills），
zotero-library-curator 從 preview-only 升級成 apply-capable。剩下 2 支（`codex-delegate`、`gemini-delegate`）
等 Phase E3 裝完對應的 CLI binary 後加進來。Phase D 給 `research-hub`、`research-hub-multi-ai`、
`literature-triage-matrix` 的 paper-search 模式接上 Python CLI 後台。

---

## Phase D — research-hub Python CLI（完整 pipeline）

加完之後有 paper discovery（arxiv / semantic scholar / pubmed 搜尋）、
Obsidian / NotebookLM 整合、cluster 管理、curator skill 會 defer 給它的 backfill / dedup operation。

### D1. 安裝 package

```bash
pip install research-hub-pipeline
```

出現 `Permission denied` 或想 isolation → 看 [F5](#f5-pip-install-permission-或-isolation)。

```bash
# verify
research-hub --version
# 預期：research-hub 0.7x 或更新
```

### D2. 互動式 setup

```bash
research-hub setup --persona researcher
```

Wizard 問 3-4 個問題：

- **Zotero default collection name**：挑一個（例如 `to-read`）。只用 root library 就跳過。
- **NotebookLM login**：先回 `n`（之後 Phase E2 再加）。
- **Install sample data**：建議 `y`、給你東西 smoke test。

`setup` 指令是 **idempotent** — 隨時重跑換 persona / refresh。

Persona 速查表：

| Persona | 何時挑這個 |
|---|---|
| `researcher` | Zotero + Obsidian + NotebookLM workflow（最常見） |
| `analyst` | 只用 Obsidian + NotebookLM、不用 Zotero |
| `humanities` | Zotero + 質性 / archival research、不寫 code repo |
| `internal` | 純讀 catalog、不裝 |

### D3. 驗證安裝健康

```bash
research-hub doctor
```

預期 output：checklist、Python 版本、Zotero local API 連接（Phase C 有做的話）、skill 目錄存在都打勾。
你沒做的 optional integration 顯示黃色 warning 沒關係。

### D4. End-to-end smoke test

Claude Code 裡：

```
用 research-hub discover 找 5 篇關於 "agent-based flood modeling" 的近期 paper，
然後出 literature triage matrix。
```

預期：Claude 呼叫 `research-hub discover`、拿到 paper list、把 list 丟給
`literature-triage-matrix`、寫出 `.research/literature_matrix.md`。

### Phase D checkpoint

14 支 skill 全部 wired up，core setup 結束。

---

## Phase E — 選擇性 add-on

每個都獨立 — 自己會用到的再裝。

### E1. Obsidian（paper notes + cluster dashboard）

1. https://obsidian.md 下載安裝。
2. 開一個 vault（任何你要拿來放研究 note 的資料夾）。
3. 告訴 research-hub 你的 vault 路徑：

```bash
research-hub config set obsidian.vault_path /path/to/your/vault
```

```bash
# verify
research-hub config get obsidian.vault_path
# 預期：印出你剛設的路徑
```

### E2. NotebookLM browser automation

1. 裝 playwright extras：
   ```bash
   pip install "research-hub-pipeline[playwright]"
   ```
2. 跑一次 browser login：
   ```bash
   research-hub notebooklm login
   ```
   瀏覽器會打開、用有 NotebookLM access 的 Google 帳號登入。
   登入完畢跳轉之後關掉瀏覽器。

```bash
# verify
research-hub notebooklm status
# 預期：印出 "logged in" + 你的 Google 帳號
```

### E3. Codex CLI / Gemini CLI（多 AI delegation）

先照 upstream README 裝 CLI binary：

- [Codex CLI](https://github.com/WenyuChiou/codex-delegate#readme) →
  `npm install -g @openai/codex`
- [Gemini CLI](https://github.com/WenyuChiou/gemini-delegate-skill#readme) →
  `npm install -g @google/gemini-cli`

然後裝 delegate plugin：

```bash
claude plugin install codex-delegate@ai-research-skills
claude plugin install gemini-delegate@ai-research-skills
```

```bash
# verify
codex --version
gemini --version
# 預期：兩個都印出版本字串
```

---

## Phase F — 故障排除

### F1. `claude: command not found`

Windows 上最常見：你在**安裝 Claude Code 之前就開好的** terminal 跑 `claude --version`。
Installer 更新 PATH、但只有新 terminal 看得到。

- **Windows**：關掉所有 PowerShell / Command Prompt 視窗、開新的。
- **macOS / Linux**：`source ~/.zshrc`（或 `~/.bashrc`）、或開新 terminal 視窗。

新 terminal 還是找不到：

- 確認安裝位置：macOS / Linux `ls "$HOME/.claude/bin/"`、Windows `dir "%USERPROFILE%\.claude\bin"`。
- 重跑 installer、讓它更新 PATH。

### F2. Claude 沒 trigger skill

你用的 trigger phrase 沒有 match 任何 skill 的 `description` 欄位。
每個 skill 的 trigger phrase 都在 `SKILL.md` 的 frontmatter `description:` 裡。

修法：

- 用 skill description 裡**完全一樣**的 trigger phrase，例如「**make a literature matrix** for these papers」。
- 或直接點名 skill：「用 `literature-triage-matrix` skill 把這幾篇 paper 整理一下。」

Trigger phrase 看 `~/.claude/skills/<skill-name>/SKILL.md`（找 "Trigger phrases" 段落）。

### F3. Zotero local API（port 23119）連不到

```bash
# 診斷
curl -v http://localhost:23119/api/users/0
```

- **`Connection refused`**：Zotero 桌面版沒開，或 Phase C2 的 "Allow other applications..." checkbox 沒勾。
- **別的 process 在用這個 port**：rare、Zotero 通常是唯一用 23119 的。停掉那個 process。
- **防火牆**：Windows Defender 或公司防火牆可能擋 localhost-to-localhost。
  加一條 inbound rule 開 port 23119（TCP）、scope 限 `127.0.0.1`。

### F4. Zotero skill 找不到 item

- 確認 Zotero 開著、F3 的 `curl` 有回 JSON。
- 確認 library 不是空的 — Zotero 桌面版裡至少加一筆 item。
- 用 Zotero Web API 替代 local API → 確認 API key 有設好，看 [zotero-skills README](https://github.com/WenyuChiou/zotero-skills#readme)。

### F5. `pip install` permission 或 isolation

`pip install research-hub-pipeline` 出現 **`Permission denied`** 或 **`error: externally-managed-environment`**：

**最好**（isolation、不需要 system pip）：

```bash
pip install --user pipx
pipx install research-hub-pipeline
```

**替代**（venv）：

```bash
python -m venv ~/.venvs/research-hub
source ~/.venvs/research-hub/bin/activate   # macOS / Linux
# 或 Windows：
~/.venvs/research-hub/Scripts/Activate.ps1
pip install research-hub-pipeline
```

裝完 `research-hub --version` 應該 work。用 venv 的話、每個要用 research-hub 的新 terminal 都要先 activate
（或把 venv 的 `bin/` 永久加到 PATH）。

### F6. `research-hub doctor` 顯示紅色錯誤

紅色標記上面那行就是失敗的 check：

- `Zotero local API: unreachable` → 看 F3。
- `Python version: too old` → 照 A2 重裝 Python 3.10+。
- `Skills directory not found` → 重跑 `claude plugin install research-workspace@ai-research-skills`（B2）。

### F7. 非 Claude Code host 上的 skill 安裝

要在 Codex CLI / Gemini CLI / Cursor / Hermes 等 agentskills.io 相容 host 上用這些 skill，
看 [README → Using these skills outside Claude Code](../README.zh-TW.md)（zh-TW 版有對應段落）
跟 [Hermes 相容性審計](../.research/hermes-compatibility-audit.md) 了解什麼經過驗證、什麼是 host-specific。

---

## 下一步

- Skill-by-skill 安裝參考：[install.zh-TW.md](install.zh-TW.md)
- Workflow-by-workflow 指南：[researcher-workflow-checklist.zh-TW.md](researcher-workflow-checklist.zh-TW.md)
- Demo：[demo-walkthrough.zh-TW.md](demo-walkthrough.zh-TW.md)
- 14 支 skill 完整 catalog：[skill-directory.zh-TW.md](skill-directory.zh-TW.md)
