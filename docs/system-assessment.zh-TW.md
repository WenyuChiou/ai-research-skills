# 系統評估與分階段整合

於 **2026-10-02** 核對以下公開 source revisions。這是 AI-for-science
生命週期評估，不是自主系統完成研究的證據。Catalog 維持 registry/routing layer；
production contracts 由各 source repositories 負責。

English: [system-assessment.md](system-assessment.md)

## 版本與依賴矩陣

| Source | 核對 commit | 已接受 package / plugin | 契約與驗證邊界 |
|---|---|---|---|
| ai-research-skills | [eee76f8](https://github.com/WenyuChiou/ai-research-skills/tree/eee76f87c3f4fbfe3cf6dcab865a657295985e01) | Catalog 1.7.2 / schema 4 | 17 skills、5 source plugins；legacy-v3 view 排除 optional harness；directory 與 marketplace URL/ref 必須解析同一 SKILL.md |
| research-hub | [a643ace](https://github.com/WenyuChiou/research-hub/tree/a643aceefc52cbf690264a3801e597d787ebd714) | Python/MCP 1.2.0 / research-workspace plugin 0.5.1 | 12 skills；native papers input、provenance/source_records、preview/idempotence；search audit/source fetch；strict ResearchEvidencePacket v1；workflow state/human gates |
| academic-writing-skills | [c28f0de](https://github.com/WenyuChiou/academic-writing-skills/tree/c28f0dedb312e9c99c0e8e15c37464f542471b43) | Plugin 1.2.0 | Scope-aware writing/review、design adapters、manuscript state、exact-candidate gate、跨檔影響與 release blockers；不為了聲稱整合而重寫 |
| zotero-skills | [5b21974](https://github.com/WenyuChiou/zotero-skills/tree/5b219747358a16e068f54d139e408d00ddd755f0) | Plugin 0.3.0；核對到的最新 tag 0.2.0 | 內層 skill 搭配 root client；不輸出憑證值的 credentials_status；CRUD/restore/merge/attach；manifest/changelog 與 release tag 是不同版本軸 |
| codex-delegate | [438f92e](https://github.com/WenyuChiou/codex-delegate/tree/438f92e4cf9b0607b25109cebfc427d27d5e1942) | Plugin 0.1.0 | On-disk brief、wrapper status/result、primary acceptance review；核對 source 時 advertised portable wrapper 路徑不存在 |
| antigravity-delegate | [a9c60d4](https://github.com/WenyuChiou/antigravity-delegate/tree/a9c60d4e40ddc06d0185ad041dcf0fb7bc398744) | Claude plugin 0.1.0 | Bounded mechanical lane、legacy CLI；目前 Google-native plugin 與 Claude marketplace manifest 是不同表面 |

機器可讀的公開 source snapshot：
[upstream-contracts.json](../test-corpus/integration/upstream-contracts.json)。
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
   同步已接受 research-workspace 0.5.1、替換錯誤的整個 repo→單一 skill 安裝指令、
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
   review、完整 required suites 後才開 draft PR。Upstream accepted 後，後續 catalog
   才能宣告新版本 stable。Merge、release、deploy、本機安裝、科學投稿、私有 upload
   各自保留授權

## 同條件比較與限制

Catalog regression 使用同一 17-skill 公開 snapshot 與 installer invocations。
修改前七個 install-contract cases 失敗：directory、nested-repo install guidance、
無 dry-run、四種無效 argument；修改後通過。額外 tests 拒絕 traversal/ref drift/
缺 producer，保留 native failure。這證明 resolver/script 行為，不證明文獻研究更好。

Source 行為檢查要執行 actual validator、wrapper、receipt 或 native ingest preview。
保留 legacy packet、provenance、idempotent preview/replay、unknown/partial、version
mismatch、provider unavailable、fabricated quote。Structural checks、production
boundary、live host loading、research-quality evaluation 分開報告。

本次雲端可檢查 Codex CLI help/version，未送 live paid model request。
Claude、Antigravity executables 不存在，實際 marketplace/native-host loading
未驗證。已找到既有 PowerShell Core 7.6.6 並在 Linux 執行檢查；native Windows
行為仍未驗證。Synthetic CLI doubles 只測 wrapper，
不能證明實際 host interoperability。Source-layout audit 不更新 historical
verification dates/tiers；不宣稱科學研究效能提升。

## 架構與圖像決策

已檢視 EN/繁中 pipeline、architecture、HITL PNG pixels，並對照 canonical
prompt/Mermaid source 與 hash manifests。修改強化既有 contract/validator boundary，
不改 stages、roles、stores、nodes、edges，因此保留原設計與已審圖片。
文字 cross-cutting table 補上原圖已有的 orchestrator；後續若 topology 改變，
必須更新 canonical source，按原設計重繪全部 reviewed exports，不另造無關圖像。
