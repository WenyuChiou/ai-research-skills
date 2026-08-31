# Image assets

Image files for the catalog README + social preview.

## Files

| Filename | Used by | Notes |
|---|---|---|
| `pipeline-overview.png` | Top of [`README.md`](../../README.md) | Image 2.0 vertical infographic: 8-stage research pipeline + 17 skills + cross-cutting tools band. See `pipeline-overview-prompt.md` for the content contract. |
| `pipeline-overview.zh-TW.png` | Top of [`README.zh-TW.md`](../../README.zh-TW.md) | Image 2.0 Traditional Chinese mirror of `pipeline-overview.png`. |
| `social-preview.png` | GitHub repo Settings → Social preview | Horizontal 1280×640 hero used when the repo URL is shared on Twitter / Threads / LinkedIn / Slack. Upload manually via repo Settings → General → Social preview (GitHub has no API for this). |
| `harness-architecture*.png` | Main READMEs | Image 2.0 bilingual architecture infographics. |
| `hitl-state-machine*.png` | Main READMEs | Image 2.0 bilingual HITL state-machine infographics. |
| `harness-architecture*.mmd/.svg`, `hitl-state-machine*.mmd/.svg` | Agent/harness builder docs + topology contract | Deterministic node/edge truth used to review the generated PNGs; builder docs retain the editable SVG render. |
| `diagram-sources.sha256` | Diagram CI | Source hashes that force topology review whenever a Mermaid source changes. |
| `image-2-assets.sha256` | Diagram CI | Hashes of the six visually reviewed Image 2.0 PNGs. |
| `image-2-generation.md` | Maintainers | H3 decision scope, prompts, failure evidence, dimensions, hashes, and regeneration checklist. |

## Style guide

- Navy (#0B2742), soft blue/white, and teal accent (#2DA89C). No orange or warning colors.
- Skill names rendered as monospace pill chips so they read as code identifiers.
- Cross-cutting tools shown in a separate band with optional dotted lines back to the stages they support.
- Repo URL in the bottom-right legend.

Image generation is not topology verification. Every regenerated PNG must be
checked against the Mermaid/content contract, reviewed in both locales, and then
recorded in [`image-2-assets.sha256`](image-2-assets.sha256). See
[`image-2-generation.md`](image-2-generation.md) for the current reviewed run.
