# 第二輪 H3 Dogfood 與失敗基準

執行日期：2026-08-31

環境：Windows 10、PowerShell 7.6.4、Python 3.14

範圍：真實唯讀學術探索，加上隔離的本機 workflow recovery

成本：USD 0；未使用付費 API，也未對 Zotero、Obsidian 或 NotebookLM 做 canonical write

這是一份小規模、以 failure mode 為導向的 dogfood 報告，不是通用排名，也不宣稱
統計上的優越性。Phase 0 沒有留下可直接比較的 live runtime 指標，因此缺少的
baseline 一律標記為 **N/A**，不事後推測或補造。

## 決策與安全邊界

H3 已明確核准三個計畫中的任務。真實學術查詢全部唯讀；中斷情境使用隔離的
`.research` 目錄與明確宣告的 no-write action。NotebookLM 認證已過期，因此
live check 標記為 **degraded/SKIP**，不是 PASS；沒有嘗試外部 mutation。

## 三個真實任務

| 任務 | 精確操作 | 結果 | 時間 |
|---|---|---|---:|
| Scoped discovery | `research-hub search "human-in-the-loop AI agents scientific research evidence verification" --limit 8 --field cs --rank-by smart --verify --json` | 8 筆結果；Semantic Scholar 回傳 HTTP 429，執行降級至其他 backend；一筆跨 backend DOI/arXiv 重複資料揭露真實缺陷 | 12.82 秒 |
| Contradictory evidence | 搜尋 `large language models simulate human survey responses validity bias`，驗證三個 identifier，再進行 no-tool packet synthesis | 3/3 source identity 驗證成功；3 個 supported claim；保留 1 個 contradiction 與 1 個 evidence gap；接受的 unsupported claim 為 0 | 18.15 秒 |
| Interrupted workflow | 初始化隔離 workflow，在已宣告的 no-write action 後注入中斷，執行 resume、reconcile、再次 resume，再重試同一 action | 未知結果以 `reconcile_required` 阻擋；明確 reconciliation 後成功 resume；duplicate retry 被拒絕 | 2.65 秒 |

第一次中斷流程使用了操作端誤填的 state filename，因此明確失敗。修正後使用 CLI
實際契約 `.research/workflow_state.yml`。這個 operator error 被保留為證據，沒有從
結果中隱藏。

## 前後比較

| 可觀察項目 | Phase 0 baseline | Round 1 + H3 觀察 |
|---|---:|---:|
| research-hub offline suite | 3,321 passed；3 failed；23 skipped；11 deselected；2 xfailed | 3,348 passed；0 failed；23 skipped；11 deselected；2 xfailed |
| 真實 source identity 驗證 | N/A | 3/3 |
| 接受的真實 unsupported claim | N/A | 0/3 |
| 保留的 contradiction | N/A | 觀察到的 1/1 contradiction |
| 修正後成功 resume 的 interruption scenario | 尚無 executable workflow runtime | 1/1 |
| 被拒絕的 duplicate no-write retry | 尚無 workflow-wide action ledger | 1/1 |
| Replay failure invariant | 尚無統一 corpus | 12/12 PASS |
| Targeted timeout/recovery tests | N/A | 4 passed；1 deselected |
| 付費 provider 成本 | N/A | USD 0 |

Live sample 刻意保持小規模。這些數量只描述本次執行，是 regression anchor，不是
整個領域的 accuracy 估計。

## Failure injection 與誠實降級

Recorded replay corpus 的 12/12 invariant 全部通過：DOI conflict、unsupported
citation、相互矛盾的 papers、provider unavailable、prompt injection、human decline、
human revise、cancel/resume、external write 後 crash、duplicate retry、policy exhaustion，
以及 NotebookLM unsupported claim。

真實執行觀察到的失敗：

- Semantic Scholar 兩次搜尋都收到 HTTP 429。其他 backend 繼續工作，該 provider
  仍被清楚標記為 degraded。
- NotebookLM authentication 已過期。Live provider check 為 SKIP；只有 recorded
  offline invariant 通過。
- 跨 backend identity reconciliation 在 arXiv backend 只提供 arXiv ID，而另一個
  backend 同時提供 DOI 與 arXiv ID 時，把同一篇 paper 視為兩筆資料。

## 由證據驅動的修整

Production behavior 只針對實際揭露的 identity 缺陷修改。research-hub refinement
會 transitive merge DOI 與 arXiv alias，同時保留 first-backend 的 title/abstract
precedence 及合併後的 provenance。Targeted tests 為 22 passed、1 deselected；完整
local suite 為 3,348 passed。詳見 [research-hub PR 130](https://github.com/WenyuChiou/research-hub/pull/130)。

沒有因為抽象層「看起來更完整」而加入新的 orchestration abstraction。Provider 429
與 NotebookLM authentication 過期仍是明確的 operational condition，不會被轉換成
假的成功。

## 重現與驗收

Offline replay：

```text
python scripts/run_harness_replay.py
# 12/12 PASS
```

Research-hub refinement commit 的驗證：

```text
python -m pytest tests/test_search_confidence.py -q
# 22 passed, 1 deselected

python -m pytest -q
# 3348 passed, 23 skipped, 11 deselected, 2 xfailed
```

驗收仍要求 public PR CI 全綠。Live provider outage 可以產生 degraded/SKIP 證據，
但不能被回報為 PASS。
