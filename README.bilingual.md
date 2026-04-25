# AI Research Skills / AI 研究 Skills

English and Traditional Chinese side-by-side guide for choosing and installing
research-oriented AI skills for researchers and research-adjacent users.

中英文對照版，給研究者與研究相關使用者快速判斷需要哪個 research AI skill，以及要去哪裡下載或安裝。

Links:

- English: [README.md](README.md)
- 繁中: [README.zh-TW.md](README.zh-TW.md)
- Full directory: [docs/skill-directory.md](docs/skill-directory.md)
- Researcher checklist: [docs/researcher-workflow-checklist.md](docs/researcher-workflow-checklist.md)
- Machine-readable catalog: [catalog/skills.yml](catalog/skills.yml)

## What This Repo Is / 這個 Repo 是什麼

| English | 繁中 |
|---|---|
| This repo is an umbrella catalog for AI skills used in research workflows. | 這個 repo 是研究工作流 AI skills 的總目錄。 |
| It does not duplicate skill bodies. Each skill remains maintained in its canonical repo. | 它不複製 skill 本體。每個 skill 仍由原本的 canonical repo 維護。 |
| Use this page to decide what to install, then follow the direct links. | 使用這頁判斷要裝什麼，然後點直接連結安裝。 |
| Target readers include graduate students, PhD researchers, postdocs, research engineers, librarians, research support staff, and AI power users. | 目標讀者包含研究生、博士生、博士後、研究人員、研究工程師、圖書館或研究支援人員，以及 AI 重度使用者。 |
| Each entry should explain the problem solved, the tool combination it fits, and where to install it. | 每一項都應該說清楚解決什麼問題、適合哪一種工具組合，以及要去哪裡安裝。 |

## Tool Combinations / 工具組合

| If you use... | 如果你使用... | Start with |
|---|---|---|
| Zotero + Obsidian | Zotero + Obsidian | [`research-hub`](https://github.com/WenyuChiou/research-hub) |
| Obsidian + NotebookLM | Obsidian + NotebookLM | [`research-hub`](https://github.com/WenyuChiou/research-hub) + [`notebooklm-brief-verifier`](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) |
| Zotero + NotebookLM | Zotero + NotebookLM | [`research-hub`](https://github.com/WenyuChiou/research-hub) |
| Zotero + Obsidian + NotebookLM | Zotero + Obsidian + NotebookLM | Full `research-hub` workflow |
| Manuscript writing or reviewer response | 論文寫作或回覆 reviewer | [`academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) |
| Deep Zotero library cleanup | 深度 Zotero library 整理 | [`zotero-skills`](https://github.com/WenyuChiou/zotero-skills) |
| Coding-heavy AI delegation | 大量 coding 工作委派 | [`codex-delegate`](https://github.com/WenyuChiou/codex-delegate) |
| Long-context or bilingual AI delegation | 長 context 或中英文工作委派 | [`gemini-delegate`](https://github.com/WenyuChiou/gemini-delegate-skill) |

## Quick Install / 快速安裝

### research-hub

English: use this if you want AI to operate Zotero, Obsidian, NotebookLM,
clusters, dashboards, and local research artifacts.

繁中：如果你想讓 AI 操作 Zotero、Obsidian、NotebookLM、clusters、dashboards 和本地研究 artifacts，先裝這個。

```bash
pip install research-hub-pipeline
research-hub install --platform claude-code
```

NotebookLM automation:

```bash
pip install "research-hub-pipeline[playwright]"
research-hub notebooklm login
```

### academic-writing-skills

English: use this for manuscript writing, reviewer response, claim-evidence
audits, journal format checks, and figure-text consistency.

繁中：用於論文寫作、reviewer response、claim-evidence audit、期刊格式檢查和圖文一致性。

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills
```

### zotero-skills

English: use this for deep Zotero CRUD, collections, tags, notes, item edits,
and PDF attachments.

繁中：用於深度 Zotero CRUD、collections、tags、notes、item edits 和 PDF attachments。

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```

### Delegation skills / AI 委派 skills

English: use these when Claude should delegate work to Codex or Gemini.

繁中：當 Claude 需要把工作委派給 Codex 或 Gemini 時使用。

```bash
git clone https://github.com/WenyuChiou/codex-delegate ~/.claude/skills/codex-delegate
git clone https://github.com/WenyuChiou/gemini-delegate-skill ~/.claude/skills/gemini-delegate-skill
```

## Complete Skill Inventory / 完整 Skill 清單

### research-hub skills

| Skill | English use case | 繁中用途 | Link |
|---|---|---|---|
| `research-hub` | Operate literature discovery, source ingest, Zotero, Obsidian, NotebookLM, dashboard, and vault maintenance. | 操作文獻探索、資料匯入、Zotero、Obsidian、NotebookLM、dashboard 和 vault 維護。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/knowledge-base/SKILL.md) |
| `research-hub-multi-ai` | Split research-hub work across Claude, Codex, Gemini, or another assistant. | 在 Claude、Codex、Gemini 或其他 assistant 之間分配 research-hub 工作。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md) |
| `research-context-compressor` | Create `.research/` manifests so future AI sessions avoid repeated repo scans. | 建立 `.research/` manifests，讓未來 AI session 不必反覆掃整個 repo。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md) |
| `research-project-orienter` | Read `.research/` manifests and produce a fast orientation memo. | 讀取 `.research/` manifests 並產生快速 project orientation memo。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md) |
| `literature-triage-matrix` | Compare papers by method, data, claim, limitation, and relevance. | 依 method、data、claim、limitation、relevance 比較文獻。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md) |
| `paper-memory-builder` | Extract `.paper/claims.yml` and `.paper/figures.yml` for manuscript work. | 為論文工作抽取 `.paper/claims.yml` 和 `.paper/figures.yml`。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md) |
| `notebooklm-brief-verifier` | Verify a downloaded NotebookLM brief against the uploaded source bundle. | 對照 source bundle 檢查下載的 NotebookLM brief 是否漏來源或產生 unsupported claims。 | [SKILL.md](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md) |

### Standalone skills / 獨立 skills

| Skill | English use case | 繁中用途 | Install / Link |
|---|---|---|---|
| `academic-writing-skills` | Manuscript revision, claim-evidence audit, reviewer response, journal compliance, and figure-text consistency. | 論文修改、claim-evidence audit、reviewer response、期刊規範和圖文一致性。 | [repo](https://github.com/WenyuChiou/academic-writing-skills) / [SKILL.md](https://github.com/WenyuChiou/academic-writing-skills/blob/main/SKILL.md) |
| `zotero-skills` | Deep Zotero CRUD, tags, collections, notes, item edits, and PDF attachments. | 深度 Zotero CRUD、tags、collections、notes、item edits 和 PDF attachments。 | [repo](https://github.com/WenyuChiou/zotero-skills) / [SKILL.md](https://github.com/WenyuChiou/zotero-skills/blob/master/SKILL.md) |
| `codex-delegate` | Delegate implementation-heavy or many-file coding work to Codex CLI. | 將大量 implementation 或 many-file coding 工作委派給 Codex CLI。 | [repo](https://github.com/WenyuChiou/codex-delegate) / [SKILL.md](https://github.com/WenyuChiou/codex-delegate/blob/master/SKILL.md) |
| `gemini-delegate` | Delegate long-context reading, bilingual/CJK writing, synthesis, or second-opinion review to Gemini CLI. | 將長 context 閱讀、中英文寫作、synthesis 或 second-opinion review 委派給 Gemini CLI。 | [repo](https://github.com/WenyuChiou/gemini-delegate-skill) / [SKILL.md](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/SKILL.md) |

## Minimal Recommendation / 最小建議組合

| English | 繁中 |
|---|---|
| Most researchers should start with `research-hub` and `academic-writing-skills`. | 多數研究者可以先從 `research-hub` 和 `academic-writing-skills` 開始。 |
| Add `zotero-skills` if you maintain a large Zotero library. | 如果你有大型 Zotero library，再加 `zotero-skills`。 |
| Add `notebooklm-brief-verifier` whenever you use NotebookLM. It is installed through `research-hub`. | 只要使用 NotebookLM，就應使用 `notebooklm-brief-verifier`。它會透過 `research-hub` 安裝。 |
| Add delegation skills only if you actively use Codex or Gemini. | 只有在你實際使用 Codex 或 Gemini 時，再安裝 delegation skills。 |
