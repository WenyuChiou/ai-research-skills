# Test Corpus: AI Agents and Social Interaction

This is a **reproducible test corpus** used by `docs/verification.md` to
exercise the catalogued skills end-to-end (literature-triage-matrix,
paper-memory-builder, notebooklm-brief-verifier, etc.).

The 5 papers below were retrieved on **2026-04-25** from `research-hub
search "AI agents social interaction" --limit 8 --rank-by smart`
(Semantic Scholar / arXiv / OpenAlex backends). Five were selected to
provide method × paper-type × domain spread:

- **Method**: empirical experiments (#1, #2, #3) vs. frameworks (#4, #5).
- **Paper type**: study (#1–3), tooling paper (#4), conceptual framework (#5).
- **Domain**: VR/health, poker/ToM, education, HCI experimentation
  infrastructure, livestreaming alignment.

A "good" triage matrix should at minimum surface this method × type ×
domain split — that's the falsifiable claim under test.

## Papers

| # | Slug | Title | Year | Venue / source |
|---|---|---|---|---|
| 1 | `01-lim-2025-vr-embodied-agents.md` | Artificial social influence via human-embodied AI agent interaction in VR | 2025 | Computers in Human Behavior: Artificial Humans (DOI 10.1016/j.chbah.2025.100172) |
| 2 | `02-lin-hou-2026-llm-poker-tom.md` | Readable Minds: Emergent Theory-of-Mind-Like Behavior in LLM Poker Agents | 2026 | arXiv 2604.04157 |
| 3 | `03-kumar-2026-multiagent-llm-learning.md` | Beyond the AI Tutor: Social Learning with LLM Agents | 2026 | arXiv 2604.02677 |
| 4 | `04-mcdonald-2026-cogrid-mug.md` | CoGrid & the Multi-User Gymnasium: A Framework for Multi-Agent Experimentation | 2026 | arXiv 2604.15044 |
| 5 | `05-wang-2026-triadic-loop-livestreaming.md` | The Triadic Loop: A Framework for Negotiating Alignment in AI Co-hosted Livestreaming | 2026 | arXiv 2604.18850 |

## Provenance

The raw search results are preserved in `search-results.json` (re-runnable
via the same command above; results may drift as new papers index).
