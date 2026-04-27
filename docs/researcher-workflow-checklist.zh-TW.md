# 研究者 Workflow Checklist

英文版：[researcher-workflow-checklist.md](researcher-workflow-checklist.md)。

很多研究者的 setup 是：論文放 Zotero、筆記寫在 Obsidian、NotebookLM
產出 source-grounded 摘要、稿子寫在 Word / LaTeX / Markdown。這份
checklist 對應這個 setup。

## 工具速查

確認你現在用的：

- [ ] Zotero：references、PDF、tag、collection。
- [ ] Obsidian：Markdown 筆記、project memory、cluster dashboard。
- [ ] NotebookLM：source-grounded 摘要、audio、mind map、Q&A。
- [ ] Word / LaTeX / Markdown：論文草稿。
- [ ] Claude / Codex / Gemini：AI 輔助研究工作。

然後對照下面安裝對應的 skill。

## Zotero + Obsidian

安裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
pip install research-hub-pipeline
research-hub setup
```

用這些 skill：

- [research-hub](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md)：找論文、ingest metadata、寫 Obsidian 筆記、維護 cluster。
- [literature-triage-matrix](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)：依 method、data、claim、limitation、relevance 比較論文。
- [research-context-compressor](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md)：產 `.research/` manifest，AI session 不必重掃整個 project。
- [research-project-orienter](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md)：讀 `.research/` manifest，快速產 orientation memo。

需要時加：

```bash
claude plugin install zotero-skills@ai-research-skills
```

- [zotero-skills](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md)：深度 Zotero CRUD、batch cleanup、tag、collection、item edit、PDF attachment。

## Obsidian + NotebookLM

安裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
pip install "research-hub-pipeline[playwright]"
research-hub setup        # 互動時選 analyst persona（無 Zotero）
research-hub notebooklm login
```

用這些 skill：

- [research-hub](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md)：把本機 PDF / DOCX / Markdown / TXT / URL 匯入 Obsidian-backed workspace。
- [notebooklm-brief-verifier](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md)：對照 source bundle 驗證下載的 NotebookLM brief。
- [literature-triage-matrix](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)：把筆記跟 brief 轉成比較表。

典型 workflow：

```text
本機檔案 -> research-hub import-folder -> Obsidian 筆記
Obsidian cluster -> NotebookLM bundle/upload/generate/download
下載的 brief -> notebooklm-brief-verifier
verified sources -> literature-triage-matrix
```

## Zotero + NotebookLM

安裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
pip install "research-hub-pipeline[playwright]"
research-hub setup        # researcher persona
research-hub notebooklm login
```

用這些 skill：

- [research-hub](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md)：從 Zotero 選論文、做 source bundle、上傳 NotebookLM、下載輸出。
- [notebooklm-brief-verifier](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md)：抓出漏掉的 source、未根據的 claim、矛盾敘述。
- [zotero-skills](https://github.com/WenyuChiou/zotero-skills/blob/master/skills/zotero-skills/SKILL.md)：超出 research-hub workflow 的 item-level Zotero 編輯時用。

## 三個都用：Zotero + Obsidian + NotebookLM

先裝 `research-hub`：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
pip install "research-hub-pipeline[playwright]"
research-hub setup        # researcher persona
research-hub notebooklm login
```

核心 skill：

- [research-hub](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub/SKILL.md)：從搜尋到 ingest 到 organize 到 NotebookLM 的完整迴路。
- [literature-triage-matrix](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)：文獻比較表。
- [notebooklm-brief-verifier](https://github.com/WenyuChiou/research-hub/blob/master/skills/notebooklm-brief-verifier/SKILL.md)：NotebookLM 輸出驗證。
- [research-context-compressor](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md)：project memory 供未來 AI session 用。
- [research-project-orienter](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md)：快速 project orientation。

典型迴路：

```text
找論文 -> Zotero collection
Zotero collection -> Obsidian 論文筆記
Obsidian cluster -> NotebookLM source bundle
NotebookLM brief -> verifier
verified sources -> literature matrix
literature matrix -> 論文 claim
```

## 寫論文中

安裝：

```bash
claude plugin install academic-writing-skills@ai-research-skills
```

用這些 skill：

- [paper-memory-builder](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/SKILL.md)：抽出 `.paper/claims.yml` 與 `.paper/figures.yml`。
- [academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills/blob/main/skills/academic-writing-skills/SKILL.md)：論文文字修改、claim-evidence audit、reviewer response、figure / journal format 檢查。

建議 manuscript workflow：

```text
manuscript + figures -> paper-memory-builder
.paper/claims.yml + .paper/figures.yml -> academic-writing-skills
revised manuscript -> reviewer response / submission checklist
```

## 多 AI assistant

裝其中一個或兩個：

```bash
claude plugin install codex-delegate@ai-research-skills
claude plugin install gemini-delegate@ai-research-skills
```

用這些 skill：

- [codex-delegate](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md)：code-heavy、機械性、跨多檔案的 implementation 工作。
- [gemini-delegate](https://github.com/WenyuChiou/gemini-delegate-skill/blob/master/skills/gemini-delegate/SKILL.md)：長 context 閱讀、雙語 / CJK 寫作、source synthesis、second-opinion review。
- [research-hub-multi-ai](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-hub-multi-ai/SKILL.md)：決定 Claude / Codex / Gemini 怎麼分 research-hub 工作。

## 最小建議

- [ ] 大部分研究者：裝 `research-workspace`（含 9 個）+ `academic-writing-skills`。
- [ ] Zotero 重度使用者：再加 `zotero-skills`。
- [ ] Coding 重度使用者：再加 `codex-delegate`。
- [ ] 長 context / 雙語使用者：再加 `gemini-delegate`。
- [ ] NotebookLM 使用者：產出 brief 後一定要先過 `notebooklm-brief-verifier`，再採用。
