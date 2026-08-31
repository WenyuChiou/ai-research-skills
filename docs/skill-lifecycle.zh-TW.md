# Skill lifecycle

Active skill 必須可被支援的 host 發現、具備完整 `SKILL.md`、所有必要
CLI/MCP/tool dependency 都存在、至少一條 happy path 可執行、failure path 可理解、
不依賴 archived-only provider、不做 silent mutation，並保留近期 behavior evidence。

`experimental` 表示契約或證據未完成；`deprecated` 表示停止新 routing，且已有替代
方案與 migration path；`retired` 表示從 active catalog、marketplace、install 與
routing surface 移除，但清楚標記的歷史證據仍保留。

`gemini-delegate` 因來源 repo 已 archived，且 baseline wrapper suite 為 2 pass / 6
fail，所以正式 retired。支援的 bounded mechanical leaves 是 `codex-delegate` 與
`antigravity-delegate`；繁中、研究判斷、governance 與 final review 留在 primary
agent。`docs/verification*.md` 內的 Gemini 結果是歷史證據，不代表目前支援。
