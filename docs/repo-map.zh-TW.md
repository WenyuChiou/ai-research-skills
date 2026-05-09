# Repo 地圖

這份文件說明每個 skill 應該住在哪個 repo。

## 各 repo 的職掌

| Repo | 負責 | 不負責 |
|---|---|---|
| `research-hub` | Zotero / Obsidian / NotebookLM 工作流、`.research/` 工作區記憶、文獻比較矩陣、NotebookLM 驗證 | 稿件文字修訂、Zotero 深度 CRUD、模型治理 |
| `academic-writing-skills` | 稿件寫作、審稿回應、主張-證據稽核、期刊規範、圖文一致性 | Zotero 流程、NotebookLM 上傳、程式碼委派 |
| `zotero-skills` | Zotero item 深度操作、tag、collection、metadata 清理 | Obsidian / NotebookLM 管線邏輯 |
| `codex-delegate` | Claude 把程式碼密集任務委派給 Codex CLI 的 leaf | 研究領域工作流邏輯 |
| `gemini-delegate-skill` | Claude 把長 context 或多語言任務委派給 Gemini CLI 的 leaf | 研究領域工作流邏輯 |
| 模型 repo | 領域特定實驗、治理、耦合契約、稽核軌跡 | 通用研究工作區或寫作 skill |

## 為什麼不用 monorepo？

把 skill 內容複製進這個總目錄 repo 會留下過期副本。改採：

- 各 canonical repo 擁有實作與測試，
- 本 repo 擁有索引與定位，
- 對外宣傳先連到本 repo，使用者再去裝他們需要的特定 repo。

## 打包規則

如果一個新 skill 主要是關於：

- 研究工作區狀態 → `research-hub`，
- 稿件寫作 → `academic-writing-skills`，
- Zotero CRUD → `zotero-skills`，
- AI CLI 接手 → delegation repo，
- 領域模擬或耦合 → 模型 repo。
