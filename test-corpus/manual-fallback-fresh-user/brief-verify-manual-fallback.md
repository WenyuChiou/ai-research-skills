# NotebookLM brief verification report (Manual fallback mode)

Generated 2026-04-26 by `notebooklm-brief-verifier` v0.68.2, **Manual
fallback mode** — verifier was given a brief file + a source list at
arbitrary paths, with **no `~/knowledge-base/.research_hub/` access**
(simulated fresh user who uploaded directly to notebooklm.google.com).

**Brief**: `test-corpus/manual-fallback-fresh-user/brief.txt`
(305 chars, generated 2026-04-26T00:15:59Z, downloaded manually)
**Source list**: `test-corpus/manual-fallback-fresh-user/sources.md`
(5 papers, plain markdown bullet list — the format SKILL.md mode #2
documents)
**Mode**: Manual fallback (per SKILL.md `## Inputs` section #2,
v0.68.2)

## Bundle inventory (parsed from sources.md)

The verifier parses the markdown bullet list and treats each row as one
`S_bundle` entry:

| # | Citation | DOI / arXiv | First-author surname |
|---|---|---|---|
| 1 | Kumar 2026 | arXiv:2604.02677 | Kumar |
| 2 | Lim 2025 | 10.1016/j.chbah.2025.100172 | Lim |
| 3 | Lin & Hou 2026 | arXiv:2604.04157 | Lin |
| 4 | McDonald 2026 | arXiv:2604.15044 | McDonald |
| 5 | Wang 2026 | arXiv:2604.18850 | Wang |

5 sources parsed cleanly from `sources.md`. **No research-hub paths
were read.**

## Source coverage scan

Same logic as research-hub-managed mode (per SKILL.md: *"The
verification logic is identical in both modes. Only the input-loading
layer differs."*):

| Source | Hits in brief body | Status |
|---|---|---|
| Kumar 2026 | content match (multi-agent LLM, math/SAT problems, essays, idea homogeneity) | **referenced (implicit)** |
| Lim 2025 | 0 hits on Lim / embodied / VR / gender | **MISSED** |
| Lin & Hou 2026 | 0 hits on Lin / Hou / poker / ToM / Theory of Mind | **MISSED** |
| McDonald 2026 | 0 hits on McDonald / CoGrid / Gymnasium / MUG / JAX | **MISSED** |
| Wang 2026 | 0 hits on Wang / Triadic / livestream / alignment | **MISSED** |

**Cited in brief: 1 / 5**. **Missed sources: 4** (Lim 2025, Lin & Hou
2026, McDonald 2026, Wang 2026).

## Unsupported / overgeneralization claims

- Body line: *"多代理人配置雖可能增加認知負荷，卻能提升學習者的自我效
  能感與參與意願"* — cognitive-load + self-efficacy claims not in any of
  the 5 source abstracts as parsed from `sources.md`. **Unsupported
  by the bundle** (or extrapolated beyond the abstract level).
- Brief title 2 promises *"Multi-Agent and Embodied AI"* but the body
  contains no embodiment content. **Title / body mismatch.**

## Cross-source contradictions

Cannot scan — only 1 of 5 sources represented.

## Spot-checked claims

- *"AI from one-on-one tutoring → multi-agent social learning"* —
  matches Kumar 2026 abstract framing in `sources.md` row #1.
  **Supported.**

## Recommended follow-up NotebookLM prompts

Same as research-hub-managed run — these can be sent into the live
notebook to repair coverage:

1. "Summarize what the *Lim 2025* paper says about embodiment and
   gender similarity-matching in VR."
2. "What does *Lin & Hou 2026* (arXiv:2604.04157) report about memory
   and ToM emergence?"
3. "Summarize the *CoGrid* and *MUG* tools from McDonald 2026."
4. "Explain the *Triadic Loop* framework from Wang 2026."
5. "Compare claims across all 5 papers, citing each by first-author
   surname."

## Verdict

- **Reliable for**: a quick summary of Kumar 2026's two studies.
- **Use with caution for**: anything labelled "the literature on AI
  agents and social interaction" — the brief covers 1/5 of the
  bundle, not 5/5.
- **Do not cite without spot-check**: the cognitive-load and
  self-efficacy claims (line 6 of the brief).
- **Action**: re-prompt NotebookLM with the 4 follow-up prompts above.

## Skill output footer

```
[notebooklm-brief-verifier · Manual fallback mode]
  Brief: brief.txt (305 chars body)
  Sources: sources.md (5 papers parsed from markdown bullet list)
  Cited in brief: 1 / 5
  Missed sources: 4 (Lim, Lin & Hou, McDonald, Wang)
  Unsupported claims: 1 (cognitive-load + self-efficacy line)
  Title/body mismatch: 1 (brief title promises "Embodied AI" but body
                         covers only Kumar)
  Spot-checked: 1 / 1 supported
  Mode: Manual fallback (no research-hub paths used)
```

## Mode parity check

| Result field | research-hub-managed mode (2026-04-25) | Manual fallback mode (2026-04-26) | Parity |
|---|---|---|---|
| Cited in brief | 1 / 5 | 1 / 5 | ✅ |
| Missed sources | 4 (Lim, Lin & Hou, McDonald, Wang) | same 4 | ✅ |
| Unsupported claims | 1 (cognitive-load line) | same 1 | ✅ |
| Spot-checked | 1 / 1 supported | same | ✅ |
| Follow-up prompts | 5 | same 5 | ✅ |

**Conclusion: Manual fallback mode produces identical verification
output to research-hub-managed mode for the same brief + source list.**
The skill is genuinely mode-agnostic — a fresh user who uploads to
NotebookLM directly (no research-hub workspace) gets the same
verification quality.
