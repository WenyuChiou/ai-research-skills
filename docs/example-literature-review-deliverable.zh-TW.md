# 範例 — 文獻回顧交付品

> **合成範例(SYNTHETIC EXAMPLE)。** 以下每一篇論文、作者、識別碼與數字
> 皆為 **虛構**,用以示範 research-hub 文獻回顧交付品的 *外形*。本文件不指涉
> 任何真實出版品。真實執行時,所有引用皆為真實且可解析。 — 不含任何真實
> maintainer 產物(依目錄的 [`## Limitations`](../README.zh-TW.md) 政策)。
>
> 語言:[English](example-literature-review-deliverable.md) | [繁中](example-literature-review-deliverable.zh-TW.md)

這是 research-hub 管線(`search` → `literature-triage-matrix` →
`research-design-helper` → `paper-memory-builder`)的端到端整合輸出 ——
這些 skill 加總起來會得到的那一份文件。

> **範本說明:** 本文件同時是「填好的範例」與「可重用的章節契約」。每個 `>`
> 斜體註記說明該章節必須包含什麼。重用方式:保留章節結構與斜體契約,把
> 合成內容換成你自己的語料。

| 欄位 | 值 |
|---|---|
| 主題 | LLM 是否會在經典認知科學典範上重現人類式的認知偏誤? |
| 範圍 | 錨定 / 框架 / persona 效應;模型規模、提示詳細度與應用領域風險 |
| 語料 | 6 篇論文 —— 僅摘要,非全文(合成) |
| 編製日期 | 2026-01-15(合成日期) |
| 管線 | research-hub:`search` → `literature-triage-matrix` → `research-design-helper` → `paper-memory-builder` |
| 證據等級 | 篩選等級分流 —— **並非系統性回顧** |

---

## 1. 重點摘要(TL;DR)

> *3–6 條:標題級發現、主要分歧、最尖銳的缺口。讀者就算只看到這裡,也該知道
> 下一步該做什麼。*

- **認知偏誤在當前 LLM 中廣泛出現。** 一個 40 模型基準(Banerjee et al.
  2025)報告 12 個偏誤類別中,22–61% 的題目出現偏誤一致回應;錨定偏誤本身
  另有獨立確認(Reyes & Okafor 2024)。
- **緩解是核心分歧。** Reyes & Okafor(2024)發現簡單的提示式修正只把錨定
  降低約 10%;Achebe et al.(2024)報告一種結構化自我稽核提示能移除大部分
  效應。兩者用不同任務與指標,目前無法排序。
- **偏誤已蔓延到應用場景** —— Voss & Hartman(2025)指出認知偏誤可被當作
  LLM 推薦系統的黑箱操弄面利用。
- **最尖銳的缺口 [G1]:** 沒有任何研究以標準化的 *自由作答* 效果量報告錨定
  —— 整個語料只用比率與百分比陳述。
- **語料告誡:** 6 篇論文、僅摘要 —— 這是用來界定研究範圍的初步分流,並非
  已成定論的證據。

---

## 2. 文獻清單

> *每個來源一列。最少欄位:ID、引用、年份、證據類型(實證 / 概念性)、相關度
> 等級加一句理由。*

| ID | 引用 | 年份 | 類型 | 相關度 |
|---|---|---|---|---|
| S1 | Reyes & Okafor — *Anchoring Effects in Instruction-Tuned Language Models* | 2024 | 實證 | **高** —— 錨定的直接證據 + 簡單緩解的負面結果 |
| S2 | Lindqvist et al. — *Cognitive Bias Risk in LLM Decision Support: A Position Paper* | 2024 | 概念性 / 立場文 | **中** —— 風險框架;非實證錨點 |
| S3 | Banerjee et al. — *BiasGrid: A 40-Model Benchmark of Cognitive Bias Prevalence* | 2025 | 實證 + 基準 | **高** —— 語料中範圍最廣的受控評估 |
| S4 | Sato & Pellegrini — *Persona Conditioning and Bias Susceptibility in LLMs* | 2025 | 實證 | **中** —— 新增 persona 調節角度 |
| S5 | Achebe et al. — *Self-Audit Prompting Reduces Anchoring in Generative Models* | 2024 | 實證 + 框架 | **高** —— 提出一種在簡單提示失效處仍有效的緩解 |
| S6 | Voss & Hartman — *Cognitive Bias as an Adversarial Surface in LLM Recommenders* | 2025 | 實證(應用) | **中高** —— 偏誤作為已部署場景中的操弄向量 |

---

## 3. 逐篇摘要

> *每個來源:研究問題 · 方法 · 樣本 · 主要發現(僅在來源有量化時才量化)·
> 作者自承的限制 · 如何使用。摘要沒給的數字絕不杜撰 —— 改寫「摘要未指明」。*

### S1 — Reyes & Okafor 2024 — Anchoring Effects in Instruction-Tuned Language Models
- **問題 / 方法:** 錨定是否出現在指令微調 LLM 中,提示式修正能否移除它?
  以帶錨點的數值估計任務,比較四種提示式緩解策略。
- **樣本:** 8 個指令微調模型;1,800 個估計提示。
- **發現:** 錨定具強健性;四種提示式緩解平均只把效應降低約 10%。
- **限制:** 僅數值估計任務;無自由作答生成。
- **用途:** §「錨定專屬證據」;引用於「簡單去偏失效」。

### S2 — Lindqvist et al. 2024 — Cognitive Bias Risk in LLM Decision Support: A Position Paper
- **問題 / 方法:** LLM 決策支援部署面臨哪些認知偏誤風險?概念性綜述;無量測。
- **樣本:** 無。
- **發現:** 指出五個偏誤家族為部署風險;提出一份緩解研究議程。
- **限制:** 無實證評估 —— 屬議題設定,非證據。
- **用途:** 引言 §「為何重要」;僅作動機。

### S3 — Banerjee et al. 2025 — BiasGrid: A 40-Model Benchmark of Cognitive Bias Prevalence
- **問題 / 方法:** 認知偏誤橫跨眾多 LLM 的盛行率如何,模型規模如何影響?
  多選題基準;12 個偏誤類別;受控提示變化。
- **樣本:** 40 個模型 × 600 題 = 24,000 次評估。
- **發現:** 12 個類別中,22–61% 的題目出現偏誤一致回應;>70B 的模型約在
  三分之一情況降低偏誤;詳細提示對多數偏誤有助益,卻惡化確認框架。
- **限制:** 多選題格式;自由作答行為未受檢驗。
- **用途:** 方法 §「評估框架」;結果 §「盛行率數字」。

### S4 — Sato & Pellegrini 2025 — Persona Conditioning and Bias Susceptibility in LLMs
- **問題 / 方法:** 指派的 persona 是否改變偏誤易感性?跨架構的 persona
  條件化評估。
- **樣本:** 摘要未指明。
- **發現:** 分析型 persona 降低偏誤易感性;「專家」persona 提高過度自信偏誤。
- **限制:**「persona」的操作化定義不透明。
- **用途:** 討論 §「偏誤的調節因子」;關於變異性的對照點。

### S5 — Achebe et al. 2024 — Self-Audit Prompting Reduces Anchoring in Generative Models
- **問題 / 方法:** 結構化的自我稽核提示能否緩解錨定?提出兩階段「自我稽核」
  提示;與基線比較。
- **樣本:** 摘要未指明。
- **發現:** 在受測任務家族上,自我稽核提示移除了大部分錨定效應 —— 而簡單的
  Chain-of-Thought 做不到。
- **限制:** 僅在單一任務家族上測試。
- **用途:** 方法 §「緩解框架」;對 S1 的直接對照點。

### S6 — Voss & Hartman 2025 — Cognitive Bias as an Adversarial Surface in LLM Recommenders
- **問題 / 方法:** 認知偏誤能否被利用來操弄 LLM 推薦系統?以偏誤原則對品項
  描述做黑箱操弄。
- **樣本:** 單一推薦系統設定;多個模型規模。
- **發現:**「社會認同」框架能可靠推高品項的推薦排名;該操弄難以偵測。
- **限制:** 單一推薦系統設定;未評估任何緩解。
- **用途:** §「應用風險 / 偏誤作為攻擊面」。

---

## 4. 跨論文綜合

> *語料一致之處、分歧之處(點名論文)、如何調和。明確標示低證據來源。不要把
> 分歧抹平 —— 要攤出來。*

- **一致 —— 偏誤廣泛存在。** S1 與 S3 各自獨立確認認知偏誤(尤其錨定)橫跨
  眾多模型出現。此現象的 *存在性* 是本語料最站得住的主張。
- **核心分歧 —— 緩解有效嗎?** S1 報告簡單提示式修正只把錨定降低約 10%;
  S5 報告結構化自我稽核提示移除大部分效應。兩者用不同任務與指標,從摘要層級
  無法調和 —— 這本身就是一個缺口([G5])。
- **應用風險** 是浮現的主題 —— S6 把認知偏誤重新框定為可被利用的操弄面,
  而非僅是公平性問題。
- **調節因子** —— S4 補充指派的 persona 會改變易感性,這使任何單一的
  「盛行率」數字都變得複雜。
- **低證據標示:** S2 是無量測的立場文 —— 用作動機,絕不作為證據錨點。

---

## 5. 研究缺口

> *每個缺口 =(a)一句陳述,(b)它「是」缺口的證據 —— 哪些論文沒涵蓋它,
> (c)什麼能補上。缺口以 `[G-n]` 標記。對應到某項計畫研究的缺口,帶上
> `.paper/claims.yml` 的 claim ID。*

| 缺口 | 陳述 | 為何是缺口(證據) | 什麼能補上 |
|---|---|---|---|
| **[G1]** | 沒有標準化的自由作答效果量用於 LLM 錨定。*(→ claims.yml C6,status: gap)* | S1 用數值估計任務;S3 用多選題;兩者皆未報告自由作答效果量。 | 一項報告標準化效果量的自由作答錨定前導研究。 |
| **[G2]** | 錨定效應對錨點合理性的依賴未受檢驗。*(→ claims.yml C5,status: gap)* | 沒有語料論文對錨點合理性分級;全用固定錨點。 | 一項分級錨點的前導研究,檢驗單調的劑量反應。 |
| **[G3]** | 跨論文結果無法比較 —— 每篇研究各用自己的基準。 | S1、S3、S5 各用不同的任務集與指標;沒有共用基準。 | 一個帶共同嚴重度指標的共用公開基準。 |
| **[G4]** | 多選題 → 自由作答的可推廣性未受驗證。 | S3 的盛行率數字全是多選題;開放式行為未受檢驗。 | 對基準子集做一次自由作答的重製。 |
| **[G5]** | 偏誤緩解的效力沒有正面對決評估。 | S1(簡單提示失效)與 S5(自我稽核有效)在各自不同設定下無法相互比較。 | 在單一基準上對緩解方法做受控的對決比較。 |
| **[G6]** | persona / 調節效應建立在不透明的操作化上。 | 只有 S4 做 persona 條件化,且其「persona」定義未指明。 | 對 S4 做全文閱讀 + 一次獨立的 persona 條件化重製。 |

---

## 6. 開放問題

> *語料無法回答、且會影響上述缺口排序的未解問題。與缺口不同:缺口可由一項
> 明確研究補上;開放問題可能需要判斷或更多閱讀。*

- **Q1:** S1 的估計任務與 S3 的 600 題基準題之間是否有任何共用情境?若無,
  兩者表面上對盛行率的一致,可能只是兩個不重疊樣本因建構方式而相符。
- **Q2:** 前導研究應對 S3 的完整範圍(22–61%)還是其高端做檢定力設計?
  此選擇改變所需樣本數;檢定力分析仍待完成。

---

## 7. 建議下一步

> *缺口分析所指向、單一最高槓桿的研究,陳述到足以開工的程度。一段 + 一行
> 範圍說明。*

缺口分析最直接指向 **[G1] + [G5]**:執行一項同時作為緩解對決比較的自由作答
錨定前導研究。在單一釘選的模型快照上,於同一個自由作答任務上比較控制提示、
簡單 Chain-of-Thought 修正(S1 那一類)、以及自我稽核提示(S5 的方法)——
例如每個條件 200 個提示 × 3 個錨點層級。為每種緩解報告錨定條件間的標準化
效果量,使 S1↔S5 的分歧在共同指標上得到解決。納入一個無錨對照以排除訓練
資料先驗。完整設計、混淆因子與風險登記:`.research/design_brief.md`。

*範圍說明:* 一週原型;單一模型快照;單一任務家族;persona 調節因子([G6])
與共用基準工作([G3])排除在原型之外。

---

## 8. References

> *完整、可解析的參考文獻 —— 至少 arXiv ID / DOI + URL,依 ID 排序。真實
> 交付品中這些識別碼為真實且可解析;以下的佔位識別碼標示本文為合成範例。
> (依學術慣例,本節維持原文,不翻譯。)*

- **[S1]** Reyes, A., & Okafor, N. (2024). *Anchoring Effects in
  Instruction-Tuned Language Models.* arXiv:XXXX.XXXXX (synthetic).
- **[S2]** Lindqvist, M., Park, J., & Mensah, K. (2024). *Cognitive Bias
  Risk in LLM Decision Support: A Position Paper.* arXiv:XXXX.XXXXX (synthetic).
- **[S3]** Banerjee, R., Cho, S., & Whitfield, T. (2025). *BiasGrid: A
  40-Model Benchmark of Cognitive Bias Prevalence.* arXiv:XXXX.XXXXX (synthetic).
- **[S4]** Sato, Y., & Pellegrini, L. (2025). *Persona Conditioning and Bias
  Susceptibility in LLMs.* arXiv:XXXX.XXXXX (synthetic).
- **[S5]** Achebe, C., Romano, D., & Idris, F. (2024). *Self-Audit Prompting
  Reduces Anchoring in Generative Models.* arXiv:XXXX.XXXXX (synthetic).
- **[S6]** Voss, E., & Hartman, G. (2025). *Cognitive Bias as an Adversarial
  Surface in LLM Recommenders.* arXiv:XXXX.XXXXX (synthetic).

---

## 9. 來源與限制

> *本交付品如何產出 + 誠實的告誡。沒有這一節的文獻回顧交付品不可信 ——
> 每位讀者都需要先知道證據等級,才能據以行動。*

- **本文是合成範例。** 全部六篇論文、其作者、其識別碼與每一個數字皆為虛構,
  用以示範 research-hub 文獻回顧交付品的 *結構*。皆不指涉真實出版品。真實
  執行會以真實、可解析的來源產出同樣的外形。
- **產出者:** research-hub skill 管線 —— `search`(語料探索)→
  `literature-triage-matrix`(§2–§4)→ `research-design-helper`(§5–§7)
  → `paper-memory-builder`(`.paper/claims.yml` 串接)。真實交付品會一併
  保存原始搜尋輸出。
- **語料限制:** 真實執行中,除非取得全文,語料僅讀摘要;量化發現由摘要
  轉錄,摘要未提之處一律寫「摘要未指明」。
- **並非系統性回顧:** 這是篩選等級的分流,並非帶正式納入 / 排除準則的可重製
  資料庫查詢。召回率未知 —— 可能有相關研究遺漏。
- **claim 狀態串接:** `.paper/claims.yml` 中的 claim 帶有 `status` 欄位;
  `status: gap` 的 claim(此處為 C5 與 C6)其 `evidence_artifacts` 為空,
  並對映到研究缺口(分別為 [G2] 與 [G1])。
- **如何升級真實交付品:** 以不同查詢措辭重跑 `search` 並合併;對高相關度
  論文做全文閱讀;執行 Q2 標示的檢定力分析。
