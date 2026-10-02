# 第一次 live 執行前的確認

這是 supervisor 審查契約，不是 catalog runtime hook。
Catalog、wrapper sidecar 與 specification fixtures 不會自動強制執行。
在第一次 **live model-backed 測試或 delegation** 前確認，包含官方 plugin task
或直接 CLI/API 呼叫。唯讀 help/status 與 offline doubles 不算 live model 測試。

English: [live-run-preflight.md](live-run-preflight.md)

## 確認並顯示真正生效的設定

使用已授權、只回報狀態的 host 介面與最後實際 invocation。
CLI arguments、wrapper defaults、provider routing 可能覆蓋設定；
configured model 名稱不代表最後實際選用的 model。

| 欄位 | Supervisor 必須顯示什麼 |
|---|---|
| Host/runtime | 實際 host 與路徑：native plugin、adapter 或直接 CLI/API |
| Provider/model | 已解析 service、真正生效的 model identifier 與 overrides |
| Authentication mode | ChatGPT subscription、API、其他已知模式或 unknown；只報可用狀態，不顯示憑證值 |
| Budget/cost policy | 已批准 quota/spend/token policy 與 fallback 上限；不能由 subscription login 推定 API 預算 |
| Data destination/scope | 哪個 provider/service 取得哪些已批准檔案或 context，以及 tools/uploads/storage 的目的地 |

不要把 key、token、auth files 或帶憑證的 URL 貼到 chat、repo notes 或 CI logs。
只記錄已清理的 mode/status。Model、auth route、budget 或 data scope 不明時，
不能先呼叫 model 再確認。

## 沿用有效選擇，缺資料才詢問

1. 先前 explicit user choice 或已批准 canonical policy 若涵蓋本次 task 與實際設定，
   就沿用。Repo defaults 與 worker proposal 不能自行授權。
   顯示真正生效的值；不要每次執行都重問相同、未變更的選擇。
2. 第一次使用前，把缺少的重要選擇合成一個問題：
   provider/model、subscription 或 API 路徑、budget、data destination/scope。
   先前 model 偏好不能替代未知的 billing 或資料分享選擇。
3. 若 provider/model、auth、cost/budget、permission 或 data destination/scope
   發生既有批准範圍外的重要變更，先重新確認。
   不得默默升級 model、換 provider 或採用昂貴 fallback。
4. Auth 不可用或 model 不支援就維持 blocked。
   需要時另走已授權的安全 setup/handoff；不要在 chat 索取 secret，
   也不由這個 preflight 建立憑證或修改安全設定。
   Quota/error sentinel 不等於新路徑已獲批准。
5. 保留 task/run、已清理的實際設定、可用的既有 choice/policy、待確認項目與決定。
   私人使用者偏好與 project context 不得寫入公開 source repository。

## 驗證與架構界線

Fixtures 用 synthetic settings 測試上述決定，不會檢查真實帳號、證明 billing/sandbox
enforcement、開始 inference 或安裝 enforcement hook。
Supervising host 必須真的執行 preflight；直接呼叫 wrapper 仍可能繞過文字契約。

這是既有 human authorization/policy boundary 在 live action 前的一次檢查，
不新增 component、store 或 research stage，因此原架構與圖片不變。
