# 審查治理與分支維護

[English](review-governance.md)

## 獨立審查門檻

此目錄倉庫以獨立 subagent 審查通過作為審查門檻，不要求正式 GitHub
reviewer `APPROVED`。審查者必須是沒有撰寫或實作本次變更的另一個 agent，
不能把作者自查改名為獨立審查。GitHub review 的實質發現仍需處理。

PR 轉為 Ready 或合併前：

1. 完成作者自查。
2. 由獨立 subagent 檢查實際 diff 與相關契約，在 PR 本文或連結報告記錄
   審查者／報告識別、完整 base/head SHA、範圍、結論、具體發現、測試證據
   及驗證缺口。通過時不得有未解決的阻擋問題。
   若審查本機快照，需記錄 tree SHA，並確認發布後 head 的 tree 完全相同，
   才能沿用該審查證據。
3. 適用本機測試與最新 head 的必要 CI 必須通過。本倉庫執行：
   `python -m pytest tests/ -q`、
   `python scripts/check_marketplace_consistency.py`、
   `python scripts/check_catalog_schema.py`。來源或版本變更另須遵循
   `CONTRIBUTING.md` 的嚴格即時來源健康檢查。
4. 再查合併狀態、未解決發現與目前 base/head。head 變更須重新獨立審查及
   重跑受影響測試／CI。base 變更須檢查整合差異並重跑受影響檢查，不能把
   不相容 base 的舊證據當成新證據。
5. 發布與合併授權分開處理。`AGENTS.md` 原有的規定仍保留：使用者收到
   審查與測試摘要後，需明確同意合併，除非目前明確使用者指示已涵蓋該動作。
   審查通過本身不授權合併、發布、部署或刪除分支。

不要提交 `APPROVE` 來製造通過紀錄，也不能略過已知阻擋、必要測試失敗或
GitHub 實際分支保護。如果 GitHub 設定仍要求正式 reviewer approval，應回報
具體衝突，另行取得設定變更授權。本文件不會修改 ruleset、分支保護、權限
或倉庫設定。

## 可設定的分支清理預覽

此倉庫有已合併 PR 留下的主題分支。預覽工具以一份唯讀報告取代逐一查詢：

```bash
python scripts/plan_branch_cleanup.py
python scripts/plan_branch_cleanup.py --config /path/to/branch-cleanup.json
```

需要 Python 3.10+ 與已設定好、可讀取此倉庫的 GitHub CLI（`gh`）。工具只做
GitHub GET 請求，完整分頁讀取分支與 PR；資料不完整或請求失敗就不產生計畫。
不登入、不建立憑證、不安裝軟體、不改權限或設定，也不刪除分支。沒有
`--apply` 選項。

`.github/branch-cleanup.json` 的預設值：

| 設定 | 預設 | 用途 |
| --- | --- | --- |
| `repository` | `WenyuChiou/ai-research-skills` | 精確倉庫 |
| `allowed_prefixes` | `codex/`、`docs/` | 字面分支前綴，須以 `/` 結尾 |
| `allowed_pr_authors` | `WenyuChiou` | 只有這些作者的已合併 PR 可列候選 |
| `keep_patterns` | `main`、`master`、`release/*`、`keep/*` | 區分大小寫的 shell 樣式保留規則 |
| `minimum_age_days` | `7` | 合併後至少經過的完整天數 |

前綴或作者清單為空就不產生候選。保留規則優先；預設分支、受保護或保護
狀態不明的分支一律保留，不因自訂允許清單而放行。

候選必須有從同一倉庫合併到目前預設分支的 PR，而且該 PR 記錄的 head SHA
須與遠端分支目前 head **完全相同**，PR 作者也須在允許清單中。仍有 open PR、
被 open PR 當作 base、存在關閉但未合併 PR、來源不明、找不到完全對應的合併
紀錄、head 已變或未滿保留天數，都會保留。Squash merge 以 PR 記錄的 head
比對，不只靠 Git 祖先關係。Fork 分支不會成為刪除目標；孤立或未合併分支
不會因為存在很久就被判定安全。PR 作者在清單中不代表沒有其他人的工作。

所有結果都是 `report-only`、`deletion_authorized: false`。候選不是刪除指令。
真正清理需另有授權，且執行前必須重查遠端 head、保護規則與 PR 相依關係，
確認沒有其他貢獻者或進行中的任務使用分支，檢查本機 worktree，並保留精確
倉庫／分支／SHA 與已合併 PR 紀錄以利復原。ref 變動或有任何疑點就保留。
此流程不刪他人工作、使用中、孤立、未合併或預設分支，也不排程自動清理。

## 離線驗證與限制

`--snapshot /path/to/snapshot.json` 可讀取完整離線匯出，欄位為 `repository`、
`branches`、`pulls`、`complete: true` 與含時區的 ISO `captured_at`。前三者
分別是 GitHub REST 倉庫物件與完整分頁的分支／PR 陣列。匯出須在 24 小時內，
但不代表遠端仍相同。只使用可信匯出；完整性標記只是輸入宣告，不是獨立
分頁稽核。不要把私人倉庫匯出存入此公開倉庫。

`python -m pytest tests/test_branch_cleanup.py -q` 檢查離線篩選、分頁、失敗與
不變更行為。單元 fixture 不等於即時 GitHub 或刪除測試。即時報告也只是當下
預覽，無法知道其他電腦的 worktree 或未推送修改。本工具不測試或執行刪除。
