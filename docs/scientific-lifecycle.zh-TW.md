# 科學研究生命週期與品質關卡

[Pipeline](pipeline.zh-TW.md) 維持既有八階段、研究者主導的設計。
本文件補足跨階段必須攜帶的證據。Skill、合法檔案、指令成功或 CI 綠燈，
都不能認證科學主張。檢查深度須符合任務；快速查詢不必變成全專案稽核。
[系統評估](system-assessment.zh-TW.md) 記錄目前涵蓋範圍與驗證限制。

English: [scientific-lifecycle.md](scientific-lifecycle.md)

## 階段輸入、輸出與前進條件

| 原圖階段 | 輸入與既有路由 | 必要交接與品質證據 | 人的決策或停止條件 |
|---|---|---|---|
| 1. 找文獻 | 使用者問題、納入限制、未解資訊需求 → research-hub/native search；Zotero 管理文獻庫 | 需求與查詢對照；實際執行的查詢與日期；work/version 身分；納入/排除原因；來源存取與證據層級；適用時區分 core、closest、classic、contrary | 研究者決定範圍。建議的地區、日期、方法不會變成未宣告的 filter。Timeout、429、paywall、缺少 payload 是未知/失敗，不是零結果證據 |
| 2. 比較與找缺口 | 已辨識的來源 → literature-triage-matrix、NotebookLM verifier、gap-to-topic | Claim–source matrix；重要發現的定位證據；最接近前作比較；反向/相反證據與 dead-end history；分開判斷開放性、貢獻/重要性、可行性；`topic_dossier.gaps.yml` 保留未知 | 研究者/指導者選題。沒找到文獻不能證明新穎性；只有方法可比的研究不能替代主題證據；有可追溯身分的檔案史料不會只因缺 DOI 被否定 |
| 3a. 框問題 | 候選 dossier 與人的答案 → research-design-helper | `design_brief.md`：問題、estimand/預期機制、假設、可識別性、能區分解釋的對照/baseline、驗證與風險；標明未回答與 placeholder segments | 研究者接受問題與預期貢獻。Placeholder 不能作為真研究關卡；不可識別或無法回答的主張回到問題設定 |
| 3b. 寫計畫 | 已接受 brief 與實際資料/資源 → research-context-compressor / research-project-orienter | `project_manifest.yml`、`experiment_matrix.yml`、`data_dictionary.yml`；保留 `provenance.from_gap`；資料取得、適用的倫理/同意、時間/算力/成本、分析與失敗條件；要求或聲稱時才加入 preregistration | 研究者承諾範圍與資源。Manifest 記錄狀態，不會補出缺少的方法或授權實驗 |
| 4. 設計與建模 | 已接受研究意圖與專案方法規格 → 研究者/primary agent；機械性工作可經 multi-AI router | 版本控制的實作、方法假設、資料轉換、方程式/演算法測試、baseline/control fixtures、明確依賴與版本 | 研究者決定重要設計改動。`design_brief.md` 是設計意圖，不是完整實作規格；delegate 回傳後仍須獨立 diff 與 acceptance review |
| 5. 執行、校正、驗證 | 已授權實驗/分析計畫與專案工具；manifest 保存 context | 可重現指令、程式/資料/model hash 或版本、適用的參數/prompt/seed、重複執行設計、失敗紀錄、輸出、敏感度/不確定性、held-out checks，區分 verification 與 empirical validation | 高成本/長時間執行須 experiment authorization。失敗保留；程式測試不能證明實證有效性；缺必要結果不能前進推論 |
| 6. 視覺化與解讀 | 已驗證輸出 → bounded delegates 寫繪圖程式；解讀留給 primary | 圖表 provenance、分母/單位/不確定性/排除規則、效應估計、條件/母群界線；caption 對應實際繪圖資料；報表解釋替代解釋與限制 | 研究者決定科學解讀。未知或未顯著不能暗中改寫成相等、不存在、因果或機制 |
| 7. Outline、撰寫、review、修改 | 設計、分析、來源與圖表 → paper-memory-builder、academic-writing-skills、paper-review | `.paper/claims.yml` / `.paper/figures.yml` 作為宣告的 authority；證據連結的 extended outline；問題→方法→結果→解讀→貢獻對齊；study-design adapters；按證據成熟度 review；修改同步影響的段落與伴隨檔案 | 作者接受科學/語義改動。流暢段落或清楚 outline 不會補足證據；局部修改不代表整篇 review |
| 8. 投稿準備、回審、收尾 | 唯一 active manuscript 與伴隨檔 → academic-writing-skills、paper-review、context capture | Exact-candidate/跨檔檢查、引用/metadata/聲明、提供或核對的期刊要求、supplement/data/code 存取、review-response ledger 與目前檔案核對、blocker/waiver、保留 final state/version | 作者判斷 readiness，另外授權投稿/發表/分享。作者資格、倫理、法律協議、付款、外部 upload 各有關卡；未提供自動期刊投稿 |

## 跨階段科學完整性

- 保留研究者的問題、母群、地區、時間、estimand 與明確 nonclaims；
  區分已接受決策與建議
- 分開驗證身分、來源可得性、quote binding、語義支持。Metadata、abstract、
  generated summary、定位 full text 支持不同主張；hash 只證明 bytes 綁定，
  不證明真實性或科學充分性
- 比較同一 work/version。保留 preprint、修訂、勘誤、撤稿的差別；保留取得紀錄與
  決策反轉；authority 改變時重新檢查相依 claims
- 保留 supported、partial、contradicted、unverifiable。矛盾需攜帶方法、母群與條件；
  尋找 counterevidence 失敗不代表可捏造反對論點
- 記錄 bounded completion：涵蓋需求、執行路徑、已審 claims、存取/身分限制、
  未解缺口與是否繼續；篇數或用完預算不等於完整文獻涵蓋
- 使用適合領域的方法；質性、理論、資料論文不會自動繼承實驗 IMRAD 或 preregistration

## 既有來源分工

- [research-hub](https://github.com/WenyuChiou/research-hub) 負責 discovery、ingest/audit
  receipts、source fetch、strict ResearchEvidencePacket、workflow state、human gates 與
  12 個 workspace skills
- [academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) 負責
  manuscript authority/lifecycle、設計相依 integrity、exact-candidate audits、科學 review、
  revision 與 release readiness
- [zotero-skills](https://github.com/WenyuChiou/zotero-skills) 負責深度 CRUD；文獻庫去重
  不會建立 work/version 的 claim 身分
- Codex 與 Antigravity leaves 做有邊界的機械工作。Native/plugin loading、wrapper 行為、
  科學有效性與投稿授權須分開核對；見 [runtime contract](runtime-contract.zh-TW.md)

## 驗證與架構邊界

這些關卡補清既有契約，不新增 stage、agent、truth store、自主實驗 runner 或期刊投稿服務。
既有 pipeline content contract、Mermaid architecture/state topology 與已審 image assets
維持 authoritative 且不變。若後續改動角色、節點、箭頭或 stage assignment，必須更新
canonical source，按原設計重繪，並重新驗證雙語與 hashes。

文件/fixture 一致性是結構證據；production validators 與 native ingest previews 只提供
各自邊界的行為證據。實際 host-load 或研究品質比較要另報環境、輸入、失敗與未驗證範圍。
