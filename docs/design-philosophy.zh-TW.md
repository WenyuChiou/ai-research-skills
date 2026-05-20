# 設計哲學

這份文件是 `ai-research-skills` 的設計契約——這個 catalog 承諾要做
什麼、刻意不做什麼。

Catalog 是一份 [Claude Code](https://claude.ai/code) plugin 的 curated
索引,專注研究工作流。每個 plugin 的程式碼住在各自的 source repo;
這個 repo 是 registry + 文件。

語言:[English](design-philosophy.md) | [繁中](design-philosophy.zh-TW.md)

---

## Catalog 是什麼

5 個 plugin、安裝完對應到 `~/.claude/skills/` 底下 14 個 SKILL.md:

| Plugin | Source repo | 內容 |
|---|---|---|
| `research-workspace` | [`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub) | 10 個 research-hub skill(文獻 triage、專案記憶、NotebookLM brief 驗證、論文整理…) |
| `academic-writing-skills` | [`WenyuChiou/academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills) | 論文修改、banned-word audit、claim-evidence check、journal format、reviewer response |
| `zotero-skills` | [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | 完整 Zotero CRUD(local + Web API) |
| `codex-delegate` | [`WenyuChiou/codex-delegate`](https://github.com/WenyuChiou/codex-delegate) | Claude → Codex CLI:把程式重的工作交給 Codex |
| `gemini-delegate` | [`WenyuChiou/gemini-delegate-skill`](https://github.com/WenyuChiou/gemini-delegate-skill) | Claude → Gemini CLI:長 context / CJK 交給 Gemini |

---

## 設計選擇

1. **Curated、不是 auto-discover。** Catalog 裡每個 plugin 都是針對
   具體研究情境手挑的,maintainer 在進行中的研究專案實際在用。
2. **沒有 pipeline orchestrator。** Skill 由研究者個別呼叫,catalog
   不會把它們鏈成 stage-1 → stage-2 的 pipeline。要編排請看
   [`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills)。
3. **有觀點的子集、不是窮舉。** 5 個 plugin、14 個 skill 是按
   maintainer 在真實研究裡踩到的洞挑的,而不是把學術人會用到的東西
   都收進來。
4. **雙語入口。** README、install、verification、pipeline、
   skill-directory、這份設計文件,全都英中雙語。每個 skill 內部的
   reference 檔依慣例只有英文。
5. **誠實 scope。** README 有 Limitations 區塊;每個 plugin 的 source
   repo 也各自有。整份 catalog 由一位研究生組裝、驗證;沒做過 corpus
   規模驗證;maintainer 的領域偏向(水資源、agent-based modeling)
   明寫出來、不粉飾。

---

## Catalog 用機器檢查的部分

CI 在每次 push、每個 PR 對 `main` 跑。它執行 `python -m pytest tests/ -q`、
`python scripts/check_marketplace_consistency.py`、
`python scripts/check_catalog_schema.py`,合在一起守住:

- `catalog/skills.yml` — 每個欄位形狀對著
  [`schema/skills.schema.json`](../schema/skills.schema.json)(JSON
  Schema Draft 2020-12)檢查:skill / family / 頂層的必要欄位、URL
  pattern 正則、`verification_status` / `verification_tier` 的 enum
  限制、`verified_on` 跟 `updated` 的 ISO 日期、未知欄位拒收
  (`additionalProperties: false`)。
- `.claude-plugin/marketplace.json` — schema 合法、plugin 順序符合
  預期、每個 plugin 都有 source URL。
- 跨文件一致性 — catalog 裡每個 skill 的 `repo_url` 對得回 plugin
  source URL;`research-workspace` 描述裡的 `<N> research-hub skills`
  數字跟 catalog 實際數量吻合;每個 `skill_url` 都是
  `/blob/<branch>/SKILL.md` 形狀。
- README 內容 — researcher-facing 受眾用語有出現(Zotero、Obsidian、
  NotebookLM 都被點名);persona 表雙語都有;canonical 安裝指令
  (`research-hub setup`)在 README + 安裝文件 + catalog YAML 一致。
- Verification 數字 — 14 個 skill、狀態分佈跟
  [`docs/verification.md`](verification.md) 對齊。

CI 紅燈擋 merge。完整檢查清單在
[`tests/test_catalog.py`](../tests/test_catalog.py)、
[`tests/test_catalog_schema.py`](../tests/test_catalog_schema.py)、
[`scripts/check_marketplace_consistency.py`](../scripts/check_marketplace_consistency.py)、
[`scripts/check_catalog_schema.py`](../scripts/check_catalog_schema.py)。

---

## Catalog **不**用機器檢查的部分

- **SKILL.md 內容品質。** 那是 source repo 的責任。每個 plugin 的
  source repo 都有自己的測試。
- **上游 URL 是否還活著。** 網路測試太 flaky;PR 時人工 review。
- **跨 skill 的 artifact 契約** — 例如 `paper-memory-builder` 寫
  `.paper/claims.yml`、`academic-writing-skills` 讀。兩邊路徑/schema
  要對齊但 catalog 不強制,要靠 [CONTRIBUTING.md](../CONTRIBUTING.md)
  §2 的人工協調規則。
- **真實世界輸入下的行為正確性。** Layer-3 驗證(拿真實 manuscript
  跑每個 skill)是 source repo 的責任,不是 catalog 的。

---

## 從相關專案借來的東西

[`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills)
(「ARS」)是 Claude Code 上學術 skill suite 的成熟、完整參考。借鑒
進這個 catalog 跟它的 plugin 的(shape,不是 scale):

- **Schema-driven 驗證** 在 catalog 層 —
  [`schema/skills.schema.json`](../schema/skills.schema.json)(JSON
  Schema Draft 2020-12)把 `catalog/skills.yml` 的形狀正式化,由
  [`scripts/check_catalog_schema.py`](../scripts/check_catalog_schema.py)
  在 CI 跑,以及
  [`tests/test_catalog_schema.py`](../tests/test_catalog_schema.py)
  每個 PR 跑。
- **誠實 provenance** — 對其他專案的任何比較(這份文件、plugin
  README、CHANGELOG 條目)都附上可驗證的 link。
- **每個 skill 的 `Limitations` 區塊** — 慣例是每個 source repo 的
  `README` 各自一份,加上 catalog 層級這一份。

刻意**不**借的:

- Pipeline orchestrator 各階段 — catalog 是 registry、不是 runner。
- Opt-in feature flag(例如 `<PROJECT>_*` env var)。要 ship 的檢查
  就 default-on。
- 宣告但不執行的 annotation。

要 pipeline 編排加完整覆蓋,ARS 是對的選擇。要一個 curated 子集、
一次裝一個 plugin 進 Claude Code,這份 catalog 是。

---

## Roadmap

Catalog 還有未完工項目跟坦承的 gap。看 open issues + PR 進度。下面
這些目前**沒有**任何版本承諾要做:

- Cross-model 獨立 judge(讓 Codex / Gemini 對 skill 行為 eval 給第
  二意見)。
- 任何 plugin 的 corpus-scale FNR/FPR 校準。
- maintainer 領域(水資源、agent-based modeling)以外的泛化驗證。
- 內部 reference 檔的翻譯(依慣例只有 top-level 文件雙語)。

---

這份文件是 catalog 的設計契約。如果你發現實際行為跟上面任何一句
不符,請開 issue。
