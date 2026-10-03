# 系統評估與分階段整合

於 **2026-10-03** 核對以下公開 source revisions。這是 AI-for-science
生命週期評估，不是自主系統完成研究的證據。Catalog 維持 registry/routing layer；
production contracts 由各 source repositories 負責。

English: [system-assessment.md](system-assessment.md)

## 版本與依賴矩陣

| Source | 核對 commit | 已接受 package / plugin | 契約與驗證邊界 |
|---|---|---|---|
| ai-research-skills | [eee76f8](https://github.com/WenyuChiou/ai-research-skills/tree/eee76f87c3f4fbfe3cf6dcab865a657295985e01) | Catalog 1.7.2 / schema 4 | 17 skills、5 source plugins；legacy-v3 view 排除 optional harness；directory 與 marketplace URL/ref 必須解析同一 SKILL.md |
| research-hub | [7e04638](https://github.com/WenyuChiou/research-hub/tree/7e046383368d85acb8dfbf0d734ecaaae335cf0a) | Python/MCP 1.2.0 / research-workspace plugin 0.5.4 | 12 skills；native input/provenance/preview；選配 source-audit 與 offline direction-review 契約；explicit human topic choice；strict packet v1 不變；須檢查 installed runtime |
| academic-writing-skills | [c28f0de](https://github.com/WenyuChiou/academic-writing-skills/tree/c28f0dedb312e9c99c0e8e15c37464f542471b43) | Plugin 1.2.0 | Scope-aware writing/review、design adapters、manuscript state、exact-candidate gate、跨檔影響與 release blockers；不為了聲稱整合而重寫 |
| zotero-skills | [1668aeb](https://github.com/WenyuChiou/zotero-skills/tree/1668aeb49c77d8e88c4132f7306b17ad69bb8206) | Plugin 0.3.0；核對到的最新 tag 0.2.0 | 內層 skill 搭配 root client；不輸出憑證值的 credentials_status 指引、修正 client/API 名稱；runtime 與 destructive safeguards 不變 |
| codex-delegate | [30f6d4a](https://github.com/WenyuChiou/codex-delegate/tree/30f6d4ae63935f5b71bd38d4d13466fcff5f33d8) | Plugin 0.1.1 | 內附 Bash/PowerShell wrappers；穩定 brief/result/sentinel adapter；dirty-content observation 與 sandbox forwarding；由 supervisor 驗收，不另造 broker |
| antigravity-delegate | [c3afa59](https://github.com/WenyuChiou/antigravity-delegate/tree/c3afa59263ea02e40df99097ba5a9c4452e887a8) | Claude plugin 0.1.1 | Bounded mechanical lane；大量輸出達 log 上限後仍等待 producer 完成；Google-native marker 與 Claude manifest 分開；live native-host loading 未驗證 |

機器可讀的公開 source snapshot：
[upstream-contracts.json](../test-corpus/integration/upstream-contracts.json)。
Catalog 列記錄已接受 baseline；其他 source 列已納入審查通過的 merge。
Source accepted 不等於 Python wheel 已發布。
已接受 source 與 proposed changes 分開記錄。不能因 preview branch 的 local tests
通過就當成 stable marketplace；未合併的 research-workspace 提案不是已接受執行契約。

Optional governance dependency 維持 `agent-collab-harness` 0.4.0/v1。
目前官方 release 為
[0.5.1](https://github.com/WenyuChiou/agent-collab-skills/releases/tag/v0.5.1)，
其文件保留 v1 interface 相容性。兩版官方 wheels 的 bytes 均符合 published hash，
並各通過已執行的 22 個 legacy hub workflow-runtime 檢查。
[Builder guide](for-agent-harness-builders.zh-TW.md) 保留 normal registry option，
另提供 checksum-bound 0.4.0 release fallback；此處的 registry failure 屬環境相依。
不進行 v2 migration 或建立新的 trust root。

已接受的 [agent-collab source 4aa56e4](https://github.com/WenyuChiou/agent-collab-skills/tree/4aa56e47011b15a416f128b5a1c395baae8d0581)
補上 task/run/baseline/current-candidate 證據審查，mtime 只作提醒。
Preset 是 declarative review contract，不是 Python runtime preset engine；
這次 source 文件修改不會更動兩版已發布 wheel。

Research-workspace 0.5.4 的已接受 source 保留選配 source-audit profile，
Python package 版本仍是 1.2.0。Plugin 更新不會替換已安裝的 wheel。
先檢查 `validate_evidence_packet` 的 `source_audit`、`artifact_root` kwargs，
以及 packaged `research-source-audit-1.0.json`，做法見
[installed-runtime 指引](https://github.com/WenyuChiou/research-hub/blob/7e046383368d85acb8dfbf0d734ecaaae335cf0a/skills/research-hub/references/source-claim-audit.md#optional-executable-source-audit-profile)。
若不支援，mechanical audit 維持 unavailable，保留 manual/native source review。
不得呼叫不存在的 kwargs，也不能把 packet-only validity 說成 source audit。
不能只憑未變更的版本字串推定新能力已存在。

已接受的 [direction-review 契約](https://github.com/WenyuChiou/research-hub/blob/7e046383368d85acb8dfbf0d734ecaaae335cf0a/docs/direction-review-contract.md)
新增選配 offline `paper direction-check`，檢查呼叫者提供的 records：

- 以 `candidate_version`、`candidate_sha256` 綁定完整 candidate，evidence 綁定
  實際 source bytes。保留 material-level provenance；local note 不等於原始全文。
  Publication version 只是記錄，未驗證真偽；explicit unknown 仍是 unknown。
  Candidate content/version 或 source bytes 改變後須重查，並保留舊 record
- 涵蓋 data/tool/model/license/cost/premise/validation-path，明列
  supported/contradicted/unknown/not-applicable。Unknown 須附 bounded next check；
  理論研究可保留有理由的 not-applicable
- 在明列的 candidate scope 中加總 resource components；共用工作需 explicit
  `sharing_basis`。不換算單位，缺 required units、demand 或 capacity 維持 unknown。
  Stale binding 使當前 resource 結論失效；保留的算術結果僅供診斷
- `semantic_assessment: not-performed`、`runtime_budget_verification: not-performed`、
  `human_selection: outside-checker`、`execution_authorized: false`。Exit 0 仍可有
  unknown、contradiction 或超出預算的 estimates，不是研究核准。Checker 不讀取 Hub
  configuration、不呼叫 model/network、不寫檔，也不啟動下一階段

沒有 optional review 仍可使用原 dossier 與 standalone design dialogue。
只有一個 eligible candidate 也不代表可自動 pre-fill design brief：沿用明確的
prior human selection，否則先問。保留 human edits，替換 provenance 前先詢問。
Guidance 現在記錄 prospective outcomes/time boundaries、two-occasion 與 vignette
的 claim limits、適用時的 matched-information comparison、minimum worthwhile gain、
smallest answerable version 及 nonclaims；固定一週 prototype 不能證明可行性。
這是 source contract 同步，並非新的品質結果：一組 guidance comparison pair
結果未定，historical T1 dates/tiers 不變，不宣稱整體科學研究能力提升。
Plugin 0.5.4 不證明已安裝 Python wheel 支援此 command；使用前檢查實際 CLI
capability，若不存在就保留原本的 ordinary/manual 路徑。

## 生命週期涵蓋與科學缺口

原圖八階段已涵蓋文獻、gap/選題、設計、計畫、執行、解讀、writing/review、投稿準備。
[科學生命週期與品質關卡](scientific-lifecycle.zh-TW.md) 補清輸入、輸出、證據限制與人的決策。

既有強項包括文獻庫/workspace 操作、native discovery handoff、source/audit receipts、
topic/design dossiers、可續接 state/gates 與 writing/review 證據鏈。仍需守住：

- 搜尋清單不證明資訊需求已涵蓋；corpus 漏掉文獻不證明有開放或重要 gap
- 低成本 screening 有價值，但記憶中的名作結果、DOI、abstract、generated brief
  不能升級為 full-text-supported central claim
- Bytes/quote/version checks 可拒絕機械性不一致；科學支持、新穎性、重要性與可行性
  仍需研究者根據可檢視證據判斷
- Manifest 保存 state，不是跨領域建模器、統計方法選擇器、驗證引擎或實驗 runner
- Delegate 可寫繪圖/scaffolding；解讀與誠實性留給 primary。投稿準備不等於投稿授權

## 最小分批修改與依賴

1. **Catalog hygiene 與 resolver acceptance。** 修正 15 個 repo-relative directories、
   依已接受 manifest 同步 marketplace version、替換錯誤的整個 repo→單一 skill 安裝指令、
   將 Zotero shadowing 標為歷史。Deterministic CI 檢查 path/ref；可用唯讀 checker
   檢查五個真實 source clones。Installer dry-run 可重跑；錯誤 scope/arguments 與
   native failure 在後續指令前停止
2. **Upstream plugin 相容性。** 修正 Codex installed-skill wrapper packaging/brief
   resolution；檢查 Antigravity 大量輸出完成性與版本相依 CLI 敘述。Native marker
   需官方 schema 與 offline checks；修改留在 respective source PRs，native-host
   execution 另列未驗證
3. **Shared research 證據紀律。** 在 research-hub 連結資訊需求與實際執行 native
   search，強化 source-level、work/version、claim binding、bounded completion。
   重用既有 audit/source-fetch/native-input；optional evidence profile 必須 versioned，
   與 strict packet v1 並存，不能偷偷插入額外 properties。不搬 AutoResearch
   ledger/operator 或 paid evaluation framework
4. **已接受整合。** 真實 producer/consumer fixtures 與 legacy contracts、最終 diff
   review、完整 required suites 後才開 draft PR。上述 accepted source commits
   支持同步的 plugin versions 與 snapshot；未合併 preview 仍不能取代它們。
   Merge、release、deploy、本機安裝、科學投稿、私有 upload
   各自保留授權

## 同條件比較與限制

第一次 live model-backed 測試前，先用
[preflight 契約](live-run-preflight.zh-TW.md) 確認實際 host/provider/model、
subscription 或 API 模式、已批准 budget、data destination/scope。
沿用有效 explicit choices；缺重要資料或設定有重要變更，先詢問再呼叫 model。
Fixtures 只規定 supervisor 行為，不代表 runtime 已強制執行。

Catalog regression 使用同一 17-skill 公開 snapshot 與 installer invocations。
修改前七個 install-contract cases 失敗：directory、nested-repo install guidance、
無 dry-run、四種無效 argument；修改後通過。額外 tests 拒絕 traversal/ref drift/
缺 producer，保留 native failure。這證明 resolver/script 行為，不證明文獻研究更好。

Source 行為檢查要執行 actual validator、wrapper、receipt 或 native ingest preview。
保留 legacy packet、provenance、idempotent preview/replay、unknown/partial、version
mismatch、provider unavailable、fabricated quote。Structural checks、production
boundary、live host loading、research-quality evaluation 分開報告。

一般 Claude Code 整合，在 runtime 適用時優先使用
[官方 codex-plugin-cc](https://github.com/openai/codex-plugin-cc/tree/db52e28f4d9ded852ab3942cea316258ae4ef346)。
Codex-delegate 保留給既有 synchronous brief、sidecar/sentinel 與
Bash/PowerShell adapter 契約，不另造 broker。
在只有 `commandExecution`、沒有 `fileChange` 的同條件 protocol fixture 中，
官方 event-derived touched-file list 為空，wrapper 的 Git observation 記錄實際修改。
三種 adapter 都產生相同的正確 artifact。這是有條件的 observation coverage，
不代表真實 shell edits 一律不發事件，也不證明 coding quality 或 total model cost 較好。
兩條路徑都不會單靠 brief 自動強制 scope。

已檢查 Codex CLI help/version、Linux 上實際 PowerShell Core 7.6.6；
新 head 的 hosted Windows/Linux process fixtures 已通過。
Claude、Antigravity executables 不存在，marketplace/native-host loading 未驗證。
尚無成功的 matched live model quality/cost A/B。Synthetic delegate 只測 transport，
不證明實際 host interoperability 或 sandbox enforcement。
Source-layout audit 不更新 historical verification dates/tiers；不宣稱科學研究效能提升。

## 架構與圖像決策

已檢視 EN/繁中 pipeline、architecture、HITL PNG pixels，並對照 canonical
prompt/Mermaid source 與 hash manifests。修改強化既有 contract/validator boundary，
不改 stages、roles、stores、nodes、edges，因此保留原設計與已審圖片。
文字 cross-cutting table 補上原圖已有的 orchestrator；後續若 topology 改變，
必須更新 canonical source，按原設計重繪全部 reviewed exports，不另造無關圖像。
