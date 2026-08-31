# Image assets

Image files for the catalog README + social preview.

## Files

| Filename | Used by | Notes |
|---|---|---|
| `pipeline-overview.png` | Top of [`README.md`](../../README.md) | Vertical infographic, 1024×1500, 8-stage research pipeline + 17 skills + cross-cutting tools band. Regenerate via ChatGPT image gen when skill count or stage mapping changes — see `pipeline-overview-prompt.md` in this folder for the canonical prompt. |
| `pipeline-overview.zh-TW.png` | Top of [`README.zh-TW.md`](../../README.zh-TW.md) | Chinese-language mirror of `pipeline-overview.png`. |
| `social-preview.png` | GitHub repo Settings → Social preview | Horizontal 1280×640 hero used when the repo URL is shared on Twitter / Threads / LinkedIn / Slack. Upload manually via repo Settings → General → Social preview (GitHub has no API for this). |
| `harness-architecture*.mmd/.svg/.png` | Agent/harness builder docs | Editable bilingual architecture source plus README-friendly exports. |
| `hitl-state-machine*.mmd/.svg/.png` | Agent/harness builder docs | Editable bilingual state-machine source plus exports. |
| `diagram-sources.sha256` | Diagram CI | Source hashes that force export review whenever a Mermaid source changes. |

## Style guide

- Navy (#0B2742), soft blue/white, and teal accent (#2DA89C). No orange or warning colors.
- Skill names rendered as monospace pill chips so they read as code identifiers.
- Cross-cutting tools shown in a separate band with optional dotted lines back to the stages they support.
- Repo URL in the bottom-right legend.
