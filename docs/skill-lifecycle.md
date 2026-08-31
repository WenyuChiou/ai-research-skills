# Skill lifecycle

Active skills must be discoverable by a supported host, have a complete
`SKILL.md`, resolve every required CLI/MCP/tool dependency, execute one happy
path, expose an understandable failure path, avoid archived-only providers and
silent mutation, and retain recent behavior evidence.

`experimental` means the contract or evidence is incomplete. `deprecated` means
new routing stops and a replacement plus migration path exists. `retired` means
the skill is absent from active catalog/marketplace/install/routing surfaces;
historical evidence stays clearly labeled.

`gemini-delegate` was retired because its source repository is archived and its
baseline wrapper suite failed 6 of 8 tests. The supported bounded mechanical
leaves are `codex-delegate` and `antigravity-delegate`; CJK, research judgment,
governance, and final review remain with the primary agent. Historical Gemini
results in `docs/verification*.md` are archival evidence, not current support.
